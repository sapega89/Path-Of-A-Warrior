extends Control
## The campaign: the lords the hero can fight for from where he is (the campaign chapter of
## his place), then the missions of a lord. A lord who is not open yet is greyed; a mission
## won has a mark. Winning takes the hero to that lord's place, so the list changes.

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Campaign := preload("res://scripts/core/campaign.gd")
const Profile := preload("res://scripts/core/profile.gd")
const DONE_MARK := "  ✓"

var campaign := Campaign.new()
var profile: RefCounted
var list: VBoxContainer
var heading: Label
## 1 lords of the hero's place, 2 missions of a lord
var level := 1
var chapter := 0
var lord_id := 0


func _ready() -> void:
	var p: Dictionary = Router.params
	profile = Profile.load_or_new(str(p.get("profile_path", Profile.PATH)))
	var col := UiTheme.menu_column(self, 640)
	heading = UiTheme.heading("campaign.lords", 40)
	col.add_child(heading)
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size = Vector2(640, 520)
	scroll.follow_focus = true
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	col.add_child(scroll)
	list = VBoxContainer.new()
	list.name = "List"
	list.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	list.add_theme_constant_override("separation", 6)
	scroll.add_child(list)
	level = clampi(int(p.get("level", 1)), 1, 2)
	chapter = int(p.get("chapter", profile.place))
	lord_id = int(p.get("lord", 0))
	show_level()
	if Cloud.enabled():
		Cloud.game_started()
		if not Cloud.has_account():  # no hero without an account: it lives on the server
			Router.push.call_deferred("register")


func show_level() -> void:
	for c in list.get_children():
		list.remove_child(c)
		c.queue_free()
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
				var text: String = tr("campaign.mission") % [i + 1, ms[i].get("name", "")]
				if profile.is_done(lord_id, i):
					text += DONE_MARK
				_item(text, _start.bind(i))
	for c in list.get_children():
		if not (c as Button).disabled:
			(c as Button).grab_focus.call_deferred()
			break


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
	level = 2
	show_level()


func _start(mission: int) -> void:
	Router.push("mission", {"lord": lord_id, "mission": mission})


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		if level > 1:
			level -= 1
			show_level()
		else:
			Router.back()
