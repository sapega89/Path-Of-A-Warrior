extends "res://tests/test_case.gd"


func test_the_sounds_are_there() -> void:
	for n in 3:
		check(ResourceLoader.exists(Audio.MUSIC_PATH % n), "tune %d" % n)
	for n in range(3, 17):
		check(ResourceLoader.exists(Audio.SFX_PATH % n), "effect %d" % n)


func test_each_screen_has_its_tune() -> void:
	Audio.play_music(-1)
	Audio._on_screen_changed("title")
	eq(Audio.music, 0, "the title")
	Audio._on_screen_changed("campaign")
	eq(Audio.music, 2, "the menus")
	Audio._on_screen_changed("mission")
	eq(Audio.music, 1, "a mission")
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
