"""A scripted player for trying Challenge / Invite An Ally alone (PHASE_9): it logs in like a
client, accepts every invitation (Options > Invitation: Accept) and plays its battles with
plain attacks. tools/mp_shot.py uses it (`bot` steps); `python -m pow_server --bot NAME` keeps
one online on a server."""
import random

from pow_server import codec_bin
from pow_server import messages as M


class Bot:
    def __init__(self, server, uid, pwd="0000", hit=(40, 88), rng=None):   # noqa: S107 (bot accounts)
        self.server, self.uid = server, uid
        self.hit = hit
        self.rng = rng or random.Random(1)
        self.inbox = []
        self.results = []                  # every 1032 it got
        s = server.connect(self._recv)
        s.receive(self._frame(M.LOGIN_FIRST, id=uid, pwd=pwd, ver=M.GAME_VER))
        ans = self.inbox.pop() if self.inbox else {}
        if ans.get("st") != 1:
            raise ValueError(f"bot {uid}: login refused ({ans})")
        token = ans["token"]
        s.close()
        self.session = server.connect(self._recv)
        self._send(M.LOGIN, id=uid, ver=M.GAME_VER, token=token)
        self.inbox.clear()

    @staticmethod
    def _frame(op, **fields):
        return codec_bin.unframe(codec_bin.encode(op, fields, to_client=False))[0][0]

    def _recv(self, frame):
        self.inbox.extend(codec_bin.decode(p, from_client=False) for p in codec_bin.unframe(frame)[0])

    def _send(self, op, **fields):
        self.session.receive(self._frame(op, **fields))

    def invite(self, uid, mode=0):
        self._send(M.INVITE, mode=mode, id=uid)

    def pump(self):
        """Answer what came in, like a client that never waits on the screen."""
        while self.inbox:
            m = self.inbox.pop(0)
            op = m["op"]
            if op in (M.ALL_READY, M.TURN_RESULT):
                self._send(M.ROUND_READY)
            elif op == M.ROUND_START:
                room = self.session.room
                me = self.session.slot
                foes = [s for s, f in room.battle.fighters.items() if f.alive and f.team != me % 2]
                self._send(M.TURN, target=foes[0] if foes else 1, action=0,
                           hit=self.rng.randint(*self.hit))
            elif op == M.STAGE_END:
                self._send(M.STAGE_NEXT)
            elif op == M.STAGE_INFO:
                self._send(M.STAGE_INTRO_DONE)
            elif op == M.BATTLE_END:
                self.results.append(m)
            elif op == M.CHAT_PUSH and m.get("channel") == 2 and m.get("id") != self.uid:
                # PORT-EXTRA chat: a private message gets one of the bots' lines back
                from pow_server import chat
                self._send(M.CHAT_SEND, channel=2, peer=m["id"], text=self.rng.choice(chat.BOT_LINES))
