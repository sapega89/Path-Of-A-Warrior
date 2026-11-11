class_name CampaignScreen
extends BaseScreen
## The campaign: the world map (world_map_view.tscn) with the hero's place and the
## places he can go to from there, then the missions of a place (a lord: one map). A place
## that is not open yet is dark; a mission won has a mark. Winning takes the hero to that
## place, so the map changes. A mission shows its description first; OK asks whether to accept it
## (the general to beat, the level and the
## gold), and Yes counts the briefing and opens it, then the map. Opened from a camp
## (Router.params camp: true) it shows the story of the mission the way led to, OK goes
## straight to its briefing (in its place, so the mission ends back in the camp) and Back
## returns to the camp.
## Back under the list goes a level up, as BACK does.

const DONE_MARK := "  ✓"
const ROW_SCENE := preload("res://screens/campaign/mission_row.tscn")

var campaign := Campaign.new()
var profile: Profile
## 1 the world map at the hero's place, 2 missions of a lord, 3 the description of a mission
var level := 1
var chapter := 0
var lord_id := 0
var mission := 0
var path: String = Profile.PATH
var from_camp := false
var rng := RandomNumberGenerator.new()

@onready var list: VBoxContainer = %List
@onready var world_view: WorldMapView = %WorldMap  # level 1
@onready var heading: Label = %Heading
@onready var scroll: ScrollContainer = %Scroll
@onready var ok: Button = %Ok  # under the description: accept the mission?
@onready var ask: AskDialog = %Ask
@onready var mission_title: Label = %Mission  # the description's two lines, under the list
@onready var description: Label = %Description
@onready var column: Control = %Center  # the list, the missions and the description


func _ready() -> void:
	var p: Dictionary = Router.params
	path = profile_path()
	profile = Profile.load_or_new(path)
	if p.has("seed"):
		rng.seed = int(p.seed)
	level = clampi(int(p.get("level", 1)), 1, 3)
	chapter = int(p.get("chapter", profile.place))
	lord_id = int(p.get("lord", 0))
	mission = int(p.get("mission", 0))
	from_camp = bool(p.get("camp", false))
	world_view.setup(WorldMap.new(campaign), profile, chapter)
	show_level()


func show_level() -> void:
	for c in _rows():
		list.remove_child(c)
		c.queue_free()
	ok.visible = level == 3
	mission_title.visible = level == 3
	description.visible = level == 3
	scroll.scroll_vertical = 0
	world_view.visible = level == 1
	scroll.visible = level != 1
	column.set_anchors_and_offsets_preset(
		Control.PRESET_TOP_WIDE if level == 1 else Control.PRESET_FULL_RECT
	)
	match level:
		1:
			heading.text = "campaign.world"
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
			mission_title.text = str(m.get("name", ""))
			description.text = I18n.text(m.get("description", ""))
	# The focus: the first one open; back from a description, that mission; OK on one.
	var rows := _rows()
	var open := rows.filter(func(c: Button) -> bool: return not c.disabled)
	if level == 2 and mission < rows.size():
		open.push_front(rows[mission])
	if level == 3:
		open = [ok]
	if level == 1:
		world_view.focus_first.call_deferred()
		return
	if not open.is_empty():
		(open[0] as Button).grab_focus.call_deferred()


## A mission of the list (mission_row.tscn), before the description's two lines.
func _item(text: String, on_press: Callable) -> Button:
	var b: Button = ROW_SCENE.instantiate()
	b.text = text
	b.pressed.connect(on_press)
	list.add_child(b)
	list.move_child(b, mission_title.get_index())
	return b


## The missions in the list now.
func _rows() -> Array[Node]:
	return list.get_children().filter(func(c: Node) -> bool: return c is Button)


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
	return (
		"%s\n%s\n\n%s"
		% [
			tr(str(general.get("name", ""))),
			tr("campaign.level_gold") % [lv, gold],
			tr("campaign.accept")
		]
	)


## OK under the description: from a camp the story goes straight on to the briefing.
func _on_ok() -> void:
	if from_camp:
		accept()
	else:
		ask_accept()


func ask_accept() -> void:
	ask.dialog_text = accept_text()
	ask.popup_centered()


## Yes: the mission is accepted, its briefing counted (and saved), then the briefing.
func accept() -> void:
	var line: int = profile.next_briefing(rng)
	profile.save_keeping_map(path)
	var go := Router.replace if from_camp else Router.push
	go.call("briefing", {"lord": lord_id, "mission": mission, "line": line, "profile_path": path})


func _screen_input(event: InputEvent) -> void:
	if level == 3 and (event.is_action_pressed("ui_up") or event.is_action_pressed("ui_down")):
		# up / down: the description a page back or on (the focus stays on OK)
		get_viewport().set_input_as_handled()
		var page := int(scroll.size.y) - 40
		scroll.scroll_vertical += page if event.is_action_pressed("ui_down") else -page


## Back (the button or BACK): the list before, or out of the campaign.
func go_back() -> void:
	if level > 1 and not from_camp:
		level -= 1
		show_level()
	else:
		Router.back()
