extends "res://tests/test_case.gd"
## The art slice (scripts/art, assets/art): the models load, the people share one clip
## library, and the camp and the battle room build with everything in place.

const PEOPLE := ["kozak", "kozak_camp", "kozak_svyta", "zholner", "luchnyk", "polkovnyk"]
const WEAPONS := ["sabre", "sabre_gold", "bulava", "spear", "shield", "bow"]
const CLIPS := [
	"idle",
	"walk",
	"run",
	"attack_slash",
	"attack_chop",
	"block_hit",
	"aim_bow",
	"sit",
	"cheer",
	"interact",
	"hit",
	"death"
]
const ICONS := ["sabre", "shield", "fire", "wind", "bulava", "potion", "coin", "ornament"]


func test_people_have_a_skeleton_and_no_clips_of_their_own() -> void:
	for kind in PEOPLE:
		var body: Node = ArtKit.scene("characters/%s.glb" % kind).instantiate()
		check(body.find_child("Skeleton3D", true, false) != null, "%s has a skeleton" % kind)
		check(
			body.find_children("*", "MeshInstance3D", true, false).size() > 0,
			"%s has a body" % kind
		)
		check(
			body.find_child("AnimationPlayer", true, false) == null,
			"%s takes the shared clips" % kind
		)
		body.free()


func test_shared_clips() -> void:
	var lib := ArtKit.clips()
	for clip in CLIPS:
		check(lib.has_animation(clip), "clip %s" % clip)
	eq(lib.get_animation("idle").loop_mode, Animation.LOOP_LINEAR, "idle repeats")
	eq(lib.get_animation("attack_slash").loop_mode, Animation.LOOP_NONE, "a blow is played once")


func test_figure_plays_and_holds_a_weapon() -> void:
	var fig: Node3D = ArtFigure.new()
	root.add_child(fig)
	fig.setup("kozak_camp")
	fig.play("walk")
	eq(String(fig.player.current_animation), "walk", "the clip plays")
	var before: int = fig.skeleton.find_children("*", "BoneAttachment3D", true, false).size()
	fig.equip("spear")
	var hands: Array = fig.skeleton.find_children("*", "BoneAttachment3D", true, false)
	eq(hands.size(), before + 1, "the spear goes into a hand")
	eq(String((hands[-1] as BoneAttachment3D).bone_name), "handslot.r", "the right hand")
	fig.face(Vector3(1, 0, 0))
	check(is_equal_approx(fig.rotation.y, PI / 2.0), "faces +X")
	fig.free()


func test_weapons() -> void:
	var source: Node = ArtKit.scene("characters/weapons.glb").instantiate()
	for w in WEAPONS:
		var mesh := source.find_child(w, true, false) as MeshInstance3D
		check(
			mesh != null and mesh.get_parent() is BoneAttachment3D, "weapon %s sits on a bone" % w
		)
	source.free()


func test_props() -> void:
	for file in DirAccess.get_files_at(ArtKit.ROOT + "props"):
		if not file.ends_with(".glb"):
			continue
		var node := ArtKit.prop(file.get_basename())
		check(
			node.find_children("*", "MeshInstance3D", true, false).size() > 0,
			"%s has a mesh" % file
		)
		node.free()


func test_icons_and_fonts() -> void:
	for name in ICONS:
		var tex := ArtHud.icon(name, 64)
		check(tex != null and tex.get_width() == 64, "icon %s at 64 px" % name)
	var f := ArtHud.font(
		[
			"res://assets/art/fonts/kurale-latin-400-normal.woff2",
			"res://assets/art/fonts/kurale-cyrillic-400-normal.woff2"
		]
	)
	check(
		f.has_char("К".unicode_at(0)) or f.fallbacks[0].has_char("К".unicode_at(0)),
		"Cyrillic letters"
	)


func test_camp_and_battle_build() -> void:
	for place in ["camp", "battle"]:
		var slice: Node3D = ArtSlice.new()
		root.add_child(slice)
		slice.build(place, 50.0)
		check(slice.hero != null, "%s: a hero" % place)
		check(slice.figures.size() >= 4, "%s: people around (%d)" % [place, slice.figures.size()])
		check(slice.camera != null and slice.camera.current, "%s: the camera" % place)
		check(slice.hud != null, "%s: the HUD" % place)
		check(slice.find_child("Ground", true, false) != null, "%s: the ground" % place)
		slice.free()


func test_no_original_pictures() -> void:
	for dir in ["res://scripts/art/", "res://assets/art/shaders/"]:
		for file in DirAccess.get_files_at(dir):
			if file.ends_with(".gd") or file.ends_with(".gdshader"):
				var text := FileAccess.get_file_as_string(dir + file)
				check(not text.contains("assets/original"), "%s uses only the new art" % file)
	# Screens redrawn in the new art: the Safe's arrow, the blacksmith's sparkle.
	for file in [
		"res://screens/live_safe/live_safe_screen.gd",
		"res://screens/shop/shop_screen.gd",
		"res://screens/shop/enchant_sparkle.gd",
	]:
		var text := FileAccess.get_file_as_string(file)
		check(not text.contains("assets/original"), "%s uses only the new art" % file)
