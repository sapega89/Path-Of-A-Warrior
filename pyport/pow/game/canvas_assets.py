"""ag.java, part of GameCanvas: loading and freeing images, sprites and data files.

A mixin of GameCanvas (pow/game/game_canvas.py); the methods keep their `# ag.java:FROM-TO`
comments. `GameCanvas` below is the real class, set by game_canvas.py once it exists.
"""

from pow.game.gfx import Gfx
from pow.game.res_reader import ResReader
from pow.game.structs import GearDef, RareDef, SpriteFrame, TreasureDef
from pow.midp.graphics import Image
from pow.midp.jint import idiv

GameCanvas = None   # set by pow/game/game_canvas.py


class AssetsMixin:
    @staticmethod
    def free_images():  # ag.java:829-865
        for b in range(2):
            GameCanvas.boss_images[b] = None
        for b in range(9):
            GameCanvas.enemy_frames[b] = None
        for b in range(len(GameCanvas.images)):
            GameCanvas.images[b] = None
        GameCanvas.hero_body_frames[1] = None
        GameCanvas.hero_body_frames[0] = None
        GameCanvas.hero_weapon_frames[1] = None
        GameCanvas.hero_weapon_frames[0] = None
        GameCanvas.trail_frames = None
        GameCanvas.shadow_image = None
        GameCanvas.spark_frames = None
        GameCanvas.skill_frames = None
        GameCanvas.hero_fx_frames = None
        GameCanvas.enemy_fx_frames = None
        GameCanvas.fire_frames = None
        GameCanvas.map.data = None
        GameCanvas.effect.frame_data = None
        GameCanvas.effect.frames = None
        GameCanvas.hero.head_frames = GameCanvas.hero.body_frames = None
        GameCanvas.hero.head_image = None
        GameCanvas.hero.body_image = None
        GameCanvas.gear_data = GameCanvas.rare_data = GameCanvas.treasure_data = None
        GameCanvas.difficulty = 0
        GameCanvas.popups.kind = 0
        GameCanvas.speed = 2
        for b in range(30):
            GameCanvas.menu_cursors[b] = 0
            GameCanvas.menu_tops[b] = 0
        GameCanvas.gear_def = GearDef()
        GameCanvas.treasure_def = TreasureDef()
        GameCanvas.rare_def = RareDef()

    def load_title_picture(self):  # ag.java:1154-1163  (title picture = title_1..4 stacked)
        if GameCanvas.images[30] is None:
            GameCanvas.images[30] = Image.createImage(240, 320)
            graphics = GameCanvas.images[30].getGraphics()
            for b in range(4):
                image = self.load_image("title_" + str(b + 1))
                graphics.drawImage(image, 0, 80 * b, 20)

    def load_menu_frames(self):  # ag.java:1165-1172
        GameCanvas.anim_step = 0
        while GameCanvas.anim_step < 4:
            GameCanvas.images[26 + GameCanvas.anim_step] = self.load_image(GameCanvas.scr_ui.get(73 + GameCanvas.anim_step))
            GameCanvas.anim_step += 1
        self.load_menu_images()

    def load_image(self, name):  # ag.java:1963-1975
        GameCanvas.gc()
        str_ = "/" + name + ".png"
        image = None
        try:
            image = Image.createImage(str_)
        except Exception:
            print("======== createMixImage failuer :" + name)
            return None
        GameCanvas.gc()
        return image

    @staticmethod
    def gc():  # ag.java:1977-1979  (System.gc)
        pass

    def load_ui_images(self):  # ag.java:2263-2269
        GameCanvas.images[34] = self.load_image(GameCanvas.scr_ui.get(22))
        GameCanvas.images[19] = self.load_image(GameCanvas.scr_ui.get(24))
        GameCanvas.images[20] = self.load_image(GameCanvas.scr_ui.get(25))
        GameCanvas.images[0] = self.load_image(GameCanvas.scr_ui.get(48))
        GameCanvas.images[32] = self.load_image(GameCanvas.scr_ui.get(37))

    @staticmethod
    def load_data_file(index):  # ag.java:2283-2285
        return ResReader.read("/" + GameCanvas.scr_data.get(index))

    def load_menu_images(self):  # ag.java:2306-2311
        GameCanvas.images[1] = self.load_image(GameCanvas.scr_ui.get(21))
        GameCanvas.images[2] = self.load_image(GameCanvas.scr_ui.get(46))
        GameCanvas.images[3] = self.load_image(GameCanvas.scr_ui.get(43))
        GameCanvas.sparkle = self.load_image(GameCanvas.scr_ui.get(38))

    def free_menu_images(self):  # ag.java:2313-2319
        GameCanvas.images[1] = None
        GameCanvas.images[2] = None
        GameCanvas.images[3] = None
        GameCanvas.sparkle = None
        GameCanvas.gc()

    def free_hero_sprites(self):  # ag.java:2400-2436
        GameCanvas.hero_weapon_frames[0] = None
        GameCanvas.hero_weapon_frames[1] = None
        GameCanvas.hero.head_frames2 = None
        GameCanvas.hero.body_frames2 = None
        GameCanvas.hero_body_frames[0] = None
        GameCanvas.hero_body_frames[1] = None
        GameCanvas.images[40] = None
        GameCanvas.images[41] = None
        if GameCanvas.tile_images is not None:
            for i in range(len(GameCanvas.tile_images)):
                GameCanvas.tile_images[i] = None
            GameCanvas.tile_images = None
        GameCanvas.trail_frames = None
        GameCanvas.images[42] = None
        GameCanvas.spark_frames = None
        GameCanvas.images[43] = None
        GameCanvas.shadow_image = None
        GameCanvas.shadow_frames = None
        GameCanvas.skill_frames = None
        GameCanvas.images[44] = None
        GameCanvas.images[31] = None
        GameCanvas.fire_frames = None
        GameCanvas.hero_fx_frames = None
        GameCanvas.boss_images[1] = None
        for b in range(2):
            GameCanvas.enemy_images[b] = None
        for b in range(9):
            GameCanvas.enemy_frames[b] = None
        GameCanvas.general_mark = None
        GameCanvas.view_size.x = GameCanvas.canvas_size.x
        GameCanvas.view_size.y = GameCanvas.canvas_size.y
        GameCanvas.view_x = 0
        GameCanvas.view_y = 0

    @staticmethod
    def free_hero_images():  # ag.java:2467-2472
        GameCanvas.hero.head_frames = None
        GameCanvas.hero.body_frames = None
        GameCanvas.hero.head_image = None
        GameCanvas.hero.body_image = None

    def load_hero_images(self):  # ag.java:3459-3465
        GameCanvas.free_hero_images()
        GameCanvas.hero.head_image = self.load_image(GameCanvas.scr_char.get(46 + GameCanvas.hero.head))
        GameCanvas.hero.head_frames = self.load_frames(47 + GameCanvas.hero.head)
        GameCanvas.hero.body_image = self.load_image(GameCanvas.scr_char.get(44))
        GameCanvas.hero.body_frames = self.load_frames(45)

    def load_frames(self, index):  # ag.java:3467-3482  (frame table from mdat_QVGA)
        pos = 1
        data = ResReader.read("/" + GameCanvas.scr_maps.get(index))
        count = data[0] & 0xFF
        frames = [None] * count
        for i in range(count):
            frames[i] = SpriteFrame()
            frames[i].src_x = GameCanvas.u16(data[pos], data[pos + 1])
            frames[i].src_y = GameCanvas.u16(data[pos + 2], data[pos + 3])
            frames[i].w = GameCanvas.u16(data[pos + 4], data[pos + 5])
            frames[i].h = GameCanvas.u16(data[pos + 6], data[pos + 7])
            frames[i].ox = GameCanvas.u16(data[pos + 8], data[pos + 9])
            frames[i].oy = GameCanvas.u16(data[pos + 10], data[pos + 11])
            pos += 12
        return frames

    def free_hud(self):  # ag.java:2277-2281
        for b in range(6):
            GameCanvas.hud_frame[b] = None
        GameCanvas.gc()

    def load_effect_image(self):  # ag.java:969-971
        GameCanvas.images[42] = self.load_image(GameCanvas.scr_effect.get(2))

    def load_enemy_sprites(self):  # ag.java:973-988  (enemy sprites, recoloured by dz.d)
        sprites = [56, 57]
        for b in range(len(sprites)):
            if GameCanvas.lords[GameCanvas.mission].tint != 0:
                GameCanvas.enemy_images[b] = None
                GameCanvas.enemy_frames[b] = None
                GameCanvas.enemy_images[b] = GameCanvas.load_recoloured(GameCanvas.scr_char.get(sprites[b]), GameCanvas.lords[GameCanvas.mission].tint)
            else:
                GameCanvas.enemy_images[b] = None
                GameCanvas.enemy_frames[b] = None
                GameCanvas.enemy_images[b] = self.load_image(GameCanvas.scr_char.get(sprites[b]))
            if GameCanvas.enemy_frames[b] is None:
                GameCanvas.enemy_frames[b] = self.load_frames(82 + b)

    _PAL = [[[236, 211, 197], [205, 143, 128], [129, 81, 69], [104, 60, 49], [79, 39, 29]],
            [[226, 205, 178], [196, 179, 152], [180, 142, 122], [135, 111, 47], [93, 73, 49]],
            [[174, 225, 242], [101, 156, 195], [61, 102, 139], [43, 78, 115], [45, 45, 84]],
            [[162, 199, 159], [135, 156, 119], [86, 123, 98], [33, 98, 63], [51, 51, 51]]]

    @staticmethod
    def load_recoloured(name, palette):  # ag.java:990-1023  (PNG with palette 0 replaced by palette paramInt)
        str_ = "/" + name + ".png"
        png = bytearray(ResReader.read(str_))
        if palette == 0:
            return Image.createImage(png, 0, len(png))
        palettes = GameCanvas._PAL
        size = len(png)
        plte = 0
        for pos in range(size - 4 + 1):
            if png[pos] == 80 and png[pos + 1] == 76 and png[pos + 2] == 84 and png[pos + 3] == 69:
                plte = pos
                break
        plte_len = png[plte - 1] & 0xFF | png[plte - 2] << 8 & 0xFF00
        for b in range(5):
            for pos in range(plte + 4, plte + plte_len - 3 + 1):
                if (png[pos] == palettes[0][b][0] and png[pos + 1] == palettes[0][b][1]
                        and png[pos + 2] == palettes[0][b][2]):
                    png[pos] = palettes[palette][b][0]
                    png[pos + 1] = palettes[palette][b][1]
                    png[pos + 2] = palettes[palette][b][2]
                    break
        crc = Gfx.crc32(png, plte, plte_len + 4)
        png[plte + plte_len + 4] = crc >> 24 & 0xFF
        png[plte + plte_len + 5] = crc >> 16 & 0xFF
        png[plte + plte_len + 6] = crc >> 8 & 0xFF
        png[plte + plte_len + 7] = crc & 0xFF
        return Image.createImage(png, 0, len(png))

    def load_lord_map(self, full):  # ag.java:1025-1037  (load the map of the current lord, room around the hero)
        from pow.game.map_scene import MapScene
        self.fill_screen_rgb(0, 0, 0)
        map_image = GameCanvas.images[34]
        self.draw_view_region(map_image, GameCanvas.canvas_size.x // 2 - map_image.getWidth() // 2, GameCanvas.canvas_size.y // 2 - map_image.getHeight() // 2,
                       map_image.getWidth(), map_image.getHeight(), 0, 0)
        GameCanvas.redraw = 1
        MapScene.hero_cell()
        GameCanvas.view_tx = idiv(GameCanvas.hero.room_pos[0].x - 1, 7) * 7 + 4 - (GameCanvas.view_tiles.x >> 1)
        GameCanvas.view_ty = idiv(GameCanvas.hero.room_pos[0].y - 1, 7) * 7 + 4 - (GameCanvas.view_tiles.y >> 1)
        GameCanvas.hero.room_pos[1].x = GameCanvas.hero.room_pos[0].x
        GameCanvas.hero.room_pos[1].y = GameCanvas.hero.room_pos[0].y
        GameCanvas.map = GameCanvas.scene.load_map(GameCanvas.map_id)
        GameCanvas.scene.load_rooms(GameCanvas.lord_ids[GameCanvas.lord])
        GameCanvas.scene.draw_tiles(GameCanvas.view_tiles.x, GameCanvas.view_tiles.y, GameCanvas.view_tx, GameCanvas.view_ty, full)

    def load_hud(self):  # ag.java:2271-2275  (HUD frame pieces)
        pieces = [79, 61, 82, 78, 83, 81]
        for b in range(6):
            GameCanvas.hud_frame[b] = self.load_image(GameCanvas.scr_ui.get(pieces[b]))

    def free_map_images(self):  # ag.java:2548-2570  (free the map images; `al` would hide the al class)
        GameCanvas.free_hero_images()
        GameCanvas.images[4] = None
        if GameCanvas.tile_images is not None:
            for i in range(len(GameCanvas.tile_images)):
                GameCanvas.tile_images[i] = None
            GameCanvas.tile_images = None
        GameCanvas.images[9] = None
        GameCanvas.images[11] = None
        GameCanvas.images[12] = None
        GameCanvas.images[16] = None
        GameCanvas.menus.free_shop_images()
        for b in range(5):
            GameCanvas.images[35 + b] = None
        for b in range(4):
            GameCanvas.images[21 + b] = None
        GameCanvas.view_size.x = GameCanvas.canvas_size.x
        GameCanvas.view_size.y = GameCanvas.canvas_size.y
        GameCanvas.view_x = 0
        GameCanvas.view_y = 0
