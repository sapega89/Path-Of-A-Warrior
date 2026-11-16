extends "res://tests/test_case.gd"
## The menus and the HUD in the new art (scripts/ui/ui_theme.gd, scripts/ui/map_hud.gd): the
## fonts of the new art with their Cyrillic, plaques and panels, the backdrop, the coin, the
## HUD's orbs and plates, the exit arrows, the hero in the Inventory as a 3D figure.

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
	var t: Theme = UiTheme.theme(UiTheme.THEME)
	eq(t.default_font, UiTheme.font("text"), "the text")
	eq(t.get_font("font", "Button"), UiTheme.font("bold"), "the buttons bold")
	eq(t.get_type_variation_base(&"Heading"), &"Label", "a heading is a label")
	eq(t.get_font("font", "Heading"), UiTheme.font("title"), "in Kurale")
	eq(t.get_color("font_color", "Heading"), UiTheme.ACCENT, "brass")


func test_plaques_and_panels() -> void:
	var t: Theme = UiTheme.theme(UiTheme.THEME)
	var normal := t.get_stylebox("normal", "Button") as StyleBoxFlat
	check(normal.corner_radius_top_left <= 3 and normal.anti_aliasing, "hard corners, smooth edges")
	eq(normal.border_color, UiTheme.IRON, "an iron rim")
	eq(
		(t.get_stylebox("pressed", "Button") as StyleBoxFlat).bg_color,
		UiTheme.BUTTON_PRESSED,
		"blood-red when pressed"
	)
	check(
		t.get_stylebox("panel", "PanelContainer") is PanelBox, "panels of leather with their rivets"
	)
	check(t.get_stylebox("embedded_border", "Window") is PanelBox, "and the dialogs")
	var plate := (t.get_stylebox("panel", "PanelContainer") as PanelBox).plate
	eq(
		[plate.bg_color, plate.border_color, plate.border_width_top],
		[Color(UiTheme.PANEL, 0.97), UiTheme.IRON, 3],
		"dark leather in an iron rim"
	)
	eq(plate.shadow_size, 10, "a shadow under it")
	check(
		(t.get_stylebox("embedded_border", "Window") as PanelBox).plate == plate, "the same plate"
	)
	var on := t.get_icon("checked", "CheckBox")
	var off := t.get_icon("unchecked", "CheckBox")
	check(on != null and off != null and on != off, "the check boxes drawn")
	var compact: Theme = UiTheme.theme(UiTheme.COMPACT_THEME)
	eq(
		(compact.get_stylebox("normal", "Button") as StyleBoxFlat).content_margin_top,
		4.0,
		"lower buttons"
	)


func test_the_backdrop_and_the_coin() -> void:
	var main: Control = load("res://scenes/main.tscn").instantiate()
	var bg: ColorRect = main.get_node("Backdrop")
	check(bg.material is ShaderMaterial, "painted by its shader")
	eq(bg.mouse_filter, Control.MOUSE_FILTER_IGNORE, "clicks pass")
	eq(bg.color, UiTheme.BG, "on soot")
	main.free()
	var coin := UiTheme.coin()
	eq(coin.get_size(), Vector2(128, 128), "the coin")
	check(coin.get_image().has_mipmaps(), "smooth when small")
	var row: GoldRow = load("res://scenes/ui/gold_row.tscn").instantiate()
	root.add_child(row)
	eq((row.get_child(0) as TextureRect).texture, coin, "the purse shows it")
	check(row.get_node("Value") is Label, "and the gold")
	row.free()


func test_the_hud_panel() -> void:
	var hud: MapHud = load("res://screens/mission/hud/map_hud.tscn").instantiate()
	root.add_child(hud)
	var panel: Rect2 = (hud.get_node("Bottom/Panel") as Control).get_global_rect()
	for orb in ["%HpOrb", "%MpOrb"]:
		var r: Rect2 = (hud.get_node(orb) as Control).get_global_rect()
		check(panel.encloses(r), "%s in the panel: %s in %s" % [orb, r, panel])
	hud.free()
	for path in ["res://screens/mission/hud/map_hud.gd", "res://screens/mission/hud/hud_orb.gd"]:
		check(
			not FileAccess.get_file_as_string(path).contains("assets/original"), "no old pictures"
		)


func test_exit_arrows() -> void:
	eq(ExitArrows.exit_arrow(0).get_size(), Vector2(72, 60), "down")
	eq(ExitArrows.exit_arrow(1).get_size(), Vector2(60, 72), "left")
	eq(ExitArrows.exit_arrow(2).get_size(), Vector2(72, 60), "up")
	var down := ExitArrows.exit_arrow(0).get_image()
	var up := ExitArrows.exit_arrow(2).get_image()
	check(
		down.get_pixel(36, 8).a < down.get_pixel(36, 52).a,
		"down: the point at the bottom is the strong one"
	)
	check(up.get_pixel(36, 8).a > up.get_pixel(36, 52).a, "up: at the top")


func test_the_hero_in_the_inventory() -> void:
	var p := Profile.new()
	p.head = 2
	p.save(TEST_PATH)
	var old: Dictionary = Router.params
	Router.params = {"profile_path": TEST_PATH}
	var inv: InventoryScreen = Router.make(Router.SCREENS["inventory"])
	root.add_child(inv)
	var gear: GearBoard = inv.gear
	check(gear.figure != null, "a figure")
	eq(gear.figure.kind, MapPeople.HEROES[2], "of his class")
	var view: SubViewport = gear.get_node("HeroView")
	check(view.own_world_3d and view.transparent_bg, "in a world of its own, on the panel")
	eq(gear.ghosts.size(), Items.EQUIPPED, "a picture for each place")
	eq(
		[gear.ghosts[0].name, gear.ghosts[0].mouse_filter, gear.ghosts[0].offset_left],
		[&"Ghost", Control.MOUSE_FILTER_IGNORE, 8.0],
		"faint, inside its place, clicks pass (place_ghost.tscn)"
	)
	for i in Items.EQUIPPED:
		check(gear.ghosts[i].texture != null, "place %d: what goes there" % i)
		eq(gear.ghosts[i].visible, gear.places[i].icon == null, "place %d: shown when empty" % i)
	check(not gear.ghosts[0].visible, "the weapon is worn")
	eq(gear.blade, 1, "the broadsword in his hand")
	inv.profile.add_item(Items.make(101))
	inv.press_cell(0)
	eq(gear.blade, 0, "a sabre, the other kind: the blade changes at once")
	inv.free()
	Router.params = old
	DirAccess.remove_absolute(TEST_PATH)


func test_touch_controls_fill_the_screen() -> void:
	var tc: Control = TouchControls.new()
	tc.force_visible = true
	root.add_child(tc)
	eq(tc.size, root.get_viewport().get_visible_rect().size, "as big as the screen")
	check(tc.button_center("attack").x > tc.size.x / 2.0, "the buttons at the right")
	tc.free()


func test_the_theme_files_keep_the_cyrillic_fallbacks() -> void:
	for path in [UiTheme.THEME, UiTheme.COMPACT_THEME, KeyGrid.KEY_THEME]:
		var t: Theme = UiTheme.theme(path)
		check(t != null, "%s loads" % path)
	var full: Theme = UiTheme.theme(UiTheme.THEME)
	for item in [["font", "Button"], ["title_font", "Window"]]:
		var f: Font = full.get_font(item[0], item[1])
		check(f.fallbacks.size() >= 1, "%s of %s falls back to the Cyrillic file" % item)
	check(full.default_font.fallbacks.size() >= 1, "and the default font")
