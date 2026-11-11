class_name Dialogue
extends VBoxContainer
## Two who talk (scenes/ui/dialogue.tscn): the speaker's portrait and words at the top, the
## hero's words and portrait at the bottom, as in a briefing or a visit.
## say() types a line out into one of the two boxes with a Tween (the other box keeps its last
## line whole); once the line is whole it stays a while, then `line_done` is emitted.

## The line said is whole and has stayed its while (or a press asked for the next one).
signal line_done

const CHARS_PER_SECOND := 40.0

var typing: Label  # the box the last line went into
var tween: Tween  # the typing and the stay after it

@onready var speaker_portrait: TextureRect = $Top/SpeakerPortrait
@onready var speaker_says: Label = $Top/SpeakerSays
@onready var hero_says: Label = $Bottom/HeroSays
@onready var hero_portrait: TextureRect = $Bottom/HeroPortrait


## Types `line` into `box` (speaker_says or hero_says); once it is whole it stays `stay`
## seconds before `line_done`.
func say(box: Label, line: String, stay: float) -> void:
	stop()
	if typing != null:
		typing.visible_characters = -1
	typing = box
	box.text = line
	box.visible_characters = 0
	tween = create_tween()
	tween.tween_property(box, "visible_ratio", 1.0, line.length() / CHARS_PER_SECOND).from(0.0)
	tween.tween_interval(stay)
	tween.tween_callback(line_done.emit)


## While a line is typed: the whole line at once, which then stays `stay` seconds; once it is
## whole: `line_done` at once.
func press(stay: float) -> void:
	stop()
	if is_typing():
		typing.visible_characters = -1
		tween = create_tween()
		tween.tween_interval(stay)
		tween.tween_callback(line_done.emit)
	else:
		line_done.emit()


func is_typing() -> bool:
	return typing != null and typing.visible_characters >= 0


## No more typing and no `line_done` for the line said.
func stop() -> void:
	if tween != null:
		tween.kill()
		tween = null
