class_name OnlineBattleScreen
extends BaseScreen
## The multiplayer battle in the new art, as the rest of the game: the stage under a painted sky
## (scripts/world/battle_stage.gd: the field of the battle's background, the fighters as the
## maps' people, the effects of the missions on them, the chevron over the target), the HUD
## over it (scripts/ui/battle_hud.gd: the plates, the cards of the actions, the changes of HP,
## the quotes), the pad of the actions (sabre, shield, wind, a skill) with the seconds left, the
## skills with their icons and the timing bar (scripts/ui/timing_bar.gd). What happens is
## scripts/net/online_battle.gd, one step every TICK_MS; the figures move and turn smoothly
## between the steps. This screen shows it and passes the keys: arrows choose (Right Attack, Left
## Defend, Up Evade, Down a skill), Enter / Space confirms and stops the timing bar, Esc asks to
## leave the battle, Tab, F, the pad's Back (the "auto" action, as auto-hunt on the map) or a
## click on AUTO in the bottom-left corner turn auto-battle on and off. The pad's buttons, the
## skills and the bar take the mouse too. The hint at the bottom names the keys of the device
## just used (InputSetup.hint: the keyboard's or the pad's).
## What the battle earned goes to the hero as soon as the result comes: gold, fame, exp (a
## level maybe), the loot into the backpack (a potion onto the belt).
## Router.params: online (the client, tests), profile_path (tests); the battle is the
## client's `battle`.

const MP := "res://assets/original/mp/"  # the battle's sounds
const AUTO_ON := UiTheme.ACCENT  # AUTO while auto-battle is on
## The pad's buttons (in the scene: Evade up, Defend left, Attack right, a skill down): key and
## icon (assets/art/ui).
const PAD := [["up", "wind"], ["left", "shield"], ["right", "sabre"], ["down", "fire"]]

var online: RefCounted
var battle: RefCounted
var hero_path: String = Profile.PATH
var rewarded := false  # the result's rewards went to the hero
var levels_gained := 0
var loot_lost := false  # no room for it
var pad_buttons := {}  # key -> Button
var skill_buttons: Array[Button] = []
var _acc := 0.0
var _bg_shown := -1
var _no_skill: Texture2D

@onready var sky: ShaderMaterial = $Sky.material
@onready var stage: BattleStage = $World/Viewport/Stage
@onready var hud: BattleHud = %Hud
@onready var center: PanelContainer = %Center
@onready var center_text: Label = %CenterText
@onready var pad: Control = %Pad
@onready var countdown: Label = %Countdown
@onready var skill_list: VBoxContainer = %Skills
@onready var bar: TimingBar = %Bar
@onready var hint: Label = %Hint
@onready var auto_button: Button = %Auto  # AUTO in the bottom-left corner
@onready var _sound_player: AudioStreamPlayer = $Sound


func _ready() -> void:
	online = OnlineClient.of(Router.params)
	battle = null if online == null else online.battle
	hero_path = profile_path()
	stage.battle = battle
	hud.battle = battle
	hud.camera = stage.camera
	bar.battle = battle
	_setup_pad()
	if battle == null:
		center_text.text = tr("live.failed")
		center.visible = true
		return
	_refresh()


func _notification(what: int) -> void:
	if what == NOTIFICATION_RESIZED and sky != null:
		_fit_sky()


# --- the sky --------------------------------------------------------------------------------
## The field of the battle's background byte and its sky.
func show_background(bg: int) -> void:
	_bg_shown = bg
	stage.arena.build(bg)
	var s: Dictionary = stage.arena.sky_settings()
	for key in s:
		sky.set_shader_parameter(key, s[key])
	_fit_sky()


## The sky's shape and its horizon where the far land meets it on screen.
func _fit_sky() -> void:
	var view := size if size.x > 0.0 and size.y > 0.0 else Vector2(1280, 720)
	sky.set_shader_parameter("aspect", view.x / view.y)
	var far := (
		stage.camera.unproject_position(Vector3(0, 1.6, -40))
		if stage.camera.is_inside_tree()
		else Vector2(0, view.y * 0.3)
	)
	sky.set_shader_parameter("horizon_y", clampf(far.y / view.y + 0.03, 0.1, 0.9))


## The pad's buttons with their icons.
func _setup_pad() -> void:
	for k in PAD:
		var b: Button = pad.get_node(str(k[0]).capitalize())
		b.icon = hud.icon(k[1], 52)
		pad_buttons[k[0]] = b


# --- steps ----------------------------------------------------------------------------------
func _process(delta: float) -> void:
	if battle == null:
		return
	if online != null and online.battle != battle:  # kicked: the account went online elsewhere
		leave()
		return
	_acc += delta * 1000.0
	stage.clock += delta
	var stepped := false
	while _acc >= OnlineBattle.TICK_MS:
		_acc -= OnlineBattle.TICK_MS
		battle.tick()
		for n in battle.sounds:
			play_sound(int(n))
		stepped = true
		if battle.left:
			break
	if stepped:
		_refresh()
	if battle.left:
		leave()
		return
	stage.move_fighters(delta, _part_of_step())


## How far the screen is from this step to the next (0..1).
func _part_of_step() -> float:
	return clampf(_acc / OnlineBattle.TICK_MS, 0.0, 1.0)


func play_sound(n: int) -> void:
	var path := MP + "snd%d.ogg" % n
	if ResourceLoader.exists(path):
		_sound_player.stream = load(path)
		_sound_player.play()


## Shows the battle as it is now.
func _refresh() -> void:
	if battle.state == OnlineBattle.RESULT and not rewarded:
		take_rewards()
	if battle.bg != _bg_shown:
		show_background(battle.bg)
	stage.show_fighters(not is_processing(), _part_of_step())
	hud.show_portraits()
	var st: int = battle.state
	var choosing: bool = st in [OnlineBattle.CHOOSE, OnlineBattle.TARGET] and not battle.exit_prompt
	pad.visible = choosing
	if choosing:
		for k in pad_buttons:
			var b: Button = pad_buttons[k]
			var mine: bool = (
				{"right": 0, "left": 1, "up": 2}.get(k, -1) == battle.chosen_action
				or (k == "down" and battle.chosen_action >= 3 and battle.chosen_action <= 13)
			)
			b.modulate = Color(1, 0.9, 0.5) if mine else Color.WHITE
			b.disabled = st != OnlineBattle.CHOOSE
		pad_buttons["down"].icon = (
			hud.icon("fire", 52) if battle.any_skill_ready() else _no_skill_icon()
		)
		countdown.text = str(battle.choose_secs) if st == OnlineBattle.CHOOSE else ""
	_show_skills()
	bar.visible = battle.bar_shown and st in [OnlineBattle.BAR, OnlineBattle.SENT]
	bar.queue_redraw()
	center.visible = true
	center_text.text = center_message()
	center.visible = not center_text.text.is_empty()
	center.reset_size()
	center.position = Vector2((size.x - center.size.x) / 2.0, size.y * 0.36 - center.size.y / 2.0)
	hint.text = hint_text()
	_show_auto()
	hud.queue_redraw()


func center_message() -> String:
	var b: RefCounted = battle
	var dots := ".".repeat(b.state_ticks % 4)
	match b.state:
		OnlineBattle.ROOM:
			return tr("online.battle_waiting") + dots
		OnlineBattle.STAGE_INTRO:
			var lines := [b.stage_title, tr("online.battle_stage") % [b.stage, b.stage_count]]
			for f in b.fighters:
				if f.present and f.team() != b.my_slot % 2:
					lines.append("%s  Lv%d" % [f.name, f.level])
			return "\n".join(lines)
		OnlineBattle.ROUND:
			if (
				b.round_no > 0
				and b.allies_alive > 0
				and b.enemies_alive > 0
				and b.fighters[0].hp > 0
			):
				return (
					tr("online.battle_round") % b.round_no
					+ "\n"
					+ tr("online.battle_waiting")
					+ dots
				)
		OnlineBattle.CHOOSE:
			if b.exit_prompt:
				var secs: int = 15 - b.exit_ticks * OnlineBattle.TIME_MS / 1000
				return (
					tr("online.battle_exit_ask")
					+ "\n"
					+ (
						("[%s]   %s" if b.exit_cursor == 0 else "%s   [%s]")
						% [tr("online.yes"), tr("online.no")]
					)
					+ "\n"
					+ tr("online.battle_remain") % secs
				)
		OnlineBattle.SENT:
			if b.state_ticks >= 4:
				return tr("online.battle_waiting") + dots
		OnlineBattle.NO_BATTLE:
			return tr("online.battle_no_battle")
		OnlineBattle.OVER:
			return tr("online.battle_waiting") + dots
		OnlineBattle.STAGE_END:
			return (
				"%s\n%s\n%s"
				% [
					b.stage_title,
					tr("online.battle_stage_n") % b.stage,
					tr("online.battle_complete")
				]
			)
		OnlineBattle.RESULT:
			if b.result_shown():
				return result_text()
	return ""


## The rewards of battle_end to the hero, once.
func take_rewards() -> void:
	rewarded = true
	var r: Dictionary = battle.result
	var p: RefCounted = Profile.load_or_new(hero_path)
	p.gold = clampi(int(p.gold) + int(r.get("gold", 0)), 0, 0x7FFFFFFF)
	p.fame = clampi(int(p.fame) + int(r.get("fame", 0)), 0, 0x7FFFFFFF)
	levels_gained = p.gain_exp(int(r.get("exp", 0))) if int(r.get("exp", 0)) > 0 else 0
	var loot: Variant = r.get("loot", {})
	if loot is Dictionary and int((loot as Dictionary).get("id", 0)) > 0:
		var item: Dictionary = (loot as Dictionary).duplicate()
		item.erase("name")
		var id := int(item.id)
		loot_lost = not (p.add_potion(id) if id <= 11 else p.add_item(item))
	p.save(hero_path)


func result_text() -> String:
	var b: RefCounted = battle
	var r: Dictionary = b.result
	var lines: Array = [str(b.fighters[0].name)]
	if b.mode != 2:
		lines.append(tr("online.battle_win") if b.battle_won == 1 else tr("online.battle_lose"))
		lines.append(tr("online.battle_wins") % b.wins)
		lines.append(tr("online.battle_losses") % b.losses)
		lines.append(tr("online.battle_gold") % int(r.get("gold", 0)))
		lines.append(tr("online.battle_fame") % int(r.get("fame", 0)))
	else:
		lines.append(
			(
				tr("online.mission_grade") % OnlineClient.grade(int(r.get("grade", 0)))
				if b.battle_won == 1
				else tr("online.battle_failed")
			)
		)
		lines.append(tr("online.battle_gold") % int(r.get("gold", 0)))
		lines.append(tr("online.battle_exp") % int(r.get("exp", 0)))
		lines.append(tr("online.battle_fame") % int(r.get("fame", 0)))
	var loot: Variant = r.get("loot", {})
	if loot is Dictionary and not (loot as Dictionary).is_empty():
		lines.append(tr("online.battle_loot") % tr(str(loot.get("name", ""))))
		if loot_lost:
			lines.append(tr("online.battle_bag_full"))
	lines.append(tr("online.battle_rank") % int(r.get("rank", 0)))
	if levels_gained > 0:
		lines.append(tr("online.battle_level_up") % levels_gained)
	lines.append("")
	lines.append(tr("online.battle_ok"))
	return "\n".join(lines)


## AUTO in the bottom-left corner while the actions are chosen: gold AUTO while
## auto-battle is on, white with its keys while it is off (named for the device in use). A click
## or a tap turns it over, as Tab, F or the pad's Back.
func _show_auto() -> void:
	auto_button.visible = battle.state >= OnlineBattle.CHOOSE and battle.state <= OnlineBattle.SENT
	auto_button.text = "AUTO" if battle.auto_battle else InputSetup.hint("online.battle_auto_key")
	var c := AUTO_ON if battle.auto_battle else Color.WHITE
	for k in [
		"font_color",
		"font_hover_color",
		"font_pressed_color",
		"font_focus_color",
		"font_hover_pressed_color"
	]:
		auto_button.add_theme_color_override(k, c)


func hint_text() -> String:
	var auto := "   " + tr("online.battle_auto_on") if battle.auto_battle else ""
	match battle.state:
		OnlineBattle.CHOOSE:
			return (
				("" if battle.exit_prompt else InputSetup.hint("online.battle_hint_choose")) + auto
			)
		OnlineBattle.SKILLS:
			return InputSetup.hint("online.battle_hint_skills") + auto
		OnlineBattle.TARGET:
			return InputSetup.hint("online.battle_hint_target") + auto
		OnlineBattle.BAR:
			return InputSetup.hint("online.battle_hint_bar") + auto
	return auto.strip_edges()


## The skill key's sign while no skill has the MP: the same, grey and dim.
func _no_skill_icon() -> Texture2D:
	if _no_skill == null:
		var img := hud.icon("fire", 52).get_image()
		for y in img.get_height():
			for x in img.get_width():
				var c := img.get_pixel(x, y)
				var v := c.get_luminance() * 0.6
				img.set_pixel(x, y, Color(v, v, v * 1.05, c.a * 0.8))
		_no_skill = ImageTexture.create_from_image(img)
	return _no_skill


func _show_skills() -> void:
	skill_list.visible = battle.state == OnlineBattle.SKILLS
	if not skill_list.visible:
		return
	if skill_buttons.size() != battle.skill_slots.size():
		for c in skill_list.get_children():
			c.queue_free()
		skill_buttons.clear()
		for k in battle.skill_slots.size():
			var b := Button.new()
			b.name = "Skill%d" % k
			b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
			b.focus_mode = Control.FOCUS_NONE
			b.alignment = HORIZONTAL_ALIGNMENT_LEFT
			b.expand_icon = false
			b.add_theme_constant_override("icon_max_width", 40)
			b.custom_minimum_size = Vector2(0, 54)
			b.pressed.connect(
				func() -> void:
					battle.skill_cursor = k
					press("fire")
			)
			skill_list.add_child(b)
			skill_buttons.append(b)
	for k in skill_buttons.size():
		var s := int(battle.skill_slots[k])
		var b := skill_buttons[k]
		b.text = (
			"%s  MP %d"
			% [
				OnlineClient.skill_name(s),
				int(battle.skill_costs[s - 3]) if s - 3 < battle.skill_costs.size() else 0
			]
		)
		b.disabled = not battle.skill_ready(s)
		b.icon = ItemSlot.icon(
			"skill" if not b.disabled else "skillgray", int(BattleHud.SKILL_ICONS.get(s, -1))
		)
		b.modulate = Color(1, 0.9, 0.5) if k == battle.skill_cursor else Color.WHITE


# --- keys -----------------------------------------------------------------------------------
func press(k: String) -> void:
	if battle == null:
		return
	battle.key(k)
	_refresh()
	if battle.left:
		leave()


## The battle reads the back key itself (below), so the base does not take it.
func handles_back() -> bool:
	return false


func _screen_input(event: InputEvent) -> void:
	if battle == null:
		if event.is_action_pressed("ui_cancel"):
			Router.back()
		return
	var keys := {
		"ui_up": "up",
		"ui_down": "down",
		"ui_left": "left",
		"ui_right": "right",
		"ui_accept": "fire",
		"ui_cancel": "back"
	}
	for action in keys:
		if event.is_action_pressed(action):
			get_viewport().set_input_as_handled()
			press(keys[action])
			return
	if event.is_action_pressed("auto"):
		get_viewport().set_input_as_handled()
		press("auto")


## Back to the menu the battle came from; the online client forgets the battle.
func leave() -> void:
	if online != null:
		online.battle_over()
	battle = null
	stage.battle = null
	hud.battle = null
	bar.battle = null
	Router.back()


## No line of control hints under this screen: it shows its own (scripts/ui/hint_bar.gd).
func controls_hint() -> String:
	return ""
