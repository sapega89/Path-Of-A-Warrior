"""Binary codec of the original protocol (PHASE_9 task 9.4).

Layout:

    frame    = u16 LE total length (these 2 bytes included) + payload
    C->S     = u16 LE opcode + fields                    (no status byte)
    S->C     = u16 LE opcode + s8 status + fields        (status 1 = OK, < 0 = error code)

Numbers are little-endian, strings are ASCII of a fixed length padded with zeros; the
reader (k.a(int)) stops at the first zero and trims. Fields come from the schemas in
messages.py. Decoding is tolerant like the original client: missing tail fields are left
out (an error answer often has only the status), extra bytes go to "_extra".
"""
import struct

from pow_server import messages as M

_NUM = {"b": 1, "B": 1, "h": 2, "H": 2, "i": 4, "I": 4}


class CodecError(ValueError):
    pass


# --- framing -----------------------------------------------------------------
def frame(payload: bytes) -> bytes:
    n = len(payload) + 2
    if n > 0xFFFF:
        raise CodecError("frame too long: %d" % n)
    return struct.pack("<H", n) + payload


def unframe(data: bytes):
    """Split a byte stream into payloads. Returns (payloads, rest)."""
    out = []
    pos = 0
    while len(data) - pos >= 2:
        n = data[pos] | data[pos + 1] << 8
        if n < 2:
            raise CodecError("bad frame length %d" % n)
        if len(data) - pos < n:
            break
        out.append(bytes(data[pos + 2:pos + n]))
        pos += n
    return out, bytes(data[pos:])


# --- fields --------------------------------------------------------------------
def _put(buf, kind, value):
    if isinstance(kind, int):  # fixed string
        raw = (value or "").encode("ascii", "replace")[:kind]
        buf += raw + b"\0" * (kind - len(raw))
    elif kind in _NUM:
        v = int(value or 0)
        if kind in "bhi":
            lo = -(1 << (8 * _NUM[kind] - 1))
            hi = (1 << (8 * _NUM[kind] - 1)) - 1
        else:
            lo, hi = 0, (1 << (8 * _NUM[kind])) - 1
        if not lo <= v <= hi:
            raise CodecError(f"value {v!r} does not fit {kind}")
        buf += struct.pack("<" + kind, v)
    else:
        raise CodecError(f"unknown field kind {kind!r}")


def _get(data, pos, kind):
    if isinstance(kind, int):
        raw = data[pos:pos + kind]
        if len(raw) < kind:
            raise IndexError
        if raw[:1] == b"\0":
            return "", pos + kind
        return raw.split(b"\0", 1)[0].decode("ascii", "replace").strip(), pos + kind
    size = _NUM[kind]
    if pos + size > len(data):
        raise IndexError
    return struct.unpack_from("<" + kind, data, pos)[0], pos + size


def _encode_fields(buf, schema, msg):
    for item in schema:                 # a count field written before its list = len(rows)
        if item[1] == "list" and isinstance(item[2], str):
            msg = dict(msg, **{item[2]: len(msg.get(item[0]) or [])})
    for item in schema:
        name, kind = item[0], item[1]
        if kind == "list":              # (name, "list", count, subschema); count = int or field name
            count, sub = item[2], item[3]
            rows = msg.get(name) or []
            if isinstance(count, int):
                rows = list(rows) + [None] * (count - len(rows))
                if len(rows) > count:
                    raise CodecError("%s: more than %d rows" % (name, count))
            for row in rows:
                _encode_row(buf, sub, row)
        elif kind == "rest":            # (name, "rest", fn) - custom tail (1028)
            item[2](buf, msg)
        else:
            _put(buf, kind, msg.get(name))


def _encode_row(buf, sub, row):
    if isinstance(sub, (str, int)):   # list of plain values
        _put(buf, sub, row if row is not None else (99 if sub == "B" else 0))
    else:
        _encode_fields(buf, sub, row or {})


def _decode_fields(data, pos, schema, msg):
    for item in schema:
        name, kind = item[0], item[1]
        if kind == "list":
            count, sub = item[2], item[3]
            n = count if isinstance(count, int) else int(msg.get(count, 0))
            rows = []
            for _ in range(n):
                if isinstance(sub, (str, int)):
                    v, pos = _get(data, pos, sub)
                else:
                    v = {}
                    pos = _decode_fields(data, pos, sub, v)
                rows.append(v)
            msg[name] = rows
        elif kind == "rest":
            pos = item[3](data, pos, msg)
        else:
            msg[name], pos = _get(data, pos, kind)
    return pos


# --- messages ------------------------------------------------------------------
def encode(op: int, msg=None, *, to_client: bool) -> bytes:
    """Message -> full frame (length prefix included)."""
    msg = msg or {}
    buf = bytearray(struct.pack("<H", op))
    if to_client:
        _put(buf, "b", msg.get("st", 1))
        schema = M.S2C.get(op, ())
        if msg.get("st", 1) != 1:
            schema = M.S2C_ERR.get(op, ())
    else:
        schema = M.C2S.get(op, ())
    _encode_fields(buf, schema, msg)
    buf += msg.get("_extra", b"")
    return frame(bytes(buf))


def decode(payload: bytes, *, from_client: bool) -> dict:
    """Payload (without the length prefix) -> {"op": .., "st": .., fields..}."""
    if len(payload) < 2:
        raise CodecError("payload shorter than an opcode")
    msg = {"op": payload[0] | payload[1] << 8}
    pos = 2
    if from_client:
        schema = M.C2S.get(msg["op"], ())
    else:
        if len(payload) < 3:
            raise CodecError("server message without status")   # the client would fail too (g(3))
        msg["st"], pos = _get(payload, 2, "b")
        schema = M.S2C.get(msg["op"], ()) if msg["st"] == 1 else M.S2C_ERR.get(msg["op"], ())
    try:
        pos = _decode_fields(payload, pos, schema, msg)
    except IndexError:
        msg["_short"] = True            # tail missing: the original reader would throw here
        return msg
    if pos < len(payload):
        msg["_extra"] = bytes(payload[pos:])
    return msg
