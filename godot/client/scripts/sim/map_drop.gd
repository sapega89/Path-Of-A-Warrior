class_name MapDrop
extends RefCounted
## Something lying on the floor: an item id (< 100 potion, < 10000 gear, 10000 + n = n gold).

var item := 0
var pos := Vector2i.ZERO
var ticks := 75
