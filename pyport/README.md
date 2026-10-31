# pyport — Path of a Warrior на Python (етап 0, пробний перенос)

Дослівний перенос J2ME-гри з декомпільованої Java (`../*.java`) на pygame-ce.
Ресурси читаються з кореня репозиторію (`config.RES_ROOT`), Godot-файли не використовуються.

## Запуск

```bash
pip install -r pyport/requirements.txt
python pyport/main.py                 # вікно 480×640
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
| `ag.java` (частина) | `pow/game/ag.py` | цикл `run`, `paint/P/L`, титул `S/E/T`, сейв `U`, фон меню `w/x`, софт-клавіші `h(int,int)` … |
| `af.java` | `pow/game/af.py` | лого → «sound enabled?» → титул |
| `e.java` (частина) | `pow/game/e.py` | Main Menu (`aJ`), карусель Game Menu (`bf`), клавіші `a/aB/aC/aD/aE/b/aF` |
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

## Headless-скріншоти

`tools/shot.py` запускає справжній цикл `ag.run` з `SDL_VIDEODRIVER=dummy` і віртуальним
годинником: час рухається лише через сон самого циклу (120 мс на тік у меню), тому кадри
відтворювані до пікселя. Сценарій — рядки `wait N`, `key NAME`, `click X Y`, `wheel up|down`, `rclick`, `shot NAME`, `save zero`.
`pyport/shots/` — поточні кадри порту (база для регресійного тесту `tests/test_screens.py`).
Скріншоти KEmulator покласти в `pyport/shots_ref/<сценарій>/` з тими самими іменами й
запустити `tools/compare_ref.py`.
