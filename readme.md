# Mercenary's Path

Гра на Godot 4.5 (GDScript): козацький найманець іде походами через 45 місць, б'ється в
3D-кімнатах, збирає речі, навички й дари генералів. Гра офлайн: герой і налаштування
зберігаються на комп'ютері. Гра й тести — один проєкт Godot у `godot/client`.

Натхнення — мобільна action-RPG «Path of a Warrior» (2008): звідти жанр і механіки, а код,
назви, тексти, графіка й музика — наші (що ще тимчасове — у [`docs/GODOT_PLAN.md`](docs/GODOT_PLAN.md)).

## Швидкий старт

Потрібен Godot 4.5.1.

```
godot --headless --path godot/client --import                 # один раз після клонування
godot --path godot/client                                     # гра
godot --headless --path godot/client res://tests/runner.tscn  # тести
```

Докладніше про запуск і будову проєкту — у [`godot/README.md`](godot/README.md),
як працювати з кодом і робити PR — у [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Що де лежить

| Шлях | Що там |
| --- | --- |
| `godot/client` | Проєкт Godot: гра, тести (`tests/`), дані (`data/`), тексти обома мовами (`i18n/`) |
| `godot/tools/art` | Графіка гри кодом (Blender): люди, зброя, реквізит, портрети |
| `godot/tools/music` | Музика гри кодом |
| `godot/FRIENDS.md` | Як запустити збірку (він же `ІНСТРУКЦІЯ.txt` в архіві) |
| `docs/GODOT_PLAN.md` | План гри |
| `CLAUDE.md` | Правила для Claude і людей: структура Godot, якість коду, тести |
