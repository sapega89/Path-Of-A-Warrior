class_name MapActor
extends RefCounted
## The hero or an enemy on the map: where he is, what he does, his stats and his hit sparks.

## weapon_kind of a long weapon, a pike (its reach 63 px; a short one, 1, reaches 53).
const LONG_WEAPON := 0

var pos := Vector2i.ZERO
var dir := 0  # 8-direction: 0 down, 2 left, 4 up, 6 right
var facing := 0
var action := 0  # 0 stand, 1 walk, 2 run, ...
var frame := 0
var slide := Vector2i.ZERO  # the corner-slide step (slide_target)
var shown_dir := 0  # the direction of the last drawn tick
var idle_ticks := 20
var prev_pos := Vector2i.ZERO  # the position at the start of the tick (for drawing)
var last_action := 0  # the action and frame at the end of the last tick
var last_frame := 0
var type := 0  # enemies: 201 swords, 202 archers, 203 a squad of swords
var level := 1
var attack := 0
var defense := 0
var attack_buff := 0
var defense_buff := 0
var hp := 0
var max_hp := 0
var alerted := 0  # 0 while walking in through the exit
var think_ticks := 0
var ai_mode := 0  # > 0: knocked back that many ticks
var hurt_ticks := 0
var combo := 0
var weapon_kind := 0  # the weapon's slot type: 0 a long one (reach 63), 1 a short one (53)
var skill_step := 0  # a general's heals so far
var mp := 0
var max_mp := 0
var attack_buff_ticks := 0
var defense_buff_ticks := 0
var hit_fx_kind := 0  # > 0: a hit spark shows (1 or 2: which pair of spark pictures)
var hit_fx_frame := 0
var hit_fx_pos := Vector2i.ZERO  # where it was hit
var on_fire := false  # burning: the fire shows on him six ticks
var fire_frame := 0  # the picture of the fire shown now (-1: from the end of this tick)
