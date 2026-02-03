extends Control
## Екран оповіді (opening story) перед грою. Текст — з gamestr.scr індекс 38 (ag.ga) або 41 (ag.fZ).

signal finished

@onready var _story_label: Label = $Margin/VBox/Scroll/StoryText
@onready var _btn_continue: Button = $Margin/VBox/Bottom/BtnContinue

## Текст історії (за замовчуванням placeholder; пізніше — з gamestr.scr)
var story_text: String = ""

func _ready() -> void:
	if story_text.is_empty():
		story_text = _story_label.text
	_story_label.text = story_text
	_btn_continue.pressed.connect(_on_continue)
	_btn_continue.focus_mode = Control.FOCUS_ALL
	_btn_continue.grab_focus()

func _input(event: InputEvent) -> void:
	if event.is_action_pressed(&"menu_confirm"):
		_finish()
		get_viewport().set_input_as_handled()

func process_menu_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"menu_confirm"):
		_finish()
		get_viewport().set_input_as_handled()

func _on_continue() -> void:
	_finish()

func _finish() -> void:
	finished.emit()
