extends Control
## Вікно розподілу статів (cM[0]==8). cz.k, cz.l, cz.F, портрет, cz.m/n/o/q (ae.aR), cz.J.

signal stats_confirmed
signal back_requested

const STAT_LABELS := ["  Atk", "  Def", "  HP ", "  MP "]
const STAT_INCREMENTS := [1, 1, 5, 3]
const PORTRAIT_PATHS := ["res://ju_1.png", "res://ju_2.png", "res://ju_3.png", "res://ju_4.png"]

var _selected_row: int = 0

@onready var _shell: Control = $SubmenuShell
@onready var _label_name: Label = $SubmenuShell/MainLayer/MenuFrame/LinksVBox/InfoRow/InfoVBox/NameLabel
@onready var _label_level: Label = $SubmenuShell/MainLayer/MenuFrame/LinksVBox/InfoRow/InfoVBox/LevelLabel
@onready var _portrait: TextureRect = $SubmenuShell/MainLayer/MenuFrame/LinksVBox/InfoRow/Portrait
@onready var _label_points: Label = $SubmenuShell/MainLayer/MenuFrame/LinksVBox/PointsLabel
@onready var _btn_confirm: Button = $SubmenuShell/MainLayer/MenuFrame/LinksVBox/BtnConfirm


func _ready() -> void:
	_shell.set_title("STATS")
	_shell.back_pressed.connect(func() -> void: back_requested.emit())
	_selected_row = 0
	_refresh_display()
	_btn_confirm.pressed.connect(_on_confirm)
	_btn_confirm.grab_focus()


func _input(event: InputEvent) -> void:
	if GameState.stat_points_left <= 0:
		return
	if event.is_action_pressed(&"menu_prev"):
		_selected_row = clampi(_selected_row - 1, 0, 3)
		_refresh_display()
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed(&"menu_next"):
		_selected_row = clampi(_selected_row + 1, 0, 3)
		_refresh_display()
		get_viewport().set_input_as_handled()


func _refresh_display() -> void:
	_label_name.text = GameState.player_name if GameState.player_name else "Hero"
	_label_level.text = "Lv.1  Fame: %d" % GameState.stat_fame
	var idx: int = clampi(GameState.hero_index, 0, PORTRAIT_PATHS.size() - 1)
	var tex: Texture2D = load(PORTRAIT_PATHS[idx]) as Texture2D
	if tex != null:
		_portrait.texture = tex
		_portrait.visible = true
	else:
		_portrait.visible = false
	var stat_nodes: Array[Label] = [
		$SubmenuShell/MainLayer/MenuFrame/LinksVBox/StatsVBox/Stat0,
		$SubmenuShell/MainLayer/MenuFrame/LinksVBox/StatsVBox/Stat1,
		$SubmenuShell/MainLayer/MenuFrame/LinksVBox/StatsVBox/Stat2,
		$SubmenuShell/MainLayer/MenuFrame/LinksVBox/StatsVBox/Stat3,
	]
	var vals: Array[int] = [GameState.stat_atk, GameState.stat_def, GameState.stat_hp, GameState.stat_mp]
	for i in 4:
		var sel: bool = (i == _selected_row) and GameState.stat_points_left > 0
		var prefix: String = ">" if sel else " "
		stat_nodes[i].text = "%s%s : %d  (+%d)" % [prefix, STAT_LABELS[i], vals[i], STAT_INCREMENTS[i]]
		if i == _selected_row and GameState.stat_points_left > 0:
			stat_nodes[i].add_theme_color_override("font_color", Color(1.0, 0.55, 0.0))
		else:
			stat_nodes[i].remove_theme_color_override("font_color")
	if GameState.stat_points_left > 0:
		_label_points.text = "Points left: %d" % GameState.stat_points_left
		_btn_confirm.text = "Add point"
	else:
		_label_points.text = "Done. Press OK to continue."
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
