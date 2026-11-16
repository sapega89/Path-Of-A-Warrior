extends Node
## How fast the 3D views draw (needs a display, not --headless):
##   godot --path godot/client res://tools/perf.tscn [-- SECONDS]
## Opens two camps and two missions with the auto-hunt fighting, lets each settle, then for
## SECONDS (5 by default) counts the frames and what the renderer drew in them: one line each,
## after a line with the graphics card and the window. The game runs as the player set it up
## (Settings: graphics, window), but without vsync, to see how fast it can go; the hero is a new
## one in a file of its own, removed at the end, so no saved game is touched.

const SETTLE := 2.0
const HERO := "user://perf_hero.json"
const CAMPS: Array[Dictionary] = [
	{"name": "camp_main", "place": 0},
	{"name": "camp_six_ways", "place": 27},
]
const MISSIONS: Array[Dictionary] = [
	{"name": "mission_1_fight", "lord": 1, "mission": 0},
	{"name": "mission_9_fight", "lord": 3, "mission": 2},
]

var _seconds := 5.0


func _ready() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() > 0:
		_seconds = float(args[0])
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps = 0
	var main: Node = load("res://scenes/main.tscn").instantiate()
	add_child(main)
	await _frames(10)
	print(
		(
			"perf %s (%s), window %s, graphics %d"
			% [
				RenderingServer.get_video_adapter_name(),
				RenderingServer.get_video_adapter_vendor(),
				DisplayServer.window_get_size(),
				int(Settings.get_value("graphics")),
			]
		)
	)
	var hero := Profile.new()
	hero.done["1:0"] = true
	for c in CAMPS:
		hero.place = int(c.place)
		hero.save(HERO)
		Router.go("camp", {"profile_path": HERO})
		await _measure(str(c.name))
	for m in MISSIONS:
		Router.go(
			"mission", {"lord": m.lord, "mission": m.mission, "seed": 1, "profile_path": HERO}
		)
		(Router.current as MissionScreen).toggle_auto()
		await _measure(str(m.name))
	Router.go("title")
	DirAccess.remove_absolute(ProjectSettings.globalize_path(HERO))
	get_tree().quit()


## Lets the screen settle, then counts its frames for _seconds and prints one line: the frames
## a second, a frame on average and the slowest 1 %, and what the renderer drew in a frame (all
## its passes: the picture, the shadows, the interface): draw calls and triangles.
func _measure(what: String) -> void:
	await _wait(SETTLE)
	var frames: Array[float] = []
	var calls := 0
	var triangles := 0
	var start := Time.get_ticks_usec()
	var last := start
	while Time.get_ticks_usec() - start < int(_seconds * 1e6):
		await get_tree().process_frame
		var now := Time.get_ticks_usec()
		frames.append((now - last) / 1000.0)
		last = now
		calls += RenderingServer.get_rendering_info(
			RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME
		)
		triangles += RenderingServer.get_rendering_info(
			RenderingServer.RENDERING_INFO_TOTAL_PRIMITIVES_IN_FRAME
		)
	var n := frames.size()
	var total := 0.0
	for f in frames:
		total += f
	frames.sort()
	print(
		(
			"perf %-16s fps %6.1f  frame %6.1f ms  slowest 1%% %6.1f ms  draws %5d  triangles %7d"
			% [
				what,
				n / (total / 1000.0),
				total / n,
				frames[mini(n - 1, int(n * 0.99))],
				calls / n,
				triangles / n,
			]
		)
	)


func _wait(t: float) -> void:
	await get_tree().create_timer(t).timeout


func _frames(n: int) -> void:
	for i in n:
		await get_tree().process_frame
