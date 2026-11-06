extends RefCounted
## One connection to the game's server (scripts/net/protocol.gd): ENet with DTLS, the
## server's certificate checked against the one the game was given. poll() every frame;
## request() sends a dictionary and calls `done` with the answer (requests made while still
## connecting go out once connected). When the connection fails or drops, every waiting
## request gets {"ok": false, "err": "offline"}.

const Protocol := preload("res://scripts/net/protocol.gd")

enum State { CLOSED, CONNECTING, CONNECTED }

const CONNECT_TIMEOUT_MS := 10000

var state := State.CLOSED
var host: ENetConnection
var peer: ENetPacketPeer
var _next_q := 1
var _waiting := {}  # q -> [request, done]
var _queued: Array[int] = []  # q of requests not sent yet
var _started := 0


## Starts connecting; OK, or the error of the DTLS setup.
func open(address: String, port: int, cert: X509Certificate, common_name := "localhost") -> int:
	close()
	host = ENetConnection.new()
	var err := host.create_host(1, Protocol.CHANNELS)
	if err == OK:
		err = host.dtls_client_setup(common_name, TLSOptions.client(cert, common_name))
	if err != OK:
		host.destroy()
		host = null
		return err
	peer = host.connect_to_host(address, port, Protocol.CHANNELS)
	if peer == null:
		host.destroy()
		host = null
		return ERR_CANT_CONNECT
	state = State.CONNECTING
	_started = Time.get_ticks_msec()
	return OK


func close() -> void:
	if host != null:
		if peer != null and state == State.CONNECTED:
			peer.peer_disconnect_now()
		host.destroy()
	host = null
	peer = null
	_lost()


func _lost() -> void:
	state = State.CLOSED
	var waiting := _waiting
	_waiting = {}
	_queued.clear()
	for q in waiting:
		var done: Callable = waiting[q][1]
		done.call({"t": waiting[q][0].get("t", "?"), "ok": false, "err": "offline", "q": q})


func request(msg: Dictionary, done: Callable = func(_r: Dictionary) -> void: pass) -> void:
	var q := _next_q
	_next_q += 1
	msg = msg.duplicate()
	msg["q"] = q
	if state == State.CLOSED:
		done.call({"t": msg.get("t", "?"), "ok": false, "err": "offline", "q": q})
		return
	_waiting[q] = [msg, done]
	if state == State.CONNECTED:
		_send(msg)
	else:
		_queued.append(q)


func _send(msg: Dictionary) -> void:
	peer.send(0, Protocol.encode(msg), ENetPacketPeer.FLAG_RELIABLE)


func poll(wait_ms := 0) -> void:
	if host == null:
		return
	if state == State.CONNECTING and Time.get_ticks_msec() - _started > CONNECT_TIMEOUT_MS:
		close()
		return
	var ev: Array = host.service(wait_ms)
	while host != null and ev[0] != ENetConnection.EVENT_NONE:
		match ev[0]:
			ENetConnection.EVENT_CONNECT:
				state = State.CONNECTED
				for q in _queued:
					_send(_waiting[q][0])
				_queued.clear()
			ENetConnection.EVENT_DISCONNECT, ENetConnection.EVENT_ERROR:
				close()
				return
			ENetConnection.EVENT_RECEIVE:
				var reply := Protocol.decode(ev[1].get_packet())
				var q: Variant = reply.get("q")
				if q is int and _waiting.has(q):
					var done: Callable = _waiting[q][1]
					_waiting.erase(q)
					done.call(reply)
		if host == null:
			return  # an answer closed the connection
		ev = host.service(0)
