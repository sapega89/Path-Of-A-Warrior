"""ag.java, part of GameCanvas: items, backpack, shop, hero stats.

A mixin of GameCanvas (pow/game/game_canvas.py); the methods keep their `# ag.java:FROM-TO`
comments. `GameCanvas` below is the real class, set by game_canvas.py once it exists.
"""

import config
from pow.game import consts
from pow.game.arr_table import ArrTable
from pow.game.structs import Item
from pow.midp.jint import i8, i16

GameCanvas = None   # set by pow/game/game_canvas.py


class ItemsMixin:
    def compact_backpack(self):  # ag.java:2372-2382  (compact inventory cz.Y)
        for b in range(config.BACKPACK_SIZE - 1):
            if GameCanvas.hero.backpack[b].id == 0:
                for other in range(b + 1, config.BACKPACK_SIZE):
                    if GameCanvas.hero.backpack[other].id != 0:
                        self.swap_items(GameCanvas.hero.backpack[b], GameCanvas.hero.backpack[other])
                        break

    def swap_items(self, a, b):  # ag.java:2384-2389
        tmp = Item()
        GameCanvas.copy_item(tmp, a)
        GameCanvas.copy_item(a, b)
        GameCanvas.copy_item(b, tmp)

    @staticmethod
    def copy_item(dst, src):  # ag.java:2391-2398
        dst.id = src.id
        dst.attack = src.attack
        dst.defense = src.defense
        dst.hp = src.hp
        dst.mp = src.mp
        dst.enchant = src.enchant

    @staticmethod
    def add_exp(exp):  # ag.java:3081-3098  (add exp; returns the levels gained)
        exp_table = [0] * 10
        b = 0
        exp += GameCanvas.hero.exp
        while True:
            j = b % 10
            if j == 0:
                exp_table = GameCanvas.menus.load_exp_table()
            j = exp_table[j]
            if exp < j:
                GameCanvas.hero.exp = exp
                return b
            exp -= j
            GameCanvas.hero.level += 1
            GameCanvas.hero.stat_points += 3
            b += 1

    @staticmethod
    def update_hero_stats():  # ag.java:1759-1773  (equipment bonuses -> derived stats)
        hero = GameCanvas.hero
        hero.gear_attack = hero.gear_defense = hero.gear_hp = hero.gear_mp = 0
        for b in range(9):
            if hero.equipped[b].id != 0:
                hero.gear_attack += hero.equipped[b].attack
                hero.gear_defense += hero.equipped[b].defense
                hero.gear_hp += hero.equipped[b].hp
                hero.gear_mp += hero.equipped[b].mp
        hero.attack = hero.base_attack + hero.gear_attack
        hero.defense = hero.base_defense + hero.gear_defense
        hero.max_hp = hero.hp = hero.base_hp + hero.gear_hp
        hero.max_mp = hero.mp = hero.base_mp + hero.gear_mp

    def new_hero(self):  # ag.java:3222-3273  (fresh hero)
        hero = GameCanvas.hero
        GameCanvas.save_flag = 0
        GameCanvas.talk_count = 0
        GameCanvas.missions_done = 35113052110447
        GameCanvas.lords_done = 0
        GameCanvas.score = 0
        GameCanvas.chapter = 0
        hero.head = 0
        hero.name = ""
        for b in range(45):
            GameCanvas.generals[1][b] = 0
            GameCanvas.generals[0][b] = 0
        GameCanvas.general_count = 0
        for b in range(8):
            GameCanvas.stats[b] = 0
        hero.level = 1
        GameCanvas.reset_base_stats()
        hero.fame = 0
        hero.gold = 0
        hero.exp = 0
        hero.live_registered = 0
        for b in range(22):
            hero.mission_progress[b] = 0
        hero.live_stat1 = 0
        hero.live_stat2 = 0
        for b in range(5):
            hero.hotkeys[b] = 0
            hero.quick_slots[b].item = 0
            hero.quick_slots[b].count = 0
        for b in range(19):
            hero.skill_levels[b] = 0
        hero.skill_levels[0] = 1
        hero.skill_levels[5] = 1
        hero.hotkeys[0] = 12
        hero.hotkeys[1] = 17
        if GameCanvas.cheat:
            for b in range(19):
                hero.skill_levels[b] = 1
            hero.skill_levels[18] = 1
        # z.a(): called through the class (in Java the field z.a shadowed it)
        for b in range(9):
            Item.clear(hero.equipped[b])
        for b in range(config.BACKPACK_SIZE):
            Item.clear(hero.backpack[b])
        self.give_item(116, 0)
        self.swap_items(hero.equipped[0], hero.backpack[0])
        hero.quick_keys[0] = 0
        hero.quick_keys[1] = 1

    @staticmethod
    def reset_base_stats():  # ag.java:3275-3284  (base stats, 5 free points)
        from pow.game import hero_classes
        hero = GameCanvas.hero
        # PORT-EXTRA: the stats of the chosen head (pow/game/hero_classes.py); the original
        # gave every head ATK 5 / DEF 4 / HP 30 / MP 10, which is still head 0
        hero_classes.set_base_stats(hero)
        hero.stat_points = 5
        GameCanvas.redraw = 1

    def give_item(self, item_id, count):  # ag.java:3286-3360  (give an item / potion / gold)
        hero = GameCanvas.hero
        b = 0
        if item_id < 100:
            if count != 0:
                free_slot = -1
                b = 0
                while b < 5:
                    if hero.quick_slots[b].item == item_id:
                        if hero.quick_slots[b].count > 4:
                            return 0
                        break
                    if hero.quick_slots[b].item == 0 and free_slot < 0:
                        free_slot = b
                    b += 1
                if free_slot > -1 and b > 4:
                    b = free_slot
                if b > 4:
                    return 0
            else:
                hero.quick_slots[GameCanvas.effect.slot].count = i16(hero.quick_slots[GameCanvas.effect.slot].count - 1)
                if hero.quick_slots[GameCanvas.effect.slot].count < 1:
                    hero.quick_slots[GameCanvas.effect.slot].item = 0
                return 1
        elif item_id < 10000:
            b = 0
            while b < config.BACKPACK_SIZE and hero.backpack[b].id != 0:
                b += 1
            if b > config.BACKPACK_SIZE - 1:
                return 0
            hero.backpack[b].id = i16(item_id)
            hero.backpack[b].attack = 0
            hero.backpack[b].defense = 0
            hero.backpack[b].hp = 0
            hero.backpack[b].mp = 0
            hero.backpack[b].enchant = 0
        if item_id < 10000:
            GameCanvas.menus.load_item_def(item_id)
        if item_id < 100:
            hero.quick_slots[b].item = i16(item_id)
            hero.quick_slots[b].count = i16(hero.quick_slots[b].count + 1)
        elif item_id < 300:
            if count != 0:
                bonus = i16(GameCanvas.gear_def.bonus + self.rand(GameCanvas.gear_def.bonus_range + 1))
            else:
                bonus = GameCanvas.gear_def.bonus
            if GameCanvas.gear_def.bonus_stat == 0:
                hero.backpack[b].attack = bonus
            elif GameCanvas.gear_def.bonus_stat == 1:
                hero.backpack[b].defense = bonus
            elif GameCanvas.gear_def.bonus_stat == 2:
                hero.backpack[b].hp = bonus
            elif GameCanvas.gear_def.bonus_stat == 3:
                hero.backpack[b].mp = bonus
        elif item_id < 500:
            hero.backpack[b].attack = GameCanvas.treasure_def.attack
            hero.backpack[b].defense = i16(GameCanvas.treasure_def.defense)
            hero.backpack[b].hp = GameCanvas.treasure_def.hp
            hero.backpack[b].mp = i16(GameCanvas.treasure_def.mp)
        elif item_id < 10000:
            hero.backpack[b].attack = GameCanvas.rare_def.attack
            hero.backpack[b].defense = i16(GameCanvas.rare_def.defense)
            hero.backpack[b].hp = GameCanvas.rare_def.hp
            hero.backpack[b].mp = i16(GameCanvas.rare_def.mp)
        else:
            hero.gold += item_id - 10000
        return 1

    @staticmethod
    def reset_quick_items():  # ag.java:3362-3375  (starting quick items)
        for b in range(8):
            if GameCanvas.shop[b] is None:
                GameCanvas.shop[b] = Item()
        GameCanvas.shop[0].id = 1
        GameCanvas.shop[1].id = 2
        GameCanvas.shop[2].id = 3
        GameCanvas.shop[3].id = 4
        GameCanvas.shop[4].id = 5
        GameCanvas.shop[5].id = 6
        GameCanvas.shop[6].id = 10
        GameCanvas.shop[7].id = 11

    def fill_shop(self):  # ag.java:3377-3398  (17 random shop items, sorted)
        ids = [0] * 17
        GameCanvas.load_item_tables()
        for b in range(17):
            ids[b] = 101 + 5 * GameCanvas.rand_range(0, 20) + GameCanvas.item_tier(GameCanvas.rand_range(0, 100))
        for b in range(16, 0, -1):
            bool_ = False
            for i in range(b):
                if ids[i] > ids[i + 1]:
                    tmp = ids[i]
                    ids[i] = ids[i + 1]
                    ids[i + 1] = tmp
                    bool_ = True
            if not bool_:
                break
        for b in range(17):
            GameCanvas.shop[8 + b] = self.make_item(ids[b])

    @staticmethod
    def load_item_tables():  # ag.java:3400-3412
        files = [47, 51, 49]
        if not GameCanvas.tables_loaded[1]:
            for b in range(3):
                if GameCanvas.item_tables[b] is None:
                    GameCanvas.item_tables[b] = ArrTable("/" + GameCanvas.scr_data.get(files[b]))
                if GameCanvas.item_tables[b] is None:
                    return False
            GameCanvas.tables_loaded[1] = True
        return True

    @staticmethod
    def item_tier(roll):  # ag.java:3414-3422  (item tier by hero level)
        limit = 0
        b = 0
        while b < 5 and GameCanvas.hero.level >= consts.tier_levels[b]:
            b += 1
        odds = consts.tier_drop_odds[b - 1]
        b = 0
        while b < 4:
            limit += odds & 0xFF
            if not roll >= limit:
                break
            odds >>= 8
            b += 1
        return b

    def make_item(self, item_id):  # ag.java:3424-3457  (make item paramInt with random bonus)
        item = Item()
        stats = [0] * 5
        item.id = i16(item_id)
        item.enchant = 0
        if item_id < 300:
            for b in range(3):
                stats[b] = GameCanvas.item_tables[0].get_int(item_id - 101, 2 + b)
            if stats[0] == 0:
                item.attack = i16(stats[1] + self.rand(stats[2]))
            elif stats[0] == 1:
                item.defense = i16(stats[1] + self.rand(stats[2]))
            elif stats[0] == 2:
                item.hp = i16(stats[1] + self.rand(stats[2]))
            elif stats[0] == 3:
                item.mp = i16(stats[1] + self.rand(stats[2]))
        else:
            tbl = GameCanvas.item_tables[1] if item_id < 500 else GameCanvas.item_tables[2]
            # ORIG-BUG B1: the original reads both tables at id - 301, so a Rare item (shinki.arr,
            # ids 501-518) gets row 200+ -> all 0; its own row is id - 501
            first = 501 if item_id >= 500 and config.ORIG_BUG["B1"] else 301
            for b in range(4):
                stats[b] = tbl.get_int(item_id - first, 2 + b)
            item.attack = i16(stats[0])
            item.defense = i16(stats[1])
            item.hp = i16(stats[2])
            item.mp = i16(stats[3])
        return item

    @staticmethod
    def backpack_slot_of(item_id):  # ag.java:3530-3536  (inventory slot of item, 1-based; 0 = none)
        for b in range(config.BACKPACK_SIZE):
            if GameCanvas.hero.backpack[b].id == item_id:
                return b + 1
        return 0

    # ---- Management: items, descriptions ---------------------------------------------------

    @staticmethod
    def item_slot_type(item_id):  # ag.java:867-870  (equipment slot type of an item)
        GameCanvas.menus.load_item_def(item_id)
        if item_id < 100:
            return 1
        if item_id < 300:
            return i8(GameCanvas.gear_def.slot)
        if item_id < 500:
            return GameCanvas.treasure_def.slot
        return GameCanvas.rare_def.slot

    @staticmethod
    def describe_shop_item(item, with_name, price):  # ag.java:1454-1457  (item description in the shop)
        # dF.a() (ak.java:10-17) - the method is shadowed by the field ak.a in Python
        info = GameCanvas.info_box
        info.shown = 0
        info.rect.x = info.rect.y = info.rect.w = info.rect.h = 0
        info.text = ""
        GameCanvas.menus.draw_shop_description(item, 0, 0, 200, 22, price, with_name)

    @staticmethod
    def quick_slot_item(slot):  # ag.java:1459-1465  (potion slot -> item)
        item = Item()
        Item.clear(item)
        item.id = slot.item
        item.attack = slot.count
        return item

    def item_under_cursor(self, index):  # ag.java:1467-1492  (item under the cursor of the item grid)
        item = Item()
        if index == -1:
            index = GameCanvas.cursor[18]
        grid = GameCanvas.cursor[0]
        if grid == 0:
            item = GameCanvas.shop[index]
        elif grid == 1:
            if index < 5:
                item = GameCanvas.quick_slot_item(GameCanvas.hero.quick_slots[index])
            else:
                item = GameCanvas.hero.backpack[index - 5]
        elif grid in (2, 3):
            if GameCanvas.cursor[27] == 0:
                item = GameCanvas.hero.backpack[index]
            else:
                item = GameCanvas.hero.equipped[index]
        return item

    @staticmethod
    def describe_potion(potion):  # ag.java:1370-1381  (potion description)
        str_ = ""
        potion -= 1
        if potion < 0 or potion > 10:
            return str_
        if potion < 9:
            str_ = (consts.potion_names[potion] + " / Recover " + str(consts.potion_percents[potion % 3]) + "% of total "
                    + consts.potion_kinds[potion // 3])
        else:
            utf = GameCanvas.edat_string(54, 24 + potion).encode("latin-1")
            str_ = consts.potion_names[potion] + " / " + GameCanvas.read_utf(utf, 0, len(utf))
        return str_

    @staticmethod
    def special_suffix(item_id):  # ag.java:1383-1399  (special item suffix)
        return {434: " / Hp 5 Increased", 435: " / MP 3 Increased", 436: " / DEF 1 Increased",
                437: " / ATK 1 Increased", 502: " / Catherine's scarf",
                504: " / all General Visiting"}.get(item_id, "")

    @staticmethod
    def set_item_name(item_id):  # ag.java:1401-1416  (item name -> dF.c, returns the level needed)
        GameCanvas.menus.load_item_def(item_id)
        if item_id > 500:
            GameCanvas.info_box.text = GameCanvas.rare_def.name
            return GameCanvas.rare_def.level
        if item_id > 300:
            GameCanvas.info_box.text = GameCanvas.treasure_def.name
            return GameCanvas.treasure_def.level
        if item_id > 100:
            GameCanvas.info_box.text = GameCanvas.gear_def.name
            return consts.tier_req_level[item_id % 5]
        return 0
