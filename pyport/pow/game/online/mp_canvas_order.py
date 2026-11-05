"""PORT-EXTRA (asked by Andrey, plan item 22): the Order window of the online game.

Not in the original jar. A seventh picture of the main menu carousel opens it; "2-on-2 Order"
in the Duel menu and "Order Ally" in the Mission menu open it as a pick list, where FIRE on a
member invites them at once (2-on-2 Together / Mission Together). An order is a
name and up to 30 players (pow_server/orders.py); the window shows who is in it and who is
online, and invites a member to a mission (768 mode 2, the jar's Invite An Ally) or to a
2-on-2 duel on my side (768 mode 3). Nothing of it reaches the single player.

States (unused numbers of the jar's menu range, so the menu music plays on):
    30  the order: its members, then "Leave Order"; without an order the Create / Join menu
    31  a member: Mission Together / 2-on-2 Together
    32  the order name on the A-Z grid (create or join)
    33  "Leave the order?" Yes / No
The window is drawn with the jar's own pieces (window, panels, boxes, buttons, fonts).
"""
from pow.game.online.rt import idiv, imod

MpCanvas = None   # set by pow/game/online/mp_canvas.py
Consts = Draw = None   # set by mp_canvas._late_imports

ORDER = 30
MEMBER = 31
NAME_INPUT = 32
LEAVE = 33
MAIN_MENU_ITEM = 6          # the main menu carousel: 0 Duel .. 5 Ranking, 6 Order
VISIBLE_ROWS = 9
MAX_MEMBERS = 30
ROW_H = 17

TEXTS = ["Order", "Create Order", "Join Order", "Leave Order", "Mission Together",
         "2-on-2 Together", "Leave the order?", "Online"]
DUEL_ITEM, MISSION_ITEM = "2-on-2 Order", "Order Ally"   # the 4th Duel / 3rd Mission menu item
PICK_TITLES = {2: MISSION_ITEM, 3: DUEL_ITEM}
PROMPTS = (["Enter the name", "of your new order.", "(4-12 letters)"],
           ["Enter the name", "of the order", "you wish to join.", "(4-12 letters)"])
# error_msg 19.. (Consts.error_lines / error_line_counts are extended by install())
ERRORS = (["No such order."], ["The order is full.", "(30 members)"],
          ["You are already", "in an order."], ["The player is not", "in your order."])
ERR_FIRST = 19
# server status -> error_msg
STATUS_ERRORS = {-6: 6, -49: 5, -20: ERR_FIRST, -21: ERR_FIRST + 1, -22: ERR_FIRST + 2,
                 -23: ERR_FIRST + 3}


def install():
    """Adds the texts the window needs to the jar's tables (once per run)."""
    if DUEL_ITEM not in Consts.duel_menu:
        Consts.duel_menu.append(DUEL_ITEM)
        Consts.mission_menu.append(MISSION_ITEM)
    if len(Consts.error_line_counts) == ERR_FIRST:
        for lines in ERRORS:
            Consts.error_lines.extend(lines)
            Consts.error_line_counts.append(len(lines))


class OrderMixin:
    order_name = ""             # "" = in no order
    order_rows = []             # [(UserID, display name, level, online, leader)]
    order_cursor = 0            # members then "Leave Order"
    order_top = 0               # first row shown
    order_creating = True       # 32: create (True) or join (False)
    order_invite = False        # the battle came from the window: back to it afterwards
    order_count = 0
    order_pick = 0              # opened from Duel (3) / Mission (2): FIRE on a member invites

    # --- requests ------------------------------------------------------------------
    def open_order(self, pick=0):
        """Asks the server for my order; the answer (1793) shows the window. pick: 768 mode a
        member is invited with at once (2 mission, 3 2-on-2 together), 0 = the member menu."""
        install()
        MpCanvas.order_pick = pick
        MpCanvas.loading_msg = 1
        MpCanvas.set_state(3)
        self.send_request(1792)

    # --- answers -------------------------------------------------------------------
    def on_order_info(self, answer):  # 1793
        if MpCanvas.answer_status != 1:
            MpCanvas.error_msg = 0
            self.push_state(4)
            return
        MpCanvas.order_name = answer.read_string(12)
        count = answer.read_s8() & 0xFF
        rows = []
        for _ in range(count):
            uid = answer.read_string(12)
            name = answer.read_string(8)
            level = answer.read_s16() & 0xFFFF
            online = answer.read_s8() != 0
            leader = answer.read_s8() != 0
            rows.append((uid, name, level, online, leader))
        MpCanvas.order_rows = rows
        MpCanvas.order_count = count
        MpCanvas.order_cursor = min(MpCanvas.order_cursor, count)
        if MpCanvas.state_stack[MpCanvas.stack_depth] == ORDER:
            MpCanvas.set_state(ORDER)          # a refresh: the window is on the stack already
        else:
            self.push_state(ORDER)
            MpCanvas.order_cursor = MpCanvas.order_top = 0

    def on_order_changed(self, answer):  # 1795 / 1797 / 1799
        if MpCanvas.answer_status != 1:
            MpCanvas.error_msg = STATUS_ERRORS.get(MpCanvas.answer_status, 0)
            self.push_state(4)
            return
        while MpCanvas.stack_depth > 0 and MpCanvas.state_stack[MpCanvas.stack_depth] != ORDER:
            MpCanvas.stack_depth -= 1          # back to the window, then refresh it
        MpCanvas.cursor_stack[MpCanvas.stack_depth] = 0
        MpCanvas.order_cursor = MpCanvas.order_top = 0
        self.open_order()

    def order_invite_error(self):
        """769 errors of mode 3 the jar does not know."""
        if MpCanvas.answer_status in STATUS_ERRORS and MpCanvas.answer_status <= -20:
            MpCanvas.error_msg = STATUS_ERRORS[MpCanvas.answer_status]
            return True
        return False

    def back_to_order(self):
        """After a battle started from the window (105 -> OK)."""
        MpCanvas.order_invite = False
        self.reset_state_stack(10)
        MpCanvas.cursor_stack[0] = MAIN_MENU_ITEM
        self.open_order()

    # --- painting ------------------------------------------------------------------
    def draw_records_order(self):
        """Character > Records: a 7th row, "Order" and the order's name (orange), "-" without one."""
        y = MpCanvas.center_y - 47 + 6 * 17
        self.draw_box(MpCanvas.screen_g, MpCanvas.center_x - 60, y, 120, 14, 2)
        self.draw_text_colored(MpCanvas.screen_g, TEXTS[0], MpCanvas.center_x - 56, y + 2, 0, 0xFFFFFF)
        name = MpCanvas.order_name or "-"
        self.draw_text_colored(MpCanvas.screen_g, name, MpCanvas.center_x + 56 - MpCanvas.font_white.string_width(name),
                               y + 2, 0, 16400640 if MpCanvas.order_name else 0x646464)

    def _paint_order(self):  # state 30
        if not MpCanvas.order_name:
            return self._paint_order_menu()
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = PICK_TITLES.get(MpCanvas.order_pick, TEXTS[0])
            self.draw_window_bg(MpCanvas.buffer_g)
            x, top = MpCanvas.center_x - 75, MpCanvas.center_y - 100
            MpCanvas.draw_panel(MpCanvas.buffer_g, x, top, 150, 15)
            self.draw_text_colored(MpCanvas.buffer_g, MpCanvas.order_name, x + 4, top + 2, 0, 16400640)
            self.draw_text_colored(MpCanvas.buffer_g, "/%d" % MAX_MEMBERS, x + 150 - 20, top + 2, 0, 0x646464)
            MpCanvas.draw_number(MpCanvas.buffer_g, x + 150 - 27, top + 3, MpCanvas.order_count, 0)
            online = sum(1 for r in MpCanvas.order_rows if r[3])
            self.draw_text_colored(MpCanvas.buffer_g, TEXTS[7], x + 4, top + 20, 0, 0x646464)
            MpCanvas.draw_number(MpCanvas.buffer_g, x + 150 - 7, top + 21, online, 0)
        self.draw_buffer()
        items = MpCanvas.order_count + 1
        cur = MpCanvas.order_cursor
        if cur < MpCanvas.order_top:
            MpCanvas.order_top = cur
        elif cur >= MpCanvas.order_top + VISIBLE_ROWS:
            MpCanvas.order_top = cur - VISIBLE_ROWS + 1
        x, y0 = MpCanvas.center_x - 75, MpCanvas.center_y - 62
        for line in range(min(VISIBLE_ROWS, items - MpCanvas.order_top)):
            i = MpCanvas.order_top + line
            y = y0 + line * ROW_H
            on = i == cur
            if i == MpCanvas.order_count:      # the last item: Leave Order
                self.draw_box(MpCanvas.screen_g, x, y, 150, 14, 3 if on else 2)
                self.draw_text_colored(MpCanvas.screen_g, TEXTS[3], MpCanvas.center_x, y + 1, 1,
                                       0xFFFFFF if on else 0x646464)
                continue
            uid, name, level, online, leader = MpCanvas.order_rows[i]
            self.draw_box(MpCanvas.screen_g, x, y, 150, 14, 3 if on else 2)
            Draw.fill_rect(MpCanvas.screen_g, x + 6, y + 5, 4, 4, 0x41FF41 if online else 0x525152)
            color = 0x41FF41 if online else (0xFFFFFF if on else 0x646464)
            if uid == MpCanvas.user_id:
                color = 16400640               # me: orange, like the order's name
            self.draw_text_colored(MpCanvas.screen_g, name, x + 14, y + 1, 0, color)
            if leader:                         # the leader's emblem: the bright shield of the menu dots
                Draw.draw_image_part(MpCanvas.screen_g, MpCanvas.menu_icon_image, x + 66, y - 1, 12, 15, 0, 0)
            self.draw_text_colored(MpCanvas.screen_g, Consts.texts[27], x + 98, y + 1, 0, 0x646464)
            MpCanvas.draw_number(MpCanvas.screen_g, x + 150 - 7, y + 3, level, 0)
        if MpCanvas.order_top > 0 or MpCanvas.order_top + VISIBLE_ROWS < items:
            self.draw_text_colored(MpCanvas.screen_g, "%d/%d" % (cur + 1, items), MpCanvas.center_x,
                                   y0 + VISIBLE_ROWS * ROW_H + 2, 1, 0x646464)
        self.draw_softkeys(-1, 1)

    def _paint_order_menu(self):  # state 30 without an order
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = TEXTS[0]
            MpCanvas.menu_size = 2
            self.draw_menu_icons()
        self.draw_buffer()
        self.draw_button(MpCanvas.screen_g, TEXTS[1 + MpCanvas.cursor_stack[MpCanvas.stack_depth]],
                         MpCanvas.center_x - 45, MpCanvas.center_y - 19, 90, 17, False, True)
        MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
        self.draw_softkeys(-1, 1)

    def _paint_order_member(self):  # state 31
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = MpCanvas.order_rows[MpCanvas.order_cursor][1]
            MpCanvas.menu_size = 2
            self.draw_menu_icons()
        self.draw_buffer()
        self.draw_button(MpCanvas.screen_g, TEXTS[4 + MpCanvas.cursor_stack[MpCanvas.stack_depth]],
                         MpCanvas.center_x - 50, MpCanvas.center_y - 19, 100, 17, False, True)
        MpCanvas.draw_menu_cursor(MpCanvas.screen_g)
        self.draw_softkeys(-1, 1)

    def _paint_order_name(self):  # state 32, like the UserID input (21)
        lines = PROMPTS[0 if MpCanvas.order_creating else 1]
        prompt_y = MpCanvas.center_y - 48
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.letter_cursor = 0
            MpCanvas.input_text = ""
            MpCanvas.title = TEXTS[1 if MpCanvas.order_creating else 2]
            self.draw_window(MpCanvas.buffer_g)
            for i, text in enumerate(lines):
                self.draw_text_centred_on(MpCanvas.buffer_g, MpCanvas.center_x, prompt_y + 12 * i, text, 0xFFFFFF)
            self.draw_box(MpCanvas.buffer_g, MpCanvas.center_x - 40, prompt_y + 59, 80, 15, 6)
        self.draw_buffer()
        self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, prompt_y + 61, MpCanvas.input_text, 0x41FF41)
        MpCanvas.draw_letter_grid(MpCanvas.letter_cursor, prompt_y + 75)
        if imod(MpCanvas.state_ticks, 4) < 2:
            text_w = MpCanvas.font_white.string_width(MpCanvas.input_text)
            if len(MpCanvas.input_text) == 12:
                text_w = text_w - MpCanvas.font_white.string_width("A") * 2
            MpCanvas.draw_line_color(MpCanvas.screen_g, MpCanvas.center_x + idiv(text_w, 2), prompt_y + 71,
                                     MpCanvas.center_x + idiv(text_w, 2) + 4, prompt_y + 71, 0xFFFFFF)
        self.draw_softkeys(4, 1 if len(MpCanvas.input_text) == 0 else 3)

    def _paint_order_leave(self):  # state 33, like the exit dialog, over the window
        self._paint_order()
        g = MpCanvas.screen_g
        self.draw_box(g, MpCanvas.center_x - 53, MpCanvas.center_y - 34, 106, 68, 5)
        self.draw_text_centred_on(g, MpCanvas.center_x, MpCanvas.center_y - 22, TEXTS[6], 0xFFFFFF)
        self.draw_text_centred_on(g, MpCanvas.center_x, MpCanvas.center_y - 7, MpCanvas.order_name, 16400640)
        cur = MpCanvas.cursor_stack[MpCanvas.stack_depth]
        for i in range(2):
            self.draw_box(g, MpCanvas.center_x - 42 + i * 55, MpCanvas.center_y + 15, 29, 14, 3 if cur == i else 2)
            self.draw_text_colored(g, Consts.texts[40 + i], MpCanvas.center_x - 27 + i * 55, MpCanvas.center_y + 17, 1,
                                   0xFFFFFF if cur == i else 0x646464)

    # --- keys ----------------------------------------------------------------------
    def _keys_order(self, key):  # state 30
        if MpCanvas.key_in == -7:
            self.pop_state()
            return
        if not MpCanvas.order_name:
            self.menu_keys(MpCanvas.key_in)
            return
        if MpCanvas.state_ticks < 2:
            return
        items = MpCanvas.order_count + 1
        if MpCanvas.key_in == -1:
            MpCanvas.order_cursor = (MpCanvas.order_cursor - 1) % items
        elif MpCanvas.key_in == -2:
            MpCanvas.order_cursor = (MpCanvas.order_cursor + 1) % items
        elif MpCanvas.key_in == -5:
            self.menu_select()

    def _keys_order_name(self, key):  # state 32, like 21
        if MpCanvas.key_in in (-5, -6):
            if MpCanvas.letter_cursor < 26:
                if len(MpCanvas.input_text) < 12:
                    MpCanvas.input_text = MpCanvas.input_text + chr(65 + MpCanvas.letter_cursor)
                return
            if MpCanvas.letter_cursor != 26 or len(MpCanvas.input_text) < 4:
                return
            MpCanvas.loading_msg = 5
            MpCanvas.set_state(3)
            self.send_request(1794 if MpCanvas.order_creating else 1796)
            return
        if key == -7:
            if len(MpCanvas.input_text) == 0:
                self.pop_state()
                return
            MpCanvas.input_text = MpCanvas.input_text[:-1]
            return
        MpCanvas.letter_grid_keys(key)

    def _keys_order_leave(self, key):  # state 33
        self.yes_no_keys(MpCanvas.key_in)

    def invite_member(self, mode):
        """768 to the member under the cursor. From the window the battle goes back to it; from
        the Duel / Mission menu item it goes back to that menu, like the jar's own modes."""
        MpCanvas.room_mode = mode
        MpCanvas.input_text = MpCanvas.order_rows[MpCanvas.order_cursor][0]
        MpCanvas.order_invite = not MpCanvas.order_pick
        MpCanvas.loading_msg = 4
        MpCanvas.set_state(3)
        self.send_request(768)

    def order_select(self):
        """FIRE on the window's states (from menu_select)."""
        cur = MpCanvas.cursor_stack[MpCanvas.stack_depth]
        if MpCanvas.state == ORDER and not MpCanvas.order_name:
            MpCanvas.order_creating = cur == 0
            self.push_state(NAME_INPUT)
        elif MpCanvas.state == ORDER:
            if MpCanvas.order_cursor == MpCanvas.order_count:
                self.push_state(LEAVE)
            elif MpCanvas.order_rows[MpCanvas.order_cursor][0] == MpCanvas.user_id:
                pass                           # not myself
            elif MpCanvas.order_pick:
                self.invite_member(MpCanvas.order_pick)
            else:
                self.push_state(MEMBER)
        elif MpCanvas.state == MEMBER:
            self.invite_member(2 if cur == 0 else 3)
        elif MpCanvas.state == LEAVE:
            if cur == 0:
                MpCanvas.loading_msg = 5
                MpCanvas.set_state(3)
                self.send_request(1798)
            else:
                self.pop_state()

    PAINT = {ORDER: _paint_order, MEMBER: _paint_order_member, NAME_INPUT: _paint_order_name,
             LEAVE: _paint_order_leave}
    KEYS = {ORDER: _keys_order, NAME_INPUT: _keys_order_name, LEAVE: _keys_order_leave}   # 31: menu keys
    ANSWERS = {1793: on_order_info, 1795: on_order_changed, 1797: on_order_changed,
               1799: on_order_changed}
