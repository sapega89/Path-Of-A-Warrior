extends "res://tests/test_case.gd"
## The menus and the HUD in the new art (scripts/ui/ui_theme.gd, scripts/ui/map_hud.gd): the
## fonts of the new art with their Cyrillic, plaques and panels, the backdrop, the coin, the
## HUD's orbs and plates, the exit arrows, the hero on the Gear page as a 3D figure.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const MapHud := preload("res://scripts/ui/map_hud.gd")
const MissionScreen := preload("res://scripts/screens/mission_screen.gd")
const Gear := preload("res://scripts/screens/gear_screen.gd")
const Profile := preload("res://scripts/core/profile.gd")
const Items := preload("res://scripts/core/items.gd")
const MapPeople := preload("res://scripts/world/map_people.gd")
const TouchControls := preload("res://scripts/ui/touch_controls.gd")
const TEST_PATH := "user://test_ui_theme.json"


func test_the_fonts_of_the_new_art() -> void:
	for kind in ["title", "text", "bold"]:
		var f := UiTheme.font(kind)
		check(f != null, kind)
		for ch in ["A", "Ж", "ї", "Ґ", "є"]:
			check(f.has_char(ch.unicode_at(0)), "%s has %s" % [kind, ch])
		check(UiTheme.font(kind) == f, "%s made once" % kind)
	check(UiTheme.font("title").get_font_name().contains("Kurale"), "headings in Kurale")
	check(UiTheme.font("text").get_font_name().contains("PT Sans"), "text in PT Sans")
	var t := UiTheme.build()
	eq(t.default_font, UiTheme.font("text"), "the text")
	eq(t.get_font("font", "Button"), UiTheme.font("bold"), "the buttons bold")
	var h := UiTheme.heading("gear.title", 44)
	check(h is Label, "a heading is a label")
	eq(h.get_theme_font("font"), UiTheme.font("title"), "in Kurale")
	eq(h.get_theme_color("font_color"), UiTheme.ACCENT, "brass")
	h.free()


func test_plaques_and_panels() -> void:
	var t := UiTheme.build()
	var normal := t.get_stylebox("normal", "Button") as StyleBoxFlat
	check(normal.corner_radius_top_left <= 3 and normal.anti_aliasing, "hard corners, smooth edges")
	eq(normal.border_color, UiTheme.IRON, "an iron rim")
	eq(
		(t.get_stylebox("pressed", "Button") as StyleBoxFlat).bg_color,
		UiTheme.BUTTON_PRESSED,
		"blood-red when pressed"
	)
	check(
		t.get_stylebox("panel", "PanelContainer") is UiTheme.PanelBox,
		"panels of leather with their rivets"
	)
	check(t.get_stylebox("embedded_border", "Window") is UiTheme.PanelBox, "and the dialogs")
	var on := t.get_icon("checked", "CheckBox")
	var off := t.get_icon("unchecked", "CheckBox")
	check(on != null and off != null and on != off, "the check boxes drawn")
	var compact := UiTheme.compact()
	eq(
		(compact.get_stylebox("normal", "Button") as StyleBoxFlat).content_margin_top,
		4.0,
		"lower buttons"
	)


func test_the_backdrop_and_the_coin() -> void:
	var bg := UiTheme.backdrop()
	check(bg.material is ShaderMaterial, "painted by its shader")
	eq(bg.mouse_filter, Control.MOUSE_FILTER_IGNORE, "clicks pass")
	bg.free()
	var coin := UiTheme.coin()
	eq(coin.get_size(), Vector2(128, 128), "the coin")
	check(coin.get_image().has_mipmaps(), "smooth when small")
	var row := UiTheme.gold_row("Gold")
	eq((row.get_child(0) as TextureRect).texture, coin, "the purse shows it")
	check(row.get_node("Value") is Label, "and the gold")
	row.free()


func test_the_hud_panel() -> void:
	for x in MapHud.ORB_X:
		check(x - MapHud.ORB_R >= 0 and x + MapHud.ORB_R <= 240, "an orb in the panel: %d" % x)
	check(
		MapHud.ORB_Y - MapHud.ORB_R > 3 and MapHud.ORB_Y + MapHud.ORB_R < MapHud.PANEL_H,
		"and under its rim"
	)
	for b in 2:
		var r := MapHud._potion_rect(Vector2.ZERO, b, 1.0)
		for x in MapHud.ORB_X:
			check(
				absf(r.get_center().x - x) > MapHud.ORB_R + MapHud.ITEM / 2.0,
				"potion %d beside the orbs" % b
			)
	var src := FileAccess.get_file_as_string("res://scripts/ui/map_hud.gd")
	check(not src.contains("assets/original"), "no old pictures")


func test_exit_arrows() -> void:
	eq(MissionScreen.exit_arrow(0).get_size(), Vector2(72, 60), "down")
	eq(MissionScreen.exit_arrow(1).get_size(), Vector2(60, 72), "left")
	eq(MissionScreen.exit_arrow(2).get_size(), Vector2(72, 60), "up")
	var down := MissionScreen.exit_arrow(0).get_image()
	var up := MissionScreen.exit_arrow(2).get_image()
	check(
		down.get_pixel(36, 8).a < down.get_pixel(36, 52).a,
		"down: the point at the bottom is the strong one"
	)
	check(up.get_pixel(36, 8).a > up.get_pixel(36, 52).a, "up: at the top")


func test_the_hero_on_the_gear_page() -> void:
	var p := Profile.new()
	p.head = 2
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var gear: Control = Gear.new()
	root.add_child(gear)
	check(gear.figure != null, "a figure")
	eq(gear.figure.kind, MapPeople.HEROES[2], "of his class")
	var view: SubViewport = gear.get_node("HeroView")
	check(view.own_world_3d and view.transparent_bg, "in a world of its own, on the panel")
	eq(gear.ghosts.size(), Items.EQUIPPED, "a picture for each place")
	for i in Items.EQUIPPED:
		check(gear.ghosts[i].texture != null, "place %d: what goes there" % i)
		eq(gear.ghosts[i].visible, gear.places[i].icon == null, "place %d: shown when empty" % i)
	check(not gear.ghosts[0].visible, "the weapon is worn")
	gear.free()
	Router.params = old
	DirAccess.remove_absolute(TEST_PATH)


func test_touch_controls_fill_the_screen() -> void:
	var tc: Control = TouchControls.new()
	tc.force_visible = true
	root.add_child(tc)
	eq(tc.size, root.get_viewport().get_visible_rect().size, "as big as the screen")
	check(tc.button_center("attack").x > tc.size.x / 2.0, "the buttons at the right")
	tc.free()
