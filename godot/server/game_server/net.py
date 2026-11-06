"""The WebSocket side: one Session per connection, text messages only, limits from security.py."""
import asyncio
import logging

import websockets

from game_server import protocol
from game_server.security import Guard, peer_address
from game_server.server import Session
from game_server.storage import Storage

log = logging.getLogger("game_server")
IDLE_TIMEOUT = 300.0


async def handle(ws, storage, guard, behind_proxy=False):
    peer = peer_address(ws, behind_proxy)
    if not guard.open_connection(peer):
        await ws.close(1013, "too many connections")
        return
    session = Session(storage, guard, peer)
    meter = guard.meter()
    try:
        while True:
            try:
                text = await asyncio.wait_for(ws.recv(), IDLE_TIMEOUT)
            except asyncio.TimeoutError:
                break
            if not isinstance(text, str):
                break
            if not meter.allow():
                log.info("%s: too many messages", peer)
                break
            await ws.send(session.handle(text))
    except websockets.ConnectionClosed:
        pass
    finally:
        guard.close_connection(peer)


async def serve(host, port, db, behind_proxy=False, ready=None):
    storage = Storage(db)
    guard = Guard()
    async with websockets.serve(lambda ws: handle(ws, storage, guard, behind_proxy), host, port,
                                max_size=protocol.MAX_MESSAGE) as server:
        log.info("listening on %s:%d", host, port)
        if ready is not None:
            ready.set_result(server)
        await asyncio.Future()
