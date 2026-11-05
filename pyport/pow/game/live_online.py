"""(asked by Andrey): "always online" (config.ALWAYS_ONLINE).

The original connected to Live only inside Game Menu > Live (popup 2 "Connect to
Live?", "Connecting...", login 530) and closed the connection on leaving it. Here:

- Continue and New Game log in at once with the account of "pow_regist", in the
  background: no popup, no "Connecting...", no locked keys. Errors stay silent (the game is just
  offline) and the login is tried again later, up to every RETRY_MAX_MS.
- Live / Warehouse open at once: no popup 2, and over the open connection no
  "Connecting..." unless an answer takes longer than QUIET_MS (Live.quiet_request()).
- The connection stays after leaving Live; a 530 every KEEPALIVE_MS keeps the server
  (pow_server/ws_server.py IDLE_TIMEOUT 300 s) from closing it. When it breaks, the next
  Live request logs in again by itself (as.l(): a request without a connection sends 530 first).
- A hero without an account gets the registration screen once on the Game Menu (after the
  prologue of a New Game, after Continue unless the player skipped it before): BACK on the empty
  UserID skips it, and a skip on Continue is remembered in SKIP_STORE.
- Server only (cloud_save.server_only(), asked by Andrey): the hero is kept only on the server,
  so it must have an account. The registration screen is offered after every Continue / New Game
  of a hero without one and cannot be skipped: BACK closes it and it opens again at once.

Live itself (live.py) is unchanged apart from the guards marked `Online` there.
"""
import config
from pow.game.game_canvas import GameCanvas
from pow.game.live_net import LiveNet
from pow.midp import system

KEEPALIVE_MS = 240000
RETRY_MS = 30000
RETRY_MAX_MS = 300000
SKIP_STORE = "pow_online_skip"   # one record: the player skipped the registration offer


class Online:
    QUIET_MS = 1500         # a request over the open connection: "Connecting..." only after this
    wanted = False          # the game started (Continue / New Game): stay logged in
    logged_in = False       # the background 530 was answered with status 1
    background = False      # the request in flight is ours, not the screen's
    offer = False           # show the registration screen on the next Game Menu frame
    offer_open = False      # the registration screen was opened by the offer
    next_try = 0            # ms: the next background login
    retry_ms = RETRY_MS
    last_sent = 0           # ms: the last background 530
    attempts = 0            # background 530s sent (tools/shot.py `logins`)
    mp_pending = False      # Main Menu > Multiplayer > YES: open Live > Multiplayer on
                            # the next free Game Menu frame (popups.py)

    @staticmethod
    def enabled():
        return config.ALWAYS_ONLINE

    @staticmethod
    def must_register():
        """Server only: no hero without an account (the save lives on the server)."""
        from pow.game import cloud_save
        return config.ALWAYS_ONLINE and cloud_save.server_only()

    @staticmethod
    def on_game_start(new_game=False):
        """Continue loaded the save / New Game created the hero."""
        if not config.ALWAYS_ONLINE:
            return
        from pow.game.live_screen import LiveScreen
        Online.wanted = True
        Online.next_try = 0
        Online.retry_ms = RETRY_MS
        if not LiveScreen.is_registered():
            Online.offer = new_game or Online.must_register() or not Online.skipped()

    @staticmethod
    def skipped():
        try:
            from pow.midp.rms import RecordStore
            rs = RecordStore.openRecordStore(SKIP_STORE, False)
            return rs is not None and rs.getNumRecords() > 0
        except Exception:
            return False

    @staticmethod
    def remember_skip():
        try:
            from pow.midp.rms import RecordStore
            rs = RecordStore.openRecordStore(SKIP_STORE, True)
            if rs.getNumRecords() == 0:
                rs.addRecord(bytearray(1), 0, 1)
        except Exception:
            pass

    @staticmethod
    def on_registration_closed(registered):
        """The offered registration screen closed: registered, or BACK on the empty UserID."""
        Online.offer_open = False
        if registered:
            Online.wanted = True
            Online.logged_in = True
            Online.last_sent = system.currentTimeMillis()
        elif Online.must_register():
            Online.offer = True              # no skip: the screen opens again
        else:
            Online.remember_skip()

    @staticmethod
    def _game_menu_free():
        return (GameCanvas.state == 2 and GameCanvas.menu[0] == 0 and not GameCanvas.in_live
                and GameCanvas.popups.kind == 0)

    @staticmethod
    def tick(live):
        """Every frame from Live.tick_live, before the screen's own requests."""
        from pow.game.live import Live
        if not config.ALWAYS_ONLINE or not Online.wanted:
            return
        if Online.background:
            return                           # check_answer() ends it
        if GameCanvas.in_live or Live.waiting or Live.pending_request != -1:
            return                           # Live is on the screen: it owns the network
        from pow.game.live_screen import LiveScreen
        if Online.offer:
            if Online._game_menu_free():
                Online.offer = False
                Online.offer_open = True
                live.open_registration()
            return
        if Online.mp_pending and Online._game_menu_free():   # Main Menu > Multiplayer > YES
            Online.mp_pending = False
            Live.auto_mp = True
            live.open_live()
            return
        if not LiveScreen.is_registered():
            return
        now = system.currentTimeMillis()
        if Online.logged_in and LiveNet.connected:
            if now - Online.last_sent < KEEPALIVE_MS:
                return
        else:                                # offline, or the last login was refused: back off
            Online.logged_in = False
            if now < Online.next_try:
                return
            Online.next_try = now + Online.retry_ms
            Online.retry_ms = min(RETRY_MAX_MS, Online.retry_ms * 2)
        Online.login(live)

    @staticmethod
    def login(live):
        """530 without the screen, with the stored UserID / password."""
        from pow.game.live import Live
        Live.screen.load_login()
        if not Live.user_id or not Live.password:
            return
        Online.background = True
        Online.attempts += 1
        Online.last_sent = system.currentTimeMillis()
        Live.reg_from_popup = False
        Live.answer_op = 0
        live.queue_request(530)

    @staticmethod
    def on_login_answer(ok):
        """531 (or its error / timeout / a failed connection) of the background login."""
        Online.background = False
        Online.logged_in = ok
        if ok:
            Online.retry_ms = RETRY_MS
