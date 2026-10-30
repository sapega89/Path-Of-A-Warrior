extends Control
## opening.scr:
##   [0..1]  — narrative scroll (передісторія)
##   [2..12] — dialog mode (діалог у Crimson Temple)
## "..." рядки (3,5,7,9,11) — просто пауза без тексту.

signal finished

const PORTRAIT_PATHS := ["res://ju_1.png", "res://ju_2.png", "res://ju_3.png", "res://ju_4.png"]
const NPC_PORTRAIT   := "res://jang_1.png"
const SCROLL_SPEED   := 28.0  ## px/s
const LAST_NARRATIVE := 1     ## pages 0..1 are narrative, 2+ are dialog

var _pages: Array[String] = []
var _page_index: int = 0
var _tween: Tween = null
var _scroll_done: bool = false

@onready var _narrative_layer: Control        = $NarrativeLayer
@onready var _story_image: TextureRect        = $NarrativeLayer/ImageFrame/StoryImage
@onready var _text_clip: Control              = $NarrativeLayer/TextClip
@onready var _text_label: Label               = $NarrativeLayer/TextClip/TextLabel
@onready var _btn_skip: Button                = $NarrativeLayer/BtnSkip

@onready var _dialog_layer: Control           = $DialogLayer
@onready var _scene_image: TextureRect        = $DialogLayer/SceneImage
@onready var _speaker_portrait: TextureRect   = $DialogLayer/DialogPanel/ContentRow/SpeakerPortrait
@onready var _dialog_text: Label              = $DialogLayer/DialogPanel/ContentRow/DialogText
@onready var _btn_next: Button                = $DialogLayer/DialogPanel/BtnNext


func _ready() -> void:
	_pages = ScrReader.read_all("res://opening.scr")
	if _pages.is_empty():
		_pages = ["(story text not found)"]

	var hero_idx: int = clampi(GameState.hero_index, 0, PORTRAIT_PATHS.size() - 1)
	_story_image.texture  = load(PORTRAIT_PATHS[hero_idx]) as Texture2D
	_scene_image.texture  = load(NPC_PORTRAIT) as Texture2D
	_speaker_portrait.texture = load(NPC_PORTRAIT) as Texture2D

	_btn_skip.pressed.connect(_on_skip)
	_btn_next.pressed.connect(_on_next)
	_page_index = 0
	_show_page()


func _show_page() -> void:
	var text: String = _pages[_page_index]
	var is_narrative: bool = (_page_index <= LAST_NARRATIVE)

	_narrative_layer.visible = is_narrative
	_dialog_layer.visible    = not is_narrative

	if is_narrative:
		_scroll_done = false
		_text_label.text = text
		_btn_skip.grab_focus()
		await get_tree().process_frame
		_start_scroll()
	else:
		_dialog_text.text = text
		_btn_next.grab_focus()


func _start_scroll() -> void:
	if _tween != null:
		_tween.kill()
	var clip_h: float  = _text_clip.size.y
	var label_h: float = _text_label.size.y
	_text_label.position = Vector2(0.0, clip_h)
	var end_y: float    = -label_h
	var distance: float = clip_h + label_h
	_tween = create_tween()
	_tween.tween_property(_text_label, "position:y", end_y, distance / SCROLL_SPEED)
	_tween.tween_callback(func() -> void: _scroll_done = true)


func _on_skip() -> void:
	if not _scroll_done:
		if _tween != null:
			_tween.kill()
		_text_label.position = Vector2(0.0, minf(0.0, _text_clip.size.y - _text_label.size.y))
		_scroll_done = true
	else:
		_advance()


func _on_next() -> void:
	_advance()


func _advance() -> void:
	var next: int = _page_index + 1
	# skip "..." separators automatically
	while next < _pages.size() and _pages[next].strip_edges() == "...":
		next += 1
	if next < _pages.size():
		_page_index = next
		_show_page()
	else:
		finished.emit()


func _input(event: InputEvent) -> void:
	if event.is_action_pressed(&"menu_confirm") or event.is_action_pressed(&"ui_cancel"):
		if _page_index <= LAST_NARRATIVE:
			_on_skip()
		else:
			_advance()
		get_viewport().set_input_as_handled()
