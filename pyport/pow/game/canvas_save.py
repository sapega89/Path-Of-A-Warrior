"""ag.java, part of GameCanvas: the save file: load / save gamevil_pow_data, options, byte readers and writers.

A mixin of GameCanvas (pow/game/game_canvas.py); the methods keep their `# ag.java:FROM-TO`
comments. `GameCanvas` below is the real class, set by game_canvas.py once it exists.
"""

import config
from pow.game.structs import Item
from pow.midp.jint import i8, i16, i32, idiv
from pow.midp.rms import RecordStore

GameCanvas = None   # set by pow/game/game_canvas.py


class SaveMixin:
    @staticmethod
    def load_options():  # ag.java:1174-1186
        record = bytearray(2)
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_env", False)
            if recordStore is None or recordStore.getNumRecords() < 1:
                return
            record = recordStore.getRecord(1)
            GameCanvas.save_pos = len(record)
        except Exception:
            pass
        if GameCanvas.save_pos >= 2:
            GameCanvas.volume = i8(record[0])
            GameCanvas.speed = i8(record[1])

    @staticmethod
    def save_options():  # ag.java:1188-1201
        record = bytearray(2)
        record[0] = GameCanvas.volume & 0xFF
        record[1] = GameCanvas.speed & 0xFF
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_env", True)
            if recordStore.getNumRecords() == 0:
                recordStore.addRecord(record, 0, len(record))
            recordStore.setRecord(1, record, 0, len(record))
        except Exception:
            return

    def load_game(self):  # ag.java:2126-2214  (load save "gamevil_pow_data")
        hero = GameCanvas.hero
        GameCanvas.save_pos = 0
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_data", False)
            if recordStore is None or recordStore.getNumRecords() < 1:
                return
            GameCanvas.save_buf = recordStore.getRecord(1)
            GameCanvas.save_pos = GameCanvas.save_buf[0] & 0xFF | GameCanvas.save_buf[1] << 8 & 0xFF00
        except Exception:
            pass
        save_end = GameCanvas.save_pos
        if GameCanvas.save_pos != 0:
            buf = GameCanvas.save_buf
            reserved = [0] * 16
            name_len = 0
            while name_len < 8 and buf[2 + name_len] != 32:
                name_len += 1
            name_utf = bytearray(name_len)
            for i in range(name_len):
                name_utf[i] = buf[2 + i]
            hero.name = GameCanvas.read_utf(name_utf, 0, name_len)
            GameCanvas.save_flag = i8(buf[18])
            GameCanvas.save_pos = 19
            GameCanvas.lord = GameCanvas.read_byte()
            GameCanvas.mission = GameCanvas.read_byte()
            GameCanvas.rooms_visited = GameCanvas.read_byte()
            GameCanvas.missions_done = GameCanvas.read_long()
            GameCanvas.lords_done = GameCanvas.read_long()
            for i in range(8):
                GameCanvas.stats[i] = GameCanvas.read_int()
            GameCanvas.mission_exp = GameCanvas.read_int()
            GameCanvas.score = GameCanvas.read_int()
            for i in range(44):
                GameCanvas.generals[0][i] = GameCanvas.read_byte()
                GameCanvas.generals[1][i] = GameCanvas.read_byte()
            GameCanvas.general_count = GameCanvas.read_byte()
            for i in range(25):
                GameCanvas.shop[i] = self.read_item()
            GameCanvas.chapter = GameCanvas.read_byte()
            hero.pos[0].x = GameCanvas.read_short()
            hero.pos[0].y = GameCanvas.read_short()
            # Java int division (values are positions >= 0, so // == /)
            hero.pos[0].x = i16((hero.pos[0].x // 27 // 7 * 7 + 4) * 27 + 8)
            hero.pos[0].y = i16((hero.pos[0].y // 27 // 7 * 7 + 4) * 27 + 8)
            for i in range(22):
                hero.mission_progress[i] = GameCanvas.read_byte()
            hero.live_stat1 = GameCanvas.read_byte()
            hero.live_stat2 = GameCanvas.read_byte()
            hero.level = GameCanvas.read_byte()
            if config.ORIG_BUG["B2"]:
                # ORIG-BUG B2: the level is one byte in the save (G(cz.l), ag.java:2908) read back
                # signed, so Lv128+ loaded as -128..; the rest of the game keeps it as an int
                hero.level &= 0xFF
            hero.base_attack = GameCanvas.read_short()
            hero.base_defense = GameCanvas.read_short()
            hero.base_hp = GameCanvas.read_short()
            hero.hp = GameCanvas.read_short()
            hero.base_mp = GameCanvas.read_short()
            hero.mp = GameCanvas.read_short()
            hero.gold = GameCanvas.read_int()
            if GameCanvas.cheat:
                hero.gold = 555000
            if config.GOLD is not None:   # PORT-EXTRA config.GOLD (POW_GOLD=N)
                hero.gold = i32(config.GOLD)
            hero.fame = GameCanvas.read_int()
            hero.exp = GameCanvas.read_int()
            hero.kills = GameCanvas.read_short()
            hero.stat_points = GameCanvas.read_short()
            hero.live_registered = GameCanvas.read_byte()
            for i in range(5):
                hero.hotkeys[i] = GameCanvas.read_byte()
            for i in range(19):
                hero.skill_levels[i] = GameCanvas.read_byte()
            for i in range(9):
                hero.equipped[i] = self.read_item()
            for i in range(25):
                hero.backpack[i] = self.read_item()
            for i in range(5):
                hero.quick_slots[i].item = GameCanvas.read_short()
                hero.quick_slots[i].count = GameCanvas.read_byte()
            hero.quick_keys[0] = GameCanvas.read_byte()
            hero.quick_keys[1] = GameCanvas.read_byte()
            hero.head = GameCanvas.read_byte()
            GameCanvas.play_time = GameCanvas.read_int()
            GameCanvas.live_time = GameCanvas.read_int()
            GameCanvas.live_gifts = GameCanvas.read_byte()
            GameCanvas.live_saved = GameCanvas.read_byte()
            GameCanvas.talk_count = GameCanvas.read_byte()
            GameCanvas.difficulty = GameCanvas.read_byte()
            for i in range(16):
                reserved[i] = GameCanvas.read_byte()
            GameCanvas.talk_points = GameCanvas.read_int()
            for i in range(4):
                GameCanvas.read_int()
            self.read_backpack_extra(save_end)
        self.compact_backpack()

    # PORT-EXTRA config.BACKPACK_SIZE: the backpack cells past the original 25 follow the original
    # save as {u8 'B', u8 n, n items}. A save without the block (an old one, or the original game's)
    # loads with those cells empty; the header length (save_buf[0..1]) tells where the save ends.
    BACKPACK_EXTRA_MARK = 0x42

    def read_backpack_extra(self, save_end):
        hero = GameCanvas.hero
        for b in range(25, config.BACKPACK_SIZE):
            hero.backpack[b] = Item()
        buf = GameCanvas.save_buf
        if GameCanvas.save_pos + 2 > save_end or buf[GameCanvas.save_pos] & 0xFF != GameCanvas.BACKPACK_EXTRA_MARK:
            return
        count = buf[GameCanvas.save_pos + 1] & 0xFF
        GameCanvas.save_pos += 2
        for b in range(count):
            if GameCanvas.save_pos + 11 > save_end:
                break
            it = self.read_item()
            if 25 + b < config.BACKPACK_SIZE:
                hero.backpack[25 + b] = it
            else:
                # a save of a bigger backpack than this build has: keep the item in the first free cell
                free = next((s for s in range(config.BACKPACK_SIZE) if hero.backpack[s].id == 0), None)
                if free is not None and it.id != 0:
                    hero.backpack[free] = it

    def write_backpack_extra(self):
        hero = GameCanvas.hero
        count = config.BACKPACK_SIZE - 25
        if count <= 0:
            return
        GameCanvas.write_byte(GameCanvas.BACKPACK_EXTRA_MARK)
        GameCanvas.write_byte(count)
        for b in range(25, config.BACKPACK_SIZE):
            self.write_item(hero.backpack[b])

    @staticmethod
    def read_long():  # ag.java:2216-2230  (u64 LE; bytes 4..7 are sign-extended then masked)
        buf, pos = GameCanvas.save_buf, GameCanvas.save_pos
        value = 0
        for nth in range(8):
            value |= (buf[pos + nth] & 0xFF) << (8 * nth)
        GameCanvas.save_pos += 8
        return value - (1 << 64) if value & (1 << 63) else value

    @staticmethod
    def read_int():  # ag.java:2232-2237
        buf, pos = GameCanvas.save_buf, GameCanvas.save_pos
        value = buf[pos] & 0xFF | buf[pos + 1] << 8 & 0xFF00 | buf[pos + 2] << 16 & 0xFF0000 | buf[pos + 3] << 24 & 0xFF000000
        GameCanvas.save_pos += 4
        return i32(value)

    @staticmethod
    def read_short():  # ag.java:2239-2244
        value = i16(GameCanvas.save_buf[GameCanvas.save_pos] & 0xFF | GameCanvas.save_buf[GameCanvas.save_pos + 1] << 8 & 0xFF00)
        GameCanvas.save_pos += 2
        return value

    @staticmethod
    def read_byte():  # ag.java:2246-2250
        b = i8(GameCanvas.save_buf[GameCanvas.save_pos] & 0xFF)
        GameCanvas.save_pos += 1
        return b

    def read_item(self):  # ag.java:2252-2261
        item = Item()
        item.id = GameCanvas.read_short()
        item.attack = GameCanvas.read_short()
        item.defense = GameCanvas.read_short()
        item.hp = GameCanvas.read_short()
        item.mp = GameCanvas.read_short()
        item.enchant = GameCanvas.read_byte()
        return item

    @staticmethod
    def has_save():  # ag.java:2862-2869  (is there a saved game?)
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_data", True)
            return recordStore.getNumRecords() != 0
        except Exception:
            return False

    def save_game(self):  # ag.java:2871-2961  (write the save "gamevil_pow_data")
        hero = GameCanvas.hero
        reserved = [0] * 16
        name = hero.name.encode("latin-1")
        if len(GameCanvas.save_buf) < 2000:
            # PORT-EXTRA: a loaded save can be shorter than ag.cF (965 bytes, e.g. tools/shot.py's);
            # the backpack block written after it needs the room of the 2000-byte buffer
            GameCanvas.save_buf = bytearray(GameCanvas.save_buf) + bytearray(2000 - len(GameCanvas.save_buf))
        buf = GameCanvas.save_buf
        for b in range(8):
            if b < len(name):
                buf[2 + b] = name[b]
            else:
                buf[2 + b] = 32
        buf[18] = GameCanvas.save_flag & 0xFF
        GameCanvas.save_pos = 19
        GameCanvas.write_byte(GameCanvas.lord)
        GameCanvas.write_byte(GameCanvas.mission)
        GameCanvas.write_byte(GameCanvas.rooms_visited)
        GameCanvas.write_long(GameCanvas.missions_done)
        GameCanvas.write_long(GameCanvas.lords_done)
        for b in range(8):
            GameCanvas.write_int(i32(GameCanvas.stats[b]))
        GameCanvas.write_int(GameCanvas.mission_exp)
        GameCanvas.write_int(GameCanvas.score)
        for b in range(44):
            GameCanvas.write_byte(GameCanvas.generals[0][b])
            GameCanvas.write_byte(GameCanvas.generals[1][b])
        GameCanvas.write_byte(GameCanvas.general_count)
        for b in range(25):
            self.write_item(GameCanvas.shop[b])
        GameCanvas.write_byte(GameCanvas.chapter)
        GameCanvas.write_short((idiv(GameCanvas.view_tx + 2, 7) * 7 + 4) * 27)
        GameCanvas.write_short((idiv(GameCanvas.view_ty + 2, 7) * 7 + 4) * 27)
        for b in range(22):
            GameCanvas.write_byte(hero.mission_progress[b])
        GameCanvas.write_byte(hero.live_stat1)
        GameCanvas.write_byte(hero.live_stat2)
        GameCanvas.write_byte(hero.level)
        GameCanvas.write_short(hero.base_attack)
        GameCanvas.write_short(hero.base_defense)
        GameCanvas.write_short(hero.base_hp)
        GameCanvas.write_short(hero.hp)
        GameCanvas.write_short(hero.base_mp)
        GameCanvas.write_short(hero.mp)
        GameCanvas.write_int(hero.gold)
        GameCanvas.write_int(hero.fame)
        GameCanvas.write_int(hero.exp)
        GameCanvas.write_short(hero.kills)
        GameCanvas.write_short(hero.stat_points)
        GameCanvas.write_byte(hero.live_registered)
        for b in range(5):
            GameCanvas.write_byte(hero.hotkeys[b])
        for b in range(19):
            GameCanvas.write_byte(hero.skill_levels[b])
        for b in range(9):
            self.write_item(hero.equipped[b])
        for b in range(25):
            self.write_item(hero.backpack[b])
        for b in range(5):
            GameCanvas.write_short(hero.quick_slots[b].item)
            GameCanvas.write_byte(hero.quick_slots[b].count)
        GameCanvas.write_byte(hero.quick_keys[0])
        GameCanvas.write_byte(hero.quick_keys[1])
        GameCanvas.write_byte(hero.head)
        GameCanvas.write_int(i32(GameCanvas.clock[0] - GameCanvas.play_time))
        GameCanvas.write_int(i32(GameCanvas.live_time))
        GameCanvas.write_byte(GameCanvas.live_gifts)
        GameCanvas.write_byte(GameCanvas.live_saved)
        GameCanvas.write_byte(GameCanvas.talk_count)
        GameCanvas.write_byte(GameCanvas.difficulty)
        for b in range(16):
            GameCanvas.write_byte(reserved[b])
        GameCanvas.write_int(GameCanvas.talk_points)
        for b in range(4):
            GameCanvas.write_int(0)
        self.write_backpack_extra()
        buf[0] = GameCanvas.save_pos & 0xFF
        buf[1] = GameCanvas.save_pos >> 8 & 0xFF
        try:
            recordStore = RecordStore.openRecordStore("gamevil_pow_data", True)
            if recordStore.getNumRecords() == 0:
                recordStore.addRecord(buf, 0, len(buf))
            recordStore.setRecord(1, buf, 0, len(buf))
        except Exception:
            pass
        return bool(GameCanvas.has_save())

    # cF holds Java bytes; the port stores them masked to 0..255 (RecordStore takes bytearray)
    @staticmethod
    def write_long(value):  # ag.java:2963-2973
        for nth in range(8):
            GameCanvas.save_buf[GameCanvas.save_pos + nth] = value >> (8 * nth) & 0xFF
        GameCanvas.save_pos += 8

    @staticmethod
    def write_int(value):  # ag.java:2975-2981
        GameCanvas.save_buf[GameCanvas.save_pos] = value & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 1] = value >> 8 & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 2] = value >> 16 & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 3] = value >> 24 & 0xFF
        GameCanvas.save_pos += 4

    @staticmethod
    def write_short(value):  # ag.java:2983-2987
        GameCanvas.save_buf[GameCanvas.save_pos] = value & 0xFF
        GameCanvas.save_buf[GameCanvas.save_pos + 1] = value >> 8 & 0xFF
        GameCanvas.save_pos += 2

    @staticmethod
    def write_byte(value):  # ag.java:2989-2992
        GameCanvas.save_buf[GameCanvas.save_pos] = value & 0xFF
        GameCanvas.save_pos += 1

    def write_item(self, item):  # ag.java:2994-3001
        GameCanvas.write_short(item.id)
        GameCanvas.write_short(item.attack)
        GameCanvas.write_short(item.defense)
        GameCanvas.write_short(item.hp)
        GameCanvas.write_short(item.mp)
        GameCanvas.write_byte(item.enchant)
