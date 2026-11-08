extends Control
## The HUD of a mission's map, drawn from the original 240x320 pictures at a whole-number
## scale: the bars at the top with the mission clock (left) and the kills or the last enemy
## hit (right), and the panel at the bottom with the HP ball (left), the MP ball (right) and
## the two potions on the potion keys. A ball empties from the top as HP or MP goes.
## Above the panel the skill bar (as in pyport): the five belt slots (keys Z X C V B) on the
## left with their counts, the five skills (keys 1-5) on the right, grey when not learned
## or without the MP; the slot in use is framed white. A click on a slot uses it. Each slot is
## labelled with its key or button for the device just used (scripts/ui/glyphs.gd: Z or the
## d-pad up, 1 or X, a PlayStation shape), and not on touch, where the slots are tapped.
## With the bar the panel does not show the two potions (the belt shows all five). In the
## bottom-left corner AUTO: white while the auto-hunt is on, grey while off; a click toggles
## it. While someone talks on the map that corner is SKIP (pyport's left soft key): a click
## skips the talk. In the bottom-right corner PAUSE (pyport's soft key): a click pauses the game.

const Glyphs := preload("res://scripts/ui/glyphs.gd")
const UI := "res://assets/original/ui/"
const BALL := 35  # the balls' size
const BALL_X := [4, 201]  # in the 240 px wide panel
const PANEL_H := 61
const TOP_Y := 16  # the clock and the kills, below the top bars
const ITEM := 28  # a frame of tool.png
const CELL := 23  # a slot of the bar: 1 px shared border and a 22 px icon
const ICON := 22  # the middle of a 28 px icon
const BAR_H := 24
const AUTO_W := 48  # the AUTO corner
const AUTO_H := 17
const PAUSE_W := 48  # the PAUSE corner

var sim: RefCounted
var kills_shown := 0  # counts up to the kills one a tick

var _box_top: Texture2D = preload(UI + "box_01.png")
var _box_top_r: Texture2D = preload(UI + "box_01_R.png")
var _panel: Texture2D = preload(UI + "box_02.png")
var _panel_r: Texture2D = preload(UI + "box_02R.png")
var _cover: Texture2D = preload(UI + "ball_black.png")
var _digits: Texture2D = preload(UI + "number1.png")
var _small: Texture2D = preload(UI + "number2.png")
var _items: Texture2D = preload(UI + "tool.png")
var _skills: Texture2D = preload(UI + "skill.png")
var _skills_gray: Texture2D = preload(UI + "skillgray.png")
var show_bar := true
var auto_on := false
var auto_allowed := true  # false on hard: no AUTO corner (scripts/screens/mission_screen.gd)


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	set_anchors_preset(Control.PRESET_FULL_RECT)


## The scale of the original pixels: as many whole times as 320 rows fit the screen.
func scale_of(view: Vector2) -> float:
	return maxf(1.0, floorf(view.y / 320.0))


func tick() -> void:
	if sim != null and sim.kills > kills_shown:
		kills_shown += 1
	queue_redraw()


func _draw() -> void:
	if sim == null:
		return
	var view := get_viewport_rect().size
	var k := scale_of(view)
	# the top bars at the corners
	_put(_box_top, Vector2(0, 2 * k), k)
	_put(_box_top_r, Vector2(view.x - _box_top_r.get_width() * k, 2 * k), k)
	var seconds: int = sim.play_seconds()
	_clock(seconds, Vector2(11 * k, (TOP_Y + 5) * k), k)
	if not sim.target_info.is_empty():
		_target(sim.target_info, view, k)
	else:
		_number(kills_shown, Vector2(view.x - 12 * k, (TOP_Y + 5) * k), k)
	# the panel at the bottom: two halves around the middle
	var origin := Vector2(view.x / 2.0 - 120.0 * k, view.y - PANEL_H * k)
	_put(_panel, origin, k)
	_put(_panel_r, origin + Vector2(120 * k, 0), k)
	var fill := [_fill(sim.hero.hp, sim.hero.max_hp), _fill(sim.hero.mp, sim.hero.max_mp)]
	for b in 2:
		var h: int = BALL - int(fill[b])
		if h > 0:
			draw_texture_rect_region(_cover, Rect2(origin + Vector2(BALL_X[b], 0) * k,
				Vector2(BALL, h) * k), Rect2(0, 0, BALL, h))
	if talking():
		_corner(Rect2(Vector2(0, view.y - AUTO_H * k), Vector2(AUTO_W, AUTO_H) * k), "SKIP", Color.WHITE, k)
	elif auto_allowed:
		_auto(view, k)
	_pause(view, k)
	if show_bar:
		_bar(origin + Vector2(0, -BAR_H) * k, k)
		return
	for b in 2:
		var slot: Array = sim.quick_slots[sim.quick_keys[b]]
		var item := int(slot[0])
		if item == 0:
			continue
		var side := 2 * b - 1
		var p := origin + Vector2(120 + side * (44 + 28 * (1 - b)), PANEL_H - 50) * k
		draw_texture_rect_region(_items, Rect2(p, Vector2(ITEM, ITEM) * k),
			Rect2((item - 1) * ITEM, 0, ITEM, ITEM))
		p = origin + Vector2(120 + side * (38 + 11 * (1 - b)), PANEL_H - 33) * k
		draw_texture_rect_region(_small, Rect2(p, Vector2(11, 12) * k), Rect2(98, 0, 11, 12))
		_number(int(slot[1]), origin + Vector2(120 + side * (28 + 10 * b), PANEL_H - 35) * k, k)


func _auto(view: Vector2, k: float) -> void:
	_corner(Rect2(Vector2(0, view.y - AUTO_H * k), Vector2(AUTO_W, AUTO_H) * k), "AUTO",
		Color.WHITE if auto_on else Color8(120, 120, 120), k)


func _pause(view: Vector2, k: float) -> void:
	_corner(Rect2(Vector2(view.x - PAUSE_W * k, view.y - AUTO_H * k), Vector2(PAUSE_W, AUTO_H) * k),
		"PAUSE", Color.WHITE, k)


## A black corner with its word in the middle.
func _corner(r: Rect2, text: String, color: Color, k: float) -> void:
	draw_rect(r, Color.BLACK)
	var font := get_theme_default_font()
	var size := int(12 * k)
	var w := font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, size).x
	draw_string(font, Vector2(r.position.x + (r.size.x - w) / 2.0, r.end.y - 4 * k), text,
		HORIZONTAL_ALIGNMENT_LEFT, -1, size, color)


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


func _bar(top: Vector2, k: float) -> void:
	draw_rect(Rect2(top, Vector2(240, BAR_H) * k), Color.BLACK)
	for b in 5:
		var at := top + Vector2(slot_x(false, b), 0) * k
		var slot: Array = sim.quick_slots[b]
		_slot_box(at, k, sim.effect_item != 0 and sim.effect_slot == b)
		var item := int(slot[0])
		if item != 0:
			draw_texture_rect_region(_items, Rect2(at + Vector2(1, 1) * k, Vector2(ICON, ICON) * k),
				Rect2((item - 1) * ITEM + 3, 3, ICON, ICON))
			if int(slot[1]) > 1:
				draw_texture_rect_region(_small, Rect2(at + Vector2(CELL - 9, BAR_H - 13) * k,
					Vector2(9, 12) * k), Rect2(int(slot[1]) * 9, 0, 9, 12))
		_key_label(_label_of("belt_%d" % (b + 1)), at, k)
	for b in 5:
		var at := top + Vector2(slot_x(true, b), 0) * k
		var s := int(sim.hotkeys[b])
		_slot_box(at, k, s != 0 and sim.hero.action == s)
		if s >= 12 and s <= 30:
			var ready: bool = sim.skill_levels[s - 12] > 0 and sim.skill_mp_need(s) <= sim.hero.mp
			draw_texture_rect_region(_skills if ready else _skills_gray,
				Rect2(at + Vector2(1, 1) * k, Vector2(ICON, ICON) * k), Rect2((s - 12) * ITEM + 3, 3, ICON, ICON))
		_key_label(_label_of("skill_%d" % (b + 1)), at, k)


func _slot_box(at: Vector2, k: float, hot: bool) -> void:
	draw_rect(Rect2(at, Vector2(CELL + 1, BAR_H) * k), Color.WHITE if hot else Color8(90, 90, 90), false, k)


## The label of an action's slot for the device just used.
static func _label_of(action: String) -> Dictionary:
	return Glyphs.short_of(action, InputSetup.device, InputSetup.pad_brand)


## A slot's key in its top-left corner (Glyphs.short_of): a word, a small d-pad with the arm to
## press lit, or a PlayStation button's shape; nothing for {}.
func _key_label(label: Dictionary, at: Vector2, k: float) -> void:
	var p := at + Vector2(2, 9) * k
	if label.has("shape"):
		_shape(str(label.shape), at + Vector2(5.5, 5.5) * k, 3.0 * k)
		return
	if label.has("dpad"):
		_dpad(label.dpad, at + Vector2(6.5, 6.5) * k, 5.0 * k)
		return
	if not label.has("text"):
		return
	var font := get_theme_default_font()
	var text := str(label.text)
	draw_string_outline(font, p, text, HORIZONTAL_ALIGNMENT_LEFT, -1, int(9 * k), int(k), Color.BLACK)
	draw_string(font, p, text, HORIZONTAL_ALIGNMENT_LEFT, -1, int(9 * k), Color.WHITE)


## A small d-pad of half-width r around c, outlined black: grey, the arm towards `dir` white.
func _dpad(dir: Vector2, c: Vector2, r: float) -> void:
	var a := maxf(1.0, r * 0.36)  # half an arm's width
	var bars := [Rect2(c - Vector2(r, a), Vector2(r, a) * 2), Rect2(c - Vector2(a, r), Vector2(a, r) * 2)]
	for b: Rect2 in bars:
		draw_rect(b.grow(maxf(1.0, r / 6.0)), Color.BLACK)
	for b: Rect2 in bars:
		draw_rect(b, Color8(90, 90, 90))
	var side := Vector2(-dir.y, dir.x)
	draw_rect(Rect2(c + side * a + dir * a, Vector2.ZERO).expand(c - side * a + dir * r), Color.WHITE)


## A PlayStation face button's sign, white on black, of radius r around c.
func _shape(shape: String, c: Vector2, r: float) -> void:
	var w := maxf(1.5, r / 2.5)
	match shape:
		"cross":
			for d in [Vector2(1, 1), Vector2(1, -1)]:
				draw_line(c - d * r, c + d * r, Color.BLACK, w + 2)
			for d in [Vector2(1, 1), Vector2(1, -1)]:
				draw_line(c - d * r, c + d * r, Color.WHITE, w)
		"circle":
			draw_arc(c, r, 0, TAU, 16, Color.BLACK, w + 2)
			draw_arc(c, r, 0, TAU, 16, Color.WHITE, w)
		"square":
			var box := Rect2(c - Vector2(r, r), Vector2(r, r) * 2)
			draw_rect(box, Color.BLACK, false, w + 2)
			draw_rect(box, Color.WHITE, false, w)
		"triangle":
			var pts := PackedVector2Array([c + Vector2(0, -r), c + Vector2(r, r * 0.8),
				c + Vector2(-r, r * 0.8), c + Vector2(0, -r)])
			draw_polyline(pts, Color.BLACK, w + 2)
			draw_polyline(pts, Color.WHITE, w)


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


func _put(tex: Texture2D, at: Vector2, k: float) -> void:
	draw_texture_rect(tex, Rect2(at, tex.get_size() * k), false)


## A number, its last digit ending at `right`, a comma before every third digit.
func _number(value: int, right: Vector2, k: float) -> void:
	var x := right.x
	var n := 0
	while true:
		if n != 0 and n % 3 == 0:
			x -= 4 * k
			draw_texture_rect_region(_digits, Rect2(Vector2(x, right.y), Vector2(5, 14) * k), Rect2(100, 0, 5, 14))
		x -= 10 * k
		draw_texture_rect_region(_digits, Rect2(Vector2(x, right.y), Vector2(10, 14) * k),
			Rect2((value % 10) * 10, 0, 10, 14))
		n += 1
		value /= 10
		if value <= 0:
			break


## The mission clock mm:ss.
func _clock(secs: int, at: Vector2, k: float) -> void:
	var xs := [0, 9, 25, 34]
	var ds := [(secs / 600) % 10, (secs / 60) % 10, (secs % 60) / 10, secs % 10]
	for i in 4:
		draw_texture_rect_region(_digits, Rect2(at + Vector2(xs[i], 0) * k, Vector2(10, 14) * k),
			Rect2(int(ds[i]) * 10, 0, 10, 14))
	draw_texture_rect_region(_digits, Rect2(at + Vector2(20, 0) * k, Vector2(4, 14) * k), Rect2(115, 0, 4, 14))


## The last enemy hit: his name, level and HP bar in place of the kills.
func _target(t: Dictionary, view: Vector2, k: float) -> void:
	var font := get_theme_default_font()
	var font_size := int(12 * k)
	var label := tr(str(t.get("name", "")))
	var w := font.get_string_size(label, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x
	var top := TOP_Y * k
	draw_string_outline(font, Vector2(view.x - 8 * k - w, top + 11 * k), label,
		HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, int(k), Color.BLACK)
	draw_string(font, Vector2(view.x - 8 * k - w, top + 11 * k), label,
		HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, Color.WHITE)
	_small_number(int(t.get("level", 1)), Vector2(view.x - 6 * k, top + 15 * k), k)
	var bar := int(t.get("hp_bar", 0))
	if bar > 0:
		var r := Rect2(Vector2(view.x - 82 * k, top + 17 * k), Vector2(mini(bar, 62), 7) * k)
		draw_rect(r, Color8(0, 0, 0))
		r = Rect2(r.position + Vector2(1, 1) * k, r.size - Vector2(2, 2) * k)
		draw_rect(r, Color8(107, 0, 0))
		r = Rect2(r.position + Vector2(0, 1) * k, Vector2(r.size.x, 3 * k))
		draw_rect(r, Color8(181, 0, 0))
		r = Rect2(r.position + Vector2(0, 1) * k, Vector2(r.size.x, k))
		draw_rect(r, Color8(255, 73, 0))


func _small_number(value: int, right: Vector2, k: float) -> void:
	var x := right.x
	while true:
		x -= 9 * k
		draw_texture_rect_region(_small, Rect2(Vector2(x, right.y), Vector2(9, 12) * k),
			Rect2((value % 10) * 9, 0, 9, 12))
		value /= 10
		if value <= 0:
			break
