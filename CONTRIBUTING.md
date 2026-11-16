# Як працювати з кодом

Повні правила — у [`CLAUDE.md`](CLAUDE.md). Тут коротко, що треба знати в перший день.

## Налаштування

1. Godot 4.5.1 (той самий, що в CI: `.github/workflows/godot.yml`).
2. `godot --headless --path godot/client --import` після клонування.
3. Дані гри (`godot/client/data/*.json`) і тексти (`godot/client/i18n/*.json`) правляться руками:
   змінили англійський текст у `data`, змініть його й у `i18n`. Графіку й музику роблять скрипти
   `godot/tools/art` і `godot/tools/music` (що їм треба — у їхніх README).

## Будова клієнта

- `scripts/core/` — автозавантаження (I18n, Settings, InputSetup, Router, Audio) і дані героя
- `scripts/screens/` — екрани; `Router` (`scripts/core/router.gd`) показує один екран і веде стек «назад»
- `scripts/sim/` — логіка гри без вузлів (`map_sim.gd` — карта тік за тіком); сцени лише малюють її стан
- `scripts/world/` — 3D-світ: карта, люди, ефекти, камера
- `scripts/ui/` — спільні елементи інтерфейсу, тема
- `tests/test_*.gd` — тести, `tests/runner.tscn` запускає всі

Код поступово переходить на звичну для Godot структуру (сцени `.tscn` для екранів, `BaseScreen`,
`GameState`, `theme.tres`, `class_name`). Новий код одразу пишеться за новими правилами з `CLAUDE.md`.

## Перед PR

```
godot --headless --path godot/client res://tests/runner.tscn
python godot/tools/check_standards.py
```

- Тести зелені, у лозі немає нових рядків `ERROR`.
- Додали скрипт, шейдер чи ассет: запустіть імпорт і закомітьте нові файли `.uid` і `.import`
  (Godot тримає в них id, на які посилаються сцени, і налаштування імпорту).
- `check_standards.py` зелений: новий код не додає порушень правил `CLAUDE.md`. Старі порушення
  записані в `godot/tools/standards_baseline.json`; прибрали якесь, тоді
  `python godot/tools/check_standards.py --update` у тому ж PR.
- Зміна поведінки має тест; зміна, яку просив гравець, описана в `godot/README.md`.
- Скриншоти CI (`tools/shots.tscn`) не змінюються, якщо зміна не про вигляд.
- Один PR — одна річ: не змішуйте рефакторинг із новою фічею.
- PR іде в гілку `dev`.
