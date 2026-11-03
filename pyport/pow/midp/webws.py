"""PORT-EXTRA: a WebSocket of the browser page for the pygbag build.

pygbag 0.9's JS bridge (`platform.window`) has no `WebSocket.new(...)` (that is pyodide's), and a
Python function set as `ws.onmessage` is never called. So the socket lives on the JS side: a small
helper (window.__powws, put into the page by eval) keeps each socket's state and received
messages, and the game polls it once per tick, as it polls the desktop `websockets` queue.

    sock = BrowserSocket("wss://host/live", binary=True)
    sock.connected / sock.failed     (read from the page each time)
    sock.recv() -> [bytes or str, ...] received since the last call
    sock.send(bytes or str)

Binary messages cross the bridge as base64 text, the list as one JSON string.
"""
import base64
import json

_HELPER = r"""(function () {
  if (window.__powws) return 1;
  var socks = {}, next = 1;
  window.__powws = {
    open: function (url, binary) {
      var id = next++, s = {ws: null, inbox: [], state: 0};
      socks[id] = s;
      try {
        var ws = new WebSocket(url);
        if (binary) ws.binaryType = 'arraybuffer';
        s.ws = ws;
        ws.onopen = function () { if (s.state === 0) s.state = 1; };
        ws.onmessage = function (ev) {
          if (typeof ev.data === 'string') { s.inbox.push('t' + ev.data); return; }
          var b = new Uint8Array(ev.data), t = '';
          for (var i = 0; i < b.length; i++) t += String.fromCharCode(b[i]);
          s.inbox.push('b' + btoa(t));
        };
        ws.onclose = ws.onerror = function () { s.state = 2; };
      } catch (e) { s.state = 2; }
      return id;
    },
    state: function (id) { return socks[id] ? socks[id].state : 2; },
    recv: function (id) {
      var s = socks[id];
      if (!s || !s.inbox.length) return '';
      var out = JSON.stringify(s.inbox);
      s.inbox = [];
      return out;
    },
    send: function (id, kind, data) {
      var s = socks[id];
      if (!s || s.state !== 1) return 0;
      if (kind === 'b') {
        var t = atob(data), b = new Uint8Array(t.length);
        for (var i = 0; i < t.length; i++) b[i] = t.charCodeAt(i);
        s.ws.send(b);
      } else {
        s.ws.send(data);
      }
      return 1;
    },
    close: function (id) {
      var s = socks[id];
      if (s) { try { if (s.ws) s.ws.close(); } catch (e) {} s.state = 2; delete socks[id]; }
      return 1;
    }
  };
  return 1;
})()"""

_ready = False


def _js(code):
    global _ready
    import platform  # pygbag: the JS bridge
    if not _ready:
        platform.window.eval(_HELPER)
        _ready = True
    return platform.window.eval(code)


class BrowserSocket:
    def __init__(self, url, binary):
        self.id = int(_js("window.__powws.open(%s, %s)" % (json.dumps(str(url)), "true" if binary else "false")))

    def _state(self):
        if self.id is None:
            return 2
        return int(_js("window.__powws.state(%d)" % self.id))

    @property
    def connected(self):
        return self._state() == 1

    @property
    def failed(self):
        return self._state() == 2

    def recv(self):
        if self.id is None:
            return []
        raw = _js("window.__powws.recv(%d)" % self.id)
        if not raw:
            return []
        return [base64.b64decode(m[1:]) if m[0] == "b" else m[1:] for m in json.loads(str(raw))]

    def send(self, data):
        if self.id is None:
            return False
        if isinstance(data, (bytes, bytearray)):
            kind, text = "b", base64.b64encode(bytes(data)).decode("ascii")
        else:
            kind, text = "t", str(data)
        return bool(_js("window.__powws.send(%d, %s, %s)" % (self.id, json.dumps(kind), json.dumps(text))))

    def close(self):
        if self.id is not None:
            try:
                _js("window.__powws.close(%d)" % self.id)
            except Exception:
                pass
            self.id = None
