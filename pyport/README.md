# pyport — Path of a Warrior на Python (етап 0, пробний перенос)

Дослівний перенос J2ME-гри з декомпільованої Java (`../*.java`) на pygame-ce.
Ресурси читаються з кореня репозиторію (`config.RES_ROOT`), Godot-файли не використовуються.

## Запуск

```bash
pip install -r pyport/requirements.txt
python pyport/main.py                 # вікно 480×640; New Game -> створення героя -> пролог -> Game Menu
python pyport/main.py --demo          # одразу покласти демо-сейв «HERO», якщо сейву ще немає
POW_SCALE=3 python pyport/main.py     # 720×960
python -m pytest -q pyport/tests      # тести (headless)
python pyport/tools/shot.py pyport/tools/scenarios/title.keys      # скріншоти -> pyport/shots/title/
python pyport/tools/sheet.py pyport/shots/title sheet.png          # усі кадри на одній картинці
```

**Клавіатура** (ПК → телефон, `PHASE_1_FOUNDATION.md` §5): стрілки/WASD, Enter/Space/J = OK,
Esc/Backspace = права софт-клавіша (BACK), Q/F1 = ліва, цифри 0–9; цифровий блок працює як
клавіатура телефону (8/2/4/6 = стрілки, 5 = OK).

**Мишка** (`pow/game/pointer.py`, клік перекладається в натискання клавіш телефону):
- титул, попап Ok — клік будь-де;
- попап Yes/No — клік лівіше центру = Yes, правіше = No (вибирає і підтверджує);
- Main Menu — стрілка ◄ / ►, клік по назві пункту = OK; колесо гортає пункти;
- Game Menu — верхня мала кнопка = вгору, велика = OK, нижня = вниз; колесо крутить карусель;
- складність — клік по Hard / Normal; герой — клік по лівій/правій голові крутить, по середній = OK;
- ім'я — клік по букві чи OK у сітці (курсор сам доходить туди стрілками і натискає OK), DEL = BACK;
- очки характеристик — клік по рядку HP / MP / ATK / DEF додає очко саме туди;
- пролог — клік = OK (увесь текст одразу), «SKIP» унизу ліворуч або Q/F1 = пропустити;
- BACK — права кнопка миші або клік по «BACK» внизу праворуч.

### Браузер (pygbag)

```bash
python pyport/tools/build_web.py --no-pygbag   # збирає pyport/build/web-src (код + ресурси, ~3.4 МБ)
python -m pygbag pyport/build/web-src           # http://localhost:8000
```

pygbag під час збирання і в браузері завантажує рантайм з `pygame-web.github.io`.
У консолі браузера (F12) має бути рядок `RMS selftest: launch #N … OK (emscripten)`;
після перезавантаження сторінки N має зрости на 1 — це перевірка збереження в `localStorage`.

## Що вже перенесено

| Java | Python | Що |
|---|---|---|
| `x.java` | `pow/game/x.py` | уся графіка гри: clip, drawImage, fillRect/drawRect/drawLine, текст, CRC |
| `g.java` | `pow/game/g.py` | бітмап-шрифт: заміна кольору палітри PNG + перерахунок CRC |
| `j.java`, `al.java` | `pow/game/j.py`, `al.py` | читання ресурсів і `.scr` |
| `ae.java` | `pow/game/ae.py` | **згенеровано** `tools/gen_ae.py` |
| поля `ag.java`, дрібні класи-структури | `pow/game/_ag_fields.py`, `structs.py` | **згенеровано** `tools/gen_fields.py` |
| `ag.java` (частина) | `pow/game/ag.py` | цикл `run`, `paint/P/L`, титул `S/E/T`, читання сейву `U` і запис `ar`, фон меню `w/x`, софт-клавіші `h(int,int)`, новий герой `au/av/aw/ax/ay/k(int,int)`, сітка імені `r/f(int,int)` … |
| `d.java`, `at.java` | `pow/game/d.py`, `at.py` | таблиці `.arr` (kibo/sungbo/shinki) і буфер імені |
| `c.java` (лише `c(int)`) | `pow/game/c.py` | сторінка прологу/епілогу; плеєр історії `ag.l(int,int)/L/M/N`, текст у рамках `e.a(int,int,int)/b(int)/R` |
| `af.java` | `pow/game/af.py` | лого → «sound enabled?» → титул |
| `e.java` (частина) | `pow/game/e.py` | Main Menu (`aJ`), карусель Game Menu (`bf`), клавіші `a/aB/aC/aD/aE/b/aF`; створення героя: складність `aU`, герой `aK`, ім'я `aL/aM`, очки `O/T`, предмети `e(int)`, `p()` |
| `l.java` (частина) | `pow/game/l.py` | попапи: рамка, кнопки Yes/No/Ok, усі текстові `e(int)`, клавіші й таймер |
| `k.java` | `pow/game/k.py` | менеджер звуку (дослівно) |
| `aq.java` | `pow/game/aq.py` | **спрощено** на pygame.mixer (дослівно — таск 1.5) |
| `Main.java` | `pow/game/Main.py` | MIDlet; `com/movaya` не переноситься |
| J2ME API | `pow/midp/*` | `Image/Graphics`, `Canvas`, `RecordStore` (файли / localStorage), `java.util.Random`, семантика int |

Екрани наступних етапів кидають `NotPorted`. У звичайному режимі гра показує попап
«Not ported yet» і повертається в меню; `POW_STRICT=1` — падати.

## Правила переносу (коротко; повні — етап 1, таск 1.11)

1. **Імена.** Метод Java зберігає ім'я, якщо воно в класі (разом з `ag` і всіма його
   підкласами) одне й не збігається з полем. Інакше — суфікс сигнатури:
   `I` int, `H` short, `B` byte, `C` char, `J` long, `Z` boolean, `T` String, `M` Image,
   `G` Graphics, `A…` масив, `L<клас>` об'єкт, `v` без параметрів.
   Приклади: `x.a(Image,int,int)` → `x.a_MII`, `ag.T()` → `ag.T_v`, `ag.a_(int)` → `ag.a__I`.
   Таблиця всіх імен — `tools/java_names.txt` (генерує `tools/java_names.py`).
   Ключові слова Python отримують `_` в кінці: `as` → `as_`.
2. **Статичні поля** читаються й пишуться лише як `ag.X` (ніколи `self.X`, бо присвоєння
   через `self` створить поле екземпляра).
3. Кожен метод має коментар `# file.java:FROM-TO`.
4. Семантика Java: `pow/midp/jint.py` (`i8/i16/i32`, `idiv/imod`, `ushr32`). `//` замість `/`
   лише там, де обидва операнди ≥ 0 (так і позначено).
5. `# DECOMP-FIX Fn` — свідоме виправлення артефакту декомпілятора, прапорець у `config.DECOMP_FIX`.

### DECOMP-FIX, використані в етапі 0

| ID | Де | Що |
|---|---|---|
| F6 | `e.java` навігація меню, `bf` | `cM[1]=cM[1]+1; if (cM[1]+1 >= cN)` → `if (++cM[1] >= cN)`; без цього Main Menu перескакує пункти |
| F8 | `ag.L()` 1526-1546 | `switch` без `break`. Падіння крізь гілки є не лише в 3/4/5, а й у **0 і 2**: інакше на лого виконався б `bb.a(1)` і впав на `ct[7] == null` |
| F9 (новий) | `l.a(String)` 469-496 | `s = s + 1; l[s] = …` → `l[s++] = …`; буквально рядок 0 лишається старим, а останній не малюється |
| F10 (новий) | `ag.f(int,int)` 1794-1819, сітка імені | `10 * p % 14`, `17 * b / 14` → `10 * (p % 14)`, `17 * (b / 14)`; буквально курсор стрибає хаотично, а букви йдуть «драбинкою» |
| F11 (новий) | `e.T(int)` 3533-3545, курсор очок | декомпільований код передає `boolean` у колір: курсор малюється кольором 0x010101 і після першого ↑/↓ зникає; з F11 він білий, як у `e.O(1)`. **Перевірити в KEmulator** |

Створення героя (`e.java` / `ag.java` / `l.java`): Main Menu → New Game (якщо сейв є — попап 3
«saved game will be deleted») → складність (екран 29, попап 36) → герой (екран 6) → ім'я
(екран 7) → 5 очок характеристик (екран 8, попап 4) → `ax/ay/ar` записують сейв → Game Menu.
Далі `ag.l(100, 0)` запускає пролог (bV = 10): дві сторінки-картинки з текстом, що
пливе вгору, і діалоги «[Master] …» / «[ім'я героя] …» з друком по букві; кінець або SKIP → Game Menu.
На картинці SKIP гортає лише одну сторінку, на діалозі — завершує пролог (так у Java, `ag.M()`). Порядок рядків «a character for battle. /
Please select» на екрані 6 — дослівно з Java (`de - 90 - b*20`), теж варто звірити з KEmulator.

## Headless-скріншоти

`tools/shot.py` запускає справжній цикл `ag.run` з `SDL_VIDEODRIVER=dummy` і віртуальним
годинником: час рухається лише через сон самого циклу (120 мс на тік у меню), тому кадри
відтворювані до пікселя. Сценарії: `title`, `gamemenu`, `mouse`, `newgame` (створення героя клавішами, з видаленням
букви і Continue після сейву), `newgame_mouse` (те саме лише мишкою).
Сценарій — рядки `wait N`, `key NAME`, `click X Y`, `wheel up|down`, `rclick`, `shot NAME`, `save zero`.
`pyport/shots/` — поточні кадри порту (база для регресійного тесту `tests/test_screens.py`).
Скріншоти KEmulator покласти в `pyport/shots_ref/<сценарій>/` з тими самими іменами й
запустити `tools/compare_ref.py`.
