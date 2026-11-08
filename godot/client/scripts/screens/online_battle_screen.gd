extends Control
## The multiplayer battle in the new art, as the rest of the game: a field of the maps' ground
## and things under a painted sky (scripts/world/battle_arena.gd, after the battle's
## background), the fighters as the maps' people (scripts/world/battle_motion.gd: who is who,
## which clip shows each animation of the battle) and the effects of the missions on them
## (scripts/world/map_effects.gd: blade trails, blood where a blow lands and under the fallen,
## sparks on a guard, dust of a dodge, the healing spiral, the light of a soul and the ring of
## its aura), and the HUD over it. A blow that lands shakes the view. What
## happens is scripts/net/online_battle.gd, one step every TICK_MS; the figures move and turn
## smoothly between the steps. This screen shows it and passes the keys: arrows choose (Right
## Attack, Left Defend, Up Evade, Down a skill), Enter / Space confirms and stops the timing bar,
## Esc asks to leave the battle, Tab, F, R3 (the "auto" action, as auto-hunt on the map) or a
## click on AUTO in the bottom-left corner turn auto-battle on and off. The pad's buttons, the
## skills and the bar take the mouse too. The hint at the bottom names the keys of the device
## just used (InputSetup.hint: the keyboard's or the pad's).
## The HUD: each fighter's plate at the top (my team at the left, the other at the right, one
## row under the other) with his portrait in an iron frame looking at the other side, his name,
## level on a cinnabar badge, HP and MP bars; the card of his action beside it; the changes of
## HP over the fighters; the quotes in parchment bubbles; the pad of the actions (sabre, shield,
## wind, a skill) with the seconds left; the skills with their icons; the timing bar (the
## cursor runs to the gold mark); a gold chevron over the target being chosen.
## What the battle earned goes to the hero as soon as the result comes: gold, fame, exp (a
## level maybe), the loot into the backpack (a potion onto the belt).
## Router.params: online (the client, tests), profile_path (tests); the battle is the
## client's `battle`.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const OnlineClient := preload("res://scripts/net/online_client.gd")
const OnlineBattle := preload("res://scripts/net/online_battle.gd")
const Profile := preload("res://scripts/core/profile.gd")
const ArtFigure := preload("res://scripts/art/art_figure.gd")
const ArtHud := preload("res://scripts/art/art_hud.gd")
const BattleArena := preload("res://scripts/world/battle_arena.gd")
const BattleMotion := preload("res://scripts/world/battle_motion.gd")
const MapEffects := preload("res://scripts/world/map_effects.gd")
const MapPeople := preload("res://scripts/world/map_people.gd")
const Pictures := preload("res://scripts/ui/pictures.gd")
const ItemSlot := preload("res://scripts/ui/item_slot.gd")
const SKY_SHADER := preload("res://assets/art/shaders/story_sky.gdshader")
const MP := "res://assets/original/mp/"  # the battle's sounds
## World units per pixel of the battle (online_battle.gd's 240×320 field): one 27 px map tile
## is one unit, as on the map.
const PX := 1.0 / 27.0
## The battle's ground line where the fighters of a 1-on-1 stand.
const GROUND_Y := 225
const TICK := OnlineBattle.TICK_MS / 1000.0
const CAMERA_AT := Vector3(0, 2.2, 10.2)
const CAMERA_TO := Vector3(0, 1.2, 0)
const CAMERA_FOV := 32.0
## The people stand a little taller than on the maps: the battle is seen closer.
const FIGURE_SCALE := 1.18
## How quickly a figure turns to its new direction (1/s).
const TURN := 14.0
const BAR_SCALE := 4.0
## The change of HP rises from this many of the battle's pixels over the feet (and its own rise).
const DAMAGE_UP := 22.0
const QUOTE_UP := 66.0  # the quote's tail over the feet
const MARKER_UP := 2.6  # the target's chevron over the feet (world units)
const SHAKE := 0.07  # how far a blow that lands shakes the view (world units)
const HIT_FLASH := Color(0.8, 0.16, 0.12)  # the flash of one who is hit: blood-red
## The rows of a 2-on-2 stand apart in depth; seen from the camera the back one would hide
## behind the front one, so the farther a fighter stands the farther out from the middle it
## is drawn (by this part of its distance from the middle per pixel of depth).
const SPREAD := 0.016
const PAD_BUTTON := 96
const BOX_W := 360.0  # a fighter's plate at the top; the card of its action beside it
const BOX_H := 80.0
const FACE := 68.0  # the portrait on the plate
const CARD_W := 230.0
const AUTO_ON := UiTheme.ACCENT  # AUTO while auto-battle is on
const PLATE := Color(0.07, 0.066, 0.062, 0.92)
const PAPER := Color("c9bb9b")  # old parchment
const HP_FILL := [Color("c23a2f"), Color("5e1510")]
const MP_FILL := [Color("5a83bd"), Color("1a2e55")]
const DAMAGE := Color("e8553f")
const HEAL := Color("8fc873")
## The pad: key, icon (assets/art/ui), caption, place in buttons.
const PAD := [["up", "wind", "online.battle_evade", Vector2(1, 0)],
	["left", "shield", "online.battle_defend", Vector2(0, 1)],
	["right", "sabre", "online.battle_attack", Vector2(2, 1)],
	["down", "fire", "online.battle_skill", Vector2(1, 2)]]
## The icons of the battle's skills (3..13): their places on the sheet of the skills (the
## same skills of the map, 12..22).
const SKILL_ICONS := {3: 0, 4: 1, 5: 2, 6: 8, 7: 9, 8: 10, 9: 3, 10: 4, 11: 5, 12: 6, 13: 7}
## The chevron over the target: brass over blood-red, inked.
const MARKER_SVG := '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 72"><path d="M8 6 L32 26 L56 6 L56 20 L32 40 L8 20 Z" fill="#b89550" stroke="#0f0d0c" stroke-width="3.5" stroke-linejoin="round"/><path d="M14 34 L32 49 L50 34 L50 45 L32 62 L14 45 Z" fill="#8a2b25" stroke="#0f0d0c" stroke-width="3.5" stroke-linejoin="round"/></svg>'

var online: RefCounted
var battle: RefCounted
var profile_path: String = Profile.PATH
var rewarded := false  # the result's rewards went to the hero
var levels_gained := 0
var loot_lost := false  # no room for it
var viewport: SubViewport
var camera: Camera3D
var stage: Node3D
var arena: Node3D  # BattleArena
var sky: ShaderMaterial
var effects: Node3D  # MapEffects
var bodies: Array[Node3D] = []  # Fighter0..3: where each fighter stands
var figures: Array = [null, null, null, null]  # the ArtFigure of each
var portraits: Array[TextureRect] = []
var marker: Sprite3D
var hud: Control
var pad: Control
var pad_buttons := {}  # key -> Button
var skill_list: VBoxContainer
var skill_buttons: Array[Button] = []
var countdown: Label
var hint: Label
var auto_button: Button  # AUTO in the bottom-left corner
var center: PanelContainer
var center_text: Label
var bar: Control
var _acc := 0.0
var _clock := 0.0
var _bg_shown := -1
var _sound_player: AudioStreamPlayer
var _looks := ["", "", "", ""]  # what each figure was made for
var _last: Array[Vector2i] = []  # [animation, ticks into it] of each fighter drawn last
var _from: Array[Vector3] = []  # where each stood at the step before and stands now
var _to: Array[Vector3] = []
var _yaw: Array[float] = []
var _fx: Array = []  # the effects of this step (MapEffects.show_effects)
var _fallen_at: Array[float] = [-1.0, -1.0, -1.0, -1.0]  # when each was first seen lying (_clock)
var _shake := 0.0  # how hard the view shakes from a blow (world units), dying away
var _icons := {}
var _no_skill: Texture2D


class Layer extends Control:
	## Draws with the screen's draw_<what>(layer).
	var screen: Object
	var what := ""

	func _draw() -> void:
		screen.call("draw_" + what, self)


func _ready() -> void:
	online = OnlineClient.of(Router.params)
	battle = null if online == null else online.battle
	profile_path = str(Router.params.get("profile_path", Profile.PATH))
	_build_world()
	_build_hud()
	_sound_player = AudioStreamPlayer.new()
	_sound_player.bus = &"SFX"
	add_child(_sound_player)
	if battle == null:
		center_text.text = tr("live.failed")
		center.visible = true
		return
	_refresh()


func _notification(what: int) -> void:
	if what == NOTIFICATION_RESIZED and sky != null:
		_fit_sky()


## An icon of the new art (assets/art/ui), drawn once at px.
func icon(icon_name: String, px := 64) -> Texture2D:
	var key := "%s %d" % [icon_name, px]
	if not _icons.has(key):
		_icons[key] = ArtHud.icon(icon_name, px)
	return _icons[key]


# --- the stage ------------------------------------------------------------------------------
func _build_world() -> void:
	var back := ColorRect.new()
	back.name = "Sky"
	back.set_anchors_preset(Control.PRESET_FULL_RECT)
	back.mouse_filter = Control.MOUSE_FILTER_IGNORE
	sky = ShaderMaterial.new()
	sky.shader = SKY_SHADER
	back.material = sky
	add_child(back)
	var container := SubViewportContainer.new()
	container.name = "World"
	container.stretch = true
	container.set_anchors_preset(Control.PRESET_FULL_RECT)
	container.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(container)
	viewport = SubViewport.new()
	viewport.own_world_3d = true
	viewport.transparent_bg = true
	viewport.msaa_3d = Viewport.MSAA_2X
	container.add_child(viewport)
	stage = Node3D.new()
	stage.name = "Stage"
	viewport.add_child(stage)
	arena = BattleArena.new()
	arena.name = "Arena"
	stage.add_child(arena)
	camera = Camera3D.new()
	camera.name = "Camera"
	camera.fov = CAMERA_FOV
	stage.add_child(camera)
	camera.look_at_from_position(CAMERA_AT, CAMERA_TO, Vector3.UP)
	effects = MapEffects.new()
	effects.name = "Effects"
	stage.add_child(effects)
	for i in 4:
		var body := Node3D.new()
		body.name = "Fighter%d" % i
		body.visible = false
		stage.add_child(body)
		bodies.append(body)
		_last.append(Vector2i(-1, 0))
		_from.append(Vector3.ZERO)
		_to.append(Vector3.ZERO)
		_yaw.append(0.0)
	marker = Sprite3D.new()
	marker.name = "Target"
	var img := Image.new()
	img.load_svg_from_string(MARKER_SVG, 1.5)
	marker.texture = ImageTexture.create_from_image(img)
	marker.pixel_size = 0.0055
	marker.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	marker.shaded = false
	marker.no_depth_test = true
	marker.render_priority = 2
	marker.visible = false
	stage.add_child(marker)


## The field of the battle's background byte and its sky.
func show_background(bg: int) -> void:
	_bg_shown = bg
	arena.build(bg)
	var s: Dictionary = arena.sky_settings()
	for key in s:
		sky.set_shader_parameter(key, s[key])
	_fit_sky()


## The sky's shape and its horizon where the far land meets it on screen.
func _fit_sky() -> void:
	var view := size if size.x > 0.0 and size.y > 0.0 else Vector2(1280, 720)
	sky.set_shader_parameter("aspect", view.x / view.y)
	var far := camera.unproject_position(Vector3(0, 1.6, -40)) if camera.is_inside_tree() else Vector2(0, view.y * 0.3)
	sky.set_shader_parameter("horizon_y", clampf(far.y / view.y + 0.03, 0.1, 0.9))


## Where a fighter's feet are: the battle's (x, y), with a leap's height kept apart.
static func world_at(sx: float, gy: float, lift: float) -> Vector3:
	var out := 1.0 + (GROUND_Y - gy) * SPREAD
	return Vector3((sx - OnlineBattle.CX) * out * PX, lift * PX, (gy - GROUND_Y) * PX)


## The figure of fighter i, made again when someone else stands in his place.
func _figure(i: int, f: RefCounted) -> Node3D:
	var kind := BattleMotion.kind_of(f)
	var weapons := BattleMotion.weapons_of(f)
	var look := "%s %s" % [kind, weapons]
	if figures[i] != null and _looks[i] == look:
		return figures[i]
	if figures[i] != null:
		figures[i].free()
	var fig: Node3D = ArtFigure.new()
	fig.name = "Figure"
	bodies[i].add_child(fig)
	fig.setup(kind)
	fig.scale = Vector3.ONE * FIGURE_SCALE
	fig.drive_manually()
	if not weapons.is_empty():
		fig.unequip_all()
		for w in weapons:
			fig.equip(w)
	figures[i] = fig
	_looks[i] = look
	_last[i] = Vector2i(-1, 0)
	return fig


## The fighters at this step: each figure's place, the way it faces, its clip; the effects on
## them; the chevron over the target. A still screen (not processing: its clips do not move
## on) shows each at once, without blending.
func _show_fighters() -> void:
	var still := not is_processing()
	_fx.clear()
	var places: Array[Vector3] = []
	for i in 4:
		var f: RefCounted = battle.fighters[i]
		var sx: float = (OnlineBattle.W - f.x) if f.mirrored() else f.x
		places.append(world_at(sx, f.y + f.lift, f.lift))
	for i in 4:
		var f: RefCounted = battle.fighters[i]
		bodies[i].visible = f.present
		if not f.present:
			continue
		var fig := _figure(i, f)
		var fresh := _last[i].x < 0  # just came: stands in his place at once
		var to := places[i]
		_from[i] = _to[i] if _to[i].distance_to(to) < 2.5 and not fresh else to
		_to[i] = to
		var anim := BattleMotion.anim_of(battle, i)
		_yaw[i] = _heading(i, f, anim, places)
		var motion: Array = BattleMotion.motion(battle, i)
		var p := BattleMotion.progress(battle, i)
		var restart := anim != _last[i].x or p.x < _last[i].y
		if restart and anim == 1 and not still:
			_shake = maxf(_shake, SHAKE)  # a blow that lands shakes the view
		_last[i] = Vector2i(anim, p.x)
		var part := float(p.x) / float(p.y)
		if BattleMotion.fallen(battle, i):
			# the fall plays on to its end; seen only now, he lies at once
			if fig.shown_clip != "death":
				fig.act(motion, 0.0, true, 1.0, 0.0)
		else:
			if f.hp > 0 and fig.shown_clip == "death":
				fig.shown_clip = ""  # up again: a new stage
			fig.act(motion, p.y * TICK, restart, part, 0.0 if still else ArtFigure.BLEND)
		fig.flash(0.4 * (1.0 - clampf(part, 0.0, 1.0)) if anim == 1 else 0.0, HIT_FLASH)
		if still or fresh:
			bodies[i].position = to
			bodies[i].rotation.y = _yaw[i]
		_effects_of(i, f, anim, to, p)
	marker.visible = false
	if battle.state == OnlineBattle.TARGET:
		var t: int = battle.target_cursor
		if battle.fighters[t].present:
			marker.visible = true
			marker.position = _to[t] + Vector3(0, MARKER_UP, 0)
	effects.show_effects(_fx, clampf(_acc / OnlineBattle.TICK_MS, 0.0, 1.0))


## The way fighter i faces: towards the other side; running in, at his target; running back,
## to his place; moving into place for a skill, the way he goes.
func _heading(i: int, f: RefCounted, anim: int, places: Array[Vector3]) -> float:
	var way := Vector3(1.0 if f.team() == 0 else -1.0, 0.0, 0.0)
	match anim:
		2:
			var t: int = battle.target
			if t >= 0 and t != i:
				way = places[t] - places[i]
		28:
			var row_y: int = OnlineBattle.CY + 65 + (0 if battle.mode == 0 else (-23 if f.row() == 0 else 23))
			way = world_at(42.0 if f.team() == 0 else OnlineBattle.W - 42.0, row_y, 0.0) - places[i]
		17, 18, 19:
			if (places[i] - _from[i]).length() > 0.01:
				way = places[i] - _from[i]
	if Vector2(way.x, way.z).length() < 0.05:
		way = Vector3(1.0 if f.team() == 0 else -1.0, 0.0, 0.0)
	return atan2(way.x, way.z)


## The effects on fighter i (feet at `at`): the trail of his blade while he strikes, healing or
## a soul's light, sparks where a blow lands on him, dust when he dodges, his aura.
func _effects_of(i: int, f: RefCounted, anim: int, at: Vector3, p: Vector2i) -> void:
	var px := Vector2(at.x / PX, at.z / PX - MapPeople.FOOT_PX)
	var ahead := 6 if f.team() == 0 else 2  # the way he faces, of the map's 8
	if i == battle.attacker and battle.state == OnlineBattle.TURN:
		match anim:
			3, 9, 10, 11, 14, 15, 16:
				var blow := 0
				match anim:
					3:
						blow = 2 if f.kind == OnlineBattle.MONSTER else 0
					10:
						blow = 2
					15:
						blow = 1
					16:
						blow = 0
					_:
						blow = (p.x / 2) % 3
				_fx.append(["trail", (ahead >> 1) * 3 + blow, px])
			12:
				_fx.append(["heal", mini(p.x * 9 / p.y, 8), px])
			13:
				_fx.append(["buff", mini(p.x * 6 / p.y, 5), px])
	match anim:
		1:
			# blood: the drops fly away from the blow, to his own side
			_fx.append(["blood", (4 if f.team() == 1 else 8) + 2 + mini(p.x, 1), px])
		4:
			_fx.append(["spark", mini(p.x, 1), px])  # steel on the guard
		5:
			_fx.append(["slash", ((ahead + 4) % 8) | mini(p.x, 1), px])
	if BattleMotion.fallen(battle, i):
		# blood spreads under the fallen (he lies on his back, his chest behind his feet) and stays;
		# a still screen shows it spread
		if _fallen_at[i] < 0.0:
			_fallen_at[i] = _clock
		var spread := 7 if not is_processing() else clampi(int((_clock - _fallen_at[i]) / 0.25), 0, 7)
		var chest := px - Vector2(1.0 if f.team() == 0 else -1.0, 0.0) * 0.8 / PX
		_fx.append(["pool", spread, chest, true])
	else:
		_fallen_at[i] = -1.0
	if f.status in [11, 12, 13] and battle.state != OnlineBattle.RESULT:
		_fx.append(["aura", battle.state_ticks % 3, px, true])


## Between the steps: the figures walk on to where the next step puts them, turn, and play
## their clips; the effects run on; the chevron bobs.
func _move_fighters(delta: float) -> void:
	var t := clampf(_acc / OnlineBattle.TICK_MS, 0.0, 1.0)
	for i in 4:
		if not bodies[i].visible or figures[i] == null:
			continue
		bodies[i].position = _from[i].lerp(_to[i], t)
		bodies[i].rotation.y = lerp_angle(bodies[i].rotation.y, _yaw[i], 1.0 - exp(-TURN * delta))
		figures[i].advance(delta)
	effects.show_effects(_fx, t)
	if marker.visible:
		marker.position.y = MARKER_UP + 0.08 * sin(_clock * 6.0)
	camera.h_offset = _shake * sin(_clock * 71.0)
	camera.v_offset = _shake * 0.6 * sin(_clock * 53.0 + 1.3)
	_shake = move_toward(_shake, 0.0, delta * SHAKE * 4.0)


# --- the HUD --------------------------------------------------------------------------------
func _build_hud() -> void:
	hud = Layer.new()
	hud.name = "Hud"
	hud.screen = self
	hud.what = "hud"
	hud.set_anchors_preset(Control.PRESET_FULL_RECT)
	hud.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(hud)
	for i in 4:
		var face := Pictures.framed("Portrait%d" % i, Vector2(FACE, FACE))
		face.size = Vector2(FACE, FACE)
		face.mouse_filter = Control.MOUSE_FILTER_IGNORE
		face.visible = false
		hud.add_child(face)
		portraits.append(face)
	center = PanelContainer.new()
	center.name = "Center"
	var box := UiTheme.box(PLATE, UiTheme.IRON, 2)
	box.set_content_margin_all(20)
	box.content_margin_left = 34
	box.content_margin_right = 34
	center.add_theme_stylebox_override("panel", box)
	center.set_anchors_preset(Control.PRESET_CENTER)
	center.visible = false
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	center_text = Label.new()
	center_text.name = "Text"
	center_text.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	center_text.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	center_text.add_theme_font_size_override("font_size", 30)
	center.add_child(center_text)
	add_child(center)
	pad = Control.new()
	pad.name = "Pad"
	pad.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	pad.position = Vector2(-1.5 * PAD_BUTTON, -56 - 3 * PAD_BUTTON)
	add_child(pad)
	# Evade up, Defend left, Attack right, a skill down
	var u := float(PAD_BUTTON)
	for k in PAD:
		var b := Button.new()
		b.name = str(k[0]).capitalize()
		b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		b.text = tr(k[2])
		b.icon = icon(k[1], 52)
		b.icon_alignment = HORIZONTAL_ALIGNMENT_CENTER
		b.vertical_icon_alignment = VERTICAL_ALIGNMENT_TOP
		b.custom_minimum_size = Vector2(u - 6, u - 6)
		b.size = Vector2(u - 6, u - 6)
		b.position = k[3] * u + Vector2(3, 3)
		b.add_theme_font_size_override("font_size", 16)
		b.add_theme_font_override("font", UiTheme.font("bold"))
		for style in ["normal", "hover", "pressed", "disabled", "focus"]:
			var sb: StyleBox = get_theme_stylebox(style, "Button").duplicate()
			if sb != null:
				sb.set_content_margin_all(6)
				sb.content_margin_top = 8
				b.add_theme_stylebox_override(style, sb)
		b.focus_mode = Control.FOCUS_NONE
		b.pressed.connect(press.bind(k[0]))
		pad.add_child(b)
		pad_buttons[k[0]] = b
	countdown = Label.new()
	countdown.name = "Countdown"
	countdown.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	countdown.add_theme_font_override("font", UiTheme.font("title"))
	countdown.add_theme_font_size_override("font_size", 56)
	countdown.add_theme_color_override("font_color", UiTheme.ACCENT)
	countdown.add_theme_color_override("font_outline_color", UiTheme.INK)
	countdown.add_theme_constant_override("outline_size", 10)
	countdown.position = Vector2(3 * u + 14, u + 6)
	pad.add_child(countdown)
	skill_list = VBoxContainer.new()
	skill_list.name = "Skills"
	skill_list.set_anchors_preset(Control.PRESET_CENTER)
	skill_list.position = Vector2(-200, -210)
	skill_list.custom_minimum_size = Vector2(400, 0)
	skill_list.add_theme_constant_override("separation", 6)
	skill_list.visible = false
	add_child(skill_list)
	bar = Layer.new()
	bar.name = "Bar"
	bar.screen = self
	bar.what = "bar"
	bar.set_anchors_preset(Control.PRESET_CENTER_BOTTOM)
	bar.position = Vector2(-55 * BAR_SCALE, -70 - 30 * BAR_SCALE)
	bar.size = Vector2(110 * BAR_SCALE, 30 * BAR_SCALE)
	bar.visible = false
	bar.gui_input.connect(func(e: InputEvent) -> void:
		if e is InputEventMouseButton and e.pressed:
			press("fire"))
	add_child(bar)
	hint = Label.new()
	hint.name = "Hint"
	hint.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	hint.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	hint.set_anchors_preset(Control.PRESET_BOTTOM_WIDE)
	hint.position.y = -44
	hint.add_theme_font_size_override("font_size", 22)
	hint.add_theme_color_override("font_color", UiTheme.TEXT)
	hint.add_theme_color_override("font_outline_color", UiTheme.INK)
	hint.add_theme_constant_override("outline_size", 6)
	add_child(hint)
	auto_button = Button.new()
	auto_button.name = "Auto"
	auto_button.focus_mode = Control.FOCUS_NONE
	auto_button.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	auto_button.set_anchors_preset(Control.PRESET_BOTTOM_LEFT)
	auto_button.position = Vector2(12, -62)
	auto_button.add_theme_font_override("font", UiTheme.font("bold"))
	auto_button.add_theme_font_size_override("font_size", 20)
	for style in ["normal", "hover", "pressed", "focus"]:
		var sb := UiTheme.box(PLATE if style != "hover" else Color(UiTheme.BUTTON_HOVER, 0.92), UiTheme.IRON, 2)
		sb.content_margin_left = 14
		sb.content_margin_right = 14
		sb.content_margin_top = 4
		sb.content_margin_bottom = 4
		auto_button.add_theme_stylebox_override(style, sb)
	auto_button.visible = false
	auto_button.pressed.connect(press.bind("auto"))
	add_child(auto_button)


## Where fighter i's plate is: my team at the top left, the other at the top right, one row
## under the other.
func plate_rect(i: int, view: Vector2) -> Rect2:
	var f: RefCounted = battle.fighters[i]
	var x0 := view.x - 20.0 - BOX_W if f.mirrored() else 20.0
	return Rect2(x0, 14.0 + f.row() * (BOX_H + 12.0), BOX_W, BOX_H)


## The portraits on the plates, each looking towards the other side.
func _show_portraits() -> void:
	for i in 4:
		var f: RefCounted = battle.fighters[i]
		var face := portraits[i]
		face.visible = f.present
		if not f.present:
			continue
		var id := BattleMotion.portrait_of(f)
		face.texture = Pictures.portrait(id)
		# the hero's portraits look to the left, the others to the right
		var looks_left := id >= BattleMotion.HERO_PORTRAIT and id < BattleMotion.HERO_PORTRAIT + 4
		face.flip_h = looks_left != f.mirrored()
		var r := plate_rect(i, hud.size)
		face.position = Vector2(r.end.x - 7.0 - FACE if f.mirrored() else r.position.x + 7.0, r.position.y + 6.0)
		face.modulate = Color(0.55, 0.55, 0.6) if f.hp <= 0 else Color.WHITE


## The fighters' plates, the cards of the actions beside them, the changes of HP over the
## fighters, the quotes.
func draw_hud(layer: Control) -> void:
	if battle == null:
		return
	for i in 4:
		var f: RefCounted = battle.fighters[i]
		if not f.present:
			continue
		var right: bool = f.mirrored()
		var r := plate_rect(i, layer.size)
		var aimed: bool = battle.state == OnlineBattle.TARGET and i == battle.target_cursor
		_plaque(layer, r, UiTheme.HIGHLIGHT if aimed else UiTheme.IRON, 3 if aimed else 2)
		var inner := Rect2(r.position + Vector2(0 if right else FACE + 16.0, 0), Vector2(r.size.x - FACE - 26.0, r.size.y))
		var name: String = f.name if f.alt_name.is_empty() or battle.round_no % 2 == 0 else f.alt_name
		var badge := Vector2(inner.position.x + 22.0 if right else inner.end.x - 12.0, r.position.y + 22.0)
		var name_at := Vector2(inner.end.x if right else inner.position.x, r.position.y + 30.0)
		_text(layer, name, name_at, 22, UiTheme.HIGHLIGHT if aimed else UiTheme.TEXT, 1 if right else -1)
		layer.draw_circle(badge, 14.0, UiTheme.RED, true, -1.0, true)
		layer.draw_arc(badge, 14.0, 0.0, TAU, 32, UiTheme.ACCENT, 2.0, true)
		_text(layer, str(f.level), badge + Vector2(0, 6), 16, UiTheme.TEXT, 0)
		var bars := Rect2(inner.position.x + (10.0 if right else 0.0), 0, inner.size.x - 10.0, 0)
		_bar(layer, Rect2(bars.position.x, r.position.y + 42, bars.size.x, 15), float(f.hp) / maxf(1.0, f.max_hp), HP_FILL, right)
		_bar(layer, Rect2(bars.position.x, r.position.y + 62, bars.size.x, 9), float(f.mp) / 100.0, MP_FILL, right)
		var a: int = battle.card_action(i)
		if a >= 0:
			_card(layer, f, a, Vector2(r.end.x + 10.0 if not right else r.position.x - 10.0 - CARD_W, r.position.y + 17.0))
	for d in battle.damage_shown:
		var p := _screen_point(float(d[0]), float(d[1]), DAMAGE_UP + float(d[2]))
		var text := ("+%d" if int(d[3]) > 0 else "%d") % int(d[3])
		_text(layer, text, p, 44, HEAL if int(d[3]) > 0 else DAMAGE, 0, 8)
	var side: int = battle.quote_side_shown()
	if side >= 0:
		for i in 4:
			if battle.says_quote(i, side):
				var f: RefCounted = battle.fighters[i]
				var q: String = f.quote_win if side == 2 else f.quote_start
				if not q.is_empty():
					var sx: float = (OnlineBattle.W - f.x) if f.mirrored() else f.x
					_quote(layer, q, _screen_point(sx, f.y, QUOTE_UP))


func _screen_point(sx: float, y: float, up_px: float) -> Vector2:
	return camera.unproject_position(world_at(sx, y, up_px))


## A plaque: a dark plate with hard corners and a rim.
static func _plaque(layer: Control, r: Rect2, rim: Color, width: int) -> void:
	var sb := UiTheme.box(PLATE, rim, width)
	sb.shadow_color = Color(0, 0, 0, 0.5)
	sb.shadow_size = 5
	layer.draw_style_box(sb, r)


## A line of text in PT Sans Bold with a dark outline: align -1 from the point, 0 centred on
## it, 1 ending at it (the point is on the baseline).
static func _text(layer: Control, text: String, at: Vector2, px: int, color: Color, align: int, outline := 4,
		ink := UiTheme.INK) -> void:
	var font := UiTheme.font("bold")
	var w := font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, px).x
	var p := at - Vector2(w * (align + 1) / 2.0, 0)
	if outline > 0:
		layer.draw_string_outline(font, p, text, HORIZONTAL_ALIGNMENT_LEFT, -1, px, outline, ink)
	layer.draw_string(font, p, text, HORIZONTAL_ALIGNMENT_LEFT, -1, px, color)


## A bar in a dark hollow with an iron rim, filled from its outer end (a right plate's from the
## right), a light line along the top of the fill.
static func _bar(layer: Control, r: Rect2, part: float, fill: Array, right: bool) -> void:
	var back := UiTheme.box(UiTheme.SLOT, UiTheme.IRON, 1)
	layer.draw_style_box(back, r)
	part = clampf(part, 0.0, 1.0)
	if part <= 0.0:
		return
	var inner := r.grow(-2.0)
	var w := maxf(inner.size.y, inner.size.x * part)
	var at := Vector2(inner.end.x - w if right else inner.position.x, inner.position.y)
	var sb := UiTheme.box(fill[1])
	layer.draw_style_box(sb, Rect2(at, Vector2(w, inner.size.y)))
	var top := UiTheme.box(fill[0])
	layer.draw_style_box(top, Rect2(at, Vector2(w, inner.size.y * 0.62)))
	if w > inner.size.y:
		var shine := inner.size.y * 0.5
		layer.draw_line(at + Vector2(shine, 2.0), at + Vector2(w - shine, 2.0), Color(1, 1, 1, 0.35), 1.5, true)


## A card of the action shown: a parchment plaque with the action's sign and its name; a
## target's card shows how the blow went.
func _card(layer: Control, f: RefCounted, a: int, at: Vector2) -> void:
	var r := Rect2(at, Vector2(CARD_W, 46))
	var sb := UiTheme.box(PAPER, UiTheme.INK, 2)
	sb.shadow_color = Color(0, 0, 0, 0.45)
	sb.shadow_size = 3
	layer.draw_style_box(sb, r)
	var as_target: bool = battle.state == OnlineBattle.TURN and battle.fighters.find(f) != battle.attacker
	var sign := action_icon(a) if not (as_target and a == OnlineBattle.RES_HIT) else null
	if sign != null:
		layer.draw_texture_rect(sign, Rect2(at + Vector2(8, 6), Vector2(34, 34)), false)
	elif as_target:
		_burst(layer, at + Vector2(25, 23), 18.0, UiTheme.RED)  # the blow got through
	var text := action_name(a, as_target)
	layer.draw_string(UiTheme.font("bold"), at + Vector2(52, 30), text, HORIZONTAL_ALIGNMENT_LEFT, CARD_W - 60, 20, UiTheme.INK)


## The sign of an action: the sabre, the shield, the wind, a skill's medallion, the mace of
## auto-battle (a target's card: 2 evaded, the wind).
func action_icon(a: int) -> Texture2D:
	match a:
		0:
			return icon("sabre")
		1:
			return icon("shield")
		2:
			return icon("wind")
		OnlineBattle.AUTO:
			return icon("bulava")
	return ItemSlot.icon("skill", int(SKILL_ICONS[a])) if SKILL_ICONS.has(a) else null


func action_name(a: int, as_target: bool) -> String:
	if as_target:
		return tr("online.battle_hit") if a == OnlineBattle.RES_HIT else tr("online.battle_evaded")
	match a:
		0:
			return tr("online.battle_attack")
		1:
			return tr("online.battle_defend")
		2:
			return tr("online.battle_evade")
		OnlineBattle.AUTO:
			return tr("online.battle_auto")
	return OnlineClient.skill_name(a) if a >= 3 and a <= 13 else ""


## A quote in a parchment bubble over the speaker, its tail pointing down at him.
func _quote(layer: Control, q: String, tip: Vector2) -> void:
	var font := UiTheme.font("text")
	var sz := font.get_string_size(q, HORIZONTAL_ALIGNMENT_LEFT, -1, 24)
	var r := Rect2(tip.x - sz.x / 2.0 - 16.0, tip.y - 58.0, sz.x + 32.0, 44.0)
	r.position.x = clampf(r.position.x, 8.0, layer.size.x - 8.0 - r.size.x)
	var tail := PackedVector2Array([Vector2(tip.x - 10.0, r.end.y - 2.0), Vector2(tip.x + 10.0, r.end.y - 2.0),
		Vector2(tip.x, tip.y)])
	var sb := UiTheme.box(PAPER, UiTheme.INK, 2)
	sb.set_corner_radius_all(4)
	sb.shadow_color = Color(0, 0, 0, 0.45)
	sb.shadow_size = 3
	layer.draw_style_box(sb, r)
	layer.draw_colored_polygon(tail, PAPER)
	layer.draw_polyline(PackedVector2Array([tail[0], tail[2], tail[1]]), UiTheme.INK, 2.0, true)
	layer.draw_string(font, Vector2(r.position.x + 16.0, r.position.y + 30.0), q, HORIZONTAL_ALIGNMENT_LEFT, -1, 24, UiTheme.INK)


## The timing bar: a dark plate, the track from where the cursor starts past the gold mark,
## the run so far filling it from blue to gold, the cursor a bright blade. When it stopped:
## a gold burst on the mark for a perfect stop, Miss past it, else a flash where it stopped.
func draw_bar(layer: Control) -> void:
	if battle == null:
		return
	var s := BAR_SCALE
	_plaque(layer, Rect2(Vector2.ZERO, layer.size), UiTheme.IRON, 2)
	var left := 11.0 * s  # BAR_LEFT inside the plate (it is 110 px wide around CX)
	var mark := left + float(OnlineBattle.MARK - OnlineBattle.BAR_LEFT) * s
	var mid := layer.size.y * 0.52
	var track := Rect2(left - 10.0, mid - 11.0, mark - left + 10.0 * s + 20.0, 22.0)
	var hollow := UiTheme.box(UiTheme.SLOT, UiTheme.IRON, 2)
	layer.draw_style_box(hollow, track)
	var x := left + float(battle.bar_x - OnlineBattle.BAR_LEFT) * s
	var to := clampf(x, left, track.end.x - 4.0)
	if to > left:
		var k := clampf((to - left) / (mark - left), 0.0, 1.0)
		var tip := MP_FILL[0].lerp(UiTheme.ACCENT, k)
		layer.draw_polygon(PackedVector2Array([Vector2(left, mid - 6), Vector2(to, mid - 6), Vector2(to, mid + 6),
			Vector2(left, mid + 6)]), PackedColorArray([MP_FILL[1], tip, tip.darkened(0.25), MP_FILL[1].darkened(0.3)]))
	var to_item := layer.get_canvas_item()
	var pulse := 1.15 if battle.state_ticks % 2 == 0 else 1.0
	UiTheme.rhombus(to_item, Vector2(mark, mid), 19.0 * pulse, UiTheme.INK)
	UiTheme.rhombus(to_item, Vector2(mark, mid), 16.0 * pulse, UiTheme.ACCENT)
	UiTheme.rhombus(to_item, Vector2(mark, mid), 7.0 * pulse, UiTheme.RED)
	var stopped: bool = battle.state == OnlineBattle.SENT and battle.bar_shown
	if stopped and battle.hit_score == 100:
		_burst(layer, Vector2(mark, mid), 44.0, UiTheme.HIGHLIGHT)
		_text(layer, tr("online.battle_perfect"), Vector2(layer.size.x / 2.0, 30.0), 24, UiTheme.HIGHLIGHT, 0)
	elif stopped and battle.hit_score == 20:
		_text(layer, tr("online.battle_miss"), Vector2(layer.size.x / 2.0, 30.0), 24, DAMAGE, 0)
	elif stopped:
		_burst(layer, Vector2(to, mid), 26.0, Color(1, 1, 1, 0.9))
	layer.draw_line(Vector2(to, mid - 22.0), Vector2(to, mid + 22.0), UiTheme.INK, 7.0, true)
	layer.draw_line(Vector2(to, mid - 20.0), Vector2(to, mid + 20.0), Color("efe4c8"), 3.0, true)


## A star of light: eight rays.
static func _burst(layer: Control, c: Vector2, r: float, color: Color) -> void:
	var pts := PackedVector2Array()
	for k in 16:
		var a := k * TAU / 16.0 - PI / 2.0
		pts.append(c + Vector2(cos(a), sin(a)) * (r if k % 2 == 0 else r * 0.38))
	layer.draw_colored_polygon(pts, color)
	layer.draw_circle(c, r * 0.3, Color(1, 1, 1, 0.95), true, -1.0, true)


# --- steps ----------------------------------------------------------------------------------
func _process(delta: float) -> void:
	if battle == null:
		return
	if online != null and online.battle != battle:  # kicked: the account went online elsewhere
		leave()
		return
	_acc += delta * 1000.0
	_clock += delta
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
	_move_fighters(delta)


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
	_show_fighters()
	_show_portraits()
	var st: int = battle.state
	var choosing: bool = st in [OnlineBattle.CHOOSE, OnlineBattle.TARGET] and not battle.exit_prompt
	pad.visible = choosing
	if choosing:
		for k in pad_buttons:
			var b: Button = pad_buttons[k]
			var mine: bool = {"right": 0, "left": 1, "up": 2}.get(k, -1) == battle.chosen_action \
				or (k == "down" and battle.chosen_action >= 3 and battle.chosen_action <= 13)
			b.modulate = Color(1, 0.9, 0.5) if mine else Color.WHITE
			b.disabled = st != OnlineBattle.CHOOSE
		pad_buttons["down"].icon = icon("fire", 52) if battle.any_skill_ready() else _no_skill_icon()
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
			if b.round_no > 0 and b.allies_alive > 0 and b.enemies_alive > 0 and b.fighters[0].hp > 0:
				return tr("online.battle_round") % b.round_no + "\n" + tr("online.battle_waiting") + dots
		OnlineBattle.CHOOSE:
			if b.exit_prompt:
				var secs: int = 15 - b.exit_ticks * OnlineBattle.TIME_MS / 1000
				return tr("online.battle_exit_ask") + "\n" + ("[%s]   %s" if b.exit_cursor == 0 else "%s   [%s]") \
					% [tr("online.yes"), tr("online.no")] + "\n" + tr("online.battle_remain") % secs
		OnlineBattle.SENT:
			if b.state_ticks >= 4:
				return tr("online.battle_waiting") + dots
		OnlineBattle.NO_BATTLE:
			return tr("online.battle_no_battle")
		OnlineBattle.OVER:
			return tr("online.battle_waiting") + dots
		OnlineBattle.STAGE_END:
			return "%s\n%s\n%s" % [b.stage_title, tr("online.battle_stage_n") % b.stage, tr("online.battle_complete")]
		OnlineBattle.RESULT:
			if b.result_shown():
				return result_text()
	return ""


## The rewards of battle_end to the hero, once.
func take_rewards() -> void:
	rewarded = true
	var r: Dictionary = battle.result
	var p: RefCounted = Profile.load_or_new(profile_path)
	p.gold = clampi(int(p.gold) + int(r.get("gold", 0)), 0, 0x7FFFFFFF)
	p.fame = clampi(int(p.fame) + int(r.get("fame", 0)), 0, 0x7FFFFFFF)
	levels_gained = p.gain_exp(int(r.get("exp", 0))) if int(r.get("exp", 0)) > 0 else 0
	var loot: Variant = r.get("loot", {})
	if loot is Dictionary and int((loot as Dictionary).get("id", 0)) > 0:
		var item: Dictionary = (loot as Dictionary).duplicate()
		item.erase("name")
		var id := int(item.id)
		loot_lost = not (p.add_potion(id) if id <= 11 else p.add_item(item))
	p.save(profile_path)


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
		lines.append(tr("online.mission_grade") % OnlineClient.grade(int(r.get("grade", 0))) if b.battle_won == 1
			else tr("online.battle_failed"))
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
## or a tap turns it over, as Tab, F or R3.
func _show_auto() -> void:
	auto_button.visible = battle.state >= OnlineBattle.CHOOSE and battle.state <= OnlineBattle.SENT
	auto_button.text = "AUTO" if battle.auto_battle else InputSetup.hint("online.battle_auto_key")
	var c := AUTO_ON if battle.auto_battle else Color.WHITE
	for k in ["font_color", "font_hover_color", "font_pressed_color", "font_focus_color",
			"font_hover_pressed_color"]:
		auto_button.add_theme_color_override(k, c)


func hint_text() -> String:
	var auto := "   " + tr("online.battle_auto_on") if battle.auto_battle else ""
	match battle.state:
		OnlineBattle.CHOOSE:
			return ("" if battle.exit_prompt else InputSetup.hint("online.battle_hint_choose")) + auto
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
		var img := icon("fire", 52).get_image()
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
			b.pressed.connect(func() -> void:
				battle.skill_cursor = k
				press("fire"))
			skill_list.add_child(b)
			skill_buttons.append(b)
	for k in skill_buttons.size():
		var s := int(battle.skill_slots[k])
		var b := skill_buttons[k]
		b.text = "%s  MP %d" % [OnlineClient.skill_name(s), int(battle.skill_costs[s - 3]) if s - 3 < battle.skill_costs.size() else 0]
		b.disabled = not battle.skill_ready(s)
		b.icon = ItemSlot.icon("skill" if not b.disabled else "skillgray", int(SKILL_ICONS.get(s, -1)))
		b.modulate = Color(1, 0.9, 0.5) if k == battle.skill_cursor else Color.WHITE


# --- keys -----------------------------------------------------------------------------------
func press(k: String) -> void:
	if battle == null:
		return
	battle.key(k)
	_refresh()
	if battle.left:
		leave()


func _unhandled_input(event: InputEvent) -> void:
	if battle == null:
		if event.is_action_pressed("ui_cancel"):
			Router.back()
		return
	var keys := {"ui_up": "up", "ui_down": "down", "ui_left": "left", "ui_right": "right",
		"ui_accept": "fire", "ui_cancel": "back"}
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
	Router.back()
