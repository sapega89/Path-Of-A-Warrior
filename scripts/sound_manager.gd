extends Node
## Музика по екранах (Java: k.java, ae.A): титул=snd0.mid, гра=snd1.mid, меню=snd2.mid.
## MidiPlayer потребує soundfont (.sf2).

const SND_PATHS := {
	"title": "res://snd0.mid",
	"menu": "res://snd2.mid",
	"game": "res://snd1.mid",
}

const SOUNDFONT_PATH := "res://FluidR3_GM.sf2"

var _midi_player: MidiPlayer
var _current_path: String = ""

func _ready() -> void:
	if not FileAccess.file_exists(SOUNDFONT_PATH):
		push_warning("SoundManager: soundfont not found at %s — music disabled" % SOUNDFONT_PATH)
		return
	_midi_player = MidiPlayer.new()
	_midi_player.bus = &"Master"
	_midi_player.volume_db = -3.0
	_midi_player.loop = true
	_midi_player.soundfont = SOUNDFONT_PATH
	add_child(_midi_player)
	_midi_player.finished.connect(_on_midi_finished)

func _on_midi_finished() -> void:
	if _current_path != "":
		_midi_player.play()

func play_music(key: String) -> void:
	if _midi_player == null or not SND_PATHS.has(key):
		return
	var path: String = SND_PATHS[key]
	if _current_path == path and _midi_player.playing:
		return
	_current_path = path
	_midi_player.set_file(path)
	_midi_player.play()

func stop_music() -> void:
	if _midi_player == null:
		return
	_current_path = ""
	_midi_player.stop()

func set_music_volume_db(db: float) -> void:
	_midi_player.volume_db = db
