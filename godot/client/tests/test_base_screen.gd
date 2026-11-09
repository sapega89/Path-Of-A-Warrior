extends "res://tests/test_case.gd"
## BaseScreen: the back key of every screen and where its hero is kept.


## A screen that counts what reaches it.
class Probe:
	extends BaseScreen
	var backs := 0
	var others: Array[String] = []
	var back_is_back := true

	func go_back() -> void:
		backs += 1

	func handles_back() -> bool:
		return back_is_back

	func _screen_input(event: InputEvent) -> void:
		if event is InputEventAction:
			others.append((event as InputEventAction).action)


func _action(action: String) -> InputEventAction:
	var ev := InputEventAction.new()
	ev.action = action
	ev.pressed = true
	return ev


func test_the_back_key_goes_to_go_back() -> void:
	var p := Probe.new()
	root.add_child(p)
	p._unhandled_input(_action("ui_cancel"))
	eq(p.backs, 1, "back once")
	eq(p.others, [] as Array[String], "the back key goes nowhere else")
	p._unhandled_input(_action("ui_accept"))
	eq(p.backs, 1, "another key is not back")
	eq(p.others, ["ui_accept"] as Array[String], "it goes to _screen_input")
	p.free()


func test_a_screen_can_take_the_back_key_for_itself() -> void:
	var p := Probe.new()
	p.back_is_back = false
	root.add_child(p)
	p._unhandled_input(_action("ui_cancel"))
	eq(p.backs, 0, "not back")
	eq(p.others, ["ui_cancel"] as Array[String], "the screen's own key")
	p.free()


func test_the_default_back_is_the_previous_screen() -> void:
	var host := Control.new()
	root.add_child(host)
	Router.attach(host)
	Router.go("title")
	Router.push("settings")
	var plain := BaseScreen.new()
	root.add_child(plain)
	plain._unhandled_input(_action("ui_cancel"))
	eq(Router.current_name(), "title", "back to the title")
	plain.free()
	Router.attach(null)
	host.free()


func test_profile_path() -> void:
	Router.params = {"profile_path": "user://test_base_screen.json"}
	eq(BaseScreen.profile_path(), "user://test_base_screen.json", "the test's file")
	Router.params = {}
	eq(BaseScreen.profile_path(), Profile.PATH, "else the hero's place")


func test_every_screen_is_a_base_screen() -> void:
	for screen_name in Router.SCREENS:
		var screen: Control = Router.make(Router.SCREENS[screen_name])
		check(screen is BaseScreen, "%s is a BaseScreen" % screen_name)
		screen.free()


func test_a_screen_from_a_scene() -> void:
	var node := BaseScreen.new()
	node.name = "FromScene"
	var label := Label.new()
	label.name = "Line"
	node.add_child(label)
	label.owner = node
	var packed := PackedScene.new()
	packed.pack(node)
	node.free()
	var path := "user://test_base_screen.tscn"
	eq(ResourceSaver.save(packed, path), OK, "saved")
	var screen: Control = Router.make(path)
	check(screen is BaseScreen, "the scene's root")
	check(screen.get_node_or_null("Line") is Label, "with its nodes")
	screen.free()
	DirAccess.remove_absolute(path)
