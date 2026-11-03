# Java → Python: імена

Порт починався дослівним (імена Java). Рефакторинг дає змістовні імена; ця таблиця зберігає зв'язок
з декомпільованою Java (гілка `java-reference`). Коментарі `# ag.java:FROM-TO` біля методів лишаються.

## Модулі одиночної гри (`pow/game`)

| Java | Python-модуль |
|---|---|
| `ag.java` | `pow/game/game_canvas.py` |
| поля `ag.java` | `pow/game/game_fields.py` |
| `ae.java` | `pow/game/consts.py` |
| `af.java` | `pow/game/boot.py` |
| `e.java` | `pow/game/menus.py` |
| `c.java` | `pow/game/map_scene.py` |
| `ar.java` | `pow/game/map_engine.py` |
| `as.java` | `pow/game/live.py` |
| `m.java` | `pow/game/live_screen.py` |
| `l.java` | `pow/game/popups.py` |
| `k.java` | `pow/game/sound.py` |
| `x.java` | `pow/game/gfx.py` |
| `g.java` | `pow/game/font.py` |
| `j.java` | `pow/game/res_reader.py` |
| `al.java` | `pow/game/scr_table.py` |
| `d.java` | `pow/game/arr_table.py` |
| `at.java` | `pow/game/name_buffer.py` |
| `aq.java` | `pow/game/player_pool.py` |
| `Main.java` | `pow/game/midlet.py` |
| `v.java` | `pow/game/live_net.py` |

## Класи

| Java | Python | Що це |
|---|---|---|
| `ag` | `GameCanvas` | головний Canvas: цикл гри, стан, спільні допоміжні методи; усі статичні поля |
| поля `ag` | `GameFields` | поля `ag.java` з початковими значеннями (база `GameCanvas`) |
| `af` | `Boot` | лого → «sound enabled?» → титул |
| `e` | `Menus` | екрани меню, створення героя, Blacksmith |
| `c` | `MapScene` | карта: завантаження, кімнати, герой, вороги, історія (пролог/епілог) |
| `ar` | `MapEngine` | тік карти й бій: ШІ ворогів, стріли, шкода, пауза-меню |
| `as` | `Live` | Gamevil Live: меню, ввід, запити |
| `m` | `LiveScreen` | Gamevil Live: малювання, реєстрація |
| `l` | `Popups` | попапи (Yes/No/Ok, підсумок місії) |
| `k` | `Sound` | менеджер звуку |
| `x` | `Gfx` | єдиний шлюз малювання |
| `g` | `Font` | бітмап-шрифт `0_font.png` |
| `j` | `ResReader` | читання ресурсів |
| `al` | `ScrTable` | таблиця рядків `.scr` |
| `d` | `ArrTable` | таблиця даних `.arr` |
| `at` | `NameBuffer` | буфер вводу імені героя |
| `aq` | `PlayerPool` | пул програвачів звуку (pygame.mixer) |
| `Main` | `Midlet` | MIDlet (`Main.java`) |
| `ab` | `LiveAnswer` | відповідь сервера Gamevil Live (`ab.java`) |
| `v` | `LiveNet` | мережа Gamevil Live (`v.java`) |
| `h` | `Point` | точка x, y |
| `ac` | `Rect` | прямокутник |
| `aa` | `MapMode` | режим карти (пауза-меню тощо) |
| `z` | `Item` | предмет (екземпляр: id, заточка) |
| `p` | `QuickSlot` | слот швидкого доступу (зілля / бомби): id і кількість |
| `ai` | `GearDef` | опис спорядження з `kibo.arr` (101-299) |
| `t` | `TreasureDef` | опис скарбу з `sungbo.arr` (301-499) |
| `ao` | `RareDef` | опис Rare-предмета з `shinki.arr` (501+) |
| `o` | `MapData` | дані карти (тайли, шари) |
| `aj` | `MapSize` | розміри карти |
| `ad` | `ActiveEffect` | предмет / ефект, що зараз діє на карті |
| `am` | `GeneralDef` | генерал з `general.arr` |
| `ak` | `InfoBox` | інфо-рамка з текстом |
| `w` | `FloatingText` | спливний текст над героєм |
| `an` | `Lord` | лорд: старт на карті, голова, генерал |
| `y` | `SpriteFrame` | шматок кадру спрайта (SP3) |
| `f` | `Arrow` | стріла лучника |
| `i` | `SpawnSpot` | вільна клітинка для появи ворога |
| `r` | `Breakable` | предмет на карті, що розбивається (бочка, ящик) |
| `a` | `Drop` | предмет, що випав на карті |
| `ah` | `ScriptSlot` | запис хеш-таблиці скриптів клітинок |
| `au` | `RoomCell` | комірка карти: слоти ворогів і параметри |
| `ap` | `Actor` | сутність на карті (ворог, герой, генерал) |
| `n` | `Hero` | герой: характеристики, інвентар, скіли |

Методи й поля поки мають Java-імена; їхні нові імена додаються сюди з наступними кроками.
