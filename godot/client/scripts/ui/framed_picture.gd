class_name FramedPicture
extends TextureRect
## A picture in the gold frame of the new art (Pictures.frame()), smooth when shown smaller:
## a portrait or a story picture. Its custom_minimum_size is its size; set its texture with
## Pictures.portrait() or Pictures.story().


func _init() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED


func _ready() -> void:
	if material == null and custom_minimum_size.y > 0.0:
		material = Pictures.frame(custom_minimum_size.x / custom_minimum_size.y)
