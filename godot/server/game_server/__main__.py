"""python -m game_server [--host 0.0.0.0] [--port 28300] [--db heroes.sqlite] [--behind-proxy]

ws://host:port/ ; behind a TLS proxy (Caddy, nginx) the game uses wss://."""
import argparse
import asyncio
import logging

from game_server.net import serve


def main(argv=None):
    ap = argparse.ArgumentParser(prog="game_server")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=28300)
    ap.add_argument("--db", default="heroes.sqlite", help='SQLite file (":memory:" keeps nothing)')
    ap.add_argument("--behind-proxy", action="store_true",
                    help="the address of a player is the last X-Forwarded-For entry")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")
    asyncio.run(serve(args.host, args.port, args.db, args.behind_proxy))


if __name__ == "__main__":
    main()
