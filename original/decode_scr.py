#!/usr/bin/env python3
"""
Розшифровка .scr файлів (Path of a Warrior J2ME).
Формат: al.java — індексна таблиця (start/end по 2 байти) + блоки рядків у UTF-8.

Використання:
  python decode_scr.py imgui.scr
  python decode_scr.py imgchar.scr --out imgchar_strings.txt
"""

import sys
import struct
from pathlib import Path


def read_uint16_be(data: bytes, offset: int) -> int:
    return (data[offset] & 0xFF) | ((data[offset + 1] & 0xFF) << 8)


def decode_java_modified_utf8(raw: bytes) -> str:
    """Декодує байти як Java Modified UTF-8 (наближено: null = C0 80, інакше як UTF-8)."""
    if not raw:
        return ""
    out = []
    i = 0
    while i < len(raw):
        b = raw[i]
        if b & 0x80 == 0:
            out.append(chr(b))
            i += 1
        elif (b & 0xE0) == 0xC0 and i + 1 < len(raw):
            # 2-byte: 110xxxxx 10xxxxxx
            if b == 0xC0 and raw[i + 1] == 0x80:
                out.append("\u0000")  # Java null
                i += 2
            else:
                try:
                    out.append(raw[i : i + 2].decode("utf-8"))
                except UnicodeDecodeError:
                    out.append("\ufffd")
                i += 2
        elif (b & 0xF0) == 0xE0 and i + 2 < len(raw):
            try:
                out.append(raw[i : i + 3].decode("utf-8"))
            except UnicodeDecodeError:
                out.append("\ufffd")
            i += 3
        else:
            out.append("\ufffd")
            i += 1
    return "".join(out)


def decode_scr(path: str) -> list[tuple[int, str]]:
    path = Path(path)
    data = path.read_bytes()
    n = len(data)
    if n < 6:
        return []

    # Як у al.java: i = 2 + paramInt*2 (у коді — по 2 байти на "слово", кожен запис = 4 байти)
    # Тобто для індексу 0: j,k з байтів 2,3,4,5; для 1: 4,5,6,7; для 2: 6,7,8,9...
    results = []
    index = 0
    while True:
        i = 2 + index * 2
        if i + 4 > n:
            break
        j = read_uint16_be(data, i)
        k = read_uint16_be(data, i + 2)
        if j < 0 or k > n or j >= k:
            break
        raw = data[j:k]
        try:
            s = decode_java_modified_utf8(raw)
        except Exception:
            s = raw.decode("utf-8", errors="replace")
        results.append((index, s))
        index += 1
    return results


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    scr_path = sys.argv[1]
    out_path = None
    if "--out" in sys.argv:
        idx = sys.argv.index("--out")
        if idx + 1 < len(sys.argv):
            out_path = sys.argv[idx + 1]

    try:
        entries = decode_scr(scr_path)
    except FileNotFoundError:
        print(f"Файл не знайдено: {scr_path}", file=sys.stderr)
        sys.exit(1)

    lines = []
    for idx, s in entries:
        line = f"{idx}\t{s}"
        lines.append(line)
        print(line)

    if out_path:
        Path(out_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"\nЗаписано {len(entries)} рядків у {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
