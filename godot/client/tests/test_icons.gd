extends "res://tests/test_case.gd"
## The icons of things and skills in the new art (assets/art/icons, godot/tools/art/icons.py;
## scripts/ui/item_slot.gd): every thing and every skill has one, drawn, smooth when small;
## the HUD and the things on the ground show them too.


## How much of an icon is painted (0..1).
func _painted(t: Texture2D) -> float:
	var img := t.get_image()
	var n := 0
	for y in range(0, img.get_height(), 4):
		for x in range(0, img.get_width(), 4):
			n += 1 if img.get_pixel(x, y).a > 0.5 else 0
	return float(n) / float((img.get_width() / 4) * (img.get_height() / 4))


func test_every_thing_has_its_icon() -> void:
	var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/items.json"))
	var seen := {}
	for section in data:
		for id in data[section]:
			var t := ItemSlot.item_icon(int(id))
			check(t != null, "%s (%s)" % [data[section][id].name, id])
			if t != null:
				seen[t] = true
	for potion in range(1, 12):
		check(ItemSlot.item_icon(potion) != null, "potion %d" % potion)
	check(seen.size() >= 40, "the things look different: %d icons" % seen.size())
	eq(ItemSlot.item_icon(0), null, "an empty place")


func test_every_skill_has_its_icon_learned_or_not() -> void:
	for skill in range(12, 31):
		var on := ItemSlot.icon("skill", skill - 12)
		var off := ItemSlot.icon("skillgray", skill - 12)
		check(on != null and off != null, "skill %d" % skill)
		var c: Color = on.get_image().get_pixel(64, 64)
		var g: Color = off.get_image().get_pixel(64, 64)
		check(
			absf(g.r - g.g) < 0.02 and absf(g.g - g.b) < 0.02,
			"skill %d: grey when not learned" % skill
		)
		check(c != g, "skill %d: in colour when learned" % skill)


func test_icons_are_drawn_and_smooth() -> void:
	for sheet in ["tool", "kibo", "sungbo", "shinki", "skill"]:
		var i := 0
		while true:
			var t := ItemSlot.icon(sheet, i)
			if t == null:
				break
			eq(t.get_size(), Vector2(ItemSlot.ART, ItemSlot.ART), "%s %d: its size" % [sheet, i])
			var painted := _painted(t)
			check(painted > 0.08 and painted < 0.97, "%s %d is drawn: %.2f" % [sheet, i, painted])
			check(t.get_image().has_mipmaps(), "%s %d has mipmaps" % [sheet, i])
			i += 1
		check(i >= 12, "%s: %d icons" % [sheet, i])
	check(is_same(ItemSlot.icon("kibo", 3), ItemSlot.icon("kibo", 3)), "made once")
	eq(ItemSlot.icon("kibo", 99), null, "past the sheet")


func test_the_hud_draws_them_smooth() -> void:
	var hud := MapHud.new()
	root.add_child(hud)
	var icons: Control = hud.get_node("Icons")
	eq(icons.texture_filter, CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS, "the icons smooth")
	eq(
		hud.get_node("Labels").texture_filter,
		CanvasItem.TEXTURE_FILTER_LINEAR,
		"the counts and keys smooth"
	)
	check(
		hud.get_node("Labels").get_index() > icons.get_index(), "the counts and keys over the icons"
	)
	hud.free()


func test_things_on_the_ground() -> void:
	var old: Dictionary = Router.params
	Router.params = {"lord": 1, "mission": 0, "seed": 2}
	var screen: Control = MissionScreen.new()
	root.add_child(screen)
	screen.set_process(false)
	for item in [1, 120, 20000]:
		var d := MapDrop.new()
		d.item = item
		d.pos = Vector2i(120, 100)
		screen.sim.drops.append(d)
	screen._place_loot()
	eq(screen.loot.size(), 3, "three on the ground")
	var potion: Sprite3D = screen.loot[screen.sim.drops[0]]
	eq(potion.texture, ItemSlot.icon("tool", 0), "a red potion")
	eq(screen.loot[screen.sim.drops[1]].texture, ItemSlot.icon("tool", 11), "gear: a box")
	eq(
		screen.loot[screen.sim.drops[2]].texture,
		ItemSlot.icon("tool", MissionScreen.GOLD_ICON),
		"gold"
	)
	check(
		absf(potion.texture.get_width() * potion.pixel_size - 28.0 / 27.0) < 0.001,
		"as big as before"
	)
	screen.queue_free()
	Router.params = old
