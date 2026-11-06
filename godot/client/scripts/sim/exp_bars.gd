extends RefCounted
## The exp bar of the pages Total Exp and Time Exp after a won mission, as in pyport
## (map_scene.make_exp_bars, menus.draw_exp_bar): 100 px for the hero's level, what he had,
## then what the mission gives, then (Time Exp) what the time gives; the new part grows 4 px
## a tick. At the end of the bar the hero goes up a level: "Level Up : Lv N" shows for 20
## ticks and the bar starts again from empty with the rest. Drawn by scripts/ui/exp_bar.gd.

const Profile := preload("res://scripts/core/profile.gd")
const W := 100  # the bar's length in original pixels
const GROW := 4  # px a tick
const LEVEL_UP_TICKS := 20
const LEVELS := 10  # the levels ahead the bar can count

## Where the parts end, in hundredths of a level: what he had, with the mission, with the
## time; a level gone up takes 100 off.
var bars := [0, 0, 0]
var part := 0  # 0: Total Exp (the mission's part grows), 1: Time Exp (the time's part grows)
var step := 0  # the ticks the growing part has grown
var level := 1  # the level shown
var level_up_ticks := 0  # "Level Up" shows while above 0
var _level0 := 1
var _exp0 := 0
var _ups := 0


## Total Exp: the hero's level and exp before the mission, and what the mission gives.
func begin(hero_level: int, hero_exp: int, reward: int) -> void:
	_level0 = hero_level
	_exp0 = hero_exp
	_ups = 0
	level = hero_level
	level_up_ticks = 0
	var need := Profile.exp_needed(hero_level)
	bars[0] = hero_exp * 100 / need if need > 0 else 0
	bars[1] = bar_of(hero_exp + reward)
	bars[2] = bars[1]
	part = 0
	step = 0


## Time Exp: what the mission gives with the exp for the time.
func begin_time(reward: int) -> void:
	bars[2] = bar_of(_exp0 + reward) - 100 * _ups
	part = 1
	step = 0


## Where the exp ends, in hundredths of the levels from the one before the mission (at
## least a little into the level reached).
func bar_of(total_exp: int) -> int:
	var sum := 0
	for lv in LEVELS:
		var need := Profile.exp_needed(_level0 + lv)
		if need <= 0:
			return lv * 100
		sum += need
		if total_exp < sum:
			var rest := need - sum + total_exp
			return maxi(rest * 100 / need + lv * 100, lv * 100 + 1)
	return LEVELS * 100


## The growing part's width now, and 0 (still growing), 1 (the bar is full: a level up) or
## 2 (all of it shown).
func grown() -> Array:
	var from: int = bars[part]
	var width := step * GROW
	var result := 0
	if from + width > int(bars[part + 1]):
		width = int(bars[part + 1]) - from
		result = 2
	if from + width > W:
		width = W - from
		result = 1
	return [width, result]


## All of the growing part is shown.
func done() -> bool:
	return level_up_ticks == 0 and grown()[1] == 2


func tick() -> void:
	var result: int = grown()[1]
	if level_up_ticks > 0:
		level_up_ticks -= 1
	elif result == 0:
		step += 1
	elif result == 1:
		bars[0] = 0
		bars[1] = maxi(int(bars[1]) - 100, 0)
		bars[2] = int(bars[2]) - 100
		step = 0
		level += 1
		_ups += 1
		level_up_ticks = LEVEL_UP_TICKS
