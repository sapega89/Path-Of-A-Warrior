"""g.java, part of MpCanvas: options in the record store, text helpers, music and volume.

A mixin of MpCanvas (pow_mp/mp_canvas.py); the methods keep their `# g.java:FROM-TO`
comments. The module names below are set by mp_canvas.py: `MpCanvas` once the class exists,
the others by its _late_imports().
"""
import config
from pow_mp.rt import (
    ByteArrayInputStream,
    DataInputStream,
    RecordStore,
    _arraycopy,
    i8,
    imod,
)

MpCanvas = None   # set by pow_mp/mp_canvas.py
MpGame = None   # set by mp_canvas._late_imports


class OptionsMixin:
    @staticmethod
    def save_options():  # g.java:4740
        record = [0] * (28)
        i = 0
        while i < len(record):
            record[i] = 0
            i = i + 1
        record[0] = i8(MpCanvas.speed)
        record[1] = i8(MpCanvas.volume)
        chars = bytearray(MpCanvas.user_id.encode("latin-1", "replace"))
        i = 0
        while i < len(chars):
            record[(2 + i)] = chars[i]
            i = i + 1
        chars = bytearray(MpCanvas.password.encode("latin-1", "replace"))
        i = 0
        while i < len(chars):
            record[(14 + i)] = chars[i]
            i = i + 1
        try:
            recordStore = RecordStore.openRecordStore("pow_mp_save", True)
            if recordStore.getNumRecords() == 0:
                recordStore.addRecord(record, 0, len(record))
            recordStore.setRecord(1, record, 0, len(record))
        except Exception:
            return

    @staticmethod
    def use_sp_account():
        """PORT-EXTRA (asked by Andrey, config.ALWAYS_ONLINE): one account for the whole game.
        The UserID / password of the single player's Gamevil Live registration
        ("gamevil_pow_regist", pow/game/cloud_save.read_login) log in to the Multiplayer game too,
        so its Login screen (state 2) is not shown; the title logs in with 278 at once. Without
        that registration the Multiplayer game asks as in the original."""
        MpCanvas.sp_account = False
        if not config.ALWAYS_ONLINE:
            return False
        try:
            from pow.game.cloud_save import read_login
            login = read_login()
        except Exception as ex:
            print(f"single player account: {ex!r}")
            return False
        if login is None:
            return False
        MpCanvas.user_id, MpCanvas.password = login
        MpCanvas.sp_account = True
        return True

    def load_options(self):  # g.java:4774
        record = [0] * (28)
        MpCanvas.speed = 0
        MpCanvas.volume = 4
        MpCanvas.user_id = ""
        MpCanvas.password = ""
        try:
            recordStore = RecordStore.openRecordStore("pow_mp_save", False)
            if (recordStore is None) or (recordStore.getNumRecords() < 1):
                return False
            record = recordStore.getRecord(1)
        except Exception:
            pass
        if len(record) >= 28:
            MpCanvas.speed = record[0]
            MpCanvas.volume = record[1]
            MpCanvas.user_id = MpCanvas.cut_at_control(MpCanvas.read_utf(record, 2, 14))
            MpCanvas.password = MpCanvas.cut_at_control(MpCanvas.read_utf(record, 14, 28))
            return True
        return False

    @staticmethod
    def read_utf(data, start, end):  # g.java:4798
        pos = start
        stop = end
        text = None
        try:
            size = (stop - pos)
            buf = [0] * (size + 2)
            utf = buf
            buf[0] = i8((size >> 8) & 0xFF)
            utf[1] = i8(size & 0xFF)
            _arraycopy(data, pos, utf, 2, size)
            byteArrayInputStream = ByteArrayInputStream(utf, 0, len(utf))
            dataInputStream = DataInputStream(byteArrayInputStream)
            text = dataInputStream.readUTF()
            byteArrayInputStream.close()
            dataInputStream.close()
        except Exception:
            pass
        return text

    @staticmethod
    def cut_at_control(text):  # g.java:4819
        i = 0
        size = len(text)
        i = 0
        while i < size:
            if ord(text[i]) < 32:
                break
            i = i + 1
        if i == 0:
            return ""
        return text[0:i]

    def start_music(self, music):  # g.java:6236
        MpCanvas.queue_music(music)

    def start_sound(self, sound):  # g.java:6240
        MpCanvas.queue_music(sound)

    @staticmethod
    def queue_music(music):  # g.java:6244
        if MpCanvas.game is not None:
            MpGame.request_music(music)

    def stop_music(self):  # g.java:6250
        if MpCanvas.game is not None:
            MpCanvas.game.stop_music()

    @staticmethod
    def get_volume():  # g.java:6256
        return MpCanvas.volume

    def volume_down(self):  # g.java:6260
        MpCanvas.volume = imod((((MpCanvas.volume + 6) - 1)), 6)
        self.stop_music()
        if MpCanvas.volume != 0:
            self.start_sound(3)

    def volume_up(self):  # g.java:6268
        MpCanvas.volume = imod(((MpCanvas.volume + 1)), 6)
        self.stop_music()
        if MpCanvas.volume != 0:
            self.start_sound(3)
