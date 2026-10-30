extends ConfirmationDialog
## [alert] Базова сцена алерту: підтвердження Yes/No або повідомлення з Ok. Не діалог з персонажем.

signal confirmed_yes
signal confirmed_no

func _ready() -> void:
	confirmed.connect(_on_confirmed)
	canceled.connect(_on_canceled)

func set_message(text: String) -> void:
	dialog_text = text

func _on_confirmed() -> void:
	confirmed_yes.emit()

func _on_canceled() -> void:
	confirmed_no.emit()
