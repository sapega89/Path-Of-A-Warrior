extends AcceptDialog
## [modal] Базове модальне вікно: повідомлення-заборона/попередження, кнопка Ok. Не діалог і не алерт.

signal closed

func _ready() -> void:
	confirmed.connect(_on_confirmed)
	canceled.connect(_on_confirmed)

func set_message(text: String) -> void:
	dialog_text = text

func _on_confirmed() -> void:
	closed.emit()
	hide()
