extends CanvasLayer
## Игровой UI поверх мира. Соответствует c.java b() — нижняя панель (cx[0], cx[2]),
## полоски HP/MP (c.a() — ball_black, 35*cz.p/cz.y).

const VIEW_W := GameState.VIEW_W
const VIEW_H := GameState.VIEW_H
const BOTTOM_BAR_H := 61
const TOP_BAR_H := 25

@onready var _bottom_bar: TextureRect = $BottomBar
@onready var _hp_bar: ProgressBar = $HpMpContainer/HPBar
@onready var _mp_bar: ProgressBar = $HpMpContainer/MPBar

func _ready() -> void:
	# Демо-значения; позже брать из GameState / персонажа (cz.p, cz.y, cz.r, cz.z)
	_hp_bar.max_value = 100.0
	_hp_bar.value = 100.0
	_mp_bar.max_value = 50.0
	_mp_bar.value = 50.0

func set_hp_mp(hp_current: float, hp_max: float, mp_current: float, mp_max: float) -> void:
	_hp_bar.max_value = maxf(1.0, hp_max)
	_hp_bar.value = clampf(hp_current, 0.0, hp_max)
	_mp_bar.max_value = maxf(1.0, mp_max)
	_mp_bar.value = clampf(mp_current, 0.0, mp_max)
