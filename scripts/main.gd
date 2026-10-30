extends Control
## Корень: титул → игровое меню (квест, магазин, кузнец…) → по «В игру» — мир (bV: 2 → 0).

const TITLE_SCENE := preload("res://scenes/title/title_screen.tscn")
const LICENSE_SCENE := preload("res://scenes/screens/license_screen.tscn")
const HELP_SCENE := preload("res://scenes/screens/help_screen.tscn")
const OPTIONS_SCENE := preload("res://scenes/screens/options_screen.tscn")
const ENDINGS_SCENE := preload("res://scenes/menus/endings_screen.tscn")
const SUBMENU_SHELL_SCENE := preload("res://scenes/submenu_shell.tscn")
const HERO_SELECTION_SCENE := preload("res://scenes/game/hero_selection.tscn")
const DIFFICULTY_SCENE := preload("res://scenes/menus/difficulty_screen.tscn")
const NAME_SCENE := preload("res://scenes/screens/name_screen.tscn")
const STATS_SCENE := preload("res://scenes/screens/stats_screen.tscn")
const STORY_SCENE := preload("res://scenes/screens/story_screen.tscn")
const GAME_MENU_SCENE := preload("res://scenes/game/game_menu.tscn")
const GAME_SCENE := preload("res://scenes/game/game.tscn")

## Базові стати нової гри (з Java: ag.aw() — однакові для всіх героїв).
const HERO_BASE_STATS := {"atk": 5, "def": 4, "hp": 30, "mp": 10, "points_left": 5}

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
	if title.has_signal("show_about"):
		title.show_about.connect(_show_about)
	if title.has_signal("show_more_games"):
		title.show_more_games.connect(_show_more_games)
	if title.has_signal("show_multiplayer"):
		title.show_multiplayer.connect(_show_multiplayer)

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

func _show_about() -> void:
	_clear_viewport()
	var about_scn: Control = LICENSE_SCENE.instantiate()
	_viewport.add_child(about_scn)
	about_scn.closed.connect(_show_title)

func _show_more_games() -> void:
	_clear_viewport()
	var stub: Control = SUBMENU_SHELL_SCENE.instantiate()
	stub.set_menu("More Games", [])
	stub.set_content_message("More Games — coming soon.")
	_viewport.add_child(stub)
	stub.closed.connect(_show_title)

func _show_multiplayer() -> void:
	_clear_viewport()
	var stub: Control = SUBMENU_SHELL_SCENE.instantiate()
	stub.set_menu("Multiplayer", [])
	stub.set_content_message("Multiplayer — coming soon.")
	_viewport.add_child(stub)
	stub.closed.connect(_show_title)

func _start_new_game() -> void:
	GameState.stat_fame = 0
	GameState.player_name = ""
	_show_difficulty()

func _show_difficulty() -> void:
	_clear_viewport()
	var screen: Control = DIFFICULTY_SCENE.instantiate()
	_viewport.add_child(screen)
	screen.difficulty_confirmed.connect(_on_difficulty_confirmed)
	screen.back_requested.connect(_show_title)

func _on_difficulty_confirmed(difficulty_index: int) -> void:
	GameState.difficulty_index = difficulty_index
	_show_hero_selection()

func _show_hero_selection() -> void:
	_clear_viewport()
	var screen: Control = HERO_SELECTION_SCENE.instantiate()
	_viewport.add_child(screen)
	screen.hero_selected.connect(_on_hero_selected)
	screen.back_requested.connect(_show_difficulty)

func _on_hero_selected(_hero_index: int) -> void:
	GameState.stat_atk = HERO_BASE_STATS.atk
	GameState.stat_def = HERO_BASE_STATS.def
	GameState.stat_hp = HERO_BASE_STATS.hp
	GameState.stat_mp = HERO_BASE_STATS.mp
	GameState.stat_points_left = HERO_BASE_STATS.points_left
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
