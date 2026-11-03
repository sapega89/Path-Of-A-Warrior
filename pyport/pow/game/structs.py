"""Small Java data classes (h.java, z.java, n.java, ...). Generated once from the Java source;
edited by hand since. Java -> Python names: pyport/NAMES.md."""
import config


class Point:  # h.java
    def __init__(self):
        self.x = 0  # h.java:2 short
        self.y = 0  # h.java:4 short


class Rect:  # ac.java
    def __init__(self, paramInt1=0, paramInt2=0, paramInt3=0, paramInt4=0):
        self.x = 0  # ac.java:2 int
        self.y = 0  # ac.java:4 int
        self.w = 0  # ac.java:6 int
        self.h = 0  # ac.java:8 int
        self.x = paramInt1  # constructor
        self.y = paramInt2  # constructor
        self.w = paramInt3  # constructor
        self.h = paramInt4  # constructor


class MapMode:  # aa.java
    def __init__(self):
        self.mode = 0  # aa.java:2 byte
        self.sub = 0  # aa.java:4 byte


class Item:  # z.java
    def __init__(self):
        self.id = 0  # z.java:2 short
        self.attack = 0  # z.java:4 short
        self.defense = 0  # z.java:6 short
        self.hp = 0  # z.java:8 short
        self.mp = 0  # z.java:10 short
        self.enchant = 0  # z.java:12 byte

    def clear(self):  # z.java:15-22
        self.id = 0
        self.attack = 0
        self.defense = 0
        self.hp = 0
        self.mp = 0
        self.enchant = 0


class QuickSlot:  # p.java
    def __init__(self):
        self.item = 0  # p.java:2 short
        self.count = 0  # p.java:4 short


class GearDef:  # ai.java
    def __init__(self):
        self.name = None  # ai.java:2 String
        self.slot = 0  # ai.java:4 short
        self.bonus_stat = 0  # ai.java:6 short
        self.bonus = 0  # ai.java:8 short
        self.bonus_range = 0  # ai.java:10 short
        self.icon = 0  # ai.java:12 short


class TreasureDef:  # t.java
    def __init__(self):
        self.name = None  # t.java:2 String
        self.slot = 0  # t.java:4 byte
        self.attack = 0  # t.java:6 short
        self.defense = 0  # t.java:8 byte
        self.hp = 0  # t.java:10 short
        self.mp = 0  # t.java:12 byte
        self.icon = 0  # t.java:14 byte
        self.level = 0  # t.java:16 short


class RareDef:  # ao.java
    def __init__(self):
        self.name = None  # ao.java:2 String
        self.slot = 0  # ao.java:4 byte
        self.attack = 0  # ao.java:6 short
        self.defense = 0  # ao.java:8 byte
        self.hp = 0  # ao.java:10 short
        self.mp = 0  # ao.java:12 byte
        self.level = 0  # ao.java:14 short


class MapData:  # o.java
    def __init__(self):
        self.data = None  # o.java:2 short[]
        self.size = None  # o.java:4 aj
        self.layer_ground = 0  # o.java:6 int
        self.layer_upper = 0  # o.java:8 int
        self.layer_objects = 0  # o.java:10 int
        self.layer_flags = 0  # o.java:12 int

    def free(self):  # o.java (final void a())
        self.data = None


class MapSize:  # aj.java
    def __init__(self):
        self.w = 0  # aj.java:2 short
        self.h = 0  # aj.java:4 short
        self.extra = 0  # aj.java:6 short


class ActiveEffect:  # ad.java
    def __init__(self):
        self.item = 0  # ad.java:2 short
        self.step = 0  # ad.java:4 short
        self.pos = Point()  # ad.java:6 h
        self.dir = 0  # ad.java:8 short
        self.slot = 0  # ad.java:10 short
        self.frame = 0  # ad.java:12 short
        self.frame_data = None  # ad.java:14 byte[]
        self.frames = None  # ad.java:16 y[]


class GeneralDef:  # am.java
    def __init__(self):
        self.name = None  # am.java:2 String
        self.look = 0  # am.java:4 char
        self.side = 0  # am.java:6 char
        self.skills = [0] * 4  # am.java:8 char[]
        self.portrait = 0  # am.java:10 char
        self.gift_table = 0  # am.java:12 char
        self.attack = 0  # am.java:14 char
        self.defense = 0  # am.java:16 char
        self.hp = 0  # am.java:18 char


class InfoBox:  # ak.java
    def __init__(self):
        self.shown = 0  # ak.java:2 byte
        self.rect = Rect(0, 0, 0, 0)  # ak.java:4 ac
        self.text = None  # ak.java:6 String
        self.text_x = 0  # ak.java:8 short


class TargetInfo:  # w.java
    def __init__(self):
        self.shown = 0  # w.java:2 short
        self.ticks = 0  # w.java:4 short
        self.name = ""  # w.java:6 String
        self.level = 0  # w.java:8 short
        self.hp_bar = 0  # w.java:10 short


class MissionDef:  # an.java
    def __init__(self):
        self.id = 0  # an.java:2 short
        self.start_x = 0  # an.java:4 short
        self.start_y = 0  # an.java:6 short
        self.tint = 0  # an.java:8 short
        self.boss_type = 0  # an.java:10 short
        self.general = 0  # an.java:12 short
        self.reward = 0  # an.java:14 short
        self.gold = 0  # an.java:16 short
        self.time_limit = 0  # an.java:18 short
        self.level_bonus = 0  # an.java:20 short


class SpriteFrame:  # y.java
    def __init__(self):
        self.src_x = 0  # y.java:2 short
        self.src_y = 0  # y.java:4 short
        self.w = 0  # y.java:6 short
        self.h = 0  # y.java:8 short
        self.ox = 0  # y.java:10 short
        self.oy = 0  # y.java:12 short


class Arrow:  # f.java
    def __init__(self):
        self.active = 0  # f.java:2 byte
        self.pos = [None] * 2  # f.java:4 h[]
        self.w = 0  # f.java:6 byte
        self.h = 0  # f.java:8 byte
        self.dir = 0  # f.java:10 byte
        self.attack = 0  # f.java:12 short
        self.ticks = 0  # f.java:14 byte
        self.pos[0] = Point()  # constructor
        self.pos[1] = Point()  # constructor


class SpawnSpot:  # i.java
    def __init__(self):
        self.tx = 0  # i.java:2 char
        self.ty = 0  # i.java:4 char
        self.dir = 0  # i.java:6 char


class Breakable:  # r.java
    def __init__(self):
        self.active = 0  # r.java:2 short
        self.pos = Point()  # r.java:4 h
        self.tile = Point()  # r.java:6 h
        self.hp = 0  # r.java:8 short
        self.break_ticks = 0  # r.java:10 short
        self.image = 0  # r.java:12 short
        self.kind = 0  # r.java:14 short
        self.break_frame = 0  # r.java:16 short


class Drop:  # a.java
    def __init__(self):
        self.item = 0  # a.java:4 short
        self.pos = None  # a.java:6 h
        self.ticks = 0  # a.java:8 short
        self.frame = 0  # a.java:10 short
        self.w = 0  # a.java:12 short
        self.h = 0  # a.java:14 short
        self.image = None  # a.java:16 Image


class ScriptSlot:  # ah.java
    def __init__(self):
        self.offset = 0  # ah.java:2 int
        self.next = 0  # ah.java:4 short
        self.used = 0  # ah.java:6 short


class RoomCell:  # au.java
    def __init__(self):
        self.exits = [0] * 4  # au.java:2 short[]
        self.max_enemies = 0  # au.java:4 short
        self.wave_0 = 0  # au.java:6 short
        self.wave_1 = 0  # au.java:8 short
        self.wave_2 = 0  # au.java:10 short
        self.wave_3 = 0  # au.java:12 short
        self.wave_4 = 0  # au.java:14 short
        self.wave_5 = 0  # au.java:16 short
        self.wave_6 = 0  # au.java:18 short
        self.wave_7 = 0  # au.java:20 short
        self.wave_8 = 0  # au.java:22 short
        self.wave_9 = 0  # au.java:24 short
        self.wave_10 = 0  # au.java:26 short
        self.wave_11 = 0  # au.java:28 short
        self.general = 0  # au.java:30 short


class Actor:  # ap.java
    def __init__(self):
        self.pos = [None] * 2  # ap.java:4 h[]
        self.target = None  # ap.java:6 h
        self.active = 0  # ap.java:8 byte
        self.facing = 0  # ap.java:10 byte
        self.dir = [0] * 2  # ap.java:12 byte[]
        self.action = [0] * 2  # ap.java:14 int[]
        self.frame = [0] * 2  # ap.java:16 byte[]
        self.type = 0  # ap.java:18 short
        self.level = 0  # ap.java:20 short
        self.attack = 0  # ap.java:22 short
        self.defense = 0  # ap.java:24 short
        self.max_hp = 0  # ap.java:26 short
        self.hp = 0  # ap.java:28 short
        self.attack_buff = 0  # ap.java:30 short
        self.defense_buff = 0  # ap.java:32 short
        self.attack_buff_ticks = 0  # ap.java:34 short
        self.defense_buff_ticks = 0  # ap.java:36 short
        self.alerted = 0  # ap.java:38 byte
        self.think_ticks = 0  # ap.java:40 byte
        self.hit_fx_kind = 0  # ap.java:42 byte
        self.hit_fx_frame = 0  # ap.java:44 byte
        self.hit_fx_pos = None  # ap.java:46 h
        self.on_fire = 0  # ap.java:48 byte
        self.fire_frame = 0  # ap.java:50 byte
        self.skill_fx = 0  # ap.java:52 byte
        self.skill_step = 0  # ap.java:54 byte
        self.ai_mode = 0  # ap.java:56 byte
        self.anims = None  # ap.java:58 short[][][]
        self.image = None  # ap.java:60 Image
        self.frames = None  # ap.java:62 y[]
        self.pos[0] = Point()  # constructor
        self.pos[1] = Point()  # constructor
        self.target = Point()  # constructor
        self.hit_fx_pos = Point()  # constructor


class Hero:  # n.java
    def __init__(self):
        self.pos = [None] * 2  # n.java:4 h[]
        self.room_pos = [None] * 2  # n.java:6 h[]
        self.facing = 0  # n.java:8 int
        self.dir = [0] * 2  # n.java:10 int[]
        self.action = [0] * 2  # n.java:12 int[]
        self.frame = [0] * 2  # n.java:14 short[]
        self.mission_progress = [0] * 22  # n.java:16 short[]
        self.live_stat1 = 0  # n.java:18 short
        self.live_stat2 = 0  # n.java:20 short
        self.slide_target = None  # n.java:22 h
        self.name = None  # n.java:24 String
        self.level = 0  # n.java:26 int
        self.base_attack = 0  # n.java:28 int
        self.base_defense = 0  # n.java:30 int
        self.base_hp = 0  # n.java:32 int
        self.hp = 0  # n.java:34 int
        self.base_mp = 0  # n.java:36 int
        self.mp = 0  # n.java:38 int
        self.gear_attack = 0  # n.java:40 int
        self.gear_defense = 0  # n.java:42 int
        self.gear_hp = 0  # n.java:44 int
        self.gear_mp = 0  # n.java:46 int
        self.attack = 0  # n.java:48 int
        self.defense = 0  # n.java:50 int
        self.max_hp = 0  # n.java:52 int
        self.max_mp = 0  # n.java:54 int
        self.attack_buff = 0  # n.java:56 int
        self.defense_buff = 0  # n.java:58 int
        self.attack_buff_ticks = 0  # n.java:60 int
        self.defense_buff_ticks = 0  # n.java:62 int
        self.gold = 0  # n.java:64 int
        self.fame = 0  # n.java:66 int
        self.exp = 0  # n.java:68 int
        self.kills = 0  # n.java:70 int
        self.kills_shown = 0  # n.java:72 int
        self.stat_points = 0  # n.java:74 int
        self.weapon_kind = 0  # n.java:76 int
        self.sprite_frame = 0  # n.java:78 int
        self.combo = 0  # n.java:80 int
        self.idle_ticks = 0  # n.java:82 int
        self.hit_fx_kind = 0  # n.java:84 int
        self.hit_fx_frame = 0  # n.java:86 int
        self.hit_fx_pos = None  # n.java:88 h
        self.hurt_ticks = 0  # n.java:90 int
        self.live_registered = 0  # n.java:92 int
        self.on_fire = 0  # n.java:94 int
        self.fire_frame = 0  # n.java:96 int
        self.hotkeys = [0] * 5  # n.java:98 int[]
        self.skill_levels = [0] * 19  # n.java:100 int[]
        self.equipped = [None] * 9  # n.java:102 z[]
        self.backpack = [None] * config.BACKPACK_SIZE  # n.java:104 z[25]; PORT-EXTRA config.BACKPACK_SIZE
        self.quick_slots = [None] * 5  # n.java:106 p[]
        self.quick_keys = [0] * 2  # n.java:108 int[]
        self.anims = [None] * 31  # n.java:110 short[][][]
        self.anim_0 = [None] * 8  # n.java:112 short[][]
        self.anim_1 = [[0] * 4 for _ in range(8)]  # n.java:114 short[][]
        self.anim_3 = [[0] * 2 for _ in range(8)]  # n.java:116 short[][]
        self.anim_4 = [[0] * 2 for _ in range(8)]  # n.java:118 short[][]
        self.anim_5 = [[0] * 2 for _ in range(8)]  # n.java:120 short[][]
        self.anim_6 = [[0] * 3 for _ in range(8)]  # n.java:122 short[][]
        self.anim_7 = [[0] * 3 for _ in range(8)]  # n.java:124 short[][]
        self.anim_8 = [[0] * 3 for _ in range(8)]  # n.java:126 short[][]
        self.anim_2 = [[0] * 3 for _ in range(8)]  # n.java:128 short[][]
        self.anim_9 = [[0] * 7 for _ in range(8)]  # n.java:130 short[][]
        self.anim_10 = [None] * 8  # n.java:132 short[][]
        self.anim_12 = [None] * 8  # n.java:134 short[][]
        self.anim_13 = [None] * 8  # n.java:136 short[][]
        self.anim_14 = [None] * 8  # n.java:138 short[][]
        self.anim_15_19 = [None] * 8  # n.java:140 short[][]
        self.anim_20 = [None] * 8  # n.java:142 short[][]
        self.anim_21 = [None] * 8  # n.java:144 short[][]
        self.anim_22 = [None] * 8  # n.java:146 short[][]
        self.anim_23_24 = [None] * 8  # n.java:148 short[][]
        self.anim_25 = [None] * 8  # n.java:150 short[][]
        self.anim_26_27 = [None] * 8  # n.java:152 short[][]
        self.anim_28 = [None] * 8  # n.java:154 short[][]
        self.anim_29 = [None] * 8  # n.java:156 short[][]
        self.anim_30 = [None] * 8  # n.java:158 short[][]
        self.anim_11 = [None] * 8  # n.java:160 short[][]
        self.head = 0  # n.java:162 int
        self.head_frames = None  # n.java:164 y[]
        self.head_frames2 = None  # n.java:166 y[]
        self.body_frames = None  # n.java:168 y[]
        self.body_frames2 = None  # n.java:170 y[]
        self.head_image = None  # n.java:172 Image
        self.body_image = None  # n.java:174 Image

    def reset_inventory(self):  # n.java:130-144
        for b in range(9):
            self.equipped[b] = Item()
        for b in range(config.BACKPACK_SIZE):
            self.backpack[b] = Item()
        for b in range(5):
            self.quick_slots[b] = QuickSlot()
        for b in range(2):
            self.pos[b] = Point()
        for b in range(2):
            self.room_pos[b] = Point()
        self.slide_target = Point()
        self.hit_fx_pos = Point()
