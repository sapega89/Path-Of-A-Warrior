class_name Dialogue
extends VBoxContainer
## Two who talk (scenes/ui/dialogue.tscn): the speaker's portrait and words at the top, the
## hero's words and portrait at the bottom, as in a briefing or a visit.

@onready var speaker_portrait: TextureRect = $Top/SpeakerPortrait
@onready var speaker_says: Label = $Top/SpeakerSays
@onready var hero_says: Label = $Bottom/HeroSays
@onready var hero_portrait: TextureRect = $Bottom/HeroPortrait
