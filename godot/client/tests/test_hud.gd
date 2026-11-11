extends "res://tests/test_case.gd"
## The HUD of a mission's map (screens/mission/hud/map_hud.tscn): its labels, its orbs and its
## buttons.

const HUD := preload("res://screens/mission/hud/map_hud.tscn")


func _hud(sim: MapSim) -> MapHud:
	var hud: MapHud = HUD.instantiate()
	hud.sim = sim
	root.add_child(hud)
	return hud


## A left click at a point of the screen, as the window sends it: pressed, then let go.
func _click(at: Vector2) -> void:
	for pressed in [true, false]:
		var ev := InputEventMouseButton.new()
		ev.button_index = MOUSE_BUTTON_LEFT
		ev.pressed = pressed
		ev.position = at
		root.get_viewport().push_input(ev, true)  # in the viewport's own pixels


func test_ball_fill() -> void:
	eq(HudOrb.level(30, 30), 35, "full")
	eq(HudOrb.level(0, 30), 0, "empty")
	eq(HudOrb.level(1, 30), 3, "a little is always seen")
	eq(HudOrb.level(15, 30), 17, "half")


func test_scale() -> void:
	eq(MapHud.scale_of(Vector2(1280, 720)), 2.0, "720 rows: twice")
	eq(MapHud.scale_of(Vector2(240, 320)), 1.0, "the original size")


func test_clock_and_kills() -> void:
	var sim := MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	sim.no_enemies = true
	for t in 200:
		sim.tick(-1, -1, sim.banner != 0)
	check(sim.play_seconds() > 0, "the clock runs: %d s" % sim.play_seconds())
	var hud := _hud(sim)
	sim.kills = 2
	hud.tick()
	eq(hud.kills_shown, 1, "the kills count up one a tick")
	eq((hud.get_node("%KillCount") as Label).text, "1", "and show it")
	hud.tick()
	hud.tick()
	eq(hud.kills_shown, 2, "up to the kills")
	eq(
		(hud.get_node("%Time") as Label).text,
		"%02d:%02d" % [sim.play_seconds() / 60, sim.play_seconds() % 60],
		"the clock"
	)
	eq((hud.get_node("%HpOrb/%Value") as Label).text, str(sim.hero.hp), "the HP in its orb")
	hud.free()


func test_the_last_enemy_hit_in_place_of_the_kills() -> void:
	var sim := MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	var hud := _hud(sim)
	sim.target_info = {"name": "Swords", "level": 2, "hp_bar": 31}
	hud.refresh()
	check(not (hud.get_node("%Kills") as Control).visible, "no kills")
	var target := hud.get_node("%Target") as Control
	check(target.visible, "the enemy")
	eq((hud.get_node("%TargetLevel") as Label).text, "2", "his level")
	eq((hud.get_node("%TargetHp") as ProgressBar).value, 31.0, "his HP bar")
	check(target.size.x >= 86 * 2, "at least as wide as the kills: %s" % target.size.x)
	hud.free()


func test_skill_bar_slots() -> void:
	var hud := _hud(MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2)))
	var got: Array = []
	hud.belt_pressed.connect(func(i: int) -> void: got.append(["belt", i]))
	hud.skill_pressed.connect(func(i: int) -> void: got.append(["skill", i]))
	var view := hud.get_viewport_rect().size
	var k := MapHud.scale_of(view)
	var y := view.y - (MapHud.PANEL_H + MapHud.BAR_H / 2) * k
	var left := view.x / 2.0 - 120.0 * k  # the bar: 23 px a slot, the skills from x 124
	_click(Vector2(left + 5 * k, y))
	eq(got, [["belt", 0]], "Z")
	got.clear()
	_click(Vector2(left + (124 + 2 * 23 + 5) * k, y))
	eq(got, [["skill", 2]], "the third skill")
	got.clear()
	_click(Vector2(view.x / 2.0, y))
	eq(got, [], "the gap between")
	_click(Vector2(left + 5 * k, y - 40 * k))
	eq(got, [], "above the bar")
	check(hud.covers(Vector2(left + 5 * k, y)), "a slot is the HUD's")
	check(hud.covers(Vector2(view.x / 2.0, view.y - 4)), "the panel too")
	check(not hud.covers(Vector2(view.x / 2.0, y)), "not the gap between")
	hud.free()


## The corners: AUTO lit while the auto-hunt is on, none on hard, SKIP while someone talks.
func test_corners() -> void:
	var sim := MapSim.new(MapBuilder.load_map(1), 0, Vector2i(4, 2))
	var hud := _hud(sim)
	var auto := hud.get_node("%Auto") as Button
	var skip := hud.get_node("%Skip") as Button
	check(auto.visible and not auto.button_pressed and not skip.visible, "AUTO, off")
	hud.auto_on = true
	hud.refresh()
	check(auto.button_pressed, "AUTO on: lit")
	MapTalks.start_general_talk(sim, 5, 0)
	hud.refresh()
	check(skip.visible and not auto.visible, "SKIP while a general talks")
	sim.talk.clear()
	hud.auto_allowed = false
	hud.refresh()
	check(not auto.visible and not skip.visible, "hard: no AUTO")
	check((hud.get_node("%Pause") as Button).visible, "PAUSE always")
	hud.free()


## The blinking arrow down to the next room sits above the HUD, not under it.
func test_the_exit_arrow_down_shows_above_the_hud() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = Router.make(Router.SCREENS["mission"])
	root.add_child(screen)
	screen.exit_arrows.show_exits(screen.sim, screen.ways_out, true)
	var view: Vector2 = screen.get_viewport_rect().size
	var a: TextureRect = screen.exit_arrows.arrows[0]
	var top := MapHud.top_of(view)
	check(
		a.position.y + a.size.y <= top,
		"above the HUD: %s + %s <= %s" % [a.position.y, a.size.y, top]
	)
	var bar_top: float = (screen.hud.get_node("%Belt1") as Control).get_global_rect().position.y
	check(absf(bar_top - top) <= 1.0 * MapHud.scale_of(view), "the bar at the HUD's top")
	screen.free()
	Router.params = old
