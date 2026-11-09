class_name EndingsScreen
extends BaseScreen
## Endings: the 24 endings of the story, five to a page. One the hero has reached plays again
## (the story player, without its reward); one not reached yet is greyed and only says so.
## Up / down pick, left / right turn the page, back leaves.

const PER_PAGE := 5

var profile: RefCounted
var path: String = Profile.PATH
var page := 0
var list: VBoxContainer
var page_label: Label
var info: Label


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	page = clampi(int(Router.params.get("page", 0)), 0, pages() - 1)
	var col := UiTheme.menu_column(self, 560)
	col.add_child(UiTheme.heading("endings.title", 40))
	list = VBoxContainer.new()
	list.name = "List"
	list.add_theme_constant_override("separation", 8)
	col.add_child(list)
	var turn := HBoxContainer.new()
	turn.alignment = BoxContainer.ALIGNMENT_CENTER
	turn.add_theme_constant_override("separation", 24)
	turn.add_child(_arrow("Prev", "◄", -1))
	page_label = Label.new()
	page_label.name = "Page"
	page_label.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	turn.add_child(page_label)
	turn.add_child(_arrow("Next", "►", 1))
	col.add_child(turn)
	info = Label.new()
	info.name = "Info"
	info.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	info.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	info.custom_minimum_size = Vector2(0, 60)
	col.add_child(info)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(func(): Router.back())
	col.add_child(back)
	show_page()


static func pages() -> int:
	return (Stories.ENDINGS + PER_PAGE - 1) / PER_PAGE


static func title(i: int) -> String:
	var titles: Array = Stories.data().get("titles", [])
	return I18n.text(titles[i]) if i >= 0 and i < titles.size() else ""


func reached(i: int) -> bool:
	return int(profile.endings) & (1 << i) != 0


func _arrow(node_name: String, text: String, step: int) -> Button:
	var b := Button.new()
	b.name = node_name
	b.text = text
	b.focus_mode = Control.FOCUS_NONE
	b.pressed.connect(func(): turn_page(step))
	return b


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
