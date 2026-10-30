extends Control
## Ігрове меню (bV == 2): txt_m sprites, m_illu, ui_arrow_menu vertical. Як у Java e.java aJ.

signal enter_game
signal back_to_title

const SUBMENU_SCENES: Array[PackedScene] = [
	preload("res://scenes/menus/mission_menu.tscn"),
	preload("res://scenes/menus/blacksmith_menu.tscn"),
	preload("res://scenes/menus/gamevil_live_menu.tscn"),
	preload("res://scenes/menus/visiting_menu.tscn"),
	preload("res://scenes/menus/management_menu.tscn"),
	preload("res://scenes/menus/etc_menu.tscn"),
]

const MISSION_LORD_SELECT_SCENE: PackedScene = preload("res://scenes/screens/mission_lord_select.tscn")
const MISSION_LIST_SCENE: PackedScene = preload("res://scenes/screens/mission_list_screen.tscn")
const MISSION_BRIEFING_SCENE: PackedScene = preload("res://scenes/screens/mission_briefing_screen.tscn")
const LORD_DIALOG_SCENE: PackedScene = preload("res://scenes/screens/lord_dialog_screen.tscn")
const ALERT_CONFIRM_SCENE: PackedScene = preload("res://scenes/screens/alert_confirm.tscn")
const VISITING_GENERAL_SCENE: PackedScene = preload("res://scenes/screens/visiting_general_screen.tscn")
const MODAL_MESSAGE_SCENE: PackedScene = preload("res://scenes/screens/modal_message.tscn")

const VISITING_CANNOT_VISIT_MSG := "Generals can not be visited at this time. Try again after completing a mission."

const MENU_ITEMS: Array[String] = [
	"Mission",
	"Blacksmith",
	"Gamevil Live",
	"Visiting",
	"Management",
	"ETC"
]

const SUBMENU_CONFIG: Array[Dictionary] = [
	{"title": "Mission", "links": []},
	{"title": "Blacksmith", "links": [{"label": "Buy Item", "action_id": 0}, {"label": "Sell Item", "action_id": 1}, {"label": "Cancel Sell", "action_id": 2}]},
	{"title": "Gamevil Live", "links": [{"label": "Coming Soon", "action_id": 0}]},
	{"title": "Visiting", "links": [{"label": "Select General", "action_id": 0}]},
	{"title": "Management", "links": [{"label": "Attributes", "action_id": 0}, {"label": "Skills", "action_id": 1}, {"label": "Gear", "action_id": 2}, {"label": "Inventory", "action_id": 3}]},
	{"title": "ETC", "links": [{"label": "Save", "action_id": 0}, {"label": "Load", "action_id": 1}]},
]

@onready var _main_layer: Control = $MainLayer
@onready var _menu_content: Control = $MainLayer/MenuContent
@onready var _submenu_layer: Control = $SubmenuLayer

func _ready() -> void:
	if _menu_content != null:
		if _menu_content.has_method("setup_menu_items"):
			_menu_content.setup_menu_items(MENU_ITEMS)
		if _menu_content.has_signal("item_selected"):
			_menu_content.item_selected.connect(_on_item_selected)
		if _menu_content.has_signal("back_requested"):
			_menu_content.back_requested.connect(func(): back_to_title.emit())
	if _submenu_layer != null:
		_submenu_layer.visible = false

func _input(event: InputEvent) -> void:
	_handle_menu_input(event)

func process_menu_input(event: InputEvent) -> void:
	_handle_menu_input(event)

func _handle_menu_input(event: InputEvent) -> void:
	if _menu_content != null and _menu_content.has_method("process_menu_input"):
		_menu_content.process_menu_input(event)

func _on_item_selected(index: int) -> void:
	if index == 0: # Mission — спочатку список місій, потім вибір лорда, бріфінг, саммарі → enter_game
		_open_mission_flow()
		return
	if index == 3: # Visiting
		if not GameState.can_visit_generals:
			_show_visit_blocked_modal()
			return
	var config: Dictionary = SUBMENU_CONFIG[index] if index < SUBMENU_CONFIG.size() else {}
	var links: Array = config.get("links", [])
	if links.is_empty():
		return
	_open_submenu(index)

func _open_mission_flow() -> void:
	## Потік: місія → лорд → бріфінг (текст місії) → підсумок з підтвердженням → діалог з лордом → карта
	if _submenu_layer == null:
		return
	for child in _submenu_layer.get_children():
		child.queue_free()
	var mission_list: Control = MISSION_LIST_SCENE.instantiate()
	mission_list.lord_index = -1
	mission_list.mission_selected.connect(_on_mission_first_selected)
	mission_list.back_to_main.connect(_close_submenu)
	_submenu_layer.add_child(mission_list)
	if _main_layer != null:
		_main_layer.visible = false
	_submenu_layer.visible = true

func _on_mission_first_selected(mission_index: int) -> void:
	GameState.selected_mission_id = mission_index
	for child in _submenu_layer.get_children():
		child.queue_free()
	var lord_select: Control = MISSION_LORD_SELECT_SCENE.instantiate()
	_submenu_layer.add_child(lord_select)
	lord_select.lord_selected.connect(_on_mission_lord_selected)
	lord_select.back_pressed.connect(_on_mission_back_to_mission_list)

func _on_mission_lord_selected(lord_index: int) -> void:
	GameState.selected_lord_id = lord_index
	var mission_name := GameState.get_mission_name(GameState.selected_mission_id)
	var mission_text := _get_mission_briefing_text(mission_name)
	for child in _submenu_layer.get_children():
		child.queue_free()
	var briefing: Control = MISSION_BRIEFING_SCENE.instantiate()
	_submenu_layer.add_child(briefing)
	briefing.set_briefing(mission_name, mission_text)
	briefing.continue_pressed.connect(_on_briefing_continue)
	briefing.back_pressed.connect(_on_briefing_back)

func _on_mission_back_to_mission_list() -> void:
	for child in _submenu_layer.get_children():
		child.queue_free()
	var mission_list: Control = MISSION_LIST_SCENE.instantiate()
	mission_list.lord_index = -1
	mission_list.mission_selected.connect(_on_mission_first_selected)
	mission_list.back_to_main.connect(_close_submenu)
	_submenu_layer.add_child(mission_list)

func _get_mission_briefing_text(_mission_name: String) -> String:
	# Java D(): текст з v(56), a(arrayOfByte1, du[dk]+dm); поки placeholder
	return "Objective: Complete the mission and return. Fulfill all conditions set by your lord."

func _on_briefing_back() -> void:
	for child in _submenu_layer.get_children():
		child.queue_free()
	var lord_select: Control = MISSION_LORD_SELECT_SCENE.instantiate()
	_submenu_layer.add_child(lord_select)
	lord_select.lord_selected.connect(_on_mission_lord_selected)
	lord_select.back_pressed.connect(_on_mission_back_to_mission_list)

func _on_briefing_continue() -> void:
	var mission_name := GameState.get_mission_name(GameState.selected_mission_id)
	var lord_name := GameState.lord_names[GameState.selected_lord_id] if GameState.selected_lord_id >= 0 and GameState.selected_lord_id < GameState.lord_names.size() else ("Lord %d" % (GameState.selected_lord_id + 1))
	var summary_dialog: ConfirmationDialog = ALERT_CONFIRM_SCENE.instantiate()
	summary_dialog.dialog_text = "Ви готові на такі умови місії?\n\n%s / %s" % [mission_name, lord_name]
	summary_dialog.ok_button_text = "Так"
	summary_dialog.cancel_button_text = "Ні"
	add_child(summary_dialog)
	summary_dialog.confirmed.connect(_on_summary_confirmed_show_lord_dialog)
	summary_dialog.canceled.connect(summary_dialog.queue_free)
	summary_dialog.popup_centered()

func _on_summary_confirmed_show_lord_dialog() -> void:
	var dlg: ConfirmationDialog = null
	for child in get_children():
		if child is ConfirmationDialog:
			dlg = child
			break
	if dlg != null:
		dlg.queue_free()
	var lord_name := "Lord %d" % (GameState.selected_lord_id + 1)
	var lord_index: int = GameState.selected_lord_id
	var dialog_text := "I assign you to this mission. Fulfill the objective and return with honour."
	for child in _submenu_layer.get_children():
		child.queue_free()
	var lord_dialog: Control = LORD_DIALOG_SCENE.instantiate()
	_submenu_layer.add_child(lord_dialog)
	lord_dialog.set_lord_dialog(lord_name, lord_index, dialog_text)
	lord_dialog.continue_pressed.connect(_on_lord_dialog_continue)
	lord_dialog.back_pressed.connect(_on_lord_dialog_back)

func _on_lord_dialog_continue() -> void:
	for child in _submenu_layer.get_children():
		child.queue_free()
	_close_submenu()
	enter_game.emit()

func _on_lord_dialog_back() -> void:
	# Повернутися до бріфінгу (текст місії)
	for child in _submenu_layer.get_children():
		child.queue_free()
	var mission_name := GameState.get_mission_name(GameState.selected_mission_id)
	var mission_text := _get_mission_briefing_text(mission_name)
	var briefing: Control = MISSION_BRIEFING_SCENE.instantiate()
	_submenu_layer.add_child(briefing)
	briefing.set_briefing(mission_name, mission_text)
	briefing.continue_pressed.connect(_on_briefing_continue)
	briefing.back_pressed.connect(_on_briefing_back)

func _open_submenu(menu_index: int) -> void:
	if _submenu_layer == null:
		return
	for child in _submenu_layer.get_children():
		child.queue_free()
	var idx := clampi(menu_index, 0, SUBMENU_SCENES.size() - 1)
	var scene_root: Control = SUBMENU_SCENES[idx].instantiate()
	_submenu_layer.add_child(scene_root)
	var shell: Control = scene_root.get_node_or_null("SubmenuShell") if scene_root.get_child_count() > 0 else scene_root
	if shell == null:
		shell = scene_root
	shell.back_pressed.connect(_close_submenu)
	shell.link_selected.connect(_on_submenu_link_selected.bind(menu_index))
	if scene_root.has_signal("general_selected"):
		scene_root.general_selected.connect(_on_general_selected)
	if _main_layer != null:
		_main_layer.visible = false
	if _submenu_layer != null:
		_submenu_layer.visible = true

func _close_submenu() -> void:
	if _submenu_layer != null:
		for child in _submenu_layer.get_children():
			child.queue_free()
		_submenu_layer.visible = false
	if _main_layer != null:
		_main_layer.visible = true

func _push_content_screen(scene: PackedScene) -> void:
	if _submenu_layer == null:
		return
	var screen: Control = scene.instantiate()
	_submenu_layer.add_child(screen)
	if screen.has_signal("closed"):
		screen.closed.connect(screen.queue_free)
	if screen.has_signal("general_selected"):
		screen.general_selected.connect(_on_general_selected)

func _on_general_selected(general_index: int) -> void:
	var screen: Control = VISITING_GENERAL_SCENE.instantiate()
	if screen.get("general_index") != null:
		screen.general_index = general_index
	_submenu_layer.add_child(screen)
	if screen.has_signal("closed"):
		screen.closed.connect(screen.queue_free)

func _show_visit_blocked_modal() -> void:
	var modal: AcceptDialog = MODAL_MESSAGE_SCENE.instantiate()
	add_child(modal)
	modal.set_message(VISITING_CANNOT_VISIT_MSG)
	if modal.has_signal("closed"):
		modal.closed.connect(modal.queue_free)
	modal.popup_centered()

func _show_modal(message: String) -> void:
	var modal: AcceptDialog = MODAL_MESSAGE_SCENE.instantiate()
	add_child(modal)
	modal.set_message(message)
	if modal.has_signal("closed"):
		modal.closed.connect(modal.queue_free)
	modal.popup_centered()

func _show_coming_soon() -> void:
	var modal: AcceptDialog = MODAL_MESSAGE_SCENE.instantiate()
	add_child(modal)
	modal.set_message("Coming soon")
	if modal.has_signal("closed"):
		modal.closed.connect(modal.queue_free)
	modal.popup_centered()

func _on_submenu_link_selected(action_id: int, menu_index: int) -> void:
	match menu_index:
		0:  # Квест
			_close_submenu()
			match action_id:
				0: print("Активні квести - TODO: quest_list screen")
				1: print("Завершені квести - TODO")
		1:  # Blacksmith (Купити, Продати, Скасувати продаж)
			_show_coming_soon()
		2:  # Gamevil Live
			_close_submenu()
			_show_coming_soon()
		3:  # Visiting — таблиця в visiting_menu.tscn, general_selected підключено в _open_submenu
			pass
		4:  # Management
			_close_submenu()
			_show_coming_soon()
		5:  # ETC
			_close_submenu()
			match action_id:
				0:  # Save
					var ok := GameState.save_game()
					_show_modal("Saved!" if ok else "Save failed")
				1:  # Load
					var ok := GameState.load_game()
					_show_modal("Loaded!" if ok else "No save found")
