class_name ExitArrows
extends Control
## The exit arrows at the screen's edges: Arrow0..3 for the room's exits (down, left, up,
## right), Arrow4..7 for a second way on a side. They blink while the exits are open, and after
## a mission won they show the ways on; the one down sits above the HUD (at the very bottom the
## HUD hid it).

## The exit arrow of the new art, pointing down: two brass chevrons in ink, the near one fainter.
# gdlint:ignore = max-line-length
const EXIT_ARROW := '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 40"><g fill="#b89550" stroke="#0f0d0c" stroke-width="2.5" stroke-linejoin="round"><path d="M4 3 L24 17 L44 3 L44 11 L24 25 L4 11 Z" fill-opacity="0.55"/><path d="M4 15 L24 29 L44 15 L44 23 L24 37 L4 23 Z"/></g><path d="M24 30.5 l3 2.5 l-3 2.5 l-3 -2.5 z" fill="#7e241f"/></svg>'

var arrows: Array[TextureRect] = []


func _ready() -> void:
	for i in 8:
		var a: TextureRect = get_node("Arrow%d" % i)
		a.texture = exit_arrow(i % 4)
		arrows.append(a)


## The exit arrow to side i (0 down, 1 left, 2 up, 3 right), 72 px across.
static func exit_arrow(i: int) -> Texture2D:
	var img := Image.new()
	img.load_svg_from_string(EXIT_ARROW, 1.5)
	match i:
		1:
			img.rotate_90(CLOCKWISE)
		2:
			img.rotate_180()
		3:
			img.rotate_90(COUNTERCLOCKWISE)
	return ImageTexture.create_from_image(img)


## The arrows of the room sim is in, lit on the ticks `blink` says; while the hero chooses the
## way on, one per way of `ways_out` (MissionScreen.ways_on).
func show_exits(sim: MapSim, ways_out: Array, blink: bool) -> void:
	var view := get_viewport_rect().size
	var lit: bool = sim.exits_open() and blink
	for i in 8:
		var a := arrows[i]
		var along := 0.5  # where on its side: the middle, or a half's middle
		if sim.choosing:
			a.visible = false
			for w in ways_out:
				if (
					int(w.exit) - 1 == i % 4
					and (int(w.half) == -1 and i < 4 or int(w.half) == i / 4)
				):
					a.visible = blink
					along = 0.5 if int(w.half) == -1 else 0.25 + 0.5 * int(w.half)
		else:
			a.visible = i < 4 and lit and sim.rooms.has_exit(sim.cell, i + 1)
		var s := a.texture.get_size()
		a.size = s
		match i % 4:
			0:
				a.position = Vector2(view.x * along - s.x / 2.0, MapHud.top_of(view) - s.y - 8)  # above the HUD
			1:
				a.position = Vector2(16, view.y * along - s.y / 2.0)
			2:
				a.position = Vector2(view.x * along - s.x / 2.0, 16)
			3:
				a.position = Vector2(view.x - s.x - 16, view.y * along - s.y / 2.0)
