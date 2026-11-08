extends Control
## The multiplayer battle in 2.5D, as the rest of the game: the original background as a 3D
## stage, the fighters as flat sprites standing on it (assets/original/mp, made by
## godot/tools/import_original.py export_mp), and the HUD drawn over it. What happens is scripts/net/online_battle.gd, one step every TICK_MS; this screen
## shows it and passes the keys: arrows choose (Right Attack, Left Defend, Up Evade, Down a
## skill), Enter / Space confirms and stops the timing bar, Esc asks to leave the battle, Tab,
## F, the pad's Back (the "auto" action, as auto-hunt on the map) or a click on AUTO in the
## bottom-left corner turn auto-battle on and off. The pad's
## buttons, the skills and the bar take the mouse too. The hint at the bottom names the keys of
## the device just used (InputSetup.hint: the keyboard's or the pad's).
## What the battle earned goes to the hero as soon as the result comes: gold, fame, exp (a
## level maybe), the loot into the backpack (a potion onto the belt).
## Router.params: online (the client, tests), profile_path (tests); the battle is the
## client's `battle`.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const OnlineClient := preload("res://scripts/net/online_client.gd")
const OnlineBattle := preload("res://scripts/net/online_battle.gd")
const MapBuilder := preload("res://scripts/world/map_builder.gd")
const Profile := preload("res://scripts/core/profile.gd")
const MP := "res://assets/original/mp/"
## World units per original pixel: one 27 px map tile is one unit, as on the map.
const PX := 1.0 / 27.0
## The original screen's ground line where the fighters of a 1-on-1 stand.
const GROUND_Y := 225
const BACKDROP_Z := -3.4
const BACKDROP_TILES := 7  # the original's screen (240 px) side by side, the middle one behind the fighters
const BACKDROP_SCALE := 1.0  # its pixels as big as the fighters'
const SKY_ABOVE := 120  # more sky over the original's, for the camera's wider view
const GROUND_NEAR := 5.0  # where the ground strip ends towards the camera
const HUD_SCALE := 3.0
const BAR_SCALE := 4.0
const FRONT_DY := [3, 8, -8, 16]
## The change of HP shows this much higher than on the original screen (the fighters are
## drawn from their feet up there; here the number rises over the head).
const DAMAGE_UP := 10.0
const QUOTE_UP := 46.0
const MARKER_UP := 50.0
## The rows of a 2-on-2 stand apart in depth; seen from the camera the back one would hide
## behind the front one, so the farther a fighter stands the farther out from the middle it
## is drawn (by this part of its distance from the middle per pixel of depth).
const SPREAD := 0.016
const PAD_BUTTON := 84
const BOX_W := 360.0  # a fighter's box at the top; the card of its action beside it
const CARD_W := 220.0
const SKY := [Color8(171, 199, 255), Color8(25, 29, 66)]  # day, night
const HP_COLORS := [Color8(181, 0, 0), Color8(255, 0, 0)]
const MP_COLORS := [Color8(49, 48, 123), Color8(140, 162, 222)]
const ORANGE := Color8(250, 64, 0)
const GREEN := Color8(65, 255, 65)

var online: RefCounted
var battle: RefCounted
var profile_path: String = Profile.PATH
var rewarded := false  # the result's rewards went to the hero
var levels_gained := 0
var loot_lost := false  # no room for it
var info := {}
var viewport: SubViewport
var camera: Camera3D
var stage: Node3D
var backdrop: MeshInstance3D
var ground: MeshInstance3D
var bodies: Array[Node3D] = []
var sprites: Array[Sprite3D] = []
var auras: Array[Sprite3D] = []
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
var _tex := {}
var _acc := 0.0
var _bg_shown := -1
var _sound_player: AudioStreamPlayer


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
	var f := FileAccess.open(OnlineBattle.DATA, FileAccess.READ)
	if f != null:
		info = JSON.parse_string(f.get_as_text())
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


func tex(name: String) -> Texture2D:
	if not _tex.has(name):
		var path := MP + name + ".png"
		_tex[name] = load(path) if ResourceLoader.exists(path) else null
	return _tex[name]


# --- the stage ------------------------------------------------------------------------------
func _build_world() -> void:
	var container := SubViewportContainer.new()
	container.name = "World"
	container.stretch = true
	container.set_anchors_preset(Control.PRESET_FULL_RECT)
	container.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(container)
	viewport = SubViewport.new()
	viewport.own_world_3d = true
	viewport.msaa_3d = Viewport.MSAA_2X
	container.add_child(viewport)
	stage = Node3D.new()
	stage.name = "Stage"
	viewport.add_child(stage)
	MapBuilder.add_environment(stage)
	camera = Camera3D.new()
	camera.name = "Camera"
	camera.fov = 32.0
	camera.position = Vector3(0, 2.6, 10.5)
	stage.add_child(camera)
	camera.look_at(Vector3(0, 1.1, 0))
	backdrop = MeshInstance3D.new()
	backdrop.name = "Backdrop"
	stage.add_child(backdrop)
	ground = MeshInstance3D.new()
	ground.name = "Ground"
	stage.add_child(ground)
	for i in 4:
		var body := Node3D.new()
		body.name = "Fighter%d" % i
		stage.add_child(body)
		var s := Sprite3D.new()
		s.name = "Sprite"
		s.region_enabled = true
		s.pixel_size = PX
		s.billboard = BaseMaterial3D.BILLBOARD_FIXED_Y
		s.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
		s.alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
		s.shaded = false
		s.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
		body.add_child(s)
		var aura := Sprite3D.new()
		aura.name = "Aura"
		aura.region_enabled = true
		aura.pixel_size = PX
		aura.billboard = BaseMaterial3D.BILLBOARD_FIXED_Y
		aura.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
		aura.shaded = false
		aura.render_priority = 1
		aura.visible = false
		body.add_child(aura)
		bodies.append(body)
		sprites.append(s)
		auras.append(aura)
	marker = Sprite3D.new()
	marker.name = "Target"
	marker.texture = tex("ui48")
	marker.pixel_size = PX
	marker.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	marker.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	marker.shaded = false
	marker.no_depth_test = true
	marker.visible = false
	stage.add_child(marker)


## The original's background for bg: bits 6-7 the sky (day, night),
## 4-5 the ground, 0-1 the scenery in front. The sky and the scenery become one picture far
## back, BACKDROP_TILES of the original's screen side by side (the sun over the middle one),
## with more sky over it; the ground strip, as wide, is the floor from there to the camera.
func show_background(bg: int) -> void:
	_bg_shown = bg
	var sky := (bg >> 6) & 3
	var ground_kind := (bg >> 4) & 3
	var front := bg & 3
	var w := 240 * BACKDROP_TILES
	var horizon := SKY_ABOVE + 160 - 95
	var h := horizon + 83
	var img := Image.create(w, h, false, Image.FORMAT_RGBA8)
	img.fill(SKY[1 if sky == 1 else 0])
	var pieces := [4, 5, 6, 7, 8] if sky != 1 else [9, 10, 11, 12, 13]
	var cloud_a := _image("gamebg%d" % pieces[0])
	var cloud_b := _image("gamebg%d" % pieces[1])
	for x in range(0, w, 30):
		_blend(img, cloud_a, x, horizon)
		_blend(img, cloud_b, x, horizon + 30)
	var sun := _image("gamebg%d" % pieces[2])
	if sun != null:
		_blend(img, sun, (BACKDROP_TILES / 2) * 240 + 150 - sun.get_width(), horizon - 2 - sun.get_height())
	for t in BACKDROP_TILES:
		_blend(img, _image("gamebg%d" % pieces[3]), t * 240 + 18, horizon - 30)
		_blend(img, _image("gamebg%d" % pieces[4]), t * 240 + 52, horizon - 15)
	var scenery := _image("gamebg%d" % front)
	for t in BACKDROP_TILES:
		_blend(img, scenery, t * 240, horizon + int(FRONT_DY[front]))
	var px := PX * BACKDROP_SCALE
	var quad := QuadMesh.new()
	quad.size = Vector2(w, h) * px
	backdrop.mesh = quad
	backdrop.position = Vector3(0, quad.size.y / 2.0, BACKDROP_Z)
	backdrop.material_override = _flat_material(ImageTexture.create_from_image(img))
	var strip := _image("gamebg%d" % (14 + ground_kind))
	var floor_img := Image.create(w, strip.get_height(), false, Image.FORMAT_RGBA8)
	for x in range(0, w, 30):
		_blend(floor_img, strip, x, 0)
	# the strip from the backdrop's foot to GROUND_NEAR, its last row on to the camera
	var depth := camera.position.z + 2.0 - BACKDROP_Z
	var floor_mesh := PlaneMesh.new()
	floor_mesh.size = Vector2(w * px, depth)
	ground.mesh = floor_mesh
	ground.position = Vector3(0, 0, BACKDROP_Z + depth / 2.0)
	var m := _flat_material(ImageTexture.create_from_image(floor_img))
	m.uv1_scale = Vector3(1, depth / (GROUND_NEAR - BACKDROP_Z), 1)
	m.texture_repeat = false
	ground.material_override = m


func _image(name: String) -> Image:
	var t := tex(name)
	if t == null:
		return null
	var img := t.get_image()
	if img.is_compressed():
		img.decompress()
	img.convert(Image.FORMAT_RGBA8)
	return img


static func _blend(dst: Image, src: Image, x: int, y: int) -> void:
	if src != null:
		dst.blend_rect(src, Rect2i(Vector2i.ZERO, src.get_size()), Vector2i(x, y))


static func _flat_material(t: Texture2D) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_texture = t
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	return m


## Where a fighter's feet are: the original's (x, y), with a leap's height kept apart.
static func world_at(sx: float, gy: float, lift: float) -> Vector3:
	var out := 1.0 + (GROUND_Y - gy) * SPREAD
	return Vector3((sx - OnlineBattle.CX) * out * PX, lift * PX, (gy - GROUND_Y) * PX)


func _show_fighters() -> void:
	var cell: Array = info.get("cell", [172, 124])
	var origin: Array = info.get("origin", [86, 112])
	var mcell: Array = info.get("monster_cell", [120, 56])
	var morigin: Array = info.get("monster_origin", [60, 44])
	var firsts: Array = info.get("set_first_cell", [0, 19, 66])
	var cols := int(info.get("columns", 16))
	for i in 4:
		var f: RefCounted = battle.fighters[i]
		bodies[i].visible = f.present
		if not f.present:
			continue
		var s := sprites[i]
		var c: Array = cell
		var o: Array = origin
		var index := 0
		if f.kind == OnlineBattle.MONSTER:
			s.texture = tex("monster_r")
			c = mcell
			o = morigin
			index = f.frame % 100
		else:
			var head: int = f.face if f.kind == OnlineBattle.PLAYER else 0
			s.texture = tex("fighter_%d_%d_%s" % [head, f.weapon, "r" if f.mirrored() else "l"])
			var pose := mini(f.frame / 100, 2)
			index = int(firsts[pose]) + f.frame % 100
		s.region_rect = Rect2((index % cols) * int(c[0]), (index / cols) * int(c[1]), int(c[0]), int(c[1]))
		# the cell's middle over the feet (the cells are as wide on both sides of them)
		s.position = Vector3(0, (float(o[1]) - float(c[1]) / 2.0) * PX, 0)
		var sx: float = (OnlineBattle.W - f.x) if f.mirrored() else f.x
		bodies[i].position = world_at(sx, f.y + f.lift, f.lift)
		var aura := auras[i]
		aura.visible = f.status in [11, 12, 13] and battle.state != OnlineBattle.RESULT
		if aura.visible:
			var k: int = (f.status - 11) * 2 + battle.state_ticks % 2
			var sc: Array = info.get("status_cell", [39, 15])
			var pt: Array = info.get("status_points", [[19, 14]])[k]
			aura.texture = tex("status_%s" % ("r" if f.mirrored() else "l"))
			aura.region_rect = Rect2(k * int(sc[0]), 0, int(sc[0]), int(sc[1]))
			var ax: float = (int(sc[0]) - int(pt[0])) if f.mirrored() else int(pt[0])
			aura.position = Vector3((float(sc[0]) / 2.0 - ax) * PX, (float(pt[1]) - float(sc[1]) / 2.0) * PX, 0.01)
	marker.visible = false
	if battle.state == OnlineBattle.TARGET and battle.state_ticks % 2 == 0:
		var t: RefCounted = battle.fighters[battle.target_cursor]
		if t.present:
			marker.visible = true
			marker.position = bodies[battle.target_cursor].position + Vector3(0, MARKER_UP * PX, 0)


# --- the HUD --------------------------------------------------------------------------------
func _build_hud() -> void:
	hud = Layer.new()
	hud.name = "Hud"
	hud.screen = self
	hud.what = "hud"
	hud.set_anchors_preset(Control.PRESET_FULL_RECT)
	hud.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(hud)
	center = PanelContainer.new()
	center.name = "Center"
	center.add_theme_stylebox_override("panel", UiTheme.box(Color(0.1, 0.09, 0.13, 0.86), UiTheme.ACCENT, 2))
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
	pad.position = Vector2(-1.5 * PAD_BUTTON, -60 - 3 * PAD_BUTTON)
	add_child(pad)
	# the original's pad: Evade up, Defend left, Attack right, a skill down
	var u := float(PAD_BUTTON)
	for k in [["up", "ui17", Vector2(u, 0)], ["left", "ui16", Vector2(0, u)],
			["right", "ui15", Vector2(2 * u, u)], ["down", "ui18", Vector2(u, 2 * u)]]:
		var b := Button.new()
		b.name = str(k[0]).capitalize()
		b.icon = tex(k[1])
		b.expand_icon = true
		b.custom_minimum_size = Vector2(PAD_BUTTON, PAD_BUTTON)
		b.size = Vector2(PAD_BUTTON, PAD_BUTTON)
		b.position = k[2]
		for style in ["normal", "hover", "pressed", "disabled", "focus"]:
			var sb: StyleBoxFlat = get_theme_stylebox(style, "Button").duplicate() as StyleBoxFlat
			if sb != null:
				sb.set_content_margin_all(6)
				b.add_theme_stylebox_override(style, sb)
		b.focus_mode = Control.FOCUS_NONE
		b.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		b.pressed.connect(press.bind(k[0]))
		pad.add_child(b)
		pad_buttons[k[0]] = b
	countdown = Label.new()
	countdown.name = "Countdown"
	countdown.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	countdown.add_theme_font_size_override("font_size", 48)
	countdown.add_theme_color_override("font_color", UiTheme.ACCENT)
	countdown.position = Vector2(3 * PAD_BUTTON + 16, PAD_BUTTON + 10)
	pad.add_child(countdown)
	skill_list = VBoxContainer.new()
	skill_list.name = "Skills"
	skill_list.set_anchors_preset(Control.PRESET_CENTER)
	skill_list.position = Vector2(-180, -200)
	skill_list.custom_minimum_size = Vector2(360, 0)
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
	hint.add_theme_color_override("font_color", UiTheme.TEXT_DIM)
	add_child(hint)
	auto_button = Button.new()
	auto_button.name = "Auto"
	auto_button.flat = true
	auto_button.focus_mode = Control.FOCUS_NONE
	auto_button.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	auto_button.set_anchors_preset(Control.PRESET_BOTTOM_LEFT)
	auto_button.position = Vector2(12, -60)
	auto_button.add_theme_font_size_override("font_size", 22)
	auto_button.visible = false
	auto_button.pressed.connect(press.bind("auto"))
	add_child(auto_button)


## The fighters' boxes: my team at the top left, the
## other at the top right, one row under the other; the cards of the actions beside them; the
## changes of HP over the fighters; the quotes.
func draw_hud(layer: Control) -> void:
	if battle == null:
		return
	var font := layer.get_theme_default_font()
	for i in 4:
		var f: RefCounted = battle.fighters[i]
		if not f.present:
			continue
		var right: bool = f.mirrored()
		var w := BOX_W
		var x0 := layer.size.x - 24.0 - w if right else 24.0
		var y0: float = 16.0 + f.row() * 92.0
		layer.draw_rect(Rect2(x0, y0, w, 74), Color(0, 0, 0, 0.55))
		var face_w := 0.0
		if f.kind == OnlineBattle.PLAYER and tex("face%d" % f.face) != null:
			var ft := tex("face%d" % f.face)
			var half := Rect2(0 if not right else ft.get_width() / 2.0, 0, ft.get_width() / 2.0, ft.get_height())
			var fw := half.size.x * HUD_SCALE
			var fx := x0 + 6 if not right else x0 + w - 6 - fw
			layer.draw_texture_rect_region(ft, Rect2(fx, y0 + 6, fw, half.size.y * HUD_SCALE), half)
			face_w = fw + 8
		var name: String = f.name if f.alt_name.is_empty() or battle.round_no % 2 == 0 else f.alt_name
		var label := "%s  Lv%d" % [name, f.level]
		var tx := x0 + 8 + face_w if not right else x0 + w - 8 - face_w - font.get_string_size(label, HORIZONTAL_ALIGNMENT_LEFT, -1, 24).x
		var col := ORANGE if battle.state == OnlineBattle.TARGET and i == battle.target_cursor else UiTheme.TEXT
		layer.draw_string(font, Vector2(tx, y0 + 30), label, HORIZONTAL_ALIGNMENT_LEFT, -1, 24, col)
		_bar(layer, Rect2(x0 + 8, y0 + 42, w - 16, 12), float(f.hp) / maxf(1.0, f.max_hp), HP_COLORS, right)
		_bar(layer, Rect2(x0 + 8, y0 + 58, w - 16, 8), float(f.mp) / 100.0, MP_COLORS, right)
		var a: int = battle.card_action(i)
		if a >= 0:
			_card(layer, font, f, a, Vector2(x0 + w + 8 if not right else x0 - 8 - CARD_W, y0 + 17))
	for d in battle.damage_shown:
		var p := _screen_point(float(d[0]), float(d[1]), DAMAGE_UP + float(d[2]))
		var text := ("+%d" if int(d[3]) > 0 else "%d") % int(d[3])
		var c := GREEN if int(d[3]) > 0 else Color(1, 0.25, 0.2)
		var sz := font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, 40)
		layer.draw_string_outline(font, p - Vector2(sz.x / 2, 0), text, HORIZONTAL_ALIGNMENT_LEFT, -1, 40, 6, Color.BLACK)
		layer.draw_string(font, p - Vector2(sz.x / 2, 0), text, HORIZONTAL_ALIGNMENT_LEFT, -1, 40, c)
	var side: int = battle.quote_side_shown()
	if side >= 0:
		for i in 4:
			if battle.says_quote(i, side):
				var f: RefCounted = battle.fighters[i]
				var q: String = f.quote_win if side == 2 else f.quote_start
				if q.is_empty():
					continue
				var sx: float = (OnlineBattle.W - f.x) if f.mirrored() else f.x
				var p := _screen_point(sx, f.y, QUOTE_UP)
				var sz := font.get_string_size(q, HORIZONTAL_ALIGNMENT_LEFT, -1, 26)
				var r := Rect2(p.x - sz.x / 2 - 12, p.y - 40, sz.x + 24, 44)
				layer.draw_rect(r, Color(1, 1, 1, 0.92))
				layer.draw_rect(r, Color.BLACK, false, 2.0)
				layer.draw_string(font, Vector2(r.position.x + 12, r.position.y + 31), q, HORIZONTAL_ALIGNMENT_LEFT, -1, 26, Color.BLACK)


func _screen_point(sx: float, y: float, up_px: float) -> Vector2:
	return camera.unproject_position(world_at(sx, y, up_px))


static func _bar(layer: Control, r: Rect2, part: float, colors: Array, right: bool) -> void:
	layer.draw_rect(r, Color(0.25, 0.25, 0.25))
	var w := r.size.x * clampf(part, 0.0, 1.0)
	if w <= 0.0:
		return
	if part > 0.0 and w < 2.0:
		w = 2.0
	var x := r.position.x + (r.size.x - w if right else 0.0)
	layer.draw_rect(Rect2(x, r.position.y, w, r.size.y), colors[1])
	layer.draw_rect(Rect2(x, r.position.y, w, 2), colors[0])
	layer.draw_rect(Rect2(x, r.position.y + r.size.y - 2, w, 2), colors[0])


## A card of the action shown: the action's mark and its name; a
## target's card shows how the blow went.
func _card(layer: Control, font: Font, f: RefCounted, a: int, at: Vector2) -> void:
	var r := Rect2(at, Vector2(CARD_W, 40))
	layer.draw_rect(r, Color8(255, 227, 198))
	layer.draw_rect(r, Color.BLACK, false, 2.0)
	var icon := tex("act%d" % (2 + mini(a, 3)))
	if icon != null:
		layer.draw_texture_rect(icon, Rect2(at + Vector2(6, 6), icon.get_size() * 2.6), false)
	var text := action_name(a, battle.state == OnlineBattle.TURN and battle.fighters.find(f) != battle.attacker)
	layer.draw_string(font, at + Vector2(80, 29), text, HORIZONTAL_ALIGNMENT_LEFT, CARD_W - 84, 22, Color.BLACK)


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


## The timing bar, BAR_SCALE times the original.
func draw_bar(layer: Control) -> void:
	if battle == null:
		return
	var s := BAR_SCALE
	var dx: Array = info.get("ui_dx", [])
	var dy: Array = info.get("ui_dy", [])
	var left := 11.0  # BAR_LEFT inside the box (the box is 110 px wide around CX)
	var mid := 15.0  # the bar's line inside the box
	layer.draw_rect(Rect2(Vector2.ZERO, layer.size), Color(0, 0, 0, 0.7))
	layer.draw_rect(Rect2(Vector2.ZERO, layer.size), UiTheme.ACCENT, false, 2.0)
	for k in [35, 36, 37]:
		var t := tex("ui%d" % k)
		if t != null:
			layer.draw_texture_rect(t, Rect2(Vector2(left + int(dx[k]), mid + int(dy[k])) * s, t.get_size() * s), false)
	var mark := 72.0
	if battle.state == OnlineBattle.SENT and battle.bar_shown:
		var shown := ""
		if battle.hit_score == 100:
			shown = "ui52"
		elif battle.hit_score == 20:
			shown = "ui53"
		var t := tex(shown) if not shown.is_empty() else tex("ui49")
		var at := Vector2(left + mark + int(dx[52 if shown == "ui52" else 53]), mid + int(dy[52 if shown == "ui52" else 53]))
		if shown.is_empty():
			var dx2: Array = info.get("ui_dx2", [])
			var dy2: Array = info.get("ui_dy2", [])
			at = Vector2(left + battle.bar_x - OnlineBattle.BAR_LEFT - 20 + int(dx2[35]), mid - 11 + int(dy2[35]))
		if t != null:
			layer.draw_texture_rect(t, Rect2(at * s, t.get_size() * s), false)
	if battle.state_ticks % 2 == 0:
		var m := tex("ui38")
		if m != null:
			layer.draw_texture_rect(m, Rect2(Vector2(left + mark + int(dx[38]), mid + int(dy[38])) * s, m.get_size() * s), false)
	var c := tex("ui34")
	if c != null:
		var x: float = left + battle.bar_x - OnlineBattle.BAR_LEFT + int(dx[34])
		layer.draw_texture_rect(c, Rect2(Vector2(x, mid + int(dy[34])) * s, c.get_size() * s), false)


# --- steps ----------------------------------------------------------------------------------
func _process(delta: float) -> void:
	if battle == null:
		return
	if online != null and online.battle != battle:  # kicked: the account went online elsewhere
		leave()
		return
	_acc += delta * 1000.0
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
		pad_buttons["down"].icon = tex("ui18" if battle.any_skill_ready() else "ui19")
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


## pyport's AUTO in the bottom-left corner while the actions are chosen: orange AUTO while
## auto-battle is on, white with its keys while it is off (named for the device in use). A click
## or a tap turns it over, as Tab, F or the pad's Back.
func _show_auto() -> void:
	auto_button.visible = battle.state >= OnlineBattle.CHOOSE and battle.state <= OnlineBattle.SENT
	auto_button.text = "AUTO" if battle.auto_battle else InputSetup.hint("online.battle_auto_key")
	var c := ORANGE if battle.auto_battle else Color.WHITE
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


## No line of control hints under this screen: it shows its own (scripts/ui/hint_bar.gd).
func controls_hint() -> String:
	return ""
