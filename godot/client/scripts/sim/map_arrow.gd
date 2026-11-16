class_name MapArrow
extends RefCounted
## An archer's arrow in flight (three at most on the map).

var active := false
var pos := Vector2i.ZERO
var dir := 0  # 0 down, 1 left, 2 up, 3 right
var ticks := 0
var attack := 0
var w := 2
var h := 11
