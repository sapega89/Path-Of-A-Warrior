extends Control
## The campaign: the lords the hero can fight for from where he is (the campaign chapter of
## his place), then the missions of a lord. A lord who is not open yet is greyed; a mission
## won has a mark. Winning takes the hero to that lord's place, so the list changes.
## A mission shows its description first; OK asks whether to accept it (the general to beat,
## the level and the gold), and Yes counts the briefing and opens it, then the map.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Campaign := preload("res://scripts/core/campaign.gd")
const Profile := preload("res://scripts/core/profile.gd")
const MapSim := preload("res://scripts/sim/map_sim.gd")
const DONE_MARK := "  ✓"

var campaign := Campaign.new()
var profile: RefCounted
var list: VBoxContainer
var heading: Label
var scroll: ScrollContainer
var ok: Button  # under the description: accept the mission?
var ask: ConfirmationDialog
## 1 lords of the hero's place, 2 missions of a lord, 3 the description of a mission
var level := 1
var chapter := 0
var lord_id := 0
var mission := 0
var path: String = Profile.PATH
var rng := RandomNumberGenerator.new()


func _ready() -> void:
	var p: Dictionary = Router.params
	path = str(p.get("profile_path", Profile.PATH))
	profile = Profile.load_or_new(path)
	if p.has("seed"):
		rng.seed = int(p.seed)
	var col := UiTheme.menu_column(self, 640)
	heading = UiTheme.heading("campaign.lords", 40)
	col.add_child(heading)
	scroll = ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(640, 520)
	scroll.follow_focus = true
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	col.add_child(scroll)
	list = VBoxContainer.new()
	list.name = "List"
	list.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	list.add_theme_constant_override("separation", 6)
	scroll.add_child(list)
	ok = Button.new()
	ok.name = "Ok"
	ok.text = "campaign.ok"
	ok.pressed.connect(ask_accept)
	col.add_child(ok)
	ask = ConfirmationDialog.new()
	ask.name = "Ask"
	ask.ok_button_text = "online.yes"
	ask.cancel_button_text = "online.no"
	ask.confirmed.connect(accept)
	add_child(ask)
	level = clampi(int(p.get("level", 1)), 1, 3)
	chapter = int(p.get("chapter", profile.place))
	lord_id = int(p.get("lord", 0))
	mission = int(p.get("mission", 0))
	show_level()
	if Cloud.enabled():
		Cloud.game_started()
		if not Cloud.has_account():  # no hero without an account: it lives on the server
			Router.push.call_deferred("register")


func show_level() -> void:
	for c in list.get_children():
		list.remove_child(c)
		c.queue_free()
	ok.visible = level == 3
	scroll.scroll_vertical = 0
	match level:
		1:
			heading.text = "campaign.lords"
			for id in campaign.chapter_lords(chapter):
				var b := _item(campaign.lord_name(id), _open_lord.bind(int(id)))
				b.disabled = not profile.is_lord_open(int(id))
		2:
			heading.text = campaign.lord_name(lord_id)
			var ms := campaign.lord_missions(lord_id)
			for i in ms.size():
				var text: String = tr("campaign.mission") % [i + 1, tr(str(ms[i].get("name", "")))]
				if profile.is_done(lord_id, i):
					text += DONE_MARK
				_item(text, _open_mission.bind(i))
		3:
			heading.text = campaign.lord_name(lord_id)
			var m := mission_data()
			var title := Label.new()
			title.name = "Mission"
			title.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
			title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			title.text = str(m.get("name", ""))
			list.add_child(title)
			var text := Label.new()
			text.name = "Description"
			text.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
			text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
			text.size_flags_horizontal = Control.SIZE_EXPAND_FILL
			text.text = str(m.get("description", ""))
			list.add_child(text)
	# The focus: the first one open; back from a description, that mission; OK on one.
	var open := list.get_children().filter(func(c): return c is Button and not c.disabled)
	if level == 2 and mission < list.get_child_count():
		open.push_front(list.get_child(mission))
	if level == 3:
		open = [ok]
	if not open.is_empty():
		(open[0] as Button).grab_focus.call_deferred()


func _item(text: String, on_press: Callable) -> Button:
	var b := Button.new()
	b.text = text
	b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	b.alignment = HORIZONTAL_ALIGNMENT_LEFT
	b.clip_text = true
	b.pressed.connect(on_press)
	list.add_child(b)
	return b


func _open_lord(id: int) -> void:
	lord_id = id
	mission = 0
	level = 2
	show_level()


func _open_mission(i: int) -> void:
	mission = i
	level = 3
	show_level()


func mission_data() -> Dictionary:
	var ms := campaign.lord_missions(lord_id)
	return ms[mission] if mission >= 0 and mission < ms.size() else {}


## The question before a mission: the general to beat, his level and the mission's gold
## (twice on hard), "Do you want to accept this mission?".
func accept_text() -> String:
	var m := mission_data()
	var general := MapSim.general_data(int(m.get("boss_type", 0)))
	var lv := int(profile.level) + int(m.get("level_bonus", 0))
	var gold := int(m.get("gold", 0)) * 150 * (1 + (int(profile.difficulty) ^ 1))
	return "%s\n%s\n\n%s" % [tr(str(general.get("name", ""))), tr("campaign.level_gold") % [lv, gold],
		tr("campaign.accept")]


func ask_accept() -> void:
	ask.dialog_text = accept_text()
	ask.popup_centered()


## Yes: the mission is accepted, its briefing counted (and saved), then the briefing.
func accept() -> void:
	var line: int = profile.next_briefing(rng)
	profile.save_keeping_map(path)
	Router.push("briefing", {"lord": lord_id, "mission": mission, "line": line, "profile_path": path})


func _unhandled_input(event: InputEvent) -> void:
	if level == 3 and (event.is_action_pressed("ui_up") or event.is_action_pressed("ui_down")):
		# up / down: the description a page back or on (the focus stays on OK)
		get_viewport().set_input_as_handled()
		var page := int(scroll.size.y) - 40
		scroll.scroll_vertical += page if event.is_action_pressed("ui_down") else -page
	elif event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		if level > 1:
			level -= 1
			show_level()
		else:
			Router.back()
