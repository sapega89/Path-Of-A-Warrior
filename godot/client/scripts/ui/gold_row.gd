class_name GoldRow
extends HBoxContainer
## A purse: the gold coin of the new art and the gold after it (its child "Value"), centred
## (scenes/ui/gold_row.tscn). The coin is drawn from its SVG when the row is made.


func _ready() -> void:
	(%Coin as TextureRect).texture = UiTheme.coin()
