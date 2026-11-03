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
    app_version = None  # g.java:25 String
    game = None  # g.java:26 m
    c = None  # g.java:27 String
    d = 0  # g.java:28 int
    screen_g = None  # g.java:29 Graphics
    buffer = None  # g.java:30 Image
    buffer_g = None  # g.java:31 Graphics
    rng = None  # g.java:32 Random
    user_id = None  # g.java:33 String
    password = None  # g.java:34 String
    k = 0  # g.java:35 int
    midlet = None  # g.java:36 Main
    key = 0  # g.java:37 int
    font_white = None  # g.java:38 j
    font_orange = None  # g.java:39 j
    font_gray = None  # g.java:40 j
    font_green = None  # g.java:41 j
    server_host = None  # g.java:42 String
    server_port = 0  # g.java:43 int
    game_ver = None  # g.java:44 String
    u = False  # g.java:45 boolean
    v = 0  # g.java:46 long
    w = False  # g.java:47 boolean
    popup_shown = False  # g.java:48 boolean
    popup_cursor = 0  # g.java:49 int
    popup_kind = 0  # g.java:50 int
    A = False  # g.java:51 boolean
    B = 0  # g.java:52 int
    letter_cursor = 0  # g.java:53 int
    D = False  # g.java:54 boolean
    E = 0  # g.java:55 int
    F = 0  # g.java:56 long
    G = False  # g.java:57 boolean
    pause_request = 0  # g.java:58 int
    music_to_resume = 0  # g.java:59 int
    paused = False  # g.java:60 boolean
    K = False  # g.java:61 boolean
    L = False  # g.java:62 boolean
    M = 0  # g.java:63 long
    login_time = 0  # g.java:64 long
    O = False  # g.java:65 boolean
    P = False  # g.java:66 boolean
    Q = 0  # g.java:67 int
    R = 0  # g.java:68 int
    S = 0  # g.java:69 int
    T = 0  # g.java:70 int
    U = 0  # g.java:71 int
    V = 0  # g.java:72 int
    W = 0  # g.java:73 int
    X = 0  # g.java:74 int
    rank_names = None  # g.java:75 String[]
    rank_ranks = None  # g.java:76 int[]
    rank_values = None  # g.java:77 int[]
    ab = 0  # g.java:78 int
    my_ranks = None  # g.java:79 int[]
    my_rank_value = 0  # g.java:80 int
    rank_kind = 0  # g.java:81 byte
    af = 0  # g.java:82 int
    ag = None  # g.java:83 String
    ah = None  # g.java:84 String
    ai = None  # g.java:85 String
    aj = None  # g.java:86 String
    ak = None  # g.java:87 String
    al = 0  # g.java:88 int
    volume = 0  # g.java:89 int
    speed = 0  # g.java:90 int
    invitation_saved = 0  # g.java:91 int
    invitation = 0  # g.java:92 int
    aq = False  # g.java:93 boolean
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
    aK = 0  # g.java:113 int
    aL = 0  # g.java:114 int
    aM = 0  # g.java:115 int
    notices_left = 0  # g.java:116 byte
    aO = 0  # g.java:117 int
    stage_count = 0  # g.java:118 int
    stage = 0  # g.java:119 int
    aR = 0  # g.java:120 int
    aS = 0  # g.java:121 int
    turn_record_count = 0  # g.java:122 int
    battle_won = 0  # g.java:123 int
    reward_gold = 0  # g.java:124 int
    reward_grade = 0  # g.java:125 byte
    reward_fame = 0  # g.java:126 int
    reward_exp = 0  # g.java:127 int
    reward_rank = 0  # g.java:128 int
    ba = 0  # g.java:129 int
    bb = 0  # g.java:130 int
    bc = 0  # g.java:131 int
    bd = 0  # g.java:132 int
    be = 0  # g.java:133 int
    skill_count = 0  # g.java:134 int
    leaving_slot = 0  # g.java:135 int
    my_slot = 0  # g.java:136 byte
    bi = False  # g.java:137 boolean
    bj = False  # g.java:138 boolean
    bk = False  # g.java:139 boolean
    bl = 0  # g.java:140 int
    bm = 0  # g.java:141 int
    bn = False  # g.java:142 boolean
    bo = 0  # g.java:143 int
    bp = 0  # g.java:144 int
    bq = False  # g.java:145 boolean
    br = False  # g.java:146 boolean
    bs = False  # g.java:147 boolean
    bt = False  # g.java:148 boolean
    bu = 0  # g.java:149 int
    bv = 0  # g.java:150 int
    bw = False  # g.java:151 boolean
    bx = False  # g.java:152 boolean
    room_bg = 0  # g.java:153 int
    room_mode = 0  # g.java:154 byte
    bA = 0  # g.java:155 int
    bB = 0  # g.java:156 int
    bC = 0  # g.java:157 int
    skill_slot_count = 0  # g.java:158 int
    skill_slots = None  # g.java:159 byte[]
    bF = None  # g.java:160 String[]
    input_text = None  # g.java:161 String
    stage_title = None  # g.java:162 String
    loot = None  # g.java:163 String
    bJ = 0  # g.java:164 int
    hp_bar_w = 0  # g.java:165 int
    bL = None  # g.java:166 String
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
    cc = None  # g.java:183 int[]
    cd = None  # g.java:184 int[]
    ce = None  # g.java:185 int[]
    fighter_hp_target = None  # g.java:186 int[]
    fighter_mp_target = None  # g.java:187 int[]
    fighter_hp_step = None  # g.java:188 int[]
    fighter_mp_step = None  # g.java:189 int[]
    fighter_hp_delta = None  # g.java:190 int[]
    fighter_x = None  # g.java:191 int[]
    fighter_y = None  # g.java:192 int[]
    cm = None  # g.java:193 int[]
    fighter_frame = None  # g.java:194 int[]
    fighter_blink = None  # g.java:195 int[]
    fighter_status = None  # g.java:196 int[]
    fighter_status_ticks = None  # g.java:197 int[]
    cr = None  # g.java:198 int[]
    key_in = 0  # g.java:199 int
    cur_slot = 0  # g.java:200 int
    cu = 0  # g.java:201 int
    cv = 0  # g.java:202 int
    cw = 0  # g.java:203 int
    cx = 0  # g.java:204 int
    cy = 0  # g.java:205 int
    cz = 0  # g.java:206 int
    cA = 0  # g.java:207 int
    cB = None  # g.java:208 byte[]
    cC = 0  # g.java:209 int
    cD = 0  # g.java:210 int
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
    dc = 0  # g.java:235 int
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
    ds = None  # g.java:251 Image
    softkey_image = None  # g.java:252 Image
    du = None  # g.java:253 Image[]
    dv = None  # g.java:254 a[]
    dw = None  # g.java:255 Image[][]
    dx = None  # g.java:256 a[][]
    dy = None  # g.java:257 Image[][]
    dz = None  # g.java:258 a[][]
    dA = None  # g.java:259 Image[][]
    dB = None  # g.java:260 a[][]
    dC = None  # g.java:261 Image[][]
    dD = None  # g.java:262 a[][]
    dE = None  # g.java:263 a[]
    dF = None  # g.java:264 Image[]
    dG = None  # g.java:265 a[]
    dH = None  # g.java:266 Image[]
    dI = None  # g.java:267 a[]
    dJ = None  # g.java:268 Image[]
    dK = None  # g.java:269 a[]
    dL = None  # g.java:270 Image[]
    dM = None  # g.java:271 a[]
    dN = None  # g.java:272 Image[]
    dO = None  # g.java:273 a[]
    net = None  # g.java:274 h
    request_opcode = 0  # g.java:275 int
    answer_status = 0  # g.java:276 int
    logo_y = 0  # g.java:277 int
    thread = None  # g.java:278 Thread
    cursor_stack = None  # g.java:279 int[]
    state_stack = None  # g.java:280 int[]
    stack_depth = 0  # g.java:281 int
    dX = False  # g.java:282 boolean
    painted = False  # g.java:283 boolean
    dZ = 0  # g.java:284 int
    disconnecting = False  # g.java:285 boolean
    eb = False  # g.java:286 boolean
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
        MpCanvas.X_v()
        MpCanvas.set_state(0)

    def load_image(self, string):  # g.java:337
        image = None
        try:
            image = Image.createImage(string)
        except Exception as exception:
            MpCanvas.log(_js("--------createImage err:", exception))
        return image

    @staticmethod
    def a_G(graphics):  # g.java:348
        n2 = idiv(80, MpCanvas.k)
        if n2 > 30:
            n2 = 30
        elif n2 < 19:
            n2 = 19
        n3 = 0
        if ((MpCanvas.state == 162) or (MpCanvas.state == 163)) or (MpCanvas.state == 164):
            n3 = 15
        elif MpCanvas.state == 10:
            n3 = 40
        Draw.draw_image_part(graphics, MpCanvas.menu_icon_image, (idiv((((MpCanvas.canvas_w - (n2 * ((MpCanvas.k - 1)))) - 11)), 2) + (n2 * MpCanvas.cursor_stack[MpCanvas.stack_depth])), ((MpCanvas.center_y + 6) + n3), 12, 15, 0, 0)

    def paint(self, graphics):  # g.java:364
        MpCanvas.screen_g = graphics
        Gfx.set_graphics(graphics)
        if MpCanvas.w:
            MpCanvas.painted = True
            return
        self.paint_screen()
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
        if (not MpCanvas.K) or MpCanvas.L:
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
                if ((n2 := (Consts.ef[MpCanvas.speed] - i32(((((l2 := system.currentTimeMillis())) - MpCanvas.frame_start)))))) > 20:
                    MpCanvas.sleep(n2)
                else:
                    MpCanvas.sleep(20)
            self.apply_pause()
            MpCanvas.K = True

    def paint_screen(self):  # g.java:474
        if MpCanvas.painted:
            return
        if (MpCanvas.state != 3) and (MpCanvas.state != 10000):
            MpCanvas.L = False
        if MpCanvas.paused:
            Draw.fill_rect(MpCanvas.screen_g, 0, 0, MpCanvas.screen_w, MpCanvas.screen_h, 0)
            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 100, 29, 0)
            self.draw_text_colored(MpCanvas.screen_g, Consts.eX[2], MpCanvas.center_x, (MpCanvas.center_y - 6), 1, 0xFFFFFF)
            return
        if NetThread.connected and (not MpCanvas.eb):
            if NetThread.idle_frames > 100:
                NetThread.idle_frames = 0
                self.send_request(39327)
                if _inc(MpCanvas, 'dZ', 1) > 20:
                    MpCanvas.dZ = 0
                    MpCanvas.cw = 13
                    MpCanvas.popup_shown = False
                    self.on_disconnect()
            else:
                NetThread.idle_frames = NetThread.idle_frames + 1
        if not MpCanvas.D:
            if MpCanvas.d == 1:
                MpCanvas.d = 0
                if MpCanvas.state == 97:
                    if (_set(MpCanvas, 'cA', (MpCanvas.cA + MpCanvas.cz))) > (((MpCanvas.center_x - 44) + 72) + MpCanvas.cz):
                        MpCanvas.cA = (((MpCanvas.center_x - 44) + 72) + MpCanvas.cz)
                    else:
                        MpCanvas.b_I(1)
                else:
                    if _inc(MpCanvas, 'ba', -1) == 0:
                        MpCanvas.bB = 1
                        MpCanvas.cA = (((MpCanvas.center_x - 44) + 72) + MpCanvas.cz)
                        self.C_v()
                    MpCanvas.b_I((10 - MpCanvas.speed))
            elif MpCanvas.d > 0:
                MpCanvas.d = MpCanvas.d - 1
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
                            MpCanvas.ds = self.load_image("/gamevillogo.png")
                            MpCanvas.softkey_image = self.load_image("/softbg.png")
                            MpCanvas.logo_y = idiv(((MpCanvas.canvas_h - ((MpCanvas.ds.getHeight() + 12)))), 2)
                            MpCanvas.ds.getHeight()
                            MpCanvas.ds.getWidth()
                        except Exception:
                            pass
                        MpCanvas.M = system.currentTimeMillis()
                        Draw.fill_rect(MpCanvas.buffer_g, 0, 0, MpCanvas.canvas_w, MpCanvas.canvas_h, 0xFFFFFF)
                    self.draw_buffer()
                    Draw.draw_image(MpCanvas.screen_g, MpCanvas.ds, idiv(MpCanvas.canvas_w, 2), MpCanvas.logo_y, 17)
                    if (system.currentTimeMillis() - MpCanvas.M) <= 3000:
                        break
                    MpCanvas.ds = None
                    MpCanvas.state = 5
                    return
                if _m4 or _sw3 == 161:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eM[5]
                        MpCanvas.k = 3
                        self.U_v()
                    self.draw_buffer()
                    self.a_GTIIIIZZ(MpCanvas.screen_g, Consts.eR[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 43), (MpCanvas.center_y - 19), 86, 17, False, True)
                    MpCanvas.a_G(MpCanvas.screen_g)
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 in (162, 163, 164):
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eR[(MpCanvas.state - 162)]
                        MpCanvas.k = 2
                        self.U_v()
                        MpCanvas.box_x = ((MpCanvas.canvas_w - 96) >> 1)
                        MpCanvas.draw_panel(MpCanvas.buffer_g, MpCanvas.box_x, (MpCanvas.center_y - 54), 96, 15)
                        self.draw_text_colored(MpCanvas.buffer_g, MpCanvas.user_id, (idiv(MpCanvas.canvas_w, 2) + 4), ((MpCanvas.center_y + 2) - 54), 1, 0xFFFFFF)
                        MpCanvas.draw_panel(MpCanvas.buffer_g, MpCanvas.box_x, ((MpCanvas.center_y + 14) - 54), 96, 15)
                        self.draw_text_colored(MpCanvas.buffer_g, Consts.eX[4], (MpCanvas.box_x + 3), (((MpCanvas.center_y + 14) + 2) - 54), 0, 0xFFFFFF)
                        MpCanvas.draw_number(MpCanvas.buffer_g, ((MpCanvas.box_x + 96) - 7), (((MpCanvas.center_y + 14) + 3) - 54), MpCanvas.my_ranks[MpCanvas.rank_kind], 0)
                        _sw5 = MpCanvas.state
                        if _sw5 == 162:
                            var1_1 = Consts.eR[0]
                        else:
                            var1_1 = Consts.eX[3]
                        MpCanvas.draw_panel(MpCanvas.buffer_g, MpCanvas.box_x, ((MpCanvas.center_y + 28) - 54), 96, 15)
                        self.draw_text_colored(MpCanvas.buffer_g, var1_1, (MpCanvas.box_x + 3), (((MpCanvas.center_y + 28) + 2) - 54), 0, 0xFFFFFF)
                        MpCanvas.draw_number(MpCanvas.buffer_g, ((MpCanvas.box_x + 96) - 7), (((MpCanvas.center_y + 28) + 3) - 54), MpCanvas.my_rank_value, 0)
                    self.draw_buffer()
                    self.a_GTIIIIZZ(MpCanvas.screen_g, Consts.eS[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 43), ((MpCanvas.center_y - 19) + 15), 86, 17, False, True)
                    MpCanvas.a_G(MpCanvas.screen_g)
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 in (170, 171):
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eS[(MpCanvas.state - 170)]
                        self.draw_window_bg(MpCanvas.buffer_g)
                        var1_2 = ((MpCanvas.canvas_w - 110) >> 1)
                        var2_7 = (MpCanvas.canvas_h >> 1)
                        _sw6 = MpCanvas.af
                        if _sw6 == 162:
                            var3_14 = Consts.eR[0]
                        elif _sw6 == 163:
                            var3_14 = Consts.eX[3]
                        else:
                            var3_14 = Consts.eX[3]
                        var4_16 = 0
                        while var4_16 < 3:
                            self.draw_text_colored(MpCanvas.buffer_g, MpCanvas.rank_names[var4_16], MpCanvas.center_x, ((var2_7 - 65) + (45 * var4_16)), 1, 0xFFFFFF)
                            MpCanvas.draw_panel(MpCanvas.buffer_g, var1_2, ((var2_7 - 52) + (45 * var4_16)), 110, 15)
                            MpCanvas.draw_panel(MpCanvas.buffer_g, var1_2, ((var2_7 - 38) + (45 * var4_16)), 110, 15)
                            self.draw_text_colored(MpCanvas.buffer_g, Consts.eX[4], (var1_2 + 3), (((var2_7 - 52) + 2) + (45 * var4_16)), 0, 0xFFFFFF)
                            MpCanvas.draw_number(MpCanvas.buffer_g, ((var1_2 + 110) - 7), ((((var2_7 - 52) + 2) + 1) + (45 * var4_16)), MpCanvas.rank_ranks[var4_16], 0)
                            self.draw_text_colored(MpCanvas.buffer_g, var3_14, (var1_2 + 3), (((var2_7 - 38) + 2) + (45 * var4_16)), 0, 0xFFFFFF)
                            MpCanvas.draw_number(MpCanvas.buffer_g, ((var1_2 + 110) - 7), ((((var2_7 - 38) + 2) + 1) + (45 * var4_16)), MpCanvas.rank_values[var4_16], 0)
                            var4_16 = var4_16 + 1
                    self.draw_buffer()
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 90:
                    _m4 = True
                    if MpCanvas.O:
                        self.draw_background()
                        self.Y_v()
                        MpCanvas.O = False
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.bk = False
                    if MpCanvas.bj:
                        if MpCanvas.fighter_kind[MpCanvas.cur_slot] == 0:
                            MpCanvas.bk = True
                        self.m_G(MpCanvas.buffer_g)
                        MpCanvas.bj = False
                    self.draw_buffer()
                    self.c_G(MpCanvas.screen_g)
                    if MpCanvas.bk:
                        self.y_v()
                        break
                    self.af_v()
                    return
                if _m4 or _sw3 == 91:
                    _m4 = True
                    self.draw_buffer()
                    self.c_G(MpCanvas.screen_g)
                    self.z_v()
                    if MpCanvas.state_ticks != idiv(1500, MpCanvas.dc):
                        break
                    self.send_request(1038)
                    return
                if _m4 or _sw3 == 92:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                    self.draw_buffer()
                    self.c_G(MpCanvas.screen_g)
                    if (MpCanvas.state_ticks >= idiv(500, MpCanvas.dc)) and (MpCanvas.state_ticks < idiv(1500, MpCanvas.dc)):
                        self.b_GI(MpCanvas.screen_g, 0)
                    elif MpCanvas.state_ticks >= idiv(1500, MpCanvas.dc):
                        self.b_GI(MpCanvas.screen_g, 1)
                    if MpCanvas.state_ticks != idiv(2500, MpCanvas.dc):
                        break
                    MpCanvas.aR = 0
                    MpCanvas.set_state(93)
                    return
                if _m4 or _sw3 == 93:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.X_v()
                        MpCanvas.state_ticks = 2
                        MpCanvas.aR = MpCanvas.aR + 1
                        if ((MpCanvas.bb == 0) or (MpCanvas.bc == 0)) or (MpCanvas.fighter_hp[0] == 0):
                            MpCanvas.set_state(103)
                        else:
                            MpCanvas.Q_v()
                    elif MpCanvas.state_ticks == idiv(1000, MpCanvas.dc):
                        self.send_request(1025)
                    self.draw_buffer()
                    self.c_G(MpCanvas.screen_g)
                    if ((((MpCanvas.aR > 0) and (MpCanvas.aR < 100)) and (MpCanvas.bb != 0)) and (MpCanvas.bc != 0)) and (MpCanvas.fighter_hp[0] != 0):
                        self.i_G(MpCanvas.screen_g)
                        self.d_GI(MpCanvas.screen_g, 2)
                        self.check_invite_timeout()
                    return
                if _m4 or _sw3 == 94:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.bt = False
                    self.draw_buffer()
                    if MpCanvas.D:
                        MpCanvas.dZ = 1
                        MpCanvas.state_ticks = MpCanvas.state_ticks - 1
                        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 120, 100, 0)
                        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) - 10), Consts.eX[60], 0xFFFFFF)
                        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) + 2), Consts.eX[61], 0xFFFFFF)
                        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) + 14), Consts.eX[62], 0xFFFFFF)
                        var1_3 = i32(((15 - idiv(((system.currentTimeMillis() - MpCanvas.F)), 1000))))
                        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) + 30), _js(Consts.eX[63], "   "), 0xFFFFFF)
                        self.draw_text_centred_on(MpCanvas.screen_g, (MpCanvas.center_x + 35), ((MpCanvas.center_y - 21) + 30), _js("", var1_3), 16400640)
                        var2_8 = 0
                        while var2_8 < 2:
                            if MpCanvas.E == var2_8:
                                self.draw_text_colored(MpCanvas.screen_g, Consts.eX[(40 + var2_8)], ((MpCanvas.center_x - 28) + (var2_8 * 55)), (MpCanvas.center_y + 28), 1, 0xFFFFFF)
                                self.draw_box(MpCanvas.screen_g, ((MpCanvas.center_x - 42) + (var2_8 * 55)), (MpCanvas.center_y + 25), 29, 14, 3)
                            else:
                                self.draw_box(MpCanvas.screen_g, ((MpCanvas.center_x - 42) + (var2_8 * 55)), (MpCanvas.center_y + 25), 29, 14, 2)
                                self.draw_text_colored(MpCanvas.screen_g, Consts.eX[(40 + var2_8)], ((MpCanvas.center_x - 28) + (var2_8 * 55)), (MpCanvas.center_y + 28), 1, 0x646464)
                            var2_8 = var2_8 + 1
                        if var1_3 > 0:
                            break
                        MpCanvas.D = False
                        break
                    self.c_G(MpCanvas.screen_g)
                    MpCanvas.j_G(MpCanvas.screen_g)
                    self.d_GI(MpCanvas.screen_g, 0)
                    return
                if _m4 or _sw3 == 95:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.skill_cursor = 0
                    self.draw_buffer()
                    self.c_G(MpCanvas.screen_g)
                    self.h_G(MpCanvas.screen_g)
                    self.d_GI(MpCanvas.screen_g, 1)
                    return
                if _m4 or _sw3 == 96:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        _sw7 = MpCanvas.bB
                        _m8 = False
                        while True:
                            if _m8 or _sw7 in (9, 10):
                                _m8 = True
                                MpCanvas.bA = 0
                                if MpCanvas.bb > 1:
                                    break
                                self.B_v()
                                return
                            if _m8 or _sw7 in (0, 3, 4, 5, 6, 7):
                                _m8 = True
                                MpCanvas.loop_i = 1
                                while MpCanvas.loop_i < 4:
                                    if MpCanvas.fighter_present[MpCanvas.loop_i] and (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) != imod(MpCanvas.fighter_slot[0], 2)):
                                        MpCanvas.bA = MpCanvas.loop_i
                                        break
                                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                                if MpCanvas.bc > 1:
                                    break
                            if _m8 or _sw7 not in (9, 10, 0, 3, 4, 5, 6, 7):
                                _m8 = True
                                self.B_v()
                            break
                    self.draw_buffer()
                    self.c_G(MpCanvas.screen_g)
                    MpCanvas.j_G(MpCanvas.screen_g)
                    self.d_G(MpCanvas.screen_g)
                    self.d_GI(MpCanvas.screen_g, 1)
                    return
                if _m4 or _sw3 == 97:
                    _m4 = True
                    self.draw_buffer()
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        if MpCanvas.bB > 2:
                            self.c_G(MpCanvas.screen_g)
                            MpCanvas.j_G(MpCanvas.screen_g)
                            self.C_v()
                            return
                        self.c_G(MpCanvas.screen_g)
                        MpCanvas.j_G(MpCanvas.screen_g)
                        MpCanvas.A_v()
                        self.e_G(MpCanvas.screen_g)
                        self.f_G(MpCanvas.screen_g)
                        return
                    if MpCanvas.state_ticks > 0:
                        self.c_G(MpCanvas.screen_g)
                        MpCanvas.j_G(MpCanvas.screen_g)
                        self.e_G(MpCanvas.screen_g)
                        self.f_G(MpCanvas.screen_g)
                        return
                    self.c_G(MpCanvas.screen_g)
                    MpCanvas.j_G(MpCanvas.screen_g)
                    self.e_G(MpCanvas.screen_g)
                    self.f_G(MpCanvas.screen_g)
                    return
                if _m4 or _sw3 == 98:
                    _m4 = True
                    self.draw_buffer()
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        self.c_G(MpCanvas.screen_g)
                        MpCanvas.j_G(MpCanvas.screen_g)
                        self.e_G(MpCanvas.screen_g)
                        if (MpCanvas.bB <= 2) and MpCanvas.bt:
                            self.f_G(MpCanvas.screen_g)
                    elif MpCanvas.state_ticks == 4:
                        self.c_G(MpCanvas.screen_g)
                        MpCanvas.j_G(MpCanvas.screen_g)
                        self.e_G(MpCanvas.screen_g)
                        self.send_request(1027)
                    else:
                        self.c_G(MpCanvas.screen_g)
                        MpCanvas.j_G(MpCanvas.screen_g)
                        if MpCanvas.state_ticks < 4:
                            self.e_G(MpCanvas.screen_g)
                    if MpCanvas.state_ticks < 4:
                        break
                    self.d_GI(MpCanvas.screen_g, 2)
                    self.check_invite_timeout()
                    return
                if _m4 or _sw3 == 99:
                    _m4 = True
                    self.draw_buffer()
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                    self.c_G(MpCanvas.screen_g)
                    self.R_v()
                    if MpCanvas.state_ticks < 4:
                        return
                    MpCanvas.bC = 0
                    self.E_v()
                    return
                if _m4 or _sw3 == 100:
                    _m4 = True
                    self.draw_buffer()
                    self.c_G(MpCanvas.screen_g)
                    self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 25), 80, 20, 0)
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 6) - 25), Consts.eX[8], 0xFFFFFF)
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        return
                    if MpCanvas.state_ticks != idiv(1000, MpCanvas.dc):
                        break
                    MpCanvas.set_state(93)
                    return
                if _m4 or _sw3 == 101:
                    _m4 = True
                    self.draw_buffer()
                    self.c_G(MpCanvas.screen_g)
                    self.reset_turn()
                    MpCanvas.set_state(102)
                    return
                if _m4 or _sw3 == 102:
                    _m4 = True
                    self.draw_buffer()
                    self.s_v()
                    self.R_v()
                    self.I_v()
                    MpCanvas.Q = MpCanvas.Q + 1
                    self.D_v()
                    return
                if _m4 or _sw3 == 103:
                    _m4 = True
                    self.draw_buffer()
                    self.c_G(MpCanvas.screen_g)
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
                        MpCanvas.du[0] = None
                        MpCanvas.du[1] = None
                        var1_4 = 0
                        while var1_4 < 3:
                            if MpCanvas.dv[var1_4] is not None:
                                MpCanvas.dv[var1_4].free()
                            MpCanvas.dv[var1_4] = None
                            var1_4 = var1_4 + 1
                        var1_4 = 0
                        while var1_4 < 10:
                            MpCanvas.dw[var1_4][0] = None
                            MpCanvas.dw[var1_4][1] = None
                            var2_9 = 0
                            while var2_9 < 3:
                                if MpCanvas.dx[var1_4][var2_9] is not None:
                                    MpCanvas.dx[var1_4][var2_9].free()
                                MpCanvas.dx[var1_4][var2_9] = None
                                var2_9 = var2_9 + 1
                            var1_4 = var1_4 + 1
                        var1_4 = 0
                        while var1_4 < 2:
                            MpCanvas.dy[var1_4][0] = None
                            MpCanvas.dy[var1_4][1] = None
                            var2_9 = 0
                            while var2_9 < 3:
                                if MpCanvas.dz[var1_4][var2_9] is not None:
                                    MpCanvas.dz[var1_4][var2_9].free()
                                MpCanvas.dz[var1_4][var2_9] = None
                                var2_9 = var2_9 + 1
                            var1_4 = var1_4 + 1
                        MpCanvas.X_v()
                    if MpCanvas.state_ticks < idiv(1000, MpCanvas.dc):
                        self.c_G(MpCanvas.screen_g)
                        self.H_v()
                        return
                    if MpCanvas.state_ticks == idiv(1000, MpCanvas.dc):
                        self.c_G(MpCanvas.screen_g)
                        MpCanvas.loop_i = 1
                        while MpCanvas.loop_i < 4:
                            if MpCanvas.fighter_present[MpCanvas.loop_i] and (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) != imod(MpCanvas.fighter_slot[0], 2)):
                                MpCanvas.fighter_present[MpCanvas.loop_i] = False
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        MpCanvas.bc = 0
                        self.send_request(1036)
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < 4:
                            MpCanvas.fighter_status[MpCanvas.loop_i] = 99
                            MpCanvas.fighter_status_ticks[MpCanvas.loop_i] = 0
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        MpCanvas.set_state(90)
                        MpCanvas.O = True
                        return
                    self.c_G(MpCanvas.screen_g)
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
                    if MpCanvas.state_ticks < idiv(1500, MpCanvas.dc):
                        MpCanvas.g_G(MpCanvas.screen_g)
                        self.c_G(MpCanvas.screen_g)
                        self.b_GI(MpCanvas.screen_g, 2)
                        return
                    if MpCanvas.state_ticks < idiv(1500, MpCanvas.dc):
                        break
                    MpCanvas.g_G(MpCanvas.screen_g)
                    self.c_G(MpCanvas.screen_g)
                    self.P_v()
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
                        MpCanvas.c = Consts.eX[9]
                        MpCanvas.k = 6
                        self.U_v()
                    self.draw_buffer()
                    Draw.draw_image(MpCanvas.screen_g, MpCanvas.mpic_images[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 40), (MpCanvas.center_y - 59), 0)
                    self.a_GTIIIIZZ(MpCanvas.screen_g, Consts.eM[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 39), (MpCanvas.center_y + 21), 78, 17, False, True)
                    MpCanvas.a_G(MpCanvas.screen_g)
                    if MpCanvas.popup_shown:
                        self.v_G(MpCanvas.screen_g)
                        break
                    self.c_II(5, 2)
                    return
                if _m4 or _sw3 == 11:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eM[0]
                        MpCanvas.k = 3
                        self.U_v()
                    Draw.draw_image(MpCanvas.screen_g, MpCanvas.buffer, 0, 0, 0)
                    self.a_GTIIIIZZ(MpCanvas.screen_g, Consts.eN[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 39), (MpCanvas.center_y - 19), 78, 17, False, True)
                    MpCanvas.a_G(MpCanvas.screen_g)
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 12:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eM[1]
                        MpCanvas.k = 2
                        self.U_v()
                    self.draw_buffer()
                    self.a_GTIIIIZZ(MpCanvas.screen_g, Consts.eO[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 45), (MpCanvas.center_y - 19), 90, 17, False, True)
                    MpCanvas.a_G(MpCanvas.screen_g)
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 16:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eM[2]
                        MpCanvas.k = 6
                        self.U_v()
                    self.draw_buffer()
                    self.a_GTIIIIZZ(MpCanvas.screen_g, Consts.eP[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 45), (MpCanvas.center_y - 19), 90, 17, False, True)
                    MpCanvas.a_G(MpCanvas.screen_g)
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 20:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.k = 2
                        self.w_G(MpCanvas.buffer_g)
                    self.draw_buffer()
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 2:
                        if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 56), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 20)), 111, 14, 3)
                            self.draw_text_colored(MpCanvas.screen_g, Consts.eX[(38 + MpCanvas.loop_i)], idiv(MpCanvas.screen_w, 2), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 20)), 1, 0xFFFFFF)
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 21:
                    _m4 = True
                    var1_6 = (MpCanvas.center_y - 48)
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.letter_cursor = 0
                        MpCanvas.input_text = ""
                        self.f_GI(MpCanvas.buffer_g, var1_6)
                    self.draw_buffer()
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (var1_6 + 61), MpCanvas.input_text, 0x41FF41)
                    MpCanvas.draw_letter_grid(MpCanvas.letter_cursor, (var1_6 + 75))
                    if imod(MpCanvas.state_ticks, 4) < 2:
                        var2_10 = MpCanvas.font_white.string_width(MpCanvas.input_text)
                        if len(MpCanvas.input_text) == 12:
                            var2_10 = (var2_10 - (MpCanvas.font_white.string_width("A") * 2))
                        MpCanvas.draw_line_color(MpCanvas.screen_g, (MpCanvas.center_x + idiv(var2_10, 2)), (var1_6 + 71), ((MpCanvas.center_x + idiv(var2_10, 2)) + 4), (var1_6 + 71), 0xFFFFFF)
                    if len(MpCanvas.input_text) == 0:
                        self.c_II(4, 1)
                        break
                    self.c_II(4, 3)
                    return
                if _m4 or _sw3 == 80:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eP[0]
                    self.Z_v()
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 81:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eP[1]
                    self.aa_v()
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 82:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eP[2]
                        self.p_G(MpCanvas.buffer_g)
                    self.draw_buffer()
                    self.ab_v()
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 83:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eP[3]
                    self.ac_v()
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 84:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.letter_cursor = 0
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eP[4]
                        self.q_G(MpCanvas.buffer_g)
                    self.draw_buffer()
                    self.r_G(MpCanvas.screen_g)
                    if len(MpCanvas.input_text) == 0:
                        self.c_II(4, 1)
                        break
                    self.c_II(4, 3)
                    return
                if _m4 or _sw3 == 88:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eM[3]
                        MpCanvas.k = 3
                        self.o_G(MpCanvas.buffer_g)
                    self.draw_buffer()
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 3:
                        if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                            self.draw_text_colored(MpCanvas.screen_g, Consts.eW[MpCanvas.loop_i], (MpCanvas.center_x - 28), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0xFFFFFF)
                            _sw9 = MpCanvas.loop_i
                            _m10 = False
                            while True:
                                if _m10 or _sw9 == 0:
                                    _m10 = True
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.eW[(3 + MpCanvas.speed)], (MpCanvas.center_x + 33), (MpCanvas.center_y - 15), 1, 0xFFFFFF)
                                    break
                                if _m10 or _sw9 == 1:
                                    _m10 = True
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.eW[(8 + MpCanvas.invitation)], (MpCanvas.center_x + 33), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0xFFFFFF)
                                    break
                                if _m10 or _sw9 == 2:
                                    _m10 = True
                                    if MpCanvas.get_volume() > 0:
                                        var2_11 = 0
                                        while var2_11 < MpCanvas.get_volume():
                                            Draw.fill_rect(MpCanvas.screen_g, ((MpCanvas.center_x + 21) + (5 * var2_11)), ((MpCanvas.center_y - 13) + (MpCanvas.loop_i * 19)), 3, 8, 0xFFFFFF)
                                            var2_11 = var2_11 + 1
                                        break
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.eW[(6 + ((0 if (MpCanvas.get_volume() > 0) else 1)))], (MpCanvas.center_x + 33), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0xFFFFFF)
                                break
                            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 58), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 19)), 61, 14, 3)
                            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x + 13), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 19)), 39, 14, 3)
                            if imod(MpCanvas.state_ticks, 4) < 2:
                                MpCanvas.c_IIM((MpCanvas.center_x + 6), ((MpCanvas.center_y - 13) + (MpCanvas.loop_i * 19)), MpCanvas.arrow_images[1])
                                MpCanvas.b_IIM((MpCanvas.center_x + 59), ((MpCanvas.center_y - 13) + (MpCanvas.loop_i * 19)), MpCanvas.arrow_images[1])
                        else:
                            _sw11 = MpCanvas.loop_i
                            _m12 = False
                            while True:
                                if _m12 or _sw11 == 0:
                                    _m12 = True
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.eW[(3 + MpCanvas.speed)], (MpCanvas.center_x + 33), (MpCanvas.center_y - 15), 1, 0x646464)
                                    break
                                if _m12 or _sw11 == 1:
                                    _m12 = True
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.eW[(8 + MpCanvas.invitation)], (MpCanvas.center_x + 33), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0x646464)
                                    break
                                if _m12 or _sw11 == 2:
                                    _m12 = True
                                    if MpCanvas.get_volume() > 0:
                                        var2_11 = 0
                                        while var2_11 < MpCanvas.get_volume():
                                            Draw.fill_rect(MpCanvas.screen_g, ((MpCanvas.center_x + 21) + (5 * var2_11)), ((MpCanvas.center_y - 13) + (MpCanvas.loop_i * 19)), 3, 8, 0x646464)
                                            var2_11 = var2_11 + 1
                                        break
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.eW[(6 + ((0 if (MpCanvas.get_volume() > 0) else 1)))], (MpCanvas.center_x + 33), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0x646464)
                                break
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 7:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eX[64]
                        self.k_G(MpCanvas.buffer_g)
                    self.draw_buffer()
                    self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 112, 48, 0)
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 18), _js(Consts.eX[64], "!"), 0xFFFFFF)
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 6), MpCanvas.user_id, 0xFFFFFF)
                    self.r_I((MpCanvas.center_y + 9))
                    return
                if _m4 or _sw3 == 6:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eX[18]
                        self.k_G(MpCanvas.buffer_g)
                    self.r_v()
                    return
                if _m4 or _sw3 == 3:
                    _m4 = True
                    self.draw_buffer()
                    if MpCanvas.state_ticks > idiv(20000, MpCanvas.dc):
                        MpCanvas.cw = 7
                        self.on_disconnect()
                        return
                    self.ae_v()
                    return
                if _m4 or _sw3 == 10000:
                    _m4 = True
                    self.draw_buffer()
                    if MpCanvas.state_ticks == 1:
                        self.connect()
                    if MpCanvas.state_ticks > idiv(20000, MpCanvas.dc):
                        MpCanvas.cw = 7
                        self.on_disconnect()
                        return
                    self.ae_v()
                    return
                if _m4 or _sw3 == 4:
                    _m4 = True
                    self.draw_buffer()
                    self.ad_v()
                    if MpCanvas.popup_shown:
                        self.v_G(MpCanvas.screen_g)
                        break
                    if (MpCanvas.cw == 7) or (MpCanvas.cw == 1):
                        self.c_II(5, 2)
                    return
                if _m4 or _sw3 == 5:
                    _m4 = True
                    Draw.fill_rect(MpCanvas.screen_g, 0, 0, MpCanvas.canvas_w, MpCanvas.canvas_h, 0)
                    self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 120, 100, 0)
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) - 10), Consts.eX[35], 0xFFFFFF)
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) + 5), Consts.eX[36], 0xFFFFFF)
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 2:
                        if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                            self.draw_text_colored(MpCanvas.screen_g, Consts.eX[(40 + MpCanvas.loop_i)], ((MpCanvas.center_x - 28) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 28), 1, 0xFFFFFF)
                            self.draw_box(MpCanvas.screen_g, ((MpCanvas.center_x - 42) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 25), 29, 14, 3)
                        else:
                            self.draw_box(MpCanvas.screen_g, ((MpCanvas.center_x - 42) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 25), 29, 14, 2)
                            self.draw_text_colored(MpCanvas.screen_g, Consts.eX[(40 + MpCanvas.loop_i)], ((MpCanvas.center_x - 28) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 28), 1, 0x646464)
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
                        MpCanvas.c = Consts.eV[0]
                        self.draw_window_bg(MpCanvas.buffer_g)
                    self.draw_buffer()
                    self.draw_popup()
                    return
                if _m4 or _sw3 == 160:
                    _m4 = True
                    self.draw_buffer()
                    _sw13 = MpCanvas.al
                    _m14 = False
                    while True:
                        if _m14 or _sw13 == 0:
                            _m14 = True
                            MpCanvas.bJ = len(MpCanvas.ag)
                            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, ((MpCanvas.bJ * 7) + 6), 45, 0)
                            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 13), MpCanvas.ag, 16400640)
                            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y + 2), MpCanvas.ah, 16400640)
                            raise _Brk_block1_457()
                        if _m14 or _sw13 == 1:
                            _m14 = True
                            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 120, 100, 0)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) - 10), MpCanvas.ag, 16400640)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) + 5), MpCanvas.ah, 16400640)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 21) + 20), Consts.eX[19], 16400640)
                            MpCanvas.loop_i = 0
                            while MpCanvas.loop_i < 2:
                                if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.eX[(40 + MpCanvas.loop_i)], ((MpCanvas.center_x - 28) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 28), 1, 16400640)
                                    self.draw_box(MpCanvas.screen_g, ((MpCanvas.center_x - 42) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 25), 29, 14, 3)
                                else:
                                    self.draw_box(MpCanvas.screen_g, ((MpCanvas.center_x - 42) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 25), 29, 14, 2)
                                    self.draw_text_colored(MpCanvas.screen_g, Consts.eX[(40 + MpCanvas.loop_i)], ((MpCanvas.center_x - 28) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 28), 1, 0xFFFFFF)
                                MpCanvas.loop_i = MpCanvas.loop_i + 1
                            raise _Brk_block1_457()
                        if _m14 or _sw13 == 2:
                            _m14 = True
                            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 120, 100, 0)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) - 10), MpCanvas.ag, 16400640)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) + 5), MpCanvas.ah, 16400640)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) + 20), MpCanvas.ai, 16400640)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) + 35), MpCanvas.aj, 16400640)
                            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 26) + 50), MpCanvas.ak, 16400640)
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
                        MpCanvas.ds = self.load_image("/outro.png")
                    Draw.fill_rect(MpCanvas.screen_g, 0, 0, MpCanvas.screen_w, MpCanvas.screen_h, 0)
                    var2_13 = MpCanvas.ds.getWidth()
                    Gfx.draw_image_part(MpCanvas.ds, (MpCanvas.center_x - idiv(var2_13, 2)), (MpCanvas.center_y - 10), var2_13, 19, 0, 0)
                    Gfx.draw_image_part(MpCanvas.ds, (MpCanvas.center_x - idiv(var2_13, 2)), (MpCanvas.screen_h - 26), var2_13, 23, 0, 19)
                    if MpCanvas.state_ticks <= 30:
                        break
                    MpCanvas.midlet.destroyApp(True)
                    MpCanvas.midlet.notifyDestroyed()
                    return
                if _m4 or _sw3 == 87:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.c = Consts.eM[4]
                        MpCanvas.k = 6
                        self.U_v()
                    self.draw_buffer()
                    self.a_GTIIIIZZ(MpCanvas.screen_g, Consts.eQ[MpCanvas.cursor_stack[MpCanvas.stack_depth]], (MpCanvas.center_x - 39), (MpCanvas.center_y - 19), 78, 17, False, True)
                    MpCanvas.a_G(MpCanvas.screen_g)
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 89:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.be = 0
                    self.T_v()
                    self.c_II((-1), 1)
                    return
                if _m4 or _sw3 == 85:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        _sw15 = MpCanvas.state
                        if _sw15 == 85:
                            MpCanvas.c = Consts.eP[5]
                        self.s_G(MpCanvas.buffer_g)
                    self.draw_buffer()
                    self.t_G(MpCanvas.screen_g)
                    if len(MpCanvas.input_text) == 0:
                        self.c_II(4, 1)
                        break
                    self.c_II(4, 3)
                    return
                if _m4 or _sw3 == 86:
                    _m4 = True
                    if MpCanvas.state_ticks < 2:
                        MpCanvas.state_ticks = 2
                        MpCanvas.k = 2
                    self.draw_buffer()
                    self.t_G(MpCanvas.screen_g)
                    self.u_G(MpCanvas.screen_g)
                break
        except _Brk_block1_457:
            pass

    @staticmethod
    def b_I(n2):  # g.java:1467
        MpCanvas.d = n2

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
    def b_IIM(n2, n3, image):  # g.java:1548
        n4 = (idiv(image.getWidth(), 2) + 1)
        n5 = image.getHeight()
        Draw.draw_image_part(MpCanvas.screen_g, image, (n2 - n4), n3, n4, n5, (n4 - 1), 0)

    @staticmethod
    def b_GIIM(graphics, n2, n3, image):  # g.java:1554
        n4 = (idiv(image.getWidth(), 2) + 1)
        n5 = image.getHeight()
        Draw.draw_image_part(graphics, image, (n2 - n4), n3, n4, n5, (n4 - 1), 0)

    @staticmethod
    def a_GIIIM(graphics, n2, n3, n4, image):  # g.java:1560
        n5 = (idiv(image.getWidth(), 2) + 1)
        Draw.draw_image_part(graphics, image, (n2 - n5), n3, n5, n4, (n5 - 1), 0)

    @staticmethod
    def a_IIMZ(n2, n3, image, bl):  # g.java:1565
        if bl:
            n4 = (idiv(image.getWidth(), 2) + 1)
            n5 = image.getHeight()
            Draw.draw_image_part(MpCanvas.screen_g, image, (n2 - n4), n3, n4, n5, (n4 - 1), 0)
            return
        Draw.draw_image(MpCanvas.screen_g, image, (n2 - image.getWidth()), n3, 0)

    @staticmethod
    def a_GIIMII(graphics, n2, n3, image, n4, n5):  # g.java:1575
        n6 = (idiv(image.getWidth(), 2) + 1)
        Draw.draw_image_part(graphics, image, n2, n3, n6, n4, 0, (n4 * n5))

    @staticmethod
    def b_GIIIM(graphics, n2, n3, n4, image):  # g.java:1580
        n5 = (idiv(image.getWidth(), 2) + 1)
        Draw.draw_image_part(graphics, image, (n2 - n5), n3, n5, n4, (n5 - 1), n4)

    @staticmethod
    def c_IIM(n2, n3, image):  # g.java:1585
        n4 = (idiv(image.getWidth(), 2) + 1)
        n5 = image.getHeight()
        Draw.draw_image_part(MpCanvas.screen_g, image, n2, n3, n4, n5, 0, 0)

    @staticmethod
    def c_GIIM(graphics, n2, n3, image):  # g.java:1591
        n4 = (idiv(image.getWidth(), 2) + 1)
        n5 = image.getHeight()
        Draw.draw_image_part(graphics, image, n2, n3, n4, n5, 0, 0)

    @staticmethod
    def c_GIIIM(graphics, n2, n3, n4, image):  # g.java:1597
        n5 = (idiv(image.getWidth(), 2) + 1)
        Draw.draw_image_part(graphics, image, n2, n3, n5, n4, 0, 0)

    def draw_buffer(self):  # g.java:1602
        Draw.draw_image(MpCanvas.screen_g, MpCanvas.buffer, 0, 0, 0)
        if (MpCanvas.state >= 90) and (MpCanvas.state <= 105):
            MpCanvas.g_G(MpCanvas.screen_g)

    def send_request(self, n2):  # g.java:1609
        if (n2 == 262) or (n2 == 278):
            MpCanvas.login_time = system.currentTimeMillis()
        if NetThread.connected and (idiv(((system.currentTimeMillis() - MpCanvas.login_time)), 1000) > 45):
            MpCanvas.dZ = 0
            MpCanvas.cw = 13
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
            NetThread.write_byte(i8(MpCanvas.ab))
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
                if MpCanvas.skill_levels[(MpCanvas.cB[MpCanvas.loop_i] - 3)] != 99:
                    NetThread.write_byte(MpCanvas.cB[MpCanvas.loop_i])
                    MpCanvas.loop_j = MpCanvas.loop_j + 1
                MpCanvas.loop_i = MpCanvas.loop_i + 1
            MpCanvas.loop_i = MpCanvas.loop_j
            while MpCanvas.loop_i < 4:
                NetThread.write_byte(i8(99))
                MpCanvas.loop_i = MpCanvas.loop_i + 1
        elif _sw17 == 1280:
            NetThread.write_string(MpCanvas.input_text, 8)
        elif _sw17 == 258:
            NetThread.write_int(MpCanvas.aO)
        elif _sw17 == 1027:
            NetThread.write_byte(i8(MpCanvas.fighter_slot[MpCanvas.bA]))
            NetThread.write_byte(i8(MpCanvas.bB))
            NetThread.write_byte(i8(MpCanvas.aS))
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
        MpCanvas.du[0] = None
        MpCanvas.du[1] = None
        n3 = 0
        while n3 < 3:
            if MpCanvas.dv[n3] is not None:
                MpCanvas.dv[n3].free()
            MpCanvas.dv[n3] = None
            n3 = n3 + 1
        n3 = 0
        while n3 < 10:
            MpCanvas.dw[n3][0] = None
            MpCanvas.dw[n3][1] = None
            n2 = 0
            while n2 < 3:
                if MpCanvas.dx[n3][n2] is not None:
                    MpCanvas.dx[n3][n2].free()
                MpCanvas.dx[n3][n2] = None
                n2 = n2 + 1
            n3 = n3 + 1
        n3 = 0
        while n3 < 2:
            MpCanvas.dy[n3][0] = None
            MpCanvas.dy[n3][1] = None
            n2 = 0
            while n2 < 3:
                if MpCanvas.dz[n3][n2] is not None:
                    MpCanvas.dz[n3][n2].free()
                MpCanvas.dz[n3][n2] = None
                n2 = n2 + 1
            n3 = n3 + 1
        n3 = 0
        while n3 < 2:
            MpCanvas.dA[n3][0] = None
            MpCanvas.dA[n3][1] = None
            n2 = 0
            while n2 < 3:
                if MpCanvas.dB[n3][n2] is not None:
                    MpCanvas.dB[n3][n2].free()
                MpCanvas.dB[n3][n2] = None
                n2 = n2 + 1
            n3 = n3 + 1
        n3 = 0
        while n3 < 2:
            MpCanvas.dC[n3][0] = None
            MpCanvas.dC[n3][1] = None
            n2 = 0
            while n2 < 3:
                if MpCanvas.dD[n3][n2] is not None:
                    MpCanvas.dD[n3][n2].free()
                MpCanvas.dD[n3][n2] = None
                n2 = n2 + 1
            n3 = n3 + 1
        MpCanvas.dF[0] = None
        MpCanvas.dF[1] = None
        n3 = 0
        while n3 < 3:
            if MpCanvas.dG[n3] is not None:
                MpCanvas.dG[n3].free()
            MpCanvas.dG[n3] = None
            n3 = n3 + 1
        MpCanvas.dH[0] = None
        MpCanvas.dH[1] = None
        if MpCanvas.dI[0] is not None:
            MpCanvas.dI[0].free()
        MpCanvas.dI[0] = None
        MpCanvas.dJ[0] = None
        MpCanvas.dJ[1] = None
        if MpCanvas.dK[0] is not None:
            MpCanvas.dK[0].free()
        MpCanvas.dK[0] = None
        MpCanvas.dL[0] = None
        MpCanvas.dL[1] = None
        if MpCanvas.dM[0] is not None:
            MpCanvas.dM[0].free()
        MpCanvas.dM[0] = None
        MpCanvas.dN[0] = None
        MpCanvas.dN[0] = None
        if MpCanvas.dO[0] is not None:
            MpCanvas.dO[0].free()
        MpCanvas.dO[0] = None
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
        MpCanvas.X_v()
        if MpCanvas.arrow_images[1] is None:
            MpCanvas.arrow_images[1] = self.load_image("/menuarrow1.png")
        self.load_menu_images()

    def on_answer(self, k2):  # g.java:1888
        MpCanvas.u = False
        if MpCanvas.paused or (MpCanvas.pause_request == 1):
            MpCanvas.cw = 7
            MpCanvas.popup_shown = False
            MpCanvas.disconnect()
            MpCanvas.b_I((-1))
            self.push_state(4)
            return
        if NetThread.last_opcode == 280:
            MpCanvas.cw = 17
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
                        MpCanvas.cv = 0
                        MpCanvas.A = False
                        MpCanvas.set_state(10000)
                        return
                    by2 = k2.read_s8()
                    self.on_disconnect()
                    if by2 == 0:
                        MpCanvas.popup_kind = 0
                        MpCanvas.cw = 14
                    elif by2 == 1:
                        MpCanvas.popup_kind = 1
                        MpCanvas.cw = 15
                    else:
                        MpCanvas.popup_kind = 0
                        MpCanvas.cw = 0
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
                        MpCanvas.aK = k2.read_s8()
                        MpCanvas.aL = k2.read_s8()
                        MpCanvas.aM = k2.read_s8()
                        if MpCanvas.aL < 0:
                            MpCanvas.aL = 0
                        if MpCanvas.aM < 0:
                            MpCanvas.aM = 0
                        MpCanvas.notices_left = k2.read_s8()
                        k2.read_string(8)
                        k2.read_string(8)
                        k2.read_s8()
                        k2.read_s8()
                        k2.read_s8()
                        MpCanvas.title_image = None
                        MpCanvas.press_image = None
                        MpCanvas.gamevil_image = None
                        MpCanvas.X_v()
                        if MpCanvas.dX:
                            if MpCanvas.P:
                                self.reset_state_stack(7)
                                return
                            self.reset_state_stack(10)
                            return
                        if MpCanvas.notices_left > 0:
                            MpCanvas.aO = 1
                            self.send_request(258)
                            return
                        MpCanvas.notices_left = 0
                        self.reset_state_stack(7)
                        return
                    elif _sw20 == (-2):
                        MpCanvas.cw = 1
                        self.on_disconnect()
                        return
                    elif _sw20 == (-9):
                        MpCanvas.cw = 8
                        self.on_disconnect()
                        return
                    MpCanvas.cw = 7
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
                            MpCanvas.cw = 0
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
                            MpCanvas.cw = 0
                            self.push_state(4)
                        break
                    return
                if _m19 or _sw18 == 259:
                    _m19 = True
                    _sw27 = MpCanvas.answer_status
                    if _sw27 == 1:
                        n4 = 0
                        while n4 < 4:
                            MpCanvas.bF[n4] = k2.read_string(16)
                            n4 = n4 + 1
                        MpCanvas.notices_left = k2.read_s8()
                        MpCanvas.bd = 1
                        MpCanvas.set_state(6)
                        return
                    MpCanvas.cw = 0
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
                        MpCanvas.w = True
                        self.free_frame_images()
                        MpCanvas.w = False
                        MpCanvas.O = True
                        return
                    MpCanvas.cw = 0
                    _sw29 = MpCanvas.answer_status
                    if _sw29 == (-11):
                        MpCanvas.cw = 8
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
                        MpCanvas.w = True
                        self.free_frame_images()
                        MpCanvas.w = False
                        MpCanvas.O = True
                        return
                    _sw31 = MpCanvas.answer_status
                    if _sw31 == (-3):
                        MpCanvas.cw = 2
                    elif _sw31 == (-4):
                        MpCanvas.cw = 3
                    elif _sw31 == (-5):
                        MpCanvas.cw = 4
                    elif _sw31 == (-12):
                        MpCanvas.cw = 9
                    elif _sw31 == (-16):
                        MpCanvas.cw = 18
                    else:
                        MpCanvas.cw = 0
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
                        MpCanvas.w = True
                        self.free_frame_images()
                        MpCanvas.w = False
                        MpCanvas.O = True
                        return
                    MpCanvas.cw = 0
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
                            MpCanvas.bb = MpCanvas.bb + 1
                        else:
                            MpCanvas.bc = MpCanvas.bc + 1
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
                        MpCanvas.cr[MpCanvas.cur_slot] = k2.read_s8()
                        MpCanvas.fighter_alt_name[MpCanvas.cur_slot] = k2.read_string(8)
                        MpCanvas.fighter_mp[MpCanvas.cur_slot] = 0
                        MpCanvas.place_fighter(MpCanvas.cur_slot)
                        MpCanvas.fighter_blink[MpCanvas.cur_slot] = imod(abs(MpCanvas.rng.nextInt()), 4)
                        MpCanvas.fighter_status[MpCanvas.cur_slot] = 99
                        MpCanvas.fighter_status_ticks[MpCanvas.cur_slot] = 0
                        MpCanvas.bj = True
                        if MpCanvas.state != 4:
                            break
                        MpCanvas.set_state(90)
                        MpCanvas.O = True
                        return
                    MpCanvas.cw = 0
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
                        MpCanvas.bB = 99
                        MpCanvas.b_I((10 - MpCanvas.speed))
                        MpCanvas.ba = 10
                        MpCanvas.G = False
                        MpCanvas.set_state(94)
                    return
                if _m19 or _sw18 == 1028:
                    _m19 = True
                    _sw36 = MpCanvas.answer_status
                    if _sw36 == 1:
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < 4:
                            MpCanvas.bi = False
                            MpCanvas.loop_j = 0
                            while MpCanvas.loop_j < 4:
                                if MpCanvas.fighter_present[MpCanvas.loop_j] and (MpCanvas.fighter_slot[MpCanvas.loop_j] == MpCanvas.loop_i):
                                    MpCanvas.cur_slot = MpCanvas.loop_j
                                    MpCanvas.bi = True
                                    break
                                MpCanvas.loop_j = MpCanvas.loop_j + 1
                            if MpCanvas.bi:
                                MpCanvas.turn_actions[MpCanvas.cur_slot] = k2.read_s8()
                            else:
                                MpCanvas.bJ = k2.read_s8()
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
                                MpCanvas.bb = MpCanvas.bb - 1
                                raise _Brk_block0_1631()
                            MpCanvas.bc = MpCanvas.bc - 1
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
                        MpCanvas.cw = 6
                        self.push_state(4)
                        return
                    elif _sw42 == (-49):
                        MpCanvas.cw = 5
                        self.push_state(4)
                        return
                    elif _sw42 == (-15):
                        MpCanvas.cw = 5
                        self.push_state(4)
                        return
                    MpCanvas.cw = 0
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
                        MpCanvas.B = 1
                        return
                    elif _sw43 == (-49):
                        MpCanvas.cw = 5
                        self.push_state(4)
                        return
                    MpCanvas.cw = 0
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
                        MpCanvas.cw = 5
                        self.push_state(4)
                        return
                    MpCanvas.cw = 0
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
                    MpCanvas.cw = 0
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
                            MpCanvas.bp = k2.read_s8()
                            MpCanvas.skill_levels[(MpCanvas.bp - 3)] = k2.read_s8()
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < MpCanvas.skill_slot_count:
                            MpCanvas.cB[MpCanvas.loop_i] = MpCanvas.skill_slots[MpCanvas.loop_i]
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        while MpCanvas.loop_i < 4:
                            MpCanvas.loop_j = 0
                            while MpCanvas.loop_j < 11:
                                MpCanvas.bq = False
                                MpCanvas.loop_k = 0
                                while MpCanvas.loop_k < MpCanvas.loop_i:
                                    if MpCanvas.cB[MpCanvas.loop_k] == (3 + MpCanvas.loop_j):
                                        MpCanvas.bq = True
                                        break
                                    MpCanvas.loop_k = MpCanvas.loop_k + 1
                                if not MpCanvas.bq:
                                    MpCanvas.cB[MpCanvas.loop_i] = i8(((3 + MpCanvas.loop_j)))
                                    break
                                MpCanvas.loop_j = MpCanvas.loop_j + 1
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        self.push_state(82)
                        return
                    MpCanvas.cw = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 1292:
                    _m19 = True
                    _sw47 = MpCanvas.answer_status
                    if _sw47 == 1:
                        MpCanvas.loop_j = 0
                        MpCanvas.loop_i = 0
                        while MpCanvas.loop_i < 4:
                            if MpCanvas.skill_levels[(MpCanvas.cB[MpCanvas.loop_i] - 3)] != 99:
                                MpCanvas.skill_slots[MpCanvas.loop_j] = MpCanvas.cB[MpCanvas.loop_i]
                                MpCanvas.loop_j = MpCanvas.loop_j + 1
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        MpCanvas.skill_slot_count = MpCanvas.loop_j
                        MpCanvas.loop_i = MpCanvas.loop_j
                        while MpCanvas.loop_i < 4:
                            MpCanvas.skill_slots[MpCanvas.loop_j] = 99
                            MpCanvas.loop_i = MpCanvas.loop_i + 1
                        self.pop_state()
                        return
                    MpCanvas.cw = 0
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
                    MpCanvas.cw = 0
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
                    MpCanvas.cw = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 1536:
                    _m19 = True
                    _sw50 = MpCanvas.answer_status
                    if _sw50 == 1:
                        MpCanvas.bd = k2.read_s8()
                        n6 = 0
                        while n6 < 4:
                            MpCanvas.bF[n6] = k2.read_string(16)
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
                    MpCanvas.cw = 0
                    self.push_state(4)
                    return
                if _m19 or _sw18 == 291:
                    _m19 = True
                    if MpCanvas.answer_status == 1:
                        self.pop_state()
                        return
                    MpCanvas.cw = 0
                    self.push_state(4)
                break
        except _Brk_block0_1631:
            pass

    def d_I(self, n2):  # g.java:2589
        if MpCanvas.state_ticks < 2:
            return
        if (n2 == (-3)) or (n2 == (-1)):
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] > 0:
                n3 = MpCanvas.stack_depth
                MpCanvas.cursor_stack[n3] = (MpCanvas.cursor_stack[n3] - 1)
            else:
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = (MpCanvas.k - 1)
        elif (n2 == (-4)) or (n2 == (-2)):
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] < (MpCanvas.k - 1):
                n4 = MpCanvas.stack_depth
                MpCanvas.cursor_stack[n4] = (MpCanvas.cursor_stack[n4] + 1)
            else:
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = 0
        if n2 == (-5):
            self.q_v()

    def e_I(self, n2):  # g.java:2613
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
            self.q_v()
            return
        if n2 == (-7):
            if (MpCanvas.state == 160) and (MpCanvas.al != 1):
                return
            MpCanvas.cursor_stack[MpCanvas.stack_depth] = 1
            self.q_v()

    def keyPressed(self, n2):  # g.java:2645
        if (n2 == (-32)) or (n2 == (-33)):
            return
        MpCanvas.key = n2
        if MpCanvas.paused:
            if MpCanvas.key == (-5):
                MpCanvas.request_pause(2)
            MpCanvas.key = (-999)

    def handle_key(self, var1_1):  # g.java:2661
        MpCanvas.dZ = 0
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
                    self.d_I(MpCanvas.key_in)
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
                        MpCanvas.aO = MpCanvas.aO + 1
                        self.send_request(258)
                        return
                    if MpCanvas.bd == 1:
                        self.reset_state_stack(7)
                        return
                    if MpCanvas.bd != 9:
                        break
                    MpCanvas.set_state(300)
                    return
                if _m53 or _sw52 == 7:
                    _m53 = True
                    MpCanvas.k = 2
                    MpCanvas.P = False
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
                        MpCanvas.P = True
                        MpCanvas.letter_cursor = 0
                        self.push_state(2)
                        return
                    if MpCanvas.key_in == (-7):
                        MpCanvas.popup_shown = True
                        MpCanvas.popup_cursor = 1
                        return
                    self.d_I(MpCanvas.key_in)
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
                                if MpCanvas.cB[MpCanvas.cursor_stack[MpCanvas.stack_depth]] > 3:
                                    v2 = MpCanvas.cursor_stack[MpCanvas.stack_depth]
                                    MpCanvas.cB[v2] = i8(((MpCanvas.cB[v2] - 1)))
                                else:
                                    MpCanvas.cB[MpCanvas.cursor_stack[MpCanvas.stack_depth]] = 13
                                MpCanvas.bq = False
                                MpCanvas.loop_i = 0
                                while MpCanvas.loop_i < 4:
                                    if (MpCanvas.loop_i != MpCanvas.cursor_stack[MpCanvas.stack_depth]) and (MpCanvas.cB[MpCanvas.cursor_stack[MpCanvas.stack_depth]] == MpCanvas.cB[MpCanvas.loop_i]):
                                        MpCanvas.bq = True
                                        raise _Cont_block47_2359()
                                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                            except _Cont_block47_2359:
                                pass
                            if not (MpCanvas.bq):
                                break
                    elif MpCanvas.key_in == (-4):
                        while True:
                            try:
                                if MpCanvas.cB[MpCanvas.cursor_stack[MpCanvas.stack_depth]] < 13:
                                    v3 = MpCanvas.cursor_stack[MpCanvas.stack_depth]
                                    MpCanvas.cB[v3] = i8(((MpCanvas.cB[v3] + 1)))
                                else:
                                    MpCanvas.cB[MpCanvas.cursor_stack[MpCanvas.stack_depth]] = 3
                                MpCanvas.bq = False
                                MpCanvas.loop_i = 0
                                while MpCanvas.loop_i < 4:
                                    if (MpCanvas.loop_i != MpCanvas.cursor_stack[MpCanvas.stack_depth]) and (MpCanvas.cB[MpCanvas.cursor_stack[MpCanvas.stack_depth]] == MpCanvas.cB[MpCanvas.loop_i]):
                                        MpCanvas.bq = True
                                        raise _Cont_block49_2378()
                                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                            except _Cont_block49_2378:
                                pass
                            if not (MpCanvas.bq):
                                break
                    if (MpCanvas.key_in != (-5)) and (MpCanvas.key_in != (-7)):
                        break
                    self.q_v()
                    return
                if _m53 or _sw52 == 84:
                    _m53 = True
                    if MpCanvas.key_in == (-7):
                        if len(MpCanvas.input_text) == 0:
                            if MpCanvas.B == 0:
                                self.pop_state()
                                return
                            MpCanvas.B = MpCanvas.B - 1
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
                        MpCanvas.cv = 5
                        MpCanvas.input_text = MpCanvas.trim_right(MpCanvas.input_text)
                        if MpCanvas.B == 0:
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
                        self.q_v()
                        return
                    if MpCanvas.key_in == (-5):
                        MpCanvas.key_in = (-4)
                        self.q_v()
                        return
                    if MpCanvas.key_in != (-7):
                        break
                    MpCanvas.save_options()
                    if MpCanvas.invitation != MpCanvas.invitation_saved:
                        MpCanvas.cv = 1
                        MpCanvas.set_state(3)
                        self.send_request(290)
                        return
                    self.pop_state()
                    self.start_sound(1)
                    return
                if _m53 or _sw52 == 89:
                    _m53 = True
                    if MpCanvas.key_in == (-3):
                        if MpCanvas.be > 0:
                            MpCanvas.be = MpCanvas.be - 1
                            return
                        MpCanvas.be = (Consts.ew[MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]] - 1)
                        return
                    if (MpCanvas.key_in == (-4)) or (MpCanvas.key_in == (-5)):
                        if MpCanvas.be < (Consts.ew[MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]] - 1):
                            MpCanvas.be = MpCanvas.be + 1
                            return
                        MpCanvas.be = 0
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
                    self.d_I(MpCanvas.key_in)
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
                            MpCanvas.cv = 2
                        elif _sw54 == 1:
                            MpCanvas.cv = 4
                        elif _sw54 == 2:
                            MpCanvas.cv = 4
                        MpCanvas.cv = 0
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
                    if MpCanvas.D:
                        if (MpCanvas.key_in == (-3)) or (MpCanvas.key_in == (-4)):
                            MpCanvas.E = imod(((MpCanvas.E + 1)), 2)
                            return
                        if MpCanvas.key_in != (-5):
                            break
                        if MpCanvas.E == 0:
                            MpCanvas.P = False
                            MpCanvas.disconnect()
                            MpCanvas.b_I((-1))
                            MpCanvas.cv = 0
                            MpCanvas.A = False
                            MpCanvas.set_state(10000)
                            return
                        MpCanvas.D = False
                        return
                    MpCanvas.bB = 99
                    if MpCanvas.key_in == (-1):
                        MpCanvas.bB = 2
                    elif MpCanvas.key_in == (-3):
                        MpCanvas.bB = 1
                    elif MpCanvas.key_in == (-4):
                        MpCanvas.bB = 0
                    elif MpCanvas.key_in == (-2):
                        if MpCanvas.skill_slot_count > 0:
                            MpCanvas.loop_k = 0
                            while MpCanvas.loop_k < MpCanvas.skill_slot_count:
                                if MpCanvas.fighter_mp[0] >= MpCanvas.skill_costs[(MpCanvas.skill_slots[MpCanvas.loop_k] - 3)]:
                                    MpCanvas.bB = 20
                                    break
                                MpCanvas.loop_k = MpCanvas.loop_k + 1
                    elif (MpCanvas.key_in == (-7)) and (not MpCanvas.G):
                        MpCanvas.G = True
                        MpCanvas.D = True
                        MpCanvas.E = 1
                        MpCanvas.F = system.currentTimeMillis()
                    if MpCanvas.bB == 20:
                        MpCanvas.set_state(95)
                        return
                    if MpCanvas.bB == 99:
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
                        MpCanvas.bB = MpCanvas.skill_slots[MpCanvas.skill_cursor]
                        MpCanvas.set_state(96)
                        return
                    if MpCanvas.key_in != (-7):
                        break
                    MpCanvas.bB = 99
                    MpCanvas.set_state(94)
                    return
                if _m53 or _sw52 == 96:
                    _m53 = True
                    if (MpCanvas.key_in == (-1)) or (MpCanvas.key_in == (-2)):
                        _sw55 = MpCanvas.bB
                        _m56 = False
                        while True:
                            if _m56 or _sw55 in (9, 10):
                                _m56 = True
                                MpCanvas.loop_i = 0
                                while MpCanvas.loop_i < 4:
                                    if (MpCanvas.fighter_present[MpCanvas.loop_i] and (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == imod(MpCanvas.fighter_slot[MpCanvas.bA], 2))) and (MpCanvas.fighter_slot[MpCanvas.loop_i] != MpCanvas.fighter_slot[MpCanvas.bA]):
                                        MpCanvas.bA = MpCanvas.loop_i
                                        raise _Brk_block0_2273()
                                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                                raise _Brk_block0_2273()
                            if _m56 or _sw55 in (0, 3, 4, 5, 6, 7):
                                _m56 = True
                                MpCanvas.loop_i = 1
                                while MpCanvas.loop_i < 4:
                                    if (MpCanvas.fighter_present[MpCanvas.loop_i] and (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == imod(MpCanvas.fighter_slot[MpCanvas.bA], 2))) and (MpCanvas.fighter_slot[MpCanvas.loop_i] != MpCanvas.fighter_slot[MpCanvas.bA]):
                                        MpCanvas.bA = MpCanvas.loop_i
                                        raise _Brk_block0_2273()
                                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                            if _m56 or _sw55 not in (9, 10, 0, 3, 4, 5, 6, 7):
                                _m56 = True
                                return
                            break
                    if MpCanvas.key_in == (-5):
                        self.B_v()
                        return
                    if MpCanvas.key_in != (-7):
                        break
                    _sw57 = MpCanvas.bB
                    if _sw57 in (3, 4, 5, 6, 7, 9, 10):
                        MpCanvas.set_state(95)
                        return
                    MpCanvas.set_state(94)
                    return
                if _m53 or _sw52 == 97:
                    _m53 = True
                    if (MpCanvas.state_ticks <= 0) or (MpCanvas.key_in != (-5)):
                        break
                    self.C_v()
                    return
                if _m53 or _sw52 == 105:
                    _m53 = True
                    if (MpCanvas.state_ticks <= idiv(1000, MpCanvas.dc)) or (MpCanvas.key_in != (-5)):
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
                        if (MpCanvas.cw != 7) and (MpCanvas.cw != 1):
                            break
                        MpCanvas.disconnect()
                        MpCanvas.popup_kind = 0
                        MpCanvas.P = True
                        MpCanvas.set_state(2)
                        MpCanvas.popup_shown = False
                        return
                    if MpCanvas.key_in == (-7):
                        if (MpCanvas.cw != 7) and (MpCanvas.cw != 1):
                            break
                        MpCanvas.popup_shown = True
                        MpCanvas.popup_cursor = 1
                        return
                    if MpCanvas.key_in != (-5):
                        break
                    if not NetThread.connected:
                        if ((MpCanvas.cw == 14) or (MpCanvas.cw == 15)) or (MpCanvas.cw == 16):
                            self.pop_state()
                            return
                        if MpCanvas.cw == 17:
                            MpCanvas.popup_kind = 0
                            MpCanvas.P = True
                            self.push_state(2)
                            return
                        if MpCanvas.cw != 1:
                            MpCanvas.cv = 0
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
                    if MpCanvas.cw == 1:
                        MpCanvas.set_state(4)
                        return
                    MpCanvas.cv = 0
                    MpCanvas.A = False
                    MpCanvas.set_state(10000)
                    return
                if _m53 or _sw52 == 2:
                    _m53 = True
                    self.popup_keys(MpCanvas.key_in)
                    return
                if _m53 or _sw52 in (86, 160):
                    _m53 = True
                    self.e_I(MpCanvas.key_in)
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
        MpCanvas.Q = 0
        MpCanvas.U = (-1)
        MpCanvas.X = (-1)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                MpCanvas.cc[MpCanvas.loop_i] = 0
                MpCanvas.cd[MpCanvas.loop_i] = 0
                MpCanvas.ce[MpCanvas.loop_i] = 0
                MpCanvas.fighter_hp_delta[MpCanvas.loop_i] = 0
                if MpCanvas.fighter_slot[MpCanvas.loop_i] == MpCanvas.turn_bytes[(0 + MpCanvas.bC)]:
                    MpCanvas.S = MpCanvas.loop_i
                    MpCanvas.fighter_hp_target[MpCanvas.loop_i] = MpCanvas.turn_hps[(0 + MpCanvas.bC)]
                    MpCanvas.fighter_mp_target[MpCanvas.loop_i] = MpCanvas.turn_bytes[(8 + MpCanvas.bC)]
                    MpCanvas.update_bars()
                if MpCanvas.fighter_slot[MpCanvas.loop_i] == MpCanvas.turn_bytes[(12 + MpCanvas.bC)]:
                    MpCanvas.T = MpCanvas.loop_i
                    MpCanvas.fighter_hp_target[MpCanvas.loop_i] = MpCanvas.turn_hps[(4 + MpCanvas.bC)]
                    MpCanvas.fighter_mp_target[MpCanvas.loop_i] = MpCanvas.turn_bytes[(20 + MpCanvas.bC)]
                    MpCanvas.update_bars()
                    _sw61 = MpCanvas.turn_bytes[(16 + MpCanvas.bC)]
                    _m62 = False
                    while True:
                        if _m62 or _sw61 == 1:
                            _m62 = True
                            if MpCanvas.turn_actions[MpCanvas.T] == 1:
                                MpCanvas.V = 4
                                break
                            MpCanvas.V = 1
                            break
                        if _m62 or _sw61 == 2:
                            _m62 = True
                            MpCanvas.V = 5
                        break
                if (MpCanvas.turn_bytes[(24 + MpCanvas.bC)] > 0) and (MpCanvas.fighter_slot[MpCanvas.loop_i] == MpCanvas.turn_bytes[(32 + MpCanvas.bC)]):
                    MpCanvas.U = MpCanvas.loop_i
                    MpCanvas.fighter_hp_target[MpCanvas.loop_i] = MpCanvas.turn_hps[(8 + MpCanvas.bC)]
                    MpCanvas.fighter_mp_target[MpCanvas.loop_i] = MpCanvas.turn_bytes[(40 + MpCanvas.bC)]
                    MpCanvas.update_bars()
                    _sw63 = MpCanvas.turn_bytes[(36 + MpCanvas.bC)]
                    _m64 = False
                    while True:
                        if _m64 or _sw63 == 1:
                            _m64 = True
                            if MpCanvas.turn_actions[MpCanvas.U] == 1:
                                MpCanvas.W = 4
                                break
                            MpCanvas.W = 1
                            break
                        if _m64 or _sw63 == 2:
                            _m64 = True
                            MpCanvas.W = 5
                        break
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        _sw65 = MpCanvas.turn_bytes[(4 + MpCanvas.bC)]
        if _sw65 in (3, 4, 5, 6, 7, 8):
            MpCanvas.cc[MpCanvas.S] = 8
        elif _sw65 in (2, 9, 10):
            MpCanvas.cc[MpCanvas.S] = 12
        elif _sw65 in (11, 12, 13):
            MpCanvas.cc[MpCanvas.S] = 13
        elif _sw65 == 0:
            MpCanvas.cc[MpCanvas.S] = 2
            MpCanvas.bl = idiv((((MpCanvas.canvas_w - 67) - 42)), Consts.eh[MpCanvas.cc[MpCanvas.S]])
            MpCanvas.bm = (0 if (MpCanvas.room_mode == 0) else ((0 if (idiv(MpCanvas.fighter_slot[MpCanvas.S], 2) == idiv(MpCanvas.turn_bytes[(12 + MpCanvas.bC)], 2)) else ((idiv(46, Consts.eh[MpCanvas.cc[MpCanvas.S]]) if (idiv(MpCanvas.fighter_slot[MpCanvas.S], 2) == 0) else idiv((-46), Consts.eh[MpCanvas.cc[MpCanvas.S]]))))))
        MpCanvas.R = Consts.eh[MpCanvas.cc[MpCanvas.S]]

    def login(self):  # g.java:3374
        if MpCanvas.A:
            self.send_request(278)
            return
        self.send_request(262)

    def connect(self):  # g.java:3382
        MpCanvas.eb = False
        if not NetThread.connected:
            if MpCanvas.net is None:
                MpCanvas.net = NetThread()
                MpCanvas.net.setPriority(10)
                MpCanvas.net.start()
            NetThread.set_game(self)
            MpCanvas.L = True
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
        MpCanvas.dX = True
        MpCanvas.b_I((-1))
        MpCanvas.sleep(100)

    def on_disconnect(self):  # g.java:3410
        MpCanvas.disconnect()
        if MpCanvas.cw > (-1):
            self.p_v()

    def p_v(self):  # g.java:3417
        if MpCanvas.aq:
            MpCanvas.aq = False
            return
        MpCanvas.set_state(4)

    def on_net_error(self, n2):  # g.java:3425
        if not MpCanvas.disconnecting:
            MpCanvas.cw = (7 if (n2 < 10) else n2)
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
            MpCanvas.cx = (n2 - idiv(n4, 2))
            MpCanvas.cy = (n3 - idiv(n5, 2))
            if n6 == 0:
                Draw.fill_rect(graphics, MpCanvas.cx, MpCanvas.cy, n4, n5, 0)
            Draw.draw_rect(graphics, (MpCanvas.cx + 1), (MpCanvas.cy + 1), (n4 - 2), (n5 - 2), 0xADAAAD)
            MpCanvas.c_GIIM(graphics, (MpCanvas.cx + Consts.eq[2]), (MpCanvas.cy + Consts.er[2]), MpCanvas.ui_images[2])
            MpCanvas.b_GIIM(graphics, ((MpCanvas.cx + n4) + Consts.eq[2]), (MpCanvas.cy + Consts.er[2]), MpCanvas.ui_images[2])
            MpCanvas.c_GIIM(graphics, (MpCanvas.cx + Consts.eq[3]), ((((MpCanvas.cy + n5) - 2) - 5) + Consts.er[3]), MpCanvas.ui_images[3])
            MpCanvas.b_GIIM(graphics, ((MpCanvas.cx + n4) + Consts.eq[3]), ((((MpCanvas.cy + n5) - 2) - 5) + Consts.er[3]), MpCanvas.ui_images[3])
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

    def q_v(self):  # g.java:3512
        _sw67 = MpCanvas.state
        try:
            _m68 = False
            while True:
                if _m68 or _sw67 == 160:
                    _m68 = True
                    _sw69 = MpCanvas.al
                    _m70 = False
                    while True:
                        if _m70 or _sw69 == 1:
                            _m70 = True
                            if MpCanvas.cursor_stack[MpCanvas.stack_depth] == 0:
                                MpCanvas.cv = 5
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
                    MpCanvas.cv = 1
                    MpCanvas.set_state(3)
                    self.send_request(1300)
                    return
                if _m68 or _sw67 in (162, 163, 164):
                    _m68 = True
                    MpCanvas.af = MpCanvas.state
                    MpCanvas.ab = ((((((MpCanvas.state_stack[MpCanvas.stack_depth] - 162) + 1)) * 10) + MpCanvas.cursor_stack[MpCanvas.stack_depth]) + 1)
                    MpCanvas.cv = 1
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
                            MpCanvas.cv = 1
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
                            MpCanvas.cv = 2
                            MpCanvas.set_state(3)
                            self.send_request(512)
                            raise _Brk_block0_2989()
                        if _m74 or _sw73 == 1:
                            _m74 = True
                            MpCanvas.room_mode = 1
                            MpCanvas.cv = 2
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
                            MpCanvas.cv = 3
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
                            MpCanvas.cv = 1
                            MpCanvas.set_state(3)
                            self.send_request(1296)
                            raise _Brk_block0_2989()
                        if _m78 or _sw77 == 1:
                            _m78 = True
                            MpCanvas.cv = 1
                            MpCanvas.set_state(3)
                            self.send_request(1287)
                            raise _Brk_block0_2989()
                        if _m78 or _sw77 == 2:
                            _m78 = True
                            MpCanvas.cv = 1
                            MpCanvas.set_state(3)
                            self.send_request(1289)
                            raise _Brk_block0_2989()
                        if _m78 or _sw77 == 3:
                            _m78 = True
                            MpCanvas.cv = 1
                            MpCanvas.set_state(3)
                            self.send_request(1298)
                            raise _Brk_block0_2989()
                        if _m78 or _sw77 == 4:
                            _m78 = True
                            MpCanvas.letter_cursor = 0
                            MpCanvas.B = 0
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
                    MpCanvas.cv = 5
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
                            MpCanvas.cv = 5
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

    def r_v(self):  # g.java:3746
        self.draw_buffer()
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 116, 76, 0)
        n2 = 0
        while n2 < 4:
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((MpCanvas.center_y - 31) + (12 * n2)), MpCanvas.bF[n2], 0xFFFFFF)
            n2 = n2 + 1
        self.r_I((MpCanvas.center_y + 22))

    def s_v(self):  # g.java:3757
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i] and (MpCanvas.loop_i != MpCanvas.S):
                _sw84 = MpCanvas.cc[MpCanvas.loop_i]
                if _sw84 == 0:
                    self.b_G(MpCanvas.screen_g)
                elif _sw84 in (1, 4):
                    self.t_v()
                elif _sw84 == 5:
                    self.u_v()
                elif _sw84 == 6:
                    self.v_v()
                else:
                    self.x_v()
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.loop_i = MpCanvas.S
        _sw85 = MpCanvas.cc[MpCanvas.S]
        if _sw85 in (2, 28):
            self.w_v()
            return
        elif _sw85 == 6:
            self.v_v()
            return
        self.x_v()

    def t_v(self):  # g.java:3801
        MpCanvas.cC = MpCanvas.cc[MpCanvas.loop_i]
        if MpCanvas.fighter_kind[MpCanvas.loop_i] == 2:
            MpCanvas.cC = (MpCanvas.cC + 21)
        MpCanvas.fighter_frame[MpCanvas.loop_i] = Consts.eg[MpCanvas.cC]
        n2 = MpCanvas.loop_i
        MpCanvas.fighter_x[n2] = (MpCanvas.fighter_x[n2] - 2)
        MpCanvas.cm[MpCanvas.loop_i] = (-1)
        self.c_GI(MpCanvas.screen_g, MpCanvas.loop_i)

    def u_v(self):  # g.java:3813
        MpCanvas.cC = (26 if (MpCanvas.fighter_kind[MpCanvas.loop_i] == 2) else 5)
        MpCanvas.fighter_frame[MpCanvas.loop_i] = Consts.eg[MpCanvas.cC]
        if MpCanvas.cd[MpCanvas.loop_i] == 0:
            n2 = MpCanvas.loop_i
            MpCanvas.fighter_x[n2] = (MpCanvas.fighter_x[n2] - 6)
            self.start_sound(3)
        elif MpCanvas.cd[MpCanvas.loop_i] == 1:
            n3 = MpCanvas.loop_i
            MpCanvas.fighter_x[n3] = (MpCanvas.fighter_x[n3] - 2)
        MpCanvas.cm[MpCanvas.loop_i] = (-1)
        self.c_GI(MpCanvas.screen_g, MpCanvas.loop_i)

    def v_v(self):  # g.java:3828
        MpCanvas.cC = (27 if (MpCanvas.fighter_kind[MpCanvas.loop_i] == 2) else 6)
        MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.eg[MpCanvas.cC] + MpCanvas.Q)
        MpCanvas.cm[MpCanvas.loop_i] = (-1)
        self.c_GI(MpCanvas.screen_g, MpCanvas.loop_i)

    def w_v(self):  # g.java:3835
        MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.eg[23] if (MpCanvas.fighter_kind[MpCanvas.loop_i] == 2) else Consts.eg[2])
        n2 = MpCanvas.loop_i
        MpCanvas.fighter_x[n2] = (MpCanvas.fighter_x[n2] + MpCanvas.bl)
        n3 = MpCanvas.loop_i
        MpCanvas.fighter_y[n3] = (MpCanvas.fighter_y[n3] + MpCanvas.bm)
        MpCanvas.cm[MpCanvas.loop_i] = (-1)
        self.c_GI(MpCanvas.screen_g, MpCanvas.loop_i)

    def x_v(self):  # g.java:3845
        MpCanvas.cC = MpCanvas.cc[MpCanvas.loop_i]
        if (MpCanvas.fighter_kind[MpCanvas.loop_i] == 2) and (MpCanvas.cC == 3):
            MpCanvas.cC = 24
        if (MpCanvas.cC == 12) and (MpCanvas.Q >= 4):
            MpCanvas.bo = MpCanvas.Q
            MpCanvas.Q = 4
        MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.eg[MpCanvas.cC] + MpCanvas.Q)
        MpCanvas.bJ = Consts.ep[MpCanvas.cC][((3 * MpCanvas.Q) + 1)]
        n2 = MpCanvas.loop_i
        MpCanvas.fighter_x[n2] = (MpCanvas.fighter_x[n2] + ((((-1) if (((MpCanvas.bJ & 0x80)) > 0) else 1)) * ((MpCanvas.bJ & 0x7F))))
        MpCanvas.bJ = Consts.ep[MpCanvas.cC][((3 * MpCanvas.Q) + 2)]
        n3 = MpCanvas.loop_i
        MpCanvas.fighter_y[n3] = (MpCanvas.fighter_y[n3] + ((((-1) if (((MpCanvas.bJ & 0x80)) > 0) else 1)) * ((MpCanvas.bJ & 0x7F))))
        self.c_GI(MpCanvas.screen_g, MpCanvas.loop_i)
        if (MpCanvas.cC == 12) and (MpCanvas.Q >= 4):
            MpCanvas.Q = MpCanvas.bo

    def b_G(self, graphics):  # g.java:3867
        if MpCanvas.fighter_hp[MpCanvas.loop_i] > 0:
            if ((((MpCanvas.state == 104) or (MpCanvas.state == 105))) and (MpCanvas.fighter_kind[MpCanvas.loop_i] != 2)) and (MpCanvas.battle_won == 1):
                if MpCanvas.state_ticks < 3:
                    MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.eg[MpCanvas.cC] + MpCanvas.state_ticks)
                    n2 = MpCanvas.loop_i
                    MpCanvas.fighter_x[n2] = (MpCanvas.fighter_x[n2] + ((((-1) if (((MpCanvas.bJ & 0x80)) > 0) else 1)) * ((MpCanvas.bJ & 0x7F))))
                    n3 = MpCanvas.loop_i
                    MpCanvas.fighter_y[n3] = (MpCanvas.fighter_y[n3] + ((((-1) if (((MpCanvas.bJ & 0x80)) > 0) else 1)) * ((MpCanvas.bJ & 0x7F))))
            else:
                if imod(MpCanvas.state_ticks, 4) == MpCanvas.fighter_blink[MpCanvas.loop_i]:
                    MpCanvas.fighter_frame[MpCanvas.loop_i] = imod(idiv(MpCanvas.state_ticks, 4), 2)
                if (MpCanvas.fighter_frame[MpCanvas.loop_i] != 0) and (MpCanvas.fighter_frame[MpCanvas.loop_i] != 1):
                    MpCanvas.fighter_frame[MpCanvas.loop_i] = 0
        else:
            MpCanvas.fighter_frame[MpCanvas.loop_i] = (Consts.eg[6] + 1)
        MpCanvas.cm[MpCanvas.loop_i] = (-1)
        if ((MpCanvas.cc[MpCanvas.S] == 12) and (MpCanvas.loop_i == MpCanvas.T)) and (MpCanvas.Q >= 4):
            MpCanvas.cm[MpCanvas.loop_i] = ((10 + MpCanvas.Q) - 4)
        self.c_GI(graphics, MpCanvas.loop_i)

    def b_GI(self, graphics, n2):  # g.java:3895
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

    def y_v(self):  # g.java:3917
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 78, 86, 0)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 34), MpCanvas.fighter_name[MpCanvas.cur_slot], 0xFFFFFF)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 20), _js(_js(Consts.eX[27], "."), MpCanvas.fighter_level[MpCanvas.cur_slot]), 0xFFFFFF)
        self.f_GIII(MpCanvas.screen_g, (MpCanvas.center_x + 22), (MpCanvas.center_y + 12), MpCanvas.fighter_wins[MpCanvas.cur_slot])
        self.draw_text_left_on(MpCanvas.screen_g, (MpCanvas.center_x - 27), (MpCanvas.center_y + 11), Consts.eX[49], 0xFFFFFF)
        self.f_GIII(MpCanvas.screen_g, (MpCanvas.center_x + 22), (MpCanvas.center_y + 24), MpCanvas.fighter_losses[MpCanvas.cur_slot])
        self.draw_text_left_on(MpCanvas.screen_g, (MpCanvas.center_x - 27), (MpCanvas.center_y + 23), Consts.eX[50], 0xFFFFFF)

    def c_G(self, graphics):  # g.java:3927
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                self.b_G(graphics)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def d_G(self, graphics):  # g.java:3937
        if imod(MpCanvas.fighter_slot[MpCanvas.bA], 2) == 0:
            self.draw_text_centred_on(graphics, 30, (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.bA], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), (MpCanvas.fighter_name[MpCanvas.bA] if ((len(MpCanvas.fighter_alt_name[MpCanvas.bA]) == 0) or (imod(MpCanvas.aR, 2) == 0)) else MpCanvas.fighter_alt_name[MpCanvas.bA]), 16400640)
            if imod(MpCanvas.state_ticks, 2) == 0:
                MpCanvas.c_GIIIM(graphics, Consts.eq[48], (((19 if (idiv(MpCanvas.fighter_slot[MpCanvas.bA], 2) == 0) else (MpCanvas.canvas_h - 19))) + Consts.er[48]), 12, MpCanvas.ui_images[48])
                return
            MpCanvas.a_GIIMII(graphics, (Consts.eq[48] + 1), (((19 if (idiv(MpCanvas.fighter_slot[MpCanvas.bA], 2) == 0) else (MpCanvas.canvas_h - 19))) + Consts.er[48]), MpCanvas.ui_images[48], 12, 1)
            return
        self.draw_text_centred_on(graphics, (MpCanvas.canvas_w - 30), (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.bA], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), (MpCanvas.fighter_name[MpCanvas.bA] if ((len(MpCanvas.fighter_alt_name[MpCanvas.bA]) == 0) or (imod(MpCanvas.aR, 2) == 0)) else MpCanvas.fighter_alt_name[MpCanvas.bA]), 16400640)
        if imod(MpCanvas.state_ticks, 2) == 0:
            MpCanvas.a_GIIIM(graphics, (MpCanvas.canvas_w - ((1 + Consts.eq[48]))), (((19 if (idiv(MpCanvas.fighter_slot[MpCanvas.bA], 2) == 0) else (MpCanvas.canvas_h - 19))) + Consts.er[48]), 12, MpCanvas.ui_images[48])
            return
        MpCanvas.b_GIIIM(graphics, (MpCanvas.canvas_w - ((2 + Consts.eq[48]))), (((19 if (idiv(MpCanvas.fighter_slot[MpCanvas.bA], 2) == 0) else (MpCanvas.canvas_h - 19))) + Consts.er[48]), 12, MpCanvas.ui_images[48])

    def z_v(self):  # g.java:3955
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 102, 86, 0)
        self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 30), MpCanvas.stage_title, 0xFFFFFF)
        self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 15), _js(_js(_js(Consts.eX[26], MpCanvas.stage), "/"), MpCanvas.stage_count), 0xFFFFFF)
        MpCanvas.loop_i = 1
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                if MpCanvas.fighter_slot[MpCanvas.loop_i] == 1:
                    self.draw_text_centred((MpCanvas.center_x - 24), (MpCanvas.center_y + 4), MpCanvas.fighter_name[MpCanvas.loop_i], 0xFFFFFF)
                    self.draw_text_left((MpCanvas.center_x + 4), (MpCanvas.center_y + 4), _js(_js(Consts.eX[27], ""), MpCanvas.fighter_level[MpCanvas.loop_i]), 0xFFFFFF)
                elif MpCanvas.fighter_slot[MpCanvas.loop_i] == 3:
                    self.draw_text_centred((MpCanvas.center_x - 24), (MpCanvas.center_y + 20), MpCanvas.fighter_name[MpCanvas.loop_i], 0xFFFFFF)
                    self.draw_text_left((MpCanvas.center_x + 4), (MpCanvas.center_y + 20), _js(_js(Consts.eX[27], ""), MpCanvas.fighter_level[MpCanvas.loop_i]), 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    @staticmethod
    def A_v():  # g.java:3974
        MpCanvas.bJ = imod(abs(MpCanvas.rng.nextInt()), 3)
        _sw86 = MpCanvas.bJ
        if _sw86 == 0:
            MpCanvas.cz = 4
        elif _sw86 == 1:
            MpCanvas.cz = 8
        else:
            MpCanvas.cz = 5
        MpCanvas.b_I(1)
        MpCanvas.cA = (MpCanvas.center_x - 44)
        MpCanvas.bt = True

    def e_G(self, graphics):  # g.java:3994
        if MpCanvas.bt:
            n2 = MpCanvas.center_y
            if MpCanvas.room_mode == 0:
                n2 = (MpCanvas.screen_h - 26)
            self.draw_box(graphics, MpCanvas.center_x, (n2 + 3), 110, 38, 0)
            Draw.draw_image(graphics, MpCanvas.ui_images[35], ((MpCanvas.center_x - 44) + Consts.eq[35]), (n2 + Consts.er[35]), 0)
            Draw.draw_image(graphics, MpCanvas.ui_images[36], ((MpCanvas.center_x - 44) + Consts.eq[36]), (n2 + Consts.er[36]), 0)
            Draw.draw_image(graphics, MpCanvas.ui_images[37], ((MpCanvas.center_x - 44) + Consts.eq[37]), (n2 + Consts.er[37]), 0)

    def f_G(self, graphics):  # g.java:4007
        n2 = MpCanvas.center_y
        if MpCanvas.room_mode == 0:
            n2 = (MpCanvas.screen_h - 26)
        if MpCanvas.state == 98:
            if MpCanvas.aS == 100:
                Draw.draw_image(graphics, MpCanvas.ui_images[52], (((MpCanvas.center_x - 44) + 72) + Consts.eq[52]), (n2 + Consts.er[52]), 0)
                self.start_sound(0)
            elif MpCanvas.aS == 20:
                Draw.draw_image(graphics, MpCanvas.ui_images[53], (((MpCanvas.center_x - 44) + 72) + Consts.eq[53]), (n2 + Consts.er[53]), 0)
            else:
                Draw.draw_image(graphics, MpCanvas.ui_images[49], ((MpCanvas.cA - 20) + Consts.eu[35]), ((n2 - 11) + Consts.ev[35]), 0)
                self.start_sound(0)
        if imod(MpCanvas.state_ticks, 2) == 0:
            Draw.draw_image(graphics, MpCanvas.ui_images[38], (((MpCanvas.center_x - 44) + 72) + Consts.eq[38]), (n2 + Consts.er[38]), 0)
        Draw.draw_image(graphics, MpCanvas.ui_images[34], (MpCanvas.cA + Consts.eq[34]), (n2 + Consts.er[34]), 0)
        if (MpCanvas.state == 97) and (MpCanvas.cA > ((MpCanvas.center_x - 44) + 72)):
            self.C_v()

    def B_v(self):  # g.java:4032
        MpCanvas.d = 0
        MpCanvas.set_state(97)

    def C_v(self):  # g.java:4037
        MpCanvas.d = 0
        if MpCanvas.bB > 2:
            MpCanvas.aS = 0
        else:
            if (((MpCanvas.cz == 6) or (MpCanvas.cz == 7))) and (abs((((MpCanvas.center_x - 44) + 72) - MpCanvas.cA)) <= idiv(MpCanvas.cz, 2)):
                MpCanvas.cA = ((MpCanvas.center_x - 44) + 72)
            MpCanvas.aS = ((((20 + MpCanvas.cA) - MpCanvas.center_x) + 44) if (MpCanvas.cA < ((MpCanvas.center_x - 44) + 72)) else ((100 if (MpCanvas.cA == ((MpCanvas.center_x - 44) + 72)) else 20)))
        MpCanvas.set_state(98)

    @staticmethod
    def a_GAMALaI(graphics, imageArray, aArray, n2):  # g.java:4050
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
        if MpCanvas.bn:
            Draw.draw_image_part(graphics, imageArray[1], (MpCanvas.canvas_w - (((MpCanvas.draw_x - a2.anchor_x[n3]) + a2.w[n3]))), (MpCanvas.draw_y - a2.anchor_y[n3]), a2.w[n3], a2.h[n3], a2.src_x[n3], a2.src_y[n3])
            return
        Draw.draw_image_part(graphics, imageArray[0], (MpCanvas.draw_x - a2.anchor_x[n3]), (MpCanvas.draw_y - a2.anchor_y[n3]), a2.w[n3], a2.h[n3], a2.src_x[n3], a2.src_y[n3])

    def c_GI(self, graphics, n2):  # g.java:4073
        n3 = 0
        MpCanvas.bn = (imod(MpCanvas.fighter_slot[n2], 2) != 0)
        MpCanvas.draw_x = MpCanvas.fighter_x[n2]
        MpCanvas.draw_y = MpCanvas.fighter_y[n2]
        self.a_IZ(n2, True)
        if MpCanvas.fighter_kind[n2] != 2:
            self.load_sprite(MpCanvas.dF, MpCanvas.dG, "sprshadow")
            MpCanvas.a_GAMALaI(graphics, MpCanvas.dF, MpCanvas.dG, MpCanvas.fighter_frame[n2])
        bl = False
        if MpCanvas.fighter_kind[n2] == 2:
            bl = Consts.eo[imod(MpCanvas.fighter_frame[n2], 100)]
            if bl:
                self.load_sprite_dir(MpCanvas.dJ, MpCanvas.dK, "spr_wp_mon", 0)
                MpCanvas.a_GAMALaI(graphics, MpCanvas.dJ, MpCanvas.dK, MpCanvas.fighter_frame[n2])
        else:
            n3 = idiv(MpCanvas.fighter_frame[n2], 100)
            if MpCanvas.fighter_weapon[n2] == 0:
                if n3 == 2:
                    bl = Consts.ek[imod(MpCanvas.fighter_frame[n2], 100)]
            else:
                bl = (Consts.em[imod(MpCanvas.fighter_frame[n2], 100)] if (n3 == 1) else ((Consts.en[imod(MpCanvas.fighter_frame[n2], 100)] if (n3 == 2) else Consts.el[imod(MpCanvas.fighter_frame[n2], 100)])))
            if bl:
                self.load_sprite(MpCanvas.dy[MpCanvas.fighter_weapon[n2]], MpCanvas.dz[MpCanvas.fighter_weapon[n2]], _js("sprwp", ((MpCanvas.fighter_weapon[n2] + 1))))
                MpCanvas.a_GAMALaI(graphics, MpCanvas.dy[MpCanvas.fighter_weapon[n2]], MpCanvas.dz[MpCanvas.fighter_weapon[n2]], MpCanvas.fighter_frame[n2])
        if MpCanvas.fighter_kind[n2] == 2:
            self.load_sprite_dir(MpCanvas.dH, MpCanvas.dI, "spr_mon", 0)
            MpCanvas.a_GAMALaI(graphics, MpCanvas.dH, MpCanvas.dI, MpCanvas.fighter_frame[n2])
        else:
            self.load_sprite(MpCanvas.dF, MpCanvas.dG, "sprshadow")
            MpCanvas.a_GAMALaI(graphics, MpCanvas.dF, MpCanvas.dG, MpCanvas.fighter_frame[n2])
            self.load_sprite(MpCanvas.du, MpCanvas.dv, "sprbody")
            MpCanvas.a_GAMALaI(graphics, MpCanvas.du, MpCanvas.dv, MpCanvas.fighter_frame[n2])
        n3 = 0
        if MpCanvas.fighter_kind[n2] != 2:
            if MpCanvas.fighter_kind[n2] == 0:
                n3 = MpCanvas.fighter_face[n2]
            self.load_sprite(MpCanvas.dw[n3], MpCanvas.dx[n3], _js("sprhead", ((n3 + 1))))
            MpCanvas.a_GAMALaI(graphics, MpCanvas.dw[n3], MpCanvas.dx[n3], MpCanvas.fighter_frame[n2])
        if MpCanvas.fighter_present[n2] and (MpCanvas.state != 105):
            _sw87 = MpCanvas.fighter_status[n2]
            if _sw87 == 11:
                self.V_v()
                MpCanvas.e_GI(graphics, 0)
            elif _sw87 == 12:
                self.V_v()
                MpCanvas.e_GI(graphics, 1)
            elif _sw87 == 13:
                self.V_v()
                MpCanvas.e_GI(graphics, 2)
        if not bl:
            if MpCanvas.fighter_kind[n2] == 2:
                self.load_sprite_dir(MpCanvas.dJ, MpCanvas.dK, "spr_wp_mon", 0)
                MpCanvas.a_GAMALaI(graphics, MpCanvas.dJ, MpCanvas.dK, MpCanvas.fighter_frame[n2])
            else:
                self.load_sprite(MpCanvas.dy[MpCanvas.fighter_weapon[n2]], MpCanvas.dz[MpCanvas.fighter_weapon[n2]], _js("sprwp", ((MpCanvas.fighter_weapon[n2] + 1))))
                MpCanvas.a_GAMALaI(graphics, MpCanvas.dy[MpCanvas.fighter_weapon[n2]], MpCanvas.dz[MpCanvas.fighter_weapon[n2]], MpCanvas.fighter_frame[n2])
        self.a_IZ(n2, False)

    def a_IZ(self, n2, bl):  # g.java:4151
        if MpCanvas.fighter_kind[n2] == 2:
            if not bl:
                self.load_sprite_dir(MpCanvas.dN, MpCanvas.dO, "spr_sword_mon", 0)
                MpCanvas.a_GAMALaI(MpCanvas.screen_g, MpCanvas.dN, MpCanvas.dO, MpCanvas.fighter_frame[n2])
                self.load_sprite_dir(MpCanvas.dL, MpCanvas.dM, "spr_eff_mon", 0)
                MpCanvas.a_GAMALaI(MpCanvas.screen_g, MpCanvas.dL, MpCanvas.dM, MpCanvas.fighter_frame[n2])
                return
        else:
            n3 = 0
            bl2 = False
            if not bl:
                self.load_sprite(MpCanvas.dA[MpCanvas.fighter_weapon[n2]], MpCanvas.dB[MpCanvas.fighter_weapon[n2]], _js("sprsword", ((MpCanvas.fighter_weapon[n2] + 1))))
                MpCanvas.a_GAMALaI(MpCanvas.screen_g, MpCanvas.dA[MpCanvas.fighter_weapon[n2]], MpCanvas.dB[MpCanvas.fighter_weapon[n2]], MpCanvas.fighter_frame[n2])
                self.load_sprite(MpCanvas.dC[0], MpCanvas.dD[0], "spreff1")
                MpCanvas.a_GAMALaI(MpCanvas.screen_g, MpCanvas.dC[0], MpCanvas.dD[0], MpCanvas.fighter_frame[n2])
            if bl == ((bl2 := (Consts.ei[imod(MpCanvas.fighter_frame[n2], 100)] if (((n3 := idiv(MpCanvas.fighter_frame[n2], 100))) == 1) else ((Consts.ej[imod(MpCanvas.fighter_frame[n2], 100)] if (n3 == 2) else False))))):
                self.load_sprite(MpCanvas.dC[1], MpCanvas.dD[1], "spreff2")
                MpCanvas.a_GAMALaI(MpCanvas.screen_g, MpCanvas.dC[1], MpCanvas.dD[1], MpCanvas.fighter_frame[n2])

    def D_v(self):  # g.java:4176
        if MpCanvas.X >= 5:
            MpCanvas.X = (-1)
            MpCanvas.loop_i = 0
            while MpCanvas.loop_i < 4:
                if MpCanvas.fighter_present[MpCanvas.loop_i] and ((((MpCanvas.loop_i == MpCanvas.S) or (MpCanvas.loop_i == MpCanvas.T)) or (MpCanvas.loop_i == MpCanvas.U))):
                    if MpCanvas.fighter_hp[MpCanvas.loop_i] != MpCanvas.fighter_hp_target[MpCanvas.loop_i]:
                        MpCanvas.fighter_hp[MpCanvas.loop_i] = MpCanvas.fighter_hp_target[MpCanvas.loop_i]
                    if MpCanvas.fighter_mp[MpCanvas.loop_i] != MpCanvas.fighter_mp_target[MpCanvas.loop_i]:
                        MpCanvas.fighter_mp[MpCanvas.loop_i] = MpCanvas.fighter_mp_target[MpCanvas.loop_i]
                MpCanvas.loop_i = MpCanvas.loop_i + 1
        if MpCanvas.Q >= MpCanvas.R:
            MpCanvas.Q = 0
            _sw88 = MpCanvas.cc[MpCanvas.S]
            _m89 = False
            while True:
                if _m89 or _sw88 in (2, 17, 18, 19):
                    _m89 = True
                    MpCanvas.fighter_x[MpCanvas.S] = (MpCanvas.canvas_w - 67)
                    MpCanvas.fighter_y[MpCanvas.S] = (MpCanvas.center_y + 65)
                    if MpCanvas.room_mode != 0:
                        n2 = MpCanvas.S
                        MpCanvas.fighter_y[n2] = (MpCanvas.fighter_y[n2] + ((((-1) if (idiv(MpCanvas.turn_bytes[(12 + MpCanvas.bC)], 2) == 0) else 1)) * 23))
                    _sw90 = MpCanvas.turn_bytes[(4 + MpCanvas.bC)]
                    if _sw90 == 3:
                        MpCanvas.cc[MpCanvas.S] = 9
                    elif _sw90 == 4:
                        MpCanvas.cc[MpCanvas.S] = 10
                    elif _sw90 == 5:
                        MpCanvas.cc[MpCanvas.S] = 11
                    elif _sw90 == 6:
                        MpCanvas.cc[MpCanvas.S] = 14
                    elif _sw90 == 7:
                        MpCanvas.cc[MpCanvas.S] = 15
                    elif _sw90 == 0:
                        MpCanvas.cc[MpCanvas.S] = 3
                    break
                if _m89 or _sw88 == 8:
                    _m89 = True
                    _sw91 = MpCanvas.turn_bytes[(4 + MpCanvas.bC)]
                    _m92 = False
                    while True:
                        if _m92 or _sw91 in (3, 4, 5):
                            _m92 = True
                            MpCanvas.cc[MpCanvas.S] = 2
                            MpCanvas.bl = idiv((((MpCanvas.canvas_w - 67) - 42)), Consts.eh[MpCanvas.cc[MpCanvas.S]])
                            if MpCanvas.room_mode == 0:
                                MpCanvas.bm = 0
                                break
                            if idiv(MpCanvas.fighter_slot[MpCanvas.S], 2) == idiv(MpCanvas.turn_bytes[(12 + MpCanvas.bC)], 2):
                                MpCanvas.bm = 0
                                break
                            if idiv(MpCanvas.fighter_slot[MpCanvas.S], 2) == 0:
                                MpCanvas.bm = idiv(46, Consts.eh[MpCanvas.cc[MpCanvas.S]])
                                break
                            MpCanvas.bm = idiv((-46), Consts.eh[MpCanvas.cc[MpCanvas.S]])
                            break
                        if _m92 or _sw91 in (6, 7):
                            _m92 = True
                            if MpCanvas.room_mode == 0:
                                MpCanvas.cc[MpCanvas.S] = 17
                                break
                            if idiv(MpCanvas.turn_bytes[(12 + MpCanvas.bC)], 2) == idiv(MpCanvas.turn_bytes[(0 + MpCanvas.bC)], 2):
                                MpCanvas.cc[MpCanvas.S] = 17
                                break
                            if idiv(MpCanvas.turn_bytes[(12 + MpCanvas.bC)], 2) == 1:
                                MpCanvas.cc[MpCanvas.S] = 18
                                break
                            MpCanvas.cc[MpCanvas.S] = 19
                            break
                        if _m92 or _sw91 == 8:
                            _m92 = True
                            MpCanvas.cc[MpCanvas.S] = 20
                        break
                    break
                if _m89 or _sw88 == 20:
                    _m89 = True
                    _sw93 = MpCanvas.turn_bytes[(4 + MpCanvas.bC)]
                    if _sw93 == 8:
                        MpCanvas.cc[MpCanvas.S] = 16
                    break
                if _m89 or _sw88 in (3, 9, 10, 11, 14, 15, 16):
                    _m89 = True
                    if (MpCanvas.turn_bytes[(28 + MpCanvas.bC)] == 3) and (MpCanvas.fighter_slot[MpCanvas.S] == MpCanvas.turn_bytes[(0 + MpCanvas.bC)]):
                        MpCanvas.bJ = MpCanvas.S
                        MpCanvas.S = MpCanvas.T
                        MpCanvas.T = MpCanvas.bJ
                        MpCanvas.cc[MpCanvas.S] = 3
                        MpCanvas.V = 1
                        break
                    MpCanvas.X = 0
                    if MpCanvas.turn_bytes[(28 + MpCanvas.bC)] == 3:
                        MpCanvas.bJ = MpCanvas.S
                        MpCanvas.S = MpCanvas.T
                        MpCanvas.T = MpCanvas.bJ
                        MpCanvas.cc[MpCanvas.T] = 0
                        MpCanvas.place_fighter(MpCanvas.T)
                    MpCanvas.cc[MpCanvas.S] = 28
                    MpCanvas.bl = idiv(((42 - MpCanvas.fighter_x[MpCanvas.S])), Consts.eh[MpCanvas.cc[MpCanvas.S]])
                    if MpCanvas.room_mode == 0:
                        MpCanvas.bm = 0
                        break
                    if idiv(MpCanvas.fighter_slot[MpCanvas.S], 2) == idiv(MpCanvas.turn_bytes[(12 + MpCanvas.bC)], 2):
                        MpCanvas.bm = 0
                        break
                    if idiv(MpCanvas.fighter_slot[MpCanvas.S], 2) == 0:
                        MpCanvas.bm = idiv((-46), Consts.eh[MpCanvas.cc[MpCanvas.S]])
                        break
                    MpCanvas.bm = idiv(46, Consts.eh[MpCanvas.cc[MpCanvas.S]])
                    break
                if _m89 or _sw88 in (12, 13, 28):
                    _m89 = True
                    MpCanvas.place_fighter(MpCanvas.S)
                    MpCanvas.bJ = (-1)
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 4:
                        if MpCanvas.fighter_present[MpCanvas.loop_i]:
                            if (MpCanvas.cc[MpCanvas.S] == 13) and (imod(MpCanvas.fighter_slot[MpCanvas.S], 2) == imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2)):
                                MpCanvas.fighter_status[MpCanvas.loop_i] = MpCanvas.turn_bytes[(4 + MpCanvas.bC)]
                                MpCanvas.fighter_status_ticks[MpCanvas.loop_i] = 3
                            if (MpCanvas.fighter_hp[MpCanvas.loop_i] == 0) and (MpCanvas.fighter_hp_delta[MpCanvas.loop_i] != 0):
                                MpCanvas.bJ = MpCanvas.loop_i
                                MpCanvas.cc[MpCanvas.bJ] = 6
                                if imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == imod(MpCanvas.fighter_slot[0], 2):
                                    MpCanvas.bb = MpCanvas.bb - 1
                                else:
                                    MpCanvas.bc = MpCanvas.bc - 1
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    if MpCanvas.bJ > 0:
                        if MpCanvas.cc[MpCanvas.S] != 6:
                            MpCanvas.cc[MpCanvas.S] = 0
                        MpCanvas.S = MpCanvas.bJ
                        break
                    MpCanvas.bC = MpCanvas.bC + 1
                    self.E_v()
                    break
                if _m89 or _sw88 == 6:
                    _m89 = True
                    MpCanvas.bC = MpCanvas.bC + 1
                    self.E_v()
                break
            MpCanvas.R = Consts.eh[MpCanvas.cc[MpCanvas.S]]
        if MpCanvas.cc[MpCanvas.S] != 6:
            self.F_v()

    def E_v(self):  # g.java:4372
        if MpCanvas.turn_record_count == 0:
            MpCanvas.set_state(100)
            return
        if MpCanvas.bC < MpCanvas.turn_record_count:
            MpCanvas.set_state(101)
            return
        MpCanvas.set_state(93)

    def F_v(self):  # g.java:4388
        if ((MpCanvas.cc[MpCanvas.S] != 12) and (MpCanvas.cc[MpCanvas.S] != 13)) and (MpCanvas.turn_bytes[(28 + MpCanvas.bC)] != 3):
            if (MpCanvas.T != (-1)) and (MpCanvas.cc[MpCanvas.T] != 0):
                n2 = MpCanvas.T
                MpCanvas.cd[n2] = (MpCanvas.cd[n2] + 1)
                if MpCanvas.cd[MpCanvas.T] >= MpCanvas.ce[MpCanvas.T]:
                    MpCanvas.cc[MpCanvas.T] = 0
                    MpCanvas.place_fighter(MpCanvas.T)
            if (MpCanvas.U != (-1)) and (MpCanvas.cc[MpCanvas.U] != 0):
                n3 = MpCanvas.U
                MpCanvas.cd[n3] = (MpCanvas.cd[n3] + 1)
                if MpCanvas.cd[MpCanvas.U] >= MpCanvas.ce[MpCanvas.U]:
                    MpCanvas.cc[MpCanvas.U] = 0
                    MpCanvas.place_fighter(MpCanvas.U)
        _sw94 = MpCanvas.cc[MpCanvas.S]
        _m95 = False
        while True:
            if _m95 or _sw94 in (3, 9, 10, 11, 14):
                _m95 = True
                _sw96 = MpCanvas.V
                _m97 = False
                while True:
                    if _m97 or _sw96 in (1, 4):
                        _m97 = True
                        if (MpCanvas.cc[MpCanvas.S] == 11) and (MpCanvas.Q == 17):
                            self.G_v()
                            MpCanvas.ce[MpCanvas.T] = 3
                            return
                        if imod(MpCanvas.Q, 2) != 1:
                            return
                        if (MpCanvas.cc[MpCanvas.S] == 11) and (MpCanvas.Q > 10):
                            return
                        self.G_v()
                        MpCanvas.ce[MpCanvas.T] = 2
                        return
                    if _m97 or _sw96 == 5:
                        _m97 = True
                        if MpCanvas.turn_bytes[(28 + MpCanvas.bC)] == 3:
                            if MpCanvas.Q != 0:
                                return
                            MpCanvas.cc[MpCanvas.T] = 5
                            MpCanvas.cd[MpCanvas.T] = 0
                            MpCanvas.ce[MpCanvas.T] = MpCanvas.R
                            return
                        else:
                            if imod(MpCanvas.Q, 2) != 1:
                                return
                            self.G_v()
                            MpCanvas.ce[MpCanvas.T] = 2
                    if _m97 or _sw96 not in (1, 4, 5):
                        _m97 = True
                        return
                    break
            if _m95 or _sw94 == 15:
                _m95 = True
                _sw98 = MpCanvas.V
                if _sw98 in (1, 4):
                    if MpCanvas.Q != 2:
                        return
                    self.G_v()
                    MpCanvas.ce[MpCanvas.T] = 4
                return
            if _m95 or _sw94 == 16:
                _m95 = True
                _sw99 = MpCanvas.V
                if _sw99 in (1, 4):
                    if MpCanvas.Q != 8:
                        return
                    self.G_v()
                    MpCanvas.ce[MpCanvas.T] = 3
                    if MpCanvas.U == (-1):
                        return
                    MpCanvas.cc[MpCanvas.U] = MpCanvas.W
                    MpCanvas.cd[MpCanvas.U] = 0
                    MpCanvas.ce[MpCanvas.U] = 3
                return
            if _m95 or _sw94 == 12:
                _m95 = True
                if MpCanvas.Q != 4:
                    return
                MpCanvas.X = 0
                self.start_sound(6)
                if MpCanvas.turn_bytes[(4 + MpCanvas.bC)] == 2:
                    return
                return
            if _m95 or _sw94 == 13:
                _m95 = True
                if (MpCanvas.Q == 4) and (MpCanvas.turn_bytes[(4 + MpCanvas.bC)] == 13):
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 4:
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    self.start_sound(5)
                    return
                if MpCanvas.Q == 7:
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 4:
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    self.start_sound(5)
                    return
                if MpCanvas.Q != 5:
                    return
                MpCanvas.X = 0
            break

    def G_v(self):  # g.java:4501
        MpCanvas.cc[MpCanvas.T] = MpCanvas.V
        MpCanvas.cd[MpCanvas.T] = 0
        if (MpCanvas.cc[MpCanvas.S] == 16) or (MpCanvas.cc[MpCanvas.S] == 15):
            self.start_sound(2)
            return
        self.start_sound(0)

    def H_v(self):  # g.java:4511
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 88, 72, 0)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 20), MpCanvas.stage_title, 0xFFFFFF)
        MpCanvas.bL = _js(_js(Consts.eX[26], " "), MpCanvas.stage)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y - 4), MpCanvas.bL, 0xFFFFFF)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (MpCanvas.center_y + 12), Consts.eX[28], 0xFFFFFF)

    def I_v(self):  # g.java:4519
        if MpCanvas.X < 0:
            return
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i] and ((((MpCanvas.loop_i == MpCanvas.S) or (MpCanvas.loop_i == MpCanvas.T)) or (MpCanvas.loop_i == MpCanvas.U))):
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
                    bl = _set(MpCanvas, 'bn', (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) != 0))
                    if not MpCanvas.bn:
                        self.e_GIII(MpCanvas.screen_g, MpCanvas.fighter_x[MpCanvas.loop_i], ((MpCanvas.fighter_y[MpCanvas.loop_i] - 40) - (2 * MpCanvas.X)), MpCanvas.fighter_hp_delta[MpCanvas.loop_i])
                    else:
                        self.e_GIII(MpCanvas.screen_g, (MpCanvas.canvas_w - MpCanvas.fighter_x[MpCanvas.loop_i]), ((MpCanvas.fighter_y[MpCanvas.loop_i] - 40) - (2 * MpCanvas.X)), MpCanvas.fighter_hp_delta[MpCanvas.loop_i])
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.g_G(MpCanvas.screen_g)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if (MpCanvas.fighter_present[MpCanvas.loop_i] and ((((MpCanvas.loop_i == MpCanvas.S) or (MpCanvas.loop_i == MpCanvas.T)) or (MpCanvas.loop_i == MpCanvas.U)))) and (MpCanvas.fighter_hp[MpCanvas.loop_i] == 0):
                MpCanvas.fighter_hp[MpCanvas.loop_i] = 1
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.X = MpCanvas.X + 1

    @staticmethod
    def g_G(graphics):  # g.java:4562
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
        MpCanvas.bb = 0
        MpCanvas.bc = 0

    def b_GIII(self, graphics, n2, n3, n4):  # g.java:4619
        MpCanvas.draw_number(graphics, n2, n3, n4, 1)

    def c_GIII(self, graphics, n2, n3, n4):  # g.java:4623
        MpCanvas.draw_number(graphics, n2, n3, n4, 2)

    def d_GIII(self, graphics, n2, n3, n4):  # g.java:4627
        MpCanvas.draw_number(graphics, n2, n3, n4, 3)

    def e_GIII(self, graphics, n2, n3, n4):  # g.java:4631
        MpCanvas.draw_number(graphics, n2, n3, n4, 4)

    def a_III(self, n2, n3, n4):  # g.java:4635
        MpCanvas.draw_number(MpCanvas.screen_g, n2, n3, n4, 5)

    def f_GIII(self, graphics, n2, n3, n4):  # g.java:4639
        MpCanvas.draw_number(graphics, n2, n3, n4, 0)

    def b_III(self, n2, n3, n4):  # g.java:4643
        MpCanvas.draw_number(MpCanvas.screen_g, n2, n3, n4, 0)

    def c_III(self, n2, n3, n4):  # g.java:4647
        MpCanvas.draw_number(MpCanvas.screen_g, n2, n3, n4, 1)

    def d_III(self, n2, n3, n4):  # g.java:4651
        MpCanvas.draw_number(MpCanvas.screen_g, n2, n3, n4, 0)

    def e_III(self, n2, n3, n4):  # g.java:4655
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
                MpCanvas.br = True
            else:
                MpCanvas.br = False
            while (idiv(n4, n6) > 0) or (n6 == 1):
                n12 = idiv(imod(n4, ((n6 * 10))), n6)
                Draw.draw_image_part(graphics, MpCanvas.number_images[n5], n2, n3, 6, 10, (n12 * 6), (10 if MpCanvas.br else 0))
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
                    self.v_G(MpCanvas.screen_g)
                    return
                n2 = (MpCanvas.center_y - 57)
                n3 = 0
                while n3 < 7:
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n2 + (12 * n3)), Consts.eV[(1 + n3)], 0xFFFFFF)
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
                    self.c_II(4, 2)
                    break
                self.c_II(4, 3)
                return
            if _m102 or _sw101 == 1:
                _m102 = True
                n2 = (MpCanvas.center_y - 45)
                n5 = 0
                while n5 < 5:
                    self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n2 + (12 * n5)), Consts.eV[(8 + n5)], 0xFFFFFF)
                    n5 = n5 + 1
                Draw.fill_rect(MpCanvas.screen_g, (MpCanvas.center_x - 40), (n2 + 63), 80, 13, 0)
                Draw.draw_rect(MpCanvas.screen_g, (MpCanvas.center_x - 40), (n2 + 63), 80, 13, 0x646464)
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n2 + 64), MpCanvas.password, 0x41FF41)
                if len(MpCanvas.password) >= 4:
                    self.c_II(0, 3)
                    return
                if len(MpCanvas.password) > 0:
                    self.c_II((-1), 3)
                    return
                self.c_II((-1), 1)
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
                MpCanvas.cv = 0
                MpCanvas.A = True
                MpCanvas.set_state(10000)
            break

    def push_state(self, n2):  # g.java:4996
        if n2 != MpCanvas.state_stack[MpCanvas.stack_depth]:
            MpCanvas.cursor_stack[_inc(MpCanvas, 'stack_depth', 1)] = 0
            MpCanvas.state_stack[MpCanvas.stack_depth] = n2
        MpCanvas.set_state(n2)

    def reset_state_stack(self, n2):  # g.java:5004
        if n2 == 10:
            MpCanvas.dX = True
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
        MpCanvas.X_v()
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
        MpCanvas.cr[0] = MpCanvas.aK
        MpCanvas.fighter_present[0] = True
        MpCanvas.bb = MpCanvas.bb + 1
        MpCanvas.place_fighter(0)
        MpCanvas.fighter_blink[0] = imod(abs(MpCanvas.rng.nextInt()), 4)
        MpCanvas.fighter_status[0] = 99
        MpCanvas.fighter_status_ticks[0] = 0
        MpCanvas.bj = False
        MpCanvas.aR = 0
        MpCanvas.D = False
        self.push_state(90)
        self.stop_music()
        MpCanvas.O = True

    def h_G(self, graphics):  # g.java:5068
        self.draw_box(graphics, MpCanvas.center_x, (MpCanvas.center_y - 26), 110, 60, 0)
        Draw.fill_rect(graphics, (MpCanvas.center_x - 51), ((MpCanvas.center_y - 51) + (MpCanvas.skill_cursor * 12)), 102, 12, 12956683)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < MpCanvas.skill_slot_count:
            if MpCanvas.fighter_mp[0] < MpCanvas.skill_costs[(MpCanvas.skill_slots[MpCanvas.loop_i] - 3)]:
                self.draw_text_centred_on(graphics, MpCanvas.center_x, ((MpCanvas.center_y - 51) + (MpCanvas.loop_i * 12)), Consts.eK[(MpCanvas.skill_slots[MpCanvas.loop_i] - 3)], 0x646464)
                if (MpCanvas.skill_slots[MpCanvas.loop_i] != 9) and (MpCanvas.skill_slots[MpCanvas.loop_i] == 10):
                    pass
            else:
                self.draw_text_centred_on(graphics, MpCanvas.center_x, ((MpCanvas.center_y - 51) + (MpCanvas.loop_i * 12)), Consts.eK[(MpCanvas.skill_slots[MpCanvas.loop_i] - 3)], 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def P_v(self):  # g.java:5085
        _sw106 = MpCanvas.room_mode
        if _sw106 in (0, 1):
            n2 = (MpCanvas.center_y - 62)
            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 102, 124, 0)
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n2 + 5), MpCanvas.fighter_name[0], 0xFFFFFF)
            string = (Consts.eX[5] if (MpCanvas.battle_won == 1) else Consts.eX[6])
            self.draw_text_colored(MpCanvas.screen_g, string, MpCanvas.center_x, (n2 + 19), 1, 16400640)
            self.draw_text_colored(MpCanvas.screen_g, Consts.eX[49], (MpCanvas.center_x - 42), (n2 + 35), 0, 0xFFFFFF)
            self.f_GIII(MpCanvas.screen_g, (MpCanvas.center_x + 36), (n2 + 36), MpCanvas.wins)
            self.draw_text_colored(MpCanvas.screen_g, Consts.eX[50], (MpCanvas.center_x - 42), (n2 + 50), 0, 0xFFFFFF)
            self.f_GIII(MpCanvas.screen_g, (MpCanvas.center_x + 36), (n2 + 51), MpCanvas.losses)
            self.draw_text_colored(MpCanvas.screen_g, Consts.eX[29], (MpCanvas.center_x - 42), (n2 + 70), 0, 0xFFFFFF)
            self.b_GIII(MpCanvas.screen_g, (MpCanvas.center_x + 36), (n2 + 71), MpCanvas.reward_gold)
            self.draw_text_colored(MpCanvas.screen_g, Consts.eR[0], (MpCanvas.center_x - 42), (n2 + 83), 0, 0xFFFFFF)
            self.b_GIII(MpCanvas.screen_g, (MpCanvas.center_x + 36), (n2 + 84), MpCanvas.reward_fame)
            self.draw_text_colored(MpCanvas.screen_g, Consts.eX[4], (MpCanvas.center_x - 42), (n2 + 96), 0, 0x41FF41)
            self.f_GIII(MpCanvas.screen_g, (MpCanvas.center_x + 36), (n2 + 97), MpCanvas.reward_rank)
            self.r_I((n2 + 109))
            return
        elif _sw106 == 2:
            n3 = (MpCanvas.center_y - 62)
            self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, 102, 124, 0)
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n3 + 3), MpCanvas.fighter_name[0], 0xFFFFFF)
            if MpCanvas.battle_won == 1:
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n3 + 15), Consts.eL[MpCanvas.reward_grade], 16400640)
            else:
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n3 + 15), Consts.eX[31], 16400640)
            self.draw_text_colored(MpCanvas.screen_g, Consts.eX[29], (MpCanvas.center_x - 34), (n3 + 30), 0, 0xFFFFFF)
            self.b_GIII(MpCanvas.screen_g, (MpCanvas.center_x + 30), (n3 + 31), MpCanvas.reward_gold)
            self.draw_text_colored(MpCanvas.screen_g, Consts.eX[32], (MpCanvas.center_x - 34), (n3 + 42), 0, 0xFFFFFF)
            self.b_GIII(MpCanvas.screen_g, (MpCanvas.center_x + 30), (n3 + 43), MpCanvas.reward_exp)
            self.draw_text_colored(MpCanvas.screen_g, Consts.eR[0], (MpCanvas.center_x - 34), (n3 + 54), 0, 0xFFFFFF)
            self.b_GIII(MpCanvas.screen_g, (MpCanvas.center_x + 30), (n3 + 55), MpCanvas.reward_fame)
            if not (MpCanvas.loot == "NONE"):
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n3 + 69), MpCanvas.loot, 0xFFFFFF)
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (n3 + 81), _js(Consts.eX[33], "!!!"), 0xFFFFFF)
            self.draw_text_colored(MpCanvas.screen_g, Consts.eX[4], (MpCanvas.center_x - 34), (n3 + 96), 0, 0x41FF41)
            self.b_GIII(MpCanvas.screen_g, (MpCanvas.center_x + 30), (n3 + 97), MpCanvas.reward_rank)
            self.r_I((n3 + 109))

    @staticmethod
    def Q_v():  # g.java:5133
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

    def R_v(self):  # g.java:5152
        MpCanvas.box_x = 0
        if MpCanvas.state_ticks == 0:
            MpCanvas.box_x = (-40)
        elif MpCanvas.state_ticks == 1:
            MpCanvas.box_x = (-20)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if (MpCanvas.fighter_present[MpCanvas.loop_i] and (MpCanvas.fighter_hp[MpCanvas.loop_i] > 0)) and (((((MpCanvas.state == 99) or (MpCanvas.loop_i == MpCanvas.S)) or (MpCanvas.loop_i == MpCanvas.T)) or (MpCanvas.loop_i == MpCanvas.U))):
                MpCanvas.box_y = (27 if (MpCanvas.room_mode == 0) else ((27 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_h - 27) - 23))))
                _sw109 = MpCanvas.fighter_kind[MpCanvas.loop_i]
                if _sw109 == 0:
                    MpCanvas.cD = MpCanvas.fighter_face[MpCanvas.loop_i]
                    MpCanvas.bx = True
                elif _sw109 == 1:
                    MpCanvas.cD = 4
                    MpCanvas.bx = False
                elif _sw109 == 2:
                    MpCanvas.cD = 5
                    MpCanvas.bx = False
                if MpCanvas.state == 99:
                    MpCanvas.bJ = MpCanvas.turn_actions[MpCanvas.loop_i]
                elif MpCanvas.loop_i == MpCanvas.S:
                    MpCanvas.bJ = MpCanvas.turn_bytes[(4 + MpCanvas.bC)]
                elif MpCanvas.loop_i == MpCanvas.T:
                    MpCanvas.bJ = MpCanvas.turn_bytes[(16 + MpCanvas.bC)]
                elif MpCanvas.loop_i == MpCanvas.U:
                    MpCanvas.bJ = MpCanvas.turn_bytes[(36 + MpCanvas.bC)]
                if imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0:
                    Draw.draw_rect(MpCanvas.screen_g, MpCanvas.box_x, MpCanvas.box_y, 60, 23, 0)
                    Draw.draw_rect(MpCanvas.screen_g, (MpCanvas.box_x + 1), (MpCanvas.box_y + 1), 58, 21, 16769990)
                    _sw110 = MpCanvas.bJ
                    if _sw110 in (0, 3, 4, 5, 6, 7, 8):
                        self.load_numbered_image(MpCanvas.act_images, "act", 0)
                        self.load_numbered_image(MpCanvas.act_images, "act", (6 + MpCanvas.cD))
                        MpCanvas.c_IIM((MpCanvas.box_x + Consts.es[0]), (MpCanvas.box_y + Consts.et[0]), MpCanvas.act_images[0])
                        MpCanvas.c_IIM((MpCanvas.box_x + Consts.es[(6 + MpCanvas.cD)]), (MpCanvas.box_y + Consts.et[(6 + MpCanvas.cD)]), MpCanvas.act_images[(6 + MpCanvas.cD)])
                    else:
                        self.load_numbered_image(MpCanvas.act_images, "act", 1)
                        self.load_numbered_image(MpCanvas.act_images, "act", (12 + MpCanvas.cD))
                        MpCanvas.c_IIM((MpCanvas.box_x + Consts.es[1]), (MpCanvas.box_y + Consts.et[1]), MpCanvas.act_images[1])
                        MpCanvas.c_IIM((MpCanvas.box_x + Consts.es[(12 + MpCanvas.cD)]), (MpCanvas.box_y + Consts.et[(12 + MpCanvas.cD)]), MpCanvas.act_images[(12 + MpCanvas.cD)])
                    MpCanvas.bJ = (3 if (MpCanvas.bJ > 2) else MpCanvas.bJ)
                    self.load_numbered_image(MpCanvas.act_images, "act", (2 + MpCanvas.bJ))
                    MpCanvas.draw_image((((MpCanvas.box_x + 60) - 19) + Consts.es[(2 + MpCanvas.bJ)]), ((0 + MpCanvas.box_y) + Consts.et[(2 + MpCanvas.bJ)]), MpCanvas.act_images[(2 + MpCanvas.bJ)])
                else:
                    MpCanvas.draw_rect(((MpCanvas.canvas_w - MpCanvas.box_x) - 60), MpCanvas.box_y, 60, 23, 0)
                    MpCanvas.draw_rect((((MpCanvas.canvas_w - MpCanvas.box_x) - 60) + 1), (MpCanvas.box_y + 1), 58, 21, 16769990)
                    _sw111 = MpCanvas.bJ
                    if _sw111 in (0, 3, 4, 5, 6, 7, 8):
                        self.load_numbered_image(MpCanvas.act_images, "act", (6 + MpCanvas.cD))
                        MpCanvas.b_IIM((MpCanvas.canvas_w - ((MpCanvas.box_x + Consts.es[0]))), (MpCanvas.box_y + Consts.et[0]), MpCanvas.act_images[0])
                        MpCanvas.a_IIMZ((MpCanvas.canvas_w - ((MpCanvas.box_x + Consts.es[(6 + MpCanvas.cD)]))), (MpCanvas.box_y + Consts.et[(6 + MpCanvas.cD)]), MpCanvas.act_images[(6 + MpCanvas.cD)], MpCanvas.bx)
                    else:
                        self.load_numbered_image(MpCanvas.act_images, "act", (12 + MpCanvas.cD))
                        MpCanvas.b_IIM((MpCanvas.canvas_w - ((MpCanvas.box_x + Consts.es[1]))), (MpCanvas.box_y + Consts.et[1]), MpCanvas.act_images[1])
                        MpCanvas.a_IIMZ((MpCanvas.canvas_w - ((MpCanvas.box_x + Consts.es[(12 + MpCanvas.cD)]))), (MpCanvas.box_y + Consts.et[(12 + MpCanvas.cD)]), MpCanvas.act_images[(12 + MpCanvas.cD)], MpCanvas.bx)
                    MpCanvas.bJ = (3 if (MpCanvas.bJ > 2) else MpCanvas.bJ)
                    self.load_numbered_image(MpCanvas.act_images, "act", (2 + MpCanvas.bJ))
                    MpCanvas.draw_image(((((MpCanvas.canvas_w - MpCanvas.box_x) - 60) + 10) + Consts.es[(2 + MpCanvas.bJ)]), ((0 + MpCanvas.box_y) + Consts.et[(2 + MpCanvas.bJ)]), MpCanvas.act_images[(2 + MpCanvas.bJ)])
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def i_G(self, graphics):  # g.java:5246
        if MpCanvas.aR < 10:
            Draw.draw_image_part(graphics, MpCanvas.number_images[3], (MpCanvas.center_x - 33), (MpCanvas.center_y - 31), 52, 13, 120, 0)
            self.d_GIII(graphics, (MpCanvas.center_x + 21), (MpCanvas.center_y - 31), MpCanvas.aR)
            return
        Draw.draw_image_part(graphics, MpCanvas.number_images[3], (MpCanvas.center_x - 39), (MpCanvas.center_y - 31), 52, 13, 120, 0)
        self.d_GIII(graphics, (MpCanvas.center_x + 27), (MpCanvas.center_y - 31), MpCanvas.aR)

    @staticmethod
    def j_G(graphics):  # g.java:5256
        MpCanvas.box_x = MpCanvas.center_x
        MpCanvas.box_y = (MpCanvas.center_y - 40)
        if MpCanvas.room_mode == 0:
            MpCanvas.box_y = (MpCanvas.box_y - 6)
        Draw.draw_image(graphics, MpCanvas.ui_images[17], (MpCanvas.box_x - 12), MpCanvas.box_y, 0)
        Draw.draw_image(graphics, MpCanvas.ui_images[16], ((MpCanvas.box_x - 36) - 1), (MpCanvas.box_y + 16), 0)
        Draw.draw_image(graphics, MpCanvas.ui_images[15], ((MpCanvas.box_x + 12) + 1), (MpCanvas.box_y + 16), 0)
        MpCanvas.bs = False
        if MpCanvas.skill_slot_count > 0:
            MpCanvas.loop_k = 0
            while MpCanvas.loop_k < MpCanvas.skill_slot_count:
                if MpCanvas.fighter_mp[0] >= MpCanvas.skill_costs[(MpCanvas.skill_slots[MpCanvas.loop_k] - 3)]:
                    MpCanvas.bs = True
                MpCanvas.loop_k = MpCanvas.loop_k + 1
        Draw.draw_image(graphics, MpCanvas.ui_images[(18 + ((0 if MpCanvas.bs else 1)))], (MpCanvas.box_x - 12), (MpCanvas.box_y + 30), 0)
        if MpCanvas.bB != 99:
            n2 = 0
            n3 = 0
            if MpCanvas.bB == 0:
                n3 = ((MpCanvas.box_x + 12) + 1)
                n2 = (MpCanvas.box_y + 16)
            elif MpCanvas.bB == 1:
                n3 = ((MpCanvas.box_x - 36) - 1)
                n2 = (MpCanvas.box_y + 16)
            elif MpCanvas.bB == 2:
                n3 = (MpCanvas.box_x - 12)
                n2 = MpCanvas.box_y
            else:
                n3 = (MpCanvas.box_x - 12)
                n2 = (MpCanvas.box_y + 30)
            Draw.draw_rect(graphics, (n3 - 1), (n2 - 1), 24, 24, 15721306)
            Draw.draw_rect(graphics, n3, n2, 23, 23, 15721306)

    def d_GI(self, graphics, n2):  # g.java:5297
        n3 = 0
        if MpCanvas.room_mode == 0:
            n3 = 25
        _sw112 = n2
        if _sw112 == 0:
            if MpCanvas.ba > 5:
                self.draw_box(graphics, MpCanvas.center_x, ((MpCanvas.center_y + 28) + n3), 120, 27, 0)
                self.draw_text_centred(MpCanvas.center_x, ((MpCanvas.center_y + 17) + n3), Consts.eX[0], 0xFFFFFF)
                self.draw_text_centred(MpCanvas.center_x, ((MpCanvas.center_y + 28) + n3), Consts.eX[1], (0x646464 if MpCanvas.G else 0xFFFFFF))
                return
            self.draw_box(graphics, MpCanvas.center_x, ((MpCanvas.center_y + 28) + n3), 26, 26, 0)
            self.c_GIII(graphics, (MpCanvas.center_x - 4), ((MpCanvas.center_y + 22) + n3), MpCanvas.ba)
            return
        elif _sw112 == 1:
            self.draw_box(graphics, MpCanvas.center_x, ((MpCanvas.center_y + 28) + n3), 120, 27, 0)
            self.draw_text_centred(MpCanvas.center_x, ((MpCanvas.center_y + 23) + n3), Consts.eX[17], 0xFFFFFF)
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
            self.draw_text_left((MpCanvas.center_x - 30), ((MpCanvas.center_y + 23) + n3), _js(Consts.eX[7], string), 0xFFFFFF)

    def check_invite_timeout(self):  # g.java:5334
        if MpCanvas.u:
            if idiv(((MpCanvas.v - system.currentTimeMillis())), 1000) >= 80:
                MpCanvas.u = False
                MpCanvas.cw = 13
                MpCanvas.popup_shown = False
                MpCanvas.disconnect()
                MpCanvas.b_I((-1))
                self.push_state(4)
                return
        else:
            MpCanvas.u = True
            MpCanvas.v = system.currentTimeMillis()

    def T_v(self):  # g.java:5351
        n2 = (MpCanvas.center_y - 57)
        self.k_G(MpCanvas.screen_g)
        MpCanvas.fill_rect(((MpCanvas.center_x - 52) - 7), (n2 - 2), 118, 123, 0)
        MpCanvas.draw_rect(((MpCanvas.center_x - 52) - 7), (n2 - 2), 118, 123, 0x949694)
        MpCanvas.fill_rect(((MpCanvas.center_x - 52) - 6), (n2 - 1), 116, 13, 0x313431)
        MpCanvas.bv = 0
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < MpCanvas.be:
            _sw113 = MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]
            if _sw113 == 0:
                MpCanvas.bv = (MpCanvas.bv + Consts.ey[MpCanvas.loop_i])
            elif _sw113 == 1:
                MpCanvas.bv = (MpCanvas.bv + Consts.eA[MpCanvas.loop_i])
            elif _sw113 == 2:
                MpCanvas.bv = (MpCanvas.bv + Consts.eC[MpCanvas.loop_i])
            elif _sw113 == 3:
                MpCanvas.bv = (MpCanvas.bv + Consts.eE[MpCanvas.loop_i])
            elif _sw113 == 4:
                MpCanvas.bv = (MpCanvas.bv + Consts.eG[MpCanvas.loop_i])
            elif _sw113 == 5:
                MpCanvas.bv = (MpCanvas.bv + Consts.eI[MpCanvas.loop_i])
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        _sw114 = MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]
        if _sw114 == 0:
            self.draw_text_centred(MpCanvas.center_x, n2, Consts.ex[MpCanvas.bv], 0xFFFFFF)
            MpCanvas.bJ = Consts.ey[MpCanvas.be]
        elif _sw114 == 1:
            self.draw_text_centred(MpCanvas.center_x, n2, Consts.ez[MpCanvas.bv], 0xFFFFFF)
            MpCanvas.bJ = Consts.eA[MpCanvas.be]
        elif _sw114 == 2:
            self.draw_text_centred(MpCanvas.center_x, n2, Consts.eB[MpCanvas.bv], 0xFFFFFF)
            MpCanvas.bJ = Consts.eC[MpCanvas.be]
        elif _sw114 == 3:
            self.draw_text_centred(MpCanvas.center_x, n2, Consts.eD[MpCanvas.bv], 0xFFFFFF)
            MpCanvas.bJ = Consts.eE[MpCanvas.be]
        elif _sw114 == 4:
            self.draw_text_centred(MpCanvas.center_x, n2, Consts.eF[MpCanvas.bv], 0xFFFFFF)
            MpCanvas.bJ = Consts.eG[MpCanvas.be]
        elif _sw114 == 5:
            self.draw_text_centred(MpCanvas.center_x, n2, Consts.eH[MpCanvas.bv], 0xFFFFFF)
            MpCanvas.bJ = Consts.eI[MpCanvas.be]
        MpCanvas.loop_i = 1
        while MpCanvas.loop_i < MpCanvas.bJ:
            _sw115 = MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]
            _m116 = False
            while True:
                if _m116 or _sw115 == 0:
                    _m116 = True
                    self.draw_text_left((MpCanvas.center_x - 56), ((n2 + (MpCanvas.loop_i * 12)) + 1), Consts.ex[(MpCanvas.bv + MpCanvas.loop_i)], 0xFFFFFF)
                    break
                if _m116 or _sw115 == 1:
                    _m116 = True
                    self.draw_text_left((MpCanvas.center_x - 56), ((n2 + (MpCanvas.loop_i * 12)) + 1), Consts.ez[(MpCanvas.bv + MpCanvas.loop_i)], 0xFFFFFF)
                    break
                if _m116 or _sw115 == 2:
                    _m116 = True
                    self.draw_text_left((MpCanvas.center_x - 56), ((n2 + (MpCanvas.loop_i * 12)) + 1), Consts.eB[(MpCanvas.bv + MpCanvas.loop_i)], 0xFFFFFF)
                    break
                if _m116 or _sw115 == 3:
                    _m116 = True
                    self.draw_text_left((MpCanvas.center_x - 56), ((n2 + (MpCanvas.loop_i * 12)) + 1), Consts.eD[(MpCanvas.bv + MpCanvas.loop_i)], 0xFFFFFF)
                    break
                if _m116 or _sw115 == 4:
                    _m116 = True
                    self.draw_text_centred(MpCanvas.center_x, ((n2 + (MpCanvas.loop_i * 17)) + 9), Consts.eF[(MpCanvas.bv + MpCanvas.loop_i)], 0xFFFFFF)
                    if MpCanvas.loop_i != 3:
                        break
                    self.draw_text_centred(MpCanvas.center_x, ((n2 + (MpCanvas.loop_i * 17)) + 9), _js("v", MpCanvas.app_version), 0xFFFFFF)
                    break
                if _m116 or _sw115 == 5:
                    _m116 = True
                    self.draw_text_left((MpCanvas.center_x - 56), ((n2 + (MpCanvas.loop_i * 12)) + 1), Consts.eH[(MpCanvas.bv + MpCanvas.loop_i)], 0xFFFFFF)
                break
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        if Consts.ew[MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]] > 1:
            self.draw_text_centred(MpCanvas.center_x, ((n2 + 72) + 38), _js(_js((MpCanvas.be + 1), "/"), Consts.ew[MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]]), 0xFFFFFF)
            MpCanvas.c_IIM((MpCanvas.center_x - 35), ((n2 + 72) + 39), MpCanvas.arrow_images[1])
            MpCanvas.b_IIM((MpCanvas.center_x + 35), ((n2 + 72) + 39), MpCanvas.arrow_images[1])

    def U_v(self):  # g.java:5456
        self.draw_window_bg(MpCanvas.buffer_g)
        n2 = idiv(80, MpCanvas.k)
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
        while MpCanvas.loop_i < MpCanvas.k:
            Draw.draw_image_part(MpCanvas.buffer_g, MpCanvas.menu_icon_image, (idiv((((MpCanvas.canvas_w - (n2 * ((MpCanvas.k - 1)))) - 11)), 2) + (n2 * MpCanvas.loop_i)), ((MpCanvas.center_y + 6) + n3), 12, 15, 12, 0)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def V_v(self):  # g.java:5477
        if MpCanvas.bn:
            self.load_named_image(MpCanvas.dC[1], "spreff2_r", 1)
        else:
            self.load_named_image(MpCanvas.dC[1], "spreff2", 0)
        if MpCanvas.dE[0] is None:
            MpCanvas.dE[0] = SpriteFrames("/spreff3.SP2")

    @staticmethod
    def e_GI(graphics, n2):  # g.java:5488
        n3 = ((n2 * 2) + imod(MpCanvas.state_ticks, 2))
        if MpCanvas.bn:
            Draw.draw_image_part(graphics, MpCanvas.dC[1][1], (MpCanvas.canvas_w - (((MpCanvas.draw_x - MpCanvas.dE[0].anchor_x[n3]) + MpCanvas.dE[0].w[n3]))), (MpCanvas.draw_y - MpCanvas.dE[0].anchor_y[n3]), MpCanvas.dE[0].w[n3], MpCanvas.dE[0].h[n3], MpCanvas.dE[0].src_x[n3], MpCanvas.dE[0].src_y[n3])
            return
        Draw.draw_image_part(graphics, MpCanvas.dC[1][0], (MpCanvas.draw_x - MpCanvas.dE[0].anchor_x[n3]), (MpCanvas.draw_y - MpCanvas.dE[0].anchor_y[n3]), MpCanvas.dE[0].w[n3], MpCanvas.dE[0].h[n3], MpCanvas.dE[0].src_x[n3], MpCanvas.dE[0].src_y[n3])

    def load_numbered_image(self, imageArray, string, n2):  # g.java:5497
        if imageArray[n2] is None:
            imageArray[n2] = self.load_image(_js(_js(_js("/", string), n2), ".png"))

    def load_named_image(self, imageArray, string, n2):  # g.java:5503
        if imageArray[n2] is None:
            imageArray[n2] = self.load_image(_js(_js("/", string), ".png"))

    def load_sprite(self, imageArray, aArray, string):  # g.java:5509
        self.load_sprite_dir(imageArray, aArray, string, 1)

    def load_sprite_dir(self, imageArray, aArray, string, n2):  # g.java:5513
        if MpCanvas.bn:
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
        MpCanvas.X_v()

    @staticmethod
    def X_v():  # g.java:5599
        None

    def load_bg(self, n2):  # g.java:5603
        if MpCanvas.bg_images[n2] is None:
            MpCanvas.bg_images[n2] = self.load_image(_js(_js("/gamebg", n2), ".png"))

    def Y_v(self):  # g.java:5609
        Draw.fill_rect(MpCanvas.buffer_g, 0, 0, MpCanvas.canvas_w, 12, 0)
        MpCanvas.o_I(0)
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
        MpCanvas.o_I(1)
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
            MpCanvas.o_I(2)
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
            MpCanvas.o_I(3)
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
    def o_I(n2):  # g.java:5663
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

    def k_G(self, graphics):  # g.java:5678
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
        self.draw_text_colored(graphics, MpCanvas.c, idiv(MpCanvas.canvas_w, 2), 2, 1, 0xFFFFFF)

    def a_GTIIIIZZ(self, graphics, string, n2, n3, n4, n5, bl, bl2):  # g.java:5730
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

    def m_G(self, graphics):  # g.java:5748
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.fighter_present[MpCanvas.loop_i]:
                if imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0:
                    if MpCanvas.fighter_kind[MpCanvas.loop_i] == 0:
                        self.load_numbered_image(MpCanvas.face_images, "face", MpCanvas.fighter_face[MpCanvas.loop_i])
                        MpCanvas.c_GIIM(graphics, 0, (0 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (MpCanvas.canvas_h - 12)), MpCanvas.face_images[MpCanvas.fighter_face[MpCanvas.loop_i]])
                        MpCanvas.face_images[MpCanvas.fighter_face[MpCanvas.loop_i]] = None
                    self.draw_box(graphics, 0, (12 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_h - 12) - 15)), 60, 15, 1)
                    if (len(MpCanvas.fighter_alt_name[MpCanvas.loop_i]) == 0) or (imod(MpCanvas.aR, 2) == 0):
                        self.draw_text_centred_on(graphics, 30, (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), MpCanvas.fighter_name[MpCanvas.loop_i], 0xFFFFFF)
                    else:
                        self.draw_text_centred_on(graphics, 30, (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), MpCanvas.fighter_alt_name[MpCanvas.loop_i], 0xFFFFFF)
                else:
                    if MpCanvas.fighter_kind[MpCanvas.loop_i] == 0:
                        self.load_numbered_image(MpCanvas.face_images, "face", MpCanvas.fighter_face[MpCanvas.loop_i])
                        MpCanvas.b_GIIM(graphics, MpCanvas.canvas_w, (0 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (MpCanvas.canvas_h - 12)), MpCanvas.face_images[MpCanvas.fighter_face[MpCanvas.loop_i]])
                        MpCanvas.face_images[MpCanvas.fighter_face[MpCanvas.loop_i]] = None
                    self.draw_box(graphics, (MpCanvas.canvas_w - 60), (12 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else ((MpCanvas.canvas_h - 12) - 15)), 60, 15, 1)
                    if (len(MpCanvas.fighter_alt_name[MpCanvas.loop_i]) == 0) or (imod(MpCanvas.aR, 2) == 0):
                        self.draw_text_centred_on(graphics, (MpCanvas.canvas_w - 30), (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), MpCanvas.fighter_name[MpCanvas.loop_i], 0xFFFFFF)
                    else:
                        self.draw_text_centred_on(graphics, (MpCanvas.canvas_w - 30), (14 if (idiv(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == 0) else (((MpCanvas.canvas_h - 12) - 15) + 2)), MpCanvas.fighter_alt_name[MpCanvas.loop_i], 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.X_v()

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

    def o_G(self, graphics):  # g.java:5820
        self.k_G(graphics)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 3:
            self.draw_box(graphics, (MpCanvas.center_x - 58), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 19)), 61, 14, 2)
            self.draw_text_colored(graphics, Consts.eW[MpCanvas.loop_i], (MpCanvas.center_x - 28), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 19)), 1, 0x646464)
            self.draw_box(graphics, (MpCanvas.center_x + 13), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 19)), 39, 14, 2)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def Z_v(self):  # g.java:5831
        self.k_G(MpCanvas.screen_g)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 6:
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 60), ((MpCanvas.center_y - 47) + (MpCanvas.loop_i * 17)), 81, 14, 2)
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x + 23), ((MpCanvas.center_y - 47) + (MpCanvas.loop_i * 17)), 37, 14, 2)
            self.draw_text_colored(MpCanvas.screen_g, Consts.eX[(46 + MpCanvas.loop_i)], (MpCanvas.center_x - 19), ((MpCanvas.center_y - 45) + (MpCanvas.loop_i * 17)), 1, 0xFFFFFF)
            _sw118 = MpCanvas.loop_i
            if _sw118 == 0:
                self.c_III((MpCanvas.center_x + 52), ((MpCanvas.center_y - 44) + (MpCanvas.loop_i * 17)), MpCanvas.level)
            elif _sw118 == 1:
                self.e_III((MpCanvas.center_x + 52), ((MpCanvas.center_y - 44) + (MpCanvas.loop_i * 17)), MpCanvas.fame)
            elif _sw118 == 2:
                MpCanvas.cu = MpCanvas.duel_grade
            elif _sw118 == 3:
                MpCanvas.cu = MpCanvas.wins
            elif _sw118 == 4:
                MpCanvas.cu = MpCanvas.losses
            elif _sw118 == 5:
                MpCanvas.cu = MpCanvas.mission_grade
            if MpCanvas.loop_i > 1:
                self.d_III((MpCanvas.center_x + 52), ((MpCanvas.center_y - 44) + (MpCanvas.loop_i * 17)), MpCanvas.cu)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def aa_v(self):  # g.java:5870
        self.k_G(MpCanvas.screen_g)
        n2 = 0
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 54), ((MpCanvas.center_y - 30) + (MpCanvas.loop_i * 17)), 39, 14, 2)
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 13), ((MpCanvas.center_y - 30) + (MpCanvas.loop_i * 17)), 67, 14, 2)
            self.draw_text_colored(MpCanvas.screen_g, Consts.eX[(42 + MpCanvas.loop_i)], (MpCanvas.center_x - 35), ((MpCanvas.center_y - 28) + (MpCanvas.loop_i * 17)), 1, 0xFFFFFF)
            _sw119 = MpCanvas.loop_i
            if _sw119 == 0:
                MpCanvas.cu = MpCanvas.attr_hp
                n2 = MpCanvas.attr_hp_bonus
            elif _sw119 == 1:
                MpCanvas.cu = MpCanvas.attr_mp
                n2 = MpCanvas.attr_mp_bonus
            elif _sw119 == 2:
                MpCanvas.cu = MpCanvas.attr_attack
                n2 = MpCanvas.attr_attack_bonus
            elif _sw119 == 3:
                MpCanvas.cu = MpCanvas.attr_defense
                n2 = MpCanvas.attr_defense_bonus
            self.b_III((MpCanvas.center_x + 9), ((MpCanvas.center_y - 27) + (MpCanvas.loop_i * 17)), MpCanvas.cu)
            self.a_III((MpCanvas.center_x + 52), ((MpCanvas.center_y - 27) + (MpCanvas.loop_i * 17)), n2)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def p_G(self, graphics):  # g.java:5905
        self.k_G(graphics)
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

    def ab_v(self):  # g.java:5922
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 4:
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                if imod(MpCanvas.state_ticks, 4) < 2:
                    MpCanvas.c_IIM((MpCanvas.center_x - 65), ((MpCanvas.center_y - 32) + (MpCanvas.loop_i * 16)), MpCanvas.arrow_images[1])
                    MpCanvas.b_IIM((MpCanvas.center_x + 40), ((MpCanvas.center_y - 32) + (MpCanvas.loop_i * 16)), MpCanvas.arrow_images[1])
                self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 58), ((MpCanvas.center_y - 35) + (MpCanvas.loop_i * 16)), 91, 14, 3)
                self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x + 43), ((MpCanvas.center_y - 35) + (MpCanvas.loop_i * 16)), 15, 14, 3)
            if MpCanvas.skill_levels[(MpCanvas.cB[MpCanvas.loop_i] - 3)] == 99:
                self.draw_text_centred_on(MpCanvas.screen_g, (MpCanvas.center_x - 12), ((MpCanvas.center_y - 33) + (MpCanvas.loop_i * 16)), Consts.eK[(MpCanvas.cB[MpCanvas.loop_i] - 3)], 0x646464)
                if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                    self.draw_text_left((MpCanvas.center_x - 50), (MpCanvas.center_y + 32), Consts.eX[34], 0x646464)
            else:
                self.draw_text_centred_on(MpCanvas.screen_g, (MpCanvas.center_x - 12), ((MpCanvas.center_y - 33) + (MpCanvas.loop_i * 16)), Consts.eK[(MpCanvas.cB[MpCanvas.loop_i] - 3)], 0xFFFFFF)
                self.c_III((MpCanvas.center_x + 48), ((MpCanvas.center_y - 32) + (MpCanvas.loop_i * 16)), MpCanvas.skill_levels[(MpCanvas.cB[MpCanvas.loop_i] - 3)])
                if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                    self.draw_text_left((MpCanvas.center_x - 50), (MpCanvas.center_y + 32), Consts.eJ[(((MpCanvas.cB[MpCanvas.loop_i] - 3)) * 2)], 0xFFFFFF)
                    self.draw_text_left((MpCanvas.center_x - 50), (MpCanvas.center_y + 45), Consts.eJ[((((MpCanvas.cB[MpCanvas.loop_i] - 3)) * 2) + 1)], 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def ac_v(self):  # g.java:5950
        self.k_G(MpCanvas.screen_g)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 3:
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 50), ((MpCanvas.center_y - 45) + (MpCanvas.loop_i * 34)), 100, 14, 2)
            self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 50), ((MpCanvas.center_y - 32) + (MpCanvas.loop_i * 34)), 100, 14, 2)
            self.draw_text_colored(MpCanvas.screen_g, Consts.eX[(52 + MpCanvas.loop_i)], MpCanvas.center_x, ((MpCanvas.center_y - 43) + (MpCanvas.loop_i * 34)), 1, 0xFFFFFF)
            _sw120 = MpCanvas.loop_i
            if _sw120 == 0:
                MpCanvas.cu = MpCanvas.exp
            elif _sw120 == 1:
                MpCanvas.cu = MpCanvas.fame
            elif _sw120 == 2:
                MpCanvas.cu = MpCanvas.gold
            self.d_III((MpCanvas.center_x + 24), ((MpCanvas.center_y - 29) + (MpCanvas.loop_i * 34)), MpCanvas.cu)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def q_G(self, graphics):  # g.java:5975
        self.k_G(graphics)
        self.draw_box(graphics, (MpCanvas.center_x - 62), (MpCanvas.center_y + 7), 126, 16, 6)

    def r_G(self, graphics):  # g.java:5980
        string = MpCanvas.input_text
        self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 44), _js(_js(Consts.eX[58], "."), ((MpCanvas.B + 1))), 16400640)
        if MpCanvas.B == 0:
            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 32), Consts.eX[23], 0xFFFFFF)
            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 20), Consts.eX[24], 0xFFFFFF)
        else:
            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 32), Consts.eX[15], 0xFFFFFF)
            self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 20), Consts.eX[16], 0xFFFFFF)
        self.draw_text_centred(MpCanvas.center_x, (MpCanvas.center_y - 8), Consts.eX[25], 0xFFFFFF)
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

    def s_G(self, graphics):  # g.java:6093
        self.k_G(graphics)
        self.draw_box(graphics, (MpCanvas.center_x - 62), (MpCanvas.center_y + 7), 126, 16, 6)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 32), Consts.eU[0], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 20), Consts.eU[1], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 8), Consts.eU[2], 0xFFFFFF)

    def t_G(self, graphics):  # g.java:6101
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y + 9), MpCanvas.input_text, 0x41FF41)
        if imod(MpCanvas.state_ticks, 4) < 2:
            n2 = MpCanvas.font_white.string_width(MpCanvas.input_text)
            if len(MpCanvas.input_text) == 8:
                n2 = (n2 - (MpCanvas.font_white.string_width("A") * 2))
            MpCanvas.draw_line_color(graphics, (MpCanvas.center_x + idiv(n2, 2)), (MpCanvas.center_y + 20), ((MpCanvas.center_x + idiv(n2, 2)) + 4), (MpCanvas.center_y + 20), 0xFFFFFF)
        MpCanvas.draw_letter_grid(MpCanvas.letter_cursor, (MpCanvas.center_y + 27))

    def u_G(self, graphics):  # g.java:6113
        self.draw_box(graphics, (MpCanvas.center_x - 60), ((MpCanvas.center_y - 35) - 5), 120, 94, 5)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 32), Consts.eU[3], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 20), Consts.eU[4], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 8), Consts.eU[5], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y + 8), MpCanvas.input_text, 0x41FF41)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 2:
            self.draw_box(graphics, ((MpCanvas.center_x - 42) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 35), 29, 14, 2)
            self.draw_text_colored(graphics, Consts.eX[(40 + MpCanvas.loop_i)], ((MpCanvas.center_x - 28) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 38), 1, 0x646464)
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] == MpCanvas.loop_i:
                self.draw_text_colored(graphics, Consts.eX[(40 + MpCanvas.loop_i)], ((MpCanvas.center_x - 28) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 38), 1, 0xFFFFFF)
                self.draw_box(graphics, ((MpCanvas.center_x - 42) + (MpCanvas.loop_i * 55)), (MpCanvas.center_y + 35), 29, 14, 3)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def v_G(self, graphics):  # g.java:6131
        self.draw_box(graphics, (MpCanvas.center_x - 53), (MpCanvas.center_y - 34), 106, 68, 5)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 22), Consts.eX[56], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 7), Consts.eX[57], 0xFFFFFF)
        n2 = 0
        while n2 < 2:
            self.draw_box(graphics, ((MpCanvas.center_x - 42) + (n2 * 55)), (MpCanvas.center_y + 15), 29, 14, (3 if (MpCanvas.popup_cursor == n2) else 2))
            self.draw_text_colored(graphics, Consts.eX[(40 + n2)], ((MpCanvas.center_x - 27) + (n2 * 55)), (MpCanvas.center_y + 17), 1, (0xFFFFFF if (MpCanvas.popup_cursor == n2) else 0x646464))
            n2 = n2 + 1

    def ad_v(self):  # g.java:6143
        MpCanvas.bu = 0
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < MpCanvas.cw:
            MpCanvas.bu = (MpCanvas.bu + Consts.eZ[MpCanvas.loop_i])
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.bJ = 0
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < Consts.eZ[MpCanvas.cw]:
            MpCanvas.bw = True
            if MpCanvas.bw:
                MpCanvas.text_lines[MpCanvas.loop_i] = Consts.eY[(MpCanvas.bu + MpCanvas.loop_i)]
            if MpCanvas.bJ < len(MpCanvas.text_lines[MpCanvas.loop_i]):
                MpCanvas.bJ = len(MpCanvas.text_lines[MpCanvas.loop_i])
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        MpCanvas.loop_j = 0
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, (MpCanvas.bJ * 7), (((((Consts.eZ[MpCanvas.cw] + 1)) * 15) + MpCanvas.loop_j) + 4), 0)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < Consts.eZ[MpCanvas.cw]:
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((((MpCanvas.center_y - idiv((Consts.eZ[MpCanvas.cw] * 15), 2)) + (MpCanvas.loop_i * 15)) - 4) - idiv(MpCanvas.loop_j, 3)), MpCanvas.text_lines[MpCanvas.loop_i], 0xFFFFFF)
            MpCanvas.loop_i = MpCanvas.loop_i + 1
        self.r_I(((MpCanvas.center_y + idiv((Consts.eZ[MpCanvas.cw] * 15), 2)) - 5))

    def w_G(self, graphics):  # g.java:6172
        self.k_G(graphics)
        MpCanvas.loop_i = 0
        while MpCanvas.loop_i < 2:
            self.draw_box(graphics, (MpCanvas.center_x - 56), ((MpCanvas.center_y - 16) + (MpCanvas.loop_i * 20)), 111, 14, 2)
            self.draw_text_colored(graphics, Consts.eX[(38 + MpCanvas.loop_i)], idiv(MpCanvas.screen_w, 2), ((MpCanvas.center_y - 15) + (MpCanvas.loop_i * 20)), 1, 0x646464)
            MpCanvas.loop_i = MpCanvas.loop_i + 1

    def f_GI(self, graphics, n2):  # g.java:6182
        self.k_G(graphics)
        n3 = 0
        while n3 < 5:
            self.draw_text_centred_on(graphics, MpCanvas.center_x, (n2 + (12 * n3)), Consts.eU[(((6 if (MpCanvas.room_mode == 0) else 12)) + n3)], 0xFFFFFF)
            n3 = n3 + 1
        self.draw_box(graphics, (MpCanvas.center_x - 40), (n2 + 59), 80, 15, 6)

    def ae_v(self):  # g.java:6192
        string = ""
        if imod(MpCanvas.state_ticks, 4) == 1:
            string = "."
        elif imod(MpCanvas.state_ticks, 4) == 2:
            string = ".."
        elif imod(MpCanvas.state_ticks, 4) == 3:
            string = "..."
        n2 = (MpCanvas.font_white.string_width(Consts.fa[MpCanvas.cv]) + 14)
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, (n2 + 22), 30, 0)
        self.draw_text_left_on(MpCanvas.screen_g, (MpCanvas.center_x - idiv(n2, 2)), ((MpCanvas.center_y - 7) + 2), _js(Consts.fa[MpCanvas.cv], string), 0xFFFFFF)

    def af_v(self):  # g.java:6206
        string = ""
        if imod(MpCanvas.state_ticks, 4) == 1:
            string = "."
        elif imod(MpCanvas.state_ticks, 4) == 2:
            string = ".."
        elif imod(MpCanvas.state_ticks, 4) == 3:
            string = "..."
        n2 = (MpCanvas.font_white.string_width(Consts.eX[7]) + 14)
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x, MpCanvas.center_y, (n2 + 22), 30, 0)
        self.draw_text_left_on(MpCanvas.screen_g, (MpCanvas.center_x - idiv(n2, 2)), (MpCanvas.center_y - 6), _js(Consts.eX[7], string), 0xFFFFFF)

    def c_II(self, n2, n3):  # g.java:6220
        if n2 != (-1):
            MpCanvas.draw_image_on(MpCanvas.screen_g, 0, (MpCanvas.screen_h - 11), MpCanvas.softkey_image)
            self.draw_text_centred_on(MpCanvas.screen_g, 28, (MpCanvas.screen_h - 11), Consts.eT[n2], 0xFFFFFF)
        if n3 != (-1):
            MpCanvas.draw_image_on(MpCanvas.screen_g, (MpCanvas.screen_w - 57), (MpCanvas.screen_h - 11), MpCanvas.softkey_image)
            self.draw_text_centred_on(MpCanvas.screen_g, (MpCanvas.screen_w - 28), (MpCanvas.screen_h - 11), Consts.eT[n3], 0xFFFFFF)

    def r_I(self, n2):  # g.java:6231
        self.draw_box(MpCanvas.screen_g, (MpCanvas.center_x - 10), (n2 + 1), 18, 9, 3)
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, n2, Consts.eT[0], 0xFFFFFF)

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
    MpCanvas.c = ""
    MpCanvas.d = 0
    MpCanvas.screen_g = None
    MpCanvas.rng = Random()
    MpCanvas.k = 7
    MpCanvas.key = (-999)
    MpCanvas.font_white = None
    MpCanvas.font_orange = None
    MpCanvas.font_gray = None
    MpCanvas.font_green = None
    MpCanvas.u = False
    MpCanvas.w = False
    MpCanvas.popup_shown = False
    MpCanvas.D = False
    MpCanvas.pause_request = 0
    MpCanvas.music_to_resume = (-1)
    MpCanvas.paused = False
    MpCanvas.K = False
    MpCanvas.L = False
    MpCanvas.O = True
    MpCanvas.P = True
    MpCanvas.rank_names = [None] * (3)
    MpCanvas.rank_ranks = [0] * (3)
    MpCanvas.rank_values = [0] * (3)
    MpCanvas.my_ranks = [0, 0, 0, 0]
    MpCanvas.volume = 4
    MpCanvas.speed = 1
    MpCanvas.invitation_saved = 1
    MpCanvas.bx = True
    MpCanvas.skill_slots = [0] * (4)
    MpCanvas.bF = [None] * (4)
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
    MpCanvas.cc = [0] * (4)
    MpCanvas.cd = [0] * (4)
    MpCanvas.ce = [0] * (4)
    MpCanvas.fighter_hp_target = [0] * (4)
    MpCanvas.fighter_mp_target = [0] * (4)
    MpCanvas.fighter_hp_step = [0] * (4)
    MpCanvas.fighter_mp_step = [0] * (4)
    MpCanvas.fighter_hp_delta = [0] * (4)
    MpCanvas.fighter_x = [0] * (4)
    MpCanvas.fighter_y = [0] * (4)
    MpCanvas.cm = [0] * (4)
    MpCanvas.fighter_frame = [0] * (4)
    MpCanvas.fighter_blink = [0] * (4)
    MpCanvas.fighter_status = [0] * (4)
    MpCanvas.fighter_status_ticks = [0] * (4)
    MpCanvas.cr = [0] * (4)
    MpCanvas.cB = [0] * (4)
    MpCanvas.skill_levels = [0] * (11)
    MpCanvas.skill_costs = [0] * (11)
    MpCanvas.turn_hps = [0] * (12)
    MpCanvas.turn_bytes = [0] * (44)
    MpCanvas.dc = 100
    MpCanvas.mpic_images = [None] * (6)
    MpCanvas.face_images = [None] * (4)
    MpCanvas.ui_images = [None] * (57)
    MpCanvas.act_images = [None] * (18)
    MpCanvas.number_images = [None] * (8)
    MpCanvas.arrow_images = [None] * (2)
    MpCanvas.bg_images = [None] * (22)
    MpCanvas.du = [None] * (2)
    MpCanvas.dv = [None] * (3)
    MpCanvas.dw = [[None] * (2) for _ in range(10)]
    MpCanvas.dx = [[None] * (3) for _ in range(10)]
    MpCanvas.dy = [[None] * (2) for _ in range(2)]
    MpCanvas.dz = [[None] * (3) for _ in range(2)]
    MpCanvas.dA = [[None] * (2) for _ in range(2)]
    MpCanvas.dB = [[None] * (3) for _ in range(2)]
    MpCanvas.dC = [[None] * (2) for _ in range(2)]
    MpCanvas.dD = [[None] * (3) for _ in range(2)]
    MpCanvas.dE = [None] * (1)
    MpCanvas.dF = [None] * (2)
    MpCanvas.dG = [None] * (3)
    MpCanvas.dH = [None] * (2)
    MpCanvas.dI = [None] * (1)
    MpCanvas.dJ = [None] * (2)
    MpCanvas.dK = [None] * (1)
    MpCanvas.dL = [None] * (2)
    MpCanvas.dM = [None] * (1)
    MpCanvas.dN = [None] * (2)
    MpCanvas.dO = [None] * (1)
    MpCanvas.cursor_stack = [0] * (10)
    MpCanvas.state_stack = [0] * (10)
    MpCanvas.stack_depth = 0
    MpCanvas.dX = False
    MpCanvas.painted = True
    MpCanvas.dZ = 0
    MpCanvas.disconnecting = False
    MpCanvas.eb = False
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
