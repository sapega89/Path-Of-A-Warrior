"""the single player's save kept on the server (pow_server/cloud.py,
pow/game/cloud_save.py)."""
import base64
import json

import pytest

import config
from pow.game import cloud_save
from pow.midp import rms
from pow.midp.rms import RecordStore
from pow_server.cloud import MAX_STORE, CloudServer
from pow_server.storage import open_storage


class FakeSocket:
    """A TextSocket wired straight to an in-process CloudServer."""
    server = None
    down = False

    def __init__(self, url):
        self.connected = self.failed = False
        self.inbox = []

    def open(self):
        if FakeSocket.down:
            self.failed = True
            return
        self.session = FakeSocket.server.connect(lambda text: self.inbox.append(text))   # noqa: PLW0108 (self.inbox is replaced later)
        self.connected = True

    def send(self, text):
        self.session.receive(text)

    def poll(self):
        out, self.inbox = self.inbox, []
        return out

    def close(self):
        self.connected = False


@pytest.fixture
def server(monkeypatch):
    st = open_storage()
    st.create_account("ANDREY", "1234")
    FakeSocket.server = CloudServer(st)
    monkeypatch.setattr(rms, "on_write", [])
    monkeypatch.setattr(FakeSocket, "down", False)
    return FakeSocket.server


class Device:
    """One computer / browser: its own save folder."""

    def __init__(self, tmp_path, name, monkeypatch, clock):
        self.dir = str(tmp_path / name)
        self.monkeypatch = monkeypatch
        self.clock = clock
        self.sync = None

    def use(self):
        self.monkeypatch.setattr(config, "SAVE_DIR", self.dir)
        self.monkeypatch.setattr(rms, "on_write", [self.sync.on_write] if self.sync else [])
        return self

    def start(self):
        self.use()
        self.sync = cloud_save.CloudSync("ws://x/save", make_socket=FakeSocket, clock=self.clock)
        self.sync.request_restart = lambda: setattr(self.sync, "restart_requested", True)
        rms.on_write[:] = [self.sync.on_write]
        return self

    def register(self, uid="ANDREY", pwd="1234"):
        rec = bytearray(28)
        rec[0:len(pwd)] = pwd.encode()
        rec[12:12 + len(uid)] = uid.encode()
        rs = RecordStore.openRecordStore("gamevil_pow_regist", True)
        if rs.getNumRecords() == 0:
            rs.addRecord(rec, 0, 28)
        rs.setRecord(1, rec, 0, 28)

    def save_hero(self, data):
        rs = RecordStore.openRecordStore("gamevil_pow_data", True)
        if rs.getNumRecords() == 0:
            rs.addRecord(data, 0, len(data))
        rs.setRecord(1, data, 0, len(data))

    def hero(self):
        try:
            return bytes(RecordStore.openRecordStore("gamevil_pow_data", False).getRecord(1))
        except rms.RecordStoreException:
            return None

    def steps(self, n=4):
        for _ in range(n):
            self.sync.step()


@pytest.fixture
def clock():
    t = [1_000_000]

    def now():
        t[0] += 1000
        return t[0]
    return now


def server_hero(server):
    e = server.storage.saves_get("ANDREY")["gamevil_pow_data"]
    return base64.b64decode(e["records"][0]), e["rev"]


# --- the server ---------------------------------------------------------------------------
def talk(server, *msgs):
    out = []
    s = server.connect(out.append)
    for m in msgs:
        s.receive(json.dumps(m))
    return [json.loads(x) for x in out]


def test_server_login_get_put_conflict(server):
    rec = base64.b64encode(b"hero").decode()
    a = talk(server, {"op": "get"}, {"op": "login", "id": "NOBODY", "pwd": "1234"},
             {"op": "login", "id": "ANDREY", "pwd": "9999"})
    assert [x.get("err") for x in a] == ["login first", "no account", "password"]
    a = talk(server, {"op": "login", "id": "ANDREY", "pwd": "1234"},
             {"op": "put", "store": "gamevil_pow_data", "base": 0, "at": 5, "records": [rec]},
             {"op": "put", "store": "gamevil_pow_data", "base": 0, "at": 6, "records": [rec]},
             {"op": "put", "store": "gamevil_pow_regist", "base": 0, "at": 6, "records": [rec]},
             {"op": "put", "store": "gamevil_pow_env", "base": 0, "at": 6,
              "records": [base64.b64encode(bytes(MAX_STORE + 1)).decode()]},
             {"op": "get"})
    assert a[0]["ok"] and a[1] == {"op": "put", "ok": True, "store": "gamevil_pow_data", "rev": 1}
    assert a[2]["err"] == "conflict" and a[2]["current"]["rev"] == 1 and a[2]["current"]["at"] == 5
    assert a[3]["err"] == "bad store" and a[4]["err"] == "too big"
    assert a[5]["stores"] == {"gamevil_pow_data": {"rev": 1, "at": 5, "records": [rec]}}


def test_server_url_from_live(monkeypatch):
    monkeypatch.setattr(config, "SAVE_SERVER", "auto")
    monkeypatch.setattr(config, "LIVE_SERVER", "local")
    assert cloud_save.server_url() is None
    monkeypatch.setattr(config, "LIVE_SERVER", "wss://pow.example:28200/live")
    assert cloud_save.server_url() == "wss://pow.example:28200/save"
    monkeypatch.setattr(config, "SAVE_SERVER", "off")
    assert cloud_save.server_url() is None


# --- the client ---------------------------------------------------------------------------
def test_nothing_sent_without_a_registration(server, tmp_path, monkeypatch, clock):
    a = Device(tmp_path, "a", monkeypatch, clock).start()
    a.save_hero(b"A1")
    a.steps()
    assert a.sync.sock is None and server.storage.saves_get("ANDREY") == {}


def test_second_device_gets_the_hero(server, tmp_path, monkeypatch, clock):
    a = Device(tmp_path, "a", monkeypatch, clock).start()
    a.save_hero(b"hero of A")
    a.register()                       # Gamevil Live registration on the first computer
    a.steps()
    assert server_hero(server) == (b"hero of A", 1)
    a.save_hero(b"hero of A, later")
    a.steps()
    assert server_hero(server) == (b"hero of A, later", 2)

    b = Device(tmp_path, "b", monkeypatch, clock).start()
    b.sync.started = True              # the game runs with B's own new hero
    b.save_hero(b"new hero of B")
    b.register()                       # the same account on the second computer
    b.steps()
    assert b.hero() == b"hero of A, later"     # the server's copy won
    assert b.sync.restart_requested            # the hero in memory was B's
    backup = json.loads(rms._load_raw("gamevil_pow_data_backup"))
    assert base64.b64decode(backup[0]) == b"new hero of B"
    assert server_hero(server) == (b"hero of A, later", 2)   # B's hero did not overwrite it


def test_boot_takes_the_newer_copy(server, tmp_path, monkeypatch, clock):
    a = Device(tmp_path, "a", monkeypatch, clock).start()
    a.register()
    a.save_hero(b"A1")
    a.steps()
    b = Device(tmp_path, "b", monkeypatch, clock).start()
    b.register()
    b.steps()
    assert b.hero() == b"A1"
    b.save_hero(b"B2")
    b.steps()
    assert server_hero(server) == (b"B2", 2)

    a.start()                          # A starts the game again: B's later save comes over
    a.steps()
    assert a.hero() == b"B2" and not a.sync.restart_requested
    # A plays offline, then B saves too, later; A's next start keeps B's (newer) one
    FakeSocket.down = True
    a.start()
    a.save_hero(b"A3 offline")
    a.steps()
    FakeSocket.down = False
    b.start()
    b.save_hero(b"B4")
    b.steps()
    a.start()
    a.steps()
    assert a.hero() == b"B4"
    assert base64.b64decode(json.loads(rms._load_raw("gamevil_pow_data_backup"))[0]) == b"A3 offline"


def test_offline_play_is_sent_on_the_next_start(server, tmp_path, monkeypatch, clock):
    a = Device(tmp_path, "a", monkeypatch, clock).start()
    a.register()
    a.save_hero(b"A1")
    a.steps()
    FakeSocket.down = True             # the server is down: A saves only locally
    a.start()
    a.save_hero(b"A2 offline")
    a.steps()
    FakeSocket.down = False
    a.start()
    a.steps()
    assert server_hero(server) == (b"A2 offline", 2)
    # a save written while the server saves were off (no CloudSync running) is sent too
    a.sync = None
    a.use()
    a.save_hero(b"A3 untracked")
    a.start()
    a.steps()
    assert server_hero(server) == (b"A3 untracked", 3)


def test_conflict_while_playing_keeps_this_device(server, tmp_path, monkeypatch, clock):
    a = Device(tmp_path, "a", monkeypatch, clock).start()
    a.register()
    a.save_hero(b"A1")
    a.steps()
    b = Device(tmp_path, "b", monkeypatch, clock).start()
    b.register()
    b.steps()
    b.save_hero(b"B2")
    b.steps()                          # server rev 2 while A is still connected at rev 1
    a.use()
    a.save_hero(b"A3")
    a.steps()
    assert server_hero(server) == (b"A3", 3)
    assert base64.b64decode(json.loads(rms._load_raw("gamevil_pow_data_backup"))[0]) == b"B2"


def test_wrong_password_stops_until_a_new_registration(server, tmp_path, monkeypatch, clock):
    a = Device(tmp_path, "a", monkeypatch, clock).start()
    a.register(pwd="9999")
    a.save_hero(b"A1")
    a.steps()
    assert a.sync.state == "off" and server.storage.saves_get("ANDREY") == {}
    a.register(pwd="1234")
    a.steps()
    assert server_hero(server) == (b"A1", 1)


# --- server only (config.SERVER_ONLY_SAVE) --------------------------------------------------
@pytest.fixture
def memory_only(monkeypatch):
    monkeypatch.setattr(rms, "memory_only", set())
    monkeypatch.setattr(rms, "memory", {})


def start_server_only(device):
    device.start()
    device.sync.server_only = True
    device.sync.purge = cloud_save.use_memory_only()
    return device


def on_disk(device, name="gamevil_pow_data"):
    import os
    return os.path.isfile(os.path.join(device.dir, name + ".rms.json"))


def test_server_only_never_writes_the_hero_to_the_device(server, tmp_path, monkeypatch, clock, memory_only):
    a = start_server_only(Device(tmp_path, "a", monkeypatch, clock))
    a.register()
    a.save_hero(b"A1")
    a.steps()
    assert server_hero(server) == (b"A1", 1)
    assert a.hero() == b"A1" and not on_disk(a)
    assert on_disk(a, "gamevil_pow_regist")          # the account stays on the device


def test_server_only_boot_takes_the_server_copy(server, tmp_path, monkeypatch, clock, memory_only):
    a = start_server_only(Device(tmp_path, "a", monkeypatch, clock))
    a.register()
    a.save_hero(b"A1")
    a.steps()
    rms.memory.clear()                                # the game closed: nothing kept
    a = start_server_only(a)
    assert a.hero() is None
    a.steps()
    assert a.sync.online and a.hero() == b"A1" and not a.sync.restart_requested


def test_server_only_moves_the_old_device_save_to_the_server(server, tmp_path, monkeypatch, clock, memory_only):
    a = Device(tmp_path, "a", monkeypatch, clock).start()
    a.register()
    FakeSocket.down = True
    a.save_hero(b"old local hero")                  # before "server only": on the device
    a.steps()
    FakeSocket.down = False
    assert on_disk(a)
    a = start_server_only(a)
    assert a.hero() == b"old local hero"
    a.steps(6)
    assert server_hero(server) == (b"old local hero", 1)
    assert not on_disk(a)                           # off the device once the server has it


def test_server_only_server_copy_wins_over_an_old_device_save(server, tmp_path, monkeypatch, clock, memory_only):
    b = Device(tmp_path, "b", monkeypatch, clock).start()
    b.register()
    b.save_hero(b"hero on the server")
    b.steps()
    a = Device(tmp_path, "a", monkeypatch, clock).start()
    a.register()
    FakeSocket.down = True
    a.save_hero(b"edited local hero")               # a later, edited copy on the device
    a.steps()
    FakeSocket.down = False
    a = start_server_only(a)
    a.steps(6)
    assert a.hero() == b"hero on the server"
    assert server_hero(server) == (b"hero on the server", 1)
    assert not on_disk(a)


def test_server_only_offline_is_not_online(server, tmp_path, monkeypatch, clock, memory_only):
    FakeSocket.down = True
    a = start_server_only(Device(tmp_path, "a", monkeypatch, clock))
    a.steps()
    assert not a.sync.online                        # no account: the server must still answer
    a.register()
    a.steps()
    assert not a.sync.online
    FakeSocket.down = False
    a.sync.retry_now()
    a.steps()
    assert a.sync.online


def test_server_only_no_account_needs_the_server(server, tmp_path, monkeypatch, clock, memory_only):
    a = start_server_only(Device(tmp_path, "a", monkeypatch, clock))
    a.steps()
    assert a.sync.online and a.sync.sock is None    # the server answered; nothing to send
    a.save_hero(b"new hero")
    a.register()                                   # the registration the game asks for
    a.steps()
    assert server_hero(server) == (b"new hero", 1) and not on_disk(a)


def test_server_only_switch(monkeypatch):
    monkeypatch.setattr(config, "LIVE_SERVER", "local")
    monkeypatch.setattr(config, "SAVE_SERVER", "auto")
    monkeypatch.setattr(config, "SERVER_ONLY_SAVE", True)
    assert not cloud_save.server_only()             # the in-game server: the save on the device
    monkeypatch.setattr(config, "LIVE_SERVER", "wss://pow.example/live")
    assert cloud_save.server_only()
    monkeypatch.setattr(config, "SERVER_ONLY_SAVE", False)
    assert not cloud_save.server_only()
