# Path of a Warrior

Гра на Godot 4.5 (GDScript): кампанія з 45 місцями, бої на 3D-картах, мультиплеєр і Live через
власний сервер. Клієнт, сервер і тести — один проєкт Godot у `godot/client`.

## Швидкий старт

Потрібні Godot 4.5.1 і Python 3 з Pillow (для конвертера даних).

```
godot --headless --path godot/client --import                 # один раз після клонування
godot --path godot/client                                     # гра (локальний сервер запускається сам)
godot --headless --path godot/client res://tests/runner.tscn  # тести
```

Докладніше про запуск, сервер і будову проєкту — у [`godot/README.md`](godot/README.md),
як працювати з кодом і робити PR — у [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Що де лежить

| Шлях | Що там |
| --- | --- |
| `godot/client` | Проєкт Godot: гра, сервер (`server/`), тести (`tests/`), дані (`data/`) |
| `godot/tools/import_original.py` | Конвертер: робить `godot/client/data` і `assets/original` з `original/` |
| `original/` | Файли оригінальної гри (графіка, карти, тексти, звуки); тільки для конвертера |
| `pyport/` | Python-версія: довідка про те, як поводиться оригінал. Нових фіч там немає |
| `docs/GODOT_PLAN.md` | План Godot-версії |
| `docs/analysis/` | Розбір оригінальної гри |
| `docs/history/` | Старі плани й документи (Python-порт, перша спроба на Godot); не актуальні |
| `CLAUDE.md` | Правила для Claude і людей: структура Godot, якість коду, тести |
