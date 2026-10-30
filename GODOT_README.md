# Path of a Warrior — порт на Godot 4.5

Игра перенесена с J2ME (Java ME) на **Godot 4.5**. Сохранено разрешение 240×320 и тайлы 27×27 пикселей.

## Как запустить

1. Установите [Godot 4.5](https://godotengine.org/download).
2. Откройте проект: в Godot **Project → Import** выберите папку с `project.godot`, либо **Project → Open** и укажите файл `project.godot`.
3. Запуск: **F5** или кнопка **Play**.

## Управление: гейм-менеджер подбирает источник ввода по устройству

**GameState** (autoload) определяет режим ввода и переключает его по событиям:
- **TOUCH** — мобилка: показывается виртуальный джойстик (←↑↓→), меню — тап по кнопкам.
- **GAMEPAD** — джойстик/геймпад: движение и меню по осям/кнопкам.
- **KEYBOARD** — клавиатура: WASD/стрелки, Enter/Space.

При старте: если устройство мобильное → TOUCH, иначе если подключён геймпад → GAMEPAD, иначе → KEYBOARD. При любом вводе (тач, кнопка геймпада, клавиша) режим обновляется, виртуальный джойстик показывается/скрывается по сигналу `input_mode_changed`.

Действия: `move_left`, `move_right`, `move_up`, `move_down` (игра), `menu_prev`, `menu_next`, `menu_confirm` (меню). Привязки — **Project → Project Settings → Input Map**.

## Структура проекта

- `project.godot` — настройки, окно 240×320, autoload GameState.
- `scenes/main.tscn` — корень: SubViewport 240×320. Цепочка: титул → игровое меню → мир.
- `scenes/title_screen.tscn` — титул: title_1..4, меню «Играть / Продолжить / Выход».
- `scenes/game_menu.tscn` — игровое меню (bV == 2): Квест, Магазин, Кузнец, Склад, Обмен, «В игру». Стрелки ← → и клик по пункту.
- `scenes/game.tscn` — мир: карта + персонаж + игровой UI (CanvasLayer).
- `scenes/game_ui.tscn` — нижняя панель (cx[0], cx[2]) и полоски HP/MP (c.java b(), c.a()).
- `scenes/player.tscn` — персонаж (CharacterBody2D).
- `scenes/virtual_pad.tscn` — виртуальный джойстик (←↑↓→) для мобилки; показывается только при `GameState.is_mobile()`.
- `scripts/main.gd` — переключение титул → игра; `game.gd`, `player.gd`, `game_ui.gd`, `title_screen.gd`, `game_menu.gd`, `virtual_pad.gd` — логика.

Тайлы подгружаются из PNG в корне: `1_01.png` … `1_16.png` для уровня 1 (формат `N_XX.png` — уровень N, тайл XX). Демо-карта строится в коде (сетка с бордюром).

**Стрілки (як у Java):** В оригіналі одна картинка `ui_arrow2.png` містить дві стрілки; в Java (m.java) їх «вирізають» через `drawImage` з різними (srcX, srcY) і clip. У Godot аналог — **AtlasTexture**: один атлас, регіони Rect2. Ресурси `textures/arrow_left.tres` і `textures/arrow_right.tres` беруть з `ui_arrow2.png` області (0,0,30,21) та (30,18,28,19). Меню та віртуальний джойстик використовують ці .tres замість окремих PNG.

## Что можно добавить дальше

- Парсинг бинарных уровней `.MAP` / `.arr` из оригинала и загрузка реальных карт.
- Меню, диалоги, бой и инвентарь по логике из `e.java`, `ar.java`, `ag.java`.
- Звуки: в папке есть `snd1.mid`, `snd3.wav` и др. — подключить через AudioStreamPlayer.
- Сохранение/загрузка (в J2ME было через RecordStore → в Godot через FileAccess или user://).

Оригинальный код: Java (J2ME), главный цикл в `ag.java`, экран в `e.java`, ресурсы через `.scr` и PNG.

---

## Соответствие Java → Godot (классы и движок)

| Java (J2ME) | Godot |
|-------------|--------|
| **ag.java** — Canvas, глобалы (bJ, bK, bV, cM, cq, cd, ce, ca) | **GameState** (autoload) — константы VIEW_W/H, TILE_SIZE, screen_type, menu_index, camera |
| **c.java** — отрисовка карты `l()`, тайлы bT, сетка eE, камера ca | **map_renderer.gd** — сетка 27×27, тайлы уровня, `set_camera_offset()` |
| **n.java (cz)** — персонаж: позиция a[0].a/b, анимация e[0], d[0] | **player.gd** — CharacterBody2D, движение, flip по направлению |
| **e.java** — экраны/меню по cM[0], вызов bf(), меню | Пока только игровой экран; меню/диалоги — добавить сцены по e.java |
| **x.java** — Graphics: drawImage, clipRect, fillRect | CanvasItem / Sprite2D, при необходимости — хелпер в GDScript |
| **g.java** — шрифт 0_font.png 8×17 | Позже: BitMapFont или Label с атласом |
| **k.java** — звук snd*.mid/wav | AudioStreamPlayer + загрузка по имени |
| **ar.java** — загрузка/логика уровней, меню | game.gd + MapRenderer; меню — отдельные сцены |
| **Main.java** — MIDlet, Display | main.tscn + SubViewport 240×320 |

Карта: в оригинале данные из v(56), cE (o.java), cJ — индексы тайлов. Сейчас демо-сетка в коде; реальные уровни — парсинг .MAP/.arr или конвертация в ресурсы Godot.
