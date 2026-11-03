"""MpCanvas (g.java): the canvas of the MP jar - screens, menus, battles.

Generated once from pyport/mp_java/g.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
from pow_mp.rt import (
    ByteArrayInputStream,
    DataInputStream,
    Image,
    Random,
    RecordStore,
    _Canvas,
    _arraycopy,
    _inc,
    _js,
    _set,
    i32,
    i8,
    idiv,
    imod,
    system,
)



class _Brk_block0_1631(BaseException):
    pass


class _Brk_block0_2273(BaseException):
    pass


class _Brk_block0_2989(BaseException):
    pass


class _Brk_block1_457(BaseException):
    pass


class _Brk_block4_3348(BaseException):
    pass


class _Brk_block5_3348(BaseException):
    pass


class _Cont_block47_2359(BaseException):
    pass


class _Cont_block49_2378(BaseException):
    pass


class MpCanvas(_Canvas):
    # PORT-EXTRA auto-battle: Tab (key -100) turns it on / off; the round's 1027 then goes out after
    # a second with action AUTO_ACTION, and the server's bot chooses (pow_server/battle.py cpu_choice)
    auto_battle = bool(getattr(__import__("config"), "AUTO_HUNT", False))
    AUTO_ACTION = 255
    app_version = None  # g.java:25 String
    game = None  # g.java:26 m
    title = None  # g.java:27 String
    timer_ticks = 0  # g.java:28 int
    screen_g = None  # g.java:29 Graphics
    buffer = None  # g.java:30 Image
    buffer_g = None  # g.java:31 Graphics
    rng = None  # g.java:32 Random
    user_id = None  # g.java:33 String
    password = None  # g.java:34 String
    menu_size = 0  # g.java:35 int
    midlet = None  # g.java:36 Main
    key = 0  # g.java:37 int
    font_white = None  # g.java:38 j
    font_orange = None  # g.java:39 j
    font_gray = None  # g.java:40 j
    font_green = None  # g.java:41 j
    server_host = None  # g.java:42 String
    server_port = 0  # g.java:43 int
    game_ver = None  # g.java:44 String
    wait_started = False  # g.java:45 boolean
    wait_start_time = 0  # g.java:46 long
    painting_blocked = False  # g.java:47 boolean
    popup_shown = False  # g.java:48 boolean
    popup_cursor = 0  # g.java:49 int
    popup_kind = 0  # g.java:50 int
    password_login = False  # g.java:51 boolean
    quote_step = 0  # g.java:52 int
    letter_cursor = 0  # g.java:53 int
    exit_prompt = False  # g.java:54 boolean
    exit_cursor = 0  # g.java:55 int
    exit_prompt_time = 0  # g.java:56 long
    exit_asked = False  # g.java:57 boolean
    pause_request = 0  # g.java:58 int
    music_to_resume = 0  # g.java:59 int
    paused = False  # g.java:60 boolean
    loop_started = False  # g.java:61 boolean
    connecting = False  # g.java:62 boolean
    logo_time = 0  # g.java:63 long
    login_time = 0  # g.java:64 long
    room_dirty = False  # g.java:65 boolean
    relogin_to_menu = False  # g.java:66 boolean
    anim_frame = 0  # g.java:67 int
    anim_length = 0  # g.java:68 int
    attacker = 0  # g.java:69 int
    target = 0  # g.java:70 int
    target2 = 0  # g.java:71 int
    target_reaction = 0  # g.java:72 int
    target2_reaction = 0  # g.java:73 int
    damage_tick = 0  # g.java:74 int
    rank_names = None  # g.java:75 String[]
    rank_ranks = None  # g.java:76 int[]
    rank_values = None  # g.java:77 int[]
    rank_list_kind = 0  # g.java:78 int
    my_ranks = None  # g.java:79 int[]
    my_rank_value = 0  # g.java:80 int
    rank_kind = 0  # g.java:81 byte
    rank_list_state = 0  # g.java:82 int
    popup_line1 = None  # g.java:83 String
    popup_line2 = None  # g.java:84 String
    popup_line3 = None  # g.java:85 String
    popup_line4 = None  # g.java:86 String
    popup_line5 = None  # g.java:87 String
    popup_style = 0  # g.java:88 int
    volume = 0  # g.java:89 int
    speed = 0  # g.java:90 int
    invitation_saved = 0  # g.java:91 int
    invitation = 0  # g.java:92 int
    skip_error_screen = False  # g.java:93 boolean
    face = 0  # g.java:94 byte
    level = 0  # g.java:95 int
    wins = 0  # g.java:96 int
    losses = 0  # g.java:97 int
    hp = 0  # g.java:98 int
    weapon = 0  # g.java:99 int
    fame = 0  # g.java:100 int
    exp = 0  # g.java:101 int
    gold = 0  # g.java:102 int
    duel_grade = 0  # g.java:103 int
    mission_grade = 0  # g.java:104 int
    attr_hp = 0  # g.java:105 int
    attr_hp_bonus = 0  # g.java:106 int
    attr_mp = 0  # g.java:107 int
    attr_mp_bonus = 0  # g.java:108 int
    attr_attack = 0  # g.java:109 int
    attr_attack_bonus = 0  # g.java:110 int
    attr_defense = 0  # g.java:111 int
    attr_defense_bonus = 0  # g.java:112 int
    profile_cr = 0  # g.java:113 int
    profile_unused1 = 0  # g.java:114 int
    profile_unused2 = 0  # g.java:115 int
    notices_left = 0  # g.java:116 byte
    notice_page = 0  # g.java:117 int
    stage_count = 0  # g.java:118 int
    stage = 0  # g.java:119 int
    round_no = 0  # g.java:120 int
    hit_score = 0  # g.java:121 int
    turn_record_count = 0  # g.java:122 int
    battle_won = 0  # g.java:123 int
    reward_gold = 0  # g.java:124 int
    reward_grade = 0  # g.java:125 byte
    reward_fame = 0  # g.java:126 int
    reward_exp = 0  # g.java:127 int
    reward_rank = 0  # g.java:128 int
    choose_secs = 0  # g.java:129 int
    allies_alive = 0  # g.java:130 int
    enemies_alive = 0  # g.java:131 int
    notice_kind = 0  # g.java:132 int
    help_page = 0  # g.java:133 int
    skill_count = 0  # g.java:134 int
    leaving_slot = 0  # g.java:135 int
    my_slot = 0  # g.java:136 byte
    slot_found = False  # g.java:137 boolean
    hud_dirty = False  # g.java:138 boolean
    show_record = False  # g.java:139 boolean
    run_dx = 0  # g.java:140 int
    run_dy = 0  # g.java:141 int
    draw_mirrored = False  # g.java:142 boolean
    saved_anim_frame = 0  # g.java:143 int
    skill_id = 0  # g.java:144 int
    skill_taken = False  # g.java:145 boolean
    number_negative = False  # g.java:146 boolean
    skill_ready = False  # g.java:147 boolean
    bar_shown = False  # g.java:148 boolean
    msg_first_line = 0  # g.java:149 int
    help_first_line = 0  # g.java:150 int
    msg_copy_line = False  # g.java:151 boolean
    card_half = False  # g.java:152 boolean
    room_bg = 0  # g.java:153 int
    room_mode = 0  # g.java:154 byte
    target_cursor = 0  # g.java:155 int
    chosen_action = 0  # g.java:156 int
    turn_rec = 0  # g.java:157 int
    skill_slot_count = 0  # g.java:158 int
    skill_slots = None  # g.java:159 byte[]
    notice_lines = None  # g.java:160 String[]
    input_text = None  # g.java:161 String
    stage_title = None  # g.java:162 String
    loot = None  # g.java:163 String
    tmp = 0  # g.java:164 int
    hp_bar_w = 0  # g.java:165 int
    stage_text = None  # g.java:166 String
    fighter_name = None  # g.java:167 String[]
    fighter_quote_start = None  # g.java:168 String[]
    fighter_quote_win = None  # g.java:169 String[]
    fighter_alt_name = None  # g.java:170 String[]
    fighter_present = None  # g.java:171 boolean[]
    fighter_slot = None  # g.java:172 int[]
    fighter_level = None  # g.java:173 int[]
    fighter_wins = None  # g.java:174 int[]
    fighter_losses = None  # g.java:175 int[]
    fighter_max_hp = None  # g.java:176 int[]
    fighter_hp = None  # g.java:177 int[]
    fighter_mp = None  # g.java:178 int[]
    fighter_weapon = None  # g.java:179 int[]
    fighter_face = None  # g.java:180 byte[]
    fighter_kind = None  # g.java:181 int[]
    turn_actions = None  # g.java:182 int[]
    fighter_anim = None  # g.java:183 int[]
    fighter_anim_tick = None  # g.java:184 int[]
    fighter_anim_len = None  # g.java:185 int[]
    fighter_hp_target = None  # g.java:186 int[]
    fighter_mp_target = None  # g.java:187 int[]
    fighter_hp_step = None  # g.java:188 int[]
    fighter_mp_step = None  # g.java:189 int[]
    fighter_hp_delta = None  # g.java:190 int[]
    fighter_x = None  # g.java:191 int[]
    fighter_y = None  # g.java:192 int[]
    fighter_fx_frame = None  # g.java:193 int[]
    fighter_frame = None  # g.java:194 int[]
    fighter_blink = None  # g.java:195 int[]
    fighter_status = None  # g.java:196 int[]
    fighter_status_ticks = None  # g.java:197 int[]
    fighter_cr = None  # g.java:198 int[]
    key_in = 0  # g.java:199 int
    cur_slot = 0  # g.java:200 int
    stat_value = 0  # g.java:201 int
    loading_msg = 0  # g.java:202 int
    error_msg = 0  # g.java:203 int
    win_x = 0  # g.java:204 int
    win_y = 0  # g.java:205 int
    bar_speed = 0  # g.java:206 int
    bar_x = 0  # g.java:207 int
    skill_order = None  # g.java:208 byte[]
    anim_id = 0  # g.java:209 int
    card_face = 0  # g.java:210 int
    name = None  # g.java:211 String
    quote_start = None  # g.java:212 String
    quote_win = None  # g.java:213 String
    skill_levels = None  # g.java:214 int[]
    skill_costs = None  # g.java:215 int[]
    turn_hps = None  # g.java:216 int[]
    turn_bytes = None  # g.java:217 byte[]
    loop_i = 0  # g.java:218 int
    loop_j = 0  # g.java:219 int
    loop_k = 0  # g.java:220 int
    box_x = 0  # g.java:221 int
    box_y = 0  # g.java:222 int
    canvas_w = 0  # g.java:223 int
    canvas_h = 0  # g.java:224 int
    screen_w = 0  # g.java:225 int
    screen_h = 0  # g.java:226 int
    draw_x = 0  # g.java:227 int
    draw_y = 0  # g.java:228 int
    center_x = 0  # g.java:229 int
    center_y = 0  # g.java:230 int
    state = 0  # g.java:231 int
    prev_state = 0  # g.java:232 int
    state_ticks = 0  # g.java:233 int
    skill_cursor = 0  # g.java:234 int
    tick_ms = 0  # g.java:235 int
    mpic_images = None  # g.java:236 Image[]
    face_images = None  # g.java:237 Image[]
    ui_images = None  # g.java:238 Image[]
    act_images = None  # g.java:239 Image[]
    number_images = None  # g.java:240 Image[]
    arrow_images = None  # g.java:241 Image[]
    bg_images = None  # g.java:242 Image[]
    border_v_image = None  # g.java:243 Image
    back_image = None  # g.java:244 Image
    border_h_image = None  # g.java:245 Image
    titlebox_image = None  # g.java:246 Image
    menu_icon_image = None  # g.java:247 Image
    title_image = None  # g.java:248 Image
    press_image = None  # g.java:249 Image
    gamevil_image = None  # g.java:250 Image
    logo_image = None  # g.java:251 Image
    softkey_image = None  # g.java:252 Image
    body_images = None  # g.java:253 Image[]
    body_frames = None  # g.java:254 a[]
    head_images = None  # g.java:255 Image[][]
    head_frames = None  # g.java:256 a[][]
    weapon_images = None  # g.java:257 Image[][]
    weapon_frames = None  # g.java:258 a[][]
    sword_images = None  # g.java:259 Image[][]
    sword_frames = None  # g.java:260 a[][]
    effect_images = None  # g.java:261 Image[][]
    effect_frames = None  # g.java:262 a[][]
    effect3_frames = None  # g.java:263 a[]
    shadow_images = None  # g.java:264 Image[]
    shadow_frames = None  # g.java:265 a[]
    monster_images = None  # g.java:266 Image[]
    monster_frames = None  # g.java:267 a[]
    mon_weapon_images = None  # g.java:268 Image[]
    mon_weapon_frames = None  # g.java:269 a[]
    mon_effect_images = None  # g.java:270 Image[]
    mon_effect_frames = None  # g.java:271 a[]
    mon_sword_images = None  # g.java:272 Image[]
    mon_sword_frames = None  # g.java:273 a[]
    net = None  # g.java:274 h
    request_opcode = 0  # g.java:275 int
    answer_status = 0  # g.java:276 int
    logo_y = 0  # g.java:277 int
    thread = None  # g.java:278 Thread
    cursor_stack = None  # g.java:279 int[]
    state_stack = None  # g.java:280 int[]
    stack_depth = 0  # g.java:281 int
    relogin = False  # g.java:282 boolean
    painted = False  # g.java:283 boolean
    ping_misses = 0  # g.java:284 int
    disconnecting = False  # g.java:285 boolean
    ping_off = False  # g.java:286 boolean
    pending_state = 0  # g.java:287 int
    text_lines = None  # g.java:288 String[]
    frame_start = 0  # g.java:289 long

    def __init__(self, main):  # g.java:295
        _Canvas.__init__(self)
        MpCanvas.midlet = main
        self.setFullScreenMode(True)

    @staticmethod
    def log(string):  # g.java:291
        print(_js(string))

    def init_screen(self):  # g.java:300
        MpCanvas.state_stack[0] = 1
        _t1 = self.getWidth()
        MpCanvas.canvas_w = _t1
        MpCanvas.screen_w = _t1
        _t2 = self.getHeight()
        MpCanvas.canvas_h = _t2
        MpCanvas.screen_h = _t2
        try:
            MpCanvas.app_version = MpCanvas.midlet.getAppProperty("MIDlet-Version")
            MpCanvas.server_host = MpCanvas.midlet.getAppProperty("GAMEVIL_SERVER")
            MpCanvas.server_port = int(MpCanvas.midlet.getAppProperty("GAMEVIL_PORT"))
            MpCanvas.game_ver = MpCanvas.midlet.getAppProperty("GAMEVIL_GAME_VER")
        except Exception:
            MpCanvas.app_version = ""
            MpCanvas.server_host = "64.14.246.182"
            MpCanvas.server_port = 28200
            MpCanvas.game_ver = "0111"
        MpCanvas.buffer = Image.createImage(MpCanvas.canvas_w, MpCanvas.canvas_h)
        MpCanvas.buffer_g = MpCanvas.buffer.getGraphics()
        MpCanvas.center_x = idiv(MpCanvas.canvas_w, 2)
        MpCanvas.center_y = idiv(MpCanvas.canvas_h, 2)
        MpCanvas.hp_bar_w = ((idiv(MpCanvas.canvas_w, 2) - 28) - 3)
        n2 = 0
        while n2 < 4:
            MpCanvas.fighter_alt_name[n2] = ""
            n2 = n2 + 1
        MpCanvas.font_white = Font("/0_font.png", 5, 11, 6, 0xFFFFFF)
        MpCanvas.font_orange = Font("/0_font.png", 5, 11, 6, 16400640)
        MpCanvas.font_gray = Font("/0_font.png", 5, 11, 6, 0x646464)
        MpCanvas.font_green = Font("/0_font.png", 5, 11, 6, 0x41FF41)
        self.load_ui_images()
        self.load_options()
        MpCanvas.game = MpGame(MpCanvas.midlet)
        MpCanvas.noop()
        MpCanvas.set_state(0)

    def load_image(self, string):  # g.java:337
        image = None
        try:
            image = Image.createImage(string)
        except Exception as exception:
            MpCanvas.log(_js("--------createImage err:", exception))
        return image

    @staticmethod
    def draw_menu_cursor(graphics):  # g.java:348
        n2 = idiv(80, MpCanvas.menu_size)
        if n2 > 30:
            n2 = 30
        elif n2 < 19:
            n2 = 19
        n3 = 0
        if ((MpCanvas.state == 162) or (MpCanvas.state == 163)) or (MpCanvas.state == 164):
            n3 = 15
        elif MpCanvas.state == 10:
            n3 = 40
        Draw.draw_image_part(graphics, MpCanvas.menu_icon_image, (idiv((((MpCanvas.canvas_w - (n2 * ((MpCanvas.menu_size - 1)))) - 11)), 2) + (n2 * MpCanvas.cursor_stack[MpCanvas.stack_depth])), ((MpCanvas.center_y + 6) + n3), 12, 15, 0, 0)

    def paint(self, graphics):  # g.java:364
        MpCanvas.screen_g = graphics
        Gfx.set_graphics(graphics)
        if MpCanvas.painting_blocked:
            MpCanvas.painted = True
            return
        self.paint_screen()
        if MpCanvas.auto_battle and 94 <= MpCanvas.state <= 98:     # PORT-EXTRA: auto-battle badge
            self.draw_text_left_on(graphics, 4, MpCanvas.canvas_h - 30, "AUTO", 16400640)
        if graphics.getClipX() > 0:
            graphics.setClip(0, 0, MpCanvas.canvas_w, MpCanvas.canvas_h)
        MpCanvas.painted = True

    @staticmethod
    def sleep(l2):  # g.java:378
        if l2 > 0:
            try:
                system.sleep(l2)
                return
            except Exception:
                pass

    @staticmethod
    def request_pause(n2):  # g.java:388
        MpCanvas.pause_request = n2

    def apply_pause(self):  # g.java:392
        if (not MpCanvas.loop_started) or MpCanvas.connecting:
            MpCanvas.pause_request = 0
            return
        if (MpCanvas.pause_request != 0) and ((MpCanvas.pause_request == 1) != MpCanvas.paused):
            if MpCanvas.pause_request == 1:
                MpCanvas.paused = True
                if MpCanvas.game is not None:
                    MpCanvas.music_to_resume = MpGame.music
                    self.stop_music()
            elif MpCanvas.pause_request == 2:
                MpCanvas.paused = False
                if (MpCanvas.game is not None) and (MpCanvas.music_to_resume != (-1)):
                    self.start_sound(MpCanvas.music_to_resume)
        MpCanvas.pause_request = 0

    def run(self):  # g.java:414
        g2 = self
        self.init_screen()
        self.main_loop()
        MpCanvas.sleep(250)

    def main_loop(self):  # g.java:423
        MpCanvas.frame_start = system.currentTimeMillis()
        while True:
            MpCanvas.frame_start = system.currentTimeMillis()
            if MpCanvas.paused:
                if MpCanvas.key != (-999):
                    self.handle_key(MpCanvas.key)
                    MpCanvas.key = (-999)
                MpCanvas.painted = False
                self.repaint()
                MpCanvas.sleep(250)
            else:
                l2 = 0
                n2 = 0
                if MpCanvas.key != (-999):
                    self.handle_key(MpCanvas.key)
                    MpCanvas.key = (-999)
                MpCanvas.painted = False
                self.repaint()
                self.serviceRepaints()
                while not MpCanvas.painted:
                    MpCanvas.sleep(10)
                if MpCanvas.game is not None:
                    if ((((((MpCanvas.state >= 10) and (MpCanvas.state <= 89)) and (MpCanvas.state != 88)) and (not MpCanvas.paused)) or (MpCanvas.state == 1)) or (MpCanvas.state == 6)) or (MpCanvas.state == 7):
                        self.start_music(1)
                    MpCanvas.game.tick_music()
                if (MpCanvas.prev_state == MpCanvas.state) and (MpCanvas.state_ticks < 25000):
                    MpCanvas.state_ticks = MpCanvas.state_ticks + 1
                if MpCanvas.state_ticks >= 25000:
                    MpCanvas.state_ticks = 100
                if ((n2 := (Consts.speed_frame_ms[MpCanvas.speed] - i32(((((l2 := system.currentTimeMillis())) - MpCanvas.frame_start)))))) > 20:
                    MpCanvas.sleep(n2)
                else:
                    MpCanvas.sleep(20)
            self.apply_pause()
            MpCanvas.loop_started = True

    def paint_screen(self):  # g.java:474
        if MpCanvas.painted:
            return
        if (MpCanvas.state != 3) and (MpCanvas.state != 10000):
            MpCanvas.connecting = False
        if MpCanvas.paused:
            Draw.fill_rect(MpCanvas.screen_g, 0, 0, MpCanvas.screen_w, MpCanvas.screen_h, 0)
            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 100, 29, 0)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[2], MpCanvas.center_x, (MpCanvas.center_y - 6), 1, 0xFFFFFF)
            return
        if NetThread.connected and (not MpCanvas.ping_off):
            if NetThread.idle_frames > 100:
                NetThread.idle_frames = 0
                self.send_request(39327)
                if _inc(MpCanvas, 'ping_misses', 1) > 20:
                    MpCanvas.ping_misses = 0
                    MpCanvas.error_msg = 13
                    MpCanvas.popup_shown = False
                    self.on_disconnect()
            else:
                NetThread.idle_frames = NetThread.idle_frames + 1
        if not MpCanvas.exit_prompt:
            if MpCanvas.timer_ticks == 1:
                MpCanvas.timer_ticks = 0
                if MpCanvas.state == 97:
                    if (_set(MpCanvas, 'bar_x', (MpCanvas.bar_x + MpCanvas.bar_speed))) > (((MpCanvas.center_x - 44) + 72) + MpCanvas.bar_speed):
                        MpCanvas.bar_x = (((MpCanvas.center_x - 44) + 72) + MpCanvas.bar_speed)
                    else:
                        MpCanvas.set_timer(1)
                else:
                    if _inc(MpCanvas, 'choose_secs', -1) == 0:
                        # PORT-EXTRA: on auto-battle the time-out sends AUTO instead of Defend
                        MpCanvas.chosen_action = MpCanvas.AUTO_ACTION if MpCanvas.auto_battle else 1
                        MpCanvas.bar_x = (((MpCanvas.center_x - 44) + 72) + MpCanvas.bar_speed)
                        self.stop_timing()
                    MpCanvas.set_timer((10 - MpCanvas.speed))
            elif MpCanvas.timer_ticks > 0:
                MpCanvas.timer_ticks = MpCanvas.timer_ticks - 1
        MpCanvas.prev_state = MpCanvas.state
        _sw3 = MpCanvas.state
        try:
            _m4 = False
            while True:
                if _m4 or _sw3 == 0:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        try:
                            MpCanvas.logo_image = self.load_image("/gamevillogo.png")
                            MpCanvas.softkey_image = self.load_image("/softbg.png")
                            MpCanvas.logo_y = idiv(((MpCanvas.canvas_h - ((MpCanvas.logo_image.getHeight() + 12)))), 2)
                            MpCanvas.logo_image.getHeight()
                            MpCanvas.logo_image.getWidth()
                        except Exception:
                            pass
                        MpCanvas.logo_time = system.currentTimeMillis()
                        Draw.fill_rect(MpCanvas.buffer_g, 0, 0, MpCanvas.canvas_w, MpCanvas.canvas_h, 0xFFFFFF)
                    self.draw_buffer()
                    Draw.draw_image(MpCanvas.screen_g, MpCanvas.logo_image, idiv(MpCanvas.canvas_w, 2), MpCanvas.logo_y, 17)
                    if (system.currentTimeMillis() - MpCanvas.logo_time) <= 3000:
                        break
                    MpCanvas.logo_image = None
                    MpCanvas.state = 5
                    return
                if _m4 or _sw3 == 161:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.main_menu[5]
                        MpCanvas.menu_size = 3
                        self.draw_menu_icons()
                    self.draw_buffer()
                    self.draw_button(MpCanvas.screen_g, Consts.rank_menu[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 43), (MpCanvas.center_y - 19), 86, 17, False, True)
                    MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
                    self.draw_softkeys((-1), 1)
                    return
                if _m4 or _sw3 in (162, 163, 164):
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.rank_menu[(MpCanvas.state - 162)]
                        MpCanvas.menu_size = 2
                        self.draw_menu_icons()
                        MpCanvas.box_x = ((MpCanvas.canvas_w - 96) >> 1)
                        MpCanvas.draw_panel(MpCanvas.buffer_g, MpCanvas.box_x, (MpCanvas.center_y - 54), 96, 15)
                        self.draw_text_colored(MpCanvas.buffer_g, MpCanvas.user_id, (idiv(MpCanvas.canvas_w, 2) + 4), ((MpCanvas.center_y + 2) - 54), 1, 0xFFFFFF)
                        MpCanvas.draw_panel(MpCanvas.buffer_g, MpCanvas.box_x, ((MpCanvas.center_y + 14) - 54), 96, 15)
                        self.draw_text_colored(MpCanvas.buffer_g, Consts.texts[4], (MpCanvas.box_x + 3), (((MpCanvas.center_y + 14) + 2) - 54), 0, 0xFFFFFF)
                        MpCanvas.draw_number(MpCanvas.buffer_g, ((MpCanvas.box_x + 96) - 7), (((MpCanvas.center_y + 14) + 3) - 54), MpCanvas.my_ranks[MpCanvas.rank_kind], 0)
                        _sw5 = MpCanvas.state
                        if _sw5 == 162:
                            var1_1 = Consts.rank_menu[0]
                        else:
                            var1_1 = Consts.texts[3]
                        MpCanvas.draw_panel(MpCanvas.buffer_g, MpCanvas.box_x, ((MpCanvas.center_y + 28) - 54), 96, 15)
                        self.draw_text_colored(MpCanvas.buffer_g, var1_1, (MpCanvas.box_x + 3), (((MpCanvas.center_y + 28) + 2) - 54), 0, 0xFFFFFF)
                        MpCanvas.draw_number(MpCanvas.buffer_g, ((MpCanvas.box_x + 96) - 7), (((MpCanvas.center_y + 28) + 3) - 54), MpCanvas.my_rank_value, 0)
                    self.draw_buffer()
                    self.draw_button(MpCanvas.screen_g, Consts.rank_view_menu[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 43), ((MpCanvas.center_y - 19) + 15), 86, 17, False, True)
                    MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
                    self.draw_softkeys((-1), 1)
                    return
                if _m4 or _sw3 in (170, 171):
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.rank_view_menu[(MpCanvas.state - 170)]
                        self.draw_window_bg(MpCanvas.buffer_g)
                        var1_2 = ((MpCanvas.canvas_w - 110) >> 1)
                        var2_7 = (MpCanvas.canvas_h >> 1)
                        _sw6 = MpCanvas.rank_list_state
                        if _sw6 == 162:
                            var3_14 = Consts.rank_menu[0]
                        elif _sw6 == 163:
                            var3_14 = Consts.texts[3]
                        else:
                            var3_14 = Consts.texts[3]
                        var4_16 = 0
                        while var4_16 < 3:
                            self.draw_text_colored(MpCanvas.buffer_g, MpCanvas.rank_names[var4_16], MpCanvas.center_x, ((var2_7 - 65) + (45 * var4_16)), 1, 0xFFFFFF)
                            MpCanvas.draw_panel(MpCanvas.buffer_g, var1_2, ((var2_7 - 52) + (45 * var4_16)), 110, 15)
                            MpCanvas.draw_panel(MpCanvas.buffer_g, var1_2, ((var2_7 - 38) + (45 * var4_16)), 110, 15)
                            self.draw_text_colored(MpCanvas.buffer_g, Consts.texts[4], (var1_2 + 3), (((var2_7 - 52) + 2) + (45 * var4_16)), 0, 0xFFFFFF)
                            MpCanvas.draw_number(MpCanvas.buffer_g, ((var1_2 + 110) - 7), ((((var2_7 - 52) + 2) + 1) + (45 * var4_16)), MpCanvas.rank_ranks[var4_16], 0)
                            self.draw_text_colored(MpCanvas.buffer_g, var3_14, (var1_2 + 3), (((var2_7 - 38) + 2) + (45 * var4_16)), 0, 0xFFFFFF)
                            MpCanvas.draw_number(MpCanvas.buffer_g, ((var1_2 + 110) - 7), ((((var2_7 - 38) + 2) + 1) + (45 * var4_16)), MpCanvas.rank_values[var4_16], 0)
                            var4_16 = var4_16 + 1
                    self.draw_buffer()
                    self.draw_softkeys((-1), 1)
                    return
                if _m4 or _sw3 == 90:
                    _m4 = True
                    if MpCanvas.room_dirty:
                        self.draw_background()
                        self.draw_hp_bar_frames()
                        MpCanvas.room_dirty = False
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.show_record = False
                    if MpCanvas.hud_dirty:
                        if MpCanvas.fighter_kind[MpCanvas.cur_slot] == 0:
                            MpCanvas.show_record = True
                        self.draw_battle_hud(MpCanvas.buffer_g)
                        MpCanvas.hud_dirty = False
                    self.draw_buffer()
                    self.draw_fighters(MpCanvas.screen_g)
                    if MpCanvas.show_record:
                        self.draw_fighter_record()
                        break
                    self.draw_waiting()
                    return
                if _m4 or _sw3 == 91:
                    _m4 = True
                    self.draw_buffer()
                    self.draw_fighters(MpCanvas.screen_g)
                    self.draw_stage_intro()
                    if MpCanvas.state_ticks != idiv(1500, MpCanvas.tick_ms):
                        break
                    self.send_request(1038)
                    return
                if _m4 or _sw3 == 92:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                    self.draw_buffer()
                    self.draw_fighters(MpCanvas.screen_g)
                    if (MpCanvas.state_ticks >= idiv(500, MpCanvas.tick_ms)) and (MpCanvas.state_ticks < idiv(1500, MpCanvas.tick_ms)):
                        self.draw_quotes(MpCanvas.screen_g, 0)
                    elif MpCanvas.state_ticks >= idiv(1500, MpCanvas.tick_ms):
                        self.draw_quotes(MpCanvas.screen_g, 1)
                    if MpCanvas.state_ticks != idiv(2500, MpCanvas.tick_ms):
                        break
                    MpCanvas.round_no = 0
                    MpCanvas.set_state(93)
                    return
                if _m4 or _sw3 == 93:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.noop()
                        MpCanvas.state_ticks = 2
                        MpCanvas.round_no = MpCanvas.round_no + 1
                        if ((MpCanvas.allies_alive == 0) or (MpCanvas.enemies_alive == 0)) or (MpCanvas.fighter_hp[0] == 0):
                            MpCanvas.set_state(103)
                        else:
                            MpCanvas.tick_status_effects()
                    elif MpCanvas.state_ticks == idiv(1000, MpCanvas.tick_ms):
                        self.send_request(1025)
                    self.draw_buffer()
                    self.draw_fighters(MpCanvas.screen_g)
                    if ((((MpCanvas.round_no > 0) and (MpCanvas.round_no < 100)) and (MpCanvas.allies_alive != 0)) and (MpCanvas.enemies_alive != 0)) and (MpCanvas.fighter_hp[0] != 0):
                        self.draw_round(MpCanvas.screen_g)
                        self.draw_battle_prompt(MpCanvas.screen_g, 2)
                        self.check_invite_timeout()
                    return
                if _m4 or _sw3 == 94:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.bar_shown = False
                    self.draw_buffer()
                    if MpCanvas.exit_prompt:
                        MpCanvas.ping_misses = 1
                        MpCanvas.state_ticks = MpCanvas.state_ticks - 1
                        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 120, 100, 0)
                        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) - 10), Consts.texts[60], 0xFFFFFF)
                        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) + 2), Consts.texts[61], 0xFFFFFF)
                        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) + 14), Consts.texts[62], 0xFFFFFF)
                        var1_3 = i32(((15 - idiv(((system.currentTimeMillis() - MpCanvas.exit_prompt_time)), 1000))))
                        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) + 30), _js(Consts.texts[63], "   "), 0xFFFFFF)
                        self.draw_text_centred_on(MpCanvas.screen_g, (MpCanvas.center_x + 35), ((MpCanvas.center_y - 21) + 30), _js("", var1_3), 16400640)
                        var2_8 = 0
                        while var2_8 < 2:
                            if MpCanvas.exit_cursor == var2_8:
                                self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(40 + var2_8)], ((MpCanvas.center_x - 28) + (var2_8 * 55)), (MpCanvas.center_y + 28), 1, 0xFFFFFF)
                                self.draw_box(MpCanvas.screen_g, ((MpCanvas.center_x - 42) + (var2_8 * 55)), (MpCanvas.center_y + 25), 29, 14, 3)
                            else:
                                self.draw_box(MpCanvas.screen_g, ((MpCanvas.center_x - 42) + (var2_8 * 55)), (MpCanvas.center_y + 25), 29, 14, 2)
                                self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(40 + var2_8)], ((MpCanvas.center_x - 28) + (var2_8 * 55)), (MpCanvas.center_y + 28), 1, 0x646464)
                            var2_8 = var2_8 + 1
                        if var1_3 > 0:
                            break
                        MpCanvas.exit_prompt = False
                        break
                    self.draw_fighters(MpCanvas.screen_g)
                    MpCanvas.draw_action_pad(MpCanvas.screen_g)
                    self.draw_battle_prompt(MpCanvas.screen_g, 0)
                    return
                if _m4 or _sw3 == 95:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.skill_cursor = 0
                    self.draw_buffer()
                    self.draw_fighters(MpCanvas.screen_g)
                    self.draw_skill_menu(MpCanvas.screen_g)
                    self.draw_battle_prompt(MpCanvas.screen_g, 1)
                    return
                if _m4 or _sw3 == 96:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        _sw7 = MpCanvas.chosen_action
                        _m8 = False
                        while True:
                            if _m8 or _sw7 in (9, 10):
                                _m8 = True
                                MpCanvas.target_cursor = 0
                                if MpCanvas.allies_alive > 1:
                                    break
                                self.start_timing()
                                return
                            if _m8 or _sw7 in (0, 3, 4, 5, 6, 7):
                                _m8 = True
                                MpCanvas.loop_i = 1
                                while MpCanvas.loop_i < 4:
                                    if MpCanvas.fighter_present[MpCanvas.loop_i] and (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) != imod(MpCanvas.fighter_slot[0], 2)):
                                        MpCanvas.target_cursor = MpCanvas.loop_i
                                        break
                                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                                if MpCanvas.enemies_alive > 1:
                                    break
                            if _m8 or _sw7 not in (9, 10, 0, 3, 4, 5, 6, 7):
                                _m8 = True
                                self.start_timing()
                            break
                    self.draw_buffer()
                    self.draw_fighters(MpCanvas.screen_g)
                    MpCanvas.draw_action_pad(MpCanvas.screen_g)
                    self.draw_target_marker(MpCanvas.screen_g)
                    self.draw_battle_prompt(MpCanvas.screen_g, 1)
                    return
                if _m4 or _sw3 == 97:
                    _m4 = True
                    self.draw_buffer()
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        if MpCanvas.chosen_action > 2:
                            self.draw_fighters(MpCanvas.screen_g)
                            MpCanvas.draw_action_pad(MpCanvas.screen_g)
                            self.stop_timing()
                            return
                        self.draw_fighters(MpCanvas.screen_g)
                        MpCanvas.draw_action_pad(MpCanvas.screen_g)
                        MpCanvas.start_timing_bar()
                        self.draw_timing_bar(MpCanvas.screen_g)
                        self.draw_timing_cursor(MpCanvas.screen_g)
                        return
                    if MpCanvas.state_ticks > 0:
                        self.draw_fighters(MpCanvas.screen_g)
                        MpCanvas.draw_action_pad(MpCanvas.screen_g)
                        self.draw_timing_bar(MpCanvas.screen_g)
                        self.draw_timing_cursor(MpCanvas.screen_g)
                        return
                    self.draw_fighters(MpCanvas.screen_g)
                    MpCanvas.draw_action_pad(MpCanvas.screen_g)
                    self.draw_timing_bar(MpCanvas.screen_g)
                    self.draw_timing_cursor(MpCanvas.screen_g)
                    return
                if _m4 or _sw3 == 98:
                    _m4 = True
                    self.draw_buffer()
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        self.draw_fighters(MpCanvas.screen_g)
                        MpCanvas.draw_action_pad(MpCanvas.screen_g)
                        self.draw_timing_bar(MpCanvas.screen_g)
                        if (MpCanvas.chosen_action <= 2) and MpCanvas.bar_shown:
                            self.draw_timing_cursor(MpCanvas.screen_g)
                    elif MpCanvas.state_ticks == 4:
                        self.draw_fighters(MpCanvas.screen_g)
                        MpCanvas.draw_action_pad(MpCanvas.screen_g)
                        self.draw_timing_bar(MpCanvas.screen_g)
                        self.send_request(1027)
                    else:
                        self.draw_fighters(MpCanvas.screen_g)
                        MpCanvas.draw_action_pad(MpCanvas.screen_g)
                        if MpCanvas.state_ticks < 4:
                            self.draw_timing_bar(MpCanvas.screen_g)
                    if MpCanvas.state_ticks < 4:
                        break
                    self.draw_battle_prompt(MpCanvas.screen_g, 2)
                    self.check_invite_timeout()
                    return
                if _m4 or _sw3 == 99:
                    _m4 = True
                    self.draw_buffer()
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                    self.draw_fighters(MpCanvas.screen_g)
                    self.draw_action_cards()
                    if MpCanvas.state_ticks < 4:
                        return
                    MpCanvas.turn_rec = 0
                    self.next_turn_record()
                    return
                if _m4 or _sw3 == 100:
                    _m4 = True
                    self.draw_buffer()
                    self.draw_fighters(MpCanvas.screen_g)
                    self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 25), 80, 20, 0)
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 6) - 25), Consts.texts[8], 0xFFFFFF)
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        return
                    if MpCanvas.state_ticks != idiv(1000, MpCanvas.tick_ms):
                        break
                    MpCanvas.set_state(93)
                    return
                if _m4 or _sw3 == 101:
                    _m4 = True
                    self.draw_buffer()
                    self.draw_fighters(MpCanvas.screen_g)
                    self.reset_turn()
                    MpCanvas.set_state(102)
                    return
                if _m4 or _sw3 == 102:
                    _m4 = True
                    self.draw_buffer()
                    self.draw_turn_fighters()
                    self.draw_action_cards()
                    self.draw_damage()
                    MpCanvas.anim_frame = MpCanvas.anim_frame + 1
                    self.step_turn_anim()
                    return
                if _m4 or _sw3 == 103:
                    _m4 = True
                    self.draw_buffer()
                    self.draw_fighters(MpCanvas.screen_g)
                    if MpCanvas.state_ticks >= 2:
                        break
                    MpCanvas.state_ticks = 2
                    self.send_request(1025)
                    return
                if _m4 or _sw3 == 104:
                    _m4 = True
                    self.draw_buffer()
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.body_images[0] = None
                        MpCanvas.body_images[1] = None
                        var1_4 = 0
                        while var1_4 < 3:
                            if MpCanvas.body_frames[var1_4] is not None:
                                MpCanvas.body_frames[var1_4].free()
                            MpCanvas.body_frames[var1_4] = None
                            var1_4 = var1_4 + 1
                        var1_4 = 0
                        while var1_4 < 10:
                            MpCanvas.head_images[var1_4][0] = None
                            MpCanvas.head_images[var1_4][1] = None
                            var2_9 = 0
                            while var2_9 < 3:
                                if MpCanvas.head_frames[var1_4][var2_9] is not None:
                                    MpCanvas.head_frames[var1_4][var2_9].free()
                                MpCanvas.head_frames[var1_4][var2_9] = None
                                var2_9 = var2_9 + 1
                            var1_4 = var1_4 + 1
                        var1_4 = 0
                        while var1_4 < 2:
                            MpCanvas.weapon_images[var1_4][0] = None
                            MpCanvas.weapon_images[var1_4][1] = None
                            var2_9 = 0
                            while var2_9 < 3:
                                if MpCanvas.weapon_frames[var1_4][var2_9] is not None:
                                    MpCanvas.weapon_frames[var1_4][var2_9].free()
                                MpCanvas.weapon_frames[var1_4][var2_9] = None
                                var2_9 = var2_9 + 1
                            var1_4 = var1_4 + 1
                        MpCanvas.noop()
                    if MpCanvas.state_ticks < idiv(1000, MpCanvas.tick_ms):
                        self.draw_fighters(MpCanvas.screen_g)
                        self.draw_stage_complete()
                        return
                    if MpCanvas.state_ticks == idiv(1000, MpCanvas.tick_ms):
                        self.draw_fighters(MpCanvas.screen_g)
                        MpCanvas.loop_i = 1
                        while MpCanvas.loop_i < 4:
                            if MpCanvas.fighter_present[MpCanvas.loop_i] and (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) != imod(MpCanvas.fighter_slot[0], 2)):
                                MpCanvas.fighter_present[MpCanvas.loop_i] = False
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        MpCanvas.enemies_alive = 0
                        self.send_request(1036)
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < 4:
                            MpCanvas.fighter_status[MpCanvas.loop_i] = 99
                            MpCanvas.fighter_status_ticks[MpCanvas.loop_i] = 0
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        MpCanvas.set_state(90)
                        MpCanvas.room_dirty = True
                        return
                    self.draw_fighters(MpCanvas.screen_g)
                    return
                if _m4 or _sw3 == 105:
                    _m4 = True
                    self.draw_buffer()
                    if MpCanvas.state_ticks < 5:
                        MpCanvas.state_ticks = 5
                        self.free_battle_images()
                        if MpCanvas.battle_won == 1:
                            self.start_sound(5)
                        else:
                            self.start_sound(4)
                    if MpCanvas.state_ticks < idiv(1500, MpCanvas.tick_ms):
                        MpCanvas.draw_hp_bars(MpCanvas.screen_g)
                        self.draw_fighters(MpCanvas.screen_g)
                        self.draw_quotes(MpCanvas.screen_g, 2)
                        return
                    if MpCanvas.state_ticks < idiv(1500, MpCanvas.tick_ms):
                        break
                    MpCanvas.draw_hp_bars(MpCanvas.screen_g)
                    self.draw_fighters(MpCanvas.screen_g)
                    self.draw_battle_result()
                    return
                if _m4 or _sw3 == 10:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        var1_5 = 0
                        while var1_5 < len(MpCanvas.face_images):
                            MpCanvas.face_images[var1_5] = None
                            var1_5 = var1_5 + 1
                        self.free_battle_images()
                        MpCanvas.title = Consts.texts[9]
                        MpCanvas.menu_size = 6
                        self.draw_menu_icons()
                    self.draw_buffer()
                    Draw.draw_image(MpCanvas.screen_g, MpCanvas.mpic_images[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 40), (MpCanvas.center_y - 59), 0)
                    self.draw_button(MpCanvas.screen_g, Consts.main_menu[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 39), (MpCanvas.center_y + 21), 78, 17, False, True)
                    MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
                    if MpCanvas.popup_shown:
                        self.draw_exit_confirm(MpCanvas.screen_g)
                        break
                    self.draw_softkeys(5, 2)
                    return
                if _m4 or _sw3 == 11:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.main_menu[0]
                        MpCanvas.menu_size = 3
                        self.draw_menu_icons()
                    Draw.draw_image(MpCanvas.screen_g, MpCanvas.buffer, 0, 0, 0)
                    self.draw_button(MpCanvas.screen_g, Consts.duel_menu[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 39), (MpCanvas.center_y - 19), 78, 17, False, True)
                    MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
                    self.draw_softkeys((-1), 1)
                    return
                if _m4 or _sw3 == 12:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.main_menu[1]
                        MpCanvas.menu_size = 2
                        self.draw_menu_icons()
                    self.draw_buffer()
                    self.draw_button(MpCanvas.screen_g, Consts.mission_menu[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 45), (MpCanvas.center_y - 19), 90, 17, False, True)
                    MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
                    self.draw_softkeys((-1), 1)
                    return
                if _m4 or _sw3 == 16:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.main_menu[2]
                        MpCanvas.menu_size = 6
                        self.draw_menu_icons()
                    self.draw_buffer()
                    self.draw_button(MpCanvas.screen_g, Consts.character_menu[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 45), (MpCanvas.center_y - 19), 90, 17, False, True)
                    MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
                    self.draw_softkeys((-1), 1)
                    return
                if _m4 or _sw3 == 20:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.menu_size = 2
                        self.draw_challenge_bg(MpCanvas.buffer_g)
                    self.draw_buffer()
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 2:
                        if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 56), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 20)), 111, 14, 3)
                            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(38 + MpCanvas.loop_i)], idiv(MpCanvas.screen_w, 2), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 20)), 1, 0xFFFFFF)
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    self.draw_softkeys((-1), 1)
                    return
                if _m4 or _sw3 == 21:
                    _m4 = True
                    var1_6 = (MpCanvas.center_y - 48)
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.letter_cursor = 0
                        MpCanvas.input_text = ""
                        self.draw_user_id_prompt(MpCanvas.buffer_g, var1_6)
                    self.draw_buffer()
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (var1_6 + 61), MpCanvas.input_text, 0x41FF41)
                    MpCanvas.draw_letter_grid(MpCanvas.letter_cursor, (var1_6 + 75))
                    if imod(MpCanvas.state_ticks, 4) < 2:
                        var2_10 = MpCanvas.font_white.string_width(MpCanvas.input_text)
                        if len(MpCanvas.input_text) == 12:
                            var2_10 = (var2_10 - (MpCanvas.font_white.string_width("A") * 2))
                        MpCanvas.draw_line_color(MpCanvas.screen_g, (MpCanvas.center_x + idiv(var2_10, 2)), (var1_6 + 71), ((MpCanvas.center_x + idiv(var2_10, 2)) + 4), (var1_6 + 71), 0xFFFFFF)
                    if len(MpCanvas.input_text) == 0:
                        self.draw_softkeys(4, 1)
                        break
                    self.draw_softkeys(4, 3)
                    return
                if _m4 or _sw3 == 80:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.character_menu[0]
                    self.draw_records()
                    self.draw_softkeys((-1), 1)
                    return
                if _m4 or _sw3 == 81:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.character_menu[1]
                    self.draw_attributes()
                    self.draw_softkeys((-1), 1)
                    return
                if _m4 or _sw3 == 82:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.character_menu[2]
                        self.draw_skills_bg(MpCanvas.buffer_g)
                    self.draw_buffer()
                    self.draw_skill_slots()
                    self.draw_softkeys((-1), 1)
                    return
                if _m4 or _sw3 == 83:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.character_menu[3]
                    self.draw_exp_fame_gold()
                    self.draw_softkeys((-1), 1)
                    return
                if _m4 or _sw3 == 84:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.letter_cursor = 0
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.character_menu[4]
                        self.draw_quote_bg(MpCanvas.buffer_g)
                    self.draw_buffer()
                    self.draw_quote_prompt(MpCanvas.screen_g)
                    if len(MpCanvas.input_text) == 0:
                        self.draw_softkeys(4, 1)
                        break
                    self.draw_softkeys(4, 3)
                    return
                if _m4 or _sw3 == 88:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.main_menu[3]
                        MpCanvas.menu_size = 3
                        self.draw_options_bg(MpCanvas.buffer_g)
                    self.draw_buffer()
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 3:
                        if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                            self.draw_text_colored(MpCanvas.screen_g, Consts.option_texts[MpCanvas.loop_i], (MpCanvas.center_x - 28), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0xFFFFFF)
                            _sw9 = MpCanvas.loop_i
                            _m10 = False
                            while True:
                                if _m10 or _sw9 == 0:
                                    _m10 = True
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.option_texts[(3 + MpCanvas.speed)], (MpCanvas.center_x + 33), (MpCanvas.center_y - 15), 1, 0xFFFFFF)
                                    break
                                if _m10 or _sw9 == 1:
                                    _m10 = True
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.option_texts[(8 + MpCanvas.invitation)], (MpCanvas.center_x + 33), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0xFFFFFF)
                                    break
                                if _m10 or _sw9 == 2:
                                    _m10 = True
                                    if MpCanvas.get_volume() > 0:
                                        var2_11 = 0
                                        while var2_11 < MpCanvas.get_volume():
                                            Draw.fill_rect(MpCanvas.screen_g, ((MpCanvas.center_x + 21) + (5 * var2_11)), ((MpCanvas.center_y - 13) + (MpCanvas.loop_i * 19)), 3, 8, 0xFFFFFF)
                                            var2_11 = var2_11 + 1
                                        break
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.option_texts[(6 + ((0 if (MpCanvas.get_volume() > 0) else 1)))], (MpCanvas.center_x + 33), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0xFFFFFF)
                                break
                            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 58), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 19)), 61, 14, 3)
                            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x + 13), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 19)), 39, 14, 3)
                            if imod(MpCanvas.state_ticks, 4) < 2:
                                MpCanvas.draw_left_half((MpCanvas.center_x + 6), ((MpCanvas.center_y - 13) + (MpCanvas.loop_i * 19)), MpCanvas.arrow_images[1])
                                MpCanvas.draw_right_half((MpCanvas.center_x + 59), ((MpCanvas.center_y - 13) + (MpCanvas.loop_i * 19)), MpCanvas.arrow_images[1])
                        else:
                            _sw11 = MpCanvas.loop_i
                            _m12 = False
                            while True:
                                if _m12 or _sw11 == 0:
                                    _m12 = True
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.option_texts[(3 + MpCanvas.speed)], (MpCanvas.center_x + 33), (MpCanvas.center_y - 15), 1, 0x646464)
                                    break
                                if _m12 or _sw11 == 1:
                                    _m12 = True
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.option_texts[(8 + MpCanvas.invitation)], (MpCanvas.center_x + 33), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0x646464)
                                    break
                                if _m12 or _sw11 == 2:
                                    _m12 = True
                                    if MpCanvas.get_volume() > 0:
                                        var2_11 = 0
                                        while var2_11 < MpCanvas.get_volume():
                                            Draw.fill_rect(MpCanvas.screen_g, ((MpCanvas.center_x + 21) + (5 * var2_11)), ((MpCanvas.center_y - 13) + (MpCanvas.loop_i * 19)), 3, 8, 0x646464)
                                            var2_11 = var2_11 + 1
                                        break
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.option_texts[(6 + ((0 if (MpCanvas.get_volume() > 0) else 1)))], (MpCanvas.center_x + 33), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0x646464)
                                break
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    self.draw_softkeys((-1), 1)
                    return
                if _m4 or _sw3 == 7:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.texts[64]
                        self.draw_window(MpCanvas.buffer_g)
                    self.draw_buffer()
                    self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 112, 48, 0)
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 18), _js(Consts.texts[64], "!"), 0xFFFFFF)
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 6), MpCanvas.user_id, 0xFFFFFF)
                    self.draw_ok_button((MpCanvas.center_y + 9))
                    return
                if _m4 or _sw3 == 6:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.texts[18]
                        self.draw_window(MpCanvas.buffer_g)
                    self.draw_notice()
                    return
                if _m4 or _sw3 == 3:
                    _m4 = True
                    self.draw_buffer()
                    if MpCanvas.state_ticks > idiv(20000, MpCanvas.tick_ms):
                        MpCanvas.error_msg = 7
                        self.on_disconnect()
                        return
                    self.draw_loading()
                    return
                if _m4 or _sw3 == 10000:
                    _m4 = True
                    self.draw_buffer()
                    if MpCanvas.state_ticks == 1:
                        self.connect()
                    if MpCanvas.state_ticks > idiv(20000, MpCanvas.tick_ms):
                        MpCanvas.error_msg = 7
                        self.on_disconnect()
                        return
                    self.draw_loading()
                    return
                if _m4 or _sw3 == 4:
                    _m4 = True
                    self.draw_buffer()
                    self.draw_error()
                    if MpCanvas.popup_shown:
                        self.draw_exit_confirm(MpCanvas.screen_g)
                        break
                    if (MpCanvas.error_msg == 7) or (MpCanvas.error_msg == 1):
                        self.draw_softkeys(5, 2)
                    return
                if _m4 or _sw3 == 5:
                    _m4 = True
                    Draw.fill_rect(MpCanvas.screen_g, 0, 0, MpCanvas.canvas_w, MpCanvas.canvas_h, 0)
                    self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 120, 100, 0)
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) - 10), Consts.texts[35], 0xFFFFFF)
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) + 5), Consts.texts[36], 0xFFFFFF)
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 2:
                        if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(40 + MpCanvas.loop_i)], ((MpCanvas.center_x - 28) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 28), 1, 0xFFFFFF)
                            self.draw_box(MpCanvas.screen_g, ((MpCanvas.center_x - 42) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 25), 29, 14, 3)
                        else:
                            self.draw_box(MpCanvas.screen_g, ((MpCanvas.center_x - 42) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 25), 29, 14, 2)
                            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(40 + MpCanvas.loop_i)], ((MpCanvas.center_x - 28) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 28), 1, 0x646464)
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    return
                if _m4 or _sw3 == 1:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        var2_12 = idiv(((MpCanvas.screen_h - 320)), 2)
                        var3_15 = 0
                        while var3_15 < 4:
                            MpCanvas.title_image = self.load_image(_js(_js("/title_", ((var3_15 + 1))), ".png"))
                            Draw.draw_image(MpCanvas.buffer_g, MpCanvas.title_image, (MpCanvas.center_x - idiv(MpCanvas.title_image.getWidth(), 2)), (var2_12 + (80 * var3_15)), 0)
                            MpCanvas.title_image = None
                            var3_15 = var3_15 + 1
                        if MpCanvas.gamevil_image is None:
                            MpCanvas.gamevil_image = self.load_image("/gamevil.png")
                        Draw.draw_image(MpCanvas.buffer_g, MpCanvas.gamevil_image, idiv(MpCanvas.canvas_w, 2), (MpCanvas.canvas_h - 1), 33)
                        if MpCanvas.press_image is None:
                            MpCanvas.press_image = self.load_image("/press.png")
                    self.draw_buffer()
                    if imod(MpCanvas.state_ticks, 4) >= 2:
                        break
                    Draw.draw_image(MpCanvas.screen_g, MpCanvas.press_image, idiv(MpCanvas.canvas_w, 2), (MpCanvas.canvas_h - 27), 33)
                    return
                if _m4 or _sw3 == 2:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.input_text = ""
                        self.free_battle_images()
                        MpCanvas.title = Consts.login_texts[0]
                        self.draw_window_bg(MpCanvas.buffer_g)
                    self.draw_buffer()
                    self.draw_popup()
                    return
                if _m4 or _sw3 == 160:
                    _m4 = True
                    self.draw_buffer()
                    _sw13 = MpCanvas.popup_style
                    _m14 = False
                    while True:
                        if _m14 or _sw13 == 0:
                            _m14 = True
                            MpCanvas.tmp = len(MpCanvas.popup_line1)
                            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, ((MpCanvas.tmp * 7) + 6), 45, 0)
                            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 13), MpCanvas.popup_line1, 16400640)
                            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y + 2), MpCanvas.popup_line2, 16400640)
                            raise _Brk_block1_457()
                        if _m14 or _sw13 == 1:
                            _m14 = True
                            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 120, 100, 0)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) - 10), MpCanvas.popup_line1, 16400640)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) + 5), MpCanvas.popup_line2, 16400640)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) + 20), Consts.texts[19], 16400640)
                            MpCanvas.loop_i = 0
                            while MpCanvas.loop_i < 2:
                                if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(40 + MpCanvas.loop_i)], ((MpCanvas.center_x - 28) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 28), 1, 16400640)
                                    self.draw_box(MpCanvas.screen_g, ((MpCanvas.center_x - 42) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 25), 29, 14, 3)
                                else:
                                    self.draw_box(MpCanvas.screen_g, ((MpCanvas.center_x - 42) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 25), 29, 14, 2)
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(40 + MpCanvas.loop_i)], ((MpCanvas.center_x - 28) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 28), 1, 0xFFFFFF)
                                MpCanvas.loop_i = MpCanvas.loop_i + 1
                            raise _Brk_block1_457()
                        if _m14 or _sw13 == 2:
                            _m14 = True
                            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 120, 100, 0)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) - 10), MpCanvas.popup_line1, 16400640)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) + 5), MpCanvas.popup_line2, 16400640)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) + 20), MpCanvas.popup_line3, 16400640)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) + 35), MpCanvas.popup_line4, 16400640)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) + 50), MpCanvas.popup_line5, 16400640)
                        if _m14 or _sw13 not in (0, 1, 2):
                            _m14 = True
                            return
                        break
                if _m4 or _sw3 == 300:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.disconnect()
                        self.stop_music()
                        MpCanvas.logo_image = self.load_image("/outro.png")
                    Draw.fill_rect(MpCanvas.screen_g, 0, 0, MpCanvas.screen_w, MpCanvas.screen_h, 0)
                    var2_13 = MpCanvas.logo_image.getWidth()
                    Gfx.draw_image_part(MpCanvas.logo_image, (MpCanvas.center_x - idiv(var2_13, 2)), (MpCanvas.center_y - 10), var2_13, 19, 0, 0)
                    Gfx.draw_image_part(MpCanvas.logo_image, (MpCanvas.center_x - idiv(var2_13, 2)), (MpCanvas.screen_h - 26), var2_13, 23, 0, 19)
                    if MpCanvas.state_ticks <= 30:
                        break
                    MpCanvas.midlet.destroyApp(True)
                    MpCanvas.midlet.notifyDestroyed()
                    return
                if _m4 or _sw3 == 87:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.title = Consts.main_menu[4]
                        MpCanvas.menu_size = 6
                        self.draw_menu_icons()
                    self.draw_buffer()
                    self.draw_button(MpCanvas.screen_g, Consts.help_topics[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 39), (MpCanvas.center_y - 19), 78, 17, False, True)
                    MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
                    self.draw_softkeys((-1), 1)
                    return
                if _m4 or _sw3 == 89:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.help_page = 0
                    self.draw_help()
                    self.draw_softkeys((-1), 1)
                    return
                if _m4 or _sw3 == 85:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        _sw15 = MpCanvas.state
                        if _sw15 == 85:
                            MpCanvas.title = Consts.character_menu[5]
                        self.draw_name_prompt(MpCanvas.buffer_g)
                    self.draw_buffer()
                    self.draw_input_line(MpCanvas.screen_g)
                    if len(MpCanvas.input_text) == 0:
                        self.draw_softkeys(4, 1)
                        break
                    self.draw_softkeys(4, 3)
                    return
                if _m4 or _sw3 == 86:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.menu_size = 2
                    self.draw_buffer()
                    self.draw_input_line(MpCanvas.screen_g)
                    self.draw_name_confirm(MpCanvas.screen_g)
                break
        except _Brk_block1_457:
            pass

    @staticmethod
    def set_timer(n2):  # g.java:1467
        MpCanvas.timer_ticks = n2

    def draw_text_centred_on(self, graphics, n2, n3, string, n4):  # g.java:1471
        self.draw_text_colored(graphics, string, n2, n3, 1, n4)

    def draw_text_centred(self, n2, n3, string, n4):  # g.java:1475
        self.draw_text_colored(MpCanvas.screen_g, string, n2, n3, 1, n4)

    def draw_text_left_on(self, graphics, n2, n3, string, n4):  # g.java:1479
        self.draw_text_colored(graphics, string, n2, n3, 0, n4)

    def draw_text_left(self, n2, n3, string, n4):  # g.java:1483
        self.draw_text_colored(MpCanvas.screen_g, string, n2, n3, 0, n4)

    def draw_text_colored(self, graphics, string, n2, n3, n4, n5):  # g.java:1487
        _sw16 = n5
        if _sw16 == 0xFFFFFF:
            Gfx.set_font(MpCanvas.font_white)
        elif _sw16 == 16400640:
            Gfx.set_font(MpCanvas.font_orange)
        elif _sw16 == 0x646464:
            Gfx.set_font(MpCanvas.font_gray)
        elif _sw16 == 0x41FF41:
            Gfx.set_font(MpCanvas.font_green)
        else:
            MpCanvas.log(_js("=======================drawString: No Color:", n5))
        Gfx.draw_string_on(graphics, string, n2, n3, n4)

    @staticmethod
    def draw_rect(n2, n3, n4, n5, n6):  # g.java:1512
        Draw.draw_rect(MpCanvas.screen_g, n2, n3, n4, n5, n6)

    @staticmethod
    def fill_rect(n2, n3, n4, n5, n6):  # g.java:1516
        Draw.fill_rect(MpCanvas.screen_g, n2, n3, n4, n5, n6)

    @staticmethod
    def fill_rect_on(graphics, n2, n3, n4, n5, n6):  # g.java:1520
        Draw.fill_rect(graphics, n2, n3, n4, n5, n6)

    @staticmethod
    def set_color(graphics, n2):  # g.java:1524
        graphics.setColor(n2)

    @staticmethod
    def draw_line_color(graphics, n2, n3, n4, n5, n6):  # g.java:1528
        Draw.draw_line_color(graphics, n2, n3, n4, n5, n6)

    @staticmethod
    def draw_line(graphics, n2, n3, n4, n5):  # g.java:1532
        Draw.draw_line(graphics, n2, n3, n4, n5)

    @staticmethod
    def draw_dot(graphics, n2, n3, n4):  # g.java:1536
        Draw.fill_rect(graphics, n2, n3, 1, 1, n4)

    @staticmethod
    def draw_image(n2, n3, image):  # g.java:1540
        Draw.draw_image(MpCanvas.screen_g, image, n2, n3, 0)

    @staticmethod
    def draw_image_on(graphics, n2, n3, image):  # g.java:1544
        Draw.draw_image(graphics, image, n2, n3, 0)

    @staticmethod
    def draw_right_half(n2, n3, image):  # g.java:1548
        n4 = (idiv(image.getWidth(), 2) + 1)
        n5 = image.getHeight()
        Draw.draw_image_part(MpCanvas.screen_g, image, (n2 - n4), n3, n4, n5, (n4 - 1), 0)

    @staticmethod
    def draw_right_half_on(graphics, n2, n3, image):  # g.java:1554
        n4 = (idiv(image.getWidth(), 2) + 1)
        n5 = image.getHeight()
        Draw.draw_image_part(graphics, image, (n2 - n4), n3, n4, n5, (n4 - 1), 0)

    @staticmethod
    def draw_right_half_h(graphics, n2, n3, n4, image):  # g.java:1560
        n5 = (idiv(image.getWidth(), 2) + 1)
        Draw.draw_image_part(graphics, image, (n2 - n5), n3, n5, n4, (n5 - 1), 0)

    @staticmethod
    def draw_right_aligned(n2, n3, image, bl):  # g.java:1565
        if bl:
            n4 = (idiv(image.getWidth(), 2) + 1)
            n5 = image.getHeight()
            Draw.draw_image_part(MpCanvas.screen_g, image, (n2 - n4), n3, n4, n5, (n4 - 1), 0)
            return
        Draw.draw_image(MpCanvas.screen_g, image, (n2 - image.getWidth()), n3, 0)

    @staticmethod
    def draw_left_half_row(graphics, n2, n3, image, n4, n5):  # g.java:1575
        n6 = (idiv(image.getWidth(), 2) + 1)
        Draw.draw_image_part(graphics, image, n2, n3, n6, n4, 0, (n4 * n5))

    @staticmethod
    def draw_right_half_row1(graphics, n2, n3, n4, image):  # g.java:1580
        n5 = (idiv(image.getWidth(), 2) + 1)
        Draw.draw_image_part(graphics, image, (n2 - n5), n3, n5, n4, (n5 - 1), n4)

    @staticmethod
    def draw_left_half(n2, n3, image):  # g.java:1585
        n4 = (idiv(image.getWidth(), 2) + 1)
        n5 = image.getHeight()
        Draw.draw_image_part(MpCanvas.screen_g, image, n2, n3, n4, n5, 0, 0)

    @staticmethod
    def draw_left_half_on(graphics, n2, n3, image):  # g.java:1591
        n4 = (idiv(image.getWidth(), 2) + 1)
        n5 = image.getHeight()
        Draw.draw_image_part(graphics, image, n2, n3, n4, n5, 0, 0)

    @staticmethod
    def draw_left_half_h(graphics, n2, n3, n4, image):  # g.java:1597
        n5 = (idiv(image.getWidth(), 2) + 1)
        Draw.draw_image_part(graphics, image, n2, n3, n5, n4, 0, 0)

    def draw_buffer(self):  # g.java:1602
        Draw.draw_image(MpCanvas.screen_g, MpCanvas.buffer, 0, 0, 0)
        if (MpCanvas.state >= 90) and (MpCanvas.state <= 105):
            MpCanvas.draw_hp_bars(MpCanvas.screen_g)

    def send_request(self, n2):  # g.java:1609
        if (n2 == 262) or (n2 == 278):
            MpCanvas.login_time = system.currentTimeMillis()
        if NetThread.connected and (idiv(((system.currentTimeMillis() - MpCanvas.login_time)), 1000) > 45):
            MpCanvas.ping_misses = 0
            MpCanvas.error_msg = 13
            MpCanvas.popup_shown = False
            self.on_disconnect()
            MpCanvas.login_time = system.currentTimeMillis()
            return
        MpCanvas.login_time = system.currentTimeMillis()
        MpCanvas.answer_status = 0
        MpCanvas.request_opcode = n2
        MpCanvas.net.begin(MpCanvas.request_opcode)
        _sw17 = MpCanvas.request_opcode
        if _sw17 == 1300:
            NetThread.write_byte(i8(((MpCanvas.rank_kind + 1))))
        elif _sw17 == 1293:
            NetThread.write_byte(i8(MpCanvas.rank_list_kind))
            NetThread.write_int(1)
        elif _sw17 == 256:
            NetThread.write_string(MpCanvas.user_id, 12)
            NetThread.write_string(MpCanvas.game_ver, 4)
        elif _sw17 == 262:
            NetThread.write_string(MpCanvas.user_id, 12)
            NetThread.write_string(MpCanvas.game_ver, 4)
        elif _sw17 == 278:
            NetThread.write_string(MpCanvas.user_id, 12)
            NetThread.write_string(MpCanvas.password, 16)
            NetThread.write_string(MpCanvas.game_ver, 4)
        elif _sw17 == 512:
            NetThread.write_byte(MpCanvas.room_mode)
        elif _sw17 == 1291:
            MpCanvas.loop_j = 0
            MpCanvas.loop_i = 0
            while MpCanvas.loop_i < 4:
                if MpCanvas.skill_levels[(MpCanvas.skill_order[MpCanvas.loop_i] - 3)] != 99:
                    NetThread.write_byte(MpCanvas.skill_order[MpCanvas.loop_i])
                    MpCanvas.loop_j = MpCanvas.loop_j + 1
                MpCanvas.loop_i = MpCanvas.loop_i + 1
            MpCanvas.loop_i = MpCanvas.loop_j
            while MpCanvas.loop_i < 4:
                NetThread.write_byte(i8(99))
                MpCanvas.loop_i = MpCanvas.loop_i + 1
        elif _sw17 == 1280:
            NetThread.write_string(MpCanvas.input_text, 8)
        elif _sw17 == 258:
            NetThread.write_int(MpCanvas.notice_page)
        elif _sw17 == 1027:
            NetThread.write_byte(i8(MpCanvas.fighter_slot[MpCanvas.target_cursor]))
            NetThread.write_byte(i8(MpCanvas.chosen_action))
            NetThread.write_byte(i8(MpCanvas.hit_score))
        elif _sw17 in (1282, 1284):
            NetThread.write_string(MpCanvas.input_text, 20)
        elif _sw17 == 768:
            NetThread.write_byte(MpCanvas.room_mode)
            NetThread.write_string(MpCanvas.input_text, 12)
        elif _sw17 == 288:
            pass
        elif _sw17 == 290:
            NetThread.write_int(MpCanvas.invitation)
        NetThread.send()

    def load_ui_images(self):  # g.java:1706
        MpCanvas.ui_images[2] = self.load_image("/ui2.png")
        MpCanvas.ui_images[3] = self.load_image("/ui3.png")
        MpCanvas.ui_images[15] = self.load_image("/ui15.png")
        MpCanvas.ui_images[16] = self.load_image("/ui16.png")
        MpCanvas.ui_images[17] = self.load_image("/ui17.png")
        MpCanvas.ui_images[18] = self.load_image("/ui18.png")
        MpCanvas.ui_images[19] = self.load_image("/ui19.png")
        n2 = 0
        while n2 < 6:
            MpCanvas.act_images[n2] = self.load_image(_js(_js("/act", n2), ".png"))
            n2 = n2 + 1
        MpCanvas.arrow_images[1] = self.load_image("/menuarrow1.png")
        n3 = 0
        while n3 < 8:
            MpCanvas.number_images[n3] = self.load_image(_js(_js("/gnum", n3), ".png"))
            n3 = n3 + 1
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
        n2 = 0
        while n2 < 6:
            if MpCanvas.mpic_images[n2] is None:
                MpCanvas.mpic_images[n2] = self.load_image(_js(_js("/mpic", n2), ".png"))
            n2 = n2 + 1
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
        n2 = 0
        MpCanvas.body_images[0] = None
        MpCanvas.body_images[1] = None
        n3 = 0
        while n3 < 3:
            if MpCanvas.body_frames[n3] is not None:
                MpCanvas.body_frames[n3].free()
            MpCanvas.body_frames[n3] = None
            n3 = n3 + 1
        n3 = 0
        while n3 < 10:
            MpCanvas.head_images[n3][0] = None
            MpCanvas.head_images[n3][1] = None
            n2 = 0
            while n2 < 3:
                if MpCanvas.head_frames[n3][n2] is not None:
                    MpCanvas.head_frames[n3][n2].free()
                MpCanvas.head_frames[n3][n2] = None
                n2 = n2 + 1
            n3 = n3 + 1
        n3 = 0
        while n3 < 2:
            MpCanvas.weapon_images[n3][0] = None
            MpCanvas.weapon_images[n3][1] = None
            n2 = 0
            while n2 < 3:
                if MpCanvas.weapon_frames[n3][n2] is not None:
                    MpCanvas.weapon_frames[n3][n2].free()
                MpCanvas.weapon_frames[n3][n2] = None
                n2 = n2 + 1
            n3 = n3 + 1
        n3 = 0
        while n3 < 2:
            MpCanvas.sword_images[n3][0] = None
            MpCanvas.sword_images[n3][1] = None
            n2 = 0
            while n2 < 3:
                if MpCanvas.sword_frames[n3][n2] is not None:
                    MpCanvas.sword_frames[n3][n2].free()
                MpCanvas.sword_frames[n3][n2] = None
                n2 = n2 + 1
            n3 = n3 + 1
        n3 = 0
        while n3 < 2:
            MpCanvas.effect_images[n3][0] = None
            MpCanvas.effect_images[n3][1] = None
            n2 = 0
            while n2 < 3:
                if MpCanvas.effect_frames[n3][n2] is not None:
                    MpCanvas.effect_frames[n3][n2].free()
                MpCanvas.effect_frames[n3][n2] = None
                n2 = n2 + 1
            n3 = n3 + 1
        MpCanvas.shadow_images[0] = None
        MpCanvas.shadow_images[1] = None
        n3 = 0
        while n3 < 3:
            if MpCanvas.shadow_frames[n3] is not None:
                MpCanvas.shadow_frames[n3].free()
            MpCanvas.shadow_frames[n3] = None
            n3 = n3 + 1
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
        n3 = 2
        while n3 < len(MpCanvas.act_images):
            MpCanvas.act_images[n3] = None
            n3 = n3 + 1
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

    def on_answer(self, k2):  # g.java:1888
        MpCanvas.wait_started = False
        if MpCanvas.paused or (MpCanvas.pause_request == 1):
            MpCanvas.error_msg = 7
            MpCanvas.popup_shown = False
            MpCanvas.disconnect()
            MpCanvas.set_timer((-1))
            self.push_state(4)
            return
        if NetThread.last_opcode == 280:
            MpCanvas.error_msg = 17
            MpCanvas.popup_shown = False
            MpCanvas.disconnect()
            self.push_state(4)
            return
        if not NetThread.connected:
            return
        s = k2.read_s16()
        by = k2.read_s8()
        MpCanvas.answer_status = by
        _sw18 = s
        try:
            _m19 = False
            while True:
                if _m19 or _sw18 == 279:
                    _m19 = True
                    if MpCanvas.answer_status == 1:
                        MpCanvas.save_options()
                        self.on_disconnect()
                        MpCanvas.loading_msg = 0
                        MpCanvas.password_login = False
                        MpCanvas.set_state(10000)
                        return
                    by2 = k2.read_s8()
                    self.on_disconnect()
                    if by2 == 0:
                        MpCanvas.popup_kind = 0
                        MpCanvas.error_msg = 14
                    elif by2 == 1:
                        MpCanvas.popup_kind = 1
                        MpCanvas.error_msg = 15
                    else:
                        MpCanvas.popup_kind = 0
                        MpCanvas.error_msg = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 263:
                    _m19 = True
                    _sw20 = MpCanvas.answer_status
                    if _sw20 == 1:
                        MpCanvas.name = k2.read_string(8)
                        MpCanvas.face = k2.read_s8()
                        MpCanvas.level = k2.read_s16()
                        MpCanvas.wins = k2.read_s32()
                        MpCanvas.losses = k2.read_s32()
                        MpCanvas.hp = k2.read_s16()
                        k2.read_s16()
                        k2.read_s16()
                        MpCanvas.weapon = k2.read_s8()
                        MpCanvas.skill_slots[0] = k2.read_s8()
                        MpCanvas.skill_slots[1] = k2.read_s8()
                        MpCanvas.skill_slots[2] = k2.read_s8()
                        MpCanvas.skill_slots[3] = k2.read_s8()
                        MpCanvas.skill_slot_count = 0
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < 4:
                            if MpCanvas.skill_slots[MpCanvas.loop_i] != 99:
                                MpCanvas.skill_slot_count = MpCanvas.skill_slot_count + 1
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        MpCanvas.quote_start = MpCanvas.trim_right(k2.read_string(20))
                        MpCanvas.quote_win = MpCanvas.trim_right(k2.read_string(20))
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < 11:
                            MpCanvas.skill_costs[MpCanvas.loop_i] = k2.read_s8()
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        MpCanvas.profile_cr = k2.read_s8()
                        MpCanvas.profile_unused1 = k2.read_s8()
                        MpCanvas.profile_unused2 = k2.read_s8()
                        if MpCanvas.profile_unused1 < 0:
                            MpCanvas.profile_unused1 = 0
                        if MpCanvas.profile_unused2 < 0:
                            MpCanvas.profile_unused2 = 0
                        MpCanvas.notices_left = k2.read_s8()
                        k2.read_string(8)
                        k2.read_string(8)
                        k2.read_s8()
                        k2.read_s8()
                        k2.read_s8()
                        MpCanvas.title_image = None
                        MpCanvas.press_image = None
                        MpCanvas.gamevil_image = None
                        MpCanvas.noop()
                        if MpCanvas.relogin:
                            if MpCanvas.relogin_to_menu:
                                self.reset_state_stack(7)
                                return
                            self.reset_state_stack(10)
                            return
                        if MpCanvas.notices_left > 0:
                            MpCanvas.notice_page = 1
                            self.send_request(258)
                            return
                        MpCanvas.notices_left = 0
                        self.reset_state_stack(7)
                        return
                    elif _sw20 == (-2):
                        MpCanvas.error_msg = 1
                        self.on_disconnect()
                        return
                    elif _sw20 == (-9):
                        MpCanvas.error_msg = 8
                        self.on_disconnect()
                        return
                    MpCanvas.error_msg = 7
                    MpCanvas.popup_shown = False
                    MpCanvas.disconnect()
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 1286:
                    _m19 = True
                    _sw21 = MpCanvas.room_mode
                    _m22 = False
                    while True:
                        if _m22 or _sw21 in (0, 1):
                            _m22 = True
                            MpCanvas.set_state(11)
                            raise _Brk_block0_1631()
                        if _m22 or _sw21 == 2:
                            _m22 = True
                            MpCanvas.set_state(12)
                        break
                    return
                if _m19 or _sw18 == 1301:
                    _m19 = True
                    _sw23 = MpCanvas.answer_status
                    _m24 = False
                    while True:
                        if _m24 or _sw23 == 1:
                            _m24 = True
                            MpCanvas.my_ranks[MpCanvas.rank_kind] = k2.read_s32()
                            MpCanvas.my_rank_value = k2.read_s32()
                            self.push_state(((161 + MpCanvas.cursor_stack[MpCanvas.stack_depth]) + 1))
                            raise _Brk_block0_1631()
                        if _m24 or _sw23 == (-1):
                            _m24 = True
                            MpCanvas.error_msg = 0
                            self.push_state(4)
                        break
                    return
                if _m19 or _sw18 == 1294:
                    _m19 = True
                    _sw25 = MpCanvas.answer_status
                    _m26 = False
                    while True:
                        if _m26 or _sw25 == 1:
                            _m26 = True
                            n2 = k2.read_s8()
                            n3 = 0
                            while n3 < n2:
                                MpCanvas.rank_ranks[n3] = k2.read_s32()
                                MpCanvas.rank_names[n3] = k2.read_string(12)
                                MpCanvas.rank_values[n3] = k2.read_s32()
                                n3 = n3 + 1
                            self.push_state((170 + MpCanvas.cursor_stack[MpCanvas.stack_depth]))
                            raise _Brk_block0_1631()
                        if _m26 or _sw25 == (-1):
                            _m26 = True
                            MpCanvas.error_msg = 0
                            self.push_state(4)
                        break
                    return
                if _m19 or _sw18 == 259:
                    _m19 = True
                    _sw27 = MpCanvas.answer_status
                    if _sw27 == 1:
                        n4 = 0
                        while n4 < 4:
                            MpCanvas.notice_lines[n4] = k2.read_string(16)
                            n4 = n4 + 1
                        MpCanvas.notices_left = k2.read_s8()
                        MpCanvas.notice_kind = 1
                        MpCanvas.set_state(6)
                        return
                    MpCanvas.error_msg = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 513:
                    _m19 = True
                    _sw28 = MpCanvas.answer_status
                    if _sw28 == 1:
                        MpCanvas.room_bg = k2.read_s8()
                        MpCanvas.my_slot = k2.read_s8()
                        MpCanvas.room_mode = k2.read_s8()
                        k2.read_s8()
                        MpCanvas.painting_blocked = True
                        self.free_frame_images()
                        MpCanvas.painting_blocked = False
                        MpCanvas.room_dirty = True
                        return
                    MpCanvas.error_msg = 0
                    _sw29 = MpCanvas.answer_status
                    if _sw29 == (-11):
                        MpCanvas.error_msg = 8
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 769:
                    _m19 = True
                    _sw30 = MpCanvas.answer_status
                    if _sw30 == 1:
                        MpCanvas.room_bg = k2.read_s8()
                        MpCanvas.my_slot = k2.read_s8()
                        MpCanvas.room_mode = k2.read_s8()
                        k2.read_s8()
                        MpCanvas.painting_blocked = True
                        self.free_frame_images()
                        MpCanvas.painting_blocked = False
                        MpCanvas.room_dirty = True
                        return
                    _sw31 = MpCanvas.answer_status
                    if _sw31 == (-3):
                        MpCanvas.error_msg = 2
                    elif _sw31 == (-4):
                        MpCanvas.error_msg = 3
                    elif _sw31 == (-5):
                        MpCanvas.error_msg = 4
                    elif _sw31 == (-12):
                        MpCanvas.error_msg = 9
                    elif _sw31 == (-16):
                        MpCanvas.error_msg = 18
                    else:
                        MpCanvas.error_msg = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 770:
                    _m19 = True
                    _sw32 = MpCanvas.answer_status
                    if _sw32 == 1:
                        MpCanvas.popup_shown = False
                        MpCanvas.room_bg = k2.read_s8()
                        MpCanvas.my_slot = k2.read_s8()
                        MpCanvas.room_mode = k2.read_s8()
                        k2.read_s8()
                        MpCanvas.painting_blocked = True
                        self.free_frame_images()
                        MpCanvas.painting_blocked = False
                        MpCanvas.room_dirty = True
                        return
                    MpCanvas.error_msg = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 514:
                    _m19 = True
                    _sw33 = MpCanvas.answer_status
                    if _sw33 == 1:
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < 4:
                            if not MpCanvas.fighter_present[MpCanvas.loop_i]:
                                MpCanvas.cur_slot = MpCanvas.loop_i
                                break
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        MpCanvas.fighter_present[MpCanvas.cur_slot] = True
                        MpCanvas.fighter_slot[MpCanvas.cur_slot] = k2.read_s8()
                        if imod(MpCanvas.fighter_slot[MpCanvas.cur_slot], 2) == imod(MpCanvas.fighter_slot[0], 2):
                            MpCanvas.allies_alive = MpCanvas.allies_alive + 1
                        else:
                            MpCanvas.enemies_alive = MpCanvas.enemies_alive + 1
                        MpCanvas.fighter_name[MpCanvas.cur_slot] = k2.read_string(8)
                        MpCanvas.fighter_level[MpCanvas.cur_slot] = k2.read_s16()
                        MpCanvas.fighter_wins[MpCanvas.cur_slot] = k2.read_s32()
                        MpCanvas.fighter_losses[MpCanvas.cur_slot] = k2.read_s32()
                        MpCanvas.fighter_hp[MpCanvas.cur_slot] = k2.read_s16()
                        MpCanvas.fighter_max_hp[MpCanvas.cur_slot] = MpCanvas.fighter_hp[MpCanvas.cur_slot]
                        MpCanvas.fighter_weapon[MpCanvas.cur_slot] = k2.read_s8()
                        MpCanvas.fighter_face[MpCanvas.cur_slot] = k2.read_s8()
                        if MpCanvas.fighter_face[MpCanvas.cur_slot] == 10:
                            MpCanvas.fighter_face[MpCanvas.cur_slot] = 0
                            MpCanvas.fighter_kind[MpCanvas.cur_slot] = 2
                        elif MpCanvas.fighter_face[MpCanvas.cur_slot] < 10:
                            MpCanvas.fighter_kind[MpCanvas.cur_slot] = 0
                        else:
                            n5 = MpCanvas.cur_slot
                            MpCanvas.fighter_face[n5] = i8(((MpCanvas.fighter_face[n5] - 30)))
                            MpCanvas.fighter_kind[MpCanvas.cur_slot] = 1
                        MpCanvas.fighter_quote_start[MpCanvas.cur_slot] = k2.read_string(20)
                        MpCanvas.fighter_quote_win[MpCanvas.cur_slot] = k2.read_string(20)
                        MpCanvas.fighter_cr[MpCanvas.cur_slot] = k2.read_s8()
                        MpCanvas.fighter_alt_name[MpCanvas.cur_slot] = k2.read_string(8)
                        MpCanvas.fighter_mp[MpCanvas.cur_slot] = 0
                        MpCanvas.place_fighter(MpCanvas.cur_slot)
                        MpCanvas.fighter_blink[MpCanvas.cur_slot] = imod(abs(MpCanvas.rng.nextInt()), 4)
                        MpCanvas.fighter_status[MpCanvas.cur_slot] = 99
                        MpCanvas.fighter_status_ticks[MpCanvas.cur_slot] = 0
                        MpCanvas.hud_dirty = True
                        if MpCanvas.state != 4:
                            break
                        MpCanvas.set_state(90)
                        MpCanvas.room_dirty = True
                        return
                    MpCanvas.error_msg = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 1024:
                    _m19 = True
                    _sw34 = MpCanvas.answer_status
                    if _sw34 == 1:
                        MpCanvas.set_state(92)
                    return
                if _m19 or _sw18 == 1026:
                    _m19 = True
                    _sw35 = MpCanvas.answer_status
                    if _sw35 == 1:
                        MpCanvas.chosen_action = 99
                        MpCanvas.set_timer((10 - MpCanvas.speed))
                        MpCanvas.choose_secs = 1 if MpCanvas.auto_battle else 10   # PORT-EXTRA auto-battle
                        MpCanvas.exit_asked = False
                        MpCanvas.set_state(94)
                    return
                if _m19 or _sw18 == 1028:
                    _m19 = True
                    _sw36 = MpCanvas.answer_status
                    if _sw36 == 1:
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < 4:
                            MpCanvas.slot_found = False
                            MpCanvas.loop_j = 0
                            while MpCanvas.loop_j < 4:
                                if MpCanvas.fighter_present[MpCanvas.loop_j] and (MpCanvas.fighter_slot[MpCanvas.loop_j] == MpCanvas.loop_i):
                                    MpCanvas.cur_slot = MpCanvas.loop_j
                                    MpCanvas.slot_found = True
                                    break
                                MpCanvas.loop_j = MpCanvas.loop_j + 1
                            if MpCanvas.slot_found:
                                MpCanvas.turn_actions[MpCanvas.cur_slot] = k2.read_s8()
                            else:
                                MpCanvas.tmp = k2.read_s8()
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        MpCanvas.turn_record_count = k2.read_s8()
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < MpCanvas.turn_record_count:
                            MpCanvas.turn_bytes[(0 + MpCanvas.loop_i)] = k2.read_s8()
                            MpCanvas.turn_bytes[(4 + MpCanvas.loop_i)] = k2.read_s8()
                            MpCanvas.turn_hps[(0 + MpCanvas.loop_i)] = k2.read_s16()
                            MpCanvas.turn_bytes[(8 + MpCanvas.loop_i)] = k2.read_s8()
                            MpCanvas.turn_bytes[(12 + MpCanvas.loop_i)] = k2.read_s8()
                            MpCanvas.turn_bytes[(16 + MpCanvas.loop_i)] = k2.read_s8()
                            MpCanvas.turn_hps[(4 + MpCanvas.loop_i)] = k2.read_s16()
                            MpCanvas.turn_bytes[(20 + MpCanvas.loop_i)] = k2.read_s8()
                            MpCanvas.turn_bytes[(24 + MpCanvas.loop_i)] = k2.read_s8()
                            MpCanvas.turn_bytes[(28 + MpCanvas.loop_i)] = k2.read_s8()
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        k2.read_s8()
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < MpCanvas.turn_record_count:
                            if MpCanvas.turn_bytes[(24 + MpCanvas.loop_i)] == 1:
                                MpCanvas.turn_bytes[(32 + MpCanvas.loop_i)] = k2.read_s8()
                                MpCanvas.turn_bytes[(36 + MpCanvas.loop_i)] = k2.read_s8()
                                MpCanvas.turn_hps[(8 + MpCanvas.loop_i)] = k2.read_s16()
                                MpCanvas.turn_bytes[(40 + MpCanvas.loop_i)] = k2.read_s8()
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        MpCanvas.set_state(99)
                    return
                if _m19 or _sw18 == 1031:
                    _m19 = True
                    _sw37 = MpCanvas.answer_status
                    if _sw37 == 1:
                        MpCanvas.room_bg = k2.read_s8()
                        MpCanvas.set_state(104)
                    return
                if _m19 or _sw18 == 1032:
                    _m19 = True
                    _sw38 = MpCanvas.answer_status
                    if _sw38 == 1:
                        MpCanvas.battle_won = k2.read_s8()
                        if MpCanvas.room_mode != 2:
                            if MpCanvas.battle_won == 1:
                                MpCanvas.wins = MpCanvas.wins + 1
                            else:
                                MpCanvas.losses = MpCanvas.losses + 1
                        MpCanvas.reward_gold = k2.read_s16()
                        MpCanvas.reward_grade = k2.read_s8()
                        MpCanvas.reward_fame = k2.read_s16()
                        MpCanvas.reward_exp = k2.read_s16()
                        MpCanvas.loot = k2.read_string(15)
                        MpCanvas.reward_rank = k2.read_s32()
                        k2.read_s8()
                        k2.read_s32()
                        k2.read_s8()
                        MpCanvas.set_state(105)
                    return
                if _m19 or _sw18 == 1037:
                    _m19 = True
                    _sw39 = MpCanvas.answer_status
                    if _sw39 == 1:
                        MpCanvas.stage_title = k2.read_string(14)
                        MpCanvas.stage_count = k2.read_s8()
                        MpCanvas.stage = k2.read_s8()
                        MpCanvas.set_state(91)
                    return
                if _m19 or _sw18 == 1035:
                    _m19 = True
                    _sw40 = MpCanvas.answer_status
                    _m41 = False
                    while True:
                        if _m41 or _sw40 == 1:
                            _m41 = True
                            MpCanvas.leaving_slot = k2.read_s8()
                            MpCanvas.loop_i = 0
                            while MpCanvas.loop_i < 4:
                                if MpCanvas.fighter_present[MpCanvas.loop_i] and (MpCanvas.fighter_slot[MpCanvas.loop_i] == MpCanvas.leaving_slot):
                                    MpCanvas.cur_slot = MpCanvas.loop_i
                                    break
                                MpCanvas.loop_i = MpCanvas.loop_i + 1
                            MpCanvas.fighter_present[MpCanvas.cur_slot] = False
                            if MpCanvas.fighter_hp[MpCanvas.cur_slot] == 0:
                                break
                            if imod(MpCanvas.fighter_slot[MpCanvas.cur_slot], 2) == imod(MpCanvas.fighter_slot[0], 2):
                                MpCanvas.allies_alive = MpCanvas.allies_alive - 1
                                raise _Brk_block0_1631()
                            MpCanvas.enemies_alive = MpCanvas.enemies_alive - 1
                        break
                    return
                if _m19 or _sw18 == 1281:
                    _m19 = True
                    _sw42 = MpCanvas.answer_status
                    if _sw42 == 1:
                        MpCanvas.name = MpCanvas.input_text
                        self.pop_states(2)
                        return
                    elif _sw42 == (-6):
                        MpCanvas.error_msg = 6
                        self.push_state(4)
                        return
                    elif _sw42 == (-49):
                        MpCanvas.error_msg = 5
                        self.push_state(4)
                        return
                    elif _sw42 == (-15):
                        MpCanvas.error_msg = 5
                        self.push_state(4)
                        return
                    MpCanvas.error_msg = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 1283:
                    _m19 = True
                    self.push_state(84)
                    _sw43 = MpCanvas.answer_status
                    if _sw43 == 1:
                        MpCanvas.quote_start = MpCanvas.input_text
                        MpCanvas.letter_cursor = 0
                        MpCanvas.input_text = MpCanvas.quote_win
                        MpCanvas.quote_step = 1
                        return
                    elif _sw43 == (-49):
                        MpCanvas.error_msg = 5
                        self.push_state(4)
                        return
                    MpCanvas.error_msg = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 1285:
                    _m19 = True
                    _sw44 = MpCanvas.answer_status
                    if _sw44 == 1:
                        MpCanvas.quote_win = MpCanvas.input_text
                        self.pop_state()
                        return
                    elif _sw44 == (-49):
                        MpCanvas.error_msg = 5
                        self.push_state(4)
                        return
                    MpCanvas.error_msg = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 1288:
                    _m19 = True
                    _sw45 = MpCanvas.answer_status
                    if _sw45 == 1:
                        MpCanvas.attr_hp = k2.read_s16()
                        MpCanvas.attr_hp_bonus = k2.read_s16()
                        MpCanvas.attr_mp = k2.read_s16()
                        MpCanvas.attr_mp_bonus = k2.read_s16()
                        MpCanvas.attr_attack = k2.read_s16()
                        MpCanvas.attr_attack_bonus = k2.read_s16()
                        MpCanvas.attr_defense = k2.read_s16()
                        MpCanvas.attr_defense_bonus = k2.read_s16()
                        self.push_state(81)
                        return
                    MpCanvas.error_msg = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 1290:
                    _m19 = True
                    _sw46 = MpCanvas.answer_status
                    if _sw46 == 1:
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < 11:
                            MpCanvas.skill_levels[MpCanvas.loop_i] = 99
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        MpCanvas.skill_count = k2.read_s8()
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < MpCanvas.skill_count:
                            MpCanvas.skill_id = k2.read_s8()
                            MpCanvas.skill_levels[(MpCanvas.skill_id - 3)] = k2.read_s8()
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < MpCanvas.skill_slot_count:
                            MpCanvas.skill_order[MpCanvas.loop_i] = MpCanvas.skill_slots[MpCanvas.loop_i]
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        while MpCanvas.loop_i < 4:
                            MpCanvas.loop_j = 0
                            while MpCanvas.loop_j < 11:
                                MpCanvas.skill_taken = False
                                MpCanvas.loop_k = 0
                                while MpCanvas.loop_k < MpCanvas.loop_i:
                                    if MpCanvas.skill_order[MpCanvas.loop_k] == (3 + MpCanvas.loop_j):
                                        MpCanvas.skill_taken = True
                                        break
                                    MpCanvas.loop_k = MpCanvas.loop_k + 1
                                if not MpCanvas.skill_taken:
                                    MpCanvas.skill_order[MpCanvas.loop_i] = i8(((3 + MpCanvas.loop_j)))
                                    break
                                MpCanvas.loop_j = MpCanvas.loop_j + 1
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        self.push_state(82)
                        return
                    MpCanvas.error_msg = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 1292:
                    _m19 = True
                    _sw47 = MpCanvas.answer_status
                    if _sw47 == 1:
                        MpCanvas.loop_j = 0
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < 4:
                            if MpCanvas.skill_levels[(MpCanvas.skill_order[MpCanvas.loop_i] - 3)] != 99:
                                MpCanvas.skill_slots[MpCanvas.loop_j] = MpCanvas.skill_order[MpCanvas.loop_i]
                                MpCanvas.loop_j = MpCanvas.loop_j + 1
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        MpCanvas.skill_slot_count = MpCanvas.loop_j
                        MpCanvas.loop_i = MpCanvas.loop_j
                        while MpCanvas.loop_i < 4:
                            MpCanvas.skill_slots[MpCanvas.loop_j] = 99
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        self.pop_state()
                        return
                    MpCanvas.error_msg = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 1297:
                    _m19 = True
                    _sw48 = MpCanvas.answer_status
                    if _sw48 == 1:
                        MpCanvas.fame = k2.read_s32()
                        MpCanvas.duel_grade = k2.read_s32()
                        MpCanvas.mission_grade = k2.read_s32()
                        self.push_state(80)
                        return
                    MpCanvas.error_msg = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 1299:
                    _m19 = True
                    _sw49 = MpCanvas.answer_status
                    if _sw49 == 1:
                        MpCanvas.exp = k2.read_s32()
                        MpCanvas.fame = k2.read_s32()
                        MpCanvas.gold = k2.read_s32()
                        self.push_state(83)
                        return
                    MpCanvas.error_msg = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 1536:
                    _m19 = True
                    _sw50 = MpCanvas.answer_status
                    if _sw50 == 1:
                        MpCanvas.notice_kind = k2.read_s8()
                        n6 = 0
                        while n6 < 4:
                            MpCanvas.notice_lines[n6] = k2.read_string(16)
                            n6 = n6 + 1
                        MpCanvas.notices_left = 0
                        MpCanvas.set_state(6)
                    return
                if _m19 or _sw18 == 289:
                    _m19 = True
                    if MpCanvas.answer_status == 1:
                        _t51 = k2.read_s32()
                        MpCanvas.invitation_saved = _t51
                        MpCanvas.invitation = _t51
                        self.push_state(88)
                        return
                    MpCanvas.error_msg = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 291:
                    _m19 = True
                    if MpCanvas.answer_status == 1:
                        self.pop_state()
                        return
                    MpCanvas.error_msg = 0
                    self.push_state(4)
                break
        except _Brk_block0_1631:
            pass

    def menu_keys(self, n2):  # g.java:2589
        if MpCanvas.state_ticks < 2:
            return
        if (n2 == (-3)) or (n2 == (-1)):
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] > 0:
                n3 = MpCanvas.stack_depth
                MpCanvas.cursor_stack[n3] = (MpCanvas.cursor_stack[n3] - 1)
            else:
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = (MpCanvas.menu_size - 1)
        elif (n2 == (-4)) or (n2 == (-2)):
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] < (MpCanvas.menu_size - 1):
                n4 = MpCanvas.stack_depth
                MpCanvas.cursor_stack[n4] = (MpCanvas.cursor_stack[n4] + 1)
            else:
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = 0
        if n2 == (-5):
            self.menu_select()

    def yes_no_keys(self, n2):  # g.java:2613
        if MpCanvas.state_ticks < 2:
            return
        if (n2 == (-3)) or (n2 == (-1)):
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] > 0:
                n3 = MpCanvas.stack_depth
                MpCanvas.cursor_stack[n3] = (MpCanvas.cursor_stack[n3] - 1)
            else:
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = 1
        elif (n2 == (-4)) or (n2 == (-2)):
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] < 1:
                n4 = MpCanvas.stack_depth
                MpCanvas.cursor_stack[n4] = (MpCanvas.cursor_stack[n4] + 1)
            else:
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = 0
        if n2 == (-5):
            self.menu_select()
            return
        if n2 == (-7):
            if (MpCanvas.state == 160) and (MpCanvas.popup_style != 1):
                return
            MpCanvas.cursor_stack[MpCanvas.stack_depth] = 1
            self.menu_select()

    def keyPressed(self, n2):  # g.java:2645
        if (n2 == (-32)) or (n2 == (-33)):
            return
        if n2 == -100:                     # PORT-EXTRA: Tab = auto-battle on / off
            MpCanvas.auto_battle = not MpCanvas.auto_battle
            if MpCanvas.auto_battle and MpCanvas.state == 94 and MpCanvas.choose_secs > 1:
                MpCanvas.choose_secs = 1            # this round too
            return
        MpCanvas.key = n2
        if MpCanvas.paused:
            if MpCanvas.key == (-5):
                MpCanvas.request_pause(2)
            MpCanvas.key = (-999)

    def handle_key(self, var1_1):  # g.java:2661
        MpCanvas.ping_misses = 0
        MpCanvas.key_in = var1_1
        _sw52 = MpCanvas.state
        try:
            _m53 = False
            while True:
                if _m53 or _sw52 == 161:
                    _m53 = True
                    if MpCanvas.key_in == (-7):
                        self.pop_state()
                        return
                if _m53 or _sw52 in (11, 12, 16, 87, 162, 163, 164):
                    _m53 = True
                    if MpCanvas.key_in == (-7):
                        self.pop_state()
                        return
                    self.menu_keys(MpCanvas.key_in)
                    return
                if _m53 or _sw52 in (170, 171):
                    _m53 = True
                    if (MpCanvas.key_in != (-7)) and (MpCanvas.key_in != (-5)):
                        break
                    self.pop_state()
                    return
                if _m53 or _sw52 == 6:
                    _m53 = True
                    if MpCanvas.notices_left > 0:
                        MpCanvas.notice_page = MpCanvas.notice_page + 1
                        self.send_request(258)
                        return
                    if MpCanvas.notice_kind == 1:
                        self.reset_state_stack(7)
                        return
                    if MpCanvas.notice_kind != 9:
                        break
                    MpCanvas.set_state(300)
                    return
                if _m53 or _sw52 == 7:
                    _m53 = True
                    MpCanvas.menu_size = 2
                    MpCanvas.relogin_to_menu = False
                    self.reset_state_stack(10)
                    return
                if _m53 or _sw52 == 10:
                    _m53 = True
                    if MpCanvas.popup_shown:
                        if (MpCanvas.key_in == (-3)) or (MpCanvas.key_in == (-4)):
                            MpCanvas.popup_cursor = imod(((MpCanvas.popup_cursor + 1)), 2)
                            return
                        if MpCanvas.key_in != (-5):
                            break
                        if MpCanvas.popup_cursor == 0:
                            MpCanvas.set_state(300)
                            return
                        MpCanvas.popup_shown = False
                        return
                    if MpCanvas.key_in == (-6):
                        MpCanvas.disconnect()
                        MpCanvas.popup_kind = 0
                        MpCanvas.relogin_to_menu = True
                        MpCanvas.letter_cursor = 0
                        self.push_state(2)
                        return
                    if MpCanvas.key_in == (-7):
                        MpCanvas.popup_shown = True
                        MpCanvas.popup_cursor = 1
                        return
                    self.menu_keys(MpCanvas.key_in)
                    return
                if _m53 or _sw52 in (80, 81, 83):
                    _m53 = True
                    if (MpCanvas.key_in != (-5)) and (MpCanvas.key_in != (-7)):
                        break
                    self.pop_state()
                    return
                if _m53 or _sw52 == 82:
                    _m53 = True
                    if MpCanvas.key_in == (-1):
                        if MpCanvas.cursor_stack[MpCanvas.stack_depth] > 0:
                            v0 = MpCanvas.stack_depth
                            MpCanvas.cursor_stack[v0] = (MpCanvas.cursor_stack[v0] - 1)
                        else:
                            MpCanvas.cursor_stack[MpCanvas.stack_depth] = 3
                    elif MpCanvas.key_in == (-2):
                        if MpCanvas.cursor_stack[MpCanvas.stack_depth] < 3:
                            v1 = MpCanvas.stack_depth
                            MpCanvas.cursor_stack[v1] = (MpCanvas.cursor_stack[v1] + 1)
                        else:
                            MpCanvas.cursor_stack[MpCanvas.stack_depth] = 0
                    elif MpCanvas.key_in == (-3):
                        while True:
                            try:
                                if MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] > 3:
                                    v2 = MpCanvas.cursor_stack[MpCanvas.stack_depth]
                                    MpCanvas.skill_order[v2] = i8(((MpCanvas.skill_order[v2] - 1)))
                                else:
                                    MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] = 13
                                MpCanvas.skill_taken = False
                                MpCanvas.loop_i = 0
                                while MpCanvas.loop_i < 4:
                                    if (MpCanvas.loop_i != MpCanvas.cursor_stack[MpCanvas.stack_depth]) and (MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] == MpCanvas.skill_order[MpCanvas.loop_i]):
                                        MpCanvas.skill_taken = True
                                        raise _Cont_block47_2359()
                                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                            except _Cont_block47_2359:
                                pass
                            if not (MpCanvas.skill_taken):
                                break
                    elif MpCanvas.key_in == (-4):
                        while True:
                            try:
                                if MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] < 13:
                                    v3 = MpCanvas.cursor_stack[MpCanvas.stack_depth]
                                    MpCanvas.skill_order[v3] = i8(((MpCanvas.skill_order[v3] + 1)))
                                else:
                                    MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] = 3
                                MpCanvas.skill_taken = False
                                MpCanvas.loop_i = 0
                                while MpCanvas.loop_i < 4:
                                    if (MpCanvas.loop_i != MpCanvas.cursor_stack[MpCanvas.stack_depth]) and (MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] == MpCanvas.skill_order[MpCanvas.loop_i]):
                                        MpCanvas.skill_taken = True
                                        raise _Cont_block49_2378()
                                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                            except _Cont_block49_2378:
                                pass
                            if not (MpCanvas.skill_taken):
                                break
                    if (MpCanvas.key_in != (-5)) and (MpCanvas.key_in != (-7)):
                        break
                    self.menu_select()
                    return
                if _m53 or _sw52 == 84:
                    _m53 = True
                    if MpCanvas.key_in == (-7):
                        if len(MpCanvas.input_text) == 0:
                            if MpCanvas.quote_step == 0:
                                self.pop_state()
                                return
                            MpCanvas.quote_step = MpCanvas.quote_step - 1
                            return
                        MpCanvas.input_text = MpCanvas.input_text[0:(len(MpCanvas.input_text) - 1)]
                        return
                    if (MpCanvas.key_in == (-5)) or (MpCanvas.key_in == (-6)):
                        if len(MpCanvas.input_text) == 0:
                            if MpCanvas.letter_cursor >= 26:
                                break
                            MpCanvas.input_text = _js(MpCanvas.input_text, chr(((((65 + MpCanvas.letter_cursor))) & 0xFFFF)))
                            return
                        if len(MpCanvas.input_text) > 20:
                            break
                        if MpCanvas.letter_cursor < 26:
                            if len(MpCanvas.input_text) >= 20:
                                break
                            MpCanvas.input_text = _js(MpCanvas.input_text, chr(((((97 + MpCanvas.letter_cursor))) & 0xFFFF)))
                            return
                        if MpCanvas.letter_cursor == 26:
                            if len(MpCanvas.input_text) >= 20:
                                break
                            MpCanvas.input_text = _js(MpCanvas.input_text, chr(32))
                            return
                        if MpCanvas.letter_cursor != 27:
                            break
                        MpCanvas.loading_msg = 5
                        MpCanvas.input_text = MpCanvas.trim_right(MpCanvas.input_text)
                        if MpCanvas.quote_step == 0:
                            self.send_request(1282)
                        else:
                            self.send_request(1284)
                        MpCanvas.set_state(3)
                        return
                    MpCanvas.letter_grid_space_keys(MpCanvas.key_in)
                    return
                if _m53 or _sw52 == 85:
                    _m53 = True
                    if MpCanvas.key_in == (-7):
                        if len(MpCanvas.input_text) == 0:
                            self.pop_state()
                            return
                        MpCanvas.input_text = MpCanvas.input_text[0:(len(MpCanvas.input_text) - 1)]
                        return
                    if (MpCanvas.key_in == (-5)) or (MpCanvas.key_in == (-6)):
                        if len(MpCanvas.input_text) == 0:
                            if MpCanvas.letter_cursor >= 26:
                                break
                            MpCanvas.input_text = _js(MpCanvas.input_text, chr(((((65 + MpCanvas.letter_cursor))) & 0xFFFF)))
                            return
                        if len(MpCanvas.input_text) > 8:
                            break
                        if MpCanvas.letter_cursor < 26:
                            if len(MpCanvas.input_text) >= 8:
                                break
                            MpCanvas.input_text = _js(MpCanvas.input_text, chr(((((97 + MpCanvas.letter_cursor))) & 0xFFFF)))
                            return
                        if MpCanvas.letter_cursor != 26:
                            break
                        self.push_state(86)
                        return
                    MpCanvas.letter_grid_keys(MpCanvas.key_in)
                    return
                if _m53 or _sw52 == 88:
                    _m53 = True
                    if MpCanvas.key_in == (-1):
                        if MpCanvas.cursor_stack[MpCanvas.stack_depth] > 0:
                            v4 = MpCanvas.stack_depth
                            MpCanvas.cursor_stack[v4] = (MpCanvas.cursor_stack[v4] - 1)
                            return
                        MpCanvas.cursor_stack[MpCanvas.stack_depth] = 2
                        return
                    if MpCanvas.key_in == (-2):
                        if MpCanvas.cursor_stack[MpCanvas.stack_depth] < 2:
                            v5 = MpCanvas.stack_depth
                            MpCanvas.cursor_stack[v5] = (MpCanvas.cursor_stack[v5] + 1)
                            return
                        MpCanvas.cursor_stack[MpCanvas.stack_depth] = 0
                        return
                    if (MpCanvas.key_in == (-3)) or (MpCanvas.key_in == (-4)):
                        self.menu_select()
                        return
                    if MpCanvas.key_in == (-5):
                        MpCanvas.key_in = (-4)
                        self.menu_select()
                        return
                    if MpCanvas.key_in != (-7):
                        break
                    MpCanvas.save_options()
                    if MpCanvas.invitation != MpCanvas.invitation_saved:
                        MpCanvas.loading_msg = 1
                        MpCanvas.set_state(3)
                        self.send_request(290)
                        return
                    self.pop_state()
                    self.start_sound(1)
                    return
                if _m53 or _sw52 == 89:
                    _m53 = True
                    if MpCanvas.key_in == (-3):
                        if MpCanvas.help_page > 0:
                            MpCanvas.help_page = MpCanvas.help_page - 1
                            return
                        MpCanvas.help_page = (Consts.help_pages[MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]] - 1)
                        return
                    if (MpCanvas.key_in == (-4)) or (MpCanvas.key_in == (-5)):
                        if MpCanvas.help_page < (Consts.help_pages[MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]] - 1):
                            MpCanvas.help_page = MpCanvas.help_page + 1
                            return
                        MpCanvas.help_page = 0
                        return
                    if MpCanvas.key_in != (-7):
                        break
                    self.pop_state()
                    return
                if _m53 or _sw52 == 20:
                    _m53 = True
                    if MpCanvas.key_in == (-7):
                        self.pop_state()
                        return
                    self.menu_keys(MpCanvas.key_in)
                    return
                if _m53 or _sw52 == 21:
                    _m53 = True
                    if (MpCanvas.key_in == (-5)) or (MpCanvas.key_in == (-6)):
                        if len(MpCanvas.input_text) > 12:
                            break
                        if MpCanvas.letter_cursor < 26:
                            if len(MpCanvas.input_text) >= 12:
                                break
                            MpCanvas.input_text = _js(MpCanvas.input_text, chr(((((65 + MpCanvas.letter_cursor))) & 0xFFFF)))
                            return
                        if (MpCanvas.letter_cursor != 26) or (len(MpCanvas.input_text) < 4):
                            break
                        _sw54 = MpCanvas.room_mode
                        if _sw54 == 0:
                            MpCanvas.loading_msg = 2
                        elif _sw54 == 1:
                            MpCanvas.loading_msg = 4
                        elif _sw54 == 2:
                            MpCanvas.loading_msg = 4
                        MpCanvas.loading_msg = 0
                        self.send_request(768)
                        MpCanvas.set_state(3)
                        return
                    if var1_1 == (-7):
                        if len(MpCanvas.input_text) == 0:
                            self.pop_state()
                            return
                        MpCanvas.input_text = MpCanvas.input_text[0:(len(MpCanvas.input_text) - 1)]
                        return
                    MpCanvas.letter_grid_keys(var1_1)
                    return
                if _m53 or _sw52 == 94:
                    _m53 = True
                    if MpCanvas.exit_prompt:
                        if (MpCanvas.key_in == (-3)) or (MpCanvas.key_in == (-4)):
                            MpCanvas.exit_cursor = imod(((MpCanvas.exit_cursor + 1)), 2)
                            return
                        if MpCanvas.key_in != (-5):
                            break
                        if MpCanvas.exit_cursor == 0:
                            MpCanvas.relogin_to_menu = False
                            MpCanvas.disconnect()
                            MpCanvas.set_timer((-1))
                            MpCanvas.loading_msg = 0
                            MpCanvas.password_login = False
                            MpCanvas.set_state(10000)
                            return
                        MpCanvas.exit_prompt = False
                        return
                    MpCanvas.chosen_action = 99
                    if MpCanvas.key_in == (-1):
                        MpCanvas.chosen_action = 2
                    elif MpCanvas.key_in == (-3):
                        MpCanvas.chosen_action = 1
                    elif MpCanvas.key_in == (-4):
                        MpCanvas.chosen_action = 0
                    elif MpCanvas.key_in == (-2):
                        if MpCanvas.skill_slot_count > 0:
                            MpCanvas.loop_k = 0
                            while MpCanvas.loop_k < MpCanvas.skill_slot_count:
                                if MpCanvas.fighter_mp[0] >= MpCanvas.skill_costs[(MpCanvas.skill_slots[MpCanvas.loop_k] - 3)]:
                                    MpCanvas.chosen_action = 20
                                    break
                                MpCanvas.loop_k = MpCanvas.loop_k + 1
                    elif (MpCanvas.key_in == (-7)) and (not MpCanvas.exit_asked):
                        MpCanvas.exit_asked = True
                        MpCanvas.exit_prompt = True
                        MpCanvas.exit_cursor = 1
                        MpCanvas.exit_prompt_time = system.currentTimeMillis()
                    if MpCanvas.chosen_action == 20:
                        MpCanvas.set_state(95)
                        return
                    if MpCanvas.chosen_action == 99:
                        break
                    MpCanvas.set_state(96)
                    return
                if _m53 or _sw52 == 95:
                    _m53 = True
                    if MpCanvas.key_in == (-1):
                        MpCanvas.skill_cursor = (_inc(MpCanvas, 'skill_cursor', -1) if (MpCanvas.skill_cursor > 0) else (MpCanvas.skill_slot_count - 1))
                    elif MpCanvas.key_in == (-2):
                        MpCanvas.skill_cursor = (_inc(MpCanvas, 'skill_cursor', 1) if (MpCanvas.skill_cursor < (MpCanvas.skill_slot_count - 1)) else 0)
                    if MpCanvas.key_in == (-5):
                        if MpCanvas.fighter_mp[0] < MpCanvas.skill_costs[(MpCanvas.skill_slots[MpCanvas.skill_cursor] - 3)]:
                            break
                        MpCanvas.chosen_action = MpCanvas.skill_slots[MpCanvas.skill_cursor]
                        MpCanvas.set_state(96)
                        return
                    if MpCanvas.key_in != (-7):
                        break
                    MpCanvas.chosen_action = 99
                    MpCanvas.set_state(94)
                    return
                if _m53 or _sw52 == 96:
                    _m53 = True
                    if (MpCanvas.key_in == (-1)) or (MpCanvas.key_in == (-2)):
                        _sw55 = MpCanvas.chosen_action
                        _m56 = False
                        while True:
                            if _m56 or _sw55 in (9, 10):
                                _m56 = True
                                MpCanvas.loop_i = 0
                                while MpCanvas.loop_i < 4:
                                    if (MpCanvas.fighter_present[MpCanvas.loop_i] and (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == imod(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2))) and (MpCanvas.fighter_slot[MpCanvas.loop_i] != MpCanvas.fighter_slot[MpCanvas.target_cursor]):
                                        MpCanvas.target_cursor = MpCanvas.loop_i
                                        raise _Brk_block0_2273()
                                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                                raise _Brk_block0_2273()
                            if _m56 or _sw55 in (0, 3, 4, 5, 6, 7):
                                _m56 = True
                                MpCanvas.loop_i = 1
                                while MpCanvas.loop_i < 4:
                                    if (MpCanvas.fighter_present[MpCanvas.loop_i] and (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == imod(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2))) and (MpCanvas.fighter_slot[MpCanvas.loop_i] != MpCanvas.fighter_slot[MpCanvas.target_cursor]):
                                        MpCanvas.target_cursor = MpCanvas.loop_i
                                        raise _Brk_block0_2273()
                                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                            if _m56 or _sw55 not in (9, 10, 0, 3, 4, 5, 6, 7):
                                _m56 = True
                                return
                            break
                    if MpCanvas.key_in == (-5):
                        self.start_timing()
                        return
                    if MpCanvas.key_in != (-7):
                        break
                    _sw57 = MpCanvas.chosen_action
                    if _sw57 in (3, 4, 5, 6, 7, 9, 10):
                        MpCanvas.set_state(95)
                        return
                    MpCanvas.set_state(94)
                    return
                if _m53 or _sw52 == 97:
                    _m53 = True
                    if (MpCanvas.state_ticks <= 0) or (MpCanvas.key_in != (-5)):
                        break
                    self.stop_timing()
                    return
                if _m53 or _sw52 == 105:
                    _m53 = True
                    if (MpCanvas.state_ticks <= idiv(1000, MpCanvas.tick_ms)) or (MpCanvas.key_in != (-5)):
                        break
                    self.reset_state_stack(10)
                    _sw58 = MpCanvas.room_mode
                    _m59 = False
                    while True:
                        if _m59 or _sw58 == 0:
                            _m59 = True
                            self.push_state(11)
                            raise _Brk_block0_2273()
                        if _m59 or _sw58 == 1:
                            _m59 = True
                            self.push_state(11)
                            MpCanvas.cursor_stack[MpCanvas.stack_depth] = 1
                            raise _Brk_block0_2273()
                        if _m59 or _sw58 == 2:
                            _m59 = True
                            MpCanvas.cursor_stack[MpCanvas.stack_depth] = 1
                            self.push_state(12)
                        break
                    return
                if _m53 or _sw52 == 4:
                    _m53 = True
                    if MpCanvas.popup_shown:
                        if (MpCanvas.key_in == (-3)) or (MpCanvas.key_in == (-4)):
                            MpCanvas.popup_cursor = imod(((MpCanvas.popup_cursor + 1)), 2)
                            return
                        if MpCanvas.key_in != (-5):
                            break
                        if MpCanvas.popup_cursor == 0:
                            MpCanvas.set_state(300)
                            return
                        MpCanvas.popup_shown = False
                        MpCanvas.popup_cursor = 1
                        return
                    if MpCanvas.key_in == (-6):
                        if (MpCanvas.error_msg != 7) and (MpCanvas.error_msg != 1):
                            break
                        MpCanvas.disconnect()
                        MpCanvas.popup_kind = 0
                        MpCanvas.relogin_to_menu = True
                        MpCanvas.set_state(2)
                        MpCanvas.popup_shown = False
                        return
                    if MpCanvas.key_in == (-7):
                        if (MpCanvas.error_msg != 7) and (MpCanvas.error_msg != 1):
                            break
                        MpCanvas.popup_shown = True
                        MpCanvas.popup_cursor = 1
                        return
                    if MpCanvas.key_in != (-5):
                        break
                    if not NetThread.connected:
                        if ((MpCanvas.error_msg == 14) or (MpCanvas.error_msg == 15)) or (MpCanvas.error_msg == 16):
                            self.pop_state()
                            return
                        if MpCanvas.error_msg == 17:
                            MpCanvas.popup_kind = 0
                            MpCanvas.relogin_to_menu = True
                            self.push_state(2)
                            return
                        if MpCanvas.error_msg != 1:
                            MpCanvas.loading_msg = 0
                            MpCanvas.set_state(10000)
                            return
                        self.reset_state_stack(1)
                        return
                    if MpCanvas.pending_state > (-1):
                        self.push_state(MpCanvas.pending_state)
                        MpCanvas.pending_state = (-1)
                        return
                    _sw60 = MpCanvas.state_stack[(MpCanvas.stack_depth - 1)]
                    if _sw60 == 105:
                        return
                    elif _sw60 == 86:
                        self.pop_states(2)
                        return
                    self.pop_state()
                    return
                if _m53 or _sw52 == 5:
                    _m53 = True
                    if (MpCanvas.key_in == (-3)) or (MpCanvas.key_in == (-4)):
                        MpCanvas.cursor_stack[MpCanvas.stack_depth] = imod(((MpCanvas.cursor_stack[MpCanvas.stack_depth] + 1)), 2)
                        return
                    if MpCanvas.key_in != (-5):
                        break
                    if MpCanvas.cursor_stack[MpCanvas.stack_depth] == 0:
                        if MpCanvas.volume == 0:
                            MpCanvas.volume = 4
                    else:
                        MpCanvas.volume = 0
                    MpCanvas.save_options()
                    MpCanvas.set_state(1)
                    self.start_music(1)
                    return
                if _m53 or _sw52 == 1:
                    _m53 = True
                    if MpCanvas.state_ticks <= 3:
                        break
                    if MpCanvas.user_id == "":
                        MpCanvas.popup_kind = 0
                        self.push_state(2)
                        return
                    if MpCanvas.error_msg == 1:
                        MpCanvas.set_state(4)
                        return
                    MpCanvas.loading_msg = 0
                    MpCanvas.password_login = False
                    MpCanvas.set_state(10000)
                    return
                if _m53 or _sw52 == 2:
                    _m53 = True
                    self.popup_keys(MpCanvas.key_in)
                    return
                if _m53 or _sw52 in (86, 160):
                    _m53 = True
                    self.yes_no_keys(MpCanvas.key_in)
                break
        except _Brk_block0_2273:
            pass

    @staticmethod
    def update_bars():  # g.java:3263
        MpCanvas.fighter_hp_delta[MpCanvas.loop_i] = (MpCanvas.fighter_hp_target[MpCanvas.loop_i] - MpCanvas.fighter_hp[MpCanvas.loop_i])
        MpCanvas.fighter_hp_step[MpCanvas.loop_i] = idiv(MpCanvas.fighter_hp_delta[MpCanvas.loop_i], 5)
        if MpCanvas.fighter_hp_step[MpCanvas.loop_i] == 0:
            if MpCanvas.fighter_hp_target[MpCanvas.loop_i] > MpCanvas.fighter_hp[MpCanvas.loop_i]:
                MpCanvas.fighter_hp_step[MpCanvas.loop_i] = 1
            elif MpCanvas.fighter_hp_target[MpCanvas.loop_i] < MpCanvas.fighter_hp[MpCanvas.loop_i]:
                MpCanvas.fighter_hp_step[MpCanvas.loop_i] = (-1)
        MpCanvas.fighter_mp_step[MpCanvas.loop_i] = idiv(((MpCanvas.fighter_mp_target[MpCanvas.loop_i] - MpCanvas.fighter_mp[MpCanvas.loop_i])), 5)
        if MpCanvas.fighter_mp_step[MpCanvas.loop_i] == 0:
            if MpCanvas.fighter_mp_target[MpCanvas.loop_i] > MpCanvas.fighter_mp[MpCanvas.loop_i]:
                MpCanvas.fighter_mp_step[MpCanvas.loop_i] = 1
                return
            if MpCanvas.fighter_mp_target[MpCanvas.loop_i] < MpCanvas.fighter_mp[MpCanvas.loop_i]:
                MpCanvas.fighter_mp_step[MpCanvas.loop_i] = (-1)

    def reset_turn(self):  # g.java:3285
        MpCanvas.anim_frame = 0
        MpCanvas.target2 = (-1)
        MpCanvas.damage_tick = (-1)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                MpCanvas.fighter_anim[MpCanvas.loop_i] = 0
                MpCanvas.fighter_anim_tick[MpCanvas.loop_i] = 0
                MpCanvas.fighter_anim_len[MpCanvas.loop_i] = 0
                MpCanvas.fighter_hp_delta[MpCanvas.loop_i] = 0
                if MpCanvas.fighter_slot[MpCanvas.loop_i] == MpCanvas.turn_bytes[(0 + MpCanvas.turn_rec)]:
                    MpCanvas.attacker = MpCanvas.loop_i
                    MpCanvas.fighter_hp_target[MpCanvas.loop_i] = MpCanvas.turn_hps[(0 + MpCanvas.turn_rec)]
                    MpCanvas.fighter_mp_target[MpCanvas.loop_i] = MpCanvas.turn_bytes[(8 + MpCanvas.turn_rec)]
                    MpCanvas.update_bars()
                if MpCanvas.fighter_slot[MpCanvas.loop_i] == MpCanvas.turn_bytes[(12 + MpCanvas.turn_rec)]:
                    MpCanvas.target = MpCanvas.loop_i
                    MpCanvas.fighter_hp_target[MpCanvas.loop_i] = MpCanvas.turn_hps[(4 + MpCanvas.turn_rec)]
                    MpCanvas.fighter_mp_target[MpCanvas.loop_i] = MpCanvas.turn_bytes[(20 + MpCanvas.turn_rec)]
                    MpCanvas.update_bars()
                    _sw61 = MpCanvas.turn_bytes[(16 + MpCanvas.turn_rec)]
                    _m62 = False
                    while True:
                        if _m62 or _sw61 == 1:
                            _m62 = True
                            if MpCanvas.turn_actions[MpCanvas.target] == 1:
                                MpCanvas.target_reaction = 4
                                break
                            MpCanvas.target_reaction = 1
                            break
                        if _m62 or _sw61 == 2:
                            _m62 = True
                            MpCanvas.target_reaction = 5
                        break
                if (MpCanvas.turn_bytes[(24 + MpCanvas.turn_rec)] > 0) and (MpCanvas.fighter_slot[MpCanvas.loop_i] == MpCanvas.turn_bytes[(32 + MpCanvas.turn_rec)]):
                    MpCanvas.target2 = MpCanvas.loop_i
                    MpCanvas.fighter_hp_target[MpCanvas.loop_i] = MpCanvas.turn_hps[(8 + MpCanvas.turn_rec)]
                    MpCanvas.fighter_mp_target[MpCanvas.loop_i] = MpCanvas.turn_bytes[(40 + MpCanvas.turn_rec)]
                    MpCanvas.update_bars()
                    _sw63 = MpCanvas.turn_bytes[(36 + MpCanvas.turn_rec)]
                    _m64 = False
                    while True:
                        if _m64 or _sw63 == 1:
                            _m64 = True
                            if MpCanvas.turn_actions[MpCanvas.target2] == 1:
                                MpCanvas.target2_reaction = 4
                                break
                            MpCanvas.target2_reaction = 1
                            break
                        if _m64 or _sw63 == 2:
                            _m64 = True
                            MpCanvas.target2_reaction = 5
                        break
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        _sw65 = MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)]
        if _sw65 in (3, 4, 5, 6, 7, 8):
            MpCanvas.fighter_anim[MpCanvas.attacker] = 8
        elif _sw65 in (2, 9, 10):
            MpCanvas.fighter_anim[MpCanvas.attacker] = 12
        elif _sw65 in (11, 12, 13):
            MpCanvas.fighter_anim[MpCanvas.attacker] = 13
        elif _sw65 == 0:
            MpCanvas.fighter_anim[MpCanvas.attacker] = 2
            MpCanvas.run_dx = idiv((((MpCanvas.canvas_w - 67) - 42)), Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]])
            MpCanvas.run_dy = (0 if (MpCanvas.room_mode == 0) else ((0 if (idiv(MpCanvas.fighter_slot[MpCanvas.attacker], 2) == idiv(MpCanvas.turn_bytes[(12 + MpCanvas.turn_rec)], 2)) else ((idiv(46, Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]]) if (idiv(MpCanvas.fighter_slot[MpCanvas.attacker], 2) == 0) else idiv((-46), Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]]))))))
        MpCanvas.anim_length = Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]]

    def login(self):  # g.java:3374
        if MpCanvas.password_login:
            self.send_request(278)
            return
        self.send_request(262)

    def connect(self):  # g.java:3382
        MpCanvas.ping_off = False
        if not NetThread.connected:
            if MpCanvas.net is None:
                MpCanvas.net = NetThread()
                MpCanvas.net.setPriority(10)
                MpCanvas.net.start()
            NetThread.set_game(self)
            MpCanvas.connecting = True
            MpCanvas.net.set_address(MpCanvas.server_host, MpCanvas.server_port)

    @staticmethod
    def disconnect():  # g.java:3396
        MpCanvas.disconnecting = True
        NetThread.connected = False
        MpCanvas.rng.k = False
        MpCanvas.sleep(400)
        if MpCanvas.net is not None:
            NetThread.close()
        MpCanvas.net = None
        MpCanvas.relogin = True
        MpCanvas.set_timer((-1))
        MpCanvas.sleep(100)

    def on_disconnect(self):  # g.java:3410
        MpCanvas.disconnect()
        if MpCanvas.error_msg > (-1):
            self.show_error_screen()

    def show_error_screen(self):  # g.java:3417
        if MpCanvas.skip_error_screen:
            MpCanvas.skip_error_screen = False
            return
        MpCanvas.set_state(4)

    def on_net_error(self, n2):  # g.java:3425
        if not MpCanvas.disconnecting:
            MpCanvas.error_msg = (7 if (n2 < 10) else n2)
            self.on_disconnect()
        MpCanvas.disconnecting = False

    def hideNotify(self):  # g.java:3433
        self.stop_music()
        MpCanvas.request_pause(1)

    def showNotify(self):  # g.java:3438
        MpCanvas.request_pause(1)

    def draw_box(self, graphics, n2, n3, n4, n5, n6):  # g.java:3442
        n7 = 0x525152
        n8 = 0xFFFFFF
        _sw66 = n6
        if _sw66 in (0, 7):
            if imod(n4, 2) == 1:
                n4 = n4 + 1
            if imod(n5, 2) == 1:
                n5 = n5 + 1
            MpCanvas.win_x = (n2 - idiv(n4, 2))
            MpCanvas.win_y = (n3 - idiv(n5, 2))
            if n6 == 0:
                Draw.fill_rect(graphics, MpCanvas.win_x, MpCanvas.win_y, n4, n5, 0)
            Draw.draw_rect(graphics, (MpCanvas.win_x + 1), (MpCanvas.win_y + 1), (n4 - 2), (n5 - 2), 0xADAAAD)
            MpCanvas.draw_left_half_on(graphics, (MpCanvas.win_x + Consts.ui_dx[2]), (MpCanvas.win_y + Consts.ui_dy[2]), MpCanvas.ui_images[2])
            MpCanvas.draw_right_half_on(graphics, ((MpCanvas.win_x + n4) + Consts.ui_dx[2]), (MpCanvas.win_y + Consts.ui_dy[2]), MpCanvas.ui_images[2])
            MpCanvas.draw_left_half_on(graphics, (MpCanvas.win_x + Consts.ui_dx[3]), ((((MpCanvas.win_y + n5) - 2) - 5) + Consts.ui_dy[3]), MpCanvas.ui_images[3])
            MpCanvas.draw_right_half_on(graphics, ((MpCanvas.win_x + n4) + Consts.ui_dx[3]), ((((MpCanvas.win_y + n5) - 2) - 5) + Consts.ui_dy[3]), MpCanvas.ui_images[3])
            return
        elif _sw66 == 1:
            MpCanvas.fill_rect_on(graphics, n2, n3, n4, n5, 0)
            MpCanvas.set_color(graphics, 0xBDBABD)
            MpCanvas.draw_line(graphics, (n2 + 14), n3, (((n2 + n4) - 14) - 1), n3)
            MpCanvas.draw_line(graphics, (n2 + 14), ((n3 + n5) - 1), (((n2 + n4) - 14) - 1), ((n3 + n5) - 1))
            MpCanvas.set_color(graphics, 0x949A94)
            MpCanvas.draw_line(graphics, (n2 + 1), n3, (n2 + 13), n3)
            MpCanvas.draw_line(graphics, ((n2 + n4) - 14), n3, ((n2 + n4) - 2), n3)
            MpCanvas.draw_line(graphics, (n2 + 1), ((n3 + n5) - 1), (n2 + 13), ((n3 + n5) - 1))
            MpCanvas.draw_line(graphics, ((n2 + n4) - 14), ((n3 + n5) - 1), ((n2 + n4) - 2), ((n3 + n5) - 1))
            MpCanvas.set_color(graphics, 0xADAAAD)
            MpCanvas.draw_line(graphics, (n2 + 5), n3, (n2 + 8), n3)
            MpCanvas.draw_line(graphics, ((n2 + n4) - 9), n3, ((n2 + n4) - 6), n3)
            MpCanvas.draw_line(graphics, (n2 + 5), ((n3 + n5) - 1), (n2 + 8), ((n3 + n5) - 1))
            MpCanvas.draw_line(graphics, ((n2 + n4) - 9), ((n3 + n5) - 1), ((n2 + n4) - 6), ((n3 + n5) - 1))
            MpCanvas.set_color(graphics, 0x949A94)
            MpCanvas.draw_line(graphics, n2, (n3 + 1), n2, ((n3 + n5) - 2))
            MpCanvas.draw_line(graphics, ((n2 + n4) - 1), (n3 + 1), ((n2 + n4) - 1), ((n3 + n5) - 2))
            MpCanvas.set_color(graphics, 0xADAAAD)
            MpCanvas.draw_line(graphics, n2, (n3 + 4), n2, ((n3 + n5) - 5))
            MpCanvas.draw_line(graphics, ((n2 + n4) - 1), (n3 + 4), ((n2 + n4) - 1), ((n3 + n5) - 5))
            return
        elif _sw66 == 3:
            MpCanvas.set_color(graphics, n8)
            MpCanvas.draw_line(graphics, n2, (n3 - 1), ((n2 + n4) - 1), (n3 - 1))
            MpCanvas.draw_line(graphics, n2, (n3 + n5), ((n2 + n4) - 1), (n3 + n5))
            MpCanvas.draw_line(graphics, (n2 - 1), n3, (n2 - 1), ((n3 + n5) - 1))
            MpCanvas.draw_line(graphics, (n2 + n4), n3, (n2 + n4), ((n3 + n5) - 1))
            MpCanvas.draw_dot(graphics, n2, n3, n8)
            MpCanvas.draw_dot(graphics, ((n2 + n4) - 1), n3, n8)
            MpCanvas.draw_dot(graphics, n2, ((n3 + n5) - 1), n8)
            MpCanvas.draw_dot(graphics, ((n2 + n4) - 1), ((n3 + n5) - 1), n8)
            return
        Draw.fill_rect(graphics, n2, (n3 + 1), 1, (n5 - 2), n7)
        Draw.fill_rect(graphics, ((n2 + n4) - 1), (n3 + 1), 1, (n5 - 2), n7)
        MpCanvas.loop_j = 1
        while MpCanvas.loop_j < (n4 - 1):
            Draw.fill_rect(graphics, (n2 + MpCanvas.loop_j), n3, 1, n5, n7)
            Draw.fill_rect(graphics, (n2 + MpCanvas.loop_j), (n3 + 1), 1, (n5 - 2), 0)
            MpCanvas.loop_j = MpCanvas.loop_j + 1

    def menu_select(self):  # g.java:3512
        _sw67 = MpCanvas.state
        try:
            _m68 = False
            while True:
                if _m68 or _sw67 == 160:
                    _m68 = True
                    _sw69 = MpCanvas.popup_style
                    _m70 = False
                    while True:
                        if _m70 or _sw69 == 1:
                            _m70 = True
                            if MpCanvas.cursor_stack[MpCanvas.stack_depth] == 0:
                                MpCanvas.loading_msg = 5
                                MpCanvas.set_state(3)
                                raise _Brk_block0_2989()
                            self.on_disconnect()
                            MpCanvas.set_state(1)
                            raise _Brk_block0_2989()
                        if _m70 or _sw69 in (0, 2):
                            _m70 = True
                            self.on_disconnect()
                            MpCanvas.set_state(1)
                        break
                    return
                if _m68 or _sw67 == 161:
                    _m68 = True
                    MpCanvas.rank_kind = i8(MpCanvas.cursor_stack[MpCanvas.stack_depth])
                    MpCanvas.loading_msg = 1
                    MpCanvas.set_state(3)
                    self.send_request(1300)
                    return
                if _m68 or _sw67 in (162, 163, 164):
                    _m68 = True
                    MpCanvas.rank_list_state = MpCanvas.state
                    MpCanvas.rank_list_kind = ((((((MpCanvas.state_stack[MpCanvas.stack_depth] - 162) + 1)) * 10) + MpCanvas.cursor_stack[MpCanvas.stack_depth]) + 1)
                    MpCanvas.loading_msg = 1
                    MpCanvas.set_state(3)
                    self.send_request(1293)
                    return
                if _m68 or _sw67 == 10:
                    _m68 = True
                    _sw71 = MpCanvas.cursor_stack[MpCanvas.stack_depth]
                    _m72 = False
                    while True:
                        if _m72 or _sw71 == 0:
                            _m72 = True
                            self.push_state(11)
                            raise _Brk_block0_2989()
                        if _m72 or _sw71 == 1:
                            _m72 = True
                            self.push_state(12)
                            raise _Brk_block0_2989()
                        if _m72 or _sw71 == 2:
                            _m72 = True
                            self.push_state(16)
                            raise _Brk_block0_2989()
                        if _m72 or _sw71 == 3:
                            _m72 = True
                            MpCanvas.loading_msg = 1
                            MpCanvas.set_state(3)
                            self.send_request(288)
                            raise _Brk_block0_2989()
                        if _m72 or _sw71 == 4:
                            _m72 = True
                            self.push_state(87)
                            raise _Brk_block0_2989()
                        if _m72 or _sw71 == 5:
                            _m72 = True
                            self.push_state(161)
                        break
                    return
                if _m68 or _sw67 == 11:
                    _m68 = True
                    _sw73 = MpCanvas.cursor_stack[MpCanvas.stack_depth]
                    _m74 = False
                    while True:
                        if _m74 or _sw73 == 0:
                            _m74 = True
                            MpCanvas.room_mode = 0
                            MpCanvas.loading_msg = 2
                            MpCanvas.set_state(3)
                            self.send_request(512)
                            raise _Brk_block0_2989()
                        if _m74 or _sw73 == 1:
                            _m74 = True
                            MpCanvas.room_mode = 1
                            MpCanvas.loading_msg = 2
                            MpCanvas.set_state(3)
                            self.send_request(512)
                            raise _Brk_block0_2989()
                        if _m74 or _sw73 == 2:
                            _m74 = True
                            self.push_state(20)
                            raise _Brk_block0_2989()
                        if _m74 or _sw73 == 3:
                            _m74 = True
                            self.push_state(87)
                            raise _Brk_block0_2989()
                        if _m74 or _sw73 == 4:
                            _m74 = True
                            self.push_state(161)
                        break
                    return
                if _m68 or _sw67 == 12:
                    _m68 = True
                    _sw75 = MpCanvas.cursor_stack[MpCanvas.stack_depth]
                    _m76 = False
                    while True:
                        if _m76 or _sw75 == 0:
                            _m76 = True
                            MpCanvas.room_mode = i8(2)
                            MpCanvas.loading_msg = 3
                            MpCanvas.set_state(3)
                            self.send_request(512)
                            raise _Brk_block0_2989()
                        if _m76 or _sw75 == 1:
                            _m76 = True
                            MpCanvas.room_mode = i8(2)
                            self.push_state(21)
                            raise _Brk_block0_2989()
                        if _m76 or _sw75 == 2:
                            _m76 = True
                            self.push_state(87)
                            raise _Brk_block0_2989()
                        if _m76 or _sw75 == 3:
                            _m76 = True
                            self.push_state(161)
                        break
                    return
                if _m68 or _sw67 == 16:
                    _m68 = True
                    _sw77 = MpCanvas.cursor_stack[MpCanvas.stack_depth]
                    _m78 = False
                    while True:
                        if _m78 or _sw77 == 0:
                            _m78 = True
                            MpCanvas.loading_msg = 1
                            MpCanvas.set_state(3)
                            self.send_request(1296)
                            raise _Brk_block0_2989()
                        if _m78 or _sw77 == 1:
                            _m78 = True
                            MpCanvas.loading_msg = 1
                            MpCanvas.set_state(3)
                            self.send_request(1287)
                            raise _Brk_block0_2989()
                        if _m78 or _sw77 == 2:
                            _m78 = True
                            MpCanvas.loading_msg = 1
                            MpCanvas.set_state(3)
                            self.send_request(1289)
                            raise _Brk_block0_2989()
                        if _m78 or _sw77 == 3:
                            _m78 = True
                            MpCanvas.loading_msg = 1
                            MpCanvas.set_state(3)
                            self.send_request(1298)
                            raise _Brk_block0_2989()
                        if _m78 or _sw77 == 4:
                            _m78 = True
                            MpCanvas.letter_cursor = 0
                            MpCanvas.quote_step = 0
                            MpCanvas.input_text = MpCanvas.quote_start
                            self.push_state(84)
                            raise _Brk_block0_2989()
                        if _m78 or _sw77 == 5:
                            _m78 = True
                            MpCanvas.letter_cursor = 0
                            MpCanvas.input_text = MpCanvas.name
                            self.push_state(85)
                        break
                    return
                if _m68 or _sw67 == 82:
                    _m68 = True
                    MpCanvas.loading_msg = 5
                    MpCanvas.set_state(3)
                    self.send_request(1291)
                    return
                if _m68 or _sw67 == 84:
                    _m68 = True
                    return
                if _m68 or _sw67 == 86:
                    _m68 = True
                    _sw79 = MpCanvas.cursor_stack[MpCanvas.stack_depth]
                    _m80 = False
                    while True:
                        if _m80 or _sw79 == 0:
                            _m80 = True
                            MpCanvas.loading_msg = 5
                            MpCanvas.set_state(3)
                            self.send_request(1280)
                            raise _Brk_block0_2989()
                        if _m80 or _sw79 == 1:
                            _m80 = True
                            self.pop_states(1)
                        break
                    return
                if _m68 or _sw67 == 88:
                    _m68 = True
                    _sw81 = MpCanvas.cursor_stack[MpCanvas.stack_depth]
                    _m82 = False
                    while True:
                        if _m82 or _sw81 == 0:
                            _m82 = True
                            if MpCanvas.key_in == (-4):
                                if _inc(MpCanvas, 'speed', 1) <= 2:
                                    break
                                MpCanvas.speed = 0
                                raise _Brk_block0_2989()
                            if (MpCanvas.key_in != (-3)) or (_inc(MpCanvas, 'speed', -1) >= 0):
                                break
                            MpCanvas.speed = 2
                            raise _Brk_block0_2989()
                        if _m82 or _sw81 == 1:
                            _m82 = True
                            if (MpCanvas.key_in != (-3)) and (MpCanvas.key_in != (-4)):
                                break
                            MpCanvas.invitation = imod(((MpCanvas.invitation + 1)), 2)
                            raise _Brk_block0_2989()
                        if _m82 or _sw81 == 2:
                            _m82 = True
                            if MpCanvas.key_in == (-3):
                                self.volume_down()
                                raise _Brk_block0_2989()
                            if MpCanvas.key_in != (-4):
                                break
                            self.volume_up()
                        break
                    return
                if _m68 or _sw67 == 87:
                    _m68 = True
                    self.push_state(89)
                    return
                if _m68 or _sw67 == 20:
                    _m68 = True
                    _sw83 = MpCanvas.cursor_stack[MpCanvas.stack_depth]
                    if _sw83 == 0:
                        MpCanvas.room_mode = 0
                    elif _sw83 == 1:
                        MpCanvas.room_mode = 1
                    self.push_state(21)
                break
        except _Brk_block0_2989:
            pass

    def draw_notice(self):  # g.java:3746
        self.draw_buffer()
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 116, 76, 0)
        n2 = 0
        while n2 < 4:
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 31) + (12 * n2)), MpCanvas.notice_lines[n2], 0xFFFFFF)
            n2 = n2 + 1
        self.draw_ok_button((MpCanvas.center_y + 22))

    def draw_turn_fighters(self):  # g.java:3757
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i] and (MpCanvas.loop_i != MpCanvas.attacker):
                _sw84 = MpCanvas.fighter_anim[MpCanvas.loop_i]
                if _sw84 == 0:
                    self.draw_fighter_idle(MpCanvas.screen_g)
                elif _sw84 in (1, 4):
                    self.draw_fighter_hit()
                elif _sw84 == 5:
                    self.draw_fighter_evade()
                elif _sw84 == 6:
                    self.draw_fighter_dying()
                else:
                    self.draw_fighter_anim()
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.loop_i = MpCanvas.attacker
        _sw85 = MpCanvas.fighter_anim[MpCanvas.attacker]
        if _sw85 in (2, 28):
            self.draw_fighter_run()
            return
        elif _sw85 == 6:
            self.draw_fighter_dying()
            return
        self.draw_fighter_anim()

    def draw_fighter_hit(self):  # g.java:3801
        MpCanvas.anim_id = MpCanvas.fighter_anim[MpCanvas.loop_i]
        if MpCanvas.fighter_kind[MpCanvas.loop_i] == 2:
            MpCanvas.anim_id = (MpCanvas.anim_id + 21)
        MpCanvas.fighter_frame[MpCanvas.loop_i] = Consts.anim_first_frame[MpCanvas.anim_id]
        n2 = MpCanvas.loop_i
        MpCanvas.fighter_x[n2] = (MpCanvas.fighter_x[n2] - 2)
        MpCanvas.fighter_fx_frame[MpCanvas.loop_i] = (-1)
        self.draw_fighter(MpCanvas.screen_g, MpCanvas.loop_i)

    def draw_fighter_evade(self):  # g.java:3813
        MpCanvas.anim_id = (26 if (MpCanvas.fighter_kind[MpCanvas.loop_i] == 2) else 5)
        MpCanvas.fighter_frame[MpCanvas.loop_i] = Consts.anim_first_frame[MpCanvas.anim_id]
        if MpCanvas.fighter_anim_tick[MpCanvas.loop_i] == 0:
            n2 = MpCanvas.loop_i
            MpCanvas.fighter_x[n2] = (MpCanvas.fighter_x[n2] - 6)
            self.start_sound(3)
        elif MpCanvas.fighter_anim_tick[MpCanvas.loop_i] == 1:
            n3 = MpCanvas.loop_i
            MpCanvas.fighter_x[n3] = (MpCanvas.fighter_x[n3] - 2)
        MpCanvas.fighter_fx_frame[MpCanvas.loop_i] = (-1)
        self.draw_fighter(MpCanvas.screen_g, MpCanvas.loop_i)

    def draw_fighter_dying(self):  # g.java:3828
        MpCanvas.anim_id = (27 if (MpCanvas.fighter_kind[MpCanvas.loop_i] == 2) else 6)
        MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.anim_first_frame[MpCanvas.anim_id] + MpCanvas.anim_frame)
        MpCanvas.fighter_fx_frame[MpCanvas.loop_i] = (-1)
        self.draw_fighter(MpCanvas.screen_g, MpCanvas.loop_i)

    def draw_fighter_run(self):  # g.java:3835
        MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.anim_first_frame[23] if (MpCanvas.fighter_kind[MpCanvas.loop_i] == 2) else Consts.anim_first_frame[2])
        n2 = MpCanvas.loop_i
        MpCanvas.fighter_x[n2] = (MpCanvas.fighter_x[n2] + MpCanvas.run_dx)
        n3 = MpCanvas.loop_i
        MpCanvas.fighter_y[n3] = (MpCanvas.fighter_y[n3] + MpCanvas.run_dy)
        MpCanvas.fighter_fx_frame[MpCanvas.loop_i] = (-1)
        self.draw_fighter(MpCanvas.screen_g, MpCanvas.loop_i)

    def draw_fighter_anim(self):  # g.java:3845
        MpCanvas.anim_id = MpCanvas.fighter_anim[MpCanvas.loop_i]
        if (MpCanvas.fighter_kind[MpCanvas.loop_i] == 2) and (MpCanvas.anim_id == 3):
            MpCanvas.anim_id = 24
        if (MpCanvas.anim_id == 12) and (MpCanvas.anim_frame >= 4):
            MpCanvas.saved_anim_frame = MpCanvas.anim_frame
            MpCanvas.anim_frame = 4
        MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.anim_first_frame[MpCanvas.anim_id] + MpCanvas.anim_frame)
        MpCanvas.tmp = Consts.anim_steps[MpCanvas.anim_id][((3 * MpCanvas.anim_frame) + 1)]
        n2 = MpCanvas.loop_i
        MpCanvas.fighter_x[n2] = (MpCanvas.fighter_x[n2] + ((((-1) if (((MpCanvas.tmp & 0x80)) > 0) else 1)) * ((MpCanvas.tmp & 0x7F))))
        MpCanvas.tmp = Consts.anim_steps[MpCanvas.anim_id][((3 * MpCanvas.anim_frame) + 2)]
        n3 = MpCanvas.loop_i
        MpCanvas.fighter_y[n3] = (MpCanvas.fighter_y[n3] + ((((-1) if (((MpCanvas.tmp & 0x80)) > 0) else 1)) * ((MpCanvas.tmp & 0x7F))))
        self.draw_fighter(MpCanvas.screen_g, MpCanvas.loop_i)
        if (MpCanvas.anim_id == 12) and (MpCanvas.anim_frame >= 4):
            MpCanvas.anim_frame = MpCanvas.saved_anim_frame

    def draw_fighter_idle(self, graphics):  # g.java:3867
        if MpCanvas.fighter_hp[MpCanvas.loop_i] > 0:
            if ((((MpCanvas.state == 104) or (MpCanvas.state == 105))) and (MpCanvas.fighter_kind[MpCanvas.loop_i] != 2)) and (MpCanvas.battle_won == 1):
                if MpCanvas.state_ticks < 3:
                    MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.anim_first_frame[MpCanvas.anim_id] + MpCanvas.state_ticks)
                    n2 = MpCanvas.loop_i
                    MpCanvas.fighter_x[n2] = (MpCanvas.fighter_x[n2] + ((((-1) if (((MpCanvas.tmp & 0x80)) > 0) else 1)) * ((MpCanvas.tmp & 0x7F))))
                    n3 = MpCanvas.loop_i
                    MpCanvas.fighter_y[n3] = (MpCanvas.fighter_y[n3] + ((((-1) if (((MpCanvas.tmp & 0x80)) > 0) else 1)) * ((MpCanvas.tmp & 0x7F))))
            else:
                if imod(MpCanvas.state_ticks, 4) == MpCanvas.fighter_blink[MpCanvas.loop_i]:
                    MpCanvas.fighter_frame[MpCanvas.loop_i] = imod(idiv(MpCanvas.state_ticks, 4), 2)
                if (MpCanvas.fighter_frame[MpCanvas.loop_i] != 0) and (MpCanvas.fighter_frame[MpCanvas.loop_i] != 1):
                    MpCanvas.fighter_frame[MpCanvas.loop_i] = 0
        else:
            MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.anim_first_frame[6] + 1)
        MpCanvas.fighter_fx_frame[MpCanvas.loop_i] = (-1)
        if ((MpCanvas.fighter_anim[MpCanvas.attacker] == 12) and (MpCanvas.loop_i == MpCanvas.target)) and (MpCanvas.anim_frame >= 4):
            MpCanvas.fighter_fx_frame[MpCanvas.loop_i] = ((10 + MpCanvas.anim_frame) - 4)
        self.draw_fighter(graphics, MpCanvas.loop_i)

    def draw_quotes(self, graphics, n2):  # g.java:3895
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            try:
                try:
                    if not MpCanvas.fighter_present[MpCanvas.loop_i]:
                        raise _Brk_block4_3348()
                    if imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == n2:
                        raise _Brk_block5_3348()
                    if n2 != 2:
                        raise _Brk_block4_3348()
                    bl = ((imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == MpCanvas.fighter_slot[0]) if (MpCanvas.battle_won == 1) else (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) != MpCanvas.fighter_slot[0]))
                    if not bl:
                        raise _Brk_block4_3348()
                except _Brk_block5_3348:
                    pass
                self.draw_box(graphics, (0 if (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (MpCanvas.canvas_w - 60)), (12 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_h - 12) - 15)), 60, 15, 1)
                self.draw_text_centred((30 if (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (MpCanvas.canvas_w - 30)), (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), MpCanvas.fighter_name[MpCanvas.loop_i], 16400640)
                MpCanvas.box_x = MpCanvas.center_x
                MpCanvas.box_y = (38 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) - 11))
                self.draw_box(graphics, MpCanvas.box_x, MpCanvas.box_y, MpCanvas.canvas_w, 22, 0)
                self.draw_text_centred(MpCanvas.box_x, (MpCanvas.box_y - 5), (MpCanvas.fighter_quote_win[MpCanvas.loop_i] if (n2 == 2) else MpCanvas.fighter_quote_start[MpCanvas.loop_i]), 0xFFFFFF)
            except _Brk_block4_3348:
                pass
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_fighter_record(self):  # g.java:3917
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 78, 86, 0)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 34), MpCanvas.fighter_name[MpCanvas.cur_slot], 0xFFFFFF)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 20), _js(_js(Consts.texts[27], "."), MpCanvas.fighter_level[MpCanvas.cur_slot]), 0xFFFFFF)
        self.draw_number0_on(MpCanvas.screen_g, (MpCanvas.center_x + 22), (MpCanvas.center_y + 12), MpCanvas.fighter_wins[MpCanvas.cur_slot])
        self.draw_text_left_on(MpCanvas.screen_g, (MpCanvas.center_x - 27), (MpCanvas.center_y + 11), Consts.texts[49], 0xFFFFFF)
        self.draw_number0_on(MpCanvas.screen_g, (MpCanvas.center_x + 22), (MpCanvas.center_y + 24), MpCanvas.fighter_losses[MpCanvas.cur_slot])
        self.draw_text_left_on(MpCanvas.screen_g, (MpCanvas.center_x - 27), (MpCanvas.center_y + 23), Consts.texts[50], 0xFFFFFF)

    def draw_fighters(self, graphics):  # g.java:3927
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                self.draw_fighter_idle(graphics)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_target_marker(self, graphics):  # g.java:3937
        if imod(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2) == 0:
            self.draw_text_centred_on(graphics, 30, (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), (MpCanvas.fighter_name[MpCanvas.target_cursor] if ((len(MpCanvas.fighter_alt_name[MpCanvas.target_cursor]) == 0) or (imod(MpCanvas.round_no, 2) == 0)) else MpCanvas.fighter_alt_name[MpCanvas.target_cursor]), 16400640)
            if imod(MpCanvas.state_ticks, 2) == 0:
                MpCanvas.draw_left_half_h(graphics, Consts.ui_dx[48], (((19 if (idiv(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2) == 0) else (MpCanvas.canvas_h - 19))) + Consts.ui_dy[48]), 12, MpCanvas.ui_images[48])
                return
            MpCanvas.draw_left_half_row(graphics, (Consts.ui_dx[48] + 1), (((19 if (idiv(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2) == 0) else (MpCanvas.canvas_h - 19))) + Consts.ui_dy[48]), MpCanvas.ui_images[48], 12, 1)
            return
        self.draw_text_centred_on(graphics, (MpCanvas.canvas_w - 30), (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), (MpCanvas.fighter_name[MpCanvas.target_cursor] if ((len(MpCanvas.fighter_alt_name[MpCanvas.target_cursor]) == 0) or (imod(MpCanvas.round_no, 2) == 0)) else MpCanvas.fighter_alt_name[MpCanvas.target_cursor]), 16400640)
        if imod(MpCanvas.state_ticks, 2) == 0:
            MpCanvas.draw_right_half_h(graphics, (MpCanvas.canvas_w - ((1 + Consts.ui_dx[48]))), (((19 if (idiv(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2) == 0) else (MpCanvas.canvas_h - 19))) + Consts.ui_dy[48]), 12, MpCanvas.ui_images[48])
            return
        MpCanvas.draw_right_half_row1(graphics, (MpCanvas.canvas_w - ((2 + Consts.ui_dx[48]))), (((19 if (idiv(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2) == 0) else (MpCanvas.canvas_h - 19))) + Consts.ui_dy[48]), 12, MpCanvas.ui_images[48])

    def draw_stage_intro(self):  # g.java:3955
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 102, 86, 0)
        self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 30), MpCanvas.stage_title, 0xFFFFFF)
        self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 15), _js(_js(_js(Consts.texts[26], MpCanvas.stage), "/"), MpCanvas.stage_count), 0xFFFFFF)
        MpCanvas.loop_i = 1
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                if MpCanvas.fighter_slot[MpCanvas.loop_i] == 1:
                    self.draw_text_centred((MpCanvas.center_x - 24), (MpCanvas.center_y + 4), MpCanvas.fighter_name[MpCanvas.loop_i], 0xFFFFFF)
                    self.draw_text_left((MpCanvas.center_x + 4), (MpCanvas.center_y + 4), _js(_js(Consts.texts[27], ""), MpCanvas.fighter_level[MpCanvas.loop_i]), 0xFFFFFF)
                elif MpCanvas.fighter_slot[MpCanvas.loop_i] == 3:
                    self.draw_text_centred((MpCanvas.center_x - 24), (MpCanvas.center_y + 20), MpCanvas.fighter_name[MpCanvas.loop_i], 0xFFFFFF)
                    self.draw_text_left((MpCanvas.center_x + 4), (MpCanvas.center_y + 20), _js(_js(Consts.texts[27], ""), MpCanvas.fighter_level[MpCanvas.loop_i]), 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    @staticmethod
    def start_timing_bar():  # g.java:3974
        MpCanvas.tmp = imod(abs(MpCanvas.rng.nextInt()), 3)
        _sw86 = MpCanvas.tmp
        if _sw86 == 0:
            MpCanvas.bar_speed = 4
        elif _sw86 == 1:
            MpCanvas.bar_speed = 8
        else:
            MpCanvas.bar_speed = 5
        MpCanvas.set_timer(1)
        MpCanvas.bar_x = (MpCanvas.center_x - 44)
        MpCanvas.bar_shown = True

    def draw_timing_bar(self, graphics):  # g.java:3994
        if MpCanvas.bar_shown:
            n2 = MpCanvas.center_y
            if MpCanvas.room_mode == 0:
                n2 = (MpCanvas.screen_h - 26)
            self.draw_box(graphics, MpCanvas.center_x, (n2 + 3), 110, 38, 0)
            Draw.draw_image(graphics, MpCanvas.ui_images[35], ((MpCanvas.center_x - 44) + Consts.ui_dx[35]), (n2 + Consts.ui_dy[35]), 0)
            Draw.draw_image(graphics, MpCanvas.ui_images[36], ((MpCanvas.center_x - 44) + Consts.ui_dx[36]), (n2 + Consts.ui_dy[36]), 0)
            Draw.draw_image(graphics, MpCanvas.ui_images[37], ((MpCanvas.center_x - 44) + Consts.ui_dx[37]), (n2 + Consts.ui_dy[37]), 0)

    def draw_timing_cursor(self, graphics):  # g.java:4007
        n2 = MpCanvas.center_y
        if MpCanvas.room_mode == 0:
            n2 = (MpCanvas.screen_h - 26)
        if MpCanvas.state == 98:
            if MpCanvas.hit_score == 100:
                Draw.draw_image(graphics, MpCanvas.ui_images[52], (((MpCanvas.center_x - 44) + 72) + Consts.ui_dx[52]), (n2 + Consts.ui_dy[52]), 0)
                self.start_sound(0)
            elif MpCanvas.hit_score == 20:
                Draw.draw_image(graphics, MpCanvas.ui_images[53], (((MpCanvas.center_x - 44) + 72) + Consts.ui_dx[53]), (n2 + Consts.ui_dy[53]), 0)
            else:
                Draw.draw_image(graphics, MpCanvas.ui_images[49], ((MpCanvas.bar_x - 20) + Consts.ui_dx2[35]), ((n2 - 11) + Consts.ui_dy2[35]), 0)
                self.start_sound(0)
        if imod(MpCanvas.state_ticks, 2) == 0:
            Draw.draw_image(graphics, MpCanvas.ui_images[38], (((MpCanvas.center_x - 44) + 72) + Consts.ui_dx[38]), (n2 + Consts.ui_dy[38]), 0)
        Draw.draw_image(graphics, MpCanvas.ui_images[34], (MpCanvas.bar_x + Consts.ui_dx[34]), (n2 + Consts.ui_dy[34]), 0)
        if (MpCanvas.state == 97) and (MpCanvas.bar_x > ((MpCanvas.center_x - 44) + 72)):
            self.stop_timing()

    def start_timing(self):  # g.java:4032
        MpCanvas.timer_ticks = 0
        MpCanvas.set_state(97)

    def stop_timing(self):  # g.java:4037
        MpCanvas.timer_ticks = 0
        if MpCanvas.chosen_action > 2:
            MpCanvas.hit_score = 0
        else:
            if (((MpCanvas.bar_speed == 6) or (MpCanvas.bar_speed == 7))) and (abs((((MpCanvas.center_x - 44) + 72) - MpCanvas.bar_x)) <= idiv(MpCanvas.bar_speed, 2)):
                MpCanvas.bar_x = ((MpCanvas.center_x - 44) + 72)
            MpCanvas.hit_score = ((((20 + MpCanvas.bar_x) - MpCanvas.center_x) + 44) if (MpCanvas.bar_x < ((MpCanvas.center_x - 44) + 72)) else ((100 if (MpCanvas.bar_x == ((MpCanvas.center_x - 44) + 72)) else 20)))
        MpCanvas.set_state(98)

    @staticmethod
    def draw_sprite_frame(graphics, imageArray, aArray, n2):  # g.java:4050
        a2 = aArray[0]
        n3 = 0
        if n2 >= 400:
            n3 = (n2 - 400)
        elif n2 >= 300:
            n3 = (n2 - 300)
        elif n2 >= 200:
            n3 = (n2 - 200)
            a2 = aArray[2]
        elif n2 >= 100:
            n3 = (n2 - 100)
            a2 = aArray[1]
        else:
            n3 = n2
        if MpCanvas.draw_mirrored:
            Draw.draw_image_part(graphics, imageArray[1], (MpCanvas.canvas_w - (((MpCanvas.draw_x - a2.anchor_x[n3]) + a2.w[n3]))), (MpCanvas.draw_y - a2.anchor_y[n3]), a2.w[n3], a2.h[n3], a2.src_x[n3], a2.src_y[n3])
            return
        Draw.draw_image_part(graphics, imageArray[0], (MpCanvas.draw_x - a2.anchor_x[n3]), (MpCanvas.draw_y - a2.anchor_y[n3]), a2.w[n3], a2.h[n3], a2.src_x[n3], a2.src_y[n3])

    def draw_fighter(self, graphics, n2):  # g.java:4073
        n3 = 0
        MpCanvas.draw_mirrored = (imod(MpCanvas.fighter_slot[n2], 2) != 0)
        MpCanvas.draw_x = MpCanvas.fighter_x[n2]
        MpCanvas.draw_y = MpCanvas.fighter_y[n2]
        self.draw_fighter_effects(n2, True)
        if MpCanvas.fighter_kind[n2] != 2:
            self.load_sprite(MpCanvas.shadow_images, MpCanvas.shadow_frames, "sprshadow")
            MpCanvas.draw_sprite_frame(graphics, MpCanvas.shadow_images, MpCanvas.shadow_frames, MpCanvas.fighter_frame[n2])
        bl = False
        if MpCanvas.fighter_kind[n2] == 2:
            bl = Consts.mon_weapon_behind[imod(MpCanvas.fighter_frame[n2], 100)]
            if bl:
                self.load_sprite_dir(MpCanvas.mon_weapon_images, MpCanvas.mon_weapon_frames, "spr_wp_mon", 0)
                MpCanvas.draw_sprite_frame(graphics, MpCanvas.mon_weapon_images, MpCanvas.mon_weapon_frames, MpCanvas.fighter_frame[n2])
        else:
            n3 = idiv(MpCanvas.fighter_frame[n2], 100)
            if MpCanvas.fighter_weapon[n2] == 0:
                if n3 == 2:
                    bl = Consts.bare_weapon_behind_pose2[imod(MpCanvas.fighter_frame[n2], 100)]
            else:
                bl = (Consts.weapon_behind_pose1[imod(MpCanvas.fighter_frame[n2], 100)] if (n3 == 1) else ((Consts.weapon_behind_pose2[imod(MpCanvas.fighter_frame[n2], 100)] if (n3 == 2) else Consts.weapon_behind_pose0[imod(MpCanvas.fighter_frame[n2], 100)])))
            if bl:
                self.load_sprite(MpCanvas.weapon_images[MpCanvas.fighter_weapon[n2]], MpCanvas.weapon_frames[MpCanvas.fighter_weapon[n2]], _js("sprwp", ((MpCanvas.fighter_weapon[n2] + 1))))
                MpCanvas.draw_sprite_frame(graphics, MpCanvas.weapon_images[MpCanvas.fighter_weapon[n2]], MpCanvas.weapon_frames[MpCanvas.fighter_weapon[n2]], MpCanvas.fighter_frame[n2])
        if MpCanvas.fighter_kind[n2] == 2:
            self.load_sprite_dir(MpCanvas.monster_images, MpCanvas.monster_frames, "spr_mon", 0)
            MpCanvas.draw_sprite_frame(graphics, MpCanvas.monster_images, MpCanvas.monster_frames, MpCanvas.fighter_frame[n2])
        else:
            self.load_sprite(MpCanvas.shadow_images, MpCanvas.shadow_frames, "sprshadow")
            MpCanvas.draw_sprite_frame(graphics, MpCanvas.shadow_images, MpCanvas.shadow_frames, MpCanvas.fighter_frame[n2])
            self.load_sprite(MpCanvas.body_images, MpCanvas.body_frames, "sprbody")
            MpCanvas.draw_sprite_frame(graphics, MpCanvas.body_images, MpCanvas.body_frames, MpCanvas.fighter_frame[n2])
        n3 = 0
        if MpCanvas.fighter_kind[n2] != 2:
            if MpCanvas.fighter_kind[n2] == 0:
                n3 = MpCanvas.fighter_face[n2]
            self.load_sprite(MpCanvas.head_images[n3], MpCanvas.head_frames[n3], _js("sprhead", ((n3 + 1))))
            MpCanvas.draw_sprite_frame(graphics, MpCanvas.head_images[n3], MpCanvas.head_frames[n3], MpCanvas.fighter_frame[n2])
        if MpCanvas.fighter_present[n2] and (MpCanvas.state != 105):
            _sw87 = MpCanvas.fighter_status[n2]
            if _sw87 == 11:
                self.load_status_effect()
                MpCanvas.draw_status_effect(graphics, 0)
            elif _sw87 == 12:
                self.load_status_effect()
                MpCanvas.draw_status_effect(graphics, 1)
            elif _sw87 == 13:
                self.load_status_effect()
                MpCanvas.draw_status_effect(graphics, 2)
        if not bl:
            if MpCanvas.fighter_kind[n2] == 2:
                self.load_sprite_dir(MpCanvas.mon_weapon_images, MpCanvas.mon_weapon_frames, "spr_wp_mon", 0)
                MpCanvas.draw_sprite_frame(graphics, MpCanvas.mon_weapon_images, MpCanvas.mon_weapon_frames, MpCanvas.fighter_frame[n2])
            else:
                self.load_sprite(MpCanvas.weapon_images[MpCanvas.fighter_weapon[n2]], MpCanvas.weapon_frames[MpCanvas.fighter_weapon[n2]], _js("sprwp", ((MpCanvas.fighter_weapon[n2] + 1))))
                MpCanvas.draw_sprite_frame(graphics, MpCanvas.weapon_images[MpCanvas.fighter_weapon[n2]], MpCanvas.weapon_frames[MpCanvas.fighter_weapon[n2]], MpCanvas.fighter_frame[n2])
        self.draw_fighter_effects(n2, False)

    def draw_fighter_effects(self, n2, bl):  # g.java:4151
        if MpCanvas.fighter_kind[n2] == 2:
            if not bl:
                self.load_sprite_dir(MpCanvas.mon_sword_images, MpCanvas.mon_sword_frames, "spr_sword_mon", 0)
                MpCanvas.draw_sprite_frame(MpCanvas.screen_g, MpCanvas.mon_sword_images, MpCanvas.mon_sword_frames, MpCanvas.fighter_frame[n2])
                self.load_sprite_dir(MpCanvas.mon_effect_images, MpCanvas.mon_effect_frames, "spr_eff_mon", 0)
                MpCanvas.draw_sprite_frame(MpCanvas.screen_g, MpCanvas.mon_effect_images, MpCanvas.mon_effect_frames, MpCanvas.fighter_frame[n2])
                return
        else:
            n3 = 0
            bl2 = False
            if not bl:
                self.load_sprite(MpCanvas.sword_images[MpCanvas.fighter_weapon[n2]], MpCanvas.sword_frames[MpCanvas.fighter_weapon[n2]], _js("sprsword", ((MpCanvas.fighter_weapon[n2] + 1))))
                MpCanvas.draw_sprite_frame(MpCanvas.screen_g, MpCanvas.sword_images[MpCanvas.fighter_weapon[n2]], MpCanvas.sword_frames[MpCanvas.fighter_weapon[n2]], MpCanvas.fighter_frame[n2])
                self.load_sprite(MpCanvas.effect_images[0], MpCanvas.effect_frames[0], "spreff1")
                MpCanvas.draw_sprite_frame(MpCanvas.screen_g, MpCanvas.effect_images[0], MpCanvas.effect_frames[0], MpCanvas.fighter_frame[n2])
            if bl == ((bl2 := (Consts.eff2_behind_pose1[imod(MpCanvas.fighter_frame[n2], 100)] if (((n3 := idiv(MpCanvas.fighter_frame[n2], 100))) == 1) else ((Consts.eff2_behind_pose2[imod(MpCanvas.fighter_frame[n2], 100)] if (n3 == 2) else False))))):
                self.load_sprite(MpCanvas.effect_images[1], MpCanvas.effect_frames[1], "spreff2")
                MpCanvas.draw_sprite_frame(MpCanvas.screen_g, MpCanvas.effect_images[1], MpCanvas.effect_frames[1], MpCanvas.fighter_frame[n2])

    def step_turn_anim(self):  # g.java:4176
        if MpCanvas.damage_tick >= 5:
            MpCanvas.damage_tick = (-1)
            MpCanvas.loop_i = 0
            while MpCanvas.loop_i < 4:
                if MpCanvas.fighter_present[MpCanvas.loop_i] and ((((MpCanvas.loop_i == MpCanvas.attacker) or (MpCanvas.loop_i == MpCanvas.target)) or (MpCanvas.loop_i == MpCanvas.target2))):
                    if MpCanvas.fighter_hp[MpCanvas.loop_i] != MpCanvas.fighter_hp_target[MpCanvas.loop_i]:
                        MpCanvas.fighter_hp[MpCanvas.loop_i] = MpCanvas.fighter_hp_target[MpCanvas.loop_i]
                    if MpCanvas.fighter_mp[MpCanvas.loop_i] != MpCanvas.fighter_mp_target[MpCanvas.loop_i]:
                        MpCanvas.fighter_mp[MpCanvas.loop_i] = MpCanvas.fighter_mp_target[MpCanvas.loop_i]
                MpCanvas.loop_i = MpCanvas.loop_i + 1
        if MpCanvas.anim_frame >= MpCanvas.anim_length:
            MpCanvas.anim_frame = 0
            _sw88 = MpCanvas.fighter_anim[MpCanvas.attacker]
            _m89 = False
            while True:
                if _m89 or _sw88 in (2, 17, 18, 19):
                    _m89 = True
                    MpCanvas.fighter_x[MpCanvas.attacker] = (MpCanvas.canvas_w - 67)
                    MpCanvas.fighter_y[MpCanvas.attacker] = (MpCanvas.center_y + 65)
                    if MpCanvas.room_mode != 0:
                        n2 = MpCanvas.attacker
                        MpCanvas.fighter_y[n2] = (MpCanvas.fighter_y[n2] + ((((-1) if (idiv(MpCanvas.turn_bytes[(12 + MpCanvas.turn_rec)], 2) == 0) else 1)) * 23))
                    _sw90 = MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)]
                    if _sw90 == 3:
                        MpCanvas.fighter_anim[MpCanvas.attacker] = 9
                    elif _sw90 == 4:
                        MpCanvas.fighter_anim[MpCanvas.attacker] = 10
                    elif _sw90 == 5:
                        MpCanvas.fighter_anim[MpCanvas.attacker] = 11
                    elif _sw90 == 6:
                        MpCanvas.fighter_anim[MpCanvas.attacker] = 14
                    elif _sw90 == 7:
                        MpCanvas.fighter_anim[MpCanvas.attacker] = 15
                    elif _sw90 == 0:
                        MpCanvas.fighter_anim[MpCanvas.attacker] = 3
                    break
                if _m89 or _sw88 == 8:
                    _m89 = True
                    _sw91 = MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)]
                    _m92 = False
                    while True:
                        if _m92 or _sw91 in (3, 4, 5):
                            _m92 = True
                            MpCanvas.fighter_anim[MpCanvas.attacker] = 2
                            MpCanvas.run_dx = idiv((((MpCanvas.canvas_w - 67) - 42)), Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]])
                            if MpCanvas.room_mode == 0:
                                MpCanvas.run_dy = 0
                                break
                            if idiv(MpCanvas.fighter_slot[MpCanvas.attacker], 2) == idiv(MpCanvas.turn_bytes[(12 + MpCanvas.turn_rec)], 2):
                                MpCanvas.run_dy = 0
                                break
                            if idiv(MpCanvas.fighter_slot[MpCanvas.attacker], 2) == 0:
                                MpCanvas.run_dy = idiv(46, Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]])
                                break
                            MpCanvas.run_dy = idiv((-46), Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]])
                            break
                        if _m92 or _sw91 in (6, 7):
                            _m92 = True
                            if MpCanvas.room_mode == 0:
                                MpCanvas.fighter_anim[MpCanvas.attacker] = 17
                                break
                            if idiv(MpCanvas.turn_bytes[(12 + MpCanvas.turn_rec)], 2) == idiv(MpCanvas.turn_bytes[(0 + MpCanvas.turn_rec)], 2):
                                MpCanvas.fighter_anim[MpCanvas.attacker] = 17
                                break
                            if idiv(MpCanvas.turn_bytes[(12 + MpCanvas.turn_rec)], 2) == 1:
                                MpCanvas.fighter_anim[MpCanvas.attacker] = 18
                                break
                            MpCanvas.fighter_anim[MpCanvas.attacker] = 19
                            break
                        if _m92 or _sw91 == 8:
                            _m92 = True
                            MpCanvas.fighter_anim[MpCanvas.attacker] = 20
                        break
                    break
                if _m89 or _sw88 == 20:
                    _m89 = True
                    _sw93 = MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)]
                    if _sw93 == 8:
                        MpCanvas.fighter_anim[MpCanvas.attacker] = 16
                    break
                if _m89 or _sw88 in (3, 9, 10, 11, 14, 15, 16):
                    _m89 = True
                    if (MpCanvas.turn_bytes[(28 + MpCanvas.turn_rec)] == 3) and (MpCanvas.fighter_slot[MpCanvas.attacker] == MpCanvas.turn_bytes[(0 + MpCanvas.turn_rec)]):
                        MpCanvas.tmp = MpCanvas.attacker
                        MpCanvas.attacker = MpCanvas.target
                        MpCanvas.target = MpCanvas.tmp
                        MpCanvas.fighter_anim[MpCanvas.attacker] = 3
                        MpCanvas.target_reaction = 1
                        break
                    MpCanvas.damage_tick = 0
                    if MpCanvas.turn_bytes[(28 + MpCanvas.turn_rec)] == 3:
                        MpCanvas.tmp = MpCanvas.attacker
                        MpCanvas.attacker = MpCanvas.target
                        MpCanvas.target = MpCanvas.tmp
                        MpCanvas.fighter_anim[MpCanvas.target] = 0
                        MpCanvas.place_fighter(MpCanvas.target)
                    MpCanvas.fighter_anim[MpCanvas.attacker] = 28
                    MpCanvas.run_dx = idiv(((42 - MpCanvas.fighter_x[MpCanvas.attacker])), Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]])
                    if MpCanvas.room_mode == 0:
                        MpCanvas.run_dy = 0
                        break
                    if idiv(MpCanvas.fighter_slot[MpCanvas.attacker], 2) == idiv(MpCanvas.turn_bytes[(12 + MpCanvas.turn_rec)], 2):
                        MpCanvas.run_dy = 0
                        break
                    if idiv(MpCanvas.fighter_slot[MpCanvas.attacker], 2) == 0:
                        MpCanvas.run_dy = idiv((-46), Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]])
                        break
                    MpCanvas.run_dy = idiv(46, Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]])
                    break
                if _m89 or _sw88 in (12, 13, 28):
                    _m89 = True
                    MpCanvas.place_fighter(MpCanvas.attacker)
                    MpCanvas.tmp = (-1)
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 4:
                        if MpCanvas.fighter_present[MpCanvas.loop_i]:
                            if (MpCanvas.fighter_anim[MpCanvas.attacker] == 13) and (imod(MpCanvas.fighter_slot[MpCanvas.attacker], 2) == imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2)):
                                MpCanvas.fighter_status[MpCanvas.loop_i] = MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)]
                                MpCanvas.fighter_status_ticks[MpCanvas.loop_i] = 3
                            if (MpCanvas.fighter_hp[MpCanvas.loop_i] == 0) and (MpCanvas.fighter_hp_delta[MpCanvas.loop_i] != 0):
                                MpCanvas.tmp = MpCanvas.loop_i
                                MpCanvas.fighter_anim[MpCanvas.tmp] = 6
                                if imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == imod(MpCanvas.fighter_slot[0], 2):
                                    MpCanvas.allies_alive = MpCanvas.allies_alive - 1
                                else:
                                    MpCanvas.enemies_alive = MpCanvas.enemies_alive - 1
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    if MpCanvas.tmp > 0:
                        if MpCanvas.fighter_anim[MpCanvas.attacker] != 6:
                            MpCanvas.fighter_anim[MpCanvas.attacker] = 0
                        MpCanvas.attacker = MpCanvas.tmp
                        break
                    MpCanvas.turn_rec = MpCanvas.turn_rec + 1
                    self.next_turn_record()
                    break
                if _m89 or _sw88 == 6:
                    _m89 = True
                    MpCanvas.turn_rec = MpCanvas.turn_rec + 1
                    self.next_turn_record()
                break
            MpCanvas.anim_length = Consts.anim_length[MpCanvas.fighter_anim[MpCanvas.attacker]]
        if MpCanvas.fighter_anim[MpCanvas.attacker] != 6:
            self.update_reactions()

    def next_turn_record(self):  # g.java:4372
        if MpCanvas.turn_record_count == 0:
            MpCanvas.set_state(100)
            return
        if MpCanvas.turn_rec < MpCanvas.turn_record_count:
            MpCanvas.set_state(101)
            return
        MpCanvas.set_state(93)

    def update_reactions(self):  # g.java:4388
        if ((MpCanvas.fighter_anim[MpCanvas.attacker] != 12) and (MpCanvas.fighter_anim[MpCanvas.attacker] != 13)) and (MpCanvas.turn_bytes[(28 + MpCanvas.turn_rec)] != 3):
            if (MpCanvas.target != (-1)) and (MpCanvas.fighter_anim[MpCanvas.target] != 0):
                n2 = MpCanvas.target
                MpCanvas.fighter_anim_tick[n2] = (MpCanvas.fighter_anim_tick[n2] + 1)
                if MpCanvas.fighter_anim_tick[MpCanvas.target] >= MpCanvas.fighter_anim_len[MpCanvas.target]:
                    MpCanvas.fighter_anim[MpCanvas.target] = 0
                    MpCanvas.place_fighter(MpCanvas.target)
            if (MpCanvas.target2 != (-1)) and (MpCanvas.fighter_anim[MpCanvas.target2] != 0):
                n3 = MpCanvas.target2
                MpCanvas.fighter_anim_tick[n3] = (MpCanvas.fighter_anim_tick[n3] + 1)
                if MpCanvas.fighter_anim_tick[MpCanvas.target2] >= MpCanvas.fighter_anim_len[MpCanvas.target2]:
                    MpCanvas.fighter_anim[MpCanvas.target2] = 0
                    MpCanvas.place_fighter(MpCanvas.target2)
        _sw94 = MpCanvas.fighter_anim[MpCanvas.attacker]
        _m95 = False
        while True:
            if _m95 or _sw94 in (3, 9, 10, 11, 14):
                _m95 = True
                _sw96 = MpCanvas.target_reaction
                _m97 = False
                while True:
                    if _m97 or _sw96 in (1, 4):
                        _m97 = True
                        if (MpCanvas.fighter_anim[MpCanvas.attacker] == 11) and (MpCanvas.anim_frame == 17):
                            self.start_reaction()
                            MpCanvas.fighter_anim_len[MpCanvas.target] = 3
                            return
                        if imod(MpCanvas.anim_frame, 2) != 1:
                            return
                        if (MpCanvas.fighter_anim[MpCanvas.attacker] == 11) and (MpCanvas.anim_frame > 10):
                            return
                        self.start_reaction()
                        MpCanvas.fighter_anim_len[MpCanvas.target] = 2
                        return
                    if _m97 or _sw96 == 5:
                        _m97 = True
                        if MpCanvas.turn_bytes[(28 + MpCanvas.turn_rec)] == 3:
                            if MpCanvas.anim_frame != 0:
                                return
                            MpCanvas.fighter_anim[MpCanvas.target] = 5
                            MpCanvas.fighter_anim_tick[MpCanvas.target] = 0
                            MpCanvas.fighter_anim_len[MpCanvas.target] = MpCanvas.anim_length
                            return
                        else:
                            if imod(MpCanvas.anim_frame, 2) != 1:
                                return
                            self.start_reaction()
                            MpCanvas.fighter_anim_len[MpCanvas.target] = 2
                    if _m97 or _sw96 not in (1, 4, 5):
                        _m97 = True
                        return
                    break
            if _m95 or _sw94 == 15:
                _m95 = True
                _sw98 = MpCanvas.target_reaction
                if _sw98 in (1, 4):
                    if MpCanvas.anim_frame != 2:
                        return
                    self.start_reaction()
                    MpCanvas.fighter_anim_len[MpCanvas.target] = 4
                return
            if _m95 or _sw94 == 16:
                _m95 = True
                _sw99 = MpCanvas.target_reaction
                if _sw99 in (1, 4):
                    if MpCanvas.anim_frame != 8:
                        return
                    self.start_reaction()
                    MpCanvas.fighter_anim_len[MpCanvas.target] = 3
                    if MpCanvas.target2 == (-1):
                        return
                    MpCanvas.fighter_anim[MpCanvas.target2] = MpCanvas.target2_reaction
                    MpCanvas.fighter_anim_tick[MpCanvas.target2] = 0
                    MpCanvas.fighter_anim_len[MpCanvas.target2] = 3
                return
            if _m95 or _sw94 == 12:
                _m95 = True
                if MpCanvas.anim_frame != 4:
                    return
                MpCanvas.damage_tick = 0
                self.start_sound(6)
                if MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] == 2:
                    return
                return
            if _m95 or _sw94 == 13:
                _m95 = True
                if (MpCanvas.anim_frame == 4) and (MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)] == 13):
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 4:
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    self.start_sound(5)
                    return
                if MpCanvas.anim_frame == 7:
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 4:
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    self.start_sound(5)
                    return
                if MpCanvas.anim_frame != 5:
                    return
                MpCanvas.damage_tick = 0
            break

    def start_reaction(self):  # g.java:4501
        MpCanvas.fighter_anim[MpCanvas.target] = MpCanvas.target_reaction
        MpCanvas.fighter_anim_tick[MpCanvas.target] = 0
        if (MpCanvas.fighter_anim[MpCanvas.attacker] == 16) or (MpCanvas.fighter_anim[MpCanvas.attacker] == 15):
            self.start_sound(2)
            return
        self.start_sound(0)

    def draw_stage_complete(self):  # g.java:4511
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 88, 72, 0)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 20), MpCanvas.stage_title, 0xFFFFFF)
        MpCanvas.stage_text = _js(_js(Consts.texts[26], " "), MpCanvas.stage)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 4), MpCanvas.stage_text, 0xFFFFFF)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y + 12), Consts.texts[28], 0xFFFFFF)

    def draw_damage(self):  # g.java:4519
        if MpCanvas.damage_tick < 0:
            return
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i] and ((((MpCanvas.loop_i == MpCanvas.attacker) or (MpCanvas.loop_i == MpCanvas.target)) or (MpCanvas.loop_i == MpCanvas.target2))):
                if MpCanvas.fighter_hp[MpCanvas.loop_i] != MpCanvas.fighter_hp_target[MpCanvas.loop_i]:
                    n2 = MpCanvas.loop_i
                    MpCanvas.fighter_hp[n2] = (MpCanvas.fighter_hp[n2] + MpCanvas.fighter_hp_step[MpCanvas.loop_i])
                    if MpCanvas.fighter_hp[MpCanvas.loop_i] < 0:
                        MpCanvas.fighter_hp[MpCanvas.loop_i] = 0
                if MpCanvas.fighter_mp[MpCanvas.loop_i] != MpCanvas.fighter_mp_target[MpCanvas.loop_i]:
                    n3 = MpCanvas.loop_i
                    MpCanvas.fighter_mp[n3] = (MpCanvas.fighter_mp[n3] + MpCanvas.fighter_mp_step[MpCanvas.loop_i])
                    if MpCanvas.fighter_mp[MpCanvas.loop_i] < 0:
                        MpCanvas.fighter_mp[MpCanvas.loop_i] = 0
                if MpCanvas.fighter_hp_delta[MpCanvas.loop_i] != 0:
                    bl = _set(MpCanvas, 'draw_mirrored', (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) != 0))
                    if not MpCanvas.draw_mirrored:
                        self.draw_damage_number(MpCanvas.screen_g, MpCanvas.fighter_x[MpCanvas.loop_i], ((MpCanvas.fighter_y[MpCanvas.loop_i] - 40) - (2 * MpCanvas.damage_tick)), MpCanvas.fighter_hp_delta[MpCanvas.loop_i])
                    else:
                        self.draw_damage_number(MpCanvas.screen_g, (MpCanvas.canvas_w - MpCanvas.fighter_x[MpCanvas.loop_i]), ((MpCanvas.fighter_y[MpCanvas.loop_i] - 40) - (2 * MpCanvas.damage_tick)), MpCanvas.fighter_hp_delta[MpCanvas.loop_i])
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.draw_hp_bars(MpCanvas.screen_g)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if (MpCanvas.fighter_present[MpCanvas.loop_i] and ((((MpCanvas.loop_i == MpCanvas.attacker) or (MpCanvas.loop_i == MpCanvas.target)) or (MpCanvas.loop_i == MpCanvas.target2)))) and (MpCanvas.fighter_hp[MpCanvas.loop_i] == 0):
                MpCanvas.fighter_hp[MpCanvas.loop_i] = 1
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.damage_tick = MpCanvas.damage_tick + 1

    @staticmethod
    def draw_hp_bars(graphics):  # g.java:4562
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                n2 = 0
                n3 = idiv((MpCanvas.fighter_hp[MpCanvas.loop_i] * MpCanvas.hp_bar_w), MpCanvas.fighter_max_hp[MpCanvas.loop_i])
                if (n3 == 0) and (MpCanvas.fighter_hp[MpCanvas.loop_i] > 0):
                    n3 = 1
                n4 = (28 if (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_w - 28) - MpCanvas.hp_bar_w))
                n5 = (0 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_h - 3) - 6))
                n3 = n3 - 1
                if MpCanvas.fighter_hp[MpCanvas.loop_i] > 0:
                    if imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0:
                        Draw.draw_hline(graphics, n4, n5, n3, 0xB50000)
                        Draw.draw_hline(graphics, n4, (n5 + 1), n3, 0xFF0000)
                        Draw.draw_hline(graphics, n4, (n5 + 2), n3, 0xB50000)
                    else:
                        n2 = (MpCanvas.hp_bar_w - n3)
                        Draw.draw_hline(graphics, (n4 + n2), n5, n3, 0xB50000)
                        Draw.draw_hline(graphics, (n4 + n2), (n5 + 1), n3, 0xFF0000)
                        Draw.draw_hline(graphics, (n4 + n2), (n5 + 2), n3, 0xB50000)
                if (((n3 := idiv((MpCanvas.fighter_mp[MpCanvas.loop_i] * MpCanvas.hp_bar_w), 100))) == 0) and (MpCanvas.fighter_mp[MpCanvas.loop_i] > 0):
                    n3 = 1
                n4 = (28 if (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_w - 28) - MpCanvas.hp_bar_w))
                n5 = (6 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (MpCanvas.canvas_h - 3))
                n3 = n3 - 1
                if MpCanvas.fighter_mp[MpCanvas.loop_i] > 0:
                    if imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0:
                        Draw.draw_hline(graphics, n4, n5, n3, 3223675)
                        Draw.draw_hline(graphics, n4, (n5 + 1), n3, 9216734)
                        Draw.draw_hline(graphics, n4, (n5 + 2), n3, 3223675)
                    else:
                        n2 = (MpCanvas.hp_bar_w - n3)
                        Draw.draw_hline(graphics, (n4 + n2), n5, n3, 3223675)
                        Draw.draw_hline(graphics, (n4 + n2), (n5 + 1), n3, 9216734)
                        Draw.draw_hline(graphics, (n4 + n2), (n5 + 2), n3, 3223675)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    @staticmethod
    def clear_fighters():  # g.java:4609
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            MpCanvas.fighter_present[MpCanvas.loop_i] = False
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.allies_alive = 0
        MpCanvas.enemies_alive = 0

    def draw_number1_on(self, graphics, n2, n3, n4):  # g.java:4619
        MpCanvas.draw_number(graphics, n2, n3, n4, 1)

    def draw_number2_on(self, graphics, n2, n3, n4):  # g.java:4623
        MpCanvas.draw_number(graphics, n2, n3, n4, 2)

    def draw_number3_on(self, graphics, n2, n3, n4):  # g.java:4627
        MpCanvas.draw_number(graphics, n2, n3, n4, 3)

    def draw_damage_number(self, graphics, n2, n3, n4):  # g.java:4631
        MpCanvas.draw_number(graphics, n2, n3, n4, 4)

    def draw_number5(self, n2, n3, n4):  # g.java:4635
        MpCanvas.draw_number(MpCanvas.screen_g, n2, n3, n4, 5)

    def draw_number0_on(self, graphics, n2, n3, n4):  # g.java:4639
        MpCanvas.draw_number(graphics, n2, n3, n4, 0)

    def draw_number0(self, n2, n3, n4):  # g.java:4643
        MpCanvas.draw_number(MpCanvas.screen_g, n2, n3, n4, 0)

    def draw_number1(self, n2, n3, n4):  # g.java:4647
        MpCanvas.draw_number(MpCanvas.screen_g, n2, n3, n4, 1)

    def draw_number0_b(self, n2, n3, n4):  # g.java:4651
        MpCanvas.draw_number(MpCanvas.screen_g, n2, n3, n4, 0)

    def draw_number1_b(self, n2, n3, n4):  # g.java:4655
        MpCanvas.draw_number(MpCanvas.screen_g, n2, n3, n4, 1)

    @staticmethod
    def draw_number(graphics, n2, n3, n4, n5):  # g.java:4659
        n6 = 1
        n7 = 0
        _sw100 = n5
        if _sw100 in (0, 1, 7):
            while (idiv(n4, n6) > 0) or (n6 == 1):
                n8 = idiv(imod(n4, ((n6 * 10))), n6)
                Draw.draw_image_part(graphics, MpCanvas.number_images[n5], n2, n3, 5, 8, (n8 * 5), 0)
                n2 = (n2 - 6)
                n6 = (n6 * 10)
                if (imod((n7 := i32(n7 + 1)), 3) != 0) or (idiv(n4, n6) <= 0):
                    continue
                Draw.draw_image_part(graphics, MpCanvas.number_images[n5], (n2 := (n2 + 2)), (n3 + 5), 2, 3, 50, 5)
                n2 = (n2 - 6)
            return
        elif _sw100 == 5:
            Draw.draw_image_part(graphics, MpCanvas.number_images[6], (n2 - 3), (n3 - 1), 3, 10, 7, 0)
            n2 = (n2 - 9)
            while (idiv(n4, n6) > 0) or (n6 == 1):
                n9 = idiv(imod(n4, ((n6 * 10))), n6)
                Draw.draw_image_part(graphics, MpCanvas.number_images[n5], n2, n3, 5, 8, (n9 * 5), 16)
                n2 = (n2 - 6)
                n6 = (n6 * 10)
                if (imod((n7 := i32(n7 + 1)), 3) != 0) or (idiv(n4, n6) <= 0):
                    continue
                Draw.fill_rect(graphics, (n2 := (n2 + 2)), (n3 + 6), 1, 3, 65280)
                n2 = (n2 - 6)
            Draw.draw_image_part(graphics, MpCanvas.number_images[6], (n2 - 2), (n3 - 1), 7, 10, 0, 0)
            return
        elif _sw100 == 2:
            while (idiv(n4, n6) > 0) or (n6 == 1):
                n10 = idiv(imod(n4, ((n6 * 10))), n6)
                Draw.draw_image_part(graphics, MpCanvas.number_images[n5], n2, n3, 7, 11, (n10 * 7), 0)
                n2 = (n2 - 8)
                n6 = (n6 * 10)
            return
        elif _sw100 == 3:
            while (idiv(n4, n6) > 0) or (n6 == 1):
                n11 = idiv(imod(n4, ((n6 * 10))), n6)
                Draw.draw_image_part(graphics, MpCanvas.number_images[n5], n2, n3, 12, 13, (n11 * 12), 0)
                n2 = (n2 - 12)
                n6 = (n6 * 10)
            return
        elif _sw100 == 4:
            if n4 < 0:
                n4 = (-n4)
                MpCanvas.number_negative = True
            else:
                MpCanvas.number_negative = False
            while (idiv(n4, n6) > 0) or (n6 == 1):
                n12 = idiv(imod(n4, ((n6 * 10))), n6)
                Draw.draw_image_part(graphics, MpCanvas.number_images[n5], n2, n3, 6, 10, (n12 * 6), (10 if MpCanvas.number_negative else 0))
                n2 = (n2 - 7)
                n6 = (n6 * 10)

    @staticmethod
    def place_fighter(n2):  # g.java:4726
        MpCanvas.fighter_x[n2] = 42
        MpCanvas.fighter_y[n2] = (MpCanvas.center_y + 65)
        if MpCanvas.room_mode != 0:
            n3 = n2
            MpCanvas.fighter_y[n3] = (MpCanvas.fighter_y[n3] + ((((-1) if (idiv(MpCanvas.fighter_slot[n2], 2) == 0) else 1)) * 23))

    @staticmethod
    def set_state(n2):  # g.java:4735
        MpCanvas.state = n2
        MpCanvas.state_ticks = 0

    @staticmethod
    def save_options():  # g.java:4740
        byArray = [0] * (28)
        n2 = 0
        while n2 < len(byArray):
            byArray[n2] = 0
            n2 = n2 + 1
        byArray[0] = i8(MpCanvas.speed)
        byArray[1] = i8(MpCanvas.volume)
        byArray2 = bytearray(MpCanvas.user_id.encode('latin-1', 'replace'))
        n2 = 0
        while n2 < len(byArray2):
            byArray[(2 + n2)] = byArray2[n2]
            n2 = n2 + 1
        byArray2 = bytearray(MpCanvas.password.encode('latin-1', 'replace'))
        n2 = 0
        while n2 < len(byArray2):
            byArray[(14 + n2)] = byArray2[n2]
            n2 = n2 + 1
        try:
            recordStore = RecordStore.openRecordStore("pow_mp_save", True)
            if recordStore.getNumRecords() == 0:
                recordStore.addRecord(byArray, 0, len(byArray))
            recordStore.setRecord(1, byArray, 0, len(byArray))
            return
        except Exception:
            return

    def load_options(self):  # g.java:4774
        byArray = [0] * (28)
        MpCanvas.speed = 0
        MpCanvas.volume = 4
        MpCanvas.user_id = ""
        MpCanvas.password = ""
        try:
            recordStore = RecordStore.openRecordStore("pow_mp_save", False)
            if (recordStore is None) or (recordStore.getNumRecords() < 1):
                return False
            byArray = recordStore.getRecord(1)
        except Exception:
            pass
        if len(byArray) >= 28:
            MpCanvas.speed = byArray[0]
            MpCanvas.volume = byArray[1]
            MpCanvas.user_id = MpCanvas.cut_at_control(MpCanvas.read_utf(byArray, 2, 14))
            MpCanvas.password = MpCanvas.cut_at_control(MpCanvas.read_utf(byArray, 14, 28))
            return True
        return False

    @staticmethod
    def read_utf(byArray, n2, n3):  # g.java:4798
        n4 = n2
        n5 = n3
        string = None
        try:
            n6 = (n5 - n4)
            byArray2 = [0] * ((n6 + 2))
            byArray3 = byArray2
            byArray2[0] = i8((((n6 >> 8) & 0xFF)))
            byArray3[1] = i8(((n6 & 0xFF)))
            _arraycopy(byArray, n4, byArray3, 2, n6)
            byteArrayInputStream = ByteArrayInputStream(byArray3, 0, len(byArray3))
            dataInputStream = DataInputStream(byteArrayInputStream)
            string = dataInputStream.readUTF()
            byteArrayInputStream.close()
            dataInputStream.close()
        except Exception:
            pass
        return string

    @staticmethod
    def cut_at_control(string):  # g.java:4819
        n2 = 0
        n3 = len(string)
        n2 = 0
        while n2 < n3:
            if ord(string[n2]) < 32:
                break
            n2 = n2 + 1
        if n2 == 0:
            return ""
        return string[0:n2]

    def draw_popup(self):  # g.java:4833
        n2 = 0
        _sw101 = MpCanvas.popup_kind
        _m102 = False
        while True:
            if _m102 or _sw101 == 0:
                _m102 = True
                if MpCanvas.popup_shown:
                    self.draw_exit_confirm(MpCanvas.screen_g)
                    return
                n2 = (MpCanvas.center_y - 57)
                n3 = 0
                while n3 < 7:
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n2 + (12 * n3)), Consts.login_texts[(1 + n3)], 0xFFFFFF)
                    n3 = n3 + 1
                Draw.fill_rect(MpCanvas.screen_g, (MpCanvas.center_x - 40), (n2 + 86), 80, 13, 0)
                Draw.draw_rect(MpCanvas.screen_g, (MpCanvas.center_x - 40), (n2 + 86), 80, 13, 0x646464)
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((n2 + 52) + 35), MpCanvas.input_text, 0x41FF41)
                MpCanvas.draw_letter_grid(MpCanvas.letter_cursor, ((n2 + 64) + 35))
                if imod(MpCanvas.state_ticks, 4) < 2:
                    n4 = MpCanvas.font_white.string_width(MpCanvas.input_text)
                    if len(MpCanvas.input_text) == 12:
                        n4 = (n4 - (MpCanvas.font_white.string_width("A") * 2))
                    MpCanvas.draw_line_color(MpCanvas.screen_g, (MpCanvas.center_x + idiv(n4, 2)), ((n2 + 62) + 35), ((MpCanvas.center_x + idiv(n4, 2)) + 4), ((n2 + 62) + 35), 0xFFFFFF)
                if len(MpCanvas.input_text) == 0:
                    self.draw_softkeys(4, 2)
                    break
                self.draw_softkeys(4, 3)
                return
            if _m102 or _sw101 == 1:
                _m102 = True
                n2 = (MpCanvas.center_y - 45)
                n5 = 0
                while n5 < 5:
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n2 + (12 * n5)), Consts.login_texts[(8 + n5)], 0xFFFFFF)
                    n5 = n5 + 1
                Draw.fill_rect(MpCanvas.screen_g, (MpCanvas.center_x - 40), (n2 + 63), 80, 13, 0)
                Draw.draw_rect(MpCanvas.screen_g, (MpCanvas.center_x - 40), (n2 + 63), 80, 13, 0x646464)
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n2 + 64), MpCanvas.password, 0x41FF41)
                if len(MpCanvas.password) >= 4:
                    self.draw_softkeys(0, 3)
                    return
                if len(MpCanvas.password) > 0:
                    self.draw_softkeys((-1), 3)
                    return
                self.draw_softkeys((-1), 1)
            break

    def popup_keys(self, n2):  # g.java:4888
        _sw103 = MpCanvas.popup_kind
        _m104 = False
        while True:
            if _m104 or _sw103 == 0:
                _m104 = True
                if MpCanvas.popup_shown:
                    if (MpCanvas.key_in == (-3)) or (MpCanvas.key_in == (-4)):
                        MpCanvas.popup_cursor = imod(((MpCanvas.popup_cursor + 1)), 2)
                        return
                    if MpCanvas.key_in != (-5):
                        break
                    if MpCanvas.popup_cursor == 0:
                        MpCanvas.set_state(300)
                        return
                    MpCanvas.popup_shown = False
                    return
                len(MpCanvas.user_id)
                bl = False
                if n2 == (-7):
                    if len(MpCanvas.input_text) == 0:
                        MpCanvas.popup_shown = True
                        return
                    MpCanvas.input_text = MpCanvas.input_text[0:(len(MpCanvas.input_text) - 1)]
                    return
                if (MpCanvas.key_in == (-5)) or (MpCanvas.key_in == (-6)):
                    if len(MpCanvas.input_text) > 12:
                        break
                    if MpCanvas.letter_cursor < 26:
                        if len(MpCanvas.input_text) >= 12:
                            break
                        MpCanvas.input_text = _js(MpCanvas.input_text, chr(((((65 + MpCanvas.letter_cursor))) & 0xFFFF)))
                        return
                    if (MpCanvas.letter_cursor != 26) or (len(MpCanvas.input_text) < 4):
                        break
                    MpCanvas.user_id = MpCanvas.input_text
                    MpCanvas.popup_kind = 1
                    MpCanvas.password = ""
                    return
                MpCanvas.letter_grid_keys(MpCanvas.key_in)
                return
            if _m104 or _sw103 == 1:
                _m104 = True
                n3 = len(MpCanvas.password)
                n4 = (-1)
                _sw105 = n2
                if _sw105 == 48:
                    n4 = 0
                elif _sw105 == 49:
                    n4 = 1
                elif _sw105 == 50:
                    n4 = 2
                elif _sw105 == 51:
                    n4 = 3
                elif _sw105 == 52:
                    n4 = 4
                elif _sw105 == 53:
                    n4 = 5
                elif _sw105 == 54:
                    n4 = 6
                elif _sw105 == 55:
                    n4 = 7
                elif _sw105 == 56:
                    n4 = 8
                elif _sw105 == 57:
                    n4 = 9
                if n2 == (-7):
                    if n3 > 0:
                        MpCanvas.password = MpCanvas.password[0:(n3 - 1)]
                        return
                    MpCanvas.popup_kind = 0
                    MpCanvas.letter_cursor = 0
                    return
                if n4 != (-1):
                    if n3 >= 12:
                        break
                    MpCanvas.password = _js(_js(MpCanvas.password, ""), n4)
                    return
                if (n2 != (-6)) or (n3 < 4):
                    break
                MpCanvas.loading_msg = 0
                MpCanvas.password_login = True
                MpCanvas.set_state(10000)
            break

    def push_state(self, n2):  # g.java:4996
        if n2 != MpCanvas.state_stack[MpCanvas.stack_depth]:
            MpCanvas.cursor_stack[_inc(MpCanvas, 'stack_depth', 1)] = 0
            MpCanvas.state_stack[MpCanvas.stack_depth] = n2
        MpCanvas.set_state(n2)

    def reset_state_stack(self, n2):  # g.java:5004
        if n2 == 10:
            MpCanvas.relogin = True
        MpCanvas.stack_depth = 0
        MpCanvas.cursor_stack[0] = 0
        MpCanvas.state_stack[0] = n2
        MpCanvas.set_state(n2)

    def pop_state(self):  # g.java:5014
        if MpCanvas.stack_depth > 0:
            MpCanvas.set_state(MpCanvas.state_stack[_inc(MpCanvas, 'stack_depth', -1)])

    def pop_states(self, n2):  # g.java:5020
        if MpCanvas.stack_depth >= n2:
            MpCanvas.set_state(MpCanvas.state_stack[_set(MpCanvas, 'stack_depth', (MpCanvas.stack_depth - n2))])

    def free_frame_images(self):  # g.java:5026
        MpCanvas.border_h_image = None
        MpCanvas.border_v_image = None
        MpCanvas.titlebox_image = None
        MpCanvas.back_image = None
        MpCanvas.menu_icon_image = None
        n2 = 0
        while n2 < 6:
            MpCanvas.mpic_images[n2] = None
            n2 = n2 + 1
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

    def draw_skill_menu(self, graphics):  # g.java:5068
        self.draw_box(graphics, MpCanvas.center_x, (MpCanvas.center_y - 26), 110, 60, 0)
        Draw.fill_rect(graphics, (MpCanvas.center_x - 51), ((MpCanvas.center_y - 51) + (MpCanvas.skill_cursor * 12)), 102, 12, 12956683)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < MpCanvas.skill_slot_count:
            if MpCanvas.fighter_mp[0] < MpCanvas.skill_costs[(MpCanvas.skill_slots[MpCanvas.loop_i] - 3)]:
                self.draw_text_centred_on(graphics, MpCanvas.center_x, ((MpCanvas.center_y - 51) + (MpCanvas.loop_i * 12)), Consts.skill_names[(MpCanvas.skill_slots[MpCanvas.loop_i] - 3)], 0x646464)
                if (MpCanvas.skill_slots[MpCanvas.loop_i] != 9) and (MpCanvas.skill_slots[MpCanvas.loop_i] == 10):
                    pass
            else:
                self.draw_text_centred_on(graphics, MpCanvas.center_x, ((MpCanvas.center_y - 51) + (MpCanvas.loop_i * 12)), Consts.skill_names[(MpCanvas.skill_slots[MpCanvas.loop_i] - 3)], 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_battle_result(self):  # g.java:5085
        _sw106 = MpCanvas.room_mode
        if _sw106 in (0, 1):
            n2 = (MpCanvas.center_y - 62)
            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 102, 124, 0)
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n2 + 5), MpCanvas.fighter_name[0], 0xFFFFFF)
            string = (Consts.texts[5] if (MpCanvas.battle_won == 1) else Consts.texts[6])
            self.draw_text_colored(MpCanvas.screen_g, string, MpCanvas.center_x, (n2 + 19), 1, 16400640)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[49], (MpCanvas.center_x - 42), (n2 + 35), 0, 0xFFFFFF)
            self.draw_number0_on(MpCanvas.screen_g, (MpCanvas.center_x + 36), (n2 + 36), MpCanvas.wins)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[50], (MpCanvas.center_x - 42), (n2 + 50), 0, 0xFFFFFF)
            self.draw_number0_on(MpCanvas.screen_g, (MpCanvas.center_x + 36), (n2 + 51), MpCanvas.losses)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[29], (MpCanvas.center_x - 42), (n2 + 70), 0, 0xFFFFFF)
            self.draw_number1_on(MpCanvas.screen_g, (MpCanvas.center_x + 36), (n2 + 71), MpCanvas.reward_gold)
            self.draw_text_colored(MpCanvas.screen_g, Consts.rank_menu[0], (MpCanvas.center_x - 42), (n2 + 83), 0, 0xFFFFFF)
            self.draw_number1_on(MpCanvas.screen_g, (MpCanvas.center_x + 36), (n2 + 84), MpCanvas.reward_fame)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[4], (MpCanvas.center_x - 42), (n2 + 96), 0, 0x41FF41)
            self.draw_number0_on(MpCanvas.screen_g, (MpCanvas.center_x + 36), (n2 + 97), MpCanvas.reward_rank)
            self.draw_ok_button((n2 + 109))
            return
        elif _sw106 == 2:
            n3 = (MpCanvas.center_y - 62)
            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 102, 124, 0)
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n3 + 3), MpCanvas.fighter_name[0], 0xFFFFFF)
            if MpCanvas.battle_won == 1:
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n3 + 15), Consts.grades[MpCanvas.reward_grade], 16400640)
            else:
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n3 + 15), Consts.texts[31], 16400640)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[29], (MpCanvas.center_x - 34), (n3 + 30), 0, 0xFFFFFF)
            self.draw_number1_on(MpCanvas.screen_g, (MpCanvas.center_x + 30), (n3 + 31), MpCanvas.reward_gold)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[32], (MpCanvas.center_x - 34), (n3 + 42), 0, 0xFFFFFF)
            self.draw_number1_on(MpCanvas.screen_g, (MpCanvas.center_x + 30), (n3 + 43), MpCanvas.reward_exp)
            self.draw_text_colored(MpCanvas.screen_g, Consts.rank_menu[0], (MpCanvas.center_x - 34), (n3 + 54), 0, 0xFFFFFF)
            self.draw_number1_on(MpCanvas.screen_g, (MpCanvas.center_x + 30), (n3 + 55), MpCanvas.reward_fame)
            if not (MpCanvas.loot == "NONE"):
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n3 + 69), MpCanvas.loot, 0xFFFFFF)
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n3 + 81), _js(Consts.texts[33], "!!!"), 0xFFFFFF)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[4], (MpCanvas.center_x - 34), (n3 + 96), 0, 0x41FF41)
            self.draw_number1_on(MpCanvas.screen_g, (MpCanvas.center_x + 30), (n3 + 97), MpCanvas.reward_rank)
            self.draw_ok_button((n3 + 109))

    @staticmethod
    def tick_status_effects():  # g.java:5133
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                _sw107 = MpCanvas.fighter_status[MpCanvas.loop_i]
                _m108 = False
                while True:
                    if _m108 or _sw107 in (11, 12, 13):
                        _m108 = True
                        n2 = MpCanvas.loop_i
                        MpCanvas.fighter_status_ticks[n2] = (MpCanvas.fighter_status_ticks[n2] - 1)
                        if MpCanvas.fighter_status_ticks[MpCanvas.loop_i] > 0:
                            break
                        MpCanvas.fighter_status[MpCanvas.loop_i] = 99
                    break
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_action_cards(self):  # g.java:5152
        MpCanvas.box_x = 0
        if MpCanvas.state_ticks == 0:
            MpCanvas.box_x = (-40)
        elif MpCanvas.state_ticks == 1:
            MpCanvas.box_x = (-20)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if (MpCanvas.fighter_present[MpCanvas.loop_i] and (MpCanvas.fighter_hp[MpCanvas.loop_i] > 0)) and (((((MpCanvas.state == 99) or (MpCanvas.loop_i == MpCanvas.attacker)) or (MpCanvas.loop_i == MpCanvas.target)) or (MpCanvas.loop_i == MpCanvas.target2))):
                MpCanvas.box_y = (27 if (MpCanvas.room_mode == 0) else ((27 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_h - 27) - 23))))
                _sw109 = MpCanvas.fighter_kind[MpCanvas.loop_i]
                if _sw109 == 0:
                    MpCanvas.card_face = MpCanvas.fighter_face[MpCanvas.loop_i]
                    MpCanvas.card_half = True
                elif _sw109 == 1:
                    MpCanvas.card_face = 4
                    MpCanvas.card_half = False
                elif _sw109 == 2:
                    MpCanvas.card_face = 5
                    MpCanvas.card_half = False
                if MpCanvas.state == 99:
                    MpCanvas.tmp = MpCanvas.turn_actions[MpCanvas.loop_i]
                elif MpCanvas.loop_i == MpCanvas.attacker:
                    MpCanvas.tmp = MpCanvas.turn_bytes[(4 + MpCanvas.turn_rec)]
                elif MpCanvas.loop_i == MpCanvas.target:
                    MpCanvas.tmp = MpCanvas.turn_bytes[(16 + MpCanvas.turn_rec)]
                elif MpCanvas.loop_i == MpCanvas.target2:
                    MpCanvas.tmp = MpCanvas.turn_bytes[(36 + MpCanvas.turn_rec)]
                if imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0:
                    Draw.draw_rect(MpCanvas.screen_g, MpCanvas.box_x, MpCanvas.box_y, 60, 23, 0)
                    Draw.draw_rect(MpCanvas.screen_g, (MpCanvas.box_x + 1), (MpCanvas.box_y + 1), 58, 21, 16769990)
                    _sw110 = MpCanvas.tmp
                    if _sw110 in (0, 3, 4, 5, 6, 7, 8):
                        self.load_numbered_image(MpCanvas.act_images, "act", 0)
                        self.load_numbered_image(MpCanvas.act_images, "act", (6 + MpCanvas.card_face))
                        MpCanvas.draw_left_half((MpCanvas.box_x + Consts.act_dx[0]), (MpCanvas.box_y + Consts.act_dy[0]), MpCanvas.act_images[0])
                        MpCanvas.draw_left_half((MpCanvas.box_x + Consts.act_dx[(6 + MpCanvas.card_face)]), (MpCanvas.box_y + Consts.act_dy[(6 + MpCanvas.card_face)]), MpCanvas.act_images[(6 + MpCanvas.card_face)])
                    else:
                        self.load_numbered_image(MpCanvas.act_images, "act", 1)
                        self.load_numbered_image(MpCanvas.act_images, "act", (12 + MpCanvas.card_face))
                        MpCanvas.draw_left_half((MpCanvas.box_x + Consts.act_dx[1]), (MpCanvas.box_y + Consts.act_dy[1]), MpCanvas.act_images[1])
                        MpCanvas.draw_left_half((MpCanvas.box_x + Consts.act_dx[(12 + MpCanvas.card_face)]), (MpCanvas.box_y + Consts.act_dy[(12 + MpCanvas.card_face)]), MpCanvas.act_images[(12 + MpCanvas.card_face)])
                    MpCanvas.tmp = (3 if (MpCanvas.tmp > 2) else MpCanvas.tmp)
                    self.load_numbered_image(MpCanvas.act_images, "act", (2 + MpCanvas.tmp))
                    MpCanvas.draw_image((((MpCanvas.box_x + 60) - 19) + Consts.act_dx[(2 + MpCanvas.tmp)]), ((0 + MpCanvas.box_y) + Consts.act_dy[(2 + MpCanvas.tmp)]), MpCanvas.act_images[(2 + MpCanvas.tmp)])
                else:
                    MpCanvas.draw_rect(((MpCanvas.canvas_w - MpCanvas.box_x) - 60), MpCanvas.box_y, 60, 23, 0)
                    MpCanvas.draw_rect((((MpCanvas.canvas_w - MpCanvas.box_x) - 60) + 1), (MpCanvas.box_y + 1), 58, 21, 16769990)
                    _sw111 = MpCanvas.tmp
                    if _sw111 in (0, 3, 4, 5, 6, 7, 8):
                        self.load_numbered_image(MpCanvas.act_images, "act", (6 + MpCanvas.card_face))
                        MpCanvas.draw_right_half((MpCanvas.canvas_w - ((MpCanvas.box_x + Consts.act_dx[0]))), (MpCanvas.box_y + Consts.act_dy[0]), MpCanvas.act_images[0])
                        MpCanvas.draw_right_aligned((MpCanvas.canvas_w - ((MpCanvas.box_x + Consts.act_dx[(6 + MpCanvas.card_face)]))), (MpCanvas.box_y + Consts.act_dy[(6 + MpCanvas.card_face)]), MpCanvas.act_images[(6 + MpCanvas.card_face)], MpCanvas.card_half)
                    else:
                        self.load_numbered_image(MpCanvas.act_images, "act", (12 + MpCanvas.card_face))
                        MpCanvas.draw_right_half((MpCanvas.canvas_w - ((MpCanvas.box_x + Consts.act_dx[1]))), (MpCanvas.box_y + Consts.act_dy[1]), MpCanvas.act_images[1])
                        MpCanvas.draw_right_aligned((MpCanvas.canvas_w - ((MpCanvas.box_x + Consts.act_dx[(12 + MpCanvas.card_face)]))), (MpCanvas.box_y + Consts.act_dy[(12 + MpCanvas.card_face)]), MpCanvas.act_images[(12 + MpCanvas.card_face)], MpCanvas.card_half)
                    MpCanvas.tmp = (3 if (MpCanvas.tmp > 2) else MpCanvas.tmp)
                    self.load_numbered_image(MpCanvas.act_images, "act", (2 + MpCanvas.tmp))
                    MpCanvas.draw_image(((((MpCanvas.canvas_w - MpCanvas.box_x) - 60) + 10) + Consts.act_dx[(2 + MpCanvas.tmp)]), ((0 + MpCanvas.box_y) + Consts.act_dy[(2 + MpCanvas.tmp)]), MpCanvas.act_images[(2 + MpCanvas.tmp)])
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_round(self, graphics):  # g.java:5246
        if MpCanvas.round_no < 10:
            Draw.draw_image_part(graphics, MpCanvas.number_images[3], (MpCanvas.center_x - 33), (MpCanvas.center_y - 31), 52, 13, 120, 0)
            self.draw_number3_on(graphics, (MpCanvas.center_x + 21), (MpCanvas.center_y - 31), MpCanvas.round_no)
            return
        Draw.draw_image_part(graphics, MpCanvas.number_images[3], (MpCanvas.center_x - 39), (MpCanvas.center_y - 31), 52, 13, 120, 0)
        self.draw_number3_on(graphics, (MpCanvas.center_x + 27), (MpCanvas.center_y - 31), MpCanvas.round_no)

    @staticmethod
    def draw_action_pad(graphics):  # g.java:5256
        MpCanvas.box_x = MpCanvas.center_x
        MpCanvas.box_y = (MpCanvas.center_y - 40)
        if MpCanvas.room_mode == 0:
            MpCanvas.box_y = (MpCanvas.box_y - 6)
        Draw.draw_image(graphics, MpCanvas.ui_images[17], (MpCanvas.box_x - 12), MpCanvas.box_y, 0)
        Draw.draw_image(graphics, MpCanvas.ui_images[16], ((MpCanvas.box_x - 36) - 1), (MpCanvas.box_y + 16), 0)
        Draw.draw_image(graphics, MpCanvas.ui_images[15], ((MpCanvas.box_x + 12) + 1), (MpCanvas.box_y + 16), 0)
        MpCanvas.skill_ready = False
        if MpCanvas.skill_slot_count > 0:
            MpCanvas.loop_k = 0
            while MpCanvas.loop_k < MpCanvas.skill_slot_count:
                if MpCanvas.fighter_mp[0] >= MpCanvas.skill_costs[(MpCanvas.skill_slots[MpCanvas.loop_k] - 3)]:
                    MpCanvas.skill_ready = True
                MpCanvas.loop_k = MpCanvas.loop_k + 1
        Draw.draw_image(graphics, MpCanvas.ui_images[(18 + ((0 if MpCanvas.skill_ready else 1)))], (MpCanvas.box_x - 12), (MpCanvas.box_y + 30), 0)
        if MpCanvas.chosen_action != 99:
            n2 = 0
            n3 = 0
            if MpCanvas.chosen_action == 0:
                n3 = ((MpCanvas.box_x + 12) + 1)
                n2 = (MpCanvas.box_y + 16)
            elif MpCanvas.chosen_action == 1:
                n3 = ((MpCanvas.box_x - 36) - 1)
                n2 = (MpCanvas.box_y + 16)
            elif MpCanvas.chosen_action == 2:
                n3 = (MpCanvas.box_x - 12)
                n2 = MpCanvas.box_y
            else:
                n3 = (MpCanvas.box_x - 12)
                n2 = (MpCanvas.box_y + 30)
            Draw.draw_rect(graphics, (n3 - 1), (n2 - 1), 24, 24, 15721306)
            Draw.draw_rect(graphics, n3, n2, 23, 23, 15721306)

    def draw_battle_prompt(self, graphics, n2):  # g.java:5297
        n3 = 0
        if MpCanvas.room_mode == 0:
            n3 = 25
        _sw112 = n2
        if _sw112 == 0:
            if MpCanvas.choose_secs > 5:
                self.draw_box(graphics, MpCanvas.center_x, ((MpCanvas.center_y + 28) + n3), 120, 27, 0)
                self.draw_text_centred(MpCanvas.center_x, ((MpCanvas.center_y + 17) + n3), Consts.texts[0], 0xFFFFFF)
                self.draw_text_centred(MpCanvas.center_x, ((MpCanvas.center_y + 28) + n3), Consts.texts[1], (0x646464 if MpCanvas.exit_asked else 0xFFFFFF))
                return
            self.draw_box(graphics, MpCanvas.center_x, ((MpCanvas.center_y + 28) + n3), 26, 26, 0)
            self.draw_number2_on(graphics, (MpCanvas.center_x - 4), ((MpCanvas.center_y + 22) + n3), MpCanvas.choose_secs)
            return
        elif _sw112 == 1:
            self.draw_box(graphics, MpCanvas.center_x, ((MpCanvas.center_y + 28) + n3), 120, 27, 0)
            self.draw_text_centred(MpCanvas.center_x, ((MpCanvas.center_y + 23) + n3), Consts.texts[17], 0xFFFFFF)
            return
        elif _sw112 == 2:
            string = ""
            if imod(MpCanvas.state_ticks, 4) == 1:
                string = "."
            elif imod(MpCanvas.state_ticks, 4) == 2:
                string = ".."
            elif imod(MpCanvas.state_ticks, 4) == 3:
                string = "..."
            self.draw_box(graphics, MpCanvas.center_x, ((MpCanvas.center_y + 28) + n3), 80, 24, 0)
            self.draw_text_left((MpCanvas.center_x - 30), ((MpCanvas.center_y + 23) + n3), _js(Consts.texts[7], string), 0xFFFFFF)

    def check_invite_timeout(self):  # g.java:5334
        if MpCanvas.wait_started:
            if idiv(((MpCanvas.wait_start_time - system.currentTimeMillis())), 1000) >= 80:
                MpCanvas.wait_started = False
                MpCanvas.error_msg = 13
                MpCanvas.popup_shown = False
                MpCanvas.disconnect()
                MpCanvas.set_timer((-1))
                self.push_state(4)
                return
        else:
            MpCanvas.wait_started = True
            MpCanvas.wait_start_time = system.currentTimeMillis()

    def draw_help(self):  # g.java:5351
        n2 = (MpCanvas.center_y - 57)
        self.draw_window(MpCanvas.screen_g)
        MpCanvas.fill_rect(((MpCanvas.center_x - 52) - 7), (n2 - 2), 118, 123, 0)
        MpCanvas.draw_rect(((MpCanvas.center_x - 52) - 7), (n2 - 2), 118, 123, 0x949694)
        MpCanvas.fill_rect(((MpCanvas.center_x - 52) - 6), (n2 - 1), 116, 13, 0x313431)
        MpCanvas.help_first_line = 0
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < MpCanvas.help_page:
            _sw113 = MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]
            if _sw113 == 0:
                MpCanvas.help_first_line = (MpCanvas.help_first_line + Consts.help_controls_lines[MpCanvas.loop_i])
            elif _sw113 == 1:
                MpCanvas.help_first_line = (MpCanvas.help_first_line + Consts.help_menu_lines[MpCanvas.loop_i])
            elif _sw113 == 2:
                MpCanvas.help_first_line = (MpCanvas.help_first_line + Consts.help_duel_lines[MpCanvas.loop_i])
            elif _sw113 == 3:
                MpCanvas.help_first_line = (MpCanvas.help_first_line + Consts.help_mission_lines[MpCanvas.loop_i])
            elif _sw113 == 4:
                MpCanvas.help_first_line = (MpCanvas.help_first_line + Consts.help_about_lines[MpCanvas.loop_i])
            elif _sw113 == 5:
                MpCanvas.help_first_line = (MpCanvas.help_first_line + Consts.help_network_lines[MpCanvas.loop_i])
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        _sw114 = MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]
        if _sw114 == 0:
            self.draw_text_centred(MpCanvas.center_x, n2, Consts.help_controls[MpCanvas.help_first_line], 0xFFFFFF)
            MpCanvas.tmp = Consts.help_controls_lines[MpCanvas.help_page]
        elif _sw114 == 1:
            self.draw_text_centred(MpCanvas.center_x, n2, Consts.help_menu[MpCanvas.help_first_line], 0xFFFFFF)
            MpCanvas.tmp = Consts.help_menu_lines[MpCanvas.help_page]
        elif _sw114 == 2:
            self.draw_text_centred(MpCanvas.center_x, n2, Consts.help_duel[MpCanvas.help_first_line], 0xFFFFFF)
            MpCanvas.tmp = Consts.help_duel_lines[MpCanvas.help_page]
        elif _sw114 == 3:
            self.draw_text_centred(MpCanvas.center_x, n2, Consts.help_mission[MpCanvas.help_first_line], 0xFFFFFF)
            MpCanvas.tmp = Consts.help_mission_lines[MpCanvas.help_page]
        elif _sw114 == 4:
            self.draw_text_centred(MpCanvas.center_x, n2, Consts.help_about[MpCanvas.help_first_line], 0xFFFFFF)
            MpCanvas.tmp = Consts.help_about_lines[MpCanvas.help_page]
        elif _sw114 == 5:
            self.draw_text_centred(MpCanvas.center_x, n2, Consts.help_network[MpCanvas.help_first_line], 0xFFFFFF)
            MpCanvas.tmp = Consts.help_network_lines[MpCanvas.help_page]
        MpCanvas.loop_i = 1
        while MpCanvas.loop_i < MpCanvas.tmp:
            _sw115 = MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]
            _m116 = False
            while True:
                if _m116 or _sw115 == 0:
                    _m116 = True
                    self.draw_text_left((MpCanvas.center_x - 56), ((n2 + (MpCanvas.loop_i * 12)) + 1), Consts.help_controls[(MpCanvas.help_first_line + MpCanvas.loop_i)], 0xFFFFFF)
                    break
                if _m116 or _sw115 == 1:
                    _m116 = True
                    self.draw_text_left((MpCanvas.center_x - 56), ((n2 + (MpCanvas.loop_i * 12)) + 1), Consts.help_menu[(MpCanvas.help_first_line + MpCanvas.loop_i)], 0xFFFFFF)
                    break
                if _m116 or _sw115 == 2:
                    _m116 = True
                    self.draw_text_left((MpCanvas.center_x - 56), ((n2 + (MpCanvas.loop_i * 12)) + 1), Consts.help_duel[(MpCanvas.help_first_line + MpCanvas.loop_i)], 0xFFFFFF)
                    break
                if _m116 or _sw115 == 3:
                    _m116 = True
                    self.draw_text_left((MpCanvas.center_x - 56), ((n2 + (MpCanvas.loop_i * 12)) + 1), Consts.help_mission[(MpCanvas.help_first_line + MpCanvas.loop_i)], 0xFFFFFF)
                    break
                if _m116 or _sw115 == 4:
                    _m116 = True
                    self.draw_text_centred(MpCanvas.center_x, ((n2 + (MpCanvas.loop_i * 17)) + 9), Consts.help_about[(MpCanvas.help_first_line + MpCanvas.loop_i)], 0xFFFFFF)
                    if MpCanvas.loop_i != 3:
                        break
                    self.draw_text_centred(MpCanvas.center_x, ((n2 + (MpCanvas.loop_i * 17)) + 9), _js("v", MpCanvas.app_version), 0xFFFFFF)
                    break
                if _m116 or _sw115 == 5:
                    _m116 = True
                    self.draw_text_left((MpCanvas.center_x - 56), ((n2 + (MpCanvas.loop_i * 12)) + 1), Consts.help_network[(MpCanvas.help_first_line + MpCanvas.loop_i)], 0xFFFFFF)
                break
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        if Consts.help_pages[MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]] > 1:
            self.draw_text_centred(MpCanvas.center_x, ((n2 + 72) + 38), _js(_js((MpCanvas.help_page + 1), "/"), Consts.help_pages[MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]]), 0xFFFFFF)
            MpCanvas.draw_left_half((MpCanvas.center_x - 35), ((n2 + 72) + 39), MpCanvas.arrow_images[1])
            MpCanvas.draw_right_half((MpCanvas.center_x + 35), ((n2 + 72) + 39), MpCanvas.arrow_images[1])

    def draw_menu_icons(self):  # g.java:5456
        self.draw_window_bg(MpCanvas.buffer_g)
        n2 = idiv(80, MpCanvas.menu_size)
        if n2 > 30:
            n2 = 30
        elif n2 < 19:
            n2 = 19
        n3 = 0
        if ((MpCanvas.state == 162) or (MpCanvas.state == 163)) or (MpCanvas.state == 164):
            n3 = 15
        elif MpCanvas.state == 10:
            n3 = 40
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < MpCanvas.menu_size:
            Draw.draw_image_part(MpCanvas.buffer_g, MpCanvas.menu_icon_image, (idiv((((MpCanvas.canvas_w - (n2 * ((MpCanvas.menu_size - 1)))) - 11)), 2) + (n2 * MpCanvas.loop_i)), ((MpCanvas.center_y + 6) + n3), 12, 15, 12, 0)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def load_status_effect(self):  # g.java:5477
        if MpCanvas.draw_mirrored:
            self.load_named_image(MpCanvas.effect_images[1], "spreff2_r", 1)
        else:
            self.load_named_image(MpCanvas.effect_images[1], "spreff2", 0)
        if MpCanvas.effect3_frames[0] is None:
            MpCanvas.effect3_frames[0] = SpriteFrames("/spreff3.SP2")

    @staticmethod
    def draw_status_effect(graphics, n2):  # g.java:5488
        n3 = ((n2 * 2) + imod(MpCanvas.state_ticks, 2))
        if MpCanvas.draw_mirrored:
            Draw.draw_image_part(graphics, MpCanvas.effect_images[1][1], (MpCanvas.canvas_w - (((MpCanvas.draw_x - MpCanvas.effect3_frames[0].anchor_x[n3]) + MpCanvas.effect3_frames[0].w[n3]))), (MpCanvas.draw_y - MpCanvas.effect3_frames[0].anchor_y[n3]), MpCanvas.effect3_frames[0].w[n3], MpCanvas.effect3_frames[0].h[n3], MpCanvas.effect3_frames[0].src_x[n3], MpCanvas.effect3_frames[0].src_y[n3])
            return
        Draw.draw_image_part(graphics, MpCanvas.effect_images[1][0], (MpCanvas.draw_x - MpCanvas.effect3_frames[0].anchor_x[n3]), (MpCanvas.draw_y - MpCanvas.effect3_frames[0].anchor_y[n3]), MpCanvas.effect3_frames[0].w[n3], MpCanvas.effect3_frames[0].h[n3], MpCanvas.effect3_frames[0].src_x[n3], MpCanvas.effect3_frames[0].src_y[n3])

    def load_numbered_image(self, imageArray, string, n2):  # g.java:5497
        if imageArray[n2] is None:
            imageArray[n2] = self.load_image(_js(_js(_js("/", string), n2), ".png"))

    def load_named_image(self, imageArray, string, n2):  # g.java:5503
        if imageArray[n2] is None:
            imageArray[n2] = self.load_image(_js(_js("/", string), ".png"))

    def load_sprite(self, imageArray, aArray, string):  # g.java:5509
        self.load_sprite_dir(imageArray, aArray, string, 1)

    def load_sprite_dir(self, imageArray, aArray, string, n2):  # g.java:5513
        if MpCanvas.draw_mirrored:
            if imageArray[1] is None:
                imageArray[1] = self.load_image(_js(_js("/", string), "_r.png"))
        elif imageArray[0] is None:
            imageArray[0] = self.load_image(_js(_js("/", string), ".png"))
        if aArray[0] is None:
            if n2 == 0:
                aArray[0] = SpriteFrames(_js(_js("/", string), ".SP2"))
                return
            if n2 == 1:
                aArray[0] = SpriteFrames(_js(_js("/", string), "_basic.SP2"))
                aArray[1] = SpriteFrames(_js(_js("/", string), "_skill1.SP2"))
                aArray[2] = SpriteFrames(_js(_js("/", string), "_skill2.SP2"))

    def draw_background(self):  # g.java:5534
        n2 = 0
        n3 = 0
        Draw.fill_rect(MpCanvas.buffer_g, 0, 0, MpCanvas.canvas_w, MpCanvas.canvas_h, 0)
        n3 = (idiv(MpCanvas.screen_h, 2) - 95)
        n4 = (idiv(MpCanvas.screen_w, 30) + 1)
        n5 = ((MpCanvas.room_bg >> 6) & 3)
        _sw117 = n5
        if _sw117 == 0:
            self.load_bg(4)
            self.load_bg(5)
            self.load_bg(6)
            self.load_bg(7)
            self.load_bg(8)
            Draw.fill_rect(MpCanvas.buffer_g, 0, 0, MpCanvas.canvas_w, (n3 + 1), 11257599)
            n2 = 0
            while n2 < n4:
                MpCanvas.draw_image_on(MpCanvas.buffer_g, (30 * n2), n3, MpCanvas.bg_images[4])
                MpCanvas.draw_image_on(MpCanvas.buffer_g, (30 * n2), (n3 + 30), MpCanvas.bg_images[5])
                n2 = n2 + 1
            MpCanvas.draw_image_on(MpCanvas.buffer_g, (MpCanvas.screen_w - MpCanvas.bg_images[6].getWidth()), ((n3 - 2) - MpCanvas.bg_images[6].getHeight()), MpCanvas.bg_images[6])
            MpCanvas.draw_image_on(MpCanvas.buffer_g, 18, (n3 - 30), MpCanvas.bg_images[7])
            MpCanvas.draw_image_on(MpCanvas.buffer_g, 52, (n3 - 15), MpCanvas.bg_images[8])
        elif _sw117 == 1:
            self.load_bg(9)
            self.load_bg(10)
            self.load_bg(11)
            self.load_bg(12)
            self.load_bg(13)
            Draw.fill_rect(MpCanvas.buffer_g, 0, 0, MpCanvas.canvas_w, (n3 + 1), 1645890)
            n2 = 0
            while n2 < n4:
                MpCanvas.draw_image_on(MpCanvas.buffer_g, (30 * n2), n3, MpCanvas.bg_images[9])
                MpCanvas.draw_image_on(MpCanvas.buffer_g, (30 * n2), (n3 + 30), MpCanvas.bg_images[10])
                n2 = n2 + 1
            MpCanvas.draw_image_on(MpCanvas.buffer_g, (MpCanvas.screen_w - MpCanvas.bg_images[6].getWidth()), ((n3 - 2) - MpCanvas.bg_images[6].getHeight()), MpCanvas.bg_images[11])
            MpCanvas.draw_image_on(MpCanvas.buffer_g, 18, (n3 - 30), MpCanvas.bg_images[12])
            MpCanvas.draw_image_on(MpCanvas.buffer_g, 52, (n3 - 15), MpCanvas.bg_images[13])
        n6 = ((MpCanvas.room_bg >> 4) & 3)
        self.load_bg((14 + n6))
        n2 = 0
        while n2 < n4:
            MpCanvas.draw_image_on(MpCanvas.buffer_g, (30 * n2), (n3 + 83), MpCanvas.bg_images[(14 + n6)])
            n2 = n2 + 1
        n7 = (MpCanvas.room_bg & 3)
        n8 = 0
        nArray = [3, 8, (-8), 16]
        self.load_bg((0 + n7))
        n8 = (n3 + nArray[n7])
        MpCanvas.draw_image_on(MpCanvas.buffer_g, 0, n8, MpCanvas.bg_images[(0 + n7)])
        n2 = 0
        while n2 < len(MpCanvas.bg_images):
            MpCanvas.bg_images[n2] = None
            n2 = n2 + 1
        MpCanvas.noop()

    @staticmethod
    def noop():  # g.java:5599
        None

    def load_bg(self, n2):  # g.java:5603
        if MpCanvas.bg_images[n2] is None:
            MpCanvas.bg_images[n2] = self.load_image(_js(_js("/gamebg", n2), ".png"))

    def draw_hp_bar_frames(self):  # g.java:5609
        Draw.fill_rect(MpCanvas.buffer_g, 0, 0, MpCanvas.canvas_w, 12, 0)
        MpCanvas.draw_hp_bar_frame(0)
        n2 = 0
        Draw.draw_hline(MpCanvas.buffer_g, 28, 4, (MpCanvas.hp_bar_w - 1), 8429760)
        Draw.draw_hline(MpCanvas.buffer_g, 28, 10, (MpCanvas.hp_bar_w - 1), 8429760)
        Draw.draw_hline(MpCanvas.buffer_g, 31, 4, ((MpCanvas.hp_bar_w - 1) - 6), 0x808080)
        Draw.draw_hline(MpCanvas.buffer_g, 31, 10, ((MpCanvas.hp_bar_w - 1) - 6), 0x808080)
        n2 = (28 + MpCanvas.hp_bar_w)
        Draw.draw_vline(MpCanvas.buffer_g, n2, 0, 10, 0x808080)
        Draw.draw_vline(MpCanvas.buffer_g, n2, 3, 1, 8429760)
        Draw.draw_vline(MpCanvas.buffer_g, n2, 4, 1, 0)
        Draw.draw_vline(MpCanvas.buffer_g, n2, 5, 1, 8429760)
        Draw.draw_vline(MpCanvas.buffer_g, n2, 9, 1, 8429760)
        MpCanvas.draw_hp_bar_frame(1)
        n2 = (((MpCanvas.canvas_w - 28) - MpCanvas.hp_bar_w) + 1)
        Draw.draw_hline(MpCanvas.buffer_g, n2, 4, (MpCanvas.hp_bar_w - 1), 8429760)
        Draw.draw_hline(MpCanvas.buffer_g, n2, 10, (MpCanvas.hp_bar_w - 1), 8429760)
        Draw.draw_hline(MpCanvas.buffer_g, (n2 + 3), 4, ((MpCanvas.hp_bar_w - 1) - 6), 0x808080)
        Draw.draw_hline(MpCanvas.buffer_g, (n2 + 3), 10, ((MpCanvas.hp_bar_w - 1) - 6), 0x808080)
        n2 = (((MpCanvas.canvas_w - 28) - 1) - MpCanvas.hp_bar_w)
        Draw.draw_vline(MpCanvas.buffer_g, n2, 0, 10, 0x808080)
        Draw.draw_vline(MpCanvas.buffer_g, n2, 3, 1, 8429760)
        Draw.draw_vline(MpCanvas.buffer_g, n2, 4, 1, 0)
        Draw.draw_vline(MpCanvas.buffer_g, n2, 5, 1, 8429760)
        Draw.draw_vline(MpCanvas.buffer_g, n2, 9, 1, 8429760)
        if MpCanvas.room_mode != 0:
            Draw.fill_rect(MpCanvas.buffer_g, 0, (MpCanvas.canvas_h - 12), MpCanvas.canvas_w, 12, 0)
            MpCanvas.draw_hp_bar_frame(2)
            Draw.draw_hline(MpCanvas.buffer_g, 28, (MpCanvas.canvas_h - 5), (MpCanvas.hp_bar_w - 1), 8429760)
            Draw.draw_hline(MpCanvas.buffer_g, 28, (MpCanvas.canvas_h - 11), (MpCanvas.hp_bar_w - 1), 8429760)
            Draw.draw_hline(MpCanvas.buffer_g, 31, (MpCanvas.canvas_h - 5), (MpCanvas.hp_bar_w - 6), 0x808080)
            Draw.draw_hline(MpCanvas.buffer_g, 31, (MpCanvas.canvas_h - 11), (MpCanvas.hp_bar_w - 6), 0x808080)
            n2 = ((28 + MpCanvas.hp_bar_w) + 1)
            Draw.draw_vline(MpCanvas.buffer_g, (n2 - 1), (MpCanvas.canvas_h - 9), 9, 0x808080)
            Draw.draw_vline(MpCanvas.buffer_g, (n2 - 1), (MpCanvas.canvas_h - 4), 1, 8429760)
            Draw.draw_vline(MpCanvas.buffer_g, (n2 - 1), (MpCanvas.canvas_h - 5), 1, 0)
            Draw.draw_vline(MpCanvas.buffer_g, (n2 - 1), (MpCanvas.canvas_h - 6), 1, 8429760)
            Draw.draw_vline(MpCanvas.buffer_g, (n2 - 1), (MpCanvas.canvas_h - 10), 1, 8429760)
            MpCanvas.draw_hp_bar_frame(3)
            n2 = (((MpCanvas.canvas_w - 28) - MpCanvas.hp_bar_w) + 1)
            Draw.draw_hline(MpCanvas.buffer_g, n2, (MpCanvas.canvas_h - 5), (MpCanvas.hp_bar_w - 1), 8429760)
            Draw.draw_hline(MpCanvas.buffer_g, n2, (MpCanvas.canvas_h - 11), (MpCanvas.hp_bar_w - 1), 8429760)
            Draw.draw_hline(MpCanvas.buffer_g, (n2 + 3), (MpCanvas.canvas_h - 5), ((MpCanvas.hp_bar_w - 1) - 6), 0x808080)
            Draw.draw_hline(MpCanvas.buffer_g, (n2 + 3), (MpCanvas.canvas_h - 11), ((MpCanvas.hp_bar_w - 1) - 6), 0x808080)
            n2 = (((MpCanvas.canvas_w - 28) - 1) - MpCanvas.hp_bar_w)
            Draw.draw_vline(MpCanvas.buffer_g, n2, (MpCanvas.canvas_h - 9), 10, 0x808080)
            Draw.draw_vline(MpCanvas.buffer_g, n2, (MpCanvas.canvas_h - 4), 1, 8429760)
            Draw.draw_vline(MpCanvas.buffer_g, n2, (MpCanvas.canvas_h - 5), 1, 0)
            Draw.draw_vline(MpCanvas.buffer_g, n2, (MpCanvas.canvas_h - 6), 1, 8429760)
            Draw.draw_vline(MpCanvas.buffer_g, n2, (MpCanvas.canvas_h - 10), 1, 8429760)

    @staticmethod
    def draw_hp_bar_frame(n2):  # g.java:5663
        n3 = (28 if (imod(n2, 2) == 0) else ((((MpCanvas.canvas_w - 28) - 1) - MpCanvas.hp_bar_w) + 2))
        n4 = (0 if (idiv(n2, 2) == 0) else ((MpCanvas.canvas_h - 3) - 6))
        n5 = 0
        while n5 < 2:
            if n5 == 1:
                n4 = (n4 + 6)
            Draw.draw_hline(MpCanvas.buffer_g, n3, n4, (MpCanvas.hp_bar_w - 1), 0x808080)
            Draw.draw_hline(MpCanvas.buffer_g, n3, (n4 + 1), (MpCanvas.hp_bar_w - 1), 0xFFFFFF)
            Draw.draw_hline(MpCanvas.buffer_g, n3, (n4 + 2), (MpCanvas.hp_bar_w - 1), 0xC0C0C0)
            n5 = n5 + 1

    def draw_window(self, graphics):  # g.java:5678
        self.draw_window_bg(graphics)

    def draw_window_bg(self, graphics):  # g.java:5682
        n2 = 0
        n3 = 0
        n4 = 0
        MpCanvas.draw_back_tiles(graphics)
        if MpCanvas.canvas_h <= 144:
            n4 = (78 - idiv(((144 - MpCanvas.canvas_h)), 2))
            n3 = ((MpCanvas.canvas_h - 18) - n4)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, 0, 5, 5, 8, 0, 0)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, 0, 13, 5, n4, 0, (8 + ((78 - n4))))
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, 0, (13 + n4), 5, n3, 0, (134 - n3))
            n2 = (MpCanvas.canvas_w - 5)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, n2, 5, 5, 8, 5, 0)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, n2, 13, 5, n4, 5, (8 + ((78 - n4))))
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, n2, (13 + n4), 5, n3, 5, (134 - n3))
        else:
            n4 = idiv(((MpCanvas.canvas_h - 144)), 2)
            n3 = ((MpCanvas.canvas_h - 144) - n4)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, 0, 5, 5, 59, 0, 0)
            MpCanvas.draw_border_v(graphics, 0, 64, n4, 0)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, 0, (64 + n4), 5, 17, 0, 59)
            MpCanvas.draw_border_v(graphics, 0, ((64 + n4) + 17), n3, 0)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, 0, ((MpCanvas.canvas_h - 5) - 58), 5, 58, 0, 76)
            n2 = (MpCanvas.canvas_w - 5)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, n2, 5, 5, 59, 5, 0)
            MpCanvas.draw_border_v(graphics, n2, 64, n4, 5)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, n2, (64 + n4), 5, 17, 5, 59)
            MpCanvas.draw_border_v(graphics, n2, ((64 + n4) + 17), n4, 5)
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, n2, ((MpCanvas.canvas_h - 5) - 58), 5, 58, 5, 76)
        n4 = idiv(((MpCanvas.canvas_w - 120)), 2)
        n3 = ((MpCanvas.canvas_w - 120) - n4)
        Draw.draw_image_part(graphics, MpCanvas.border_h_image, 0, 0, 21, 5, 0, 0)
        MpCanvas.draw_border_h(graphics, 21, 0, n4, 0)
        Draw.draw_image_part(graphics, MpCanvas.border_h_image, (21 + n4), 0, 77, 5, 21, 0)
        MpCanvas.draw_border_h(graphics, (98 + n4), 0, n3, 0)
        Draw.draw_image_part(graphics, MpCanvas.border_h_image, (MpCanvas.canvas_w - 21), 0, 21, 5, 98, 0)
        n2 = (MpCanvas.canvas_h - 5)
        Draw.draw_image_part(graphics, MpCanvas.border_h_image, 0, n2, 37, 5, 0, 5)
        MpCanvas.draw_border_h(graphics, 37, n2, n4, 5)
        Draw.draw_image_part(graphics, MpCanvas.border_h_image, (37 + n4), n2, 45, 5, 37, 5)
        MpCanvas.draw_border_h(graphics, (82 + n4), n2, n3, 5)
        Draw.draw_image_part(graphics, MpCanvas.border_h_image, (MpCanvas.canvas_w - 37), n2, 37, 5, 82, 5)
        Draw.draw_image_part(graphics, MpCanvas.titlebox_image, (MpCanvas.center_x - 46), 0, 46, 15, 0, 0)
        Draw.draw_image_part(graphics, MpCanvas.titlebox_image, MpCanvas.center_x, 0, 46, 15, 17, 0)
        self.draw_text_colored(graphics, MpCanvas.title, idiv(MpCanvas.canvas_w, 2), 2, 1, 0xFFFFFF)

    def draw_button(self, graphics, string, n2, n3, n4, n5, bl, bl2):  # g.java:5730
        if bl:
            Draw.draw_frame(graphics, (n2 - 1), (n3 - 1), (n4 + 2), (n5 + 2), 1, 0xFFFFFF)
            Draw.draw_rect(graphics, n2, n3, n4, n5, 0xFFFFFF)
        MpCanvas.draw_panel(graphics, n2, n3, n4, n5)
        if not bl2:
            self.draw_text_centred((n2 + idiv(n4, 2)), (n3 + idiv(((n5 - 11)), 2)), string, 0x646464)
            return
        self.draw_text_centred((n2 + idiv(n4, 2)), (n3 + idiv(((n5 - 11)), 2)), string, 0xFFFFFF)

    @staticmethod
    def draw_panel(graphics, n2, n3, n4, n5):  # g.java:5743
        Draw.draw_frame(graphics, n2, n3, n4, n5, 1, 0x949694)
        Draw.fill_rect(graphics, (n2 + 1), (n3 + 1), (n4 - 2), (n5 - 2), 0)

    def draw_battle_hud(self, graphics):  # g.java:5748
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                if imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0:
                    if MpCanvas.fighter_kind[MpCanvas.loop_i] == 0:
                        self.load_numbered_image(MpCanvas.face_images, "face", MpCanvas.fighter_face[MpCanvas.loop_i])
                        MpCanvas.draw_left_half_on(graphics, 0, (0 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (MpCanvas.canvas_h - 12)), MpCanvas.face_images[MpCanvas.fighter_face[MpCanvas.loop_i]])
                        MpCanvas.face_images[MpCanvas.fighter_face[MpCanvas.loop_i]] = None
                    self.draw_box(graphics, 0, (12 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_h - 12) - 15)), 60, 15, 1)
                    if (len(MpCanvas.fighter_alt_name[MpCanvas.loop_i]) == 0) or (imod(MpCanvas.round_no, 2) == 0):
                        self.draw_text_centred_on(graphics, 30, (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), MpCanvas.fighter_name[MpCanvas.loop_i], 0xFFFFFF)
                    else:
                        self.draw_text_centred_on(graphics, 30, (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), MpCanvas.fighter_alt_name[MpCanvas.loop_i], 0xFFFFFF)
                else:
                    if MpCanvas.fighter_kind[MpCanvas.loop_i] == 0:
                        self.load_numbered_image(MpCanvas.face_images, "face", MpCanvas.fighter_face[MpCanvas.loop_i])
                        MpCanvas.draw_right_half_on(graphics, MpCanvas.canvas_w, (0 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (MpCanvas.canvas_h - 12)), MpCanvas.face_images[MpCanvas.fighter_face[MpCanvas.loop_i]])
                        MpCanvas.face_images[MpCanvas.fighter_face[MpCanvas.loop_i]] = None
                    self.draw_box(graphics, (MpCanvas.canvas_w - 60), (12 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_h - 12) - 15)), 60, 15, 1)
                    if (len(MpCanvas.fighter_alt_name[MpCanvas.loop_i]) == 0) or (imod(MpCanvas.round_no, 2) == 0):
                        self.draw_text_centred_on(graphics, (MpCanvas.canvas_w - 30), (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), MpCanvas.fighter_name[MpCanvas.loop_i], 0xFFFFFF)
                    else:
                        self.draw_text_centred_on(graphics, (MpCanvas.canvas_w - 30), (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), MpCanvas.fighter_alt_name[MpCanvas.loop_i], 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.noop()

    @staticmethod
    def draw_border_v(graphics, n2, n3, n4, n5):  # g.java:5783
        n6 = (idiv(n4, 11) + 1)
        n7 = 0
        while n7 < n6:
            Draw.draw_image_part(graphics, MpCanvas.border_v_image, n2, (n3 + (11 * n7)), 5, 11, n5, 8)
            n7 = n7 + 1

    @staticmethod
    def draw_back_tiles(graphics):  # g.java:5792
        n2 = (idiv(MpCanvas.canvas_w, MpCanvas.back_image.getWidth()) + 1)
        n3 = (idiv(MpCanvas.canvas_h, MpCanvas.back_image.getHeight()) + 1)
        n4 = 0
        while n4 < n2:
            n5 = 0
            while n5 < n3:
                if imod(n5, 2) != 0:
                    Draw.draw_image(graphics, MpCanvas.back_image, (MpCanvas.back_image.getWidth() * n4), (MpCanvas.back_image.getHeight() * n5), 0)
                else:
                    Draw.draw_image_part(graphics, MpCanvas.back_image, (MpCanvas.back_image.getWidth() * n4), (MpCanvas.back_image.getHeight() * n5), 21, 24, 31, 0)
                    Draw.draw_image_part(graphics, MpCanvas.back_image, ((MpCanvas.back_image.getWidth() * n4) + 21), (MpCanvas.back_image.getHeight() * n5), 31, 24, 0, 0)
                n5 = n5 + 1
            n4 = n4 + 1

    @staticmethod
    def draw_border_h(graphics, n2, n3, n4, n5):  # g.java:5811
        n6 = (idiv(n4, 11) + 1)
        n7 = 0
        while n7 < n6:
            Draw.draw_image_part(graphics, MpCanvas.border_h_image, (n2 + (11 * n7)), n3, 11, 5, 10, n5)
            n7 = n7 + 1

    def draw_options_bg(self, graphics):  # g.java:5820
        self.draw_window(graphics)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 3:
            self.draw_box(graphics, (MpCanvas.center_x - 58), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 19)), 61, 14, 2)
            self.draw_text_colored(graphics, Consts.option_texts[MpCanvas.loop_i], (MpCanvas.center_x - 28), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0x646464)
            self.draw_box(graphics, (MpCanvas.center_x + 13), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 19)), 39, 14, 2)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_records(self):  # g.java:5831
        self.draw_window(MpCanvas.screen_g)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 6:
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 60), ((MpCanvas.center_y - 47) + (MpCanvas.loop_i * 17)), 81, 14, 2)
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x + 23), ((MpCanvas.center_y - 47) + (MpCanvas.loop_i * 17)), 37, 14, 2)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(46 + MpCanvas.loop_i)], (MpCanvas.center_x - 19), ((MpCanvas.center_y - 45) + (MpCanvas.loop_i * 17)), 1, 0xFFFFFF)
            _sw118 = MpCanvas.loop_i
            if _sw118 == 0:
                self.draw_number1((MpCanvas.center_x + 52), ((MpCanvas.center_y - 44) + (MpCanvas.loop_i * 17)), MpCanvas.level)
            elif _sw118 == 1:
                self.draw_number1_b((MpCanvas.center_x + 52), ((MpCanvas.center_y - 44) + (MpCanvas.loop_i * 17)), MpCanvas.fame)
            elif _sw118 == 2:
                MpCanvas.stat_value = MpCanvas.duel_grade
            elif _sw118 == 3:
                MpCanvas.stat_value = MpCanvas.wins
            elif _sw118 == 4:
                MpCanvas.stat_value = MpCanvas.losses
            elif _sw118 == 5:
                MpCanvas.stat_value = MpCanvas.mission_grade
            if MpCanvas.loop_i > 1:
                self.draw_number0_b((MpCanvas.center_x + 52), ((MpCanvas.center_y - 44) + (MpCanvas.loop_i * 17)), MpCanvas.stat_value)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_attributes(self):  # g.java:5870
        self.draw_window(MpCanvas.screen_g)
        n2 = 0
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 54), ((MpCanvas.center_y - 30) + (MpCanvas.loop_i * 17)), 39, 14, 2)
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 13), ((MpCanvas.center_y - 30) + (MpCanvas.loop_i * 17)), 67, 14, 2)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(42 + MpCanvas.loop_i)], (MpCanvas.center_x - 35), ((MpCanvas.center_y - 28) + (MpCanvas.loop_i * 17)), 1, 0xFFFFFF)
            _sw119 = MpCanvas.loop_i
            if _sw119 == 0:
                MpCanvas.stat_value = MpCanvas.attr_hp
                n2 = MpCanvas.attr_hp_bonus
            elif _sw119 == 1:
                MpCanvas.stat_value = MpCanvas.attr_mp
                n2 = MpCanvas.attr_mp_bonus
            elif _sw119 == 2:
                MpCanvas.stat_value = MpCanvas.attr_attack
                n2 = MpCanvas.attr_attack_bonus
            elif _sw119 == 3:
                MpCanvas.stat_value = MpCanvas.attr_defense
                n2 = MpCanvas.attr_defense_bonus
            self.draw_number0((MpCanvas.center_x + 9), ((MpCanvas.center_y - 27) + (MpCanvas.loop_i * 17)), MpCanvas.stat_value)
            self.draw_number5((MpCanvas.center_x + 52), ((MpCanvas.center_y - 27) + (MpCanvas.loop_i * 17)), n2)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_skills_bg(self, graphics):  # g.java:5905
        self.draw_window(graphics)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 5:
            self.draw_box(graphics, (MpCanvas.center_x - 58), ((MpCanvas.center_y - 51) + (MpCanvas.loop_i * 16)), 91, 14, 2)
            self.draw_box(graphics, (MpCanvas.center_x + 43), ((MpCanvas.center_y - 51) + (MpCanvas.loop_i * 16)), 15, 14, 2)
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        self.draw_text_centred_on(graphics, (MpCanvas.center_x - 13), (MpCanvas.center_y - 49), "NAME", 0xFFFFFF)
        self.draw_text_centred_on(graphics, (MpCanvas.center_x + 51), (MpCanvas.center_y - 49), "LV", 0xFFFFFF)
        MpCanvas.fill_rect_on(graphics, (MpCanvas.center_x - 52), (MpCanvas.center_y + 31), 104, 27, 0)
        MpCanvas.draw_line_color(graphics, (MpCanvas.center_x - 52), (MpCanvas.center_y + 30), (MpCanvas.center_x + 51), (MpCanvas.center_y + 30), 0x804000)
        MpCanvas.draw_line_color(graphics, (MpCanvas.center_x - 52), (MpCanvas.center_y + 58), (MpCanvas.center_x + 51), (MpCanvas.center_y + 58), 0x804000)
        MpCanvas.draw_line_color(graphics, (MpCanvas.center_x - 53), (MpCanvas.center_y + 31), (MpCanvas.center_x - 53), (MpCanvas.center_y + 57), 0x804000)
        MpCanvas.draw_line_color(graphics, (MpCanvas.center_x + 52), (MpCanvas.center_y + 31), (MpCanvas.center_x + 52), (MpCanvas.center_y + 57), 0x804000)

    def draw_skill_slots(self):  # g.java:5922
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                if imod(MpCanvas.state_ticks, 4) < 2:
                    MpCanvas.draw_left_half((MpCanvas.center_x - 65), ((MpCanvas.center_y - 32) + (MpCanvas.loop_i * 16)), MpCanvas.arrow_images[1])
                    MpCanvas.draw_right_half((MpCanvas.center_x + 40), ((MpCanvas.center_y - 32) + (MpCanvas.loop_i * 16)), MpCanvas.arrow_images[1])
                self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 58), ((MpCanvas.center_y - 35) + (MpCanvas.loop_i * 16)), 91, 14, 3)
                self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x + 43), ((MpCanvas.center_y - 35) + (MpCanvas.loop_i * 16)), 15, 14, 3)
            if MpCanvas.skill_levels[(MpCanvas.skill_order[MpCanvas.loop_i] - 3)] == 99:
                self.draw_text_centred_on(MpCanvas.screen_g, (MpCanvas.center_x - 12), ((MpCanvas.center_y - 33) + (MpCanvas.loop_i * 16)), Consts.skill_names[(MpCanvas.skill_order[MpCanvas.loop_i] - 3)], 0x646464)
                if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                    self.draw_text_left((MpCanvas.center_x - 50), (MpCanvas.center_y + 32), Consts.texts[34], 0x646464)
            else:
                self.draw_text_centred_on(MpCanvas.screen_g, (MpCanvas.center_x - 12), ((MpCanvas.center_y - 33) + (MpCanvas.loop_i * 16)), Consts.skill_names[(MpCanvas.skill_order[MpCanvas.loop_i] - 3)], 0xFFFFFF)
                self.draw_number1((MpCanvas.center_x + 48), ((MpCanvas.center_y - 32) + (MpCanvas.loop_i * 16)), MpCanvas.skill_levels[(MpCanvas.skill_order[MpCanvas.loop_i] - 3)])
                if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                    self.draw_text_left((MpCanvas.center_x - 50), (MpCanvas.center_y + 32), Consts.skill_info[(((MpCanvas.skill_order[MpCanvas.loop_i] - 3)) * 2)], 0xFFFFFF)
                    self.draw_text_left((MpCanvas.center_x - 50), (MpCanvas.center_y + 45), Consts.skill_info[((((MpCanvas.skill_order[MpCanvas.loop_i] - 3)) * 2) + 1)], 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_exp_fame_gold(self):  # g.java:5950
        self.draw_window(MpCanvas.screen_g)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 3:
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 50), ((MpCanvas.center_y - 45) + (MpCanvas.loop_i * 34)), 100, 14, 2)
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 50), ((MpCanvas.center_y - 32) + (MpCanvas.loop_i * 34)), 100, 14, 2)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(52 + MpCanvas.loop_i)], MpCanvas.center_x, ((MpCanvas.center_y - 43) + (MpCanvas.loop_i * 34)), 1, 0xFFFFFF)
            _sw120 = MpCanvas.loop_i
            if _sw120 == 0:
                MpCanvas.stat_value = MpCanvas.exp
            elif _sw120 == 1:
                MpCanvas.stat_value = MpCanvas.fame
            elif _sw120 == 2:
                MpCanvas.stat_value = MpCanvas.gold
            self.draw_number0_b((MpCanvas.center_x + 24), ((MpCanvas.center_y - 29) + (MpCanvas.loop_i * 34)), MpCanvas.stat_value)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_quote_bg(self, graphics):  # g.java:5975
        self.draw_window(graphics)
        self.draw_box(graphics, (MpCanvas.center_x - 62), (MpCanvas.center_y + 7), 126, 16, 6)

    def draw_quote_prompt(self, graphics):  # g.java:5980
        string = MpCanvas.input_text
        self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 44), _js(_js(Consts.texts[58], "."), ((MpCanvas.quote_step + 1))), 16400640)
        if MpCanvas.quote_step == 0:
            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 32), Consts.texts[23], 0xFFFFFF)
            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 20), Consts.texts[24], 0xFFFFFF)
        else:
            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 32), Consts.texts[15], 0xFFFFFF)
            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 20), Consts.texts[16], 0xFFFFFF)
        self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 8), Consts.texts[25], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y + 9), string, 0x41FF41)
        if imod(MpCanvas.state_ticks, 4) < 2:
            n2 = MpCanvas.font_white.string_width(string)
            if len(string) == 20:
                n2 = (n2 - (MpCanvas.font_white.string_width("A") * 2))
            MpCanvas.draw_line_color(graphics, (MpCanvas.center_x + idiv(n2, 2)), (MpCanvas.center_y + 20), ((MpCanvas.center_x + idiv(n2, 2)) + 4), (MpCanvas.center_y + 20), 0xFFFFFF)
        MpCanvas.draw_letter_grid_space(MpCanvas.letter_cursor, (MpCanvas.center_y + 27))

    @staticmethod
    def draw_letter_grid(n2, n3):  # g.java:6002
        n4 = (MpCanvas.center_x - 57)
        stringArray = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "OK"]
        Gfx.fill_rect(n4, n3, 115, 22, 0)
        Gfx.fill_rect((n4 + 99), (n3 + 12), 13, 9, 255)
        if imod(MpCanvas.state_ticks, 4) < 2:
            if n2 == 26:
                Gfx.fill_rect((n4 + 99), (n3 + 12), 13, 9, 0xFF0000)
            else:
                Gfx.fill_rect(((n4 + 2) + (imod(n2, 14) * 8)), ((n3 + 1) + (11 * (idiv(n2, 14)))), 7, 9, 0xFF0000)
        Gfx.set_font(MpCanvas.font_white)
        n5 = 0
        while n5 < len(stringArray):
            n6 = (1 if (n5 == 8) else ((1 if (n5 == 26) else 0)))
            Gfx.draw_string(stringArray[n5], (((n4 + 3) + (imod(n5, 14) * 8)) + n6), (n3 + (11 * (idiv(n5, 14)))), 0)
            n5 = n5 + 1

    @staticmethod
    def letter_grid_keys(n2):  # g.java:6023
        n3 = n2
        if ((n2 != (-7)) and (n2 != (-5))) and (n2 != (-6)):
            if n2 == (-1):
                MpCanvas.letter_cursor = imod((((MpCanvas.letter_cursor + 28) - 14)), 28)
            elif n2 == (-2):
                MpCanvas.letter_cursor = imod((((MpCanvas.letter_cursor + 28) + 14)), 28)
            elif n2 == (-3):
                MpCanvas.letter_cursor = imod((((MpCanvas.letter_cursor + 28) - 1)), 28)
            elif (n2 == (-4)) and ((_set(MpCanvas, 'letter_cursor', imod((((MpCanvas.letter_cursor + 28) + 1)), 28))) == 27):
                MpCanvas.letter_cursor = 0
        if MpCanvas.letter_cursor == 27:
            MpCanvas.letter_cursor = 26
        return n3

    @staticmethod
    def draw_letter_grid_space(n2, n3):  # g.java:6042
        n4 = (MpCanvas.center_x - 60)
        stringArray = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " ", "OK"]
        Gfx.fill_rect(n4, n3, 120, 22, 0)
        Gfx.fill_rect((n4 + 99), (n3 + 13), 5, 7, 0x666666)
        Gfx.fill_rect((n4 + 106), (n3 + 12), 13, 9, 255)
        if imod(MpCanvas.state_ticks, 4) < 2:
            if n2 == 27:
                Gfx.fill_rect((n4 + 106), (n3 + 12), 13, 9, 0xFF0000)
            else:
                Gfx.fill_rect(((n4 + 2) + (imod(n2, 14) * 8)), ((n3 + 1) + (11 * (idiv(n2, 14)))), 7, 9, 0xFF0000)
        Gfx.set_font(MpCanvas.font_white)
        n5 = 0
        while n5 < len(stringArray):
            n6 = (1 if (n5 == 8) else ((1 if (n5 == 26) else 0)))
            Gfx.draw_string(stringArray[n5], (((n4 + 3) + (imod(n5, 14) * 8)) + n6), (n3 + (11 * (idiv(n5, 14)))), 0)
            n5 = n5 + 1

    @staticmethod
    def letter_grid_space_keys(n2):  # g.java:6064
        n3 = n2
        if ((n2 != (-7)) and (n2 != (-5))) and (n2 != (-6)):
            if n2 == (-1):
                MpCanvas.letter_cursor = imod((((MpCanvas.letter_cursor + 28) - 14)), 28)
            elif n2 == (-2):
                MpCanvas.letter_cursor = imod((((MpCanvas.letter_cursor + 28) + 14)), 28)
            elif n2 == (-3):
                MpCanvas.letter_cursor = imod((((MpCanvas.letter_cursor + 28) - 1)), 28)
            elif n2 == (-4):
                MpCanvas.letter_cursor = imod((((MpCanvas.letter_cursor + 28) + 1)), 28)
        return n3

    @staticmethod
    def trim_right(string):  # g.java:6080
        n2 = len(string)
        n3 = (n2 - 1)
        while n3 >= 0:
            if ord(string[n3]) != 32:
                break
            n3 = n3 - 1
        if n3 == 0:
            return ""
        return string[0:(n3 + 1)]

    def draw_name_prompt(self, graphics):  # g.java:6093
        self.draw_window(graphics)
        self.draw_box(graphics, (MpCanvas.center_x - 62), (MpCanvas.center_y + 7), 126, 16, 6)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 32), Consts.input_prompts[0], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 20), Consts.input_prompts[1], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 8), Consts.input_prompts[2], 0xFFFFFF)

    def draw_input_line(self, graphics):  # g.java:6101
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y + 9), MpCanvas.input_text, 0x41FF41)
        if imod(MpCanvas.state_ticks, 4) < 2:
            n2 = MpCanvas.font_white.string_width(MpCanvas.input_text)
            if len(MpCanvas.input_text) == 8:
                n2 = (n2 - (MpCanvas.font_white.string_width("A") * 2))
            MpCanvas.draw_line_color(graphics, (MpCanvas.center_x + idiv(n2, 2)), (MpCanvas.center_y + 20), ((MpCanvas.center_x + idiv(n2, 2)) + 4), (MpCanvas.center_y + 20), 0xFFFFFF)
        MpCanvas.draw_letter_grid(MpCanvas.letter_cursor, (MpCanvas.center_y + 27))

    def draw_name_confirm(self, graphics):  # g.java:6113
        self.draw_box(graphics, (MpCanvas.center_x - 60), ((MpCanvas.center_y - 35) - 5), 120, 94, 5)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 32), Consts.input_prompts[3], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 20), Consts.input_prompts[4], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 8), Consts.input_prompts[5], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y + 8), MpCanvas.input_text, 0x41FF41)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 2:
            self.draw_box(graphics, ((MpCanvas.center_x - 42) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 35), 29, 14, 2)
            self.draw_text_colored(graphics, Consts.texts[(40 + MpCanvas.loop_i)], ((MpCanvas.center_x - 28) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 38), 1, 0x646464)
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                self.draw_text_colored(graphics, Consts.texts[(40 + MpCanvas.loop_i)], ((MpCanvas.center_x - 28) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 38), 1, 0xFFFFFF)
                self.draw_box(graphics, ((MpCanvas.center_x - 42) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 35), 29, 14, 3)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_exit_confirm(self, graphics):  # g.java:6131
        self.draw_box(graphics, (MpCanvas.center_x - 53), (MpCanvas.center_y - 34), 106, 68, 5)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 22), Consts.texts[56], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 7), Consts.texts[57], 0xFFFFFF)
        n2 = 0
        while n2 < 2:
            self.draw_box(graphics, ((MpCanvas.center_x - 42) + (n2 * 55)), (MpCanvas.center_y + 15), 29, 14, (3 if (MpCanvas.popup_cursor == n2) else 2))
            self.draw_text_colored(graphics, Consts.texts[(40 + n2)], ((MpCanvas.center_x - 27) + (n2 * 55)), (MpCanvas.center_y + 17), 1, (0xFFFFFF if (MpCanvas.popup_cursor == n2) else 0x646464))
            n2 = n2 + 1

    def draw_error(self):  # g.java:6143
        MpCanvas.msg_first_line = 0
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < MpCanvas.error_msg:
            MpCanvas.msg_first_line = (MpCanvas.msg_first_line + Consts.error_line_counts[MpCanvas.loop_i])
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.tmp = 0
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < Consts.error_line_counts[MpCanvas.error_msg]:
            MpCanvas.msg_copy_line = True
            if MpCanvas.msg_copy_line:
                MpCanvas.text_lines[MpCanvas.loop_i] = Consts.error_lines[(MpCanvas.msg_first_line + MpCanvas.loop_i)]
            if MpCanvas.tmp < len(MpCanvas.text_lines[MpCanvas.loop_i]):
                MpCanvas.tmp = len(MpCanvas.text_lines[MpCanvas.loop_i])
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.loop_j = 0
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, (MpCanvas.tmp * 7), (((((Consts.error_line_counts[MpCanvas.error_msg] + 1)) * 15) + MpCanvas.loop_j) + 4), 0)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < Consts.error_line_counts[MpCanvas.error_msg]:
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((((MpCanvas.center_y - idiv((Consts.error_line_counts[MpCanvas.error_msg] * 15), 2)) + (MpCanvas.loop_i * 15)) - 4) - idiv(MpCanvas.loop_j, 3)), MpCanvas.text_lines[MpCanvas.loop_i], 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        self.draw_ok_button(((MpCanvas.center_y + idiv((Consts.error_line_counts[MpCanvas.error_msg] * 15), 2)) - 5))

    def draw_challenge_bg(self, graphics):  # g.java:6172
        self.draw_window(graphics)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 2:
            self.draw_box(graphics, (MpCanvas.center_x - 56), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 20)), 111, 14, 2)
            self.draw_text_colored(graphics, Consts.texts[(38 + MpCanvas.loop_i)], idiv(MpCanvas.screen_w, 2), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 20)), 1, 0x646464)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def draw_user_id_prompt(self, graphics, n2):  # g.java:6182
        self.draw_window(graphics)
        n3 = 0
        while n3 < 5:
            self.draw_text_centred_on(graphics, MpCanvas.center_x, (n2 + (12 * n3)), Consts.input_prompts[(((6 if (MpCanvas.room_mode == 0) else 12)) + n3)], 0xFFFFFF)
            n3 = n3 + 1
        self.draw_box(graphics, (MpCanvas.center_x - 40), (n2 + 59), 80, 15, 6)

    def draw_loading(self):  # g.java:6192
        string = ""
        if imod(MpCanvas.state_ticks, 4) == 1:
            string = "."
        elif imod(MpCanvas.state_ticks, 4) == 2:
            string = ".."
        elif imod(MpCanvas.state_ticks, 4) == 3:
            string = "..."
        n2 = (MpCanvas.font_white.string_width(Consts.loading_texts[MpCanvas.loading_msg]) + 14)
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, (n2 + 22), 30, 0)
        self.draw_text_left_on(MpCanvas.screen_g, (MpCanvas.center_x - idiv(n2, 2)), ((MpCanvas.center_y - 7) + 2), _js(Consts.loading_texts[MpCanvas.loading_msg], string), 0xFFFFFF)

    def draw_waiting(self):  # g.java:6206
        string = ""
        if imod(MpCanvas.state_ticks, 4) == 1:
            string = "."
        elif imod(MpCanvas.state_ticks, 4) == 2:
            string = ".."
        elif imod(MpCanvas.state_ticks, 4) == 3:
            string = "..."
        n2 = (MpCanvas.font_white.string_width(Consts.texts[7]) + 14)
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, (n2 + 22), 30, 0)
        self.draw_text_left_on(MpCanvas.screen_g, (MpCanvas.center_x - idiv(n2, 2)), (MpCanvas.center_y - 6), _js(Consts.texts[7], string), 0xFFFFFF)

    def draw_softkeys(self, n2, n3):  # g.java:6220
        if n2 != (-1):
            MpCanvas.draw_image_on(MpCanvas.screen_g, 0, (MpCanvas.screen_h - 11), MpCanvas.softkey_image)
            self.draw_text_centred_on(MpCanvas.screen_g, 28, (MpCanvas.screen_h - 11), Consts.softkeys[n2], 0xFFFFFF)
        if n3 != (-1):
            MpCanvas.draw_image_on(MpCanvas.screen_g, (MpCanvas.screen_w - 57), (MpCanvas.screen_h - 11), MpCanvas.softkey_image)
            self.draw_text_centred_on(MpCanvas.screen_g, (MpCanvas.screen_w - 28), (MpCanvas.screen_h - 11), Consts.softkeys[n3], 0xFFFFFF)

    def draw_ok_button(self, n2):  # g.java:6231
        self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 10), (n2 + 1), 18, 9, 3)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, n2, Consts.softkeys[0], 0xFFFFFF)

    def start_music(self, n2):  # g.java:6236
        MpCanvas.queue_music(n2)

    def start_sound(self, n2):  # g.java:6240
        MpCanvas.queue_music(n2)

    @staticmethod
    def queue_music(n2):  # g.java:6244
        if MpCanvas.game is not None:
            MpGame.request_music(n2)

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


def _static_init():
    MpCanvas.title = ""
    MpCanvas.timer_ticks = 0
    MpCanvas.screen_g = None
    MpCanvas.rng = Random()
    MpCanvas.menu_size = 7
    MpCanvas.key = (-999)
    MpCanvas.font_white = None
    MpCanvas.font_orange = None
    MpCanvas.font_gray = None
    MpCanvas.font_green = None
    MpCanvas.wait_started = False
    MpCanvas.painting_blocked = False
    MpCanvas.popup_shown = False
    MpCanvas.exit_prompt = False
    MpCanvas.pause_request = 0
    MpCanvas.music_to_resume = (-1)
    MpCanvas.paused = False
    MpCanvas.loop_started = False
    MpCanvas.connecting = False
    MpCanvas.room_dirty = True
    MpCanvas.relogin_to_menu = True
    MpCanvas.rank_names = [None] * (3)
    MpCanvas.rank_ranks = [0] * (3)
    MpCanvas.rank_values = [0] * (3)
    MpCanvas.my_ranks = [0, 0, 0, 0]
    MpCanvas.volume = 4
    MpCanvas.speed = 1
    MpCanvas.invitation_saved = 1
    MpCanvas.card_half = True
    MpCanvas.skill_slots = [0] * (4)
    MpCanvas.notice_lines = [None] * (4)
    MpCanvas.fighter_name = [None] * (4)
    MpCanvas.fighter_quote_start = [None] * (4)
    MpCanvas.fighter_quote_win = [None] * (4)
    MpCanvas.fighter_alt_name = [None] * (4)
    MpCanvas.fighter_present = [False] * (4)
    MpCanvas.fighter_slot = [0] * (4)
    MpCanvas.fighter_level = [0] * (4)
    MpCanvas.fighter_wins = [0] * (4)
    MpCanvas.fighter_losses = [0] * (4)
    MpCanvas.fighter_max_hp = [0] * (4)
    MpCanvas.fighter_hp = [0] * (4)
    MpCanvas.fighter_mp = [0] * (4)
    MpCanvas.fighter_weapon = [0] * (4)
    MpCanvas.fighter_face = [0] * (4)
    MpCanvas.fighter_kind = [0] * (4)
    MpCanvas.turn_actions = [0] * (4)
    MpCanvas.fighter_anim = [0] * (4)
    MpCanvas.fighter_anim_tick = [0] * (4)
    MpCanvas.fighter_anim_len = [0] * (4)
    MpCanvas.fighter_hp_target = [0] * (4)
    MpCanvas.fighter_mp_target = [0] * (4)
    MpCanvas.fighter_hp_step = [0] * (4)
    MpCanvas.fighter_mp_step = [0] * (4)
    MpCanvas.fighter_hp_delta = [0] * (4)
    MpCanvas.fighter_x = [0] * (4)
    MpCanvas.fighter_y = [0] * (4)
    MpCanvas.fighter_fx_frame = [0] * (4)
    MpCanvas.fighter_frame = [0] * (4)
    MpCanvas.fighter_blink = [0] * (4)
    MpCanvas.fighter_status = [0] * (4)
    MpCanvas.fighter_status_ticks = [0] * (4)
    MpCanvas.fighter_cr = [0] * (4)
    MpCanvas.skill_order = [0] * (4)
    MpCanvas.skill_levels = [0] * (11)
    MpCanvas.skill_costs = [0] * (11)
    MpCanvas.turn_hps = [0] * (12)
    MpCanvas.turn_bytes = [0] * (44)
    MpCanvas.tick_ms = 100
    MpCanvas.mpic_images = [None] * (6)
    MpCanvas.face_images = [None] * (4)
    MpCanvas.ui_images = [None] * (57)
    MpCanvas.act_images = [None] * (18)
    MpCanvas.number_images = [None] * (8)
    MpCanvas.arrow_images = [None] * (2)
    MpCanvas.bg_images = [None] * (22)
    MpCanvas.body_images = [None] * (2)
    MpCanvas.body_frames = [None] * (3)
    MpCanvas.head_images = [[None] * (2) for _ in range(10)]
    MpCanvas.head_frames = [[None] * (3) for _ in range(10)]
    MpCanvas.weapon_images = [[None] * (2) for _ in range(2)]
    MpCanvas.weapon_frames = [[None] * (3) for _ in range(2)]
    MpCanvas.sword_images = [[None] * (2) for _ in range(2)]
    MpCanvas.sword_frames = [[None] * (3) for _ in range(2)]
    MpCanvas.effect_images = [[None] * (2) for _ in range(2)]
    MpCanvas.effect_frames = [[None] * (3) for _ in range(2)]
    MpCanvas.effect3_frames = [None] * (1)
    MpCanvas.shadow_images = [None] * (2)
    MpCanvas.shadow_frames = [None] * (3)
    MpCanvas.monster_images = [None] * (2)
    MpCanvas.monster_frames = [None] * (1)
    MpCanvas.mon_weapon_images = [None] * (2)
    MpCanvas.mon_weapon_frames = [None] * (1)
    MpCanvas.mon_effect_images = [None] * (2)
    MpCanvas.mon_effect_frames = [None] * (1)
    MpCanvas.mon_sword_images = [None] * (2)
    MpCanvas.mon_sword_frames = [None] * (1)
    MpCanvas.cursor_stack = [0] * (10)
    MpCanvas.state_stack = [0] * (10)
    MpCanvas.stack_depth = 0
    MpCanvas.relogin = False
    MpCanvas.painted = True
    MpCanvas.ping_misses = 0
    MpCanvas.disconnecting = False
    MpCanvas.ping_off = False
    MpCanvas.pending_state = (-1)
    MpCanvas.text_lines = [None] * (10)


def _late_imports():
    global SpriteFrames, PlayerPool, NetThread, ResReader, Consts, Draw, Gfx, Font, Answer, FrameWriter, FrameReader, MpGame
    from pow_mp.sprite_frames import SpriteFrames
    from pow_mp.player_pool import PlayerPool
    from pow_mp.net_thread import NetThread
    from pow_mp.res_reader import ResReader
    from pow_mp.consts import Consts
    from pow_mp.draw import Draw
    from pow_mp.gfx import Gfx
    from pow_mp.font import Font
    from pow_mp.answer import Answer
    from pow_mp.frame_writer import FrameWriter
    from pow_mp.frame_reader import FrameReader
    from pow_mp.mp_game import MpGame
