"""MpCanvas (g.java): the canvas of the MP jar - screens, menus, battles.

Generated once from pyport/mp_java/g.java (branch java-reference) by the old
tools/j2py_mp.py; edited by hand since.
"""
import config
from pow_mp import (
    mp_canvas_assets,
    mp_canvas_battle,
    mp_canvas_chat,
    mp_canvas_draw,
    mp_canvas_input,
    mp_canvas_net,
    mp_canvas_options,
    mp_canvas_order,
    mp_canvas_screens,
)
from pow_mp.mp_canvas_assets import AssetsMixin
from pow_mp.mp_canvas_battle import BattleMixin
from pow_mp.mp_canvas_chat import ChatMixin
from pow_mp.mp_canvas_draw import DrawMixin
from pow_mp.mp_canvas_input import InputMixin
from pow_mp.mp_canvas_net import NetMixin
from pow_mp.mp_canvas_options import OptionsMixin
from pow_mp.mp_canvas_order import OrderMixin
from pow_mp.mp_canvas_screens import ScreensMixin
from pow_mp.rt import (
    Image,
    Random,
    _Canvas,
    _inc,
    _js,
    _set,
    i32,
    idiv,
    imod,
    system,
)


class MpCanvas(DrawMixin, BattleMixin, NetMixin, InputMixin, ScreensMixin, AssetsMixin, OptionsMixin,
               OrderMixin, ChatMixin, _Canvas):
    # PORT-EXTRA auto-battle: Tab (key -100) turns it on / off; the round's 1027 then goes out after
    # a second with action AUTO_ACTION, and the server's bot chooses (pow_server/battle.py cpu_choice)
    auto_battle = config.AUTO_HUNT
    sound_from_sp = None   # PORT-EXTRA: the single player's sound answer (mp_main.play), None = ask
    embedded = False       # PORT-EXTRA: a part of the single player (main.py): BACK in the main
                           # menu leaves at once, no exit popup, no outro picture
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
    sp_account = False  # PORT-EXTRA: user_id / password are the single player's (use_sp_account)
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
        self.text_input = self.chat_text_key   # PORT-EXTRA: a PC keyboard types into the chat
        MpCanvas.midlet = main
        self.setFullScreenMode(True)

    @staticmethod
    def log(text):  # g.java:291
        print(_js(text))

    def init_screen(self):  # g.java:300
        MpCanvas.state_stack[0] = 1
        width = self.getWidth()
        MpCanvas.canvas_w = width
        MpCanvas.screen_w = width
        height = self.getHeight()
        MpCanvas.canvas_h = height
        MpCanvas.screen_h = height
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
        i = 0
        while i < 4:
            MpCanvas.fighter_alt_name[i] = ""
            i = i + 1
        MpCanvas.font_white = Font("/0_font.png", 5, 11, 6, 0xFFFFFF)
        MpCanvas.font_orange = Font("/0_font.png", 5, 11, 6, 16400640)
        MpCanvas.font_gray = Font("/0_font.png", 5, 11, 6, 0x646464)
        MpCanvas.font_green = Font("/0_font.png", 5, 11, 6, 0x41FF41)
        self.load_ui_images()
        self.load_options()
        self.use_sp_account()           # PORT-EXTRA: the single player's account, no Login screen
        MpCanvas.game = MpGame(MpCanvas.midlet)
        MpCanvas.noop()
        MpCanvas.set_state(0)

    def paint(self, graphics):  # g.java:364
        MpCanvas.screen_g = graphics
        Gfx.set_graphics(graphics)
        if MpCanvas.painting_blocked:
            MpCanvas.painted = True
            return
        self.paint_screen()
        if 94 <= MpCanvas.state <= 98 and (MpCanvas.auto_battle or config.AUTO_BUTTON):
            # PORT-EXTRA auto-battle button: orange AUTO = on, white with the keys = off (Tab / F / R3)
            if MpCanvas.auto_battle:
                self.draw_text_left_on(graphics, 4, MpCanvas.canvas_h - 30, "AUTO", 16400640)
            else:
                self.draw_text_left_on(graphics, 4, MpCanvas.canvas_h - 30, "AUTO: Tab/F", 0xFFFFFF)
        if graphics.getClipX() > 0:
            graphics.setClip(0, 0, MpCanvas.canvas_w, MpCanvas.canvas_h)
        MpCanvas.painted = True

    @staticmethod
    def sleep(ms):  # g.java:378
        if ms > 0:
            try:
                system.sleep(ms)
            except Exception:
                pass

    @staticmethod
    def request_pause(kind):  # g.java:388
        MpCanvas.pause_request = kind

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
                wait_ms = 0
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
                if (wait_ms := (Consts.speed_frame_ms[MpCanvas.speed] - i32((system.currentTimeMillis()) - MpCanvas.frame_start))) > 20:
                    MpCanvas.sleep(wait_ms)
                else:
                    MpCanvas.sleep(20)
            self.apply_pause()
            MpCanvas.loop_started = True

    def paint_screen(self):  # g.java:474
        if MpCanvas.painted:
            return
        if MpCanvas.state not in {3, 10000}:
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
                if _inc(MpCanvas, "ping_misses", 1) > 20:
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
                    if (_set(MpCanvas, "bar_x", (MpCanvas.bar_x + MpCanvas.bar_speed))) > (((MpCanvas.center_x - 44) + 72) + MpCanvas.bar_speed):
                        MpCanvas.bar_x = (((MpCanvas.center_x - 44) + 72) + MpCanvas.bar_speed)
                    else:
                        MpCanvas.set_timer(1)
                else:
                    if _inc(MpCanvas, "choose_secs", -1) == 0:
                        # PORT-EXTRA: on auto-battle the time-out sends AUTO instead of Defend
                        MpCanvas.chosen_action = MpCanvas.AUTO_ACTION if MpCanvas.auto_battle else 1
                        MpCanvas.bar_x = (((MpCanvas.center_x - 44) + 72) + MpCanvas.bar_speed)
                        self.stop_timing()
                    MpCanvas.set_timer(10 - MpCanvas.speed)
            elif MpCanvas.timer_ticks > 0:
                MpCanvas.timer_ticks = MpCanvas.timer_ticks - 1
        MpCanvas.prev_state = MpCanvas.state
        handler = self._PAINT_BY_STATE.get(MpCanvas.state)
        if handler is not None:
            handler(self)

    def _paint_logo(self):  # state 0
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
        if config.NO_GAMEVIL:  # PORT-EXTRA: no Gamevil logo screen (rebrand.py)
            MpCanvas.logo_time = 0
        else:
            Draw.draw_image(MpCanvas.screen_g, MpCanvas.logo_image, idiv(MpCanvas.canvas_w, 2), MpCanvas.logo_y, 17)
        if MpCanvas.sound_from_sp is not None:
            # PORT-EXTRA: started from the single player's Main Menu (mp_main.play): it already
            # showed the logo and asked about the sound, so its answer goes straight on
            MpCanvas.logo_image = None
            self.answer_sound_prompt(MpCanvas.sound_from_sp)
            return
        if (system.currentTimeMillis() - MpCanvas.logo_time) <= 3000:
            return
        MpCanvas.logo_image = None
        MpCanvas.state = 5

    def _paint_ranking_menu(self):  # state 161
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = Consts.main_menu[5]
            MpCanvas.menu_size = 3
            self.draw_menu_icons()
        self.draw_buffer()
        self.draw_button(MpCanvas.screen_g, Consts.rank_menu[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 43), (MpCanvas.center_y - 19), 86, 17, False, True)
        MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
        self.draw_softkeys((-1), 1)

    def _paint_my_rank(self):  # state 162/163/164
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
            if MpCanvas.state == 162:
                rank_label = Consts.rank_menu[0]
            else:
                rank_label = Consts.texts[3]
            MpCanvas.draw_panel(MpCanvas.buffer_g, MpCanvas.box_x, ((MpCanvas.center_y + 28) - 54), 96, 15)
            self.draw_text_colored(MpCanvas.buffer_g, rank_label, (MpCanvas.box_x + 3), (((MpCanvas.center_y + 28) + 2) - 54), 0, 0xFFFFFF)
            MpCanvas.draw_number(MpCanvas.buffer_g, ((MpCanvas.box_x + 96) - 7), (((MpCanvas.center_y + 28) + 3) - 54), MpCanvas.my_rank_value, 0)
        self.draw_buffer()
        self.draw_button(MpCanvas.screen_g, Consts.rank_view_menu[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 43), ((MpCanvas.center_y - 19) + 15), 86, 17, False, True)
        MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
        self.draw_softkeys((-1), 1)

    def _paint_rank_list(self):  # state 170/171
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = Consts.rank_view_menu[(MpCanvas.state - 170)]
            self.draw_window_bg(MpCanvas.buffer_g)
            panel_x = ((MpCanvas.canvas_w - 110) >> 1)
            mid_y = (MpCanvas.canvas_h >> 1)
            if MpCanvas.rank_list_state == 162:
                value_label = Consts.rank_menu[0]
            elif MpCanvas.rank_list_state == 163:
                value_label = Consts.texts[3]
            else:
                value_label = Consts.texts[3]
            i = 0
            while i < 3:
                self.draw_text_colored(MpCanvas.buffer_g, MpCanvas.rank_names[i], MpCanvas.center_x, ((mid_y - 65) + (45 * i)), 1, 0xFFFFFF)
                MpCanvas.draw_panel(MpCanvas.buffer_g, panel_x, ((mid_y - 52) + (45 * i)), 110, 15)
                MpCanvas.draw_panel(MpCanvas.buffer_g, panel_x, ((mid_y - 38) + (45 * i)), 110, 15)
                self.draw_text_colored(MpCanvas.buffer_g, Consts.texts[4], (panel_x + 3), (((mid_y - 52) + 2) + (45 * i)), 0, 0xFFFFFF)
                MpCanvas.draw_number(MpCanvas.buffer_g, ((panel_x + 110) - 7), ((((mid_y - 52) + 2) + 1) + (45 * i)), MpCanvas.rank_ranks[i], 0)
                self.draw_text_colored(MpCanvas.buffer_g, value_label, (panel_x + 3), (((mid_y - 38) + 2) + (45 * i)), 0, 0xFFFFFF)
                MpCanvas.draw_number(MpCanvas.buffer_g, ((panel_x + 110) - 7), ((((mid_y - 38) + 2) + 1) + (45 * i)), MpCanvas.rank_values[i], 0)
                i = i + 1
        self.draw_buffer()
        self.draw_softkeys((-1), 1)

    def _paint_waiting_room(self):  # state 90
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
            return
        self.draw_waiting()

    def _paint_stage_intro(self):  # state 91
        self.draw_buffer()
        self.draw_fighters(MpCanvas.screen_g)
        self.draw_stage_intro()
        if MpCanvas.state_ticks != idiv(1500, MpCanvas.tick_ms):
            return
        self.send_request(1038)

    def _paint_start_quotes(self):  # state 92
        MpCanvas.state_ticks = max(MpCanvas.state_ticks, 2)
        self.draw_buffer()
        self.draw_fighters(MpCanvas.screen_g)
        if (MpCanvas.state_ticks >= idiv(500, MpCanvas.tick_ms)) and (MpCanvas.state_ticks < idiv(1500, MpCanvas.tick_ms)):
            self.draw_quotes(MpCanvas.screen_g, 0)
        elif MpCanvas.state_ticks >= idiv(1500, MpCanvas.tick_ms):
            self.draw_quotes(MpCanvas.screen_g, 1)
        if MpCanvas.state_ticks != idiv(2500, MpCanvas.tick_ms):
            return
        MpCanvas.round_no = 0
        MpCanvas.set_state(93)

    def _paint_round_start(self):  # state 93
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

    def _paint_choose_action(self):  # state 94
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
            secs_left = i32(15 - idiv(((system.currentTimeMillis() - MpCanvas.exit_prompt_time)), 1000))
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) + 30), _js(Consts.texts[63], "   "), 0xFFFFFF)
            self.draw_text_centred_on(MpCanvas.screen_g, (MpCanvas.center_x + 35), ((MpCanvas.center_y - 21) + 30), _js("", secs_left), 16400640)
            i_btn = 0
            while i_btn < 2:
                if MpCanvas.exit_cursor == i_btn:
                    self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(40 + i_btn)], ((MpCanvas.center_x - 28) + (i_btn * 55)), (MpCanvas.center_y + 28), 1, 0xFFFFFF)
                    self.draw_box(MpCanvas.screen_g, ((MpCanvas.center_x - 42) + (i_btn * 55)), (MpCanvas.center_y + 25), 29, 14, 3)
                else:
                    self.draw_box(MpCanvas.screen_g, ((MpCanvas.center_x - 42) + (i_btn * 55)), (MpCanvas.center_y + 25), 29, 14, 2)
                    self.draw_text_colored(MpCanvas.screen_g, Consts.texts[(40 + i_btn)], ((MpCanvas.center_x - 28) + (i_btn * 55)), (MpCanvas.center_y + 28), 1, 0x646464)
                i_btn = i_btn + 1
            if secs_left > 0:
                return
            MpCanvas.exit_prompt = False
            return
        self.draw_fighters(MpCanvas.screen_g)
        MpCanvas.draw_action_pad(MpCanvas.screen_g)
        self.draw_battle_prompt(MpCanvas.screen_g, 0)

    def _paint_skill_list(self):  # state 95
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.skill_cursor = 0
        self.draw_buffer()
        self.draw_fighters(MpCanvas.screen_g)
        self.draw_skill_menu(MpCanvas.screen_g)
        self.draw_battle_prompt(MpCanvas.screen_g, 1)

    def _paint_choose_target(self):  # state 96
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            while True:
                if MpCanvas.chosen_action in (9, 10):
                    MpCanvas.target_cursor = 0
                    if MpCanvas.allies_alive > 1:
                        break
                    self.start_timing()
                    return
                if MpCanvas.chosen_action in (0, 3, 4, 5, 6, 7):
                    MpCanvas.loop_i = 1
                    while MpCanvas.loop_i < 4:
                        if MpCanvas.fighter_present[MpCanvas.loop_i] and (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) != imod(MpCanvas.fighter_slot[0], 2)):
                            MpCanvas.target_cursor = MpCanvas.loop_i
                            break
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    if MpCanvas.enemies_alive > 1:
                        break
                    self.start_timing()
                else:
                    self.start_timing()
                break
        self.draw_buffer()
        self.draw_fighters(MpCanvas.screen_g)
        MpCanvas.draw_action_pad(MpCanvas.screen_g)
        self.draw_target_marker(MpCanvas.screen_g)
        self.draw_battle_prompt(MpCanvas.screen_g, 1)

    def _paint_timing_bar(self):  # state 97
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

    def _paint_hit_effect(self):  # state 98
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
            return
        self.draw_battle_prompt(MpCanvas.screen_g, 2)
        self.check_invite_timeout()

    def _paint_reveal_actions(self):  # state 99
        self.draw_buffer()
        MpCanvas.state_ticks = max(MpCanvas.state_ticks, 2)
        self.draw_fighters(MpCanvas.screen_g)
        self.draw_action_cards()
        if MpCanvas.state_ticks < 4:
            return
        MpCanvas.turn_rec = 0
        self.next_turn_record()

    def _paint_no_battle(self):  # state 100
        self.draw_buffer()
        self.draw_fighters(MpCanvas.screen_g)
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 25), 80, 20, 0)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 6) - 25), Consts.texts[8], 0xFFFFFF)
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            return
        if MpCanvas.state_ticks != idiv(1000, MpCanvas.tick_ms):
            return
        MpCanvas.set_state(93)

    def _paint_turn_start(self):  # state 101
        self.draw_buffer()
        self.draw_fighters(MpCanvas.screen_g)
        self.reset_turn()
        MpCanvas.set_state(102)

    def _paint_turn_replay(self):  # state 102
        self.draw_buffer()
        self.draw_turn_fighters()
        self.draw_action_cards()
        self.draw_damage()
        MpCanvas.anim_frame = MpCanvas.anim_frame + 1
        self.step_turn_anim()

    def _paint_battle_over(self):  # state 103
        self.draw_buffer()
        self.draw_fighters(MpCanvas.screen_g)
        if MpCanvas.state_ticks >= 2:
            return
        MpCanvas.state_ticks = 2
        self.send_request(1025)

    def _paint_stage_complete(self):  # state 104
        self.draw_buffer()
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.body_images[0] = None
            MpCanvas.body_images[1] = None
            i_set = 0
            while i_set < 3:
                if MpCanvas.body_frames[i_set] is not None:
                    MpCanvas.body_frames[i_set].free()
                MpCanvas.body_frames[i_set] = None
                i_set = i_set + 1
            i_set = 0
            while i_set < 10:
                MpCanvas.head_images[i_set][0] = None
                MpCanvas.head_images[i_set][1] = None
                i_frame = 0
                while i_frame < 3:
                    if MpCanvas.head_frames[i_set][i_frame] is not None:
                        MpCanvas.head_frames[i_set][i_frame].free()
                    MpCanvas.head_frames[i_set][i_frame] = None
                    i_frame = i_frame + 1
                i_set = i_set + 1
            i_set = 0
            while i_set < 2:
                MpCanvas.weapon_images[i_set][0] = None
                MpCanvas.weapon_images[i_set][1] = None
                i_frame = 0
                while i_frame < 3:
                    if MpCanvas.weapon_frames[i_set][i_frame] is not None:
                        MpCanvas.weapon_frames[i_set][i_frame].free()
                    MpCanvas.weapon_frames[i_set][i_frame] = None
                    i_frame = i_frame + 1
                i_set = i_set + 1
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

    def _paint_battle_result(self):  # state 105
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
            return
        MpCanvas.draw_hp_bars(MpCanvas.screen_g)
        self.draw_fighters(MpCanvas.screen_g)
        self.draw_battle_result()

    def _paint_main_menu(self):  # state 10
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            i_face = 0
            while i_face < len(MpCanvas.face_images):
                MpCanvas.face_images[i_face] = None
                i_face = i_face + 1
            self.free_battle_images()
            MpCanvas.title = Consts.texts[9]
            MpCanvas.menu_size = 8         # PORT-EXTRA: 6 = Order, 7 = Chat (mp_canvas_order / _chat)
            MpCanvas.order_invite = False
            self.draw_menu_icons()
        self.draw_buffer()
        item = MpCanvas.cursor_stack[MpCanvas.stack_depth]
        Draw.draw_image(MpCanvas.screen_g, MpCanvas.mpic_images[item], (MpCanvas.center_x - 40), (MpCanvas.center_y - 59), 0)
        label = Consts.main_menu[item] if item < 6 else (mp_canvas_order.TEXTS[0] if item == 6 else mp_canvas_chat.TEXTS[0])
        self.draw_button(MpCanvas.screen_g, label, (MpCanvas.center_x - 39), (MpCanvas.center_y + 21), 78, 17, False, True)
        self.draw_chat_badge()             # PORT-EXTRA: unread order / private messages
        MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
        if MpCanvas.popup_shown:
            self.draw_exit_confirm(MpCanvas.screen_g)
            return
        # PORT-EXTRA: no LOGIN (another account) with the single player's account
        self.draw_softkeys(-1 if MpCanvas.sp_account else 5, 2)

    def _paint_duel_menu(self):  # state 11
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = Consts.main_menu[0]
            mp_canvas_order.install()
            MpCanvas.menu_size = len(Consts.duel_menu)   # PORT-EXTRA: + 2-on-2 Order
            self.draw_menu_icons()
        Draw.draw_image(MpCanvas.screen_g, MpCanvas.buffer, 0, 0, 0)
        self.draw_button(MpCanvas.screen_g, Consts.duel_menu[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 39), (MpCanvas.center_y - 19), 78, 17, False, True)
        MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
        self.draw_softkeys((-1), 1)

    def _paint_mission_menu(self):  # state 12
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = Consts.main_menu[1]
            mp_canvas_order.install()
            MpCanvas.menu_size = len(Consts.mission_menu)   # PORT-EXTRA: + Order Ally
            self.draw_menu_icons()
        self.draw_buffer()
        self.draw_button(MpCanvas.screen_g, Consts.mission_menu[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 45), (MpCanvas.center_y - 19), 90, 17, False, True)
        MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
        self.draw_softkeys((-1), 1)

    def _paint_character_menu(self):  # state 16
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = Consts.main_menu[2]
            MpCanvas.menu_size = 6
            self.draw_menu_icons()
        self.draw_buffer()
        self.draw_button(MpCanvas.screen_g, Consts.character_menu[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 45), (MpCanvas.center_y - 19), 90, 17, False, True)
        MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
        self.draw_softkeys((-1), 1)

    def _paint_challenge_menu(self):  # state 20
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

    def _paint_user_id_input(self):  # state 21
        prompt_y = (MpCanvas.center_y - 48)
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.letter_cursor = 0
            MpCanvas.input_text = ""
            self.draw_user_id_prompt(MpCanvas.buffer_g, prompt_y)
        self.draw_buffer()
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (prompt_y + 61), MpCanvas.input_text, 0x41FF41)
        MpCanvas.draw_letter_grid(MpCanvas.letter_cursor, (prompt_y + 75))
        if imod(MpCanvas.state_ticks, 4) < 2:
            text_w = MpCanvas.font_white.string_width(MpCanvas.input_text)
            if len(MpCanvas.input_text) == 12:
                text_w = (text_w - (MpCanvas.font_white.string_width("A") * 2))
            MpCanvas.draw_line_color(MpCanvas.screen_g, (MpCanvas.center_x + idiv(text_w, 2)), (prompt_y + 71), ((MpCanvas.center_x + idiv(text_w, 2)) + 4), (prompt_y + 71), 0xFFFFFF)
        if len(MpCanvas.input_text) == 0:
            self.draw_softkeys(4, 1)
            return
        self.draw_softkeys(4, 3)

    def _paint_records(self):  # state 80
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = Consts.character_menu[0]
        self.draw_records()
        self.draw_softkeys((-1), 1)

    def _paint_attributes(self):  # state 81
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = Consts.character_menu[1]
        self.draw_attributes()
        self.draw_softkeys((-1), 1)

    def _paint_skills(self):  # state 82
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = Consts.character_menu[2]
            self.draw_skills_bg(MpCanvas.buffer_g)
        self.draw_buffer()
        self.draw_skill_slots()
        self.draw_softkeys((-1), 1)

    def _paint_exp_fame_gold(self):  # state 83
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = Consts.character_menu[3]
        self.draw_exp_fame_gold()
        self.draw_softkeys((-1), 1)

    def _paint_change_quote(self):  # state 84
        if MpCanvas.state_ticks < 2:
            MpCanvas.letter_cursor = 0
            MpCanvas.state_ticks = 2
            MpCanvas.title = Consts.character_menu[4]
            self.draw_quote_bg(MpCanvas.buffer_g)
        self.draw_buffer()
        self.draw_quote_prompt(MpCanvas.screen_g)
        if len(MpCanvas.input_text) == 0:
            self.draw_softkeys(4, 1)
            return
        self.draw_softkeys(4, 3)

    def _paint_options(self):  # state 88
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
                while True:
                    if MpCanvas.loop_i == 0:
                        self.draw_text_colored(MpCanvas.screen_g, Consts.option_texts[(3 + MpCanvas.speed)], (MpCanvas.center_x + 33), (MpCanvas.center_y - 15), 1, 0xFFFFFF)
                    elif MpCanvas.loop_i == 1:
                        self.draw_text_colored(MpCanvas.screen_g, Consts.option_texts[(8 + MpCanvas.invitation)], (MpCanvas.center_x + 33), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0xFFFFFF)
                    elif MpCanvas.loop_i == 2:
                        if MpCanvas.get_volume() > 0:
                            i_vol = 0
                            while i_vol < MpCanvas.get_volume():
                                Draw.fill_rect(MpCanvas.screen_g, ((MpCanvas.center_x + 21) + (5 * i_vol)), ((MpCanvas.center_y - 13) + (MpCanvas.loop_i * 19)), 3, 8, 0xFFFFFF)
                                i_vol = i_vol + 1
                            break
                        self.draw_text_colored(MpCanvas.screen_g, Consts.option_texts[(6 + (0 if (MpCanvas.get_volume() > 0) else 1))], (MpCanvas.center_x + 33), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0xFFFFFF)
                    break
                self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 58), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 19)), 61, 14, 3)
                self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x + 13), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 19)), 39, 14, 3)
                if imod(MpCanvas.state_ticks, 4) < 2:
                    MpCanvas.draw_left_half((MpCanvas.center_x + 6), ((MpCanvas.center_y - 13) + (MpCanvas.loop_i * 19)), MpCanvas.arrow_images[1])
                    MpCanvas.draw_right_half((MpCanvas.center_x + 59), ((MpCanvas.center_y - 13) + (MpCanvas.loop_i * 19)), MpCanvas.arrow_images[1])
            else:
                while True:
                    if MpCanvas.loop_i == 0:
                        self.draw_text_colored(MpCanvas.screen_g, Consts.option_texts[(3 + MpCanvas.speed)], (MpCanvas.center_x + 33), (MpCanvas.center_y - 15), 1, 0x646464)
                    elif MpCanvas.loop_i == 1:
                        self.draw_text_colored(MpCanvas.screen_g, Consts.option_texts[(8 + MpCanvas.invitation)], (MpCanvas.center_x + 33), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0x646464)
                    elif MpCanvas.loop_i == 2:
                        if MpCanvas.get_volume() > 0:
                            i_vol = 0
                            while i_vol < MpCanvas.get_volume():
                                Draw.fill_rect(MpCanvas.screen_g, ((MpCanvas.center_x + 21) + (5 * i_vol)), ((MpCanvas.center_y - 13) + (MpCanvas.loop_i * 19)), 3, 8, 0x646464)
                                i_vol = i_vol + 1
                            break
                        self.draw_text_colored(MpCanvas.screen_g, Consts.option_texts[(6 + (0 if (MpCanvas.get_volume() > 0) else 1))], (MpCanvas.center_x + 33), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0x646464)
                    break
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        self.draw_softkeys((-1), 1)

    def _paint_welcome(self):  # state 7
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = Consts.texts[64]
            self.draw_window(MpCanvas.buffer_g)
        self.draw_buffer()
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 112, 48, 0)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 18), _js(Consts.texts[64], "!"), 0xFFFFFF)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 6), MpCanvas.user_id, 0xFFFFFF)
        self.draw_ok_button(MpCanvas.center_y + 9)

    def _paint_notices(self):  # state 6
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = Consts.texts[18]
            self.draw_window(MpCanvas.buffer_g)
        self.draw_notice()

    def _paint_spinner(self):  # state 3
        self.draw_buffer()
        if MpCanvas.state_ticks > idiv(20000, MpCanvas.tick_ms):
            MpCanvas.error_msg = 7
            self.on_disconnect()
            return
        self.draw_loading()

    def _paint_connecting(self):  # state 10000
        self.draw_buffer()
        if MpCanvas.state_ticks == 1:
            self.connect()
        if MpCanvas.state_ticks > idiv(20000, MpCanvas.tick_ms):
            MpCanvas.error_msg = 7
            self.on_disconnect()
            return
        self.draw_loading()

    def _paint_error(self):  # state 4
        self.draw_buffer()
        self.draw_error()
        if MpCanvas.popup_shown:
            self.draw_exit_confirm(MpCanvas.screen_g)
            return
        if MpCanvas.error_msg in {7, 1}:
            self.draw_softkeys(5, 2)

    def _paint_sound_prompt(self):  # state 5
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

    def _paint_title(self):  # state 1
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            top_y = idiv(((MpCanvas.screen_h - 320)), 2)
            i_title = 0
            while i_title < 4:
                MpCanvas.title_image = self.load_image(_js(_js("/title_", (i_title + 1)), ".png"))
                Draw.draw_image(MpCanvas.buffer_g, MpCanvas.title_image, (MpCanvas.center_x - idiv(MpCanvas.title_image.getWidth(), 2)), (top_y + (80 * i_title)), 0)
                MpCanvas.title_image = None
                i_title = i_title + 1
            if not config.NO_GAMEVIL:  # PORT-EXTRA: no "(c) 2008 GAMEVIL INC." line (rebrand.py)
                if MpCanvas.gamevil_image is None:
                    MpCanvas.gamevil_image = self.load_image("/gamevil.png")
                Draw.draw_image(MpCanvas.buffer_g, MpCanvas.gamevil_image, idiv(MpCanvas.canvas_w, 2), (MpCanvas.canvas_h - 1), 33)
            if MpCanvas.press_image is None:
                MpCanvas.press_image = self.load_image("/press.png")
        self.draw_buffer()
        if imod(MpCanvas.state_ticks, 4) >= 2:
            return
        Draw.draw_image(MpCanvas.screen_g, MpCanvas.press_image, idiv(MpCanvas.canvas_w, 2), (MpCanvas.canvas_h - 27), 33)

    def _paint_login(self):  # state 2
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.input_text = ""
            self.free_battle_images()
            MpCanvas.title = Consts.login_texts[0]
            self.draw_window_bg(MpCanvas.buffer_g)
        self.draw_buffer()
        self.draw_popup()

    def _paint_dialog(self):  # state 160
        self.draw_buffer()
        if MpCanvas.popup_style == 0:
            MpCanvas.tmp = len(MpCanvas.popup_line1)
            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, ((MpCanvas.tmp * 7) + 6), 45, 0)
            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 13), MpCanvas.popup_line1, 16400640)
            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y + 2), MpCanvas.popup_line2, 16400640)
        elif MpCanvas.popup_style == 1:
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
        elif MpCanvas.popup_style == 2:
            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 120, 100, 0)
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) - 10), MpCanvas.popup_line1, 16400640)
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) + 5), MpCanvas.popup_line2, 16400640)
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) + 20), MpCanvas.popup_line3, 16400640)
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) + 35), MpCanvas.popup_line4, 16400640)
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) + 50), MpCanvas.popup_line5, 16400640)
        else:
            return

    def _paint_outro(self):  # state 300
        if MpCanvas.embedded:                # PORT-EXTRA: back to the single player at once
            MpCanvas.disconnect()
            self.stop_music()
            MpCanvas.midlet.destroyApp(True)
            MpCanvas.midlet.notifyDestroyed()
            return
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.disconnect()
            self.stop_music()
            MpCanvas.logo_image = self.load_image("/outro.png")
        Draw.fill_rect(MpCanvas.screen_g, 0, 0, MpCanvas.screen_w, MpCanvas.screen_h, 0)
        logo_w = MpCanvas.logo_image.getWidth()
        Gfx.draw_image_part(MpCanvas.logo_image, (MpCanvas.center_x - idiv(logo_w, 2)), (MpCanvas.center_y - 10), logo_w, 19, 0, 0)
        Gfx.draw_image_part(MpCanvas.logo_image, (MpCanvas.center_x - idiv(logo_w, 2)), (MpCanvas.screen_h - 26), logo_w, 23, 0, 19)
        if MpCanvas.state_ticks <= 30:
            return
        MpCanvas.midlet.destroyApp(True)
        MpCanvas.midlet.notifyDestroyed()

    def _paint_help_menu(self):  # state 87
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = Consts.main_menu[4]
            MpCanvas.menu_size = 6
            self.draw_menu_icons()
        self.draw_buffer()
        self.draw_button(MpCanvas.screen_g, Consts.help_topics[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 39), (MpCanvas.center_y - 19), 78, 17, False, True)
        MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
        self.draw_softkeys((-1), 1)

    def _paint_help_page(self):  # state 89
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.help_page = 0
        self.draw_help()
        self.draw_softkeys((-1), 1)

    def _paint_display_name(self):  # state 85
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            if MpCanvas.state == 85:
                MpCanvas.title = Consts.character_menu[5]
            self.draw_name_prompt(MpCanvas.buffer_g)
        self.draw_buffer()
        self.draw_input_line(MpCanvas.screen_g)
        if len(MpCanvas.input_text) == 0:
            self.draw_softkeys(4, 1)
            return
        self.draw_softkeys(4, 3)

    def _paint_name_confirm(self):  # state 86
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.menu_size = 2
        self.draw_buffer()
        self.draw_input_line(MpCanvas.screen_g)
        self.draw_name_confirm(MpCanvas.screen_g)

    _PAINT_BY_STATE = {  # state -> handler, the branches of paint_screen
        0: _paint_logo,
        161: _paint_ranking_menu,
        162: _paint_my_rank,
        163: _paint_my_rank,
        164: _paint_my_rank,
        170: _paint_rank_list,
        171: _paint_rank_list,
        90: _paint_waiting_room,
        91: _paint_stage_intro,
        92: _paint_start_quotes,
        93: _paint_round_start,
        94: _paint_choose_action,
        95: _paint_skill_list,
        96: _paint_choose_target,
        97: _paint_timing_bar,
        98: _paint_hit_effect,
        99: _paint_reveal_actions,
        100: _paint_no_battle,
        101: _paint_turn_start,
        102: _paint_turn_replay,
        103: _paint_battle_over,
        104: _paint_stage_complete,
        105: _paint_battle_result,
        10: _paint_main_menu,
        11: _paint_duel_menu,
        12: _paint_mission_menu,
        16: _paint_character_menu,
        20: _paint_challenge_menu,
        21: _paint_user_id_input,
        80: _paint_records,
        81: _paint_attributes,
        82: _paint_skills,
        83: _paint_exp_fame_gold,
        84: _paint_change_quote,
        88: _paint_options,
        7: _paint_welcome,
        6: _paint_notices,
        3: _paint_spinner,
        10000: _paint_connecting,
        4: _paint_error,
        5: _paint_sound_prompt,
        1: _paint_title,
        2: _paint_login,
        160: _paint_dialog,
        300: _paint_outro,
        87: _paint_help_menu,
        89: _paint_help_page,
        85: _paint_display_name,
        86: _paint_name_confirm,
    }

    @staticmethod
    def set_timer(ticks):  # g.java:1467
        MpCanvas.timer_ticks = ticks

    def hideNotify(self):  # g.java:3433
        self.stop_music()
        MpCanvas.request_pause(1)

    def showNotify(self):  # g.java:3438
        MpCanvas.request_pause(1)

    @staticmethod
    def set_state(state):  # g.java:4735
        MpCanvas.state = state
        MpCanvas.state_ticks = 0

    def push_state(self, state):  # g.java:4996
        if state != MpCanvas.state_stack[MpCanvas.stack_depth]:
            MpCanvas.cursor_stack[_inc(MpCanvas, "stack_depth", 1)] = 0
            MpCanvas.state_stack[MpCanvas.stack_depth] = state
        MpCanvas.set_state(state)

    def reset_state_stack(self, state):  # g.java:5004
        if state == 10:
            MpCanvas.relogin = True
        MpCanvas.stack_depth = 0
        MpCanvas.cursor_stack[0] = 0
        MpCanvas.state_stack[0] = state
        MpCanvas.set_state(state)

    def pop_state(self):  # g.java:5014
        if MpCanvas.stack_depth > 0:
            MpCanvas.set_state(MpCanvas.state_stack[_inc(MpCanvas, "stack_depth", -1)])

    def pop_states(self, count):  # g.java:5020
        if MpCanvas.stack_depth >= count:
            MpCanvas.set_state(MpCanvas.state_stack[_set(MpCanvas, "stack_depth", (MpCanvas.stack_depth - count))])

    @staticmethod
    def noop():  # g.java:5599
        pass


def _static_init():
    MpCanvas.title = ""
    MpCanvas.timer_ticks = 0
    MpCanvas.screen_g = None
    MpCanvas.rng = Random()
    MpCanvas.menu_size = 8
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
    MpCanvas.mpic_images = [None] * (8)   # PORT-EXTRA: mpic6 = Order, mpic7 = Chat
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
    from pow_mp.answer import Answer
    from pow_mp.consts import Consts
    from pow_mp.draw import Draw
    from pow_mp.font import Font
    from pow_mp.frame_reader import FrameReader
    from pow_mp.frame_writer import FrameWriter
    from pow_mp.gfx import Gfx
    from pow_mp.mp_game import MpGame
    from pow_mp.net_thread import NetThread
    from pow_mp.player_pool import PlayerPool
    from pow_mp.res_reader import ResReader
    from pow_mp.sprite_frames import SpriteFrames
    for _part in _PARTS:
        vars(_part).update({_name: globals()[_name] for _name in _LATE_NAMES if _name in vars(_part)})


_LATE_NAMES = ("SpriteFrames", "PlayerPool", "NetThread", "ResReader", "Consts", "Draw", "Gfx", "Font", "Answer", "FrameWriter", "FrameReader", "MpGame")
_PARTS = (mp_canvas_draw, mp_canvas_battle, mp_canvas_net, mp_canvas_input, mp_canvas_screens, mp_canvas_assets,
          mp_canvas_options, mp_canvas_order, mp_canvas_chat)
for _part in _PARTS:
    _part.MpCanvas = MpCanvas
# PORT-EXTRA: the Order window's states and answers (pow_mp/mp_canvas_order.py)
MpCanvas._PAINT_BY_STATE.update(OrderMixin.PAINT)
MpCanvas._KEYS_BY_STATE.update(OrderMixin.KEYS)
MpCanvas._KEYS_BY_STATE[mp_canvas_order.MEMBER] = InputMixin._keys_duel_menu
MpCanvas._ANSWER_BY_OPCODE.update(OrderMixin.ANSWERS)
# PORT-EXTRA: the Chat window's states and answers (pow_mp/mp_canvas_chat.py)
MpCanvas._PAINT_BY_STATE.update(ChatMixin.PAINT)
MpCanvas._KEYS_BY_STATE.update(ChatMixin.KEYS)
MpCanvas._ANSWER_BY_OPCODE.update(ChatMixin.ANSWERS)
