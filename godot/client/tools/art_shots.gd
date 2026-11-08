extends Node
## Screenshots of the art slice (the new style), for review. Needs a display:
##   godot --path godot/client --resolution 1280x720 res://tools/art_shots.tscn -- OUT_DIR
## CI runs it after tools/shots.gd into the same folder (.github/workflows/godot.yml).

const ArtSlice := preload("res://scripts/art/art_slice.gd")
## name, place, camera pitch, camera distance
const SHOTS := [
	["art_camp_overview", "camp", 50.0, 24.0],
	["art_camp_45", "camp", 45.0, 13.0],
	["art_camp_50", "camp", 50.0, 13.0],
	["art_camp_55", "camp", 55.0, 13.0],
	["art_battle_50", "battle", 50.0, 13.0],
	["art_lineup", "lineup", 0.0, 13.0],
	["art_people", "people", 0.0, 13.0],
	["art_effects", "effects", 35.0, 13.0],
	["art_effects_room", "effects_room", 35.0, 15.0],
]


func _ready() -> void:
	var args := OS.get_cmdline_user_args()
	var out := args[0] if args.size() > 0 else "user://art_shots"
	var only := args[1] if args.size() > 1 else ""
	DirAccess.make_dir_recursive_absolute(out)
	for s in SHOTS:
		if not only.is_empty() and not String(s[0]).contains(only):
			continue
		var slice: Node3D = ArtSlice.new()
		slice.distance = s[3]
		add_child(slice)
		slice.build(s[1], s[2])
		await _frames(4)
		await get_tree().create_timer(1.2).timeout
		slice.burst()
		await get_tree().create_timer(0.12).timeout
		await RenderingServer.frame_post_draw
		var img := get_viewport().get_texture().get_image()
		var path := out.path_join(String(s[0]) + ".png")
		img.save_png(path)
		print("shot ", s[0])
		slice.queue_free()
		await _frames(2)
	get_tree().quit()


func _frames(n: int) -> void:
	for i in n:
		await get_tree().process_frame
