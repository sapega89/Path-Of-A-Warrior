# Правила проекту (з CLAUDE.md)

## Tech Stack
- **Engine:** Godot 4.5
- **Language:** GDScript
- **Resolution:** 240×320 (QVGA)
- **Tile size:** 27×27 px

## Обов'язкові правила

### 1. Тільки Godot 4.5
```gdscript
# ✅ Правильно (4.5):
@onready var node = $Node
signal my_signal(value: int)
super._ready()
%UniqueNode

# ❌ Неправильно (3.x):
onready var node = $Node
setget set_value
.parent_method()
```

### 2. Scenes First
- Спочатку будуй `.tscn` сцену
- Скрипт додавай ТІЛЬКИ якщо без нього неможливо
- Якщо сцена працює без скрипту — так і залишається

### 3. Visual First
- Спочатку статична сцена (layout, кольори, текстури)
- Потім логіка і анімація

### 4. Не чіпай існуючий код
- Без явної вказівки в таску — не змінюй інші файли
- Баг фікс не потребує рефакторингу сусіднього коду

### 5. Аналіз перед реалізацією
- Завжди читай Java оригінал перед тим як писати код
- `JAVA_REFERENCE.md` — довідник по класах
- `docs/*_SPEC.md` — специфікації від PM

### 6. Таски перед реалізацією
- Декомпозиція через TaskCreate
- Один таск = одна атомарна зміна
- Позначати in_progress → completed
