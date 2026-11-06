extends Control
## Help: the original's topics (Missions, Visiting, Blacksmith, Skills, Gear, Experience,
## Saving, Control), each a few pages, ◄ n / m ►. The Control pages tell this version's
## keys, buttons and touch controls (the original's were the phone keypad).
## Up / down pick a topic, left / right turn the page, back returns to the topics, then leaves.
## Multiplayer > Help (Router.params.kind "mp"): the online game's topics (Controls, Menu, Duel,
## Missions, About, Network; data/mp.json), its Controls pages this version's battle keys.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const PATH := "res://data/help.json"
const CONTROL_TOPIC := 7
const CONTROL_PAGES := ["help.control_1", "help.control_2"]
const MP_PATH := "res://data/mp.json"
const MP_CONTROL_PAGES := ["help.mp_control_1", "help.mp_control_2"]

var topics: Array = []
var control_topic := CONTROL_TOPIC
var control_pages: Array = CONTROL_PAGES
var topic := -1  # -1: the list of topics
var page := 0
var list: VBoxContainer
var page_box: VBoxContainer
var heading: Label
var text: Label
var page_label: Label
## Shown over another screen (the mission's pause menu): what leaving does instead of going back.
var close := Callable()


func _ready() -> void:
	var path := PATH
	var key := "topics"
	if str(Router.params.get("kind", "")) == "mp":
		path = MP_PATH
		key = "help"
		control_topic = 0
		control_pages = MP_CONTROL_PAGES
	var f := FileAccess.open(path, FileAccess.READ)
	if f != null:
		var d: Variant = JSON.parse_string(f.get_as_text())
		if typeof(d) == TYPE_DICTIONARY:
			topics = d.get(key, [])
	var col := UiTheme.menu_column(self, 640)
	heading = UiTheme.heading("help.title", 40)
	col.add_child(heading)
	list = VBoxContainer.new()
	list.name = "List"
	list.add_theme_constant_override("separation", 6)
	for i in topics.size():
		var b := Button.new()
		b.name = "Topic%d" % i
		b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		b.text = str(topics[i].get("name", ""))
		b.pressed.connect(open.bind(i))
		list.add_child(b)
	col.add_child(list)
	page_box = VBoxContainer.new()
	page_box.name = "Page"
	page_box.add_theme_constant_override("separation", 12)
	var frame := PanelContainer.new()
	frame.add_theme_stylebox_override("panel", UiTheme.box(Color(0, 0, 0, 0.35), UiTheme.ACCENT, 2))
	text = Label.new()
	text.name = "Text"
	text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	text.custom_minimum_size = Vector2(600, 220)
	text.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	frame.add_child(text)
	page_box.add_child(frame)
	var turn := HBoxContainer.new()
	turn.alignment = BoxContainer.ALIGNMENT_CENTER
	turn.add_theme_constant_override("separation", 24)
	turn.add_child(_arrow("Prev", "◄", -1))
	page_label = Label.new()
	page_label.name = "Number"
	page_label.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	turn.add_child(page_label)
	turn.add_child(_arrow("Next", "►", 1))
	page_box.add_child(turn)
	col.add_child(page_box)
	var back := Button.new()
	back.name = "Back"
	back.text = "common.back"
	back.pressed.connect(go_back)
	col.add_child(back)
	show_topics()


func _arrow(node_name: String, label: String, step: int) -> Button:
	var b := Button.new()
	b.name = node_name
	b.text = label
	b.focus_mode = Control.FOCUS_NONE
	b.pressed.connect(func(): turn_page(step))
	return b


func show_topics() -> void:
	topic = -1
	heading.text = "help.title"
	heading.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_INHERIT
	list.visible = true
	page_box.visible = false
	if list.get_child_count() > 0:
		(list.get_child(0) as Button).grab_focus.call_deferred()


func pages_of(i: int) -> Array:
	if i == control_topic:
		return control_pages.map(func(k): return tr(k))
	return topics[i].get("pages", []) if i >= 0 and i < topics.size() else []


func open(i: int) -> void:
	topic = i
	page = 0
	heading.text = str(topics[i].get("name", ""))
	heading.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	list.visible = false
	page_box.visible = true
	show_page()


func show_page() -> void:
	var pages := pages_of(topic)
	text.text = str(pages[page]) if page < pages.size() else ""
	page_label.text = "%d / %d" % [page + 1, pages.size()]


func turn_page(step: int) -> void:
	if topic < 0:
		return
	page = posmod(page + step, pages_of(topic).size())
	show_page()


## Back: from a topic to the list, from the list out.
func go_back() -> void:
	if topic >= 0:
		var was := topic
		show_topics()
		(list.get_child(was) as Button).grab_focus.call_deferred()
	elif close.is_valid():
		close.call()
	else:
		Router.back()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		go_back()
	elif topic >= 0 and (event.is_action_pressed("ui_left") or event.is_action_pressed("ui_right")):
		get_viewport().set_input_as_handled()
		turn_page(-1 if event.is_action_pressed("ui_left") else 1)
	elif topic >= 0 and (event.is_action_pressed("ui_accept") or event.is_action_pressed("attack")):
		get_viewport().set_input_as_handled()
		turn_page(1)
