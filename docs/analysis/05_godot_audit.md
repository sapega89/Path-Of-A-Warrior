# 05 — Технічний аудит Godot-порту «Path of a Warrior»

> **Примітка (30.10.2026).** Аудит робився на неповній копії проєкту.
> - Не копіювались: PNG, `.import`, `addons/`, `views/`, `*.tmp`, `.tres`, MIDI і частина агентів (`ba.md`, `qa.md`, `reviewer.md`).
> - Твердження про їхню відсутність (§0, §1.3) стосуються копії, а не вашої папки.
> - Висновки щодо коду й сцен чинні.
> - Godot-версію заморожено, тому список техборгу в кінці — для історії.

Предмет аудиту: поточний порт на Godot 4.5 у `/home/claude/pow`. Java-код я використовував лише як еталон. Вихідний проєкт не змінювався: усі перевірки йшли на копіях `/home/claude/pow_check*`.

## 0. Коротко

- **Скрипти компілюються.** Є Godot 4.5 headless (`/home/claude/godot/Godot_v4.5-stable_linux.x86_64`). З заглушками на місці відсутніх ассетів усі 36 `.gd` компілюються, і всі 42 `.tscn` інстанціюються без помилок «Node not found». Виняток — дві биті сцени з `scenes/buttons/`. Попереджень GDScript із дефолтним рівнем лише 7.
- **Головна проблема — маршрутизація вводу (P0, підтверджено автотестом).** Коли в ігровому меню відкрите будь-яке підменю (Mission, Visiting, Blacksmith…), клавіатуру отримує прихована карусель головного меню:
  - DOWN прокручує карусель;
  - ENTER відкриває інший пункт: зі списку місій відкрився Blacksmith, у Visiting замість діалогу з генералом підменю перевідкрилось;
  - ESC викидає на титул.
  Поведінка ще й залежить від того, чи клікали мишею у вікно (фокус `SubViewportContainer`). З клавіатури підменю фактично непрохідні.
- **Дані — суцільні плейсхолдери, хоча оригінал уже розбирається.** Назви місій, лордів і генералів, кількість місій, спавн, бріфінги, пункти меню, Help, Endings, Options вигадані. Водночас оригінальні файли розбираються тривіально: я розібрав `mission.arr`, `sideinfo.arr`, `ruler.arr`, `brief.scr` і `general.arr` приблизно в 40 рядках Python. Семантика флоу місій переплутана: «лорди» і «місії» помінялись місцями, кількості теж (1 і 4 замість 4 і 1).
- **Ігрова сцена — прототип із багами:**
  - карта скролиться вдвічі швидше за гравця (Camera2D плюс ручний зсув карти);
  - немає колізій і немає виходу з гри в меню;
  - HUD наполовину за екраном;
  - віртуальний джойстик не з'являється ніколи;
  - збереження пишуть лише 3 поля.
- **Документація розходиться з кодом.** Кілька рішень у vault (Tasks #6/#7: «Blacksmith = 3 пункти», «Assign Items не з Java») суперечать даним оригіналу. Імовірна причина: `decode_scr.py` обрізає `uimenu.scr` до 28 з 60 рядків, тож агенти працювали з неповним дампом.

**Відмінності копії від опису задачі.** У копії немає `addons/midi`, `views/`, кореневих `main.gd`/`main.tscn`, `*.tmp`, `godot_midi.gd`, `midi_*.gd`, `openxr_action_map.tres`, PNG, `.import` і `.uid`. Немає також ресурсів `.tres` (`theme_*.tres`, `textures/*.tres`), `.mid` і `.sf2`. Скриптів 36, а не близько 43. У `.claude/agents/` лише 3 агенти: pm, tech-lead, developer. BA, Reviewer і QA, описані у vault, відсутні.

---

## 1. Інвентаризація

Позначення статусів:
- **OK** — працює;
- **PART** — частково (працює, але з плейсхолдерами або багами);
- **STUB** — заглушка;
- **DEAD** — ніде не використовується;
- **BROKEN** — зламано.

### 1.1 Сцени (42)

| Сцена | Призначення | Статус | Залежності / примітки |
|---|---|---|---|
| `scenes/main.tscn` | Корінь: `SubViewportContainer/SubViewport` 240×320 | OK | `main.gd` |
| `scenes/title/title_screen.tscn` | Титул: title_1..4, Press any key, меню з `M_text.png` | OK | `title_screen.gd`, `title_menu_row.tscn`, `theme_game.tres` |
| `scenes/title/title_menu_row.tscn` | Горизонтальний рядок пункту (атлас M_text) + стрілки | OK | `title_menu_row.gd`, `textures/arrow_title_*.tres` |
| `scenes/game/game_menu.tscn` | Хаб ігрового меню: `MainLayer` (карусель) + `SubmenuLayer` | PART (P0-баг вводу) | `game_menu.gd`, `game_menu_vertical.tscn` |
| `scenes/game/game_menu_vertical.tscn` | Карусель на 3 рядки (txt_m/txt_b, bar_m/bar_b, m_illu) | OK | `game_menu_vertical.gd`; *наслідує* `submenu_shell.tscn` (editable children) |
| `scenes/game/hero_selection.tscn` | Вибір героя ju_1..4 | OK (лише ↑/↓) | `hero_selection.gd`, shell |
| `scenes/game/game.tscn` | Світ: MapRenderer + Player(Camera2D) + GameUI + VirtualPad | PART/BROKEN | `game.gd`, `map_renderer.gd`, `player.tscn` |
| `scenes/game/game_ui.tscn` | HUD: нижня панель, HP/MP | BROKEN (якорі) | `game_ui.gd`; `BottomBar` = x −240…240 |
| `scenes/menus/player.tscn` | Гравець (CharacterBody2D), спрайт `wep_long.png` | PART, **не та папка** | `player.gd`; має лежати в `scenes/game/` |
| `scenes/virtual_pad.tscn` | Тач-джойстик | BROKEN | `virtual_pad.gd`; кнопки `visible=false`, скрипт вмикає лише CanvasLayer |
| `scenes/submenu_shell.tscn` | Спільний шаблон: фон, рамка, тайтл, `LinksVBox`, BACK | OK (ядро UI) | `submenu_shell.gd`, `back_btn_wrap.tscn`, `theme_list_button*.tres` |
| `scenes/back_btn_wrap.tscn` | Кнопка BACK (softbg.png) | OK | `theme_back_button.tres` |
| `scenes/buttons/button_back.tscn` | Шаблон BACK | **BROKEN + DEAD** | `parent="ButtonBack"` замість `"."`; Godot: «Parent path './ButtonBack' … has vanished» |
| `scenes/buttons/button_list_item.tscn` | Шаблон кнопки списку | **BROKEN + DEAD** | те саме (`parent="ButtonListItem"`) |
| `scenes/menus/difficulty_screen.tscn` | Складність Hard/Normal | OK | shell + `Config(menu_id=6)` + `difficulty_screen.gd` |
| `scenes/menus/blacksmith_menu.tscn` | Blacksmith: 3 лінки → «Coming soon» | STUB | shell + `Config(1)` |
| `scenes/menus/gamevil_live_menu.tscn` | Gamevil Live | STUB | shell + `Config(2)` |
| `scenes/menus/management_menu.tscn` | Management: 4 лінки → «Coming soon» | STUB | shell + `Config(4)` |
| `scenes/menus/etc_menu.tscn` | ETC: Save/Load | PART | shell + `Config(5)`; зберігає 3 поля |
| `scenes/menus/endings_screen.tscn` | Endings: 3 «??? (заблокировано)» | STUB | `endings_screen.gd`; в оригіналі 4 кінцівки |
| `scenes/menus/visiting_menu.tscn` | Visiting: таблиця генералів | PART | `generals_select_screen.gd`, `generals_table.tscn` |
| `scenes/menus/mission_menu.tscn` | Сітка місій 4×2 | **DEAD** | `mission_menu.gd`; є в `SUBMENU_SCENES[0]`, але індекс 0 перехоплює `_open_mission_flow()` |
| `scenes/menus/mission_grid.tscn` | Сітка 8 кнопок | **DEAD** | лише з `mission_menu.gd` |
| `scenes/menus/mission_grid_cell.tscn` | Клітинка сітки | **DEAD** | |
| `scenes/menus/menu_row_arrows.tscn` | Старий рядок меню зі стрілками | **DEAD** | `menu_row_arrows.gd` |
| `scenes/screens/license_screen.tscn` | License / About | PART | `license_screen.gd`; текст вигаданий (див. §6) |
| `scenes/screens/help_screen.tscn` | Help | STUB | 1 рядок російською; в оригіналі 9 тем + 39 текстів |
| `scenes/screens/options_screen.tscn` | Options | STUB | «скоро» |
| `scenes/screens/name_screen.tscn` | Ім'я (≥4 символи) | OK (ENTER не підтверджує) | `name_screen.gd` |
| `scenes/screens/stats_screen.tscn` | Розподіл 5 очок | OK | `stats_screen.gd` |
| `scenes/screens/story_screen.tscn` | Пролог з `opening.scr` | OK | `story_screen.gd`, `ScrReader` |
| `scenes/screens/mission_list_screen.tscn` | Список місій | PART (фейкові дані) | `mission_list_screen.gd` |
| `scenes/screens/mission_lord_select.tscn` | Вибір «лорда» | PART (бере імена генералів) | `mission_lord_select.gd` |
| `scenes/screens/mission_briefing_screen.tscn` | Бріфінг | PART (текст-плейсхолдер) | `mission_briefing_screen.gd` |
| `scenes/screens/lord_dialog_screen.tscn` | Діалог з лордом | PART (плейсхолдер, ім'я «Lord N») | `lord_dialog_screen.gd` |
| `scenes/screens/briefing_screen.tscn` | Старий об'єднаний бріфінг/діалог | **DEAD** | `briefing_screen.gd` |
| `scenes/screens/alert_confirm.tscn` | ConfirmationDialog Yes/No | OK | `alert_confirm.gd` (сигнали `confirmed_yes/no` ніде не слухаються) |
| `scenes/screens/modal_message.tscn` | AcceptDialog Ok | OK | `modal_message.gd` |
| `scenes/screens/visiting_general_screen.tscn` | «Діалог» з генералом | STUB | статичний текст «Generals can not be visited at this time.»; BACK-текстура `ui_back.png` (DESIGN §7 забороняє) |
| `scenes/screens/generals_select_screen.tscn` | Інший варіант екрана Visiting | **DEAD** | дублікат `visiting_menu.tscn` з тим самим скриптом |
| `scenes/screens/generals_table.tscn` | HeaderRow + Row0..5 | OK | заголовок показує дефолтні «name / 0» |
| `scenes/screens/generals_table_row.tscn` | Рядок: NameCell + RelCell | OK | `generals_table_row.gd` **не підключений** |

### 1.2 Скрипти (36)

| Скрипт | Роль | Статус / примітки |
|---|---|---|
| `game_state.gd` (autoload) | Константи, режим вводу, генерали, лорди, місії, save | PART: 18 полів/методів ніде не використовуються (§3.5), дані — плейсхолдери |
| `sound_manager.gd` (autoload) | MIDI через `MidiPlayer` (addon) + `FluidR3_GM.sf2` | PART: без аддона не компілюється; `set_music_volume_db()` падає на `null`, якщо немає sf2 |
| `main.gd` | Перемикач екранів (15 функцій `_show_*`) + форвардинг вводу | PART (P0, §2.4) |
| `title_screen.gd`, `title_menu_row.gd` | Титул | OK |
| `game_menu.gd` | Хаб підменю, флоу місій, Save/Load, модалки | PART (P0); `_push_content_screen()` мертвий; `SUBMENU_CONFIG` дублює `submenu_config.gd` |
| `game_menu_vertical.gd` | Карусель | OK; `_items_vbox`, `_carousel_step` не потрібні; `load()` ілюстрації на кожен кадр зміни |
| `submenu_shell.gd` | Шаблон | OK; `get_links_container()`, `set_display_title()` не використовуються |
| `submenu_config.gd` | Конфіг лінків за `menu_id` | OK, але дублікат; записи 0 (Mission) і 3 (Visiting) мертві |
| `difficulty_screen.gd`, `hero_selection.gd`, `name_screen.gd`, `stats_screen.gd`, `story_screen.gd` | Флоу нової гри | OK (зауваження в §3) |
| `license_screen.gd`, `help_screen.gd`, `options_screen.gd`, `endings_screen.gd` | Текстові екрани | 4 майже ідентичні копії (≈40 рядків кожна); `_on_back()` мертві |
| `mission_list_screen.gd`, `mission_lord_select.gd`, `mission_briefing_screen.gd`, `lord_dialog_screen.gd` | Флоу місій | PART: UI будується кодом (порушення «scenes-first»), дані фейкові |
| `briefing_screen.gd` | Старий бріфінг | **DEAD** |
| `mission_menu.gd`, `menu_row_arrows.gd`, `generals_table_row.gd` | — | **DEAD** |
| `generals_select_screen.gd` | Visiting | PART: клік/тап по рядку нічого не робить (у кнопок немає `pressed`) |
| `visiting_general_screen.gd` | +5 дружби при закритті | STUB |
| `alert_confirm.gd`, `modal_message.gd` | Діалоги | OK |
| `game.gd`, `map_renderer.gd`, `player.gd`, `game_ui.gd`, `virtual_pad.gd` | Світ | PART/BROKEN (§3.2) |
| `scr_reader.gd` (`class_name ScrReader`) | Читач `.scr` | OK, неповний (§3.7) |

### 1.3 Залишки в корені та що можна видаляти

**Безпечно видалити (посилань немає, перевірено grep і смоук-тестом):**
- `scenes/buttons/button_back.tscn`, `scenes/buttons/button_list_item.tscn` — биті й не використовуються;
- `scenes/menus/mission_menu.tscn` + `scripts/mission_menu.gd`, `scenes/menus/mission_grid.tscn`, `scenes/menus/mission_grid_cell.tscn`. Перед цим прибрати `mission_menu.tscn` з `SUBMENU_SCENES` у `game_menu.gd:8` і зсунути індекси (або замінити на `null`);
- `scenes/menus/menu_row_arrows.tscn` + `scripts/menu_row_arrows.gd`;
- `scenes/screens/briefing_screen.tscn` + `scripts/briefing_screen.gd`;
- `scenes/screens/generals_select_screen.tscn` (скрипт залишити — його використовує `visiting_menu.tscn`);
- `scripts/generals_table_row.gd`. Або підключити до `generals_table_row.tscn` і використовувати замість ручного обходу нод у `generals_select_screen.gd`;
- `readme.md` у корені — це README аддона godot-midi-player, а не проєкту;
- `gamestr_strings_full.txt` — байт-у-байт дорівнює `gamestr_strings.txt` і так само обрізаний;
- `kemulator.cfg` — конфіг емулятора.

**Не видаляти, а перенести.** `*.java`, `JAVA_REFERENCE.md`, `META-INF/`, `.jad` — у `original/` або `reference/`. Двійкові дані (`*.MAP`, `*.arr`, `*.scr`, `item-mixing-table.bin`, `*.SP3`, `*.pal`, `*.ft2`) — у `data/original/`. Зараз вони лежать у корені `res://` разом із 48 Java-файлами. Плутанина — не головна біда. Головне: `.scr/.arr/.MAP` **не потраплять в експорт** без include-фільтра (§3.7).

**Застарілі, оновити або видалити:** `GODOT_README.md` (§6), `decode_scr.py` (баг: зупиняється на першому порожньому записі, §3.7), `uimenu_strings.txt` і `gamestr_strings.txt` — обрізані дампи (28 з 60 і 67 з 71 записів).

**Зазначені в задачі, але відсутні в копії** (оцінити неможливо; загальні правила):
- `scenes/*.tmp` — тимчасові файли редактора Godot, видаляти безпечно завжди;
- кореневі `main.gd`/`main.tscn` — `project.godot` вказує `run/main_scene="res://scenes/main.tscn"`, тож кореневі майже напевно залишки. Перевірка перед видаленням: `grep -rn "res://main\.\(gd\|tscn\)" --include=*.gd --include=*.tscn --include=*.godot .`;
- `openxr_action_map.tres` — Godot створює його автоматично; без XR видалити, переконавшись, що `xr/openxr/enabled` вимкнено;
- `views/` і `godot_midi.gd`/`midi_*.gd` — схоже на демо аддона MIDI; видалити, якщо grep не знаходить посилань з `scripts/`/`scenes/`;
- `addons/midi` — **потрібен** (`sound_manager.gd` використовує `MidiPlayer`, а `project.godot` вмикає `res://addons/midi/plugin.cfg`).

---

## 2. Фактичний runtime-флоу

### 2.1 Autoload і налаштування

- Autoload: `GameState` (`scripts/game_state.gd`) і `SoundManager` (`scripts/sound_manager.gd`). Editor plugin: `res://addons/midi/plugin.cfg`.
- Вікно та рендер:
  - вікно 240×320, `stretch/mode="canvas_items"`, `window/size/mode=2` (maximized), `handheld/orientation=1`;
  - рендерер **Forward Plus**: для 2D-гри під мобільні краще `gl_compatibility` або `mobile`;
  - `default_texture_filter` не задано (Linear), тож піксель-арт при масштабуванні розмиватиметься.
- `GameState._ready()`:
  - `_ensure_input_actions()` додає дії **лише якщо їх немає**. Оскільки `project.godot` вже містить `menu_prev/menu_next/menu_confirm`, рантаймові прив'язки для меню (Left/Right/Space/KP_Enter) мертві. Реально додаються тільки `move_*` (WASD + стрілки);
  - `detect_input_mode()`, потім `_init_generals_if_needed()` — заповнення демо-даних.

**Фактичний Input Map (з рантайму):** `menu_prev = Up`, `menu_next = Down`, `menu_confirm = Enter`, `move_left = A, Left` (і так далі), `ui_*` дефолтні. **Жодного джойпад-івента в `menu_*`/`move_*`.** Геймпад працює лише там, де код дивиться на дефолтні `ui_up/ui_down/ui_cancel`: карусель, `submenu_shell`.

### 2.2 SubViewport

`main.tscn` містить `Main (Control)` → `GameContainer (SubViewportContainer, stretch=true)` → `SubViewport (240×320, handle_input_locally=true, update=always)`. Як це працює з вводом у Godot 4.5 (перевірено за вихідним кодом `scene/gui/subviewport_container.cpp`, тег 4.5-stable):

- На ENTER_TREE контейнер примусово робить `SubViewport.handle_input_locally = false`. Значення з `.tscn` ігнорується; рантайм показує `false`. Тому `get_viewport().set_input_as_handled()` усередині SubViewport позначає подію обробленою **в root-вікні**.
- Непозиційні події (клавіші, геймпад) контейнер передає в SubViewport:
  - через `unhandled_input`, якщо контейнер не у фокусі (за замовчуванням);
  - через `input`, якщо контейнер у фокусі. `focus_mode = FOCUS_CLICK`, тобто фокус з'являється після першого кліку мишею у вікно.

Отже клавіатура **вже** доходить до екранів у SubViewport без жодного форвардингу. `Main._input()` (`main.gd:26-32`) додає другий, паралельний шлях.

Окрема думка: SubViewport тут нічого не дає. Root-вьюпорт і так 240×320 у режимі `canvas_items`. Див. §5.

### 2.3 Граф екранів (що досяжне)

```
TitleScreen ── Press any key ──► меню M_text (9 пунктів, ↑/↓, Enter)
  0 Continue ───────────────► GameMenu (без завантаження сейву!)
  1 New Game ─► Difficulty ─► HeroSelection ─► Name ─► Stats ─► Story(opening.scr) ─► GameMenu
               (back→Title)   (back→Difficulty) (back→Title!) (back→Title!)
  2 Options / 3 Help / 4 Endings / 5 About(=License) ─► текстовий екран ─► Title (Enter/Esc/BACK)
  6 More Games / 7 Multiplayer ─► SubmenuShell-заглушка ─► Title (лише Esc/BACK)
  8 Exit ─► quit
GameMenu (карусель 6: Mission, Blacksmith, Gamevil Live, Visiting, Management, ETC; Esc ─► Title)
  Mission ─► MissionList(1 фейкова місія) ─► LordSelect(6 «лордів» = імена генералів)
          ─► MissionBriefing(плейсхолдер) ─► ConfirmationDialog «Ви готові…» ─► LordDialog ─► Game
  Blacksmith / Management ─► лінки ─► модалка «Coming soon»
  Gamevil Live ─► лінк «Coming Soon» ─► модалка
  Visiting ─► (can_visit_generals=false → модалка) / таблиця 2 генералів ─► VisitingGeneralScreen(+5)
  ETC ─► Save / Load (3 поля) ─► модалка
Game ─► (тупик: ні паузи, ні Esc, ні завершення місії)
```

Музика: `title` (snd0) на титулі, `menu` (snd2) у GameMenu, `game` (snd1) у Game. Під час флоу нової гри трек не змінюється, лишається snd0.

### 2.4 Як насправді обробляється ввід

Хто з екранів має який обробник:

| Має `process_menu_input` (викликає Main) | Має лише `_input` (отримує через SubViewport) |
|---|---|
| title_screen, title_menu_row, game_menu, game_menu_vertical, license/help/options/endings | hero_selection, stats, story, submenu_shell (і все, що його інстанціює), generals_select_screen, visiting_general_screen |

Половина екранів має **обидва** обробники з однаковим кодом (`title_screen.gd:39-53`, `game_menu.gd:59-63`, license, help, options, endings). Подвійної обробки немає лише тому, що перший обробник викликає `set_input_as_handled()`, а той піднімається до root.

**Корінь P0-бага.** `game_menu.process_menu_input()` і `game_menu._input()` (`game_menu.gd:59-67`) **завжди** передають подію каруселі, навіть коли `MainLayer` прихований і відкрито підменю. Карусель (`game_menu_vertical.gd:82-99`) обробляє Up/Down/Enter/Esc і позначає подію обробленою. Що з цього виходить:
- **Контейнер не у фокусі** (клавіатура з самого старту). Подію першим отримує `Main._input` → `GameMenu` → прихована карусель. До підменю нічого не доходить.
- **Контейнер у фокусі** (після кліку мишею). У SubViewport першим спрацьовує `_input` верхнього підменю. Esc обробляє `submenu_shell`, і це працює. Але Up/Down у списках, побудованих не через `set_menu()` (місії, лорди), підменю не обробляє, тож подія знову падає в карусель.

**Підтвердження з автотесту** (`05_godot_audit_tools/flow_test.gd`, лог `/home/claude/pow_audit_logs/2_flow_test.log`):

```
mission opened:             carousel_idx=0 main_visible=false submenu=[MissionListScreen]
after DOWN in mission list: carousel_idx=1 main_visible=false submenu=[MissionListScreen]
after ENTER in mission list:carousel_idx=1 main_visible=false submenu=[BlacksmithMenu]   ← відкрився не той екран
after ESC in submenu:       cur=TitleScreen                                              ← вилетіли на титул
focused, after DOWN in submenu: carousel_idx=1 …                                          ← у фокус-режимі теж
visiting opened:            submenu=[VisitingMenu]
after ENTER in visiting:    submenu=[@Control@439]  ← Visiting перевідкрився замість діалогу з генералом
```

Інші підтверджені факти:
- на титулі ←/→ не працюють, працюють ↑/↓, хоча меню горизонтальне;
- у HeroSelection так само: RIGHT змінює героя з 0 на 0, DOWN — з 0 на 1;
- у NameScreen ENTER не підтверджує ім'я: `text_submitted` не підключено, потрібен клік по OK або Tab+Space;
- у грі Esc нічого не робить.

---

## 3. Коректність

### 3.1 Результати headless-валідації

Godot 4.5-stable завантажився без проблем. Перевірки:

1. **Сира копія** (`/home/claude/pow_check`, `--import` і `--quit-after 120`). Усі помилки — наслідок відсутніх ассетів:
   - `Preload file "res://theme_list_button.tres" does not exist` у `submenu_shell.gd:10-11`. Це **parse error**, а не warning: відсутня тема валить компіляцію `submenu_shell.gd` і всіх екранів, що від нього залежать;
   - `Identifier "MidiPlayer" not declared` у `sound_manager.gd:13,20`. Без аддона autoload `SoundManager` не створюється, `main.gd` падає на `SoundManager.play_music` (Nil);
   - решта — `Failed loading resource *.png/*.tres`.
2. **Копія із заглушками** (`/home/claude/pow_check_stub`: згенеровані PNG потрібних розмірів, порожні Theme, AtlasTexture, мінімальний клас-заглушка `MidiPlayer` з тим самим API). Імпорт, запуск `main.tscn` на 120 кадрів, інстанціювання **всіх 42 сцен** і скриптований прохід флоу дали **0 SCRIPT ERROR**. Лишилися тільки:
   - 2× `Parent path … has vanished` (`scenes/buttons/*.tscn`);
   - попередження про відсутній soundfont;
   - 38 попереджень `invalid UID`. Вони очікувані, бо `.uid`/`.import` не скопійовано, але див. 3.6.
3. **Попередження GDScript** (копія `/home/claude/pow_check_warn`: усі дефолтні попередження переведені в error, крім `return_value_discarded`, який у Godot за замовчуванням вимкнений). Їх 7:
   - `game_state.gd:207` — integer division;
   - `game_menu_vertical.gd:37` — `_items_vbox` не використовується;
   - `game_ui.gd:10` — `_bottom_bar` не використовується;
   - `map_renderer.gd:98` — `tile_x`, `tile_y` не використовуються;
   - `name_screen.gd:31` — змінна `len` затіняє вбудовану функцію;
   - `title_screen.gd:7` — сигнал `show_license` ніколи не емітиться.
4. Режим `--check-only -s` для скриптів із autoload **непридатний**: autoload-и не реєструються, і з'являється хибне «Identifier not found: GameState».

API Godot 3.x не знайдено: `@onready`, `Tween` через `create_tween()`, `FileAccess`, типізовані масиви — усе Godot 4. Шляхи `$...`/`get_node` у пройдених екранах розв'язались без помилок.

### 3.2 Баги (за пріоритетом)

**P0**
1. Прихована карусель перехоплює ввід у всіх підменю (§2.4). Файли: `game_menu.gd:59-67`, `main.gd:26-32`.
2. Флоу місій семантично перевернутий. Java: спершу `C()` → список сторін/кампаній `dt[]` з `mission.arr` (для cq=0 одна: «The Rise»), потім `bi()` → місії цієї сторони, назви `dA[]` з `ruler.arr` через `sideinfo.arr` (для «The Rise» 4 місії: Lord Gabriel, Lord Frederick, Lord Vincent, Lord Edison, спавн (4,2)/(4,20)). Порт показує спочатку «місії» (1 шт., «First Strike»), потім «лордів» (6 шт.). У `game_state.gd:66-67` кількості переплутані (`missions_count_in_chapter=1`, `lords_count_in_chapter=4`). Коментар у `mission_list_screen.gd:2` сам каже «bi() → dA[]», а `bi()` вимагає вже вибраного `dk`.
3. Один лорд на трьох екранах має три різні імена (автотест): у списку «Reeve» (`mission_lord_select.gd:44` бере **`general_names`**), у підтвердженні «Lord North» (`game_menu.gd:142`, `lord_names`), у діалозі «[Lord 1]» (`game_menu.gd:160`).

**P1**

4. Карта скролиться вдвічі. `game.gd:17-28` щокадру зсуває `MapRenderer` на `center − player`, а `Camera2D` (дочірня до `Player`, `game.tscn`) ще й слідкує за гравцем. Тест: гравець +27 px → тайл на екрані −54 px.
5. Немає колізій: у MapRenderer немає колізійних форм, `is_walkable()` не викликається. Гравець вільно йде в (−2000, −2000). Рух — вільний 90 px/с, а не по тайлах.
6. HUD за екраном. `game_ui.tscn`: `BottomBar` має `anchors_preset=12` (bottom-wide) і `offset_left=-240`, тож rect = (−240,259) 480×61. `HpMpContainer` = (−232,266) 464×46. HP/MP — дефолтні ProgressBar, а не `ball_black` з Java; `set_hp_mp()` ніхто не викликає.
7. Віртуальний джойстик ніколи не видно. Кнопки `PadLeft/PadRight/PadUp/PadDown` мають у сцені `visible=false`, а `virtual_pad.gd:24-25` перемикає лише `CanvasLayer.visible`. Тест у TOUCH-режимі: `VirtualPad.visible=true`, кнопки `false`. Плюс на мобільному (TOUCH) Visiting непрохідний, бо рядки не клікабельні (п. 10).
8. З гри немає виходу: ні паузи (в оригіналі `uimenu[41]`: «Resume|Options|Save|Assign Items|Help|Exit to Menu|Exit Game»), ні завершення місії. `set_mission_completed()` не викликається ніде, тож прогресія неможлива.
9. Save/Load: `game_state.gd:265-297` зберігає лише `hero_index`, `difficulty_index`, `player_name`. Стати, слава, генерали, прогрес не зберігаються (тест: `stat_atk` після load = 1). «Continue» на титулі не викликає `load_game()` (`main.gd:39` → `_on_show_game_menu`) і не буває вимкненим, хоча рядок 9 у M_text — «Continue (disabled)».
10. Visiting: у кнопок рядків (`NameCell/Button`) немає `pressed`, тож клік і тап нічого не роблять (`generals_select_screen.gd:60-82`). Шапка таблиці показує «name / 0». Якщо запрошених немає, ENTER все одно емітить генерала 0.

**P2**

11. `NameScreen`: ENTER у LineEdit не підтверджує ім'я. «Назад» з Name і Stats веде на **титул** (`main.gd:140,150`), а з Hero — на Difficulty: непослідовно.
12. `sound_manager.gd:48-49`: `set_music_volume_db()` без перевірки `_midi_player == null` впаде, якщо sf2 відсутній. `FluidR3_GM.sf2` — це близько 140 МБ (і він має потрапити в експорт), що для мобільного білду неприйнятно (§5).
13. `main.gd:30`: `_viewport.get_child(0)` у кадрі, де екран щойно замінено, повертає старий екран, позначений `queue_free`. Рідкісний race при двох подіях за кадр.
14. `game_menu.gd` п'ять разів повторює шаблон «очистити SubmenuLayer → інстанціювати → підключити». Нові ноди з тим самим ім'ям отримують авто-імена (`@Control@439`), бо старі ще не звільнені. Так само `generals_select_screen.gd:57` перейменовує дублікати рядків у зайняті імена.
15. `ConfirmationDialog`/`AcceptDialog` вбудовуються в root-вікно (`is_embedded=true`), а не в SubViewport. Тема в них дефолтна, Godot-розміру; текст підтвердження українською («Ви готові…», «Так/Ні») серед англомовного UI.
16. Endings показує 3 кінцівки, а файлів `ending0..3.scr` чотири. License приписує копірайт «Thanhdaik» — це `MIDlet-Vendor` з MANIFEST перепакувальника, а не правовласник; гра — Gamevil.
17. `visiting_general_screen.tscn`: текст «Generals can not be visited at this time.» показується навіть тоді, коли відвідування дозволене. BACK має текстуру `ui_back.png` замість `softbg.png`.
18. `ScrReader` читає файл повністю при кожному виклику, без кешу. Два записи (`brief.scr[24]`, `event3.scr[45]`) містять сирі байти CP949 (`0xA1AF`, `0xA1A6`), і `get_string_from_utf8` видасть Unicode-помилки.

### 3.3 Шляхи нод `.gd` ↔ `.tscn`

Усі `@onready`/`$`-шляхи пройдених екранів розв'язались у рантаймі: титул, ігрове меню з каруселлю, усі екрани місій, Visiting, діалог генерала, модалки, Difficulty/Hero/Name/Stats/Story, License/Help/Options/Endings/More Games/Multiplayer, Game. Автотест і смоук-тест усіх 42 сцен не дали жодного «Node not found». Зауваження:
- `scenes/buttons/*.tscn` мають неправильні `parent=`: битий шлях у самій сцені;
- `hero_selection.tscn`, `name_screen.tscn`, `stats_screen.tscn` додають дітей у `SubmenuShell/MainLayer/MenuFrame/LinksVBox` **без** `[editable path="SubmenuShell"]`. Godot це завантажує, але в редакторі ці ноди «невидимі» всередині інстансу. Крихко: перейменування `LinksVBox` у shell мовчки зламає 4 сцени і 7 скриптів, які звертаються до нього рядковим шляхом. Варто виставити `LinksVBox` як `%LinksVBox` (unique name) або віддавати через метод `get_content()`, як уже частково зроблено;
- `difficulty_screen` та інші з `Config`: `submenu_config._ready()` спрацьовує раніше за `_ready()` shell-а (діти готуються першими), тож `set_menu()` бачить `@onready` = null. Працює лише завдяки null-перевіркам у `_update_ui()`.

### 3.4 Сигнали

Підключень до неіснуючих методів не знайдено: усі `connect(...)` вказують на існуючі функції або лямбди. Мертві сигнали:
- `title_screen.show_license` — ніколи не емітиться;
- `mission_list_screen.back_to_lords` — ніхто не слухає, бо `lord_index` завжди −1;
- `alert_confirm.confirmed_yes/confirmed_no` — ніхто не слухає;
- `generals_select_screen.closed` — ніхто не слухає;
- `mission_menu.mission_selected` — мертва сцена;
- `main.gd` перевіряє `has_signal()` для 8 сигналів титулу, які завжди існують. Це маскує помилки, замість того щоб їх виявляти.

### 3.5 Невикористані змінні та функції

- **GameState:** `screen_type`, `ScreenType`, `menu_index`, `selected_battle_general_id`, `player_lord_id`, `lord_generals` (+ `_init_lord_generals`, `is_general_of_lord`, `get_general_ids_allowed_on_battlefield`), `mission_chapter`, `lords_count_in_chapter` (зовні), `mission_names` (зовні), `mission_completed`, `set_mission_completed`, `camera_tile_x/y`, `camera_offset_x/y`, `spawn_tile_per_lord`, `MAP_VISIBLE_COLS/ROWS` (лише в map_renderer). Приватна функція `_init_generals_if_needed()` викликається з 4 інших скриптів.
- **Решта:** `game_menu._push_content_screen()`; `_show_coming_soon()` дублює `_show_modal()`; `submenu_shell.get_links_container()`/`set_display_title()`; `game_menu_vertical.get_current_index()`, `setup_menu_items()` (порожній); `map_renderer.set_level()/get_tile_at_pixel()/is_walkable()`; `game_ui.set_hp_mp()`; `sound_manager.set_music_volume_db()`; `_on_back()` у 4 текстових екранах і в `mission_menu`.

### 3.6 Дублювання та сміття в конфігурації

- `game_menu.gd:35-42` `SUBMENU_CONFIG` ≡ `submenu_config.gd:6-12` `CONFIGS[0..5]`. Перший використовується лише для `links.is_empty()`, другий реально заповнює shell. Синхронізація вручну (vault Task #6/#7 «обидва файли синхронізовані») — гарантований майбутній розсинхрон. `MENU_ITEMS` у `game_menu.gd:26` і `MENU_LABELS` у `game_menu_vertical.gd:7` — ще одна копія.
- `license/help/options/endings_screen.gd` — 4 копії одного екрана. `briefing_screen.gd` ≈ `mission_briefing_screen.gd` + `lord_dialog_screen.gd`.
- Двічі продубльовано `PORTRAIT_PATHS = ju_1..4` (hero, stats, story), шаблон `load("res://jang_%d.png")` — тричі.
- Рукописні UID: 24 сцени мають вигадані `uid://cmain001`, `uid://heroselect` і подібні. 9 з них синтаксично невалідні, бо містять `_`: `uid://mission_grid_01`, `uid://mission_list_screen`, `uid://alert_confirm_01` та ін. Godot ігнорує такі UID і пише warning при кожному завантаженні. Слід перезберегти сцени в редакторі.

### 3.7 Захардкоджені дані проти оригінальних файлів і повнота `scr_reader.gd`

Усі `.arr`-таблиці мають один формат — Java-клас `d`: байт N колонок, N ширин, далі рядки. Один читач на 30 рядків покриває `general.arr` (141×13), `kibo.arr` (100×8), `sungbo.arr` (137×9), `shinki.arr` (18×8), `visitgen.arr` (44), `visitpro.arr` (9×8), `exp.arr` (199). Решта — фіксовані записи (`mission.arr`: 38 Б, `sideinfo.arr`: 11 Б, `ruler.arr`: 15 Б).

| Що захардкоджено | Де | Справжнє джерело |
|---|---|---|
| 37 генералів «General N», «Reeve», «Gabriel», демо-запрошення/дружба | `game_state.gd:37,159-174` | `general.arr` (141 запис, кол. 0 = ім'я; «Gabriel» насправді «Lord Gabriel» з `ruler.arr`); запрошені — `visitgen.arr` + прогрес |
| «Лорди» Lord North/South/East/West, 6 слотів, усі розблоковані | `game_state.gd:57-58,176-184,222-227` | `mission.arr` `ds/dt/du/dv` за главою `cq` (cq=0: «The Rise»); розблокування — бітмаска `dw` |
| Назви місій «First Strike»… | `game_state.gd:190` | `ruler.arr` через `sideinfo.arr[].a` |
| Кількості `missions=1`, `lords=4` | `game_state.gd:66-67` | `mission.arr` `dv[dk]` (4), `dr` (1) |
| `Z_RANGES [5,3,6,3,5,6,7,2,2]` як «кількість місій» | `mission_list_screen.gd:56` | **хибне джерело**: це різниці `ae.z` (офсети Help/Story); місій — `dv[dk]` |
| Спавн (4,4) | `game_state.gd:220` | `sideinfo.arr` b,c (напр. (4,2), (4,20)) |
| Текст бріфінгу | `game_menu.gd:130` | `brief.scr[du[dk]+dm]` (102 записи) |
| Репліка лорда | `game_menu.gd:162` | `event*.scr`, `v(57+dG)` (ag.z()) |
| Пункти меню | `game_menu.gd:26-42`, `submenu_config.gd`, `game_menu_vertical.gd:7` | `uimenu.scr`: [36] ігрове меню, [39] Blacksmith «Buy\|Sell\|Enchant\|Combine», [40] Management «Attributes\|Skills\|Gear\|Inventory\|Assign Items», [37] ETC «Options\|Help», [41] пауза, [0..29] заголовки екранів |
| Help (1 рядок RU) | `help_screen.gd:15` | `uimenu[38]` — 9 тем; `help.scr` (39), `help_m.scr` (5) |
| Endings (3 заглушки) | `endings_screen.gd:17` | `ending0..3.scr`, повідомлення про блокування з `gamestr` |
| Options («скоро») | `options_screen.gd:13` | `uimenu[42..59]`: Sound/Volume/Speed/Diff, OFF/ON, Slow…Fast |
| License-текст | `license_screen.gd:7-21` | вигаданий |
| «Please select a character for battle.», заголовки «CHARACTER/NAME/STATS» | `hero_selection.tscn`, `*_screen.gd` | `gamestr[65,66]`, `uimenu[6,7,8]` (у Java «ATTRIBUTES», а не «STATS») |
| Демо-карта 20×20 | `map_renderer.gd:48-61` | `mdat_QVGA.scr` → `N.arr`/`*.MAP` (карта = `ds[dk]`) |
| Предмети, досвід | відсутні | `kibo/sungbo/shinki.arr`, `item-mixing-table.bin`, `exp.arr` |

**`scr_reader.gd`: що є і чого бракує.**
- **Формат правильний** і відповідає `al.java`: офсети LE з `2+i*2`. Використовує лічильник із заголовка, і це **краще**, ніж `decode_scr.py`. Python-скрипт обриває читання на першому порожньому записі (`decode_scr.py:71`), тому `uimenu_strings.txt` (28/60) і `gamestr_strings.txt` (67/71) неповні. Через це, найімовірніше, у Tasks #6/#7 і в `BLACKSMITH_SPEC` пропустили `uimenu[39..41]`.
- **Бракує:**
  - кешу й API доступу за індексом (`get(path, i)`);
  - fallback для CP949-байтів (див. 3.2.18);
  - пост-обробки форматів: `|`-списки, `\` як перенос рядка, префікс типу вікна «1»/«2» у `gamestr`, записи `0|Lord Frederick|…` у `brief.scr`, `[Speaker]` у діалогах;
  - читачів `.arr` (клас `d`) і фіксованих записів (`mission`/`sideinfo`/`ruler`), карт (`*.MAP`, `N.arr`), `item-mixing-table.bin`.
- **Експорт.** `FileAccess.open("res://opening.scr")` працює в редакторі, але в експортованому білді не-ресурсні файли (`*.scr`, `*.arr`, `*.MAP`, `*.bin`, `*.mid`, `*.sf2`) **не включаються** без «Filters to export non-resource files». Інший варіант — один раз конвертувати дані в `.tres`/`.json`.

---

## 4. Як запустити валідацію (відтворювано)

Інструменти лежать у `/home/claude/analysis/05_godot_audit_tools/`:
- `make_stubs.py` — заглушки ассетів;
- `flow_test.gd` — скриптований прохід вводу і флоу;
- `all_scenes.gd` — інстанціювання всіх сцен;
- `load_all.gd` — компіляція всіх скриптів;
- `run_checks.sh` — усе разом.

```bash
# одноразово
mkdir -p /home/claude/godot && cd /home/claude/godot
curl -L -o godot.zip https://github.com/godotengine/godot/releases/download/4.5-stable/Godot_v4.5-stable_linux.x86_64.zip
unzip -o godot.zip && chmod +x Godot_v4.5-stable_linux.x86_64

# повний прогін (вихідний /home/claude/pow не змінюється; копії: pow_check, pow_check_stub, pow_check_warn)
/home/claude/analysis/05_godot_audit_tools/run_checks.sh      # логи → /home/claude/pow_audit_logs/

# окремі кроки вручну
G=/home/claude/godot/Godot_v4.5-stable_linux.x86_64
$G --headless --path /home/claude/pow_check_stub --import
$G --headless --path /home/claude/pow_check_stub --quit-after 120          # запуск main.tscn
$G --headless --path /home/claude/pow_check_stub res://audit/flow_test.tscn # автотест вводу/флоу
```

Важливо: `--check-only -s res://scripts/x.gd` дає хибні помилки для скриптів, що звертаються до autoload. Компіляцію треба перевіряти запуском сцени (`load_all.gd`). Попередження Godot у консоль не друкує, тому для них потрібна копія з `debug/gdscript/warnings/*=2`.

---

## 5. Архітектура перед кроком «карта, бій, предмети, кампанія»

### 5.1 Що зараз

- **`GameState`** — God-object на 320 рядків. У ньому змішані:
  - константи екрана;
  - сервіс режиму вводу;
  - плейсхолдер-дані кампанії й генералів;
  - save/load;
  - реєстрація input actions.

  Типізованої моделі немає, сигналів зміни стану немає (крім `input_mode_changed`). Третина полів не використовується, «приватні» функції викликаються ззовні.
- **`main.gd`** — імперативний перемикач: 15 майже однакових `_show_*`, перевірки `has_signal`, без стека історії. Тому «назад» із Name/Stats веде на титул.
- **`game_menu.gd`** — другий перемикач усередині першого, зі своїм ручним «стеком» через `queue_free`.
- **Ввід** — дві паралельні системи (`Main._input → process_menu_input` і SubViewport → `_input`), до того ж приховані шари не вимикаються.
- Порушення «scenes-first» з CLAUDE.md: License/Help/Options/Endings, список місій, лорди, бріфінг, діалог лорда, тайли карти й позиції пада будуються кодом у `_ready()`.

### 5.2 Цільова структура (мінімальна, ідіоматична для Godot)

```
autoload:
  GameData      scripts/data/game_data.gd     — read-only: кампанія, генерали, предмети, рядки (з оригінальних файлів або сконвертованих .tres)
  GameState     scripts/state/game_state.gd   — лише runtime-стан + save/load + сигнали changed
  SoundManager  (як є, + null-guard)
  (InputMode → scripts/state/input_mode.gd або залишити в GameState, але окремим блоком)
scripts/data/    scr_reader.gd, arr_table.gd (клас d), campaign_loader.gd (mission/sideinfo/ruler/brief), map_loader.gd
scripts/state/   player_state.gd, campaign_state.gd, relations_state.gd (class_name … extends Resource)
scripts/systems/ combat_rules.gd, inventory.gd, progression.gd — чисті статичні функції, тестовані headless
scenes/ui/       screen_router (main), text_screen.tscn, list_button.tscn, hud.tscn, pause_menu.tscn
scenes/world/    world.tscn (TileMapLayer + TileSet з N_XX.png), player.tscn, enemy.tscn, npc.tscn
scenes/battle/   battle.tscn (якщо бій окремим екраном, Java cM[0]=20)
tests/           headless-ранер (на основі flow_test.gd) — запускати перед кожним мержем
```

- **Стан.** `PlayerState`: герой, ім'я, рівень, exp, gold, fame, стати, очки, 25 слотів інвентаря, екіпіровка. `CampaignState`: `cq`, бітмаска сторін `dw`, біти завершених місій `dy`, поточні `dk/dm`. `RelationsState`: friendship[], invited[]. Save — одна `to_dict()/from_dict()` з полем `version`.
- **Місія.** Флоу місій створює `MissionContext` (Resource: side id, mission index, map id, spawn, battle id, time limit, gold mult) і передає його у `world.start(ctx)`. Наприкінці світ викликає єдиний `GameState.apply_mission_result(result)`. Бойовий і картовий runtime-стан живе у сцені світу, **не в autoload**.
- **Навігація.** `main.tscn` стає роутером зі стеком: `ROUTES := {&"title": preload(...), …}`. Кожен екран емітить уніфіковані `navigate(route, args)` / `back()`. Неактивні (нижні) екрани отримують `process_mode = PROCESS_MODE_DISABLED`; це вимикає і їхній `_input`. Те саме — для `MainLayer` у game_menu, поки відкрито підменю. Так P0 закривається системно, а не латками.
- **SubViewport.** Рекомендую прибрати `SubViewportContainer`: root і так 240×320 у `canvas_items`. Для піксель-арту краще `stretch/mode="viewport"`, `stretch/scale_mode="integer"`, `rendering/textures/canvas_textures/default_texture_filter=0` (Nearest). Якщо SubViewport потрібен (наприклад, для майбутнього пост-шейдера), то обов'язково видалити `Main._input`-форвардинг і всі `process_menu_input`. В обох варіантах ввід іде **одним** шляхом.
- **Карта.** Замість Sprite2D на кожен тайл і ручного зсуву — `TileMapLayer` + `TileSet` з `N_01..16.png` (27×27) з колізійним шаром, `Camera2D` з `limit_*` за розміром карти. Дані карти бере `map_loader.gd`.
- **Аудіо.** DESIGN §2.2 і JAVA_REFERENCE §8 радять конвертувати `snd0/1/2.mid` в `.ogg`. Це прибирає залежність від аддона і близько 140 МБ `FluidR3_GM.sf2` з мобільного білду.

### 5.3 Конкретні рефактори, які потрібні **до** геймплею (у порядку)

1. Єдиний шлях вводу + вимкнення неактивних шарів (TD-1) і Input Map з DESIGN §4.2 (TD-2).
2. Шар даних (`ArrTable`, `ScrReader` з кешем, `GameData`) і заміна плейсхолдерів (TD-3), потім виправлення семантики флоу місій (TD-4).
3. Модель стану й повний save (TD-7).
4. Базова ігрова сцена: TileMapLayer, одна камера, колізії, HUD, пауза, пад (TD-5).
5. Роутер екранів і прибирання дублікатів та мертвого коду (TD-8, TD-9).

**CLAUDE.md** містить правило «Do not modify existing working functionality unless explicitly asked». Пункти TD-1, TD-8 і TD-9 зачіпають робочий код, тож для них потрібен явний дозвіл власника, бажано одним рішенням на всю групу.

---

## 6. Документація проти реальності

| Твердження | Джерело | Насправді |
|---|---|---|
| «Реалізовано: Навігація по меню (тайтл → нова гра → меню)» | vault/01 | Лише до ігрового меню; у підменю клавіатура керує прихованою каруселлю (§2.4) |
| «Реалізовано: Мультиінпут touch/gamepad/клавіатура» | vault/01, GODOT_README | Пад ніколи не видно; у `menu_*`/`move_*` немає жодної джойпад-прив'язки; у Visiting не працює тап |
| «Реалізовано: Рух гравця по тайлах» | vault/01 | Вільний рух 90 px/с, без сітки й колізій |
| «Реалізовано: Рендер карти з PNG тайлів» | vault/01 | Демо-сітка 20×20 у коді; скрол удвічі |
| «Реалізовано: Система 37 генералів» | vault/01 | 35 «General N» + 2 імені, демо-дружба; в оригіналі 141 запис |
| «Реалізовано: MIDI музика (3 треки)» | vault/01 | Залежить від аддона та ~140 МБ sf2 (у копії немає жодного) |
| «Реалізовано: Флоу місій» | vault/01 | Лише кліком, фейкові дані, перевернута семантика, завершення не фіксується |
| «Відсутнє: Парсинг .scr» | vault/01 | `ScrReader` є й використовується (`opening.scr`) |
| «Відсутнє: Система збережень» | vault/01 | Частково є (Task #8), але лише 3 поля |
| «Команда з 6 агентів», файли ba/reviewer/qa створені | vault/02, vault/05 | У `.claude/agents/` лише pm, tech-lead, developer |
| Task #6: «Blacksmith 3 пункти (не 4…)», Task #7: «Assign Items прибрано (не відповідає Java)» | vault/05 | `e.java` case 12 → `fX = uimenu[39]` = «Buy Item\|Sell Item\|Enchant Item\|Combine Items»; case 13 → `fY = uimenu[40]` = «…\|Assign Items». 3 пункти з `as.java` — мережевий маркет (Gamevil Live) |
| US-5.2 «Blacksmith — 4 пункти» проти US-6.1 «3 пункти»; US-6.2/7.2 «placeholder-екран» | GAME_MENU_STORIES | Сторі суперечать одна одній; у коді замість екранів модалка «Coming soon» |
| «Input handling ✅»; «Missing: Save/Load» | GAME_MENU_SPEC §6 | Ввід у підменю зламаний; Save/Load уже частково є |
| Пункт «To Game» в ігровому меню; «застосовується конфіг з SUBMENU_CONFIG» | TECHNICAL §3 | «To Game» немає (є ETC); конфіг застосовує `submenu_config.gd`, а `SUBMENU_CONFIG` лише фільтрує |
| «GENERAL_NAMES, GENERAL_RELATIONSHIP у generals_select_screen.gd» | TECHNICAL §5 | Таких констант немає, дані в `GameState` |
| «Ввід передається поточній сцені через process_menu_input()» | TECHNICAL §2 | Лише 5 скриптів мають цей метод, решта на `_input` |
| «BACK зазвичай не через окрему action» | TECHNICAL §9 | `ui_cancel` обробляють shell, карусель і story |
| Ігрове меню = Mission…Management + **To Game** (6), або «сім пунктів» | DESIGN §2.5, §5.2, §6.2, §10 | 6 пунктів з ETC; у грі можна потрапити тільки через Mission; DESIGN сам себе суперечить (6 чи 7) |
| «Continue → завантаження збереження» | DESIGN §5.1 | Continue одразу відкриває ігрове меню без load |
| New Game: Hero → Difficulty → Name… | DESIGN §2.5 | Код: Difficulty → Hero → Name |
| Підтвердити: Enter/KP_Enter/Space/Joy A; Назад: Esc/Backspace/Joy B; W/S | DESIGN §4.2 | Лише Up/Down/Enter (+ дефолтний `ui_cancel`) |
| Анімація каруселі ~0.14 с | DESIGN §6.2 | 0.22 с |
| Save/Load «не в головному меню» | DESIGN §6.6 | Save/Load саме в ETC головного меню. За Java ETC = «Options\|Help» (`uimenu[37]`), Save — у паузі (`uimenu[41]`) |
| Mission — сітка 4×2 | DESIGN §6.6 | Сітка існує, але мертва; реально використовується список |
| Help — багато тем; Endings — список, текст, катсцена; Visit dialog — текст | DESIGN §6.6.2/6.6.4/6.5 | Один рядок; 3 заглушки; статичний невірний текст |
| BACK = `softbg.png`, `ui_back.png` — лише фон | DESIGN §7 | `visiting_general_screen.tscn` BtnBack = `ui_back.png` |
| Підписи меню з `fV[]` (uimenu 30..35) | DESIGN §8 | `fV` — це текстове титульне меню; ігрове меню — `fU = uimenu[36]` |
| Шляхи `scenes/title_screen.tscn`, меню «Квест, Магазин, Кузнец, Склад, Обмен, В игру», «Стрелки ← →», `is_mobile()` | GODOT_README.md | Застаріло повністю: інші шляхи й пункти, ←/→ не працюють, функція зветься `is_mobile_device()`, пад не з'являється |
| `scenes/button_list_item.tscn`, `scenes/button_back.tscn` | BUTTON_TEMPLATE | Лежать у `scenes/buttons/`, биті й не використовуються |
| ETC = «Save User Data\|Load User Data» | JAVA_REFERENCE §7b | Це серверний save з `as.java bh()`; локальний ETC — `fW` = «Options\|Help» |

---

## Tech debt tasks

Оцінки — для одного розробника, знайомого з кодом.

**TD-1 (P0) — Один шлях вводу, неактивні шари не слухають.** ~5 год
- **Мета:** клавіатура й геймпад потрапляють лише у верхній активний екран.
- **Файли:** `main.gd`, `game_menu.gd`, `game_menu_vertical.gd`, `title_screen.gd`, `license/help/options/endings_screen.gd`, `submenu_shell.gd`.
- **Готово, коли:**
  - `process_menu_input` прибрано (або прибрано `Main._input`);
  - `MainLayer` отримує `process_mode=DISABLED`, поки відкрите підменю;
  - `flow_test.gd` у **обох** режимах (фокус і без фокуса) показує: DOWN/ENTER/ESC у списку місій, Visiting і Blacksmith не змінюють `carousel_idx`, ENTER у Visiting відкриває `VisitingGeneralScreen`, ESC закриває підменю, а не гру.

**TD-2 (P0) — Input Map за DESIGN §4.2.** ~2 год
- **Мета:** повні прив'язки, включно з джойпадом і горизонтальними діями.
- **Файли:** `project.godot`, `game_state.gd:299-320`, `title_menu_row.gd`, `hero_selection.gd`.
- **Готово, коли:**
  - додано `menu_left/menu_right` для титулу й героя;
  - `menu_confirm` = Enter, KP_Enter, Space, Joy A;
  - `menu_back` = Esc, Backspace, Joy B;
  - prev/next = Up, W, D-pad, вісь;
  - `_ensure_input_actions` або видалено, або лишає лише `move_*`;
  - дамп InputMap збігається з таблицею DESIGN;
  - в автотесті ←/→ на титулі змінюють пункт, `InputEventJoypadButton(A)` підтверджує.

**TD-3 (P0) — Шар даних з оригінальних файлів.** ~7 год
- **Мета:** прибрати всі плейсхолдери з §3.7.
- **Файли:** нові `scripts/data/arr_table.gd`, `campaign_loader.gd`, `game_data.gd` (autoload); `scr_reader.gd` (кеш, `get(i)`, fallback CP949); `game_state.gd`.
- **Готово, коли:** headless-тест друкує:
  - cq=0 → сторона «The Rise», 4 місії «Lord Gabriel…Lord Edison» зі спавном (4,2)…;
  - 141 генерал (`general.arr[4]` = «Reeve»);
  - предметів 100/137/18;
  - для кожного `.scr` кількість записів = лічильник у заголовку;
  - у `game_state.gd` немає захардкоджених імен.

**TD-4 (P0) — Правильна семантика флоу місій.** ~6 год
- **Мета:** Java-порядок «сторона (`dt`) → місії (`dA`) → бріфінг (`brief.scr`) → підтвердження → діалог → карта (map=`ds[dk]`, спавн з `sideinfo`)».
- **Файли:** `game_menu.gd`, `mission_list_screen.gd`, `mission_lord_select.gd`, `mission_briefing_screen.gd`, `lord_dialog_screen.gd`, `game_state.gd`.
- **Готово, коли:**
  - одне й те саме ім'я на всіх екранах (автотест);
  - `Z_RANGES` видалено;
  - доступність місій рахується з бітів `dy`;
  - `set_mission_completed` викликається з результату місії.

**TD-5 (P1) — Базова ігрова сцена.** ~8 год
- **Мета:** світ без багів, готовий для бою й ворогів.
- **Файли:** `game.tscn`, `game.gd`, заміна `map_renderer.gd` на `TileMapLayer` + `TileSet`, `player.tscn` (перенести в `scenes/game/`), `game_ui.tscn`, `virtual_pad.tscn/.gd`, новий `pause_menu.tscn` (`uimenu[41]`).
- **Готово, коли** автотест показує:
  - гравець +27 px → тайл −27 px;
  - стіна зупиняє гравця;
  - `BottomBar` rect = (0,259,240,61);
  - у TOUCH-режимі кнопки пада видимі;
  - ESC відкриває паузу, «Exit to Menu» повертає в GameMenu.

**TD-6 (P1) — Завантажувач реальних карт.** ~10 год (з дослідженням)
- **Мета:** читати `mdat_QVGA.scr` → `N.arr`/`*.MAP` у TileMapLayer, плюс комірки `eO[]` і сутності `ex[]`.
- **Файли:** `scripts/data/map_loader.gd`, `JAVA_REFERENCE.md` (задокументувати формат).
- **Готово, коли:** карта сторони «The Rise» рендериться з правильним розміром і тайлсетом, спавн на (4,2); є скріншот-порівняння з емулятором.

**TD-7 (P1) — Модель стану і повний save.** ~5 год
- **Мета:** `PlayerState`, `CampaignState`, `RelationsState` (Resource) і версіонований save.
- **Файли:** `scripts/state/*`, `game_state.gd`, `main.gd` (Continue), `title_menu_row.gd` (рядок 9 «Continue disabled»).
- **Готово, коли:**
  - round-trip save→load відновлює всі поля (тест);
  - Continue без сейву вимкнений, із сейвом викликає load;
  - збереження доступне з паузи, як у Java.

**TD-8 (P1) — Роутер екранів зі стеком.** ~5 год
- **Мета:** прибрати 15 `_show_*` і ручні `queue_free`-стеки.
- **Файли:** `main.gd`, `game_menu.gd`, усі екрани (уніфіковані сигнали `navigate/back`).
- **Готово, коли:**
  - `main.gd` < 80 рядків, без `has_signal`;
  - «Назад» з Name → Hero, зі Stats → Name;
  - у `game_menu.gd` немає циклів `for child in _submenu_layer…queue_free`;
  - flow-тест зелений.

**TD-9 (P2) — Видалити мертве, злити дублікати.** ~3 год
- **Мета:** менше коду і одне джерело правди.
- **Файли:** список з §1.3; `license/help/options/endings_screen.gd` об'єднати в `text_screen.tscn/.gd` (scenes-first: ScrollContainer + Label у сцені); видалити `SUBMENU_CONFIG`, `MENU_ITEMS`, `MENU_LABELS` (лейбли з `GameData`/`uimenu.scr`).
- **Готово, коли:** grep не знаходить посилань на видалене; `all_scenes.gd` показує 0 WARN/ERROR; 7 GDScript-попереджень виправлено.

**TD-10 (P2) — Меню за даними Java.** ~7 год (після переузгодження з PM)
- **Мета:** Blacksmith = 4 пункти (`fX`), Management = 5 (`fY`), ETC = Options/Help (`fW`), Help = 9 тем з `help.scr`, Endings = 4 з повідомленням про блокування, Options = Sound/Volume/Speed/Diff.
- **Файли:** `submenu_config.gd` (або дані), `help_screen`, `endings_screen`, `options_screen`; `docs/BLACKSMITH_SPEC.md` і `docs/GAME_MENU_STORIES.md` переписати.
- **Готово, коли:** пункти й тексти збігаються з `uimenu.scr`/`*.scr` (тест порівнює рядки).

**TD-11 (P2) — Visiting.** ~3 год
- **Мета:** робочий екран для тачу й клавіатури.
- **Файли:** `generals_select_screen.gd`, `generals_table.tscn`/`_row.tscn` (підключити `generals_table_row.gd`), `visiting_general_screen.tscn/.gd`.
- **Готово, коли:**
  - тап по рядку відкриває діалог;
  - шапка показує «Name / Friendship»;
  - діалог бере текст з `visit.scr` і показує «Friendship increased by 5» / «Friendship: 100%»;
  - BACK використовує `softbg.png`;
  - без запрошених генералів ENTER нічого не робить.

**TD-12 (P2) — Проєктні налаштування й експорт.** ~4 год
- **Мета:** білд для мобільних і чіткий піксель-арт.
- **Файли:** `project.godot`, `export_presets.cfg`, `sound_manager.gd`, сцени з рукописними UID.
- **Готово, коли:**
  - Nearest-фільтр і вирішене питання stretch (SubViewport прибраний або залишений без форвардингу);
  - рендерер `gl_compatibility`/`mobile`;
  - дані або сконвертовані в `.tres`, або є include-фільтр `*.scr,*.arr,*.MAP,*.bin`;
  - музика в `.ogg` (або обґрунтовано лишити MIDI з малим sf2);
  - null-guard у `SoundManager`;
  - сцени перезбережено в редакторі, `invalid UID` = 0;
  - експортований APK/desktop показує пролог (`opening.scr` читається).

**TD-13 (P2) — Інструменти й тести.** ~3 год
- **Мета:** автоперевірка замість ручного QA.
- **Файли:** `decode_scr.py` (лічильник із заголовка), регенерувати `*_strings.txt`; перенести `05_godot_audit_tools/*` у `tests/` проєкту; додати відсутні агенти або поправити vault.
- **Готово, коли:** `uimenu_strings.txt` має 60 рядків; одна команда (`tests/run.sh`) проходить import, компіляцію, сцени й флоу; Reviewer-хук або QA-агент викликає саме її.

**TD-14 (P3) — Синхронізувати документацію та мову UI.** ~2 год
- **Мета:** документи відповідають коду, рядки UI — англійські з оригіналу.
- **Файли:** `docs/DESIGN.md`, `docs/TECHNICAL.md`, `docs/history/vault/01`, `docs/history/vault/05`, `GODOT_README.md`, рядки RU/UK у `*.gd`.
- **Готово, коли:** усі рядки таблиці §6 закриті; у `scripts/` немає кириличних UI-рядків (лише коментарі).

**Разом:** близько 70 год. Мінімум перед геймплеєм (TD-1…TD-5, TD-7) — близько 33 год.
