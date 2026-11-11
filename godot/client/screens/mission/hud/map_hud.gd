class_name MapHud
extends Control
## The HUD of a mission's map (map_hud.tscn), laid out on the original 240x320 grid at a
## whole-number scale: the mission clock on a plaque at the top left, the kills (or the last
## enemy hit: his name, his level on a badge and his HP bar) at the top right, and at the bottom
## the skill bar over the panel with the HP orb (left) and the MP orb (right, HudOrb). The bar
## has the five belt slots (keys Z X C V B) on the left with their counts and the five skills
## (keys 1-5) on the right, grey when not learned or without the MP; each slot (HudSlot) is
## labelled with its key or button for the device just used (scripts/ui/glyphs.gd), and not on
## touch, where the slots are tapped. In the bottom-left corner AUTO: brass while the auto-hunt
## is on, grey while off, none on hard; while someone talks on the map that corner is SKIP. In
## the bottom-right corner PAUSE.
## The slots and the corners are buttons: a click or a tap on one is a signal of the HUD, and the
## mission screen acts on it.
## The scene is laid out for a screen of 720 rows (the grid twice); on another scale its places,
## its fonts and the rims of its theme grow or shrink with the grid (_fit).

signal belt_pressed(slot: int)
signal skill_pressed(slot: int)
signal auto_pressed
signal skip_pressed
signal pause_pressed

const PANEL_H := 61  # the panel's rows on the 240x320 grid
const BAR_H := 24  # the skill bar's rows above the panel
const LAID_OUT := 2.0  # the scale of the grid the scene is laid out at
const SABRES_BOX := 12.0  # the crossed sabres before the kills, on the grid
const BADGE_BOX := 17.0  # the badge of the last enemy's level, on the grid
const TARGET_MIN := 86.0  # the plaque of the last enemy hit at its narrowest, on the grid
const TARGET_ROOM := 30.0  # its room beside the name: the margins and the badge, on the grid

var sim: MapSim
var kills_shown := 0  # counts up to the kills one a tick
var auto_on := false
var auto_allowed := true  # false on hard: no AUTO corner (screens/mission/mission_screen.gd)

var _scale := LAID_OUT
var _laid_out_theme: Theme
var _laid_out := {}  # Control -> its offsets at LAID_OUT: [left, top, right, bottom]

@onready var _time: Label = %Time
@onready var _kills: Control = %Kills
@onready var _sabres: Control = %Sabres
@onready var _kill_count: Label = %KillCount
@onready var _target: Control = %Target
@onready var _target_name: Label = %TargetName
@onready var _badge: Control = %Badge
@onready var _target_level: Label = %TargetLevel
@onready var _target_hp: ProgressBar = %TargetHp
@onready var _target_shine: ProgressBar = %Shine  # a light stripe along the top of the HP
@onready var _hp: HudOrb = %HpOrb
@onready var _mp: HudOrb = %MpOrb
@onready var _belt: Array[HudSlot] = [%Belt1, %Belt2, %Belt3, %Belt4, %Belt5]
@onready var _skills: Array[HudSlot] = [%Skill1, %Skill2, %Skill3, %Skill4, %Skill5]
@onready var _auto: Button = %Auto
@onready var _skip: Button = %Skip
@onready var _pause: Button = %Pause


func _ready() -> void:
	UiTheme.font("bold")  # with its Cyrillic letters: the names of the enemies
	_laid_out_theme = theme
	for c: Control in find_children("*", "Control", true, false):
		_laid_out[c] = [c.offset_left, c.offset_top, c.offset_right, c.offset_bottom]
	for i in 5:
		_belt[i].pressed.connect(belt_pressed.emit.bind(i))
		_skills[i].pressed.connect(skill_pressed.emit.bind(i))
	_auto.pressed.connect(auto_pressed.emit)
	_skip.pressed.connect(skip_pressed.emit)
	_pause.pressed.connect(pause_pressed.emit)
	_sabres.draw.connect(_draw_sabres)
	_badge.draw.connect(_draw_badge)
	_target_hp.share(_target_shine)
	resized.connect(_fit)
	_fit()
	refresh()


## The scale of the HUD's grid: as many whole times as 320 rows fit the screen.
static func scale_of(view: Vector2) -> float:
	return maxf(1.0, floorf(view.y / 320.0))


## The top of the HUD (its skill bar) on a screen of this size.
static func top_of(view: Vector2) -> float:
	return view.y - (PANEL_H + BAR_H) * scale_of(view)


## The label of an action's slot for the device just used.
static func _label_of(action: String) -> Dictionary:
	return Glyphs.short_of(action, InputSetup.device, InputSetup.pad_brand)


## The theme laid out at one scale, at f times it: its font sizes, outlines, rims, corners and
## margins.
static func _scaled_theme(laid_out: Theme, f: float) -> Theme:
	var t: Theme = laid_out.duplicate()
	for type in t.get_type_list():
		for item in t.get_font_size_list(type):
			t.set_font_size(item, type, roundi(t.get_font_size(item, type) * f))
		for item in t.get_constant_list(type):
			t.set_constant(item, type, roundi(t.get_constant(item, type) * f))
		for item in t.get_stylebox_list(type):
			var box: StyleBox = t.get_stylebox(item, type).duplicate()
			for side in [SIDE_LEFT, SIDE_TOP, SIDE_RIGHT, SIDE_BOTTOM]:
				if box.get_content_margin(side) > 0.0:
					box.set_content_margin(side, box.get_content_margin(side) * f)
			if box is StyleBoxFlat:
				_scale_flat(box as StyleBoxFlat, f)
			t.set_stylebox(item, type, box)
	return t


## A flat box's rims (at least a pixel), corners and expanded margins at f times.
static func _scale_flat(box: StyleBoxFlat, f: float) -> void:
	for side in [SIDE_LEFT, SIDE_TOP, SIDE_RIGHT, SIDE_BOTTOM]:
		var w := box.get_border_width(side)
		box.set_border_width(side, maxi(1, int(w * f)) if w > 0 else 0)
		box.set_expand_margin(side, box.get_expand_margin(side) * f)
	for corner in [CORNER_TOP_LEFT, CORNER_TOP_RIGHT, CORNER_BOTTOM_RIGHT, CORNER_BOTTOM_LEFT]:
		box.set_corner_radius(corner, int(box.get_corner_radius(corner) * f))


func tick() -> void:
	if sim != null and sim.kills > kills_shown:
		kills_shown += 1
	refresh()


## Shows the state of the mission: the clock, the kills or the last enemy hit, the orbs, the
## slots, and the corner's AUTO or SKIP.
func refresh() -> void:
	if sim == null:
		return
	var seconds: int = sim.play_seconds()
	_time.text = "%02d:%02d" % [(seconds / 60) % 100, seconds % 60]
	_show_target(sim.target_info)
	_hp.show_value(sim.hero.hp, sim.hero.max_hp)
	_mp.show_value(sim.hero.mp, sim.hero.max_mp)
	for b in 5:
		var item := int(sim.quick_slots[b][0])
		_belt[b].show_item(
			ItemSlot.icon("tool", item - 1) if item != 0 else null,
			int(sim.quick_slots[b][1]) if item != 0 else 0,
			sim.effect_item != 0 and sim.effect_slot == b
		)
		_belt[b].show_key(_label_of("belt_%d" % (b + 1)))
		var s := int(sim.hotkeys[b])
		_skills[b].show_item(_skill_icon(s), 0, s != 0 and sim.hero.action == s)
		_skills[b].show_key(_label_of("skill_%d" % (b + 1)))
	_skip.visible = talking()
	_auto.visible = auto_allowed and not talking()
	_auto.set_pressed_no_signal(auto_on)


## Someone talks on the map (the general who comes, his words after the fight).
func talking() -> bool:
	return sim != null and not sim.talk.is_empty()


## Is the point on the rows of the panel or on a slot of the bar? Dragging over them does not
## turn the hero.
func covers(p: Vector2) -> bool:
	var view := get_viewport_rect().size
	if p.y >= view.y - PANEL_H * scale_of(view):
		return true
	for slot: HudSlot in _belt + _skills:
		if slot.get_global_rect().has_point(p):
			return true
	return false


## The scene is laid out at LAID_OUT; on a screen of another scale its places and its theme grow
## or shrink with the grid.
func _fit() -> void:
	var k := scale_of(get_viewport_rect().size)
	if k == _scale:
		return
	_scale = k
	var f := k / LAID_OUT
	theme = _laid_out_theme if f == 1.0 else _scaled_theme(_laid_out_theme, f)
	for c: Control in _laid_out:
		var o: Array = _laid_out[c]
		c.offset_left = o[0] * f
		c.offset_top = o[1] * f
		c.offset_right = o[2] * f
		c.offset_bottom = o[3] * f


## The kills, or in their place the last enemy hit: his name, his level and his HP bar.
func _show_target(t: Dictionary) -> void:
	_kills.visible = t.is_empty()
	_target.visible = not t.is_empty()
	if t.is_empty():
		_kill_count.text = str(kills_shown)
		return
	var title := tr(str(t.get("name", "")))
	_target_name.text = title
	_target_level.text = str(int(t.get("level", 1)))
	_target_hp.value = int(t.get("hp_bar", 0))
	var w := (
		_target_name
		. get_theme_font("font")
		. get_string_size(
			title, HORIZONTAL_ALIGNMENT_LEFT, -1, _target_name.get_theme_font_size("font_size")
		)
		. x
	)
	_target.offset_left = (
		_target.offset_right - maxf(TARGET_MIN * _scale, w + TARGET_ROOM * _scale)
	)


func _skill_icon(s: int) -> Texture2D:
	if s < 12 or s > 30:
		return null
	var ready: bool = sim.skill_levels[s - 12] > 0 and sim.skill_mp_need(s) <= sim.hero.mp
	return ItemSlot.icon("skill" if ready else "skillgray", s - 12)


## Two crossed sabres, before the kills.
func _draw_sabres() -> void:
	var k := _sabres.size.x / SABRES_BOX
	var c := _sabres.size / 2.0
	for side in [-1.0, 1.0]:
		var tip := c + Vector2(side * 6, -6) * k
		var hilt := c + Vector2(-side * 5, 5) * k
		_sabres.draw_line(hilt, tip, UiTheme.TEXT, 1.6 * k, true)
		_sabres.draw_line(
			hilt + Vector2(side * 2.2, 0.6) * k,
			hilt + Vector2(side * 0.2, -2.6) * k,
			UiTheme.ACCENT,
			1.4 * k,
			true
		)


## A cinnabar badge with a brass rim, under the last enemy's level.
func _draw_badge() -> void:
	var k := _badge.size.x / BADGE_BOX
	var c := _badge.size / 2.0
	_badge.draw_circle(c, 7.5 * k, UiTheme.RED, true, -1.0, true)
	_badge.draw_arc(c, 7.5 * k, 0.0, TAU, 32, UiTheme.ACCENT, 1.4 * k, true)
