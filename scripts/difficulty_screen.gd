extends Control
## Екран вибору складності. Shell+Config налаштовано в сцені (menu_id=6).

signal difficulty_confirmed(index: int)
signal back_requested

@onready var _shell: Control = $SubmenuShell

func _ready() -> void:
	_shell.link_selected.connect(func(id: int) -> void: difficulty_confirmed.emit(id))
	_shell.back_pressed.connect(func() -> void: back_requested.emit())
