class_name MapBreakable
extends RefCounted
## A breakable object of the room (barrels, crates, ...): a cell of the objects layer.

var active := true
var tile := Vector2i.ZERO
var pos := Vector2i.ZERO
var kind := 0
var hp := 21
var break_frame := 0  # > 0: the hit spark shows
var break_ticks := 0  # > 0: broken, blinking out
