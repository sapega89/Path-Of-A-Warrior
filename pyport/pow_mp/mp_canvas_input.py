"""g.java, part of MpCanvas: key handling: menus, yes/no, popups, the letter grid for names and ids.

A mixin of MpCanvas (pow_mp/mp_canvas.py); the methods keep their `# g.java:FROM-TO`
comments. The module names below are set by mp_canvas.py: `MpCanvas` once the class exists,
the others by its _late_imports().
"""
from pow_mp.rt import (
    _inc,
    _js,
    _set,
    i8,
    idiv,
    imod,
    system,
)

MpCanvas = None   # set by pow_mp/mp_canvas.py
NetThread = Consts = Draw = Gfx = None   # set by mp_canvas._late_imports


class InputMixin:
    def menu_keys(self, key):  # g.java:2589
        if MpCanvas.state_ticks < 2:
            return
        if key in (-3, -1):
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] > 0:
                MpCanvas.cursor_stack[MpCanvas.stack_depth] -= 1
            else:
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = (MpCanvas.menu_size - 1)
        elif key in (-4, -2):
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] < (MpCanvas.menu_size - 1):
                MpCanvas.cursor_stack[MpCanvas.stack_depth] += 1
            else:
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = 0
        if key == (-5):
            self.menu_select()

    def yes_no_keys(self, key):  # g.java:2613
        if MpCanvas.state_ticks < 2:
            return
        if key in (-3, -1):
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] > 0:
                MpCanvas.cursor_stack[MpCanvas.stack_depth] -= 1
            else:
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = 1
        elif key in (-4, -2):
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] < 1:
                MpCanvas.cursor_stack[MpCanvas.stack_depth] += 1
            else:
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = 0
        if key == (-5):
            self.menu_select()
            return
        if key == (-7):
            if (MpCanvas.state == 160) and (MpCanvas.popup_style != 1):
                return
            MpCanvas.cursor_stack[MpCanvas.stack_depth] = 1
            self.menu_select()

    def keyPressed(self, key):  # g.java:2645
        if key in (-32, -33):
            return
        if key == -100:                     # PORT-EXTRA: Tab = auto-battle on / off
            MpCanvas.auto_battle = not MpCanvas.auto_battle
            if MpCanvas.auto_battle and MpCanvas.state == 94 and MpCanvas.choose_secs > 1:
                MpCanvas.choose_secs = 1            # this round too
            return
        MpCanvas.key = key
        if MpCanvas.paused:
            if MpCanvas.key == (-5):
                MpCanvas.request_pause(2)
            MpCanvas.key = (-999)

    def handle_key(self, key):  # g.java:2661
        MpCanvas.ping_misses = 0
        MpCanvas.key_in = key
        if MpCanvas.state == 161:
            if MpCanvas.key_in == (-7):
                self.pop_state()
                return
            if MpCanvas.key_in == (-7):
                self.pop_state()
                return
            self.menu_keys(MpCanvas.key_in)
        elif MpCanvas.state in (11, 12, 16, 87, 162, 163, 164):
            if MpCanvas.key_in == (-7):
                self.pop_state()
                return
            self.menu_keys(MpCanvas.key_in)
        elif MpCanvas.state in (170, 171):
            if MpCanvas.key_in not in (-7, -5):
                return
            self.pop_state()
        elif MpCanvas.state == 6:
            if MpCanvas.notices_left > 0:
                MpCanvas.notice_page = MpCanvas.notice_page + 1
                self.send_request(258)
                return
            if MpCanvas.notice_kind == 1:
                self.reset_state_stack(7)
                return
            if MpCanvas.notice_kind != 9:
                return
            MpCanvas.set_state(300)
        elif MpCanvas.state == 7:
            MpCanvas.menu_size = 2
            MpCanvas.relogin_to_menu = False
            self.reset_state_stack(10)
        elif MpCanvas.state == 10:
            if MpCanvas.popup_shown:
                if MpCanvas.key_in in (-3, -4):
                    MpCanvas.popup_cursor = imod(((MpCanvas.popup_cursor + 1)), 2)
                    return
                if MpCanvas.key_in != (-5):
                    return
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
        elif MpCanvas.state in (80, 81, 83):
            if MpCanvas.key_in not in (-5, -7):
                return
            self.pop_state()
        elif MpCanvas.state == 82:
            if MpCanvas.key_in == (-1):
                if MpCanvas.cursor_stack[MpCanvas.stack_depth] > 0:
                    MpCanvas.cursor_stack[MpCanvas.stack_depth] -= 1
                else:
                    MpCanvas.cursor_stack[MpCanvas.stack_depth] = 3
            elif MpCanvas.key_in == (-2):
                if MpCanvas.cursor_stack[MpCanvas.stack_depth] < 3:
                    MpCanvas.cursor_stack[MpCanvas.stack_depth] += 1
                else:
                    MpCanvas.cursor_stack[MpCanvas.stack_depth] = 0
            elif MpCanvas.key_in == (-3):
                while True:
                    if MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] > 3:
                        MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] = i8(MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] - 1)
                    else:
                        MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] = 13
                    MpCanvas.skill_taken = False
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 4:
                        if (MpCanvas.loop_i != MpCanvas.cursor_stack[MpCanvas.stack_depth]) and (MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] == MpCanvas.skill_order[MpCanvas.loop_i]):
                            MpCanvas.skill_taken = True
                            break
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    if not (MpCanvas.skill_taken):
                        break
            elif MpCanvas.key_in == (-4):
                while True:
                    if MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] < 13:
                        MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] = i8(MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] + 1)
                    else:
                        MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] = 3
                    MpCanvas.skill_taken = False
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 4:
                        if (MpCanvas.loop_i != MpCanvas.cursor_stack[MpCanvas.stack_depth]) and (MpCanvas.skill_order[MpCanvas.cursor_stack[MpCanvas.stack_depth]] == MpCanvas.skill_order[MpCanvas.loop_i]):
                            MpCanvas.skill_taken = True
                            break
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    if not (MpCanvas.skill_taken):
                        break
            if MpCanvas.key_in not in (-5, -7):
                return
            self.menu_select()
        elif MpCanvas.state == 84:
            if MpCanvas.key_in == (-7):
                if len(MpCanvas.input_text) == 0:
                    if MpCanvas.quote_step == 0:
                        self.pop_state()
                        return
                    MpCanvas.quote_step = MpCanvas.quote_step - 1
                    return
                MpCanvas.input_text = MpCanvas.input_text[0:(len(MpCanvas.input_text) - 1)]
                return
            if MpCanvas.key_in in (-5, -6):
                if len(MpCanvas.input_text) == 0:
                    if MpCanvas.letter_cursor >= 26:
                        return
                    MpCanvas.input_text = _js(MpCanvas.input_text, chr((((65 + MpCanvas.letter_cursor))) & 0xFFFF))
                    return
                if len(MpCanvas.input_text) > 20:
                    return
                if MpCanvas.letter_cursor < 26:
                    if len(MpCanvas.input_text) >= 20:
                        return
                    MpCanvas.input_text = _js(MpCanvas.input_text, chr((((97 + MpCanvas.letter_cursor))) & 0xFFFF))
                    return
                if MpCanvas.letter_cursor == 26:
                    if len(MpCanvas.input_text) >= 20:
                        return
                    MpCanvas.input_text = _js(MpCanvas.input_text, chr(32))
                    return
                if MpCanvas.letter_cursor != 27:
                    return
                MpCanvas.loading_msg = 5
                MpCanvas.input_text = MpCanvas.trim_right(MpCanvas.input_text)
                if MpCanvas.quote_step == 0:
                    self.send_request(1282)
                else:
                    self.send_request(1284)
                MpCanvas.set_state(3)
                return
            MpCanvas.letter_grid_space_keys(MpCanvas.key_in)
        elif MpCanvas.state == 85:
            if MpCanvas.key_in == (-7):
                if len(MpCanvas.input_text) == 0:
                    self.pop_state()
                    return
                MpCanvas.input_text = MpCanvas.input_text[0:(len(MpCanvas.input_text) - 1)]
                return
            if MpCanvas.key_in in (-5, -6):
                if len(MpCanvas.input_text) == 0:
                    if MpCanvas.letter_cursor >= 26:
                        return
                    MpCanvas.input_text = _js(MpCanvas.input_text, chr((((65 + MpCanvas.letter_cursor))) & 0xFFFF))
                    return
                if len(MpCanvas.input_text) > 8:
                    return
                if MpCanvas.letter_cursor < 26:
                    if len(MpCanvas.input_text) >= 8:
                        return
                    MpCanvas.input_text = _js(MpCanvas.input_text, chr((((97 + MpCanvas.letter_cursor))) & 0xFFFF))
                    return
                if MpCanvas.letter_cursor != 26:
                    return
                self.push_state(86)
                return
            MpCanvas.letter_grid_keys(MpCanvas.key_in)
        elif MpCanvas.state == 88:
            if MpCanvas.key_in == (-1):
                if MpCanvas.cursor_stack[MpCanvas.stack_depth] > 0:
                    MpCanvas.cursor_stack[MpCanvas.stack_depth] -= 1
                    return
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = 2
                return
            if MpCanvas.key_in == (-2):
                if MpCanvas.cursor_stack[MpCanvas.stack_depth] < 2:
                    MpCanvas.cursor_stack[MpCanvas.stack_depth] += 1
                    return
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = 0
                return
            if MpCanvas.key_in in (-3, -4):
                self.menu_select()
                return
            if MpCanvas.key_in == (-5):
                MpCanvas.key_in = (-4)
                self.menu_select()
                return
            if MpCanvas.key_in != (-7):
                return
            MpCanvas.save_options()
            if MpCanvas.invitation != MpCanvas.invitation_saved:
                MpCanvas.loading_msg = 1
                MpCanvas.set_state(3)
                self.send_request(290)
                return
            self.pop_state()
            self.start_sound(1)
        elif MpCanvas.state == 89:
            if MpCanvas.key_in == (-3):
                if MpCanvas.help_page > 0:
                    MpCanvas.help_page = MpCanvas.help_page - 1
                    return
                MpCanvas.help_page = (Consts.help_pages[MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]] - 1)
                return
            if MpCanvas.key_in in (-4, -5):
                if MpCanvas.help_page < (Consts.help_pages[MpCanvas.cursor_stack[(MpCanvas.stack_depth - 1)]] - 1):
                    MpCanvas.help_page = MpCanvas.help_page + 1
                    return
                MpCanvas.help_page = 0
                return
            if MpCanvas.key_in != (-7):
                return
            self.pop_state()
        elif MpCanvas.state == 20:
            if MpCanvas.key_in == (-7):
                self.pop_state()
                return
            self.menu_keys(MpCanvas.key_in)
        elif MpCanvas.state == 21:
            if MpCanvas.key_in in (-5, -6):
                if len(MpCanvas.input_text) > 12:
                    return
                if MpCanvas.letter_cursor < 26:
                    if len(MpCanvas.input_text) >= 12:
                        return
                    MpCanvas.input_text = _js(MpCanvas.input_text, chr((((65 + MpCanvas.letter_cursor))) & 0xFFFF))
                    return
                if (MpCanvas.letter_cursor != 26) or (len(MpCanvas.input_text) < 4):
                    return
                if MpCanvas.room_mode == 0:
                    MpCanvas.loading_msg = 2
                elif MpCanvas.room_mode in {1, 2}:
                    MpCanvas.loading_msg = 4
                MpCanvas.loading_msg = 0
                self.send_request(768)
                MpCanvas.set_state(3)
                return
            if key == (-7):
                if len(MpCanvas.input_text) == 0:
                    self.pop_state()
                    return
                MpCanvas.input_text = MpCanvas.input_text[0:(len(MpCanvas.input_text) - 1)]
                return
            MpCanvas.letter_grid_keys(key)
        elif MpCanvas.state == 94:
            if MpCanvas.exit_prompt:
                if MpCanvas.key_in in (-3, -4):
                    MpCanvas.exit_cursor = imod(((MpCanvas.exit_cursor + 1)), 2)
                    return
                if MpCanvas.key_in != (-5):
                    return
                if MpCanvas.exit_cursor == 0:
                    MpCanvas.relogin_to_menu = False
                    MpCanvas.disconnect()
                    MpCanvas.set_timer(-1)
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
                return
            MpCanvas.set_state(96)
        elif MpCanvas.state == 95:
            if MpCanvas.key_in == (-1):
                MpCanvas.skill_cursor = (_inc(MpCanvas, "skill_cursor", -1) if (MpCanvas.skill_cursor > 0) else (MpCanvas.skill_slot_count - 1))
            elif MpCanvas.key_in == (-2):
                MpCanvas.skill_cursor = (_inc(MpCanvas, "skill_cursor", 1) if (MpCanvas.skill_cursor < (MpCanvas.skill_slot_count - 1)) else 0)
            if MpCanvas.key_in == (-5):
                if MpCanvas.fighter_mp[0] < MpCanvas.skill_costs[(MpCanvas.skill_slots[MpCanvas.skill_cursor] - 3)]:
                    return
                MpCanvas.chosen_action = MpCanvas.skill_slots[MpCanvas.skill_cursor]
                MpCanvas.set_state(96)
                return
            if MpCanvas.key_in != (-7):
                return
            MpCanvas.chosen_action = 99
            MpCanvas.set_state(94)
        elif MpCanvas.state == 96:
            if MpCanvas.key_in in (-1, -2):
                if MpCanvas.chosen_action in (9, 10):
                    MpCanvas.loop_i = 0
                    while MpCanvas.loop_i < 4:
                        if (MpCanvas.fighter_present[MpCanvas.loop_i] and (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == imod(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2))) and (MpCanvas.fighter_slot[MpCanvas.loop_i] != MpCanvas.fighter_slot[MpCanvas.target_cursor]):
                            MpCanvas.target_cursor = MpCanvas.loop_i
                            return
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    return
                if MpCanvas.chosen_action in (0, 3, 4, 5, 6, 7):
                    MpCanvas.loop_i = 1
                    while MpCanvas.loop_i < 4:
                        if (MpCanvas.fighter_present[MpCanvas.loop_i] and (imod(MpCanvas.fighter_slot[MpCanvas.loop_i], 2) == imod(MpCanvas.fighter_slot[MpCanvas.target_cursor], 2))) and (MpCanvas.fighter_slot[MpCanvas.loop_i] != MpCanvas.fighter_slot[MpCanvas.target_cursor]):
                            MpCanvas.target_cursor = MpCanvas.loop_i
                            return
                        MpCanvas.loop_i = MpCanvas.loop_i + 1
                    return
                return
            if MpCanvas.key_in == (-5):
                self.start_timing()
                return
            if MpCanvas.key_in != (-7):
                return
            if MpCanvas.chosen_action in (3, 4, 5, 6, 7, 9, 10):
                MpCanvas.set_state(95)
                return
            MpCanvas.set_state(94)
        elif MpCanvas.state == 97:
            if (MpCanvas.state_ticks <= 0) or (MpCanvas.key_in != (-5)):
                return
            self.stop_timing()
        elif MpCanvas.state == 105:
            if (MpCanvas.state_ticks <= idiv(1000, MpCanvas.tick_ms)) or (MpCanvas.key_in != (-5)):
                return
            self.reset_state_stack(10)
            if MpCanvas.room_mode == 0:
                self.push_state(11)
            elif MpCanvas.room_mode == 1:
                self.push_state(11)
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = 1
            elif MpCanvas.room_mode == 2:
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = 1
                self.push_state(12)
        elif MpCanvas.state == 4:
            if MpCanvas.popup_shown:
                if MpCanvas.key_in in (-3, -4):
                    MpCanvas.popup_cursor = imod(((MpCanvas.popup_cursor + 1)), 2)
                    return
                if MpCanvas.key_in != (-5):
                    return
                if MpCanvas.popup_cursor == 0:
                    MpCanvas.set_state(300)
                    return
                MpCanvas.popup_shown = False
                MpCanvas.popup_cursor = 1
                return
            if MpCanvas.key_in == (-6):
                if MpCanvas.error_msg not in {7, 1}:
                    return
                MpCanvas.disconnect()
                MpCanvas.popup_kind = 0
                MpCanvas.relogin_to_menu = True
                MpCanvas.set_state(2)
                MpCanvas.popup_shown = False
                return
            if MpCanvas.key_in == (-7):
                if MpCanvas.error_msg not in {7, 1}:
                    return
                MpCanvas.popup_shown = True
                MpCanvas.popup_cursor = 1
                return
            if MpCanvas.key_in != (-5):
                return
            if not NetThread.connected:
                if (MpCanvas.error_msg in {14, 15}) or (MpCanvas.error_msg == 16):
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
            if MpCanvas.state_stack[(MpCanvas.stack_depth - 1)] == 105:
                return
            if MpCanvas.state_stack[(MpCanvas.stack_depth - 1)] == 86:
                self.pop_states(2)
                return
            self.pop_state()
        elif MpCanvas.state == 5:
            if MpCanvas.key_in in (-3, -4):
                MpCanvas.cursor_stack[MpCanvas.stack_depth] = imod(((MpCanvas.cursor_stack[MpCanvas.stack_depth] + 1)), 2)
                return
            if MpCanvas.key_in != (-5):
                return
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] == 0:
                if MpCanvas.volume == 0:
                    MpCanvas.volume = 4
            else:
                MpCanvas.volume = 0
            MpCanvas.save_options()
            MpCanvas.set_state(1)
            self.start_music(1)
        elif MpCanvas.state == 1:
            if MpCanvas.state_ticks <= 3:
                return
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
        elif MpCanvas.state == 2:
            self.popup_keys(MpCanvas.key_in)
        elif MpCanvas.state in (86, 160):
            self.yes_no_keys(MpCanvas.key_in)

    def menu_select(self):  # g.java:3512
        if MpCanvas.state == 160:
            if MpCanvas.popup_style == 1:
                if MpCanvas.cursor_stack[MpCanvas.stack_depth] == 0:
                    MpCanvas.loading_msg = 5
                    MpCanvas.set_state(3)
                    return
                self.on_disconnect()
                MpCanvas.set_state(1)
            elif MpCanvas.popup_style in (0, 2):
                self.on_disconnect()
                MpCanvas.set_state(1)
        elif MpCanvas.state == 161:
            MpCanvas.rank_kind = i8(MpCanvas.cursor_stack[MpCanvas.stack_depth])
            MpCanvas.loading_msg = 1
            MpCanvas.set_state(3)
            self.send_request(1300)
        elif MpCanvas.state in (162, 163, 164):
            MpCanvas.rank_list_state = MpCanvas.state
            MpCanvas.rank_list_kind = ((((((MpCanvas.state_stack[MpCanvas.stack_depth] - 162) + 1)) * 10) + MpCanvas.cursor_stack[MpCanvas.stack_depth]) + 1)
            MpCanvas.loading_msg = 1
            MpCanvas.set_state(3)
            self.send_request(1293)
        elif MpCanvas.state == 10:
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] == 0:
                self.push_state(11)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 1:
                self.push_state(12)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 2:
                self.push_state(16)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 3:
                MpCanvas.loading_msg = 1
                MpCanvas.set_state(3)
                self.send_request(288)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 4:
                self.push_state(87)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 5:
                self.push_state(161)
        elif MpCanvas.state == 11:
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] == 0:
                MpCanvas.room_mode = 0
                MpCanvas.loading_msg = 2
                MpCanvas.set_state(3)
                self.send_request(512)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 1:
                MpCanvas.room_mode = 1
                MpCanvas.loading_msg = 2
                MpCanvas.set_state(3)
                self.send_request(512)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 2:
                self.push_state(20)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 3:
                self.push_state(87)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 4:
                self.push_state(161)
        elif MpCanvas.state == 12:
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] == 0:
                MpCanvas.room_mode = i8(2)
                MpCanvas.loading_msg = 3
                MpCanvas.set_state(3)
                self.send_request(512)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 1:
                MpCanvas.room_mode = i8(2)
                self.push_state(21)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 2:
                self.push_state(87)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 3:
                self.push_state(161)
        elif MpCanvas.state == 16:
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] == 0:
                MpCanvas.loading_msg = 1
                MpCanvas.set_state(3)
                self.send_request(1296)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 1:
                MpCanvas.loading_msg = 1
                MpCanvas.set_state(3)
                self.send_request(1287)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 2:
                MpCanvas.loading_msg = 1
                MpCanvas.set_state(3)
                self.send_request(1289)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 3:
                MpCanvas.loading_msg = 1
                MpCanvas.set_state(3)
                self.send_request(1298)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 4:
                MpCanvas.letter_cursor = 0
                MpCanvas.quote_step = 0
                MpCanvas.input_text = MpCanvas.quote_start
                self.push_state(84)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 5:
                MpCanvas.letter_cursor = 0
                MpCanvas.input_text = MpCanvas.name
                self.push_state(85)
        elif MpCanvas.state == 82:
            MpCanvas.loading_msg = 5
            MpCanvas.set_state(3)
            self.send_request(1291)
        elif MpCanvas.state == 84:
            return
        elif MpCanvas.state == 86:
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] == 0:
                MpCanvas.loading_msg = 5
                MpCanvas.set_state(3)
                self.send_request(1280)
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 1:
                self.pop_states(1)
        elif MpCanvas.state == 88:
            while True:
                if MpCanvas.cursor_stack[MpCanvas.stack_depth] == 0:
                    if MpCanvas.key_in == (-4):
                        if _inc(MpCanvas, "speed", 1) <= 2:
                            break
                        MpCanvas.speed = 0
                        return
                    if (MpCanvas.key_in != (-3)) or (_inc(MpCanvas, "speed", -1) >= 0):
                        break
                    MpCanvas.speed = 2
                    return
                if MpCanvas.cursor_stack[MpCanvas.stack_depth] == 1:
                    if MpCanvas.key_in not in (-3, -4):
                        break
                    MpCanvas.invitation = imod(((MpCanvas.invitation + 1)), 2)
                    return
                if MpCanvas.cursor_stack[MpCanvas.stack_depth] == 2:
                    if MpCanvas.key_in == (-3):
                        self.volume_down()
                        return
                    if MpCanvas.key_in != (-4):
                        break
                    self.volume_up()
                break
        elif MpCanvas.state == 87:
            self.push_state(89)
        elif MpCanvas.state == 20:
            if MpCanvas.cursor_stack[MpCanvas.stack_depth] == 0:
                MpCanvas.room_mode = 0
            elif MpCanvas.cursor_stack[MpCanvas.stack_depth] == 1:
                MpCanvas.room_mode = 1
            self.push_state(21)

    def draw_popup(self):  # g.java:4833
        top = 0
        if MpCanvas.popup_kind == 0:
            if MpCanvas.popup_shown:
                self.draw_exit_confirm(MpCanvas.screen_g)
                return
            top = (MpCanvas.center_y - 57)
            i = 0
            while i < 7:
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (top + (12 * i)), Consts.login_texts[(1 + i)], 0xFFFFFF)
                i = i + 1
            Draw.fill_rect(MpCanvas.screen_g, (MpCanvas.center_x - 40), (top + 86), 80, 13, 0)
            Draw.draw_rect(MpCanvas.screen_g, (MpCanvas.center_x - 40), (top + 86), 80, 13, 0x646464)
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, ((top + 52) + 35), MpCanvas.input_text, 0x41FF41)
            MpCanvas.draw_letter_grid(MpCanvas.letter_cursor, ((top + 64) + 35))
            if imod(MpCanvas.state_ticks, 4) < 2:
                text_w = MpCanvas.font_white.string_width(MpCanvas.input_text)
                if len(MpCanvas.input_text) == 12:
                    text_w = (text_w - (MpCanvas.font_white.string_width("A") * 2))
                MpCanvas.draw_line_color(MpCanvas.screen_g, (MpCanvas.center_x + idiv(text_w, 2)), ((top + 62) + 35), ((MpCanvas.center_x + idiv(text_w, 2)) + 4), ((top + 62) + 35), 0xFFFFFF)
            if len(MpCanvas.input_text) == 0:
                self.draw_softkeys(4, 2)
                return
            self.draw_softkeys(4, 3)
        elif MpCanvas.popup_kind == 1:
            top = (MpCanvas.center_y - 45)
            j = 0
            while j < 5:
                self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (top + (12 * j)), Consts.login_texts[(8 + j)], 0xFFFFFF)
                j = j + 1
            Draw.fill_rect(MpCanvas.screen_g, (MpCanvas.center_x - 40), (top + 63), 80, 13, 0)
            Draw.draw_rect(MpCanvas.screen_g, (MpCanvas.center_x - 40), (top + 63), 80, 13, 0x646464)
            self.draw_text_centred_on(MpCanvas.screen_g, MpCanvas.center_x, (top + 64), MpCanvas.password, 0x41FF41)
            if len(MpCanvas.password) >= 4:
                self.draw_softkeys(0, 3)
                return
            if len(MpCanvas.password) > 0:
                self.draw_softkeys((-1), 3)
                return
            self.draw_softkeys((-1), 1)

    def popup_keys(self, key):  # g.java:4888
        if MpCanvas.popup_kind == 0:
            if MpCanvas.popup_shown:
                if MpCanvas.key_in in (-3, -4):
                    MpCanvas.popup_cursor = imod(((MpCanvas.popup_cursor + 1)), 2)
                    return
                if MpCanvas.key_in != (-5):
                    return
                if MpCanvas.popup_cursor == 0:
                    MpCanvas.set_state(300)
                    return
                MpCanvas.popup_shown = False
                return
            if key == (-7):
                if len(MpCanvas.input_text) == 0:
                    MpCanvas.popup_shown = True
                    return
                MpCanvas.input_text = MpCanvas.input_text[0:(len(MpCanvas.input_text) - 1)]
                return
            if MpCanvas.key_in in (-5, -6):
                if len(MpCanvas.input_text) > 12:
                    return
                if MpCanvas.letter_cursor < 26:
                    if len(MpCanvas.input_text) >= 12:
                        return
                    MpCanvas.input_text = _js(MpCanvas.input_text, chr((((65 + MpCanvas.letter_cursor))) & 0xFFFF))
                    return
                if (MpCanvas.letter_cursor != 26) or (len(MpCanvas.input_text) < 4):
                    return
                MpCanvas.user_id = MpCanvas.input_text
                MpCanvas.popup_kind = 1
                MpCanvas.password = ""
                return
            MpCanvas.letter_grid_keys(MpCanvas.key_in)
        elif MpCanvas.popup_kind == 1:
            size = len(MpCanvas.password)
            digit = (-1)
            if key == 48:
                digit = 0
            elif key == 49:
                digit = 1
            elif key == 50:
                digit = 2
            elif key == 51:
                digit = 3
            elif key == 52:
                digit = 4
            elif key == 53:
                digit = 5
            elif key == 54:
                digit = 6
            elif key == 55:
                digit = 7
            elif key == 56:
                digit = 8
            elif key == 57:
                digit = 9
            if key == (-7):
                if size > 0:
                    MpCanvas.password = MpCanvas.password[0:(size - 1)]
                    return
                MpCanvas.popup_kind = 0
                MpCanvas.letter_cursor = 0
                return
            if digit != (-1):
                if size >= 12:
                    return
                MpCanvas.password = _js(_js(MpCanvas.password, ""), digit)
                return
            if (key != (-6)) or (size < 4):
                return
            MpCanvas.loading_msg = 0
            MpCanvas.password_login = True
            MpCanvas.set_state(10000)

    @staticmethod
    def draw_letter_grid(cursor, y):  # g.java:6002
        left = (MpCanvas.center_x - 57)
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "OK"]
        Gfx.fill_rect(left, y, 115, 22, 0)
        Gfx.fill_rect((left + 99), (y + 12), 13, 9, 255)
        if imod(MpCanvas.state_ticks, 4) < 2:
            if cursor == 26:
                Gfx.fill_rect((left + 99), (y + 12), 13, 9, 0xFF0000)
            else:
                Gfx.fill_rect(((left + 2) + (imod(cursor, 14) * 8)), ((y + 1) + (11 * (idiv(cursor, 14)))), 7, 9, 0xFF0000)
        Gfx.set_font(MpCanvas.font_white)
        i = 0
        while i < len(letters):
            dx = (1 if (i == 8) else (1 if (i == 26) else 0))
            Gfx.draw_string(letters[i], (((left + 3) + (imod(i, 14) * 8)) + dx), (y + (11 * (idiv(i, 14)))), 0)
            i = i + 1

    @staticmethod
    def letter_grid_keys(key):  # g.java:6023
        result = key
        if (key not in (-7, -5)) and (key != (-6)):
            if key == (-1):
                MpCanvas.letter_cursor = imod((((MpCanvas.letter_cursor + 28) - 14)), 28)
            elif key == (-2):
                MpCanvas.letter_cursor = imod((((MpCanvas.letter_cursor + 28) + 14)), 28)
            elif key == (-3):
                MpCanvas.letter_cursor = imod((((MpCanvas.letter_cursor + 28) - 1)), 28)
            elif (key == (-4)) and ((_set(MpCanvas, "letter_cursor", imod((((MpCanvas.letter_cursor + 28) + 1)), 28))) == 27):
                MpCanvas.letter_cursor = 0
        if MpCanvas.letter_cursor == 27:
            MpCanvas.letter_cursor = 26
        return result

    @staticmethod
    def draw_letter_grid_space(cursor, y):  # g.java:6042
        left = (MpCanvas.center_x - 60)
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " ", "OK"]
        Gfx.fill_rect(left, y, 120, 22, 0)
        Gfx.fill_rect((left + 99), (y + 13), 5, 7, 0x666666)
        Gfx.fill_rect((left + 106), (y + 12), 13, 9, 255)
        if imod(MpCanvas.state_ticks, 4) < 2:
            if cursor == 27:
                Gfx.fill_rect((left + 106), (y + 12), 13, 9, 0xFF0000)
            else:
                Gfx.fill_rect(((left + 2) + (imod(cursor, 14) * 8)), ((y + 1) + (11 * (idiv(cursor, 14)))), 7, 9, 0xFF0000)
        Gfx.set_font(MpCanvas.font_white)
        i = 0
        while i < len(letters):
            dx = (1 if (i == 8) else (1 if (i == 26) else 0))
            Gfx.draw_string(letters[i], (((left + 3) + (imod(i, 14) * 8)) + dx), (y + (11 * (idiv(i, 14)))), 0)
            i = i + 1

    @staticmethod
    def letter_grid_space_keys(key):  # g.java:6064
        result = key
        if (key not in (-7, -5)) and (key != (-6)):
            if key == (-1):
                MpCanvas.letter_cursor = imod((((MpCanvas.letter_cursor + 28) - 14)), 28)
            elif key == (-2):
                MpCanvas.letter_cursor = imod((((MpCanvas.letter_cursor + 28) + 14)), 28)
            elif key == (-3):
                MpCanvas.letter_cursor = imod((((MpCanvas.letter_cursor + 28) - 1)), 28)
            elif key == (-4):
                MpCanvas.letter_cursor = imod((((MpCanvas.letter_cursor + 28) + 1)), 28)
        return result

    @staticmethod
    def trim_right(text):  # g.java:6080
        size = len(text)
        i = (size - 1)
        while i >= 0:
            if ord(text[i]) != 32:
                break
            i = i - 1
        if i == 0:
            return ""
        return text[0:(i + 1)]

    def draw_name_prompt(self, graphics):  # g.java:6093
        self.draw_window(graphics)
        self.draw_box(graphics, (MpCanvas.center_x - 62), (MpCanvas.center_y + 7), 126, 16, 6)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 32), Consts.input_prompts[0], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 20), Consts.input_prompts[1], 0xFFFFFF)
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y - 8), Consts.input_prompts[2], 0xFFFFFF)

    def draw_input_line(self, graphics):  # g.java:6101
        self.draw_text_centred_on(graphics, MpCanvas.center_x, (MpCanvas.center_y + 9), MpCanvas.input_text, 0x41FF41)
        if imod(MpCanvas.state_ticks, 4) < 2:
            text_w = MpCanvas.font_white.string_width(MpCanvas.input_text)
            if len(MpCanvas.input_text) == 8:
                text_w = (text_w - (MpCanvas.font_white.string_width("A") * 2))
            MpCanvas.draw_line_color(graphics, (MpCanvas.center_x + idiv(text_w, 2)), (MpCanvas.center_y + 20), ((MpCanvas.center_x + idiv(text_w, 2)) + 4), (MpCanvas.center_y + 20), 0xFFFFFF)
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

    def draw_user_id_prompt(self, graphics, y):  # g.java:6182
        self.draw_window(graphics)
        i = 0
        while i < 5:
            self.draw_text_centred_on(graphics, MpCanvas.center_x, (y + (12 * i)), Consts.input_prompts[(((6 if (MpCanvas.room_mode == 0) else 12)) + i)], 0xFFFFFF)
            i = i + 1
        self.draw_box(graphics, (MpCanvas.center_x - 40), (y + 59), 80, 15, 6)
