extends "res://tests/test_case.gd"


func test_the_sounds_are_there() -> void:
	for tune: String in Audio.TUNES:
		check(ResourceLoader.exists(Audio.MUSIC_PATH % tune), tune)
	for n in range(3, 17):
		check(ResourceLoader.exists(Audio.SFX_PATH % n), "effect %d" % n)


func test_the_tunes_are_long_loops() -> void:
	for tune: String in Audio.TUNES:
		var stream := load(Audio.MUSIC_PATH % tune) as AudioStreamOggVorbis
		check(stream != null and stream.get_length() > 60.0, "%s goes on over a minute" % tune)
	Audio.play_music(-1)
	Audio.play_music(1)
	var playing := Audio.get_node("Music") as AudioStreamPlayer
	check((playing.stream as AudioStreamOggVorbis).loop, "and plays round and round")
	Audio.play_music(-1)


func test_each_screen_has_its_tune() -> void:
	Audio.play_music(-1)
	Audio._on_screen_changed("title")
	eq(Audio.music, 0, "the title")
	Audio._on_screen_changed("campaign")
	eq(Audio.music, 2, "the menus")
	Audio._on_screen_changed("mission")
	eq(Audio.music, 1, "a mission")
	Audio._on_screen_changed("camp")
	eq(Audio.music, 2, "the camp has the menus' tune")
	Audio._on_screen_changed("mission")
	Audio._on_screen_changed("story")
	eq(Audio.music, 1, "the story chooses its own")
	Audio.play_music(-1)
	eq(Audio.music, -1, "stopped")


func test_nothing_plays_just_after_effect_9() -> void:
	Audio._last = -1
	check(Audio.play_sound(15), "a strike plays")
	check(Audio.play_sound(9), "a big strike plays")
	check(not Audio.play_sound(3), "held back for half a second")
	eq(Audio.played.back(), 9, "the last one played")
	Audio._last = -1
