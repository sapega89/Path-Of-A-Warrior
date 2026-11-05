"""g.java, part of MpCanvas: loading and freeing images and sprites.

A mixin of MpCanvas (pow_mp/mp_canvas.py); the methods keep their `# g.java:FROM-TO`
comments. The module names below are set by mp_canvas.py: `MpCanvas` once the class exists,
the others by its _late_imports().
"""
from pow_mp.rt import (
    Image,
    _js,
    imod,
)

MpCanvas = None   # set by pow_mp/mp_canvas.py
SpriteFrames = None   # set by mp_canvas._late_imports


class AssetsMixin:
    def load_image(self, path):  # g.java:337
        image = None
        try:
            image = Image.createImage(path)
        except Exception as exception:
            MpCanvas.log(_js("--------createImage err:", exception))
        return image

    def load_ui_images(self):  # g.java:1706
        MpCanvas.ui_images[2] = self.load_image("/ui2.png")
        MpCanvas.ui_images[3] = self.load_image("/ui3.png")
        MpCanvas.ui_images[15] = self.load_image("/ui15.png")
        MpCanvas.ui_images[16] = self.load_image("/ui16.png")
        MpCanvas.ui_images[17] = self.load_image("/ui17.png")
        MpCanvas.ui_images[18] = self.load_image("/ui18.png")
        MpCanvas.ui_images[19] = self.load_image("/ui19.png")
        i = 0
        while i < 6:
            MpCanvas.act_images[i] = self.load_image(_js(_js("/act", i), ".png"))
            i = i + 1
        MpCanvas.arrow_images[1] = self.load_image("/menuarrow1.png")
        j = 0
        while j < 8:
            MpCanvas.number_images[j] = self.load_image(_js(_js("/gnum", j), ".png"))
            j = j + 1
        self.load_menu_images()

    def load_ui_images2(self):  # g.java:1728
        MpCanvas.ui_images[34] = self.load_image("/ui34.png")
        MpCanvas.ui_images[35] = self.load_image("/ui35.png")
        MpCanvas.ui_images[36] = self.load_image("/ui36.png")
        MpCanvas.ui_images[37] = self.load_image("/ui37.png")
        MpCanvas.ui_images[38] = self.load_image("/ui38.png")
        MpCanvas.ui_images[48] = self.load_image("/ui48.png")
        MpCanvas.ui_images[49] = self.load_image("/ui49.png")
        MpCanvas.ui_images[52] = self.load_image("/ui52.png")
        MpCanvas.ui_images[53] = self.load_image("/ui53.png")

    def load_menu_images(self):  # g.java:1740
        i = 0
        while i < 8:                   # PORT-EXTRA: mpic6 = Order, mpic7 = Chat
            if MpCanvas.mpic_images[i] is None:
                MpCanvas.mpic_images[i] = self.load_image(_js(_js("/mpic", i), ".png"))
            i = i + 1
        if MpCanvas.border_h_image is None:
            MpCanvas.border_h_image = self.load_image("/ui_borderh.png")
        if MpCanvas.border_v_image is None:
            MpCanvas.border_v_image = self.load_image("/ui_borderv.png")
        if MpCanvas.titlebox_image is None:
            MpCanvas.titlebox_image = self.load_image("/ui_titlebox.png")
        if MpCanvas.back_image is None:
            MpCanvas.back_image = self.load_image("/ui_back.png")
        if MpCanvas.menu_icon_image is None:
            MpCanvas.menu_icon_image = self.load_image("/ui_menuicon.png")

    def free_battle_images(self):  # g.java:1765
        j = 0
        MpCanvas.body_images[0] = None
        MpCanvas.body_images[1] = None
        i = 0
        while i < 3:
            if MpCanvas.body_frames[i] is not None:
                MpCanvas.body_frames[i].free()
            MpCanvas.body_frames[i] = None
            i = i + 1
        i = 0
        while i < 10:
            MpCanvas.head_images[i][0] = None
            MpCanvas.head_images[i][1] = None
            j = 0
            while j < 3:
                if MpCanvas.head_frames[i][j] is not None:
                    MpCanvas.head_frames[i][j].free()
                MpCanvas.head_frames[i][j] = None
                j = j + 1
            i = i + 1
        i = 0
        while i < 2:
            MpCanvas.weapon_images[i][0] = None
            MpCanvas.weapon_images[i][1] = None
            j = 0
            while j < 3:
                if MpCanvas.weapon_frames[i][j] is not None:
                    MpCanvas.weapon_frames[i][j].free()
                MpCanvas.weapon_frames[i][j] = None
                j = j + 1
            i = i + 1
        i = 0
        while i < 2:
            MpCanvas.sword_images[i][0] = None
            MpCanvas.sword_images[i][1] = None
            j = 0
            while j < 3:
                if MpCanvas.sword_frames[i][j] is not None:
                    MpCanvas.sword_frames[i][j].free()
                MpCanvas.sword_frames[i][j] = None
                j = j + 1
            i = i + 1
        i = 0
        while i < 2:
            MpCanvas.effect_images[i][0] = None
            MpCanvas.effect_images[i][1] = None
            j = 0
            while j < 3:
                if MpCanvas.effect_frames[i][j] is not None:
                    MpCanvas.effect_frames[i][j].free()
                MpCanvas.effect_frames[i][j] = None
                j = j + 1
            i = i + 1
        MpCanvas.shadow_images[0] = None
        MpCanvas.shadow_images[1] = None
        i = 0
        while i < 3:
            if MpCanvas.shadow_frames[i] is not None:
                MpCanvas.shadow_frames[i].free()
            MpCanvas.shadow_frames[i] = None
            i = i + 1
        MpCanvas.monster_images[0] = None
        MpCanvas.monster_images[1] = None
        if MpCanvas.monster_frames[0] is not None:
            MpCanvas.monster_frames[0].free()
        MpCanvas.monster_frames[0] = None
        MpCanvas.mon_weapon_images[0] = None
        MpCanvas.mon_weapon_images[1] = None
        if MpCanvas.mon_weapon_frames[0] is not None:
            MpCanvas.mon_weapon_frames[0].free()
        MpCanvas.mon_weapon_frames[0] = None
        MpCanvas.mon_effect_images[0] = None
        MpCanvas.mon_effect_images[1] = None
        if MpCanvas.mon_effect_frames[0] is not None:
            MpCanvas.mon_effect_frames[0].free()
        MpCanvas.mon_effect_frames[0] = None
        MpCanvas.mon_sword_images[0] = None
        MpCanvas.mon_sword_images[0] = None
        if MpCanvas.mon_sword_frames[0] is not None:
            MpCanvas.mon_sword_frames[0].free()
        MpCanvas.mon_sword_frames[0] = None
        i = 2
        while i < len(MpCanvas.act_images):
            MpCanvas.act_images[i] = None
            i = i + 1
        MpCanvas.ui_images[34] = None
        MpCanvas.ui_images[35] = None
        MpCanvas.ui_images[36] = None
        MpCanvas.ui_images[37] = None
        MpCanvas.ui_images[38] = None
        MpCanvas.ui_images[48] = None
        MpCanvas.ui_images[49] = None
        MpCanvas.ui_images[52] = None
        MpCanvas.ui_images[53] = None
        MpCanvas.noop()
        if MpCanvas.arrow_images[1] is None:
            MpCanvas.arrow_images[1] = self.load_image("/menuarrow1.png")
        self.load_menu_images()

    def free_frame_images(self):  # g.java:5026
        MpCanvas.border_h_image = None
        MpCanvas.border_v_image = None
        MpCanvas.titlebox_image = None
        MpCanvas.back_image = None
        MpCanvas.menu_icon_image = None
        i = 0
        while i < 8:
            MpCanvas.mpic_images[i] = None
            i = i + 1
        MpCanvas.arrow_images[1] = None
        MpCanvas.noop()
        self.load_ui_images2()
        MpCanvas.clear_fighters()
        MpCanvas.fighter_slot[0] = MpCanvas.my_slot
        MpCanvas.fighter_name[0] = MpCanvas.name
        MpCanvas.fighter_level[0] = MpCanvas.level
        MpCanvas.fighter_wins[0] = MpCanvas.wins
        MpCanvas.fighter_losses[0] = MpCanvas.losses
        MpCanvas.fighter_hp[0] = MpCanvas.hp
        MpCanvas.fighter_max_hp[0] = MpCanvas.fighter_hp[0]
        MpCanvas.fighter_mp[0] = 0
        MpCanvas.fighter_weapon[0] = MpCanvas.weapon
        MpCanvas.fighter_face[0] = MpCanvas.face
        MpCanvas.fighter_quote_start[0] = MpCanvas.quote_start
        MpCanvas.fighter_quote_win[0] = MpCanvas.quote_win
        MpCanvas.fighter_cr[0] = MpCanvas.profile_cr
        MpCanvas.fighter_present[0] = True
        MpCanvas.allies_alive = MpCanvas.allies_alive + 1
        MpCanvas.place_fighter(0)
        MpCanvas.fighter_blink[0] = imod(abs(MpCanvas.rng.nextInt()), 4)
        MpCanvas.fighter_status[0] = 99
        MpCanvas.fighter_status_ticks[0] = 0
        MpCanvas.hud_dirty = False
        MpCanvas.round_no = 0
        MpCanvas.exit_prompt = False
        self.push_state(90)
        self.stop_music()
        MpCanvas.room_dirty = True

    def load_numbered_image(self, images, name, index):  # g.java:5497
        if images[index] is None:
            images[index] = self.load_image(_js(_js(_js("/", name), index), ".png"))

    def load_named_image(self, images, name, index):  # g.java:5503
        if images[index] is None:
            images[index] = self.load_image(_js(_js("/", name), ".png"))

    def load_sprite(self, images, sets, name):  # g.java:5509
        self.load_sprite_dir(images, sets, name, 1)

    def load_sprite_dir(self, images, sets, name, single):  # g.java:5513
        if MpCanvas.draw_mirrored:
            if images[1] is None:
                images[1] = self.load_image(_js(_js("/", name), "_r.png"))
        elif images[0] is None:
            images[0] = self.load_image(_js(_js("/", name), ".png"))
        if sets[0] is None:
            if single == 0:
                sets[0] = SpriteFrames(_js(_js("/", name), ".SP2"))
                return
            if single == 1:
                sets[0] = SpriteFrames(_js(_js("/", name), "_basic.SP2"))
                sets[1] = SpriteFrames(_js(_js("/", name), "_skill1.SP2"))
                sets[2] = SpriteFrames(_js(_js("/", name), "_skill2.SP2"))

    def load_bg(self, index):  # g.java:5603
        if MpCanvas.bg_images[index] is None:
            MpCanvas.bg_images[index] = self.load_image(_js(_js("/gamebg", index), ".png"))
