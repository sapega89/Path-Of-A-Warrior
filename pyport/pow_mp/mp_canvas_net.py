"""g.java, part of MpCanvas: the server connection: requests, answers, login, disconnects and errors.

A mixin of MpCanvas (pow_mp/mp_canvas.py); the methods keep their `# g.java:FROM-TO`
comments. The module names below are set by mp_canvas.py: `MpCanvas` once the class exists,
the others by its _late_imports().
"""
from pow_mp.rt import (
    i8,
    idiv,
    imod,
    system,
)

MpCanvas = None   # set by pow_mp/mp_canvas.py
NetThread = None   # set by mp_canvas._late_imports


class NetMixin:
    def send_request(self, opcode):  # g.java:1609
        if opcode in {262, 278}:
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
        MpCanvas.request_opcode = opcode
        MpCanvas.net.begin(MpCanvas.request_opcode)
        if MpCanvas.request_opcode == 1300:
            NetThread.write_byte(i8(MpCanvas.rank_kind + 1))
        elif MpCanvas.request_opcode == 1293:
            NetThread.write_byte(i8(MpCanvas.rank_list_kind))
            NetThread.write_int(1)
        elif MpCanvas.request_opcode in {256, 262}:
            NetThread.write_string(MpCanvas.user_id, 12)
            NetThread.write_string(MpCanvas.game_ver, 4)
        elif MpCanvas.request_opcode == 278:
            NetThread.write_string(MpCanvas.user_id, 12)
            NetThread.write_string(MpCanvas.password, 16)
            NetThread.write_string(MpCanvas.game_ver, 4)
        elif MpCanvas.request_opcode == 512:
            NetThread.write_byte(MpCanvas.room_mode)
        elif MpCanvas.request_opcode == 1291:
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
        elif MpCanvas.request_opcode == 1280:
            NetThread.write_string(MpCanvas.input_text, 8)
        elif MpCanvas.request_opcode == 258:
            NetThread.write_int(MpCanvas.notice_page)
        elif MpCanvas.request_opcode == 1027:
            NetThread.write_byte(i8(MpCanvas.fighter_slot[MpCanvas.target_cursor]))
            NetThread.write_byte(i8(MpCanvas.chosen_action))
            NetThread.write_byte(i8(MpCanvas.hit_score))
        elif MpCanvas.request_opcode in (1282, 1284):
            NetThread.write_string(MpCanvas.input_text, 20)
        elif MpCanvas.request_opcode == 768:
            NetThread.write_byte(MpCanvas.room_mode)
            NetThread.write_string(MpCanvas.input_text, 12)
        elif MpCanvas.request_opcode == 288:
            pass
        elif MpCanvas.request_opcode == 290:
            NetThread.write_int(MpCanvas.invitation)
        NetThread.send()

    def on_answer(self, answer):  # g.java:1888
        MpCanvas.wait_started = False
        if MpCanvas.paused or (MpCanvas.pause_request == 1):
            MpCanvas.error_msg = 7
            MpCanvas.popup_shown = False
            MpCanvas.disconnect()
            MpCanvas.set_timer(-1)
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
        s = answer.read_s16()
        status = answer.read_s8()
        MpCanvas.answer_status = status
        if s == 279:
            if MpCanvas.answer_status == 1:
                MpCanvas.save_options()
                self.on_disconnect()
                MpCanvas.loading_msg = 0
                MpCanvas.password_login = False
                MpCanvas.set_state(10000)
                return
            reason = answer.read_s8()
            self.on_disconnect()
            if reason == 0:
                MpCanvas.popup_kind = 0
                MpCanvas.error_msg = 14
            elif reason == 1:
                MpCanvas.popup_kind = 1
                MpCanvas.error_msg = 15
            else:
                MpCanvas.popup_kind = 0
                MpCanvas.error_msg = 0
            self.push_state(4)
        elif s == 263:
            if MpCanvas.answer_status == 1:
                MpCanvas.name = answer.read_string(8)
                MpCanvas.face = answer.read_s8()
                MpCanvas.level = answer.read_s16()
                MpCanvas.wins = answer.read_s32()
                MpCanvas.losses = answer.read_s32()
                MpCanvas.hp = answer.read_s16()
                answer.read_s16()
                answer.read_s16()
                MpCanvas.weapon = answer.read_s8()
                MpCanvas.skill_slots[0] = answer.read_s8()
                MpCanvas.skill_slots[1] = answer.read_s8()
                MpCanvas.skill_slots[2] = answer.read_s8()
                MpCanvas.skill_slots[3] = answer.read_s8()
                MpCanvas.skill_slot_count = 0
                MpCanvas.loop_i = 0
                while MpCanvas.loop_i < 4:
                    if MpCanvas.skill_slots[MpCanvas.loop_i] != 99:
                        MpCanvas.skill_slot_count = MpCanvas.skill_slot_count + 1
                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                MpCanvas.quote_start = MpCanvas.trim_right(answer.read_string(20))
                MpCanvas.quote_win = MpCanvas.trim_right(answer.read_string(20))
                MpCanvas.loop_i = 0
                while MpCanvas.loop_i < 11:
                    MpCanvas.skill_costs[MpCanvas.loop_i] = answer.read_s8()
                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                MpCanvas.profile_cr = answer.read_s8()
                MpCanvas.profile_unused1 = answer.read_s8()
                MpCanvas.profile_unused2 = answer.read_s8()
                MpCanvas.profile_unused1 = max(MpCanvas.profile_unused1, 0)
                MpCanvas.profile_unused2 = max(MpCanvas.profile_unused2, 0)
                MpCanvas.notices_left = answer.read_s8()
                answer.read_string(8)
                answer.read_string(8)
                answer.read_s8()
                answer.read_s8()
                answer.read_s8()
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
            if MpCanvas.answer_status == (-2):
                MpCanvas.error_msg = 1
                self.on_disconnect()
                return
            if MpCanvas.answer_status == (-9):
                MpCanvas.error_msg = 8
                self.on_disconnect()
                return
            MpCanvas.error_msg = 7
            MpCanvas.popup_shown = False
            MpCanvas.disconnect()
            self.push_state(4)
        elif s == 1286:
            if MpCanvas.room_mode in (0, 1):
                MpCanvas.set_state(11)
            elif MpCanvas.room_mode == 2:
                MpCanvas.set_state(12)
        elif s == 1301:
            if MpCanvas.answer_status == 1:
                MpCanvas.my_ranks[MpCanvas.rank_kind] = answer.read_s32()
                MpCanvas.my_rank_value = answer.read_s32()
                self.push_state((161 + MpCanvas.cursor_stack[MpCanvas.stack_depth]) + 1)
            elif MpCanvas.answer_status == (-1):
                MpCanvas.error_msg = 0
                self.push_state(4)
        elif s == 1294:
            if MpCanvas.answer_status == 1:
                count = answer.read_s8()
                i = 0
                while i < count:
                    MpCanvas.rank_ranks[i] = answer.read_s32()
                    MpCanvas.rank_names[i] = answer.read_string(12)
                    MpCanvas.rank_values[i] = answer.read_s32()
                    i = i + 1
                self.push_state(170 + MpCanvas.cursor_stack[MpCanvas.stack_depth])
            elif MpCanvas.answer_status == (-1):
                MpCanvas.error_msg = 0
                self.push_state(4)
        elif s == 259:
            if MpCanvas.answer_status == 1:
                i_line = 0
                while i_line < 4:
                    MpCanvas.notice_lines[i_line] = answer.read_string(16)
                    i_line = i_line + 1
                MpCanvas.notices_left = answer.read_s8()
                MpCanvas.notice_kind = 1
                MpCanvas.set_state(6)
                return
            MpCanvas.error_msg = 0
            self.push_state(4)
        elif s == 513:
            if MpCanvas.answer_status == 1:
                MpCanvas.room_bg = answer.read_s8()
                MpCanvas.my_slot = answer.read_s8()
                MpCanvas.room_mode = answer.read_s8()
                answer.read_s8()
                MpCanvas.painting_blocked = True
                self.free_frame_images()
                MpCanvas.painting_blocked = False
                MpCanvas.room_dirty = True
                return
            MpCanvas.error_msg = 0
            if MpCanvas.answer_status == (-11):
                MpCanvas.error_msg = 8
            self.push_state(4)
        elif s == 769:
            if MpCanvas.answer_status == 1:
                MpCanvas.room_bg = answer.read_s8()
                MpCanvas.my_slot = answer.read_s8()
                MpCanvas.room_mode = answer.read_s8()
                answer.read_s8()
                MpCanvas.painting_blocked = True
                self.free_frame_images()
                MpCanvas.painting_blocked = False
                MpCanvas.room_dirty = True
                return
            if MpCanvas.answer_status == (-3):
                MpCanvas.error_msg = 2
            elif MpCanvas.answer_status == (-4):
                MpCanvas.error_msg = 3
            elif MpCanvas.answer_status == (-5):
                MpCanvas.error_msg = 4
            elif MpCanvas.answer_status == (-12):
                MpCanvas.error_msg = 9
            elif MpCanvas.answer_status == (-16):
                MpCanvas.error_msg = 18
            else:
                MpCanvas.error_msg = 0
            self.push_state(4)
        elif s == 770:
            if MpCanvas.answer_status == 1:
                MpCanvas.popup_shown = False
                MpCanvas.room_bg = answer.read_s8()
                MpCanvas.my_slot = answer.read_s8()
                MpCanvas.room_mode = answer.read_s8()
                answer.read_s8()
                MpCanvas.painting_blocked = True
                self.free_frame_images()
                MpCanvas.painting_blocked = False
                MpCanvas.room_dirty = True
                return
            MpCanvas.error_msg = 0
            self.push_state(4)
        elif s == 514:
            if MpCanvas.answer_status == 1:
                MpCanvas.loop_i = 0
                while MpCanvas.loop_i < 4:
                    if not MpCanvas.fighter_present[MpCanvas.loop_i]:
                        MpCanvas.cur_slot = MpCanvas.loop_i
                        break
                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                MpCanvas.fighter_present[MpCanvas.cur_slot] = True
                MpCanvas.fighter_slot[MpCanvas.cur_slot] = answer.read_s8()
                if imod(MpCanvas.fighter_slot[MpCanvas.cur_slot], 2) == imod(MpCanvas.fighter_slot[0], 2):
                    MpCanvas.allies_alive = MpCanvas.allies_alive + 1
                else:
                    MpCanvas.enemies_alive = MpCanvas.enemies_alive + 1
                MpCanvas.fighter_name[MpCanvas.cur_slot] = answer.read_string(8)
                MpCanvas.fighter_level[MpCanvas.cur_slot] = answer.read_s16()
                MpCanvas.fighter_wins[MpCanvas.cur_slot] = answer.read_s32()
                MpCanvas.fighter_losses[MpCanvas.cur_slot] = answer.read_s32()
                MpCanvas.fighter_hp[MpCanvas.cur_slot] = answer.read_s16()
                MpCanvas.fighter_max_hp[MpCanvas.cur_slot] = MpCanvas.fighter_hp[MpCanvas.cur_slot]
                MpCanvas.fighter_weapon[MpCanvas.cur_slot] = answer.read_s8()
                MpCanvas.fighter_face[MpCanvas.cur_slot] = answer.read_s8()
                if MpCanvas.fighter_face[MpCanvas.cur_slot] == 10:
                    MpCanvas.fighter_face[MpCanvas.cur_slot] = 0
                    MpCanvas.fighter_kind[MpCanvas.cur_slot] = 2
                elif MpCanvas.fighter_face[MpCanvas.cur_slot] < 10:
                    MpCanvas.fighter_kind[MpCanvas.cur_slot] = 0
                else:
                    MpCanvas.fighter_face[MpCanvas.cur_slot] = i8(MpCanvas.fighter_face[MpCanvas.cur_slot] - 30)
                    MpCanvas.fighter_kind[MpCanvas.cur_slot] = 1
                MpCanvas.fighter_quote_start[MpCanvas.cur_slot] = answer.read_string(20)
                MpCanvas.fighter_quote_win[MpCanvas.cur_slot] = answer.read_string(20)
                MpCanvas.fighter_cr[MpCanvas.cur_slot] = answer.read_s8()
                MpCanvas.fighter_alt_name[MpCanvas.cur_slot] = answer.read_string(8)
                MpCanvas.fighter_mp[MpCanvas.cur_slot] = 0
                MpCanvas.place_fighter(MpCanvas.cur_slot)
                MpCanvas.fighter_blink[MpCanvas.cur_slot] = imod(abs(MpCanvas.rng.nextInt()), 4)
                MpCanvas.fighter_status[MpCanvas.cur_slot] = 99
                MpCanvas.fighter_status_ticks[MpCanvas.cur_slot] = 0
                MpCanvas.hud_dirty = True
                if MpCanvas.state != 4:
                    return
                MpCanvas.set_state(90)
                MpCanvas.room_dirty = True
                return
            MpCanvas.error_msg = 0
            self.push_state(4)
        elif s == 1024:
            if MpCanvas.answer_status == 1:
                MpCanvas.set_state(92)
        elif s == 1026:
            if MpCanvas.answer_status == 1:
                MpCanvas.chosen_action = 99
                MpCanvas.set_timer(10 - MpCanvas.speed)
                MpCanvas.choose_secs = 1 if MpCanvas.auto_battle else 10   # PORT-EXTRA auto-battle
                MpCanvas.exit_asked = False
                MpCanvas.set_state(94)
        elif s == 1028:
            if MpCanvas.answer_status == 1:
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
                        MpCanvas.turn_actions[MpCanvas.cur_slot] = answer.read_s8()
                    else:
                        MpCanvas.tmp = answer.read_s8()
                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                MpCanvas.turn_record_count = answer.read_s8()
                MpCanvas.loop_i = 0
                while MpCanvas.loop_i < MpCanvas.turn_record_count:
                    MpCanvas.turn_bytes[(0 + MpCanvas.loop_i)] = answer.read_s8()
                    MpCanvas.turn_bytes[(4 + MpCanvas.loop_i)] = answer.read_s8()
                    MpCanvas.turn_hps[(0 + MpCanvas.loop_i)] = answer.read_s16()
                    MpCanvas.turn_bytes[(8 + MpCanvas.loop_i)] = answer.read_s8()
                    MpCanvas.turn_bytes[(12 + MpCanvas.loop_i)] = answer.read_s8()
                    MpCanvas.turn_bytes[(16 + MpCanvas.loop_i)] = answer.read_s8()
                    MpCanvas.turn_hps[(4 + MpCanvas.loop_i)] = answer.read_s16()
                    MpCanvas.turn_bytes[(20 + MpCanvas.loop_i)] = answer.read_s8()
                    MpCanvas.turn_bytes[(24 + MpCanvas.loop_i)] = answer.read_s8()
                    MpCanvas.turn_bytes[(28 + MpCanvas.loop_i)] = answer.read_s8()
                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                answer.read_s8()
                MpCanvas.loop_i = 0
                while MpCanvas.loop_i < MpCanvas.turn_record_count:
                    if MpCanvas.turn_bytes[(24 + MpCanvas.loop_i)] == 1:
                        MpCanvas.turn_bytes[(32 + MpCanvas.loop_i)] = answer.read_s8()
                        MpCanvas.turn_bytes[(36 + MpCanvas.loop_i)] = answer.read_s8()
                        MpCanvas.turn_hps[(8 + MpCanvas.loop_i)] = answer.read_s16()
                        MpCanvas.turn_bytes[(40 + MpCanvas.loop_i)] = answer.read_s8()
                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                MpCanvas.set_state(99)
        elif s == 1031:
            if MpCanvas.answer_status == 1:
                MpCanvas.room_bg = answer.read_s8()
                MpCanvas.set_state(104)
        elif s == 1032:
            if MpCanvas.answer_status == 1:
                MpCanvas.battle_won = answer.read_s8()
                if MpCanvas.room_mode != 2:
                    if MpCanvas.battle_won == 1:
                        MpCanvas.wins = MpCanvas.wins + 1
                    else:
                        MpCanvas.losses = MpCanvas.losses + 1
                MpCanvas.reward_gold = answer.read_s16()
                MpCanvas.reward_grade = answer.read_s8()
                MpCanvas.reward_fame = answer.read_s16()
                MpCanvas.reward_exp = answer.read_s16()
                MpCanvas.loot = answer.read_string(15)
                MpCanvas.reward_rank = answer.read_s32()
                answer.read_s8()
                answer.read_s32()
                answer.read_s8()
                MpCanvas.set_state(105)
        elif s == 1037:
            if MpCanvas.answer_status == 1:
                MpCanvas.stage_title = answer.read_string(14)
                MpCanvas.stage_count = answer.read_s8()
                MpCanvas.stage = answer.read_s8()
                MpCanvas.set_state(91)
        elif s == 1035:
            while True:
                if MpCanvas.answer_status == 1:
                    MpCanvas.leaving_slot = answer.read_s8()
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
                        return
                    MpCanvas.enemies_alive = MpCanvas.enemies_alive - 1
                break
        elif s == 1281:
            if MpCanvas.answer_status == 1:
                MpCanvas.name = MpCanvas.input_text
                self.pop_states(2)
                return
            if MpCanvas.answer_status == (-6):
                MpCanvas.error_msg = 6
                self.push_state(4)
                return
            if MpCanvas.answer_status in (-49, -15):
                MpCanvas.error_msg = 5
                self.push_state(4)
                return
            MpCanvas.error_msg = 0
            self.push_state(4)
        elif s == 1283:
            self.push_state(84)
            if MpCanvas.answer_status == 1:
                MpCanvas.quote_start = MpCanvas.input_text
                MpCanvas.letter_cursor = 0
                MpCanvas.input_text = MpCanvas.quote_win
                MpCanvas.quote_step = 1
                return
            if MpCanvas.answer_status == (-49):
                MpCanvas.error_msg = 5
                self.push_state(4)
                return
            MpCanvas.error_msg = 0
            self.push_state(4)
        elif s == 1285:
            if MpCanvas.answer_status == 1:
                MpCanvas.quote_win = MpCanvas.input_text
                self.pop_state()
                return
            if MpCanvas.answer_status == (-49):
                MpCanvas.error_msg = 5
                self.push_state(4)
                return
            MpCanvas.error_msg = 0
            self.push_state(4)
        elif s == 1288:
            if MpCanvas.answer_status == 1:
                MpCanvas.attr_hp = answer.read_s16()
                MpCanvas.attr_hp_bonus = answer.read_s16()
                MpCanvas.attr_mp = answer.read_s16()
                MpCanvas.attr_mp_bonus = answer.read_s16()
                MpCanvas.attr_attack = answer.read_s16()
                MpCanvas.attr_attack_bonus = answer.read_s16()
                MpCanvas.attr_defense = answer.read_s16()
                MpCanvas.attr_defense_bonus = answer.read_s16()
                self.push_state(81)
                return
            MpCanvas.error_msg = 0
            self.push_state(4)
        elif s == 1290:
            if MpCanvas.answer_status == 1:
                MpCanvas.loop_i = 0
                while MpCanvas.loop_i < 11:
                    MpCanvas.skill_levels[MpCanvas.loop_i] = 99
                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                MpCanvas.skill_count = answer.read_s8()
                MpCanvas.loop_i = 0
                while MpCanvas.loop_i < MpCanvas.skill_count:
                    MpCanvas.skill_id = answer.read_s8()
                    MpCanvas.skill_levels[(MpCanvas.skill_id - 3)] = answer.read_s8()
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
                            MpCanvas.skill_order[MpCanvas.loop_i] = i8(3 + MpCanvas.loop_j)
                            break
                        MpCanvas.loop_j = MpCanvas.loop_j + 1
                    MpCanvas.loop_i = MpCanvas.loop_i + 1
                self.push_state(82)
                return
            MpCanvas.error_msg = 0
            self.push_state(4)
        elif s == 1292:
            if MpCanvas.answer_status == 1:
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
        elif s == 1297:
            if MpCanvas.answer_status == 1:
                MpCanvas.fame = answer.read_s32()
                MpCanvas.duel_grade = answer.read_s32()
                MpCanvas.mission_grade = answer.read_s32()
                self.push_state(80)
                return
            MpCanvas.error_msg = 0
            self.push_state(4)
        elif s == 1299:
            if MpCanvas.answer_status == 1:
                MpCanvas.exp = answer.read_s32()
                MpCanvas.fame = answer.read_s32()
                MpCanvas.gold = answer.read_s32()
                self.push_state(83)
                return
            MpCanvas.error_msg = 0
            self.push_state(4)
        elif s == 1536:
            if MpCanvas.answer_status == 1:
                MpCanvas.notice_kind = answer.read_s8()
                j_line = 0
                while j_line < 4:
                    MpCanvas.notice_lines[j_line] = answer.read_string(16)
                    j_line = j_line + 1
                MpCanvas.notices_left = 0
                MpCanvas.set_state(6)
        elif s == 289:
            if MpCanvas.answer_status == 1:
                invitation = answer.read_s32()
                MpCanvas.invitation_saved = invitation
                MpCanvas.invitation = invitation
                self.push_state(88)
                return
            MpCanvas.error_msg = 0
            self.push_state(4)
        elif s == 291:
            if MpCanvas.answer_status == 1:
                self.pop_state()
                return
            MpCanvas.error_msg = 0
            self.push_state(4)

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
        MpCanvas.set_timer(-1)
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

    def on_net_error(self, code):  # g.java:3425
        if not MpCanvas.disconnecting:
            MpCanvas.error_msg = (7 if (code < 10) else code)
            self.on_disconnect()
        MpCanvas.disconnecting = False

    def check_invite_timeout(self):  # g.java:5334
        if MpCanvas.wait_started:
            if idiv(((MpCanvas.wait_start_time - system.currentTimeMillis())), 1000) >= 80:
                MpCanvas.wait_started = False
                MpCanvas.error_msg = 13
                MpCanvas.popup_shown = False
                MpCanvas.disconnect()
                MpCanvas.set_timer(-1)
                self.push_state(4)
        else:
            MpCanvas.wait_started = True
            MpCanvas.wait_start_time = system.currentTimeMillis()
