"""Small the original data classes. Generated once from the original;
edited by hand since."""
import config


class Point:
    def __init__(self):
        self.x = 0  # short
        self.y = 0  # short


class Rect:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = 0  # int
        self.y = 0  # int
        self.w = 0  # int
        self.h = 0  # int
        self.x = x  # constructor
        self.y = y  # constructor
        self.w = w  # constructor
        self.h = h  # constructor


class MapMode:
    def __init__(self):
        self.mode = 0  # byte
        self.sub = 0  # byte


class Item:
    def __init__(self):
        self.id = 0  # short
        self.attack = 0  # short
        self.defense = 0  # short
        self.hp = 0  # short
        self.mp = 0  # short
        self.enchant = 0  # byte

    def clear(self):
        self.id = 0
        self.attack = 0
        self.defense = 0
        self.hp = 0
        self.mp = 0
        self.enchant = 0


class QuickSlot:
    def __init__(self):
        self.item = 0  # short
        self.count = 0  # short


class GearDef:
    def __init__(self):
        self.name = None  # String
        self.slot = 0  # short
        self.bonus_stat = 0  # short
        self.bonus = 0  # short
        self.bonus_range = 0  # short
        self.icon = 0  # short


class TreasureDef:
    def __init__(self):
        self.name = None  # String
        self.slot = 0  # byte
        self.attack = 0  # short
        self.defense = 0  # byte
        self.hp = 0  # short
        self.mp = 0  # byte
        self.icon = 0  # byte
        self.level = 0  # short


class RareDef:
    def __init__(self):
        self.name = None  # String
        self.slot = 0  # byte
        self.attack = 0  # short
        self.defense = 0  # byte
        self.hp = 0  # short
        self.mp = 0  # byte
        self.level = 0  # short


class MapData:
    def __init__(self):
        self.data = None  # short[]
        self.size = None  # aj
        self.layer_ground = 0  # int
        self.layer_upper = 0  # int
        self.layer_objects = 0  # int
        self.layer_flags = 0  # int

    def free(self):  # (final void a())
        self.data = None


class MapSize:
    def __init__(self):
        self.w = 0  # short
        self.h = 0  # short
        self.extra = 0  # short


class ActiveEffect:
    def __init__(self):
        self.item = 0  # short
        self.step = 0  # short
        self.pos = Point()  # h
        self.dir = 0  # short
        self.slot = 0  # short
        self.frame = 0  # short
        self.frame_data = None  # byte[]
        self.frames = None  # y[]


class GeneralDef:
    def __init__(self):
        self.name = None  # String
        self.look = 0  # char
        self.side = 0  # char
        self.skills = [0] * 4  # char[]
        self.portrait = 0  # char
        self.gift_table = 0  # char
        self.attack = 0  # char
        self.defense = 0  # char
        self.hp = 0  # char


class InfoBox:
    def __init__(self):
        self.shown = 0  # byte
        self.rect = Rect(0, 0, 0, 0)  # ac
        self.text = None  # String
        self.text_x = 0  # short


class TargetInfo:
    def __init__(self):
        self.shown = 0  # short
        self.ticks = 0  # short
        self.name = ""  # String
        self.level = 0  # short
        self.hp_bar = 0  # short


class MissionDef:
    def __init__(self):
        self.id = 0  # short
        self.start_x = 0  # short
        self.start_y = 0  # short
        self.tint = 0  # short
        self.boss_type = 0  # short
        self.general = 0  # short
        self.reward = 0  # short
        self.gold = 0  # short
        self.time_limit = 0  # short
        self.level_bonus = 0  # short


class SpriteFrame:
    def __init__(self):
        self.src_x = 0  # short
        self.src_y = 0  # short
        self.w = 0  # short
        self.h = 0  # short
        self.ox = 0  # short
        self.oy = 0  # short


class Arrow:
    def __init__(self):
        self.active = 0  # byte
        self.pos = [None] * 2  # h[]
        self.w = 0  # byte
        self.h = 0  # byte
        self.dir = 0  # byte
        self.attack = 0  # short
        self.ticks = 0  # byte
        self.pos[0] = Point()  # constructor
        self.pos[1] = Point()  # constructor


class SpawnSpot:
    def __init__(self):
        self.tx = 0  # char
        self.ty = 0  # char
        self.dir = 0  # char


class Breakable:
    def __init__(self):
        self.active = 0  # short
        self.pos = Point()  # h
        self.tile = Point()  # h
        self.hp = 0  # short
        self.break_ticks = 0  # short
        self.image = 0  # short
        self.kind = 0  # short
        self.break_frame = 0  # short


class Drop:
    def __init__(self):
        self.item = 0  # short
        self.pos = None  # h
        self.ticks = 0  # short
        self.frame = 0  # short
        self.w = 0  # short
        self.h = 0  # short
        self.image = None  # Image


class ScriptSlot:
    def __init__(self):
        self.offset = 0  # int
        self.next = 0  # short
        self.used = 0  # short


class RoomCell:
    def __init__(self):
        self.exits = [0] * 4  # short[]
        self.max_enemies = 0  # short
        self.wave_0 = 0  # short
        self.wave_1 = 0  # short
        self.wave_2 = 0  # short
        self.wave_3 = 0  # short
        self.wave_4 = 0  # short
        self.wave_5 = 0  # short
        self.wave_6 = 0  # short
        self.wave_7 = 0  # short
        self.wave_8 = 0  # short
        self.wave_9 = 0  # short
        self.wave_10 = 0  # short
        self.wave_11 = 0  # short
        self.general = 0  # short


class Actor:
    def __init__(self):
        self.pos = [None] * 2  # h[]
        self.target = None  # h
        self.active = 0  # byte
        self.facing = 0  # byte
        self.dir = [0] * 2  # byte[]
        self.action = [0] * 2  # int[]
        self.frame = [0] * 2  # byte[]
        self.type = 0  # short
        self.level = 0  # short
        self.attack = 0  # short
        self.defense = 0  # short
        self.max_hp = 0  # short
        self.hp = 0  # short
        self.attack_buff = 0  # short
        self.defense_buff = 0  # short
        self.attack_buff_ticks = 0  # short
        self.defense_buff_ticks = 0  # short
        self.alerted = 0  # byte
        self.think_ticks = 0  # byte
        self.hit_fx_kind = 0  # byte
        self.hit_fx_frame = 0  # byte
        self.hit_fx_pos = None  # h
        self.on_fire = 0  # byte
        self.fire_frame = 0  # byte
        self.skill_fx = 0  # byte
        self.skill_step = 0  # byte
        self.ai_mode = 0  # byte
        self.anims = None  # short[][][]
        self.image = None  # Image
        self.frames = None  # y[]
        self.pos[0] = Point()  # constructor
        self.pos[1] = Point()  # constructor
        self.target = Point()  # constructor
        self.hit_fx_pos = Point()  # constructor


class Hero:
    def __init__(self):
        self.pos = [None] * 2  # h[]
        self.room_pos = [None] * 2  # h[]
        self.facing = 0  # int
        self.dir = [0] * 2  # int[]
        self.action = [0] * 2  # int[]
        self.frame = [0] * 2  # short[]
        self.mission_progress = [0] * 22  # short[]
        self.live_stat1 = 0  # short
        self.live_stat2 = 0  # short
        self.slide_target = None  # h
        self.name = None  # String
        self.level = 0  # int
        self.base_attack = 0  # int
        self.base_defense = 0  # int
        self.base_hp = 0  # int
        self.hp = 0  # int
        self.base_mp = 0  # int
        self.mp = 0  # int
        self.gear_attack = 0  # int
        self.gear_defense = 0  # int
        self.gear_hp = 0  # int
        self.gear_mp = 0  # int
        self.attack = 0  # int
        self.defense = 0  # int
        self.max_hp = 0  # int
        self.max_mp = 0  # int
        self.attack_buff = 0  # int
        self.defense_buff = 0  # int
        self.attack_buff_ticks = 0  # int
        self.defense_buff_ticks = 0  # int
        self.gold = 0  # int
        self.fame = 0  # int
        self.exp = 0  # int
        self.kills = 0  # int
        self.kills_shown = 0  # int
        self.stat_points = 0  # int
        self.weapon_kind = 0  # int
        self.sprite_frame = 0  # int
        self.combo = 0  # int
        self.idle_ticks = 0  # int
        self.hit_fx_kind = 0  # int
        self.hit_fx_frame = 0  # int
        self.hit_fx_pos = None  # h
        self.hurt_ticks = 0  # int
        self.live_registered = 0  # int
        self.on_fire = 0  # int
        self.fire_frame = 0  # int
        self.hotkeys = [0] * 5  # int[]
        self.skill_levels = [0] * 19  # int[]
        self.equipped = [None] * 9  # z[]
        self.backpack = [None] * config.BACKPACK_SIZE  # z[25]; config.BACKPACK_SIZE
        self.quick_slots = [None] * 5  # p[]
        self.quick_keys = [0] * 2  # int[]
        self.anims = [None] * 31  # short[][][]
        self.anim_0 = [None] * 8  # short[][]
        self.anim_1 = [[0] * 4 for _ in range(8)]  # short[][]
        self.anim_3 = [[0] * 2 for _ in range(8)]  # short[][]
        self.anim_4 = [[0] * 2 for _ in range(8)]  # short[][]
        self.anim_5 = [[0] * 2 for _ in range(8)]  # short[][]
        self.anim_6 = [[0] * 3 for _ in range(8)]  # short[][]
        self.anim_7 = [[0] * 3 for _ in range(8)]  # short[][]
        self.anim_8 = [[0] * 3 for _ in range(8)]  # short[][]
        self.anim_2 = [[0] * 3 for _ in range(8)]  # short[][]
        self.anim_9 = [[0] * 7 for _ in range(8)]  # short[][]
        self.anim_10 = [None] * 8  # short[][]
        self.anim_12 = [None] * 8  # short[][]
        self.anim_13 = [None] * 8  # short[][]
        self.anim_14 = [None] * 8  # short[][]
        self.anim_15_19 = [None] * 8  # short[][]
        self.anim_20 = [None] * 8  # short[][]
        self.anim_21 = [None] * 8  # short[][]
        self.anim_22 = [None] * 8  # short[][]
        self.anim_23_24 = [None] * 8  # short[][]
        self.anim_25 = [None] * 8  # short[][]
        self.anim_26_27 = [None] * 8  # short[][]
        self.anim_28 = [None] * 8  # short[][]
        self.anim_29 = [None] * 8  # short[][]
        self.anim_30 = [None] * 8  # short[][]
        self.anim_11 = [None] * 8  # short[][]
        self.head = 0  # int
        self.head_frames = None  # y[]
        self.head_frames2 = None  # y[]
        self.body_frames = None  # y[]
        self.body_frames2 = None  # y[]
        self.head_image = None  # Image
        self.body_image = None  # Image

    def reset_inventory(self):
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
