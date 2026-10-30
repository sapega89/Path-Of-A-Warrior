# Технічний документ — Path of a Warrior (Godot 4)

Порт J2ME-гри на Godot 4, цільова роздільність 240×320. Усі екрани та меню описані в сценах (.tscn), стилі — в темах/ресурсах (.tres).

**Джерело правди для дизайну:** зміни в поведінці екранів, потоках і правилах UI вносяться в **docs/DESIGN.md**. При розробці орієнтуватися спочатку на DESIGN.md, технічні деталі — тут.

---

## 1. Загальна структура проєкту

| Каталог / файл | Призначення |
|----------------|-------------|
| **scenes/** | Усі сцени: головне меню, підменю, екрани, кнопки, гра |
| **scenes/title/** | Титульний екран, пункти меню (New Game, Continue, ETC) |
| **scenes/game/** | Ігрове меню (game_menu), вертикальний список, сама гра (game.tscn) |
| **scenes/menus/** | Підменю: Mission, Blacksmith, Visiting, Management, ETC, difficulty, endings |
| **scenes/screens/** | Екрани контенту: License, Help, Options, Visiting General, таблиця генералів |
| **scenes/buttons/** | Кнопки списку, BACK |
| **scripts/** | Логіка до сцен (один .gd на сцену або спільні допоміжні) |
| **docs/** | Документація: шаблони кнопок, технічний опис |

**Принципи:**
- UI-структура визначається в .tscn (ноди, контейнери, інстанси).
- Візуальні стилі (кольори, рамки, шрифти) — у .tres або в коді через `add_theme_*_override`.
- Логіка навігації, вводу та даних — у прив’язаних .gd скриптах.

---

## 2. Основний потік (main.gd)

```
Title Screen → (New Game / Continue / ETC) → Game Menu → підменю або «To Game» → гра
```

- **main.tscn** — корінь; містить `GameContainer/SubViewport`, куди підставляються сцени.
- **main.gd** перемикає екрани: титул, ліцензія, допомога, опції, кінцівки, вибір героя, складність, ім’я, статистика, історія, **game_menu**, гра.
- Ввід (клавіатура/геймпад) передається поточній сцені через `process_menu_input()`.

---

## 3. Ігрове меню (game_menu)

**Сцена:** `scenes/game/game_menu.tscn`  
**Скрипт:** `scripts/game_menu.gd`

- Вертикальний список пунктів: Mission, Blacksmith, Gamevil Live, **Visiting**, Management, ETC, To Game.
- При виборі пункту з підменю відкривається відповідна сцена з `SUBMENU_SCENES` і застосовується конфіг з `SUBMENU_CONFIG` (title, links).
- Підменю мають спільний шаблон **SubmenuShell**: рамка, заголовок, контейнер посилань (LinksVBox), кнопка BACK.
- Сигнали: `enter_game`, `back_to_title`; для Visiting — `general_selected` підключається до екрану діалогу з генералом.

---

## 4. Шаблон підменю (SubmenuShell)

**Сцена:** `scenes/submenu_shell.tscn`  
**Скрипт:** `scripts/submenu_shell.gd`

- Один вигляд для всіх підменю: фон, тайтл-бокс, MenuFrame з бордерами, **LinksVBox** (контейнер для кнопок або іншого вмісту), BACK внизу справа.
- `set_menu(title, links)` — встановлює заголовок і список посилань; якщо `links` порожній, у LinksVBox можна класти власний вміст (наприклад, таблицю).
- `get_links_container()` — повертає `LinksVBox` для додавання дочірніх нод (таблиця генералів, текст тощо).
- Сигнали: `link_selected(action_id)`, `back_pressed`.
- Стилі кнопок списку та BACK описані в **docs/BUTTON_TEMPLATE.md**.

---

## 5. Visiting — екран вибору генерала

**Сцена:** `scenes/menus/visiting_menu.tscn`  
**Скрипт:** `scripts/generals_select_screen.gd`

- Пункт головного меню **Visiting** відкриває саме цю сцену (без окремого екрану «Select»).
- У сцені фізично: **SubmenuShell** + інстанс **GeneralsTable** у `SubmenuShell/MainLayer/MenuFrame/LinksVBox`.
- Таблиця — заголовок (HeaderRow) + рядки (Row0..RowN). Кількість рядків (наприклад, 37) і дані задаються в `generals_select_screen.gd` (GENERAL_NAMES, GENERAL_RELATIONSHIP).
- Навігація: стрілки вгору/вниз, Enter — вибір генерала (сигнал `general_selected`), BACK — закриття підменю.
- Після вибору генерала game_menu відкриває **visiting_general_screen** (діалог з генералом).

---

## 6. Таблиця генералів (дві колонки з бордерами)

**Сцени:**
- **generals_table.tscn** — VBoxContainer: HeaderRow + Row0..Row5 (шаблон; скрипт може дублювати рядки й очищати зайві).
- **generals_table_row.tscn** — один рядок: HBoxContainer з двома **ячейками з окремими бордерами**:
  - **NameCell** (PanelContainer + StyleBoxFlat): кнопка з ім’ям (і опційно іконка jang_1..37).
  - **RelCell** (PanelContainer + StyleBoxFlat): лейбл «Рівень відносин» (число, вирівнювання по правому краю).

**Скрипти:**
- **generals_select_screen.gd** — прив’язаний до кореня visiting_menu: заповнює таблицю, керує виділенням, вводом, емітить `general_selected` і `closed`.
- **generals_table_row.gd** (якщо є) — логіка одного рядка (set_data, set_selected тощо); екран може звертатися до рядків через ноди `NameCell/Button`, `RelCell/RelationshipLabel`.

Прокрутка: якщо потрібно, ScrollContainer створюється або є в сцені навколо GeneralsTable; у скрипті використовується `ensure_control_visible(row)` для вибраного рядка.

---

## 7. Інші екрани та підменю

- **submenu_config.gd** — конфіг для підменю за `menu_id`: title і links з масиву CONFIGS; використовується в меню з окремим вузлом Config.
- **submenu_shell** — єдиний шаблон: і для підменю з посиланнями (Blacksmith, Management), і для екранів з контентом (License, Help, Options, Endings). Режим посилань: `set_menu(title, links)`; режим контенту: `set_menu(title, [])`, потім `get_content()` або `set_content_message()`.
- **visiting_general_screen** — діалог з обраним генералом (текст, можливо портрет).

---

## 8. Ключові шляхи до сцен і скриптів

| Що | Шлях |
|----|------|
| Головне меню гри | scenes/game/game_menu.tscn, scripts/game_menu.gd |
| Visiting (таблиця генералів) | scenes/menus/visiting_menu.tscn, scripts/generals_select_screen.gd |
| Шаблон підменю | scenes/submenu_shell.tscn, scripts/submenu_shell.gd |
| Рядок таблиці (2 ячейки з бордерами) | scenes/screens/generals_table_row.tscn |
| Таблиця (заголовок + рядки) | scenes/screens/generals_table.tscn |
| Діалог з генералом | scenes/screens/visiting_general_screen.tscn |
| Стилі кнопок | docs/BUTTON_TEMPLATE.md, theme_list_button*.tres, submenu_shell.gd |

---

## 9. Вхідні дії (input actions)

- Меню: `menu_confirm` (Enter/прийняти), `menu_prev` / `menu_next` або `ui_up` / `ui_down` для навігації.
- BACK зазвичай через сигнал кнопки підменю, не через окрему action.

---

Цей документ описує архітектуру та потіки; деталі кнопок і стилів — у **BUTTON_TEMPLATE.md**.
