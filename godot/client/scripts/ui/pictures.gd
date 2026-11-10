class_name Pictures
extends RefCounted
## The pictures of the new art in the screens: the portraits (busts of the game's people painted
## in the shader of the maps, assets/art/portraits/<number>.png, made by tools/portraits.tscn)
## and the story pictures (assets/art/story/e<n>.png, made by tools/story_pictures.tscn), shown
## in a gold frame (assets/art/shaders/portrait_frame.gdshader).

const PORTRAIT := "res://assets/art/portraits/%d.png"
const STORY := "res://assets/art/story/e%d.png"
## A story picture's width over its height.
const STORY_ASPECT := 1.3
const FRAME := preload("res://assets/art/shaders/portrait_frame.gdshader")

static var _textures := {}
static var _frames := {}


## The portrait of a number (a number without a portrait gets the one of anybody, 0).
static func portrait(id: int) -> Texture2D:
	return texture(PORTRAIT % (id if ResourceLoader.exists(PORTRAIT % id) else 0))


## Story picture n (1..15).
static func story(n: int) -> Texture2D:
	return texture(STORY % n)


## A picture with mipmaps, so that it stays smooth when shown smaller (made once; it takes the
## place of the imported one at its path).
static func texture(path: String) -> Texture2D:
	if not _textures.has(path):
		var img := (load(path) as Texture2D).get_image()
		img.generate_mipmaps()
		var tex := ImageTexture.create_from_image(img)
		tex.take_over_path(path)
		_textures[path] = tex
	return _textures[path]


## A framed picture of the given size; set its texture with portrait() or story().
static func framed(node_name: String, size: Vector2) -> TextureRect:
	var t := FramedPicture.new()
	t.name = node_name
	t.custom_minimum_size = size
	t.material = frame(size.x / size.y)
	return t


## The frame's material for pictures of a shape (width over height).
static func frame(aspect: float) -> ShaderMaterial:
	var key := snappedf(aspect, 0.01)
	if not _frames.has(key):
		var m := ShaderMaterial.new()
		m.shader = FRAME
		m.set_shader_parameter("aspect", key)
		if key > 1.0:
			# a wide picture: a thinner rim and smaller corners for its size
			m.set_shader_parameter("radius", 0.012)
			m.set_shader_parameter("width", 0.02)
		_frames[key] = m
	return _frames[key]
