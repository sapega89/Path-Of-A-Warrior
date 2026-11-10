class_name OnlineFighter
extends RefCounted
## A fighter of an online battle (scripts/net/online_battle.gd): who he is, where he stands on
## the battle's 240 x 320 screen, his animation and his HP and MP running to what the server
## says.

var present := false
var slot := 0
var name := ""
var alt_name := ""
var level := 1
var wins := 0
var losses := 0
var hp := 0
var max_hp := 1
var mp := 0
var weapon := 0
var face := 0
var kind := OnlineBattle.PLAYER
var quote_start := ""
var quote_win := ""
var x := 0
var y := 0
var frame := 0
var anim := 0
var anim_tick := 0
var anim_len := 0
var hp_target := 0
var mp_target := 0
var hp_step := 0
var mp_step := 0
var hp_delta := 0
var blink := 0
var status := 99  # 11..13: a soul's aura (its action), 99 none
var status_ticks := 0
## How high over the ground the fighter is now, in pixels: the part of an animation's
## up-and-down that is a leap, not a step along the ground (the 2.5D screen shows it as
## height; y stays as on the original screen).
var lift := 0
var leap_from := 0


func team() -> int:
	return slot % 2


func row() -> int:
	return slot / 2


func mirrored() -> bool:
	return slot % 2 != 0
