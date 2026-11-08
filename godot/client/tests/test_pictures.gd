extends "res://tests/test_case.gd"
## The pictures of the new art in the screens (scripts/ui/pictures.gd): the 46 portraits (42-45
## the fighters of the multiplayer battles), the 15 story pictures, both with mipmaps and in a
## gold frame, and the screens that show them.

const Pictures := preload("res://scripts/ui/pictures.gd")
const Stories := preload("res://scripts/core/stories.gd")
const ArtKit := preload("res://scripts/art/art_kit.gd")
const SIDES := ["plain", "cossack", "crown", "horde", "hero", "upyr"]
const SCREENS := ["story_screen", "briefing_screen", "visiting_screen", "new_game_screen", "mission_screen",
	"online_battle_screen"]


func test_every_portrait_painted() -> void:
	var info: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://assets/art/portraits/busts.json"))
	eq(info.size(), 46, "a bust for every portrait")
	for id in 46:
		var t := Pictures.portrait(id)
		check(t != null and t.get_size() == Vector2(256, 256), "portrait %d" % id)
		check(t.resource_path == Pictures.PORTRAIT % id, "portrait %d of the new art" % id)
		check(String(info[str(id)].side) in SIDES, "portrait %d: the colour of its side" % id)
	for head in 4:
		eq(info[str(Stories.HERO_PORTRAIT + head)].side, "hero", "the hero's portraits: their own colour")
	check(int(info["38"].look) < 0 and int(info["1"].look) > 0, "the hero looks at the one he talks to")
	eq([info["43"].side, info["44"].side, info["45"].side], ["crown", "horde", "upyr"], "the battles' fighters")


func test_mipmaps_made_once() -> void:
	var t := Pictures.portrait(5)
	check(t.get_image().has_mipmaps(), "smooth when smaller")
	check(Pictures.portrait(5) == t, "made once")
	check(load(Pictures.PORTRAIT % 5) == t, "in the place of the imported one")
	eq(Pictures.portrait(99), Pictures.portrait(0), "no portrait: anybody's")


func test_every_story_picture_painted() -> void:
	for n in range(1, 16):
		var t := Pictures.story(n)
		check(t != null and t.get_size() == Vector2(520, 400), "story picture %d" % n)
	check(is_equal_approx(520.0 / 400.0, Pictures.STORY_ASPECT), "as wide as the old ones for their height")


func test_framed() -> void:
	var p := Pictures.framed("Face", Vector2(138, 138))
	eq(p.texture_filter, CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS, "smooth")
	eq((p.material as ShaderMaterial).shader, Pictures.FRAME, "a gold frame")
	eq(p.custom_minimum_size, Vector2(138, 138), "its size")
	var wide := Pictures.framed("Picture", Vector2(351, 270))
	check(is_equal_approx(float((wide.material as ShaderMaterial).get_shader_parameter("aspect")), 1.3), "a wide frame")
	check(wide.material != p.material and Pictures.framed("Other", Vector2(46, 46)).material == p.material,
		"one frame for each shape")
	p.free()
	wide.free()


func test_screens_show_the_new_pictures() -> void:
	for name in SCREENS:
		var text := FileAccess.get_file_as_string("res://scripts/screens/%s.gd" % name)
		check(not text.contains("original/portraits") and not text.contains("original/story"),
			"%s shows the new portraits and pictures" % name)
		check(text.contains("Pictures."), "%s through Pictures" % name)


func test_the_girl_of_the_story() -> void:
	var body: Node = ArtKit.scene("characters/divchyna.glb").instantiate()
	check(body.find_child("Skeleton3D", true, false) != null, "a skeleton, as the people of the maps")
	check(body.find_children("*", "MeshInstance3D", true, false).size() == 1, "her body, no weapons")
	body.free()
