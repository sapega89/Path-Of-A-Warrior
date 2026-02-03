extends Control
## Вікно розподілу статів (cM[0]==8). cz.k, cz.l, cz.F, портрет, cz.m/n/o/q (ae.aR), cz.J.

signal stats_confirmed
signal back_requested

const STAT_LABELS := ["Atk Up : ", "Def Up : ", "HP Up : ", "MP Up : "]
const STAT_INCREMENTS := [1, 1, 5, 3]
const PORTRAIT_PATHS := ["res://char_head1.png", "res://char_head2.png", "res://char_head3.png", "res://char_head4.png"]

var _selected_row: int = 0

@onready var _label_name: Label = $Margin/VBox/InfoRow/NameLabel
@onready var _label_level: Label = $Margin/VBox/InfoRow/LevelLabel
@onready var _portrait: TextureRect = $Margin/VBox/StatsRow/PortraitWrap/Portrait
@onready var _stat_labels: Array[Label] = []
@onready var _label_points: Label = $Margin/VBox/PointsLabel
@onready var _btn_confirm: Button = $Margin/VBox/BottomRow/BtnConfirm
@onready var _btn_back: Button = $Margin/VBox/BottomRow/BtnBack


func _ready() -> void:
	_stat_labels = [
		$Margin/VBox/StatsRow/StatsVBox/Stat0,
		$Margin/VBox/StatsRow/StatsVBox/Stat1,
		$Margin/VBox/StatsRow/StatsVBox/Stat2,
		$Margin/VBox/StatsRow/StatsVBox/Stat3
	]
	_selected_row = 0
	_refresh_display()
	_btn_confirm.pressed.connect(_on_confirm)
	_btn_back.pressed.connect(_on_back)
	_btn_confirm.grab_focus()


func _input(event: InputEvent) -> void:
	if GameState.stat_points_left <= 0:
		if event.is_action_pressed(&"ui_cancel"):
			_on_back()
			get_viewport().set_input_as_handled()
		return
	if event.is_action_pressed(&"menu_prev") or event.is_action_pressed(&"menu_next"):
		_selected_row = clampi(_selected_row + (1 if event.is_action_pressed(&"menu_next") else -1), 0, 3)
		_refresh_display()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"ui_cancel"):
		_on_back()
		get_viewport().set_input_as_handled()


func process_menu_input(event: InputEvent) -> void:
	if GameState.stat_points_left <= 0:
		if event.is_action_pressed(&"ui_cancel"):
			_on_back()
			get_viewport().set_input_as_handled()
		return
	if event.is_action_pressed(&"menu_prev"):
		_selected_row = clampi(_selected_row - 1, 0, 3)
		_refresh_display()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"menu_next"):
		_selected_row = clampi(_selected_row + 1, 0, 3)
		_refresh_display()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"ui_cancel"):
		_on_back()
		get_viewport().set_input_as_handled()


func _refresh_display() -> void:
	_label_name.text = GameState.player_name if GameState.player_name else "Hero"
	_label_level.text = "Lv.1  Fame: %d" % GameState.stat_fame
	var tex: Texture2D = load(PORTRAIT_PATHS[GameState.hero_index]) as Texture2D
	if tex != null:
		_portrait.texture = tex
		_portrait.visible = true
	else:
		_portrait.visible = false
	var vals: Array[int] = [GameState.stat_atk, GameState.stat_def, GameState.stat_hp, GameState.stat_mp]
	for i in 4:
		var prefix: String = "> " if i == _selected_row else "  "
		_stat_labels[i].text = prefix + STAT_LABELS[i] + str(vals[i])
		if i == _selected_row and GameState.stat_points_left > 0:
			_stat_labels[i].add_theme_color_override("font_color", Color(1.0, 0.55, 0.0))
		else:
			_stat_labels[i].add_theme_color_override("font_color", Color(1, 1, 1))
	_label_points.text = "Points left: %d" % GameState.stat_points_left if GameState.stat_points_left > 0 else "Done. Press OK to continue."
	if GameState.stat_points_left > 0:
		_btn_confirm.text = "Add point"
	else:
		_btn_confirm.text = "OK"


func _on_confirm() -> void:
	if GameState.stat_points_left > 0:
		GameState.stat_points_left -= 1
		match _selected_row:
			0: GameState.stat_atk += STAT_INCREMENTS[0]
			1: GameState.stat_def += STAT_INCREMENTS[1]
			2: GameState.stat_hp += STAT_INCREMENTS[2]
			3: GameState.stat_mp += STAT_INCREMENTS[3]
		_refresh_display()
	else:
		stats_confirmed.emit()


func _on_back() -> void:
	back_requested.emit()
