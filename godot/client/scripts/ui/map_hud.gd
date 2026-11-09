class_name MapHud
extends Control
## The HUD of a mission's map in the new art, laid out on the original 240x320 grid at a
## whole-number scale (so the places to click stay where they were) and drawn smooth: the
## mission clock on a plaque at the top left, the kills (or the last enemy hit: his name, level
## and HP) at the top right, and the panel at the bottom: a dark plate with an iron rim and a
## riveted iron bar, the HP orb (left, blood-red) and the MP orb (right, blue) that empty from
## the top as HP or MP goes, with the value in the middle, and the two potions on the potion
## keys. Above the panel the skill bar (as in pyport): the five belt slots (keys Z X C V B) on
## the left with their counts, the five skills (keys 1-5) on the right, grey when not learned
## or without the MP; the slot in use has a light rim. A click on a slot uses it. Each slot is
## labelled with its key or button for the device just used (scripts/ui/glyphs.gd: Z or the
## d-pad up, 1 or X, a PlayStation shape), and not on touch, where the slots are tapped. With the
## bar the panel does not show the two potions (the belt shows all five). In the bottom-left corner
## AUTO: brass while the auto-hunt is on, grey while off; a click toggles it. While someone talks
## on the map that corner is SKIP (pyport's left soft key): a click skips the talk. In the
## bottom-right corner PAUSE (pyport's soft key): a click pauses the game.
## The icons of the potions and the skills are the new art's (ItemSlot.icon), drawn smooth on
## a layer of their own over the plates, the counts and the keys on a layer over them.

const BALL := 35  # how full an orb is: 0..BALL
const ORB_X := [26, 214]  # the orbs' middles in the 240 px wide panel
const ORB_Y := 33
const ORB_R := 22
const PANEL_H := 61
const ITEM := 28  # a potion on the panel
const CELL := 23  # a slot of the bar: 1 px shared border and a 22 px icon
const ICON := 22  # an icon in a slot of the bar
const BAR_H := 24
const AUTO_W := 48  # the AUTO corner
const AUTO_H := 17
const PAUSE_W := 48  # the PAUSE corner

var sim: RefCounted
var kills_shown := 0  # counts up to the kills one a tick

## The colours of the orbs: [top of the liquid, its bottom].
const HP_LIQUID := [Color("bf3a2e"), Color("4a0f0c")]
const MP_LIQUID := [Color("4f78b0"), Color("101d36")]
const PLATE := Color(0.07, 0.066, 0.062, 0.92)

var _icons: Control  # the icons, drawn smooth
var _labels: Control  # the counts and the keys over them
var show_bar := true
var auto_on := false
var auto_allowed := true  # false on hard: no AUTO corner (screens/mission/mission_screen.gd)


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_preset(Control.PRESET_FULL_RECT)
	_icons = _layer("Icons", CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS, _draw_icons)
	_labels = _layer("Labels", CanvasItem.TEXTURE_FILTER_LINEAR, _draw_labels)


func _layer(layer_name: String, filter: int, drawn: Callable) -> Control:
	var c := Control.new()
	c.name = layer_name
	c.mouse_filter = Control.MOUSE_FILTER_IGNORE
	c.texture_filter = filter
	c.set_anchors_preset(Control.PRESET_FULL_RECT)
	c.draw.connect(drawn)
	add_child(c)
	return c


## The scale of the HUD's grid: as many whole times as 320 rows fit the screen.
func scale_of(view: Vector2) -> float:
	return maxf(1.0, floorf(view.y / 320.0))


## The top of the HUD (its skill bar, or the panel without it) on a screen of this size.
func top_of(view: Vector2) -> float:
	return view.y - (PANEL_H + (BAR_H if show_bar else 0)) * scale_of(view)


func tick() -> void:
	if sim != null and sim.kills > kills_shown:
		kills_shown += 1
	queue_redraw()


func _draw() -> void:
	if _icons != null:
		_icons.queue_redraw()
		_labels.queue_redraw()
	if sim == null:
		return
	var view := get_viewport_rect().size
	var k := scale_of(view)
	# the clock at the top left, the kills or the last enemy hit at the top right
	var seconds: int = sim.play_seconds()
	_plaque(Rect2(Vector2(4, 4) * k, Vector2(58, 20) * k), k)
	_text(
		"%02d:%02d" % [(seconds / 60) % 100, seconds % 60],
		Vector2(33, 19) * k,
		13 * k,
		UiTheme.TEXT,
		k,
		0
	)
	if not sim.target_info.is_empty():
		_target(sim.target_info, view, k)
	else:
		_kills(kills_shown, view, k)
	# the panel at the bottom with the orbs
	var origin := Vector2(view.x / 2.0 - 120.0 * k, view.y - PANEL_H * k)
	_panel(origin, k)
	_orb(
		origin + Vector2(ORB_X[0], ORB_Y) * k,
		ORB_R * k,
		_fill(sim.hero.hp, sim.hero.max_hp),
		HP_LIQUID,
		sim.hero.hp,
		k
	)
	_orb(
		origin + Vector2(ORB_X[1], ORB_Y) * k,
		ORB_R * k,
		_fill(sim.hero.mp, sim.hero.max_mp),
		MP_LIQUID,
		sim.hero.mp,
		k
	)
	if not show_bar:
		for b in 2:
			_socket(_potion_rect(origin, b, k), k, false)
	if talking():
		_corner(
			Rect2(Vector2(0, view.y - AUTO_H * k), Vector2(AUTO_W, AUTO_H) * k),
			"SKIP",
			UiTheme.TEXT,
			k
		)
	elif auto_allowed:
		_auto(view, k)
	_pause(view, k)
	if show_bar:
		_bar(origin + Vector2(0, -BAR_H) * k, k)


## Where the HUD's panel starts and its scale: [origin, k].
func _frame() -> Array:
	var view := get_viewport_rect().size
	var k := scale_of(view)
	return [Vector2(view.x / 2.0 - 120.0 * k, view.y - PANEL_H * k), k]


## The icons: the potions on the panel or the belt and the skills of the bar.
func _draw_icons() -> void:
	if sim == null:
		return
	var f := _frame()
	var origin: Vector2 = f[0]
	var k: float = f[1]
	if not show_bar:
		for b in 2:
			var item := int(sim.quick_slots[sim.quick_keys[b]][0])
			if item != 0:
				_icon("tool", item - 1, _potion_rect(origin, b, k).grow(-2 * k))
		return
	var top := origin + Vector2(0, -BAR_H) * k
	for b in 5:
		var item := int(sim.quick_slots[b][0])
		if item != 0:
			_icon(
				"tool",
				item - 1,
				Rect2(top + Vector2(slot_x(false, b) + 1, 1) * k, Vector2(ICON, ICON) * k)
			)
		var s := int(sim.hotkeys[b])
		if s >= 12 and s <= 30:
			var ready: bool = sim.skill_levels[s - 12] > 0 and sim.skill_mp_need(s) <= sim.hero.mp
			_icon(
				"skill" if ready else "skillgray",
				s - 12,
				Rect2(top + Vector2(slot_x(true, b) + 1, 1) * k, Vector2(ICON, ICON) * k)
			)


func _icon(sheet: String, i: int, r: Rect2) -> void:
	var t := ItemSlot.icon(sheet, i)
	if t != null:
		_icons.draw_texture_rect(t, r, false)


## Over the icons: how many of each potion, the keys of the slots.
func _draw_labels() -> void:
	if sim == null:
		return
	var f := _frame()
	var origin: Vector2 = f[0]
	var k: float = f[1]
	if not show_bar:
		for b in 2:
			var slot: Array = sim.quick_slots[sim.quick_keys[b]]
			if int(slot[0]) == 0:
				continue
			var r := _potion_rect(origin, b, k)
			_text(
				"x%d" % int(slot[1]), r.end - Vector2(2, 3) * k, 10 * k, UiTheme.TEXT, k, 1, _labels
			)
		return
	var top := origin + Vector2(0, -BAR_H) * k
	for b in 5:
		var at := top + Vector2(slot_x(false, b), 0) * k
		var slot: Array = sim.quick_slots[b]
		if int(slot[0]) != 0 and int(slot[1]) > 1:
			_text(
				str(int(slot[1])),
				at + Vector2(CELL - 1, BAR_H - 3) * k,
				10 * k,
				UiTheme.TEXT,
				k,
				1,
				_labels
			)
		_key_label(_label_of("belt_%d" % (b + 1)), at, k)
		_key_label(_label_of("skill_%d" % (b + 1)), top + Vector2(slot_x(true, b), 0) * k, k)


func _auto(view: Vector2, k: float) -> void:
	_corner(
		Rect2(Vector2(0, view.y - AUTO_H * k), Vector2(AUTO_W, AUTO_H) * k),
		"AUTO",
		UiTheme.HIGHLIGHT if auto_on else UiTheme.TEXT_DIM,
		k
	)


func _pause(view: Vector2, k: float) -> void:
	_corner(
		Rect2(Vector2(view.x - PAUSE_W * k, view.y - AUTO_H * k), Vector2(PAUSE_W, AUTO_H) * k),
		"PAUSE",
		UiTheme.TEXT,
		k
	)


## A plaque in a bottom corner with its word in the middle.
func _corner(r: Rect2, text: String, color: Color, k: float) -> void:
	_plaque(Rect2(r.position + Vector2(1, 1) * k, r.size - Vector2(2, 1) * k), k)
	_text(text, Vector2(r.get_center().x, r.end.y - 5 * k), 10 * k, color, k, 0)


## Is the point on the PAUSE corner?
func pause_at(p: Vector2) -> bool:
	var view := get_viewport_rect().size
	var k := scale_of(view)
	return p.x >= view.x - PAUSE_W * k and p.y >= view.y - AUTO_H * k


## Is the point on the rows of the panel at the bottom?
func panel_at(p: Vector2) -> bool:
	var view := get_viewport_rect().size
	return p.y >= view.y - PANEL_H * scale_of(view)


## Someone talks on the map (the general who comes, his words after the fight).
func talking() -> bool:
	return sim != null and not sim.talk.is_empty()


func _left_corner_at(p: Vector2) -> bool:
	var view := get_viewport_rect().size
	var k := scale_of(view)
	return p.x < AUTO_W * k and p.y >= view.y - AUTO_H * k


## Is the point on the AUTO corner (not while someone talks: then it is SKIP)?
func auto_at(p: Vector2) -> bool:
	return auto_allowed and not talking() and _left_corner_at(p)


## Is the point on the SKIP corner of a talk?
func skip_at(p: Vector2) -> bool:
	return talking() and _left_corner_at(p)


## The x of slot i of the belt (left) or the skills (right) in the 240 px panel.
static func slot_x(skill: bool, i: int) -> int:
	return (240 - CELL * 5 - 1 if skill else 0) + i * CELL


## The bar's slots: a dark hollow each (the icons and the keys: their layers).
func _bar(top: Vector2, k: float) -> void:
	for b in 5:
		_socket(
			Rect2(top + Vector2(slot_x(false, b), 0) * k, Vector2(CELL + 1, BAR_H) * k).grow(
				-0.5 * k
			),
			k,
			sim.effect_item != 0 and sim.effect_slot == b
		)
		var s := int(sim.hotkeys[b])
		_socket(
			Rect2(top + Vector2(slot_x(true, b), 0) * k, Vector2(CELL + 1, BAR_H) * k).grow(
				-0.5 * k
			),
			k,
			s != 0 and sim.hero.action == s
		)


## The label of an action's slot for the device just used.
static func _label_of(action: String) -> Dictionary:
	return Glyphs.short_of(action, InputSetup.device, InputSetup.pad_brand)


## A slot's key in its top-left corner (Glyphs.short_of), in brass outlined in ink: a word, a
## small d-pad with the arm to press lit, or a PlayStation button's shape; nothing for {}.
func _key_label(label: Dictionary, at: Vector2, k: float) -> void:
	if label.has("shape"):
		_shape(str(label.shape), at + Vector2(5.5, 5.5) * k, 3.0 * k)
	elif label.has("dpad"):
		_dpad(label.dpad, at + Vector2(6.5, 6.5) * k, 5.0 * k)
	elif label.has("text"):
		_text(str(label.text), at + Vector2(2.5, 8.5) * k, 8 * k, UiTheme.ACCENT, k, -1, _labels)


## A small d-pad of half-width r around c, outlined in ink: dark iron, the arm towards `dir` brass.
func _dpad(dir: Vector2, c: Vector2, r: float) -> void:
	var a := maxf(1.0, r * 0.36)  # half an arm's width
	var bars := [
		Rect2(c - Vector2(r, a), Vector2(r, a) * 2), Rect2(c - Vector2(a, r), Vector2(a, r) * 2)
	]
	for b: Rect2 in bars:
		_labels.draw_rect(b.grow(maxf(1.0, r / 6.0)), UiTheme.INK)
	for b: Rect2 in bars:
		_labels.draw_rect(b, UiTheme.IRON)
	var side := Vector2(-dir.y, dir.x)
	_labels.draw_rect(
		Rect2(c + side * a + dir * a, Vector2.ZERO).expand(c - side * a + dir * r), UiTheme.ACCENT
	)


## A PlayStation face button's sign of radius r around c, in brass outlined in ink.
func _shape(shape: String, c: Vector2, r: float) -> void:
	var w := maxf(1.5, r / 2.5)
	for stroke in [[UiTheme.INK, w + 2.0], [UiTheme.ACCENT, w]]:
		var color: Color = stroke[0]
		var width: float = stroke[1]
		match shape:
			"cross":
				for d in [Vector2(1, 1), Vector2(1, -1)]:
					_labels.draw_line(c - d * r, c + d * r, color, width, true)
			"circle":
				_labels.draw_arc(c, r, 0, TAU, 16, color, width, true)
			"square":
				_labels.draw_rect(Rect2(c - Vector2(r, r), Vector2(r, r) * 2), color, false, width)
			"triangle":
				_labels.draw_polyline(
					PackedVector2Array(
						[
							c + Vector2(0, -r),
							c + Vector2(r, r * 0.8),
							c + Vector2(-r, r * 0.8),
							c + Vector2(0, -r)
						]
					),
					color,
					width,
					true
				)


## The bar's slot under a point of the screen: ["belt", 0..4], ["skill", 0..4], or [].
func slot_at(p: Vector2) -> Array:
	if not show_bar or sim == null:
		return []
	var view := get_viewport_rect().size
	var k := scale_of(view)
	var top := view.y - (PANEL_H + BAR_H) * k
	if p.y < top or p.y >= top + BAR_H * k:
		return []
	var x := (p.x - (view.x / 2.0 - 120.0 * k)) / k
	for b in 5:
		for skill in [false, true]:
			if x >= slot_x(skill, b) and x < slot_x(skill, b) + CELL + 1:
				return ["skill" if skill else "belt", b]
	return []


## How much of a ball (0..35) is full; a little is always seen while anything is left.
static func _fill(v: int, most: int) -> int:
	var f := BALL * v / maxi(most, 1)
	return maxi(f, 3) if f != 0 else 0


## A plaque: a dark plate with hard corners and a thin iron rim.
func _plaque(r: Rect2, k: float) -> void:
	var sb := UiTheme.box(PLATE, UiTheme.IRON, maxi(1, int(k)))
	sb.set_corner_radius_all(int(k))
	draw_style_box(sb, r)


## A dark hollow for an icon; the one in use has a light rim.
func _socket(r: Rect2, k: float, hot: bool) -> void:
	var sb := UiTheme.box(
		Color(UiTheme.SLOT, 0.88),
		UiTheme.HIGHLIGHT if hot else UiTheme.SLOT_RIM,
		int(2 * k) if hot else maxi(1, int(k / 2))
	)
	sb.set_corner_radius_all(int(k))
	draw_style_box(sb, r)


## Where potion b (0 left, 1 right) sits on the panel when there is no bar.
static func _potion_rect(origin: Vector2, b: int, k: float) -> Rect2:
	return Rect2(origin + Vector2(64 if b == 0 else 148, 15) * k, Vector2(ITEM, ITEM) * k)


## The panel: a dark plate with an iron rim along its top and a riveted iron bar between the orbs.
func _panel(origin: Vector2, k: float) -> void:
	var plate := UiTheme.box(PLATE, UiTheme.IRON, int(1.5 * k))
	plate.corner_radius_top_left = int(3 * k)
	plate.corner_radius_top_right = int(3 * k)
	plate.corner_radius_bottom_left = 0
	plate.corner_radius_bottom_right = 0
	plate.border_width_bottom = 0
	draw_style_box(plate, Rect2(origin + Vector2(0, 3) * k, Vector2(240, PANEL_H - 3) * k))
	var line := Color(UiTheme.IRON_LIGHT, 0.4)
	for y in [12.0, 54.0]:
		draw_line(origin + Vector2(52, y) * k, origin + Vector2(188, y) * k, line, k, true)
	var to := get_canvas_item()
	var reach := 4 if show_bar else 1  # without the bar the potions sit on it
	var bar := Rect2(
		origin + Vector2(120 - reach * 15 - 6, 29) * k, Vector2(reach * 30 + 12, 8) * k
	)
	var iron := UiTheme.box(UiTheme.IRON.darkened(0.45), UiTheme.INK, maxi(1, int(k / 2)))
	iron.set_corner_radius_all(int(k))
	draw_style_box(iron, bar)
	draw_line(
		bar.position + Vector2(k, k),
		Vector2(bar.end.x - k, bar.position.y + k),
		Color(UiTheme.IRON_LIGHT, 0.5),
		k,
		true
	)
	for i in range(-reach, reach + 1):
		var c := origin + Vector2(120 + i * 15, 33) * k
		if i == 0:
			UiTheme.rhombus(to, c, 6.5 * k, UiTheme.INK)
			UiTheme.rhombus(to, c, 5.5 * k, UiTheme.ACCENT_DARK)
			UiTheme.rhombus(to, c, 2.5 * k, UiTheme.RED)
		else:
			UiTheme.rivet(to, c, 2.6 * k)
	for side in [-1, 1]:
		UiTheme.rivet(to, origin + Vector2(120 + side * 66, 12) * k, 1.8 * k)
		UiTheme.rivet(to, origin + Vector2(120 + side * 66, 54) * k, 1.8 * k)


## An orb of glass: the liquid up to fill (0..BALL) with a light surface, the value in the
## middle, a shine on the glass and an iron rim.
func _orb(c: Vector2, r: float, fill: int, liquid: Array, value: int, k: float) -> void:
	draw_circle(c, r + 2.5 * k, UiTheme.INK, true, -1.0, true)
	draw_circle(c, r, UiTheme.SLOT, true, -1.0, true)
	var f := float(fill) / float(BALL)
	if f > 0.0:
		var s := clampf(1.0 - 2.0 * f, -1.0, 1.0)
		var a0 := asin(s)
		var points := PackedVector2Array()
		var colors := PackedColorArray()
		var n := 32
		for i in n + 1:
			var t := lerpf(a0, PI - a0, float(i) / float(n))
			var p := c + Vector2(cos(t), sin(t)) * (r - 0.5 * k)
			points.append(p)
			colors.append(
				(liquid[0] as Color).lerp(
					liquid[1], clampf((p.y - (c.y - r)) / (2.0 * r), 0.0, 1.0)
				)
			)
		draw_polygon(points, colors)
		if f < 0.98:
			var half := sqrt(maxf(0.0, 1.0 - s * s)) * (r - 0.5 * k)
			var y := c.y + s * r
			draw_line(
				Vector2(c.x - half, y),
				Vector2(c.x + half, y),
				(liquid[0] as Color).lightened(0.35),
				1.2 * k,
				true
			)
	# the glass: a dark ring inside the rim, a shine at the upper left
	draw_arc(c, r - 1.5 * k, 0.0, TAU, 48, Color(0, 0, 0, 0.35), 3.0 * k, true)
	var shine := PackedVector2Array()
	for i in 13:
		var t := lerpf(PI * 1.02, PI * 1.5, i / 12.0)
		shine.append(c + Vector2(cos(t), sin(t)) * r * 0.84)
	for i in 13:
		var t := lerpf(PI * 1.5, PI * 1.02, i / 12.0)
		shine.append(c + Vector2(0.1, 0.12) * r + Vector2(cos(t), sin(t)) * r * 0.76)
	draw_colored_polygon(shine, Color(1, 1, 1, 0.2))
	draw_circle(c + Vector2(-0.38, -0.52) * r, r * 0.07, Color(1, 1, 1, 0.45), true, -1.0, true)
	draw_arc(c, r + 0.8 * k, 0.0, TAU, 64, UiTheme.IRON_LIGHT, 2.2 * k, true)
	_text(str(value), c + Vector2(0, 4.5 * k), 12 * k, UiTheme.TEXT, k, 0)


## A line of text in PT Sans Bold with a dark outline: align -1 from the point, 0 centred on
## it, 1 ending at it (the point is on the baseline).
func _text(
	text: String,
	at: Vector2,
	size: float,
	color: Color,
	k: float,
	align: int,
	on: CanvasItem = self
) -> void:
	var font := UiTheme.font("bold")
	var px := int(size)
	var w := font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, px).x
	var p := at - Vector2(w * (align + 1) / 2.0, 0)
	on.draw_string_outline(
		font, p, text, HORIZONTAL_ALIGNMENT_LEFT, -1, px, maxi(2, int(2 * k)), UiTheme.INK
	)
	on.draw_string(font, p, text, HORIZONTAL_ALIGNMENT_LEFT, -1, px, color)


## The kills on a plaque at the top right, after two crossed sabres.
func _kills(value: int, view: Vector2, k: float) -> void:
	var r := Rect2(Vector2(view.x - 62 * k, 4 * k), Vector2(58, 20) * k)
	_plaque(r, k)
	var c := r.position + Vector2(11, 10) * k
	for side in [-1.0, 1.0]:
		var tip := c + Vector2(side * 6, -6) * k
		var hilt := c + Vector2(-side * 5, 5) * k
		draw_line(hilt, tip, UiTheme.TEXT, 1.6 * k, true)
		draw_line(
			hilt + Vector2(side * 2.2, 0.6) * k,
			hilt + Vector2(side * 0.2, -2.6) * k,
			UiTheme.ACCENT,
			1.4 * k,
			true
		)
	_text(str(value), Vector2(r.end.x - 6 * k, r.position.y + 15 * k), 13 * k, UiTheme.TEXT, k, 1)


## The last enemy hit: his name, his level on a cinnabar badge and his HP bar, in place of the
## kills.
func _target(t: Dictionary, view: Vector2, k: float) -> void:
	var font := UiTheme.font("bold")
	var label := tr(str(t.get("name", "")))
	var w := font.get_string_size(label, HORIZONTAL_ALIGNMENT_LEFT, -1, int(11 * k)).x / k
	var width := maxf(86.0, w + 30.0)
	var r := Rect2(Vector2(view.x - (width + 4) * k, 4 * k), Vector2(width, 30) * k)
	_plaque(r, k)
	_text(label, r.position + Vector2(6, 13) * k, 11 * k, UiTheme.TEXT, k, -1)
	var badge := Vector2(r.end.x - 11 * k, r.position.y + 10 * k)
	draw_circle(badge, 7.5 * k, UiTheme.RED, true, -1.0, true)
	draw_arc(badge, 7.5 * k, 0.0, TAU, 32, UiTheme.ACCENT, 1.4 * k, true)
	_text(str(int(t.get("level", 1))), badge + Vector2(0, 3.5 * k), 9 * k, UiTheme.TEXT, k, 0)
	var track := Rect2(r.position + Vector2(6, 20) * k, Vector2(width - 12, 6) * k)
	var back := UiTheme.box(UiTheme.SLOT, UiTheme.IRON, maxi(1, int(k / 2)))
	back.set_corner_radius_all(int(k))
	draw_style_box(back, track)
	var bar := clampi(int(t.get("hp_bar", 0)), 0, 62)
	if bar > 0:
		var fill := UiTheme.box(HP_LIQUID[0])
		fill.set_corner_radius_all(int(k))
		fill.border_blend = false
		var inner := track.grow(-1 * k)
		draw_style_box(
			fill, Rect2(inner.position, Vector2(inner.size.x * bar / 62.0, inner.size.y))
		)
		draw_rect(
			Rect2(
				inner.position + Vector2(1, 0.6) * k,
				Vector2(inner.size.x * bar / 62.0 - 2 * k, 1.2 * k)
			),
			Color(1, 0.6, 0.5, 0.45)
		)
