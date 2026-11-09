class_name EndingsScreen
extends BaseScreen
## Endings: the 24 endings of the story, five to a page. One the hero has reached plays again
## (the story player, without its reward); one not reached yet is greyed and only says so.
## Up / down pick, left / right turn the page, back leaves.

const PER_PAGE := 5

var profile: RefCounted
var path: String = Profile.PATH
var page := 0
@onready var list: VBoxContainer = %List
@onready var page_label: Label = %Page
@onready var info: Label = %Info


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	page = clampi(int(Router.params.get("page", 0)), 0, pages() - 1)
	show_page()


static func pages() -> int:
	return (Stories.ENDINGS + PER_PAGE - 1) / PER_PAGE


static func title(i: int) -> String:
	var titles: Array = Stories.data().get("titles", [])
	return I18n.text(titles[i]) if i >= 0 and i < titles.size() else ""


func reached(i: int) -> bool:
	return int(profile.endings) & (1 << i) != 0


func show_page() -> void:
	for c in list.get_children():
		list.remove_child(c)
		c.queue_free()
	for k in PER_PAGE:
		var i := page * PER_PAGE + k
		if i >= Stories.ENDINGS:
			break
		var b := Button.new()
		b.name = "Ending%d" % i
		b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		b.text = title(i)
		if not reached(i):
			b.add_theme_color_override("font_color", Color(0.5, 0.5, 0.5))
			b.add_theme_color_override("font_focus_color", Color(0.6, 0.6, 0.6))
		b.pressed.connect(open.bind(i))
		list.add_child(b)
	page_label.text = "%d / %d" % [page + 1, pages()]
	info.text = ""
	(list.get_child(0) as Button).grab_focus.call_deferred()


func prev_page() -> void:
	turn_page(-1)


func next_page() -> void:
	turn_page(1)


func turn_page(step: int) -> void:
	page = posmod(page + step, pages())
	show_page()


## Plays an ending reached (again: without the numbers at its end); one not reached only says
## why.
func open(i: int) -> bool:
	if not reached(i):
		info.text = "endings.locked"
		return false
	Router.params["page"] = page
	Router.push("story", {"story": i, "replay": true, "profile_path": path})
	return true


func _screen_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_left"):
		get_viewport().set_input_as_handled()
		turn_page(-1)
	elif event.is_action_pressed("ui_right"):
		get_viewport().set_input_as_handled()
		turn_page(1)
