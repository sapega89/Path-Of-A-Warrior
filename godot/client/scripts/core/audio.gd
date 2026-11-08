extends Node
## The music and the sound effects: the three tunes (0 the title, 1 the missions, 2 the
## menus) and the effects 3..16, from assets/original/sound (godot/tools/import_original.py).
## Each screen has its tune (SCREEN_MUSIC); the story chooses its own by the page. A tune
## asked for again goes on playing. An effect cuts off the effects still playing, except
## the short hits (OVERLAPPING); after effect 9 nothing new plays for half a second.

const MUSIC_PATH := "res://assets/original/sound/music_%d.ogg"
const SFX_PATH := "res://assets/original/sound/sfx_%d.wav"
const SCREEN_MUSIC := {
	"title": 0, "main_menu": 0, "game_menu": 2, "mission": 1, "campaign": 2, "settings": 2, "management": 2,
	"attributes": 2, "skills": 2, "blacksmith": 2, "shop": 2, "gear": 2, "inventory": 2, "assign_items": 2,
	"live_warehouse": -1, "live_safe": -1, "live_trade": -1, "live_buy": -1,  # Live is quiet
	"live_sell": -1, "live_cancel": -1, "online_character": -1, "online_skills": -1,
	"online_text": -1, "online_ranking": -1, "online_order": -1, "online_chat": -1, "online_options": -1,
	"online_battle": -1, "online_battles": -1,
}
const OVERLAPPING := [3, 4, 15, 16]
const MIN_GAP_MS := {9: 500}
const PLAYERS := 4

var music := -1
## The effects played, the newest last (at most 32).
var played: Array[int] = []
var _music_player: AudioStreamPlayer
var _sfx: Array[AudioStreamPlayer] = []
var _streams := {}
var _last := -1
var _last_time := 0


func _ready() -> void:
	_music_player = AudioStreamPlayer.new()
	_music_player.name = "Music"
	_music_player.bus = &"Music"
	add_child(_music_player)
	for i in PLAYERS:
		var p := AudioStreamPlayer.new()
		p.name = "Sfx%d" % i
		p.bus = &"SFX"
		add_child(p)
		_sfx.append(p)
	Router.screen_changed.connect(_on_screen_changed)


func play_music(tune: int) -> void:
	if tune == music:
		return
	music = tune
	_music_player.stop()
	if tune < 0:
		return
	var stream := _stream(MUSIC_PATH % tune)
	if stream is AudioStreamOggVorbis:
		(stream as AudioStreamOggVorbis).loop = true
	_music_player.stream = stream
	if stream != null:
		_music_player.play()


## Plays effect n (3..16), at a pitch and a volume (dB) of its own (the hits on the map vary
## them a little: scripts/world/combat_feel.gd). False when it is held back by the one before.
func play_sound(n: int, pitch: float = 1.0, volume_db: float = 0.0) -> bool:
	var now := Time.get_ticks_msec()
	if _last != -1 and MIN_GAP_MS.has(_last) and now - _last_time < int(MIN_GAP_MS[_last]):
		return false
	_last = n
	_last_time = now
	played.append(n)
	if played.size() > 32:
		played.pop_front()
	if n not in OVERLAPPING:
		for p in _sfx:
			p.stop()
	var free: AudioStreamPlayer = _sfx[0]
	for p in _sfx:
		if not p.playing:
			free = p
			break
	free.stream = _stream(SFX_PATH % n)
	free.pitch_scale = pitch
	free.volume_db = volume_db
	if free.stream != null:
		free.play()
	return true


func _stream(path: String) -> AudioStream:
	if not _streams.has(path):
		_streams[path] = load(path) if ResourceLoader.exists(path) else null
	return _streams[path]


func _on_screen_changed(screen_name: String) -> void:
	if SCREEN_MUSIC.has(screen_name):
		play_music(int(SCREEN_MUSIC[screen_name]))
