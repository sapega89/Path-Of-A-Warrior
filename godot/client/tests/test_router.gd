extends "res://tests/test_case.gd"

const RouterScript := preload("res://scripts/core/router.gd")


func test_go_push_back() -> void:
	var host := Control.new()
	root.add_child(host)
	var r: Node = RouterScript.new()
	r.attach(host)
	check(r.go("title"), "go title")
	eq(r.current_name(), "title", "on title")
	check(r.push("settings"), "push settings")
	eq(r.depth(), 2, "depth")
	eq(host.get_child_count(), 1, "one screen shown")
	check(r.back(), "back")
	eq(r.current_name(), "title", "back on title")
	check(not r.back(), "nothing to go back to")
	check(not r.push("nope"), "unknown screen")
	check(r.push("settings", {"a": 1}), "push with params")
	eq(r.params, {"a": 1}, "params")
	r.back()
	eq(r.params, {}, "params of the screen below")
	r.free()
	host.free()


func test_every_screen_opens() -> void:
	var host := Control.new()
	root.add_child(host)
	var r: Node = RouterScript.new()
	r.attach(host)
	for screen in RouterScript.SCREENS:
		check(r.go(screen), "open %s" % screen)
		check(r.current != null and r.current.is_inside_tree(), "%s in tree" % screen)
	r.free()
	host.free()
