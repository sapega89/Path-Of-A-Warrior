class_name HelpScreen
extends BaseScreen
## Help, one for the whole game: the campaign's topics (Missions, Visiting, Blacksmith, Skills,
## Gear, Experience, Saving, Control; data/help.json), then the multiplayer's Duel and Online
## Missions (data/mp.json), each a few pages, ◄ n / m ►. The Control pages tell this version's
## keys, buttons and touch controls, on the map and in an online battle.
## Up / down pick a topic, left / right turn the page, back returns to the topics, then leaves.

const PATH := "res://data/help.json"
const CONTROL_TOPIC := 7
const CONTROL_PAGES := ["help.control_1", "help.control_2"]
const MP_PATH := "res://data/mp.json"
const MP_CONTROL_PAGES := ["help.mp_control_1", "help.mp_control_2"]
## The multiplayer topics shown, by their name in data/mp.json, and the name they get here.
const MP_TOPICS := {"Duel": "online.duel", "Missions": "menu.online_missions"}

var topics: Array = []
var topic := -1  # -1: the list of topics
var page := 0
@onready var list: VBoxContainer = %List
@onready var page_box: VBoxContainer = %Page
@onready var heading: Label = %Heading
@onready var text: Label = %Text
@onready var page_label: Label = %Number
## Shown over another screen (the mission's pause menu): what leaving does instead of going back.
var close := Callable()


func _ready() -> void:
	topics = _read(PATH, "topics")
	for t in _read(MP_PATH, "help"):
		if MP_TOPICS.has(t.get("name")):
			topics.append({"name": tr(MP_TOPICS[t.name]), "pages": t.get("pages", [])})
	for i in topics.size():
		var b := Button.new()
		b.name = "Topic%d" % i
		b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
		b.text = I18n.text(topics[i].get("name", ""))
		b.pressed.connect(open.bind(i))
		list.add_child(b)
	show_topics()


static func _read(path: String, key: String) -> Array:
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return []
	var d: Variant = JSON.parse_string(f.get_as_text())
	return d.get(key, []) if typeof(d) == TYPE_DICTIONARY else []


func show_topics() -> void:
	topic = -1
	heading.text = "help.title"
	heading.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_INHERIT
	list.visible = true
	page_box.visible = false
	if list.get_child_count() > 0:
		(list.get_child(0) as Button).grab_focus.call_deferred()


func pages_of(i: int) -> Array:
	if i == CONTROL_TOPIC:
		return (CONTROL_PAGES + MP_CONTROL_PAGES).map(func(k): return tr(k))
	return topics[i].get("pages", []).map(I18n.text) if i >= 0 and i < topics.size() else []


func open(i: int) -> void:
	topic = i
	page = 0
	heading.text = I18n.text(topics[i].get("name", ""))
	heading.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	list.visible = false
	page_box.visible = true
	show_page()


func show_page() -> void:
	var pages := pages_of(topic)
	text.text = str(pages[page]) if page < pages.size() else ""
	page_label.text = "%d / %d" % [page + 1, pages.size()]


func prev_page() -> void:
	turn_page(-1)


func next_page() -> void:
	turn_page(1)


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


func _screen_input(event: InputEvent) -> void:
	if topic >= 0 and (event.is_action_pressed("ui_left") or event.is_action_pressed("ui_right")):
		get_viewport().set_input_as_handled()
		turn_page(-1 if event.is_action_pressed("ui_left") else 1)
	elif topic >= 0 and (event.is_action_pressed("ui_accept") or event.is_action_pressed("attack")):
		get_viewport().set_input_as_handled()
		turn_page(1)
