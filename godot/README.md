# Mercenary's Path — Godot 4

План: [`docs/GODOT_PLAN.md`](../docs/GODOT_PLAN.md).

**Крок 1 (зараз): переносимо гру як є.** Карти, місії, правила й оригінальна графіка
беремо з оригіналу (поведінка описана в `pyport/`), нічого нового не вигадуємо.
Вигляд: 3D-світ і 2D-спрайти (рішення 06.11.2026). Своя графіка, назви й процедурні
карти — крок 2, після перенесення.

```
godot/
  client/                 проєкт Godot 4.5 (GDScript)
    project.godot
    scenes/main.tscn      корінь: тема + роутер екранів
    scripts/core/         автозавантаження: I18n, Settings, InputSetup, Router
    scripts/screens/      екрани: title, main_menu, settings, map_viewer
    scripts/world/        3D-світ: map_builder (карта з оригінальних шарів), hero, follow_camera
    scripts/ui/           тема, сенсорні кнопки
    i18n/strings.json     тексти українською й англійською
    data/maps/N.json      45 оригінальних карт (робить tools/import_original.py)
    assets/original/      тайли й кадри героя з оригіналу (теж import_original.py)
    tests/                тести: test_*.gd, запуск runner.tscn
  tools/import_original.py  конвертер оригінальних ресурсів з кореня репо
```

## Запуск

```
python godot/tools/import_original.py                       # після змін у конвертері
godot --path godot/client                                   # гра
godot --headless --path godot/client --import               # один раз після клонування
godot --headless --path godot/client res://tests/runner.tscn  # тести
```

Тести також ганяє GitHub Actions (`.github/workflows/godot.yml`) на кожен PR, що змінює `godot/`.

## Як карта стає 3D

- 1 тайл (27 px) = 1 одиниця світу; тайл (x, y) лежить на X = x..x+1, Z = y..y+1.
- Шар `ground` — підлога, шар `upper` — наклейки на підлозі (дороги, трава).
- Клітинки з прапорцем «заблоковано» або «малюється над героєм» з тайлом у `upper` —
  це фасади будинків, дерева, стіни, намальовані в оригіналі «спереду». Кожен стовпчик таких
  клітинок ставиться вертикально на передній (нижній на екрані) клітинці і росте вгору.
- Шар `objects` — предмети, які можна розбити (бочки, ящики): спрайти, що дивляться на камеру.
- Зіткнення як в оригіналі: заблокована клітинка або предмет — суцільний блок.

## Керування

| Дія | Клавіатура | Геймпад |
|---|---|---|
| рух | WASD / стрілки | лівий стік / хрестовина |
| атака | J / пробіл | A |
| скіли 1–4 | 1–4 / U I O P | X, Y, LB, RB |
| пауза / назад | Esc | Start |

На телефоні — стік зліва і кнопки справа (`scripts/ui/touch_controls.gd`).
У переглядачі карт 3 / 4 (LB / RB) — попередня / наступна карта.
