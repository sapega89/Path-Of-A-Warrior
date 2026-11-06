extends Control
## Picking a mission from the original campaign: chapter -> lord -> mission.
## (The original's own Game Menu flow is ported later; this list opens every mission.)

const UiTheme := preload("res://scripts/ui/ui_theme.gd")
const Campaign := preload("res://scripts/core/campaign.gd")

var campaign := Campaign.new()
var list: VBoxContainer
var heading: Label
## 0 chapters, 1 lords of a chapter, 2 missions of a lord
var level := 0
var chapter := 0
var lord_id := 0


func _ready() -> void:
	var col := UiTheme.menu_column(self, 640)
	heading = UiTheme.heading("campaign.chapters", 40)
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
	var p: Dictionary = Router.params
	level = int(p.get("level", 0))
	chapter = int(p.get("chapter", 0))
	lord_id = int(p.get("lord", 0))
	show_level()


func show_level() -> void:
	for c in list.get_children():
		list.remove_child(c)
		c.queue_free()
	match level:
		0:
			heading.text = "campaign.chapters"
			for i in campaign.chapters.size():
				var names: Array = campaign.chapter_lords(i).map(func(id): return campaign.lord_name(id))
				_item(tr("campaign.chapter") % (i + 1) + "  " + ", ".join(names), _open_chapter.bind(i))
		1:
			heading.text = tr("campaign.chapter") % (chapter + 1)
			for id in campaign.chapter_lords(chapter):
				_item(campaign.lord_name(id), _open_lord.bind(int(id)))
		2:
			heading.text = campaign.lord_name(lord_id)
			var ms := campaign.lord_missions(lord_id)
			for i in ms.size():
				_item(tr("campaign.mission") % [i + 1, ms[i].get("name", "")], _start.bind(i))
	if list.get_child_count() > 0:
		(list.get_child(0) as Button).grab_focus.call_deferred()


func _item(text: String, on_press: Callable) -> void:
	var b := Button.new()
	b.text = text
	b.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	b.alignment = HORIZONTAL_ALIGNMENT_LEFT
	b.clip_text = true
	b.pressed.connect(on_press)
	list.add_child(b)


func _open_chapter(i: int) -> void:
	chapter = i
	level = 1
	show_level()


func _open_lord(id: int) -> void:
	lord_id = id
	level = 2
	show_level()


func _start(mission: int) -> void:
	Router.push("mission", {"lord": lord_id, "mission": mission})


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("ui_cancel"):
		get_viewport().set_input_as_handled()
		if level > 0:
			level -= 1
			show_level()
		else:
			Router.back()
