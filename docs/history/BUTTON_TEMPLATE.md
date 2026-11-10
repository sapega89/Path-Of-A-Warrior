# Шаблон стандартної кнопки (інвентар, підменю, списки)

Один стиль кнопок для підменю (Blacksmith, Management), інвентаря, списків предметів тощо.

**Ресурси (.tscn і .tres):**
- **theme_list_button.tres** — тема для кнопки пункту списку (чорний фон, сіра рамка, білий текст).
- **theme_back_button.tres** — тема для кнопки BACK (темно-сірий фон, рамка, радіус 2 px).
- **scenes/button_list_item.tscn** — сцена однієї кнопки списку (instance = готова кнопка з темою).
- **scenes/button_back.tscn** — сцена кнопки BACK.

Реалізація в коді (selected/hover): `scripts/submenu_shell.gd`.

---

## 1. Кнопка пункту списку (Buy Item, Sell Item, Trade…)

**Вигляд:**
- **Не обрана:** чорний фон, сіра рамка 1 px, білий текст. При наведенні — темніший фон (0.1,0.1,0.1).
- **Обрана (hover/selected):** чорний фон, **біла рамка 2 px**, **червоний текст** (0.9, 0.15, 0.15). При наведенні — світліший червоний (1, 0.25, 0.25).

**Код створення та стилю** (з `submenu_shell.gd`):

```gdscript
func _create_link_button(label_text: String, action_id: int, index: int) -> Button:
	var btn := Button.new()
	btn.text = label_text
	btn.flat = true
	btn.custom_minimum_size = Vector2(200, 28)
	btn.add_theme_font_size_override("font_size", 16)
	btn.pressed.connect(_on_link_pressed.bind(action_id))
	btn.mouse_entered.connect(_on_link_hovered.bind(index))
	_apply_link_button_style(btn, index == _selected_link_index)
	return btn

func _apply_link_button_style(btn: Button, selected: bool) -> void:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0, 0, 0, 1)
	style.set_corner_radius_all(0)
	if selected:
		style.border_color = Color(1, 1, 1, 1)
		style.set_border_width_all(2)
		btn.add_theme_color_override("font_color", Color(0.9, 0.15, 0.15))
		btn.add_theme_color_override("font_hover_color", Color(1, 0.25, 0.25))
	else:
		style.border_color = Color(0.45, 0.45, 0.45, 1)
		style.set_border_width_all(1)
		btn.add_theme_color_override("font_color", Color(1, 1, 1, 1))
		btn.add_theme_color_override("font_hover_color", Color(0.9, 0.9, 0.9, 1))
	btn.add_theme_stylebox_override("normal", style)
	var style_hover := style.duplicate()
	style_hover.bg_color = Color(0.1, 0.1, 0.1, 1)
	btn.add_theme_stylebox_override("hover", style_hover)
	btn.add_theme_stylebox_override("pressed", style_hover)
```

**Параметри:**

| Стан      | Рамка       | Текст (font_color) |
|-----------|-------------|--------------------|
| не обрана | 1 px, сіра  | білий              |
| обрана    | 2 px, біла  | червоний           |

---

## 2. Кнопка BACK (внизу справа)

**Вигляд:** темно-сірий фон (0.25, 0.23, 0.21), рамка 1 px (0.45, 0.42, 0.38), радіус 2 px. При hover/pressed — ще темніший фон (0.2, 0.18, 0.16).

**Код** (з `submenu_shell.gd`):

```gdscript
func _style_back_button() -> void:
	if _back_btn == null:
		return
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.25, 0.23, 0.21, 1)
	style.border_color = Color(0.45, 0.42, 0.38, 1)
	style.set_border_width_all(1)
	style.set_corner_radius_all(2)
	_back_btn.add_theme_stylebox_override("normal", style)
	var style_press := style.duplicate()
	style_press.bg_color = Color(0.2, 0.18, 0.16, 1)
	_back_btn.add_theme_stylebox_override("hover", style_press)
	_back_btn.add_theme_stylebox_override("pressed", style_press)
	_back_btn.flat = false
```

---

## 3. Як використовувати в інвентарі / новому екрані

1. **Список пунктів:** створюй `Button.new()`, задай `text`, `custom_minimum_size` (наприклад 200×28), викликай функцію типу `_apply_link_button_style(btn, selected)` з вищезаданими кольорами та рамками.
2. **Вибір пункту:** зберігай `_selected_link_index`, на `mouse_entered` оновлюй індекс і викликай `_refresh_link_styles()` (перезастосуй стиль до всіх кнопок).
3. **BACK:** якщо є готова кнопка в сцені — у `_ready()` викликай `_style_back_button()` або скопіюй блок з `_style_back_button()` для своєї кнопки.

Файл-референс: `scripts/submenu_shell.gd` (функції `_create_link_button`, `_apply_link_button_style`, `_style_back_button`).
