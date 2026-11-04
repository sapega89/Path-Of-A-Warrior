"""PORT-EXTRA (asked by Andrey): the Chat window of the online game.

Not in the original jar. An eighth picture of the main menu carousel opens it. Three tabs
(pow_server/chat.py): Lobby (everyone online), Order (my order) and Private (a list of my
conversations; "New Message" asks for a UserID). Messages are up to 40 printable ASCII
characters: the jar's bitmap font has no other glyphs.

Text is typed on a keyboard grid (A-Z, a-z, digits and signs, Space, Send) with the arrows
and FIRE, like the jar's A-Z grid for the UserID, so it works on phone keys and on a gamepad;
a PC or browser keyboard types straight into it (Canvas.text_input). The server pushes new
messages (1812) to whoever reads the conversation; the others count them as unread: a badge
on the main menu (order and private messages) and a number on each tab.

States (unused numbers of the jar's menu range, so the menu music plays on):
    40  the tabs: Lobby / Order messages, the Private list
    41  a private conversation
    42  the keyboard: a message, or the UserID of a new private conversation
"""
from pow_mp.rt import imod

MpCanvas = None   # set by pow_mp/mp_canvas.py
Consts = Draw = NetThread = None   # set by mp_canvas._late_imports

CHAT = 40
TALK = 41
WRITE = 42
MAIN_MENU_ITEM = 7          # the main menu carousel: 0 Duel .. 6 Order, 7 Chat
LOBBY, ORDER, PRIVATE = 0, 1, 2
MAX_TEXT = 40
MAX_ID = 12
LINE_H = 12
ROW_H = 17
ORANGE, WHITE, GRAY, GREEN = 16400640, 0xFFFFFF, 0x646464, 0x41FF41

TEXTS = ["Chat", "Lobby", "Order", "Private", "New Message", "FIRE: write a message",
         "You are not in an order.", "No messages yet.", "No conversations yet.",
         "Enter the UserID", "of the player.", "(4-12 letters)", "Space", "Send", "more"]
# the keyboard: 6 rows of 14 cells; (label, character or None for Space / Send, cells wide)
KEY_ROWS = [
    [(c, c, 1) for c in "ABCDEFGHIJKLMN"],
    [(c, c, 1) for c in "OPQRSTUVWXYZ.,"],
    [(c, c, 1) for c in "abcdefghijklmn"],
    [(c, c, 1) for c in "opqrstuvwxyz!?"],
    [(c, c, 1) for c in "0123456789'-:)"],
    [*[(c, c, 1) for c in "(/+=*#@&%;"], ("Space", " ", 2), ("Send", None, 2)],
]
KEY_W, KEY_H = 15, 13
# error_msg numbers of the chat (Consts.error_lines / error_line_counts are extended by install())
ERRORS = (["Not so fast!", "Wait a moment."], ["No such player."], ["You cannot write", "to yourself."],
          ["The message is", "not acceptable."])
STATUS_ERRORS = {-24: 0, -26: 1, -27: 2, -49: 3}   # server status -> ERRORS index
_err_first = None


def install():
    """Adds the error texts to the jar's tables (once per run, after the Order window's)."""
    global _err_first
    from pow_mp import mp_canvas_order
    mp_canvas_order.install()
    if _err_first is None or len(Consts.error_line_counts) <= _err_first:
        _err_first = len(Consts.error_line_counts)
        for lines in ERRORS:
            Consts.error_lines.extend(lines)
            Consts.error_line_counts.append(len(lines))


def printable(ch):
    """A character the font can draw and the server accepts (no backslash)."""
    return len(ch) == 1 and 32 <= ord(ch) <= 126 and ch != "\\"


def wrap(font, name, text, width):
    """Lines of one message, [[(text, colour), ...], ...], at most `width` pixels each:
    "name:" (colour None, set by the caller) and the words; a word longer than a line is cut."""
    tokens = [(name + ":", None)] + [(w, WHITE) for w in text.split(" ") if w]
    lines, line, w = [], [], 0
    for token, colour in tokens:
        word = token
        while word:
            piece = (" " if line else "") + word
            pw = font.string_width(piece)
            if w + pw <= width:
                line.append((piece, colour))
                w += pw
                break
            if line:
                lines.append(line)
                line, w = [], 0
                continue
            n = len(word)
            while n > 1 and font.string_width(word[:n]) > width:
                n -= 1
            lines.append([(word[:n], colour)])
            word = word[n:]
    if line:
        lines.append(line)
    return lines


class ChatMixin:
    chat_tab = LOBBY
    chat_rows = {}              # (channel, peer) -> [(UserID, name, text)], oldest first
    chat_loaded = set()         # conversations read from the server since the login
    chat_peer = ""              # the private conversation (41) / its UserID
    chat_peer_name = ""
    chat_peers = []             # [[UserID, name, unread, online]] newest first
    chat_unread = [0, 0, 0]     # lobby, order, private
    chat_no_order = False
    chat_scroll = 0             # lines scrolled up from the newest
    chat_cursor = 0             # Private list: 0 New Message, then the peers
    chat_text = ""
    chat_key = (0, 0)           # keyboard cursor: row, cell
    chat_to = False             # 42 types a UserID (New Message), not a message
    chat_opening = False        # 1809 / 1814 pushes the window (from the main menu)
    chat_open_talk = False      # 1809 opens the private conversation (from New Message / the list)
    chat_seen_live = False      # a push arrived while reading: read again when leaving
    chat_req = (0, "")          # (channel, peer) of the next 1808 / 1810
    chat_out = ""               # the text of the next 1810

    # --- the conversation on screen ---------------------------------------------------
    def chat_key_now(self):
        """(channel, peer) shown now, or None outside the window."""
        top = MpCanvas.state_stack[MpCanvas.stack_depth]
        if MpCanvas.state not in (CHAT, TALK, WRITE) or top not in (CHAT, TALK, WRITE):
            return None
        under = top if top != WRITE else MpCanvas.state_stack[MpCanvas.stack_depth - 1]
        if under == TALK:
            return (PRIVATE, MpCanvas.chat_peer)
        if MpCanvas.chat_tab == PRIVATE:
            return None
        return (MpCanvas.chat_tab, "")

    # --- requests ------------------------------------------------------------------
    def open_chat(self):
        """From the main menu: the tab with unread messages (order, then private), else Lobby."""
        install()
        MpCanvas.chat_tab = ORDER if MpCanvas.chat_unread[ORDER] else (
            PRIVATE if MpCanvas.chat_unread[PRIVATE] else LOBBY)
        MpCanvas.chat_opening = True
        MpCanvas.loading_msg = 1
        MpCanvas.set_state(3)
        self.chat_request_tab()

    def chat_request_tab(self):
        MpCanvas.chat_scroll = 0
        if MpCanvas.chat_tab == PRIVATE:
            self.send_request(1813)
        else:
            self.chat_read(MpCanvas.chat_tab, "")

    def chat_read(self, channel, peer):
        MpCanvas.chat_req = (channel, peer)
        self.send_request(1808)

    def chat_send(self):
        channel, peer = (PRIVATE, MpCanvas.chat_peer) if self.chat_key_now() == (PRIVATE, MpCanvas.chat_peer) \
            else (MpCanvas.chat_tab, "")
        MpCanvas.chat_req = (channel, peer)
        MpCanvas.chat_out = MpCanvas.chat_text
        self.send_request(1810)

    def chat_write_request(self):
        """The body of 1808 / 1810 (send_request)."""
        channel, peer = MpCanvas.chat_req
        NetThread.write_byte(channel)
        NetThread.write_string(peer, 12)
        if MpCanvas.request_opcode == 1810:
            NetThread.write_string(MpCanvas.chat_out, MAX_TEXT)

    def chat_leave_conversation(self):
        """Leaving a conversation where pushes arrived: the server marks them read too."""
        key = self.chat_key_now()
        if MpCanvas.chat_seen_live and key is not None and key[0] != LOBBY:
            MpCanvas.chat_seen_live = False
            self.chat_read(*key)

    # --- answers -------------------------------------------------------------------
    def on_chat_read(self, answer):  # 1809
        st = MpCanvas.answer_status
        if st == -25:                           # the Order tab without an order
            MpCanvas.chat_no_order = True
            MpCanvas.chat_unread[ORDER] = 0
            return self._chat_show(False)
        if st != 1:
            return self._chat_error(st)
        channel = answer.read_s8()
        peer = answer.read_string(12)
        peer_name = answer.read_string(8)
        n = answer.read_s8() & 0xFF
        rows = [(answer.read_string(12), answer.read_string(8), answer.read_string(MAX_TEXT)) for _ in range(n)]
        MpCanvas.chat_rows[(channel, peer)] = rows
        MpCanvas.chat_loaded.add((channel, peer))
        if channel == ORDER:
            MpCanvas.chat_no_order = False
            MpCanvas.chat_unread[ORDER] = 0
        elif channel == LOBBY:
            MpCanvas.chat_unread[LOBBY] = 0
        else:
            for p in MpCanvas.chat_peers:
                if p[0] == peer:
                    MpCanvas.chat_unread[PRIVATE] = max(0, MpCanvas.chat_unread[PRIVATE] - p[2])
                    p[2] = 0
            if MpCanvas.chat_open_talk:
                MpCanvas.chat_open_talk = False
                MpCanvas.chat_peer, MpCanvas.chat_peer_name = peer, peer_name or peer[:8]
                MpCanvas.chat_scroll = 0
                while MpCanvas.stack_depth > 0 and MpCanvas.state_stack[MpCanvas.stack_depth] != CHAT:
                    MpCanvas.stack_depth -= 1  # back to the tabs, then the conversation over them
                self.push_state(TALK)
                return None
        return self._chat_show(False)

    def on_chat_peers(self, answer):  # 1814
        if MpCanvas.answer_status != 1:
            return self._chat_error(MpCanvas.answer_status)
        n = answer.read_s8() & 0xFF
        peers = [[answer.read_string(12), answer.read_string(8), answer.read_s8() & 0xFF, answer.read_s8() != 0]
                 for _ in range(n)]
        MpCanvas.chat_peers = peers
        MpCanvas.chat_unread[PRIVATE] = sum(p[2] for p in peers)
        MpCanvas.chat_cursor = min(MpCanvas.chat_cursor, len(peers))
        return self._chat_show(True)

    def _chat_show(self, peers):
        if MpCanvas.chat_opening:
            MpCanvas.chat_opening = False
            MpCanvas.chat_cursor = 0
            self.push_state(CHAT)
        elif MpCanvas.state in (CHAT, TALK, WRITE):
            MpCanvas.state_ticks = min(MpCanvas.state_ticks, 1)   # redraw the background

    def _chat_error(self, st):
        install()
        MpCanvas.chat_opening = MpCanvas.chat_open_talk = False
        MpCanvas.error_msg = _err_first + STATUS_ERRORS[st] if st in STATUS_ERRORS else 0
        self.push_state(4)

    def on_chat_sent(self, answer):  # 1811 (the message itself comes back as 1812)
        if MpCanvas.answer_status != 1:
            self._chat_error(MpCanvas.answer_status)

    def on_chat_push(self, answer):  # 1812, any time: never changes the screen
        channel = answer.read_s8()
        peer = answer.read_string(12)
        row = (answer.read_string(12), answer.read_string(8), answer.read_string(MAX_TEXT))
        key = (channel, peer)
        if key in MpCanvas.chat_loaded:
            rows = MpCanvas.chat_rows.setdefault(key, [])
            rows.append(row)
            del rows[:-30]
        mine = row[0] == MpCanvas.user_id
        if channel == PRIVATE:
            old = next((p for p in MpCanvas.chat_peers if p[0] == peer), None)
            entry = old or [peer, row[1] if not mine else peer[:8], 0, True]
            MpCanvas.chat_peers = [entry] + [p for p in MpCanvas.chat_peers if p is not entry]
        if self.chat_key_now() == key:
            MpCanvas.chat_scroll = 0
            if not mine:
                MpCanvas.chat_seen_live = True
            return
        if mine:
            return
        MpCanvas.chat_unread[channel] = min(99, MpCanvas.chat_unread[channel] + 1)
        if channel == PRIVATE:
            MpCanvas.chat_peers[0][2] = min(99, MpCanvas.chat_peers[0][2] + 1)

    def on_chat_unread(self, answer):  # 1815, pushed after the login
        MpCanvas.chat_unread[ORDER] = answer.read_s8() & 0xFF
        MpCanvas.chat_unread[PRIVATE] = answer.read_s8() & 0xFF

    def on_chat_answer(self, answer):
        """PORT-EXTRA pushes 1812 / 1815 come between the jar's own answers: they must not
        touch its state (answer_status, the wait timer, a pause)."""
        op = answer.read_s16()
        answer.read_s8()
        if op == 1812:
            self.on_chat_push(answer)
        else:
            self.on_chat_unread(answer)

    # --- painting ------------------------------------------------------------------
    def draw_chat_badge(self):
        """The main menu: unread order and private messages, at the picture's corner."""
        n = MpCanvas.chat_unread[ORDER] + MpCanvas.chat_unread[PRIVATE]
        if n <= 0:
            return
        text = str(min(n, 99))
        w = MpCanvas.font_white.string_width(text) + 6
        x, y = MpCanvas.center_x + 40 - w + 3, MpCanvas.center_y - 62
        Draw.fill_rect(MpCanvas.screen_g, x, y, w, 13, 0xC00000)
        Draw.draw_rect(MpCanvas.screen_g, x, y, w - 1, 12, 0xFFFFFF)
        self.draw_text_colored(MpCanvas.screen_g, text, x + 3, y + 1, 0, WHITE)

    def _chat_lines(self, key, width):
        rows = MpCanvas.chat_rows.get(key, [])
        lines = []
        for uid, name, text in rows:
            colour = ORANGE if uid == MpCanvas.user_id else GREEN
            lines.extend([(t, colour if c is None else c) for t, c in line]
                         for line in wrap(MpCanvas.font_white, name or uid[:8], text, width))
        return lines

    def _draw_messages(self, key, top, bottom):
        x, width = 9, MpCanvas.canvas_w - 18
        g = MpCanvas.screen_g
        if key is None:
            return
        if key == (ORDER, "") and MpCanvas.chat_no_order:
            self.draw_text_centred_on(g, MpCanvas.center_x, top + 30, TEXTS[6], GRAY)
            return
        lines = self._chat_lines(key, width)
        if not lines:
            self.draw_text_centred_on(g, MpCanvas.center_x, top + 30, TEXTS[7], GRAY)
            return
        fit = (bottom - top) // LINE_H
        MpCanvas.chat_scroll = max(0, min(MpCanvas.chat_scroll, len(lines) - fit))
        end = len(lines) - MpCanvas.chat_scroll
        shown = lines[max(0, end - fit):end]
        y = bottom - len(shown) * LINE_H
        for line in shown:
            lx = x
            for text, colour in line:
                if text:
                    self.draw_text_colored(g, text, lx, y, 0, colour)
                    lx += MpCanvas.font_white.string_width(text)
            y += LINE_H
        if end - fit > 0:                       # older lines above
            self.draw_text_colored(g, TEXTS[14], MpCanvas.canvas_w - 9, top - 2, 8, GRAY)

    def _draw_tabs(self):
        g = MpCanvas.screen_g
        w = (MpCanvas.canvas_w - 24) // 3
        for i in range(3):
            x = 9 + i * (w + 3)
            on = i == MpCanvas.chat_tab
            self.draw_box(g, x, 20, w, 14, 3 if on else 2)
            label = TEXTS[1 + i]
            n = MpCanvas.chat_unread[i]
            if n:
                label = "%s %d" % (label, min(n, 99))
            self.draw_text_colored(g, label, x + w // 2, 21, 1, GREEN if n and not on else (WHITE if on else GRAY))

    def _draw_input_hint(self):
        y = MpCanvas.canvas_h - 34
        self.draw_box(MpCanvas.screen_g, 9, y, MpCanvas.canvas_w - 18, 14, 2)
        self.draw_text_colored(MpCanvas.screen_g, TEXTS[5], MpCanvas.center_x, y + 1, 1, GRAY)

    def _draw_peers(self, top):
        g = MpCanvas.screen_g
        x, w = 9, MpCanvas.canvas_w - 18
        visible = (MpCanvas.canvas_h - 34 - top) // ROW_H
        items = 1 + len(MpCanvas.chat_peers)
        first = max(0, min(MpCanvas.chat_cursor - visible + 1, items - visible))
        for line in range(min(visible, items - first)):
            i = first + line
            y = top + line * ROW_H
            on = i == MpCanvas.chat_cursor
            self.draw_box(g, x, y, w, 14, 3 if on else 2)
            if i == 0:
                self.draw_text_colored(g, TEXTS[4], MpCanvas.center_x, y + 1, 1, WHITE if on else GRAY)
                continue
            uid, name, unread, online = MpCanvas.chat_peers[i - 1]
            Draw.fill_rect(g, x + 6, y + 5, 4, 4, GREEN if online else 0x525152)
            self.draw_text_colored(g, name or uid[:8], x + 14, y + 1, 0, WHITE if on else GRAY)
            if unread:
                self.draw_text_colored(g, str(unread), x + w - 6, y + 1, 8, GREEN)
        if len(MpCanvas.chat_peers) == 0:
            self.draw_text_centred_on(g, MpCanvas.center_x, top + ROW_H + 14, TEXTS[8], GRAY)

    def _paint_chat(self):  # state 40
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = TEXTS[0]
            self.draw_window_bg(MpCanvas.buffer_g)
        self.draw_buffer()
        self._draw_tabs()
        if MpCanvas.chat_tab == PRIVATE:
            self._draw_peers(40)
        else:
            self._draw_messages((MpCanvas.chat_tab, ""), 40, MpCanvas.canvas_h - 38)
            if not (MpCanvas.chat_tab == ORDER and MpCanvas.chat_no_order):
                self._draw_input_hint()
        self.draw_softkeys(-1, 1)

    def _paint_talk(self):  # state 41
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = MpCanvas.chat_peer_name
            self.draw_window_bg(MpCanvas.buffer_g)
        self.draw_buffer()
        self._draw_messages((PRIVATE, MpCanvas.chat_peer), 22, MpCanvas.canvas_h - 38)
        self._draw_input_hint()
        self.draw_softkeys(-1, 1)

    def _paint_write(self):  # state 42
        under = MpCanvas.state_stack[MpCanvas.stack_depth - 1]
        if MpCanvas.state_ticks < 2:
            MpCanvas.state_ticks = 2
            MpCanvas.title = TEXTS[4] if MpCanvas.chat_to else (
                MpCanvas.chat_peer_name if under == TALK else TEXTS[0])
            self.draw_window_bg(MpCanvas.buffer_g)
        self.draw_buffer()
        g = MpCanvas.screen_g
        ky = MpCanvas.canvas_h - 16 - 6 * KEY_H
        box_y = ky - 19
        if MpCanvas.chat_to:
            for i in range(3):
                self.draw_text_centred_on(g, MpCanvas.center_x, 60 + 14 * i, TEXTS[9 + i], WHITE)
        else:
            top = 22
            if under == CHAT:
                self._draw_tabs()
                top = 40
            key = (PRIVATE, MpCanvas.chat_peer) if under == TALK else (MpCanvas.chat_tab, "")
            self._draw_messages(key, top, box_y - 3)
        # the text box: the end of the text fits, the cursor blinks after it
        width = MpCanvas.canvas_w - 18
        self.draw_box(g, 9, box_y, width, 15, 6)
        text = MpCanvas.chat_text
        limit = MAX_ID if MpCanvas.chat_to else MAX_TEXT
        count = "%d/%d" % (len(MpCanvas.chat_text), limit)
        while MpCanvas.font_white.string_width(text) > width - 16 - MpCanvas.font_white.string_width(count):
            text = text[1:]
        self.draw_text_colored(g, text, 13, box_y + 2, 0, GREEN)
        if imod(MpCanvas.state_ticks, 4) < 2:
            cx = 13 + MpCanvas.font_white.string_width(text)
            MpCanvas.draw_line_color(g, cx, box_y + 11, cx + 4, box_y + 11, 0xFFFFFF)
        self.draw_text_colored(g, count, MpCanvas.canvas_w - 13, box_y + 2, 8, GRAY)
        self._draw_keyboard(ky)
        self.draw_softkeys(0, 1 if len(MpCanvas.chat_text) == 0 else 3)

    def _draw_keyboard(self, ky):
        g = MpCanvas.screen_g
        left = MpCanvas.center_x - 7 * KEY_W
        Draw.fill_rect(g, left - 2, ky - 1, 14 * KEY_W + 4, 6 * KEY_H + 2, 0)
        blink = imod(MpCanvas.state_ticks, 4) < 2
        for r, row in enumerate(KEY_ROWS):
            col = 0
            for c, (label, ch, span) in enumerate(row):
                x, y, w = left + col * KEY_W, ky + r * KEY_H, span * KEY_W
                usable = self._chat_key_ok(ch)
                if (r, c) == MpCanvas.chat_key and blink:
                    Draw.fill_rect(g, x + 1, y, w - 2, KEY_H - 1, 0xFF0000)
                elif span > 1:
                    Draw.fill_rect(g, x + 1, y, w - 2, KEY_H - 1, 255 if ch is None else 0x525152)
                self.draw_text_colored(g, label, x + w // 2, y + 1, 1, WHITE if usable else GRAY)
                col += span

    @staticmethod
    def _chat_key_ok(ch):
        """A key usable now: the UserID takes A-Z only."""
        if not MpCanvas.chat_to or ch is None:
            return True
        return "A" <= ch <= "Z"

    # --- keys ----------------------------------------------------------------------
    def _keys_chat(self, key):  # state 40
        k = MpCanvas.key_in
        if k == -7:
            self.chat_leave_conversation()
            self.pop_state()
            return
        if MpCanvas.state_ticks < 2:
            return
        if k in (-3, -4):
            self.chat_leave_conversation()
            MpCanvas.chat_tab = (MpCanvas.chat_tab + (1 if k == -4 else 2)) % 3
            MpCanvas.chat_cursor = 0
            MpCanvas.state_ticks = 1
            self.chat_request_tab()
            return
        if MpCanvas.chat_tab == PRIVATE:
            items = 1 + len(MpCanvas.chat_peers)
            if k == -1:
                MpCanvas.chat_cursor = (MpCanvas.chat_cursor - 1) % items
            elif k == -2:
                MpCanvas.chat_cursor = (MpCanvas.chat_cursor + 1) % items
            elif k in (-5, -6):
                if MpCanvas.chat_cursor == 0:
                    self._chat_start_write(True)
                else:
                    peer = MpCanvas.chat_peers[MpCanvas.chat_cursor - 1]
                    MpCanvas.chat_open_talk = True
                    MpCanvas.chat_peer_name = peer[1]
                    self.chat_read(PRIVATE, peer[0])
            return
        if k == -1:
            MpCanvas.chat_scroll += 1
        elif k == -2:
            MpCanvas.chat_scroll = max(0, MpCanvas.chat_scroll - 1)
        elif k in (-5, -6) and not (MpCanvas.chat_tab == ORDER and MpCanvas.chat_no_order):
            self._chat_start_write(False)

    def _keys_talk(self, key):  # state 41
        k = MpCanvas.key_in
        if k == -7:
            self.chat_leave_conversation()
            self.pop_state()
            self.send_request(1813)            # the list again: unread numbers, the order
            return
        if k == -1:
            MpCanvas.chat_scroll += 1
        elif k == -2:
            MpCanvas.chat_scroll = max(0, MpCanvas.chat_scroll - 1)
        elif k in (-5, -6):
            self._chat_start_write(False)

    def _chat_start_write(self, to):
        MpCanvas.chat_to = to
        MpCanvas.chat_text = ""
        MpCanvas.chat_key = (0, 0)
        self.push_state(WRITE)

    def _chat_type(self, ch):
        limit = MAX_ID if MpCanvas.chat_to else MAX_TEXT
        if MpCanvas.chat_to:
            ch = ch.upper()
            if not ("A" <= ch <= "Z"):
                return
        if len(MpCanvas.chat_text) < limit and printable(ch):
            if ch == " " and (not MpCanvas.chat_text or MpCanvas.chat_text.endswith(" ")):
                return
            MpCanvas.chat_text += ch

    def _chat_submit(self):
        text = MpCanvas.chat_text.strip()
        if MpCanvas.chat_to:
            if len(text) < 4:
                return
            MpCanvas.chat_open_talk = True
            MpCanvas.chat_peer_name = text[:8]
            MpCanvas.chat_text = ""
            self.chat_read(PRIVATE, text)
            return
        if not text:
            return
        MpCanvas.chat_text = text
        self.chat_send()
        MpCanvas.chat_text = ""
        MpCanvas.chat_scroll = 0
        self.pop_state()

    def _keys_write(self, key):  # state 42
        k = MpCanvas.key_in
        if k == -7:
            if not MpCanvas.chat_text:
                self.pop_state()
            else:
                MpCanvas.chat_text = MpCanvas.chat_text[:-1]
            return
        if k == -6:
            self._chat_submit()
            return
        r, c = MpCanvas.chat_key
        if k == -5:
            ch = KEY_ROWS[r][c][1]
            if ch is None:
                self._chat_submit()
            elif self._chat_key_ok(ch):
                self._chat_type(ch)
            return
        if k in (-3, -4):
            c = (c + (1 if k == -4 else -1)) % len(KEY_ROWS[r])
        elif k in (-1, -2):
            col = self._key_col(r, c)
            r = (r + (1 if k == -2 else -1)) % len(KEY_ROWS)
            c = self._key_at(r, col)
        MpCanvas.chat_key = (r, c)

    @staticmethod
    def _key_col(r, c):
        return sum(span for _, _, span in KEY_ROWS[r][:c])

    @staticmethod
    def _key_at(r, col):
        x = 0
        for i, (_, _, span) in enumerate(KEY_ROWS[r]):
            if x <= col < x + span:
                return i
            x += span
        return len(KEY_ROWS[r]) - 1

    def chat_text_key(self, ch):
        """A PC / browser keyboard (pow/midp/canvas.py Canvas.text_input): True = used here."""
        if MpCanvas.state != WRITE or not ch:
            return False
        if ch == "\x08":                       # Backspace
            if MpCanvas.chat_text:
                MpCanvas.chat_text = MpCanvas.chat_text[:-1]
            return True
        if ch in ("\r", "\n"):                 # Enter sends
            self._chat_submit()
            return True
        if ch == "\x1b":                       # Esc closes the keyboard
            self.pop_state()
            return True
        if printable(ch):
            self._chat_type(ch)
            return True
        return False

    PAINT = {CHAT: _paint_chat, TALK: _paint_talk, WRITE: _paint_write}
    KEYS = {CHAT: _keys_chat, TALK: _keys_talk, WRITE: _keys_write}
    ANSWERS = {1809: on_chat_read, 1811: on_chat_sent, 1814: on_chat_peers}
