extends Control
## Корень: титул → игровое меню (квест, магазин, кузнец…) → по «В игру» — мир (bV: 2 → 0).

const TITLE_SCENE := preload("res://scenes/title_screen.tscn")
const LICENSE_SCENE := preload("res://scenes/license_screen.tscn")
const HELP_SCENE := preload("res://scenes/help_screen.tscn")
const OPTIONS_SCENE := preload("res://scenes/options_screen.tscn")
const ENDINGS_SCENE := preload("res://scenes/endings_screen.tscn")
const HERO_SELECTION_SCENE := preload("res://scenes/hero_selection.tscn")
const DIFFICULTY_SCENE := preload("res://scenes/difficulty_screen.tscn")
const NAME_SCENE := preload("res://scenes/name_screen.tscn")
const STATS_SCENE := preload("res://scenes/stats_screen.tscn")
const STORY_SCENE := preload("res://scenes/story_screen.tscn")
const GAME_MENU_SCENE := preload("res://scenes/game_menu.tscn")
const GAME_SCENE := preload("res://scenes/game.tscn")

@onready var _viewport: SubViewport = $GameContainer/SubViewport

func _ready() -> void:
	_show_title()

func _input(event: InputEvent) -> void:
	# На ПК клава/геймпад идут в корневой viewport — пробрасываем в меню (титул или game_menu)
	if not event is InputEventKey and not event is InputEventJoypadButton and not event is InputEventJoypadMotion:
		return
	var cur := _viewport.get_child(0)
	if cur != null and cur.has_method("process_menu_input"):
		cur.process_menu_input(event)

func _show_title() -> void:
	SoundManager.play_music("title")
	_clear_viewport()
	var title: Control = TITLE_SCENE.instantiate()
	_viewport.add_child(title)
	title.start_game.connect(_on_show_game_menu)
	title.exit_game.connect(_on_exit_game)
	if title.has_signal("new_game"):
		title.new_game.connect(_start_new_game)
	if title.has_signal("show_license"):
		title.show_license.connect(_show_license)
	if title.has_signal("show_help"):
		title.show_help.connect(_show_help)
	if title.has_signal("show_options"):
		title.show_options.connect(_show_options)
	if title.has_signal("show_endings"):
		title.show_endings.connect(_show_endings)

func _show_license() -> void:
	_clear_viewport()
	var license_scn: Control = LICENSE_SCENE.instantiate()
	_viewport.add_child(license_scn)
	license_scn.closed.connect(_show_title)

func _show_help() -> void:
	_clear_viewport()
	var help_scn: Control = HELP_SCENE.instantiate()
	_viewport.add_child(help_scn)
	help_scn.closed.connect(_show_title)

func _show_options() -> void:
	_clear_viewport()
	var options_scn: Control = OPTIONS_SCENE.instantiate()
	_viewport.add_child(options_scn)
	options_scn.closed.connect(_show_title)

func _show_endings() -> void:
	_clear_viewport()
	var endings_scn: Control = ENDINGS_SCENE.instantiate()
	_viewport.add_child(endings_scn)
	endings_scn.closed.connect(_show_title)

func _start_new_game() -> void:
	GameState.stat_atk = 1
	GameState.stat_def = 1
	GameState.stat_hp = 5
	GameState.stat_mp = 3
	GameState.stat_fame = 0
	GameState.stat_points_left = 5
	_show_hero_selection()

func _show_hero_selection() -> void:
	_clear_viewport()
	var screen: Control = HERO_SELECTION_SCENE.instantiate()
	_viewport.add_child(screen)
	screen.hero_selected.connect(_on_hero_selected)
	screen.back_requested.connect(_show_title)

func _on_hero_selected(_hero_index: int) -> void:
	_show_difficulty()

func _show_difficulty() -> void:
	_clear_viewport()
	var screen: Control = DIFFICULTY_SCENE.instantiate()
	_viewport.add_child(screen)
	screen.difficulty_confirmed.connect(_on_difficulty_confirmed)
	screen.back_requested.connect(_show_title)

func _on_difficulty_confirmed(_difficulty_index: int) -> void:
	_show_name_screen()

func _show_name_screen() -> void:
	_clear_viewport()
	var screen: Control = NAME_SCENE.instantiate()
	_viewport.add_child(screen)
	screen.name_confirmed.connect(_on_name_confirmed)
	screen.back_requested.connect(_show_title)

func _on_name_confirmed(_player_name: String) -> void:
	_show_stats_screen()

func _show_stats_screen() -> void:
	_clear_viewport()
	var screen: Control = STATS_SCENE.instantiate()
	_viewport.add_child(screen)
	screen.stats_confirmed.connect(_on_stats_confirmed)
	screen.back_requested.connect(_show_title)

func _on_stats_confirmed() -> void:
	_show_story()

func _show_story() -> void:
	_clear_viewport()
	var story: Control = STORY_SCENE.instantiate()
	_viewport.add_child(story)
	story.finished.connect(_on_story_finished)

func _on_story_finished() -> void:
	_on_show_game_menu()

func _on_show_game_menu() -> void:
	SoundManager.play_music("menu")
	_clear_viewport()
	var menu: Control = GAME_MENU_SCENE.instantiate()
	_viewport.add_child(menu)
	menu.enter_game.connect(_on_enter_game)
	if menu.has_signal("back_to_title"):
		menu.back_to_title.connect(_show_title)

func _on_enter_game() -> void:
	SoundManager.play_music("game")
	_clear_viewport()
	var game: Node2D = GAME_SCENE.instantiate()
	_viewport.add_child(game)

func _clear_viewport() -> void:
	for child in _viewport.get_children():
		child.queue_free()

func _on_exit_game() -> void:
	SoundManager.stop_music()
	get_tree().quit()
