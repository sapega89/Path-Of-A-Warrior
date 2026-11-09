# 03 — Предмети, економіка, менеджмент персонажа, Gamevil Live

> **Примітка (30.10.2026).** Звіт писався, коли ціллю був Godot.
> - Технічна частина (формати, формули, посилання на рядки Java) чинна.
> - Розділ «План порту на Godot» у кінці застарів. Актуальний план — `docs/history/ROADMAP.md` і `docs/history/plans/`.
> - Розбір робився на копії без PNG, тому звіт пише «PNG немає». У вашій папці вони є.
> - Виправлення до старих документів — `ERRATA.md`.

Аналіз декомпільованого J2ME «Path of a Warrior» (240×320, Gamevil, MIDlet 1.4.0, BUILD_ID `POW_CIN_NK_N75`) для порту на Godot 4.5.
Джерела: `/home/claude/pow/*.java`, бінарні дані `*.arr / *.bin / *.scr`, поточний порт `/home/claude/pow/scripts/*.gd`.
Усі номери рядків прочитані мною в цій копії. Припущення позначено **[guess]** / **[medium]**.

---

## 0. Головне (виправлення поточних уявлень)

| Що вважалося | Що насправді в Java | Доказ |
|---|---|---|
| Blacksmith = «Buy Item / Sell Item / Cancel Sell» | Локальний Blacksmith = **Buy Item / Sell Item / Enchant Item / Combine Items** (екрани `cM[0]` = 21/22/23/24) | `uimenu.scr[39]` → `ag.fX` (ag.java 2339), `ae.aW[12] = {21,22,23,24…}` (ae.java 259), e.java 744-746, 2709-2710 |
| «Buy Item\|Sell Item\|Cancel Sell» | Це підменю **GAMEVIL LIVE → Trade** (онлайн-аукціон між гравцями) | `as.bf()` 2083-2093, `hn = hl[3]` = gamestr[5] «Trade» |
| Management = «Trade\|Warehouse\|Safe\|Management» | Це **кореневе меню GAMEVIL LIVE** (`hn = hl[2]` = «GAMEVIL LIVE») | `as.aH()` 1157-1176 |
| — | Ігровий Management = **Attributes / Skills / Gear / Inventory / Assign Items** (`cM[0]` = 14..18) | `uimenu.scr[40]` → `ag.fY` (ag.java 2340), `ae.aW[13]`, e.java 747-748 |
| ETC = Save / Load | Ігровий ETC = **Options / Help** (`uimenu.scr[37]` → `ag.fW`). Ручного Save/Load в ігровому меню немає, гра **автозберігається** (`ag.ar()`). «Save User Data / Load User Data» — це GAMEVIL LIVE → Management (серверний бекап) | ag.java 2337, e.java 741-743, `as.bh()` 2137-2143 |
| «Normal Items\|Special Items\|Rare Items» — категорії кузні | Це категорії **GL Trade → Buy Item** (`as.hw`, `as.aZ()`) | as.java 170, 1814-1824 |
| `as.java` — модуль сейву | `as.java` — **мережевий модуль** (Gamevil Live). Сейв — `ag.ar()` / `ag.U()` | ag.java 2126-2214, 2871-2961 |
| Мережа через HttpConnection | **Сирий TCP-сокет** `socket://GAMEVIL_SERVER:28230`, власний бінарний LE-протокол. HTTP — лише `platformRequest` (браузер) для More Games / Multiplayer | v.java 57-70, ag.java 604-621, l.java 120-134 |
| `uimenu_strings.txt`, `gamestr_strings_full.txt` повні | **Обрізані**: uimenu має 60 рядків (у txt 28), gamestr — 71 (у txt 67). `decode_scr.py` зупиняється на першому порожньому рядку | заголовок `.scr` = u16 count; §2.6 |
| Gift = подарунок генералу | Gift = подарунок **іншому гравцю** через GL (gift tax). У цьому білді **відправку подарунків не реалізовано**, є лише прийом Gift List | gamestr 9, 45, 47, 52, 53; в as.java немає жодного використання `hl[7]` / `cS.d(37/38)` |

**com/movaya (DRM):** `Main extends com.movaya.M123456`, `startApp()` → `tryNBuy_123456()` → `startApp_123456()` (Main.java 1-48). Це обгортка «try & buy» на старті MIDlet. Класів `com/movaya` у копії немає, на геймплей вона не впливає.

Окремо є прапорець `GAMEVIL_CHEAT` (`ag.bi`, ag.java 625-631). Він дає: 555000 золота при завантаженні (2179-2180), усі скіли (3260-3263), стати 2000 (916-926). У JAD він вимкнений (`NO`).

---

## 1. Опис для гравця

### 1.1 Золото (`cz.E`)
Звідки береться:
1. **Дроп** — мішечок `ct[32]` = `gold.png` (imgui[37]): **20** золота (Normal) / **40** (Hard). Кодується як предмет з id `10000+сума` (ar.java 2076; зарахування в `ag.k()` 3356-3357).
2. **Нагорода за місію:** `dz.h × 150 × (Hard ? 2 : 1)` (c.java 1603; також показується в діалозі місії, l.java 667). `dz.h` — байт 7 запису `sideinfo.arr`. Значення 3..15, тобто 450..2250 золота на Normal.
3. **Продаж у Blacksmith** — ½ ціни (e.java 2903).
4. **GL**: переказ із Safe; виручка від аукціону (надходить у Safe на сервері).

Куди витрачається: купівля (Blacksmith, GL), плата за Enchant і Combine, податки GL.
Показ: рамка з іконкою `ct[32]` і числом (`ag.J()` 1278-1291, `ag.i()` 1270-1272). Нова гра починається з **0 золота** (ag.java 3242).

### 1.2 Категорії предметів
| id | Категорія | Дані | Як отримати |
|---|---|---|---|
| 1–11 | **Consumables** (`tool.png`) | захардкоджено в `ae.java` (aN, aO, aP, y) | магазин (1–6, 10, 11), дроп (1–11), Visiting |
| 101–200 | **Normal** (`kibo.arr`), 20 видів × 5 тірів | `ag.bH[0]` | Blacksmith (випадковий асортимент), дроп, нагорода місії/візиту |
| 301–437 | **Special** (`sungbo.arr`), 137 шт. | `ag.bH[1]` | **лише** Combine або GL |
| 501–518 | **Rare** (`shinki.arr`), 18 шт. | `ag.bH[2]` | Combine, GL; 502 — сюжетна нагорода |
| ≥10000 | золото (сума = id−10000) | — | дроп |

Предмети з особливою логікою (ag.java 1383-1399, e.java 953-981, 3143-3154):
- **434 Rise Potion / 435 Azure Potion / 436 Falls Medicine / 437 Forest Medicine** — використовуються в Inventory і назавжди дають HP+5 / MP+3 / DEF+1 / ATK+1. Не виставляються на GL (as.java 1414-1416).
- **502 Silk Towel** («Catherine's scarf») видається за кінцівку №2 (c.java 1569-1570). Кінцівка №3 зараховується лише якщо 502 лежить у рюкзаку (c.java 1544-1545). Не вдягається. Інгредієнт у 55 рецептах. Назви кінцівок за text.scr[38+i] — **[medium]**.
- **504 Emperor's Seal** («all General Visiting») відкриває у Visiting усіх 44 генералів (e.java 798-801). **Локально ніде не видається**, тож доступний лише через GL. Інгредієнт у 62 рецептах із 149.

### 1.3 Інвентар
- **Рюкзак** `cz.Y[25]`: записи `z` = {id, ATK, DEF, HP, MP, enchant}. Ущільнюється функцією `ag.ag()` (2372-2383).
- **Пояс** `cz.Z[5]`: consumables `{id, count ≤ 5}` (ag.java 3286-3308, e.java 2842-2860).
- **Екіпіровка** `cz.X[9]` — див. 1.4.
- **Швидкі слоти** `cz.aa[2]`: індекси слотів пояса на клавішах `*` (42) і `#` (35) (c.java 1701-1718).
- **На сервері (GL):** Warehouse `as.gw[100]`, Safe `as.gy` (золото).
- **Повний рюкзак:** дроп не підбирається (`k()` повертає 0). Магазин пише «Your backpack is full…» (fK[20]=6); для стека з 5 штук — «You cannot buy anymore.» (fK[20]=5).

### 1.4 Слоти екіпіровки (`ae.aE = {0,0,3,5,2,8,6,1,4,7}`, ae.java 209; e.java 979; позиції — `e.n()` 1632-1654)
| Слот | Тип(и) | Позиція (dx,dy) |
|---|---|---|
| 0 | 0 Weapon-long (Blade/Pike/Spear, спрайт `wep_long`), 1 Weapon-short (Sword/Claymore/Axe, `wep_short`) | (−77,+21) |
| 1 | 7 Armlet | (−77,−15) |
| 2 | 4 Gauntlets | (−77,−51) |
| 3 | 2 Helmet/Crown | (−33,−79) |
| 4 | 8 Amulet | (+3,−79) |
| 5 | 3 Armour | (+47,−51) |
| 6 | 6 Belt | (+47,−15) |
| 7 | 9 Special: луки, коні, сувої, артефакти типу 9 | (+47,+21) |
| 8 | 5 Boots | (−15,+49) |

Тип предмета в слоті 0 задає `cz.K` (0 long / 1 short) і спрайт `ct[40+K]` (ag.java 873, 949).

### 1.5 Blacksmith (локальний)
Чотири екрани (`fT[21..24]`) мають одну сітку: 5 колонок × N рядків, 3 рядки видно, плюс скролбар і бігучий рядок опису (`e.aZ()` 2709-2754, `ag.b(...)` 1293-1352, `e.a(z,…)` 3083-3206).
- **Buy Item** (`fK[0]=0`):
  - `ag.fL[25]` = 8 consumables (1,2,3,4,5,6,10,11, **безлімітні**) + 17 випадкових Normal, відсортованих за id.
  - Куплена Normal-клітинка порожніє.
  - Асортимент оновлюється **після кожної місії** (c.java 1604) і на новій грі (l.java 140-141), зберігається в сейві.
  - OK купує одразу, без підтвердження → «You bought 1 X.».
- **Sell Item** (`fK[0]=1`):
  - Сітка 6×5: перший рядок — пояс, далі 25 клітинок рюкзака.
  - OK продає 1 шт. за ½ ціни → «You sold X.». Обмежень немає (502 продається за 0).
- **Enchant Item** (`fK[0]=2`):
  - Діалог «Price is N. If enchanting fails, Items can be lost. Continue?» → іскра `itemReinforce.png` (5 кадрів) → «Enchant Success/Fail».
  - Rare і consumables не заточуються («Not possible to enchant.»); на максимумі — «Fully enchanted.».
- **Combine Items** (`fK[0]=3`):
  - Потрібно ≥3 предметів у рюкзаку (l.java 843-849); обрати 3 (не consumables).
  - Якщо рецепт є: «Compounding fee is N. Selected items could be lost when it fails. Continue?» → «Compounding Success/Fail».
  - Якщо рецепта немає: «Not possible.».

### 1.6 Management (ігровий)
- **Attributes** (`cM[0]=14`; той самий рендер, що й `cM[0]=8` при створенні персонажа):
  - Рядки **HP / MP / ATK / DEF**, кожен із базою та «+бонусом» від екіпіровки; також ім'я, рівень, Fame, портрет `ju_N`, лічильник очок.
  - 1 очко дає HP+5 / MP+3 / ATK+1 / DEF+1 (e.java 882-907, 1429-1469).
- **Skills** (`cM[0]=15`):
  - 5 гарячих клавіш **1,3,7,9,0** (`cz.V[0..4]`); 7 груп (MOVE/HEAL/PASV/FWD/NEAR/RANGE/WHOLE, uimenu 48..54), до 3 скілів у групі (`ae.aC`). Призначити можна лише вивчений.
  - Рівні скілів (до 10) дає **лише Visiting** (e.java 3217-3230). MP-вартість — `ar.e()` 743-756.
- **Gear** (`cM[0]=16`): лялька з 9 слотами. OK на слоті відкриває Inventory для вибору; зайнятий слот знімається у вільну клітинку рюкзака (e.java 758-764).
- **Inventory** (`cM[0]=17`): сітка 5×5.
  - OK перевіряє рівень (`m(id) ≤ cz.l`, інакше «You can't take this equipment.»).
  - Еліксири 434–437 застосовуються; 502/504 не вдягаються.
  - Решта міняється місцями зі слотом `ae.aE[type]` (e.java 949-987).
- **Assign Items** (`cM[0]=18`): 5 слотів пояса з позначками `*`/`#` (e.java 3022-3058, `ar.c()` 249-260).
- Вихід із будь-якого екрана 14–18 викликає **автосейв** (e.java 1004-1012).

### 1.7 Рівень і очки
- **Досвід:** таблиця `exp.arr` (§2.5), кап рівня 200. Кожен рівень дає **+3 очки** (e.java 2963-2964; `ag.H()` 3094-3095).
- **Старт** (ag.java 3221-3273, `aw()` 3275-3284):
  - Lv1; ATK 5, DEF 4, HP 30, MP 10; **5 очок**; 0 золота.
  - Скіли `W[0]=W[5]=1` на клавішах (`V[0]=12`, `V[1]=17`).
  - Екіпірований **116 Iron Claymore**.
- **Підтвердження розподілу:** «Character settings are complete. Continue?» (l.java 653-656). **No** викликає `ag.aw()` і скидає стати для перерозподілу (l.java 193-200).
- **Провал місії при Lv>9:** шанс `Lv/4 %` втратити випадковий екіпірований предмет («Lost!!», l.java 744-760).

### 1.8 Gamevil Live (для гравця)
Ігрове меню → «Gamevil Live» (e.java 815-821 → `as.g()`).
1. Питання «Connect to Gamevil Live?» (gamestr 17).
   - Перший вхід: реєстрація UserID (4–12 літер, сітка A–Z) і пароля (4–12 цифр) (`as.h()` 192-208, `as.Q()` 1271-1328, `m.bp()` 157-208).
2. Після логіну йде автоматичний ланцюжок (§5.3):
   - оголошення сервера;
   - «Sale List» — ваші продані лоти;
   - «Gift List» — отримані подарунки;
   - застосування Exp/Fame, збережених на сервері;
   - вивантаження рюкзака і золота;
   - отримання вмісту Warehouse і балансу Safe.
3. Меню **GAMEVIL LIVE: Trade | Warehouse | Safe | Management**.
   - **Trade → Buy Item / Sell Item / Cancel Sell.**
     - Buy: категорія (Normal/Special/Rare) → вид (13/13/18) → рівень заточки 0–9 з кількістю лотів (для Rare цей крок пропускається) → сторінка лотів → «Buy for N Gold?». Предмет іде в рюкзак, а якщо той повний — у склад.
     - Sell: джерело (Backpack або Warehouse) → предмет → ціна (до 9 цифр, «ht[4]% of total will go to taxes»). Клавіша −6 відкриває Price Info. Максимум 5 лотів; виручка йде в Safe.
     - Cancel: список своїх лотів.
   - **Warehouse:** переміщення предметів рюкзак (25) ↔ склад (100).
   - **Safe:** переказ золота між локальним гаманцем і сервером.
   - **Management → Save User Data / Load User Data:** бекап прогресу **без предметів і золота** (gamestr 31, 32). Перед Load треба зняти екіпіровку (gamestr 48).

---

## 2. Формати даних (перевірено Python)

### 2.1 Формат `d.java` (7-48)
```
[u8 N] [N × u8 width] [rows…], рядок = sum(widths) байт
int-колонка = unsigned LE на width байт (d.a(row,col)); str = байти + trim() (d.b)
```
`e.e(int)` (e.java 3465-3531) читає ті самі файли напряму із захардкодженими зсувами: заголовок 9/10/9 байт, рядок 23/24/27 байт. Таблиці завантажує `ag.az()` (3400-3412) з edat 47 (kibo), 51 (sungbo), 49 (shinki).

### 2.2 Колонки
**kibo.arr:** 8 колонок, widths `[15,1,1,1,1,1,2,1]`, рядок 23 Б, 100 рядків → id 101–200.

| col | Значення | Хто читає |
|---|---|---|
| 0 | name | `e.c()` 2779 |
| 1 | type 0..8 | `cX.b`, `ag.g()` 867-870 |
| 2 | statType (0 ATK, 1 DEF, 2 HP, 3 MP) | `J()` 3432-3440, `k()` 3332-3345 |
| 3 | base | `cX.d` |
| 4 | spread | `cX.e` |
| 5 | **maxEnchant** (5..9) | `be()` e.java 2917 |
| 6 | **basePrice** (u16) | `b(z)` e.java 2822 |
| 7 | кадр іконки в `kibo.png` (28 px) = «kind» на GL | e.java 1894, as.java 1429 |

reqLevel у файлі немає; він береться за тіром `(id−101)%5` з `ae.w={1,10,25,45,70}` (e.java 3124; `ag.m()` 1413 дає те саме через `ae.aM`).

**sungbo.arr:** 9 колонок, widths `[15,1,2,1,1,1,1,1,1]`, рядок 24 Б, 137 рядків → id 301–437.

| col | Значення | Хто читає |
|---|---|---|
| 0 | name | |
| 1 | type | `cY.b` |
| 2 | ATK (u16) | `J()` 3442-3447 |
| 3 | DEF | |
| 4 | HP | |
| 5 | MP | |
| 6 | **maxEnchant** (0 = не заточується) **і** множник ціни (0 → 800, інакше 400) | `be()` 2919, `b(z)` 2824 |
| 7 | іконка/kind (0..16) | e.java 1891, as.java 1426 |
| 8 | **reqLevel** | `cY.h`, `ag.m()` 1409, e.java 3127, `aX()` 2605 |

**shinki.arr:** 8 колонок, widths `[15,1,2,1,2,1,4,1]`, рядок 27 Б, 18 рядків → id 501–518.

| col | Значення | Хто читає |
|---|---|---|
| 0 | name | |
| 1 | type | |
| 2 | ATK (u16) | |
| 3 | DEF | |
| 4 | HP (u16) | |
| 5 | MP | |
| 6 | **price** (u32) | `b(z)` 2827 |
| 7 | **reqLevel** | `ag.m()` 1405, e.java 3130, `aX()` 2608 |

Іконка Rare = кадр `id−501` у `shinki.png` (e.java 1887-1888).

### 2.3 Consumables (ae.java 20-22, 230-236; ефект — c.java 2544-2581)
| id | Назва | Ефект | Ціна | Продаж | У магазині |
|---|---|---|---|---|---|
| 1 | Red Potion (S) | HP +30% max | 60 | 30 | так |
| 2 | Red Potion (M) | HP +60% | 100 | 50 | так |
| 3 | Red Potion (L) | HP +100% | 150 | 75 | так |
| 4 | Blue Potion(S) | MP +30% | 60 | 30 | так |
| 5 | Blue Potion(M) | MP +60% | 100 | 50 | так |
| 6 | Blue Potion(L) | MP +100% | 150 | 75 | так |
| 7 | H.M.Potion(S) | HP&MP +30% | 100 | 50 | ні |
| 8 | H.M.Potion(M) | HP&MP +60% | 250 | 125 | ні |
| 9 | H.M.Potion(M) [так в оригіналі; насправді L] | HP&MP +100% | 400 | 200 | ні |
| 10 | Powerful Bomb | метання, «Ranged ATK» (text.scr 33) | 150 | 75 | так |
| 11 | Handy Dynamite | «Ranged ATK & Knocks back» (text.scr 34) | 200 | 100 | так |

Лікування = `y|z × % / 100`, потім кап до максимуму (`ar.b()` 262-267).

### 2.4 `item-mixing-table.bin` (1192 Б)
```
596 × u16 LE, колонково по 149:
 [0..148] in1 (найменший id)   [149..297] in2   [298..446] in3   [447..595] result
```
Перевірено:
- рядки відсортовані за (in1,in2,in3), у кожному in1≤in2≤in3;
- 14 трійок мають 2–3 рядки — тоді результат випадковий;
- 149 різних результатів (id 301–518).

Пошук — `e.aX()` 2568-2626:
1. Три обрані id сортуються.
2. Діапазон звужується тричі через `e.b(col,id,start,count)` (2674-2692).
3. `S(n)` читає u16 LE (2670-2672); рядок обирається як `start+C(count)`.

Статистика:
- 504 потрібен у 62 рецептах, 502 — у 55, обидва — у 45;
- 68 рецептів лише з Normal-інгредієнтів;
- 16 рецептів дають Rare.

### 2.5 `exp.arr` (798 Б)
- Формат: u16 `0x0401` (значення невідоме) + **199 × u32 LE** = досвід, потрібний для переходу з рівня L на L+1.
- `e.p()` (3547-3560) бере вікно з 10 значень; кап рівня 200.
- Значення: 50, 104, 165, 236, 320, 420, 539, 680, 846, 1040 …; L51 = 46410; L101 = 478235; L191 = 9611214.
- Сума до Lv10 = 3360, до Lv50 = 479785, до Lv100 = 10575085.

### 2.6 Формат `.scr` (виправлення JAVA_REFERENCE §1)
`al.java` 11-29: `[u16 LE count][(count+1)×u16 LE offset][UTF-8]`, рядок i = `[off[i], off[i+1])`. «4 байти на запис» — неправильно.

`decode_scr.py` виходить із циклу на першому порожньому рядку, тому:
- uimenu обрізано до 28 з 60;
- gamestr — до 67 з 71.

Повний uimenu (потрібні мені індекси):
- 12–18: Blacksmith, Management, Attributes, Skills, Gear, Inventory, Assign Items;
- 21–24: Buy/Sell/Enchant Item/Combine; 26: Network; 29: DIFFICULTY;
- 30–35: пункти титульного меню;
- **36** `1. Missions|2. Blacksmith|3. Network|4. Visiting|5. Equipment|6. Etc`;
- **37** `Options|Help`;
- **39** `Buy Item|Sell Item|Enchant Item|Combine Items`;
- **40** `Attributes|Skills|Gear|Inventory|Assign Items`;
- **41** `Resume|Options|Save|Assign Items|Help|Exit to Menu|Exit Game`;
- 48–54: `MOVE HEAL PASV FWD NEAR RANGE WHOLE`;
- 55–59: Slow…Fast.

gamestr 67–70: '', '.', 'Please enter', 'your character name.'.

### 2.7 Python, який я запускав (`python3 -I`, скрипти в scratchpad, дані передаються аргументом)
```python
def load(path):                         # формат d.java
    b=open(path,'rb').read(); n=b[0]; widths=list(b[1:1+n])
    offs=[]; k=0
    for w in widths: offs.append(k); k+=w
    return widths, offs, k, b[1+n:]
def geti(d,rs,offs,w,r,c):
    base=r*rs+offs[c]; v=0
    for i in range(w[c]): v|=d[base+i]<<(8*i)
    return v
def gets(d,rs,offs,w,r,c):
    base=r*rs+offs[c]; return d[base:base+w[c]].split(b'\0')[0].decode('latin1').strip()
# kibo: 8 cols [15,1,1,1,1,1,2,1] row 23 ×100; sungbo: 9 cols [15,1,2,1,1,1,1,1,1] row 24 ×137; shinki: 8 cols [15,1,2,1,2,1,4,1] row 27 ×18

def strings(path):                      # формат al.java (.scr)
    a=open(path,'rb').read(); n=a[0]|a[1]<<8
    return [a[(a[2+i*2]|a[3+i*2]<<8):(a[4+i*2]|a[5+i*2]<<8)].decode('utf-8','replace') for i in range(n)]

b=open('item-mixing-table.bin','rb').read(); S=lambda n:b[n*2]|b[n*2+1]<<8; N=149
rows=[(S(r),S(N+r),S(2*N+r),S(3*N+r)) for r in range(N)]   # sorted=True, ascending-in-row=True

vals=[int.from_bytes(e[2+4*i:6+4*i],'little') for i in range(199)]   # exp.arr
# ae.x unpack: 5200→[80,20,0,0] 1321000→[40,40,20,0] 169745950→[30,30,30,10] 421075205→[5,25,25,25] 572588032→[0,0,33,34]
```

### 2.8 Декодовані таблиці
Колонки:
- `spread`: у магазині стат = base + 0..spread−1 (`J()`), у дропі — base + 0..spread (`k(id,1)`);
- `shop price range`: `b(z)` для мінімального й максимального стату з `J()`;
- `sell` = ½ ціни.

#### kibo.arr — Normal items (id 101–200)

| id | name | type→slot | stat | base | spread | maxEnch | basePrice | icon/kind | reqLv | shop price range | sell (½) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 101 | Iron Blade | Weapon-long→0 | ATK | 2 | 3 | 5 | 120 | 3 | 1 | 320–520 | 160–260 |
| 102 | Steel Blade | Weapon-long→0 | ATK | 5 | 4 | 6 | 220 | 3 | 10 | 720–1020 | 360–510 |
| 103 | War Blade | Weapon-long→0 | ATK | 10 | 5 | 7 | 360 | 3 | 25 | 1360–1760 | 680–880 |
| 104 | Great Blade | Weapon-long→0 | ATK | 16 | 6 | 8 | 500 | 3 | 45 | 2100–2600 | 1050–1300 |
| 105 | Fleet Blade | Weapon-long→0 | ATK | 23 | 7 | 9 | 700 | 3 | 70 | 3000–3600 | 1500–1800 |
| 106 | Spontoon Pike | Weapon-long→0 | ATK | 3 | 2 | 5 | 160 | 4 | 1 | 460–560 | 230–280 |
| 107 | Iron Pike | Weapon-long→0 | ATK | 6 | 3 | 6 | 320 | 4 | 10 | 920–1120 | 460–560 |
| 108 | Steel Pike | Weapon-long→0 | ATK | 10 | 4 | 7 | 480 | 4 | 25 | 1480–1780 | 740–890 |
| 109 | Thrust Pike | Weapon-long→0 | ATK | 15 | 5 | 8 | 640 | 4 | 45 | 2140–2540 | 1070–1270 |
| 110 | Impaling Pike | Weapon-long→0 | ATK | 21 | 6 | 9 | 840 | 4 | 70 | 2940–3440 | 1470–1720 |
| 111 | Brawn Blade | Weapon-long→0 | ATK | 1 | 4 | 5 | 80 | 5 | 1 | 180–480 | 90–240 |
| 112 | Lead Blade | Weapon-long→0 | ATK | 6 | 5 | 6 | 120 | 5 | 10 | 720–1120 | 360–560 |
| 113 | Fealty Blade | Weapon-long→0 | ATK | 12 | 6 | 7 | 220 | 5 | 25 | 1420–1920 | 710–960 |
| 114 | Salvo Blade | Weapon-long→0 | ATK | 19 | 7 | 8 | 320 | 5 | 45 | 2220–2820 | 1110–1410 |
| 115 | A. Blade | Weapon-long→0 | ATK | 27 | 8 | 9 | 480 | 5 | 70 | 3180–3880 | 1590–1940 |
| 116 | Iron Claymore | Weapon-short→0 | ATK | 1 | 2 | 5 | 80 | 0 | 1 | 180–280 | 90–140 |
| 117 | Steel Claymore | Weapon-short→0 | ATK | 3 | 3 | 6 | 120 | 0 | 10 | 420–620 | 210–310 |
| 118 | War Claymore | Weapon-short→0 | ATK | 6 | 4 | 7 | 220 | 0 | 25 | 820–1120 | 410–560 |
| 119 | Great Claymore | Weapon-short→0 | ATK | 10 | 5 | 8 | 320 | 0 | 45 | 1320–1720 | 660–860 |
| 120 | Fleet Claymore | Weapon-short→0 | ATK | 15 | 6 | 9 | 480 | 0 | 70 | 1980–2480 | 990–1240 |
| 121 | Strong Sword | Weapon-short→0 | ATK | 2 | 2 | 5 | 120 | 1 | 1 | 320–420 | 160–210 |
| 122 | Steel Sword | Weapon-short→0 | ATK | 4 | 3 | 6 | 220 | 1 | 10 | 620–820 | 310–410 |
| 123 | War Sword | Weapon-short→0 | ATK | 7 | 4 | 7 | 360 | 1 | 25 | 1060–1360 | 530–680 |
| 124 | Bastard Sword | Weapon-short→0 | ATK | 11 | 5 | 8 | 500 | 1 | 45 | 1600–2000 | 800–1000 |
| 125 | Great Sword | Weapon-short→0 | ATK | 16 | 6 | 9 | 700 | 1 | 70 | 2300–2800 | 1150–1400 |
| 126 | Half-Axe | Weapon-short→0 | ATK | 3 | 2 | 5 | 120 | 2 | 1 | 420–520 | 210–260 |
| 127 | Steel Axe | Weapon-short→0 | ATK | 5 | 3 | 6 | 220 | 2 | 10 | 720–920 | 360–460 |
| 128 | Battle Axe | Weapon-short→0 | ATK | 8 | 4 | 7 | 360 | 2 | 25 | 1160–1460 | 580–730 |
| 129 | Crusader's Axe | Weapon-short→0 | ATK | 12 | 5 | 8 | 500 | 2 | 45 | 1700–2100 | 850–1050 |
| 130 | War Hammer Axe | Weapon-short→0 | ATK | 17 | 6 | 9 | 700 | 2 | 70 | 2400–2900 | 1200–1450 |
| 131 | Leather Helmet | Helmet→3 | DEF | 1 | 2 | 5 | 80 | 6 | 1 | 180–280 | 90–140 |
| 132 | Steel Helmet | Helmet→3 | DEF | 4 | 3 | 6 | 140 | 6 | 10 | 540–740 | 270–370 |
| 133 | Demon Helmet | Helmet→3 | DEF | 8 | 4 | 7 | 200 | 6 | 25 | 1000–1300 | 500–650 |
| 134 | Sage Helmet | Helmet→3 | DEF | 13 | 5 | 8 | 260 | 6 | 45 | 1560–1960 | 780–980 |
| 135 | Great Helmet | Helmet→3 | DEF | 19 | 6 | 9 | 340 | 6 | 70 | 2240–2740 | 1120–1370 |
| 136 | Leather Armour | Armour→5 | DEF | 3 | 3 | 5 | 160 | 7 | 1 | 460–660 | 230–330 |
| 137 | Enforced Armour | Armour→5 | DEF | 7 | 4 | 6 | 240 | 7 | 10 | 940–1240 | 470–620 |
| 138 | Chain Armour | Armour→5 | DEF | 12 | 5 | 7 | 320 | 7 | 25 | 1520–1920 | 760–960 |
| 139 | Fierce Armour | Armour→5 | DEF | 18 | 6 | 8 | 400 | 7 | 45 | 2200–2700 | 1100–1350 |
| 140 | Demon Armour | Armour→5 | DEF | 25 | 7 | 9 | 500 | 7 | 70 | 3000–3600 | 1500–1800 |
| 141 | Lord Armour | Armour→5 | HP | 15 | 15 | 5 | 260 | 7 | 1 | 560–760 | 280–380 |
| 142 | Emperor Armour | Armour→5 | HP | 35 | 20 | 6 | 400 | 7 | 10 | 1100–1400 | 550–700 |
| 143 | Sage Armour | Armour→5 | HP | 60 | 25 | 7 | 540 | 7 | 25 | 1740–2140 | 870–1070 |
| 144 | Scrybe Armour | Armour→5 | HP | 90 | 30 | 8 | 680 | 7 | 45 | 2480–2980 | 1240–1490 |
| 145 | Vast Armour | Armour→5 | HP | 125 | 35 | 9 | 880 | 7 | 70 | 3380–3980 | 1690–1990 |
| 146 | Steel Gauntlets | Gauntlets→2 | HP | 5 | 10 | 5 | 60 | 11 | 1 | 160–260 | 80–130 |
| 147 | Cross Gauntlets | Gauntlets→2 | HP | 20 | 15 | 6 | 120 | 11 | 10 | 520–720 | 260–360 |
| 148 | Demon Gauntlets | Gauntlets→2 | HP | 40 | 20 | 7 | 180 | 11 | 25 | 980–1280 | 490–640 |
| 149 | Sage Gauntlets | Gauntlets→2 | HP | 65 | 25 | 8 | 240 | 11 | 45 | 1540–1940 | 770–970 |
| 150 | Sky Gauntlets | Gauntlets→2 | HP | 95 | 30 | 9 | 320 | 11 | 70 | 2220–2720 | 1110–1360 |
| 151 | Leather Boots | Boots→8 | HP | 5 | 10 | 5 | 60 | 12 | 1 | 160–260 | 80–130 |
| 152 | Steel Boots | Boots→8 | HP | 20 | 15 | 6 | 120 | 12 | 10 | 520–720 | 260–360 |
| 153 | Fierce Boots | Boots→8 | HP | 40 | 20 | 7 | 180 | 12 | 25 | 980–1280 | 490–640 |
| 154 | Demon Boots | Boots→8 | HP | 65 | 25 | 8 | 240 | 12 | 45 | 1540–1940 | 770–970 |
| 155 | Alpha Boots | Boots→8 | HP | 95 | 30 | 9 | 320 | 12 | 70 | 2220–2720 | 1110–1360 |
| 156 | Leather Belt | Belt→6 | HP | 5 | 10 | 5 | 80 | 8 | 1 | 180–280 | 90–140 |
| 157 | Steel Belt | Belt→6 | HP | 20 | 15 | 6 | 130 | 8 | 10 | 530–730 | 265–365 |
| 158 | Fierce Belt | Belt→6 | HP | 40 | 20 | 7 | 180 | 8 | 25 | 980–1280 | 490–640 |
| 159 | Sage Belt | Belt→6 | HP | 65 | 25 | 8 | 230 | 8 | 45 | 1530–1930 | 765–965 |
| 160 | Enchanted Belt | Belt→6 | HP | 95 | 30 | 9 | 300 | 8 | 70 | 2200–2700 | 1100–1350 |
| 161 | Hawk Armlet | Armlet→1 | DEF | 1 | 1 | 5 | 60 | 9 | 1 | 160–160 | 80–80 |
| 162 | Mystic Armlet | Armlet→1 | DEF | 2 | 2 | 6 | 120 | 9 | 10 | 320–420 | 160–210 |
| 163 | Phoenix Armlet | Armlet→1 | DEF | 4 | 2 | 7 | 180 | 9 | 25 | 580–680 | 290–340 |
| 164 | Tiger Armlet | Armlet→1 | DEF | 6 | 2 | 8 | 240 | 9 | 45 | 840–940 | 420–470 |
| 165 | Demon Armlet | Armlet→1 | DEF | 8 | 2 | 9 | 320 | 9 | 70 | 1120–1220 | 560–610 |
| 166 | Energy Armlet | Armlet→1 | ATK | 1 | 2 | 5 | 160 | 9 | 1 | 260–360 | 130–180 |
| 167 | Fire Armlet | Armlet→1 | ATK | 4 | 3 | 6 | 320 | 9 | 10 | 720–920 | 360–460 |
| 168 | Thunder Armlet | Armlet→1 | ATK | 8 | 4 | 7 | 480 | 9 | 25 | 1280–1580 | 640–790 |
| 169 | Flame Armlet | Armlet→1 | ATK | 13 | 5 | 8 | 640 | 9 | 45 | 1940–2340 | 970–1170 |
| 170 | Light Armlet | Armlet→1 | ATK | 19 | 6 | 9 | 840 | 9 | 70 | 2740–3240 | 1370–1620 |
| 171 | Lord Armlet | Armlet→1 | HP | 5 | 10 | 5 | 80 | 9 | 1 | 180–280 | 90–140 |
| 172 | Emperor Armlet | Armlet→1 | HP | 20 | 10 | 6 | 130 | 9 | 10 | 530–630 | 265–315 |
| 173 | Sage Armlet | Armlet→1 | HP | 35 | 10 | 7 | 180 | 9 | 25 | 880–980 | 440–490 |
| 174 | Bliss Armlet | Armlet→1 | HP | 50 | 10 | 8 | 230 | 9 | 45 | 1230–1330 | 615–665 |
| 175 | Heaven's Armlet | Armlet→1 | HP | 65 | 10 | 9 | 300 | 9 | 70 | 1600–1700 | 800–850 |
| 176 | Zero Armlet | Armlet→1 | MP | 3 | 6 | 5 | 80 | 9 | 1 | 180–280 | 90–140 |
| 177 | Dead Armlet | Armlet→1 | MP | 10 | 9 | 6 | 130 | 9 | 10 | 430–730 | 215–365 |
| 178 | Ancient Armlet | Armlet→1 | MP | 20 | 12 | 7 | 180 | 9 | 25 | 780–1180 | 390–590 |
| 179 | Vision Armlet | Armlet→1 | MP | 33 | 15 | 8 | 230 | 9 | 45 | 1330–1730 | 665–865 |
| 180 | Majestic Armlet | Armlet→1 | MP | 49 | 18 | 9 | 300 | 9 | 70 | 1900–2500 | 950–1250 |
| 181 | Hawk Amulet | Amulet→4 | DEF | 1 | 1 | 5 | 60 | 10 | 1 | 160–160 | 80–80 |
| 182 | Mystic Amulet | Amulet→4 | DEF | 2 | 2 | 6 | 120 | 10 | 10 | 320–420 | 160–210 |
| 183 | Phoenix Amulet | Amulet→4 | DEF | 4 | 2 | 7 | 180 | 10 | 25 | 580–680 | 290–340 |
| 184 | Tiger Amulet | Amulet→4 | DEF | 6 | 2 | 8 | 240 | 10 | 45 | 840–940 | 420–470 |
| 185 | Demon Amulet | Amulet→4 | DEF | 8 | 2 | 9 | 320 | 10 | 70 | 1120–1220 | 560–610 |
| 186 | Energy Amulet | Amulet→4 | ATK | 2 | 2 | 5 | 160 | 10 | 1 | 360–460 | 180–230 |
| 187 | Fire Amulet | Amulet→4 | ATK | 5 | 3 | 6 | 320 | 10 | 10 | 820–1020 | 410–510 |
| 188 | Thunder Amulet | Amulet→4 | ATK | 9 | 4 | 7 | 480 | 10 | 25 | 1380–1680 | 690–840 |
| 189 | Flame Amulet | Amulet→4 | ATK | 14 | 5 | 8 | 640 | 10 | 45 | 2040–2440 | 1020–1220 |
| 190 | Light Amulet | Amulet→4 | ATK | 20 | 6 | 9 | 840 | 10 | 70 | 2840–3340 | 1420–1670 |
| 191 | Lord Amulet | Amulet→4 | HP | 10 | 10 | 5 | 80 | 10 | 1 | 280–380 | 140–190 |
| 192 | Emperor Amulet | Amulet→4 | HP | 25 | 15 | 6 | 130 | 10 | 10 | 630–830 | 315–415 |
| 193 | Sage Amulet | Amulet→4 | HP | 45 | 20 | 7 | 180 | 10 | 25 | 1080–1380 | 540–690 |
| 194 | Bliss Amulet | Amulet→4 | HP | 70 | 20 | 8 | 230 | 10 | 45 | 1630–1930 | 815–965 |
| 195 | Heaven's Amulet | Amulet→4 | HP | 95 | 20 | 9 | 300 | 10 | 70 | 2200–2500 | 1100–1250 |
| 196 | Zero Amulet | Amulet→4 | MP | 3 | 3 | 5 | 80 | 10 | 1 | 180–180 | 90–90 |
| 197 | Dead Amulet | Amulet→4 | MP | 7 | 6 | 6 | 130 | 10 | 10 | 330–530 | 165–265 |
| 198 | Ancient Amulet | Amulet→4 | MP | 14 | 9 | 7 | 180 | 10 | 25 | 580–880 | 290–440 |
| 199 | Vision Amulet | Amulet→4 | MP | 24 | 12 | 8 | 230 | 10 | 45 | 1030–1330 | 515–665 |
| 200 | Majestic Amulet | Amulet→4 | MP | 37 | 15 | 9 | 300 | 10 | 70 | 1500–2000 | 750–1000 |

#### sungbo.arr — Special items (id 301–437)

| id | name | type→slot | ATK | DEF | HP | MP | maxEnch | icon/kind | reqLv | price (b()) | sell |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 301 | Steel Spear | Weapon-long→0 | 30 | 1 | 0 | 0 | 9 | 3 | 62 | 12400 | 6200 |
| 302 | Impale Pike | Weapon-long→0 | 35 | 1 | 0 | 0 | 9 | 5 | 72 | 14400 | 7200 |
| 303 | Shadow Spear | Weapon-long→0 | 32 | 2 | 0 | 0 | 9 | 3 | 68 | 13600 | 6800 |
| 304 | Lunar Pike | Weapon-long→0 | 38 | 3 | 0 | 0 | 9 | 5 | 82 | 16400 | 8200 |
| 305 | Light Spear | Weapon-long→0 | 32 | 2 | 0 | 0 | 9 | 3 | 68 | 13600 | 6800 |
| 306 | Slayer Spear | Weapon-long→0 | 45 | 5 | 0 | 0 | 9 | 3 | 100 | 20000 | 10000 |
| 307 | Upshot Pike | Weapon-long→0 | 28 | 3 | 0 | 0 | 9 | 4 | 62 | 12400 | 6200 |
| 308 | Sarissa Spear | Weapon-long→0 | 30 | 1 | 0 | 0 | 9 | 4 | 62 | 12400 | 6200 |
| 309 | Barchi Spear | Weapon-long→0 | 30 | 0 | 0 | 0 | 9 | 3 | 60 | 12000 | 6000 |
| 310 | Raze Pike | Weapon-long→0 | 32 | 2 | 0 | 0 | 9 | 4 | 68 | 13600 | 6800 |
| 311 | Boar Spear | Weapon-long→0 | 30 | 3 | 0 | 0 | 9 | 3 | 66 | 13200 | 6600 |
| 312 | Piercing Spear | Weapon-long→0 | 30 | 4 | 0 | 0 | 9 | 3 | 68 | 13600 | 6800 |
| 313 | Piercing Pike | Weapon-long→0 | 32 | 5 | 0 | 0 | 9 | 4 | 74 | 14800 | 7400 |
| 314 | Dawn Pike | Weapon-long→0 | 35 | 1 | 0 | 0 | 9 | 3 | 72 | 14400 | 7200 |
| 315 | Arete Pike | Weapon-long→0 | 25 | 8 | 0 | 0 | 9 | 3 | 66 | 13200 | 6600 |
| 316 | Godendag Pike | Weapon-long→0 | 45 | 4 | 0 | 0 | 9 | 3 | 98 | 19600 | 9800 |
| 317 | Holy Pike | Weapon-long→0 | 35 | 2 | 0 | 0 | 9 | 5 | 74 | 14800 | 7400 |
| 318 | Amethyst Sword | Weapon-short→0 | 24 | 3 | 0 | 0 | 9 | 1 | 54 | 10800 | 5400 |
| 319 | Demon Sword | Weapon-short→0 | 24 | 4 | 0 | 0 | 9 | 1 | 56 | 11200 | 5600 |
| 320 | Myriad Claymore | Weapon-short→0 | 27 | 6 | 0 | 0 | 9 | 1 | 66 | 13200 | 6600 |
| 321 | Pyrrhic Sword | Weapon-short→0 | 27 | 8 | 0 | 0 | 9 | 0 | 70 | 14000 | 7000 |
| 322 | Command Axe | Weapon-short→0 | 20 | 6 | 0 | 0 | 9 | 2 | 52 | 10400 | 5200 |
| 323 | Savoir Sword | Weapon-short→0 | 24 | 6 | 0 | 0 | 9 | 1 | 60 | 12000 | 6000 |
| 324 | Ballistic Sword | Weapon-short→0 | 27 | 3 | 0 | 0 | 9 | 1 | 60 | 12000 | 6000 |
| 325 | Templar Axe | Weapon-short→0 | 22 | 3 | 0 | 0 | 9 | 2 | 50 | 10000 | 5000 |
| 326 | Suffuse Sword | Weapon-short→0 | 24 | 3 | 0 | 0 | 9 | 1 | 54 | 10800 | 5400 |
| 327 | Lucent Axe | Weapon-short→0 | 32 | 3 | 0 | 0 | 9 | 2 | 70 | 14000 | 7000 |
| 328 | Vestige Sword | Weapon-short→0 | 27 | 6 | 0 | 0 | 9 | 1 | 66 | 13200 | 6600 |
| 329 | Excel Claymore | Weapon-short→0 | 27 | 9 | 0 | 0 | 9 | 0 | 72 | 14400 | 7200 |
| 330 | Celest Claymore | Weapon-short→0 | 30 | 6 | 0 | 0 | 9 | 0 | 72 | 14400 | 7200 |
| 331 | Triton Claymore | Weapon-short→0 | 32 | 6 | 0 | 0 | 9 | 0 | 76 | 15200 | 7600 |
| 332 | Bane Sword | Weapon-short→0 | 32 | 3 | 0 | 0 | 9 | 1 | 70 | 14000 | 7000 |
| 333 | Sear Sword | Weapon-short→0 | 30 | 3 | 0 | 0 | 9 | 1 | 66 | 13200 | 6600 |
| 334 | Fervor Claymore | Weapon-short→0 | 34 | 8 | 0 | 0 | 9 | 0 | 84 | 16800 | 8400 |
| 335 | Saint Claymore | Weapon-short→0 | 37 | 3 | 0 | 0 | 9 | 1 | 80 | 16000 | 8000 |
| 336 | Carmine Axe | Weapon-short→0 | 37 | 6 | 0 | 0 | 9 | 2 | 86 | 17200 | 8600 |
| 337 | Liege Axe | Weapon-short→0 | 27 | 3 | 0 | 0 | 9 | 2 | 60 | 12000 | 6000 |
| 338 | Fierce Sword | Weapon-short→0 | 32 | 3 | 0 | 0 | 9 | 1 | 70 | 14000 | 7000 |
| 339 | Sage Sword | Weapon-short→0 | 34 | 8 | 0 | 0 | 9 | 1 | 84 | 16800 | 8400 |
| 340 | Austere Sword | Weapon-short→0 | 37 | 4 | 0 | 0 | 9 | 1 | 82 | 16400 | 8200 |
| 341 | Flatbow | Special→7 | 15 | 0 | 0 | 0 | 9 | 6 | 30 | 6000 | 3000 |
| 342 | Longbow | Special→7 | 12 | 0 | 0 | 0 | 6 | 6 | 24 | 4800 | 2400 |
| 343 | Mongol Bow | Special→7 | 10 | 0 | 0 | 0 | 7 | 6 | 20 | 4000 | 2000 |
| 344 | Perso Bow | Special→7 | 8 | 0 | 0 | 0 | 6 | 6 | 16 | 3200 | 1600 |
| 345 | Hungarian Bow | Special→7 | 5 | 0 | 0 | 0 | 9 | 6 | 10 | 2000 | 1000 |
| 346 | Hun Bow | Special→7 | 3 | 0 | 0 | 15 | 9 | 6 | 16 | 3200 | 1600 |
| 347 | Weald Crown | Helmet→3 | 0 | 27 | 0 | 15 | 5 | 7 | 64 | 12800 | 6400 |
| 348 | Venerable Crown | Helmet→3 | 0 | 30 | 0 | 0 | 4 | 7 | 60 | 12000 | 6000 |
| 349 | Lucent Crown | Helmet→3 | 0 | 33 | 25 | 0 | 6 | 7 | 76 | 15200 | 7600 |
| 350 | Triple Crown | Helmet→3 | 0 | 36 | 0 | 0 | 7 | 7 | 72 | 14400 | 7200 |
| 351 | Mystic Crown | Helmet→3 | 0 | 30 | 0 | 60 | 8 | 7 | 100 | 20000 | 10000 |
| 352 | Plate Armour | Armour→5 | 0 | 35 | 150 | 0 | 8 | 8 | 130 | 26000 | 13000 |
| 353 | Plate Armour | Armour→5 | 0 | 35 | 150 | 0 | 8 | 8 | 130 | 26000 | 13000 |
| 354 | Brute Armour | Armour→5 | 0 | 41 | 150 | 0 | 9 | 8 | 142 | 28400 | 14200 |
| 355 | Bliss Armour | Armour→5 | 0 | 38 | 145 | 0 | 9 | 8 | 134 | 26800 | 13400 |
| 356 | Azul Armour | Armour→5 | 0 | 27 | 0 | 30 | 7 | 8 | 74 | 14800 | 7400 |
| 357 | Auric Armour | Armour→5 | 0 | 24 | 0 | 39 | 6 | 8 | 74 | 14800 | 7400 |
| 358 | Herald Armour | Armour→5 | 0 | 21 | 0 | 99 | 9 | 8 | 108 | 21600 | 10800 |
| 359 | Omega Boots | Boots→8 | 0 | 0 | 130 | 15 | 5 | 9 | 69 | 12400 | 6200 |
| 360 | Stalwart Boots | Boots→8 | 0 | 0 | 145 | 18 | 6 | 9 | 78 | 14000 | 7000 |
| 361 | Excel Boots | Boots→8 | 0 | 0 | 160 | 21 | 5 | 9 | 87 | 15600 | 7800 |
| 362 | Faith Boots | Boots→8 | 0 | 0 | 175 | 24 | 7 | 9 | 96 | 17200 | 8600 |
| 363 | War Boots | Boots→8 | 0 | 0 | 230 | 0 | 5 | 9 | 102 | 18400 | 9200 |
| 364 | Vim Boots | Boots→8 | 0 | 0 | 145 | 9 | 6 | 9 | 71 | 12800 | 6400 |
| 365 | Azul Boots | Boots→8 | 0 | 0 | 130 | 0 | 5 | 9 | 58 | 10400 | 5200 |
| 366 | Havoc Boots | Boots→8 | 0 | 0 | 255 | 0 | 6 | 9 | 113 | 20400 | 10200 |
| 367 | Lancer Boots | Boots→8 | 0 | 0 | 155 | 21 | 5 | 9 | 84 | 15200 | 7600 |
| 368 | Virtue Boots | Boots→8 | 0 | 0 | 180 | 24 | 8 | 9 | 98 | 17600 | 8800 |
| 369 | Scabre Belt | Belt→6 | 0 | 0 | 150 | 0 | 7 | 10 | 60 | 12000 | 6000 |
| 370 | Palisade Belt | Belt→6 | 0 | 0 | 135 | 0 | 6 | 10 | 54 | 10800 | 5400 |
| 371 | Belvedere Belt | Belt→6 | 0 | 0 | 120 | 15 | 5 | 10 | 58 | 11600 | 5800 |
| 372 | Enchanted Belt | Belt→6 | 0 | 0 | 150 | 30 | 7 | 10 | 80 | 16000 | 8000 |
| 373 | Heartfire Belt | Belt→6 | 0 | 0 | 165 | 0 | 9 | 10 | 66 | 13200 | 6600 |
| 374 | Iron Will Belt | Belt→6 | 0 | 0 | 125 | 30 | 7 | 10 | 70 | 14000 | 7000 |
| 375 | Ardent Belt | Belt→6 | 0 | 0 | 150 | 0 | 6 | 10 | 60 | 12000 | 6000 |
| 376 | Galvanic Belt | Belt→6 | 0 | 0 | 125 | 30 | 9 | 10 | 70 | 14000 | 7000 |
| 377 | Palomino Rouncy | Special→7 | 0 | 3 | 25 | 0 | 0 | 11 | 16 | 6400 | 3200 |
| 378 | Gray Garron | Special→7 | 0 | 5 | 50 | 0 | 0 | 11 | 30 | 12000 | 6000 |
| 379 | Black Barb | Special→7 | 0 | 4 | 75 | 36 | 0 | 11 | 62 | 24800 | 12400 |
| 380 | Dun Sumpter | Special→7 | 0 | 1 | 35 | 0 | 0 | 11 | 16 | 6400 | 3200 |
| 381 | Light Palfrey | Special→7 | 0 | 2 | 40 | 0 | 0 | 11 | 20 | 8000 | 4000 |
| 382 | Gray Clydesdale | Special→7 | 0 | 6 | 100 | 0 | 0 | 11 | 52 | 20800 | 10400 |
| 383 | Black Garron | Special→7 | 0 | 25 | 50 | 0 | 0 | 11 | 70 | 28000 | 14000 |
| 384 | White Barb | Special→7 | 0 | 0 | 75 | 39 | 0 | 11 | 56 | 22400 | 11200 |
| 385 | Black Courser | Special→7 | 0 | 0 | 65 | 45 | 0 | 11 | 56 | 22400 | 11200 |
| 386 | Dark Palfrey | Special→7 | 0 | 8 | 40 | 0 | 0 | 11 | 32 | 12800 | 6400 |
| 387 | Dark Sumpter | Special→7 | 0 | 3 | 35 | 60 | 0 | 11 | 60 | 24000 | 12000 |
| 388 | Black Destrier | Special→7 | 0 | 2 | 90 | 0 | 0 | 11 | 40 | 16000 | 8000 |
| 389 | Black Palfrey | Special→7 | 0 | 10 | 40 | 0 | 0 | 11 | 36 | 14400 | 7200 |
| 390 | Chestnut Rouncy | Special→7 | 0 | 9 | 30 | 0 | 0 | 11 | 30 | 12000 | 6000 |
| 391 | Gray Sumpter | Special→7 | 0 | 10 | 30 | 0 | 0 | 11 | 32 | 12800 | 6400 |
| 392 | White Garron | Special→7 | 0 | 11 | 50 | 0 | 0 | 11 | 42 | 16800 | 8400 |
| 393 | Dark Clydesdale | Special→7 | 0 | 12 | 100 | 0 | 0 | 11 | 64 | 25600 | 12800 |
| 394 | Chestnut Garron | Special→7 | 0 | 0 | 55 | 0 | 0 | 11 | 22 | 8800 | 4400 |
| 395 | Dark Courser | Special→7 | 0 | 0 | 60 | 0 | 0 | 11 | 24 | 9600 | 4800 |
| 396 | Light Courser | Special→7 | 0 | 0 | 60 | 0 | 0 | 11 | 24 | 9600 | 4800 |
| 397 | White Courser | Special→7 | 0 | 0 | 65 | 0 | 0 | 11 | 26 | 10400 | 5200 |
| 398 | Chestnut Barb | Special→7 | 0 | 0 | 70 | 0 | 0 | 11 | 28 | 11200 | 5600 |
| 399 | Dark Barb | Special→7 | 0 | 0 | 75 | 0 | 0 | 11 | 30 | 12000 | 6000 |
| 400 | Albino Rouncy | Special→7 | 0 | 0 | 10 | 60 | 0 | 11 | 44 | 17600 | 8800 |
| 401 | Light Barb | Special→7 | 0 | 0 | 75 | 45 | 0 | 11 | 60 | 24000 | 12000 |
| 402 | White Destrier | Special→7 | 0 | 0 | 80 | 0 | 0 | 11 | 32 | 12800 | 6400 |
| 403 | Element Scroll | Special→7 | 0 | 0 | 0 | 84 | 0 | 12 | 56 | 22400 | 11200 |
| 404 | Tactical Scroll | Special→7 | 10 | 0 | 0 | 0 | 0 | 12 | 20 | 8000 | 4000 |
| 405 | Royalty Scroll | Special→7 | 0 | 0 | 0 | 15 | 0 | 12 | 10 | 4000 | 2000 |
| 406 | A-Scroll | Special→7 | 0 | 0 | 0 | 24 | 0 | 12 | 16 | 6400 | 3200 |
| 407 | Turn Scroll | Special→7 | 0 | 0 | 0 | 30 | 0 | 12 | 20 | 8000 | 4000 |
| 408 | History Scroll | Special→7 | 0 | 5 | 0 | 0 | 0 | 12 | 10 | 4000 | 2000 |
| 409 | Ethics Scroll | Special→7 | 0 | 0 | 0 | 15 | 0 | 12 | 10 | 4000 | 2000 |
| 410 | Fiber Scroll | Special→7 | 0 | 0 | 0 | 36 | 0 | 12 | 24 | 9600 | 4800 |
| 411 | Far East Scroll | Special→7 | 0 | 0 | 0 | 45 | 0 | 12 | 30 | 12000 | 6000 |
| 412 | Morality Scroll | Special→7 | 0 | 0 | 105 | 0 | 0 | 12 | 42 | 16800 | 8400 |
| 413 | Feoff Scroll | Special→7 | 0 | 10 | 0 | 0 | 0 | 12 | 20 | 8000 | 4000 |
| 414 | Mana Scroll | Special→7 | 0 | 0 | 0 | 120 | 0 | 12 | 80 | 32000 | 16000 |
| 415 | Western Scroll | Special→7 | 0 | 15 | 0 | 0 | 0 | 12 | 30 | 12000 | 6000 |
| 416 | Dutiful Scroll | Special→7 | 0 | 0 | 0 | 135 | 0 | 12 | 90 | 36000 | 18000 |
| 417 | Duty Scroll | Special→7 | 0 | 0 | 0 | 54 | 0 | 12 | 36 | 14400 | 7200 |
| 418 | Rapture Scroll | Special→7 | 0 | 0 | 210 | 0 | 0 | 12 | 84 | 33600 | 16800 |
| 419 | Sire Scroll | Special→7 | 0 | 0 | 0 | 180 | 0 | 12 | 120 | 48000 | 24000 |
| 420 | Signory Scroll | Special→7 | 0 | 20 | 0 | 0 | 0 | 12 | 40 | 16000 | 8000 |
| 421 | Heart Scroll | Special→7 | 0 | 0 | 0 | 60 | 0 | 12 | 40 | 16000 | 8000 |
| 422 | Insight Scroll | Special→7 | 0 | 0 | 0 | 75 | 0 | 12 | 50 | 20000 | 10000 |
| 423 | Autumn Scroll | Special→7 | 0 | 0 | 0 | 90 | 0 | 12 | 60 | 24000 | 12000 |
| 424 | Peace Scroll | Special→7 | 0 | 0 | 225 | 0 | 0 | 12 | 90 | 36000 | 18000 |
| 425 | Soul Scroll | Special→7 | 0 | 0 | 0 | 105 | 0 | 12 | 70 | 28000 | 14000 |
| 426 | Sprint Scroll | Special→7 | 0 | 0 | 0 | 120 | 0 | 12 | 80 | 32000 | 16000 |
| 427 | Ferver Scroll | Special→7 | 0 | 0 | 0 | 72 | 0 | 12 | 48 | 19200 | 9600 |
| 428 | Ardor Scroll | Special→7 | 0 | 0 | 0 | 45 | 0 | 12 | 30 | 12000 | 6000 |
| 429 | Trial Scroll | Special→7 | 0 | 0 | 0 | 27 | 0 | 12 | 18 | 7200 | 3600 |
| 430 | Chastity Scroll | Special→7 | 0 | 0 | 0 | 18 | 0 | 12 | 12 | 4800 | 2400 |
| 431 | Dogma Scroll | Special→7 | 0 | 0 | 0 | 15 | 0 | 12 | 10 | 4000 | 2000 |
| 432 | Pith Scroll | Special→7 | 0 | 0 | 0 | 90 | 0 | 12 | 60 | 24000 | 12000 |
| 433 | Nature Scroll | Special→7 | 0 | 20 | 0 | 0 | 0 | 12 | 40 | 16000 | 8000 |
| 434 | Rise Potion | Special→7 | 0 | 0 | 0 | 0 | 0 | 13 | 0 | 0 | 0 |
| 435 | Azure Potion | Special→7 | 0 | 0 | 0 | 0 | 0 | 14 | 0 | 0 | 0 |
| 436 | Falls Medicine | Special→7 | 0 | 0 | 0 | 0 | 0 | 15 | 0 | 0 | 0 |
| 437 | Forest Medicine | Special→7 | 0 | 0 | 0 | 0 | 0 | 16 | 0 | 0 | 0 |

#### shinki.arr — Rare items (id 501–518)

| id | name | type→slot | ATK | DEF | HP | MP | price | reqLv | sell |
|---|---|---|---|---|---|---|---|---|---|
| 501 | Book of Valor | Special→7 | 0 | 0 | 150 | 150 | 150000 | 130 | 75000 |
| 502 | Silk Towel | Special→7 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| 503 | Heaven's Pike | Weapon-long→0 | 135 | 36 | 0 | 0 | 256500 | 135 | 128250 |
| 504 | Emperor's Seal | Special→7 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| 505 | Heaven's Armour | Armour→5 | 0 | 90 | 350 | 0 | 310000 | 145 | 155000 |
| 506 | Great Stallion | Special→7 | 0 | 40 | 300 | 150 | 285000 | 100 | 142500 |
| 507 | Heaven's Boots | Boots→8 | 10 | 80 | 165 | 0 | 217500 | 99 | 108750 |
| 508 | Heaven's Sword | Weapon-long→0 | 128 | 25 | 0 | 0 | 229500 | 125 | 114750 |
| 509 | Next Claymore | Weapon-short→0 | 90 | 30 | 0 | 0 | 180000 | 90 | 90000 |
| 510 | Swift Falchion | Weapon-long→0 | 125 | 5 | 0 | 0 | 195000 | 110 | 97500 |
| 511 | Tragedy Blade | Weapon-long→0 | 130 | 5 | 0 | 0 | 202500 | 130 | 101250 |
| 512 | Canon Claymore | Weapon-short→0 | 93 | 33 | 0 | 0 | 189000 | 95 | 94500 |
| 513 | Heaven's Sabre | Weapon-long→0 | 128 | 4 | 0 | 0 | 198000 | 115 | 99000 |
| 514 | Sky Claymore | Weapon-short→0 | 96 | 28 | 0 | 0 | 186000 | 95 | 93000 |
| 515 | Sky Sword | Special→7 | 55 | 0 | 0 | 0 | 82500 | 92 | 41250 |
| 516 | Heaven's Sword | Weapon-short→0 | 105 | 15 | 0 | 0 | 180000 | 90 | 90000 |
| 517 | Heaven's Crown | Helmet→3 | 0 | 30 | 200 | 0 | 145000 | 100 | 72500 |
| 518 | Heaven's Belt | Belt→6 | 0 | 80 | 150 | 0 | 195000 | 80 | 97500 |

#### item-mixing-table.bin — 149 рецептів
- `p_success` = (⌊(200−reqLv)/12⌋+1)/101.
- `p_lose1` = ймовірність при провалі втратити **один** випадковий інгредієнт (§3.7).

| row | in1 | in2 | in3 | → result | reqLv | p_success | p_lose1 (on fail) |
|---|---|---|---|---|---|---|---|
| 0 | 101 Iron Blade | 156 Leather Belt | 186 Energy Amulet | **342 Longbow** | 24 | 14.9% | 57% |
| 1 | 104 Great Blade | 161 Hawk Armlet | 188 Thunder Amulet | **301 Steel Spear** | 62 | 11.9% | 59% |
| 2 | 104 Great Blade | 161 Hawk Armlet | 188 Thunder Amulet | **309 Barchi Spear** | 60 | 11.9% | 59% |
| 3 | 104 Great Blade | 161 Hawk Armlet | 189 Flame Amulet | **303 Shadow Spear** | 68 | 11.9% | 59% |
| 4 | 104 Great Blade | 161 Hawk Armlet | 189 Flame Amulet | **305 Light Spear** | 68 | 11.9% | 59% |
| 5 | 104 Great Blade | 162 Mystic Armlet | 188 Thunder Amulet | **311 Boar Spear** | 66 | 11.9% | 59% |
| 6 | 104 Great Blade | 163 Phoenix Armlet | 188 Thunder Amulet | **312 Piercing Spear** | 68 | 11.9% | 59% |
| 7 | 104 Great Blade | 165 Demon Armlet | 187 Fire Amulet | **315 Arete Pike** | 66 | 11.9% | 59% |
| 8 | 105 Fleet Blade | 161 Hawk Armlet | 190 Light Amulet | **314 Dawn Pike** | 72 | 10.9% | 60% |
| 9 | 105 Fleet Blade | 163 Phoenix Armlet | 190 Light Amulet | **306 Slayer Spear** | 100 | 8.9% | 61% |
| 10 | 105 Fleet Blade | 163 Phoenix Armlet | 190 Light Amulet | **316 Godendag Pike** | 98 | 8.9% | 61% |
| 11 | 106 Spontoon Pike | 156 Leather Belt | 186 Energy Amulet | **341 Flatbow** | 30 | 14.9% | 57% |
| 12 | 109 Thrust Pike | 161 Hawk Armlet | 188 Thunder Amulet | **308 Sarissa Spear** | 62 | 11.9% | 59% |
| 13 | 109 Thrust Pike | 161 Hawk Armlet | 189 Flame Amulet | **310 Raze Pike** | 68 | 11.9% | 59% |
| 14 | 109 Thrust Pike | 162 Mystic Armlet | 187 Fire Amulet | **307 Upshot Pike** | 62 | 11.9% | 59% |
| 15 | 110 Impaling Pike | 163 Phoenix Armlet | 189 Flame Amulet | **313 Piercing Pike** | 74 | 10.9% | 60% |
| 16 | 111 Brawn Blade | 156 Leather Belt | 186 Energy Amulet | **343 Mongol Bow** | 20 | 15.8% | 56% |
| 17 | 115 A. Blade | 161 Hawk Armlet | 190 Light Amulet | **302 Impale Pike** | 72 | 10.9% | 60% |
| 18 | 115 A. Blade | 161 Hawk Armlet | 190 Light Amulet | **317 Holy Pike** | 74 | 10.9% | 60% |
| 19 | 115 A. Blade | 162 Mystic Armlet | 190 Light Amulet | **304 Lunar Pike** | 82 | 9.9% | 60% |
| 20 | 116 Iron Claymore | 166 Energy Armlet | 186 Energy Amulet | **346 Hun Bow** | 16 | 15.8% | 56% |
| 21 | 120 Fleet Claymore | 164 Tiger Armlet | 188 Thunder Amulet | **330 Celest Claymore** | 72 | 10.9% | 60% |
| 22 | 120 Fleet Claymore | 164 Tiger Armlet | 189 Flame Amulet | **331 Triton Claymore** | 76 | 10.9% | 60% |
| 23 | 120 Fleet Claymore | 165 Demon Armlet | 187 Fire Amulet | **321 Pyrrhic Sword** | 70 | 10.9% | 60% |
| 24 | 120 Fleet Claymore | 165 Demon Armlet | 187 Fire Amulet | **329 Excel Claymore** | 72 | 10.9% | 60% |
| 25 | 120 Fleet Claymore | 165 Demon Armlet | 189 Flame Amulet | **334 Fervor Claymore** | 84 | 9.9% | 60% |
| 26 | 121 Strong Sword | 166 Energy Armlet | 186 Energy Amulet | **345 Hungarian Bow** | 10 | 15.8% | 56% |
| 27 | 124 Bastard Sword | 162 Mystic Armlet | 187 Fire Amulet | **318 Amethyst Sword** | 54 | 12.9% | 58% |
| 28 | 124 Bastard Sword | 162 Mystic Armlet | 187 Fire Amulet | **324 Ballistic Sword** | 60 | 11.9% | 59% |
| 29 | 124 Bastard Sword | 162 Mystic Armlet | 187 Fire Amulet | **326 Suffuse Sword** | 54 | 12.9% | 58% |
| 30 | 124 Bastard Sword | 162 Mystic Armlet | 188 Thunder Amulet | **333 Sear Sword** | 66 | 11.9% | 59% |
| 31 | 124 Bastard Sword | 163 Phoenix Armlet | 187 Fire Amulet | **319 Demon Sword** | 56 | 12.9% | 58% |
| 32 | 124 Bastard Sword | 164 Tiger Armlet | 187 Fire Amulet | **320 Myriad Claymore** | 66 | 11.9% | 59% |
| 33 | 124 Bastard Sword | 164 Tiger Armlet | 187 Fire Amulet | **323 Savoir Sword** | 60 | 11.9% | 59% |
| 34 | 124 Bastard Sword | 164 Tiger Armlet | 187 Fire Amulet | **328 Vestige Sword** | 66 | 11.9% | 59% |
| 35 | 125 Great Sword | 162 Mystic Armlet | 189 Flame Amulet | **332 Bane Sword** | 70 | 10.9% | 60% |
| 36 | 125 Great Sword | 162 Mystic Armlet | 189 Flame Amulet | **338 Fierce Sword** | 70 | 10.9% | 60% |
| 37 | 125 Great Sword | 162 Mystic Armlet | 190 Light Amulet | **335 Saint Claymore** | 80 | 10.9% | 60% |
| 38 | 125 Great Sword | 163 Phoenix Armlet | 190 Light Amulet | **340 Austere Sword** | 82 | 9.9% | 60% |
| 39 | 125 Great Sword | 165 Demon Armlet | 189 Flame Amulet | **339 Sage Sword** | 84 | 9.9% | 60% |
| 40 | 126 Half-Axe | 166 Energy Armlet | 186 Energy Amulet | **344 Perso Bow** | 16 | 15.8% | 56% |
| 41 | 129 Crusader's Axe | 162 Mystic Armlet | 187 Fire Amulet | **325 Templar Axe** | 50 | 12.9% | 58% |
| 42 | 129 Crusader's Axe | 162 Mystic Armlet | 187 Fire Amulet | **337 Liege Axe** | 60 | 11.9% | 59% |
| 43 | 129 Crusader's Axe | 164 Tiger Armlet | 187 Fire Amulet | **322 Command Axe** | 52 | 12.9% | 58% |
| 44 | 130 War Hammer Axe | 162 Mystic Armlet | 189 Flame Amulet | **327 Lucent Axe** | 70 | 10.9% | 60% |
| 45 | 130 War Hammer Axe | 164 Tiger Armlet | 190 Light Amulet | **336 Carmine Axe** | 86 | 9.9% | 60% |
| 46 | 134 Sage Helmet | 161 Hawk Armlet | 198 Ancient Amulet | **347 Weald Crown** | 64 | 11.9% | 59% |
| 47 | 134 Sage Helmet | 162 Mystic Armlet | 191 Lord Amulet | **348 Venerable Crown** | 60 | 11.9% | 59% |
| 48 | 135 Great Helmet | 162 Mystic Armlet | 180 Majestic Armlet | **351 Mystic Crown** | 100 | 8.9% | 61% |
| 49 | 135 Great Helmet | 164 Tiger Armlet | 181 Hawk Amulet | **350 Triple Crown** | 72 | 10.9% | 60% |
| 50 | 135 Great Helmet | 165 Demon Armlet | 192 Emperor Amulet | **349 Lucent Crown** | 76 | 10.9% | 60% |
| 51 | 140 Demon Armour | 162 Mystic Armlet | 199 Vision Amulet | **357 Auric Armour** | 74 | 10.9% | 60% |
| 52 | 140 Demon Armour | 163 Phoenix Armlet | 198 Ancient Amulet | **356 Azul Armour** | 74 | 10.9% | 60% |
| 53 | 140 Demon Armour | 180 Majestic Armlet | 200 Majestic Amulet | **358 Herald Armour** | 108 | 7.9% | 62% |
| 54 | 145 Vast Armour | 174 Bliss Armlet | 194 Bliss Amulet | **355 Bliss Armour** | 134 | 5.9% | 63% |
| 55 | 145 Vast Armour | 175 Heaven's Armlet | 194 Bliss Amulet | **352 Plate Armour** | 130 | 5.9% | 63% |
| 56 | 145 Vast Armour | 175 Heaven's Armlet | 194 Bliss Amulet | **353 Plate Armour** | 130 | 5.9% | 63% |
| 57 | 145 Vast Armour | 175 Heaven's Armlet | 195 Heaven's Amulet | **354 Brute Armour** | 142 | 5.0% | 64% |
| 58 | 151 Leather Boots | 174 Bliss Armlet | 181 Hawk Amulet | **365 Azul Boots** | 58 | 11.9% | 59% |
| 59 | 151 Leather Boots | 175 Heaven's Armlet | 198 Ancient Amulet | **359 Omega Boots** | 69 | 10.9% | 60% |
| 60 | 152 Steel Boots | 175 Heaven's Armlet | 197 Dead Amulet | **364 Vim Boots** | 71 | 10.9% | 60% |
| 61 | 152 Steel Boots | 175 Heaven's Armlet | 198 Ancient Amulet | **360 Stalwart Boots** | 78 | 10.9% | 60% |
| 62 | 153 Fierce Boots | 174 Bliss Armlet | 198 Ancient Amulet | **367 Lancer Boots** | 84 | 9.9% | 60% |
| 63 | 153 Fierce Boots | 175 Heaven's Armlet | 198 Ancient Amulet | **361 Excel Boots** | 87 | 9.9% | 60% |
| 64 | 154 Demon Boots | 175 Heaven's Armlet | 199 Vision Amulet | **362 Faith Boots** | 96 | 8.9% | 61% |
| 65 | 154 Demon Boots | 175 Heaven's Armlet | 199 Vision Amulet | **368 Virtue Boots** | 98 | 8.9% | 61% |
| 66 | 155 Alpha Boots | 175 Heaven's Armlet | 195 Heaven's Amulet | **363 War Boots** | 102 | 8.9% | 61% |
| 67 | 155 Alpha Boots | 175 Heaven's Armlet | 195 Heaven's Amulet | **366 Havoc Boots** | 113 | 7.9% | 62% |
| 68 | 163 Phoenix Armlet | 502 Silk Towel | 504 Emperor's Seal | **408 History Scroll** | 10 | 15.8% | 56% |
| 69 | 165 Demon Armlet | 502 Silk Towel | 504 Emperor's Seal | **413 Feoff Scroll** | 20 | 15.8% | 56% |
| 70 | 168 Thunder Armlet | 502 Silk Towel | 504 Emperor's Seal | **404 Tactical Scroll** | 20 | 15.8% | 56% |
| 71 | 172 Emperor Armlet | 194 Bliss Amulet | 502 Silk Towel | **370 Palisade Belt** | 54 | 12.9% | 58% |
| 72 | 173 Sage Armlet | 193 Sage Amulet | 502 Silk Towel | **371 Belvedere Belt** | 58 | 11.9% | 59% |
| 73 | 173 Sage Armlet | 194 Bliss Amulet | 502 Silk Towel | **369 Scabre Belt** | 60 | 11.9% | 59% |
| 74 | 173 Sage Armlet | 195 Heaven's Amulet | 502 Silk Towel | **373 Heartfire Belt** | 66 | 11.9% | 59% |
| 75 | 174 Bliss Armlet | 194 Bliss Amulet | 502 Silk Towel | **375 Ardent Belt** | 60 | 11.9% | 59% |
| 76 | 174 Bliss Armlet | 195 Heaven's Amulet | 502 Silk Towel | **374 Iron Will Belt** | 70 | 10.9% | 60% |
| 77 | 175 Heaven's Armlet | 194 Bliss Amulet | 502 Silk Towel | **376 Galvanic Belt** | 70 | 10.9% | 60% |
| 78 | 175 Heaven's Armlet | 195 Heaven's Amulet | 502 Silk Towel | **372 Enchanted Belt** | 80 | 10.9% | 60% |
| 79 | 176 Zero Armlet | 199 Vision Amulet | 504 Emperor's Seal | **427 Ferver Scroll** | 48 | 12.9% | 58% |
| 80 | 176 Zero Armlet | 200 Majestic Amulet | 504 Emperor's Seal | **425 Soul Scroll** | 70 | 10.9% | 60% |
| 81 | 176 Zero Armlet | 502 Silk Towel | 504 Emperor's Seal | **407 Turn Scroll** | 20 | 15.8% | 56% |
| 82 | 177 Dead Armlet | 199 Vision Amulet | 504 Emperor's Seal | **422 Insight Scroll** | 50 | 12.9% | 58% |
| 83 | 177 Dead Armlet | 200 Majestic Amulet | 504 Emperor's Seal | **414 Mana Scroll** | 80 | 10.9% | 60% |
| 84 | 177 Dead Armlet | 502 Silk Towel | 504 Emperor's Seal | **429 Trial Scroll** | 18 | 15.8% | 56% |
| 85 | 178 Ancient Armlet | 199 Vision Amulet | 504 Emperor's Seal | **403 Element Scroll** | 56 | 12.9% | 58% |
| 86 | 178 Ancient Armlet | 200 Majestic Amulet | 504 Emperor's Seal | **426 Sprint Scroll** | 80 | 10.9% | 60% |
| 87 | 178 Ancient Armlet | 502 Silk Towel | 504 Emperor's Seal | **410 Fiber Scroll** | 24 | 14.9% | 57% |
| 88 | 179 Vision Armlet | 198 Ancient Amulet | 504 Emperor's Seal | **417 Duty Scroll** | 36 | 13.9% | 58% |
| 89 | 179 Vision Armlet | 199 Vision Amulet | 504 Emperor's Seal | **423 Autumn Scroll** | 60 | 11.9% | 59% |
| 90 | 179 Vision Armlet | 200 Majestic Amulet | 504 Emperor's Seal | **416 Dutiful Scroll** | 90 | 9.9% | 60% |
| 91 | 179 Vision Armlet | 502 Silk Towel | 504 Emperor's Seal | **411 Far East Scroll** | 30 | 14.9% | 57% |
| 92 | 180 Majestic Armlet | 198 Ancient Amulet | 504 Emperor's Seal | **421 Heart Scroll** | 40 | 13.9% | 58% |
| 93 | 180 Majestic Armlet | 199 Vision Amulet | 504 Emperor's Seal | **432 Pith Scroll** | 60 | 11.9% | 59% |
| 94 | 180 Majestic Armlet | 200 Majestic Amulet | 504 Emperor's Seal | **419 Sire Scroll** | 120 | 6.9% | 62% |
| 95 | 180 Majestic Armlet | 502 Silk Towel | 504 Emperor's Seal | **428 Ardor Scroll** | 30 | 14.9% | 57% |
| 96 | 185 Demon Amulet | 331 Triton Claymore | 333 Sear Sword | **509 Next Claymore** | 90 | 9.9% | 75% |
| 97 | 189 Flame Amulet | 502 Silk Towel | 504 Emperor's Seal | **415 Western Scroll** | 30 | 14.9% | 57% |
| 98 | 190 Light Amulet | 502 Silk Towel | 504 Emperor's Seal | **420 Signory Scroll** | 40 | 13.9% | 58% |
| 99 | 190 Light Amulet | 502 Silk Towel | 504 Emperor's Seal | **433 Nature Scroll** | 40 | 13.9% | 58% |
| 100 | 193 Sage Amulet | 502 Silk Towel | 504 Emperor's Seal | **412 Morality Scroll** | 42 | 13.9% | 58% |
| 101 | 194 Bliss Amulet | 502 Silk Towel | 504 Emperor's Seal | **418 Rapture Scroll** | 84 | 9.9% | 60% |
| 102 | 195 Heaven's Amulet | 502 Silk Towel | 504 Emperor's Seal | **424 Peace Scroll** | 90 | 9.9% | 60% |
| 103 | 196 Zero Amulet | 502 Silk Towel | 504 Emperor's Seal | **409 Ethics Scroll** | 10 | 15.8% | 56% |
| 104 | 197 Dead Amulet | 502 Silk Towel | 504 Emperor's Seal | **405 Royalty Scroll** | 10 | 15.8% | 56% |
| 105 | 198 Ancient Amulet | 502 Silk Towel | 504 Emperor's Seal | **431 Dogma Scroll** | 10 | 15.8% | 56% |
| 106 | 199 Vision Amulet | 502 Silk Towel | 504 Emperor's Seal | **430 Chastity Scroll** | 12 | 15.8% | 56% |
| 107 | 200 Majestic Amulet | 502 Silk Towel | 504 Emperor's Seal | **406 A-Scroll** | 16 | 15.8% | 56% |
| 108 | 303 Shadow Spear | 304 Lunar Pike | 420 Signory Scroll | **508 Heaven's Sword** | 125 | 6.9% | 78% |
| 109 | 306 Slayer Spear | 419 Sire Scroll | 504 Emperor's Seal | **511 Tragedy Blade** | 130 | 5.9% | 79% |
| 110 | 313 Piercing Pike | 336 Carmine Axe | 516 Heaven's Sword | **503 Heaven's Pike** | 135 | 5.9% | 79% |
| 111 | 314 Dawn Pike | 339 Sage Sword | 404 Tactical Scroll | **510 Swift Falchion** | 110 | 7.9% | 77% |
| 112 | 316 Godendag Pike | 419 Sire Scroll | 504 Emperor's Seal | **513 Heaven's Sabre** | 115 | 7.9% | 77% |
| 113 | 334 Fervor Claymore | 419 Sire Scroll | 504 Emperor's Seal | **512 Canon Claymore** | 95 | 8.9% | 76% |
| 114 | 334 Fervor Claymore | 419 Sire Scroll | 504 Emperor's Seal | **514 Sky Claymore** | 95 | 8.9% | 76% |
| 115 | 335 Saint Claymore | 338 Fierce Sword | 433 Nature Scroll | **516 Heaven's Sword** | 90 | 9.9% | 75% |
| 116 | 341 Flatbow | 342 Longbow | 343 Mongol Bow | **515 Sky Sword** | 92 | 9.9% | 75% |
| 117 | 343 Mongol Bow | 349 Lucent Crown | 354 Brute Armour | **507 Heaven's Boots** | 99 | 8.9% | 76% |
| 118 | 351 Mystic Crown | 355 Bliss Armour | 502 Silk Towel | **517 Heaven's Crown** | 100 | 8.9% | 76% |
| 119 | 354 Brute Armour | 372 Enchanted Belt | 502 Silk Towel | **518 Heaven's Belt** | 80 | 10.9% | 75% |
| 120 | 355 Bliss Armour | 363 War Boots | 372 Enchanted Belt | **505 Heaven's Armour** | 145 | 5.0% | 80% |
| 121 | 377 Palomino Rouncy | 502 Silk Towel | 504 Emperor's Seal | **380 Dun Sumpter** | 16 | 15.8% | 56% |
| 122 | 378 Gray Garron | 502 Silk Towel | 504 Emperor's Seal | **402 White Destrier** | 32 | 14.9% | 57% |
| 123 | 379 Black Barb | 383 Black Garron | 393 Dark Clydesdale | **506 Great Stallion** | 100 | 8.9% | 76% |
| 124 | 379 Black Barb | 502 Silk Towel | 504 Emperor's Seal | **393 Dark Clydesdale** | 64 | 11.9% | 59% |
| 125 | 380 Dun Sumpter | 502 Silk Towel | 504 Emperor's Seal | **381 Light Palfrey** | 20 | 15.8% | 56% |
| 126 | 381 Light Palfrey | 502 Silk Towel | 504 Emperor's Seal | **394 Chestnut Garron** | 22 | 14.9% | 57% |
| 127 | 382 Gray Clydesdale | 502 Silk Towel | 504 Emperor's Seal | **385 Black Courser** | 56 | 12.9% | 58% |
| 128 | 384 White Barb | 502 Silk Towel | 504 Emperor's Seal | **401 Light Barb** | 60 | 11.9% | 59% |
| 129 | 385 Black Courser | 502 Silk Towel | 504 Emperor's Seal | **384 White Barb** | 56 | 12.9% | 58% |
| 130 | 386 Dark Palfrey | 502 Silk Towel | 504 Emperor's Seal | **391 Gray Sumpter** | 32 | 14.9% | 57% |
| 131 | 387 Dark Sumpter | 502 Silk Towel | 504 Emperor's Seal | **379 Black Barb** | 62 | 11.9% | 59% |
| 132 | 388 Black Destrier | 502 Silk Towel | 504 Emperor's Seal | **392 White Garron** | 42 | 13.9% | 58% |
| 133 | 389 Black Palfrey | 502 Silk Towel | 504 Emperor's Seal | **388 Black Destrier** | 40 | 13.9% | 58% |
| 134 | 390 Chestnut Rouncy | 502 Silk Towel | 504 Emperor's Seal | **378 Gray Garron** | 30 | 14.9% | 57% |
| 135 | 391 Gray Sumpter | 502 Silk Towel | 504 Emperor's Seal | **389 Black Palfrey** | 36 | 13.9% | 58% |
| 136 | 392 White Garron | 502 Silk Towel | 504 Emperor's Seal | **382 Gray Clydesdale** | 52 | 12.9% | 58% |
| 137 | 393 Dark Clydesdale | 502 Silk Towel | 504 Emperor's Seal | **383 Black Garron** | 70 | 10.9% | 60% |
| 138 | 394 Chestnut Garron | 502 Silk Towel | 504 Emperor's Seal | **396 Light Courser** | 24 | 14.9% | 57% |
| 139 | 395 Dark Courser | 502 Silk Towel | 504 Emperor's Seal | **397 White Courser** | 26 | 14.9% | 57% |
| 140 | 396 Light Courser | 502 Silk Towel | 504 Emperor's Seal | **395 Dark Courser** | 24 | 14.9% | 57% |
| 141 | 397 White Courser | 502 Silk Towel | 504 Emperor's Seal | **398 Chestnut Barb** | 28 | 14.9% | 57% |
| 142 | 398 Chestnut Barb | 502 Silk Towel | 504 Emperor's Seal | **399 Dark Barb** | 30 | 14.9% | 57% |
| 143 | 399 Dark Barb | 502 Silk Towel | 504 Emperor's Seal | **390 Chestnut Rouncy** | 30 | 14.9% | 57% |
| 144 | 401 Light Barb | 502 Silk Towel | 504 Emperor's Seal | **387 Dark Sumpter** | 60 | 11.9% | 59% |
| 145 | 402 White Destrier | 502 Silk Towel | 504 Emperor's Seal | **386 Dark Palfrey** | 32 | 14.9% | 57% |
| 146 | 419 Sire Scroll | 424 Peace Scroll | 504 Emperor's Seal | **501 Book of Valor** | 130 | 5.9% | 79% |
| 147 | 419 Sire Scroll | 502 Silk Towel | 504 Emperor's Seal | **400 Albino Rouncy** | 44 | 13.9% | 58% |
| 148 | 432 Pith Scroll | 502 Silk Towel | 504 Emperor's Seal | **377 Palomino Rouncy** | 16 | 15.8% | 56% |

---

## 3. Формули

### 3.1 Ціна `e.b(z)` (e.java 2817-2830)
```
id<100   : ae.y[id-1]
101..299 : kibo.col6 + ATK*100 + DEF*100 + (HP/5)*100 + (MP/3)*100
301..499 : k = (sungbo.col6==0) ? 800 : 400;  ATK*k + DEF*k + (HP/5)*k + (MP/3)*k
>=500    : shinki.col6 (фіксована)
```
Ціна рахується з поточних статів, тому заточка підвищує ціну Normal/Special.

### 3.2 Купівля `e.bc()` (2832-2883)
1. Якщо `cz.E < price` → «Not enough Gold» (fK[20]=4).
2. Consumable: до стека того ж id (максимум 5; на 5 → «You cannot buy anymore», fK[20]=5) або в перший вільний слот пояса (усі 5 зайняті → fK[20]=6).
3. Предмет: копіюється в перший вільний `Y[]`, клітинка магазину очищується. Повний рюкзак → fK[20]=6.
4. Після успіху: `E -= price`, автосейв.

### 3.3 Продаж `e.bd()` (2885-2905)
`E += b(z)/2` за 1 шт. (consumable − 1 зі стека), потім автосейв.

### 3.4 Асортимент (`ag.ax()` 3362-3375, `ag.ay()` 3377-3398, `I()` 3414-3422)
- `fL[0..7]` = {1,2,3,4,5,6,10,11}.
- 17 разів: `id = 101 + 5*rand(0..19) + I(rand(0..99))`, далі bubble sort і `fL[8+b]=J(id)`.

| Lv гравця | тір0 (Lv1) | тір1 (Lv10) | тір2 (Lv25) | тір3 (Lv45) | тір4 (Lv70) |
|---|---|---|---|---|---|
| 1–9 | 80% | 20% | – | – | – |
| 10–24 | 40% | 40% | 20% | – | – |
| 25–44 | 30% | 30% | 30% | 10% | – |
| 45–69 | 5% | 25% | 25% | 25% | 20% |
| ≥70 | – | – | 33% | 34% | 33% |

`J(id)` (3424-3457):
- kibo: `col3 + C(col4)`;
- sungbo: стати як є;
- **shinki: баг.** Рядок береться як `id-301` замість `id-501`, `d.a()` ловить виняток → **0 статів**.

`C(n)` = рівномірне 0..n−1 (ag.java 2735-2741). Дроп і нагороди йдуть через `k(id,1)` і дають `col3 + C(col4+1)`; `k(id,0)` дає рівно base.

### 3.5 Бонуси `ag.O()` (1759-1773)
```
s,t,u,v = Σ X[i].(ATK,DEF,HP,MP)
w = m+s,  x = n+t,  y = p = o+u,  z = r = q+v      ← O() також повністю відновлює HP/MP
```

### 3.6 Enchant (`be()` 2907-2936, `aV()` 2396-2451, `c(boolean)` 1912-2111, `aQ()` 2113-2135, `a(z,n)` 2628-2668)
```
eligible 100<id<500;  maxE = kibo.col5 | sungbo.col6 (0 → неможливо);  f>=maxE → "Fully enchanted"
fee = ATK*100 + DEF*100 + HP*100/5 + MP*100/3       (fee>gold → "Not enough Gold")
gold -= fee (завжди)
success% = {100,90,80,70,60,45,30,10,1}[f]
  +1 рівень; кожен ненульовий стат += max(1, round(stat*j/1000)), j∈{50,60,70,80,90,100}, P={30,25,20,15,9,2}/101
fail: destroy% = {0,10,20,40,50,60,70,80,90}[f] + 1  → предмет знищено
автосейв
```
Заточувати можна лише рюкзак: `fK[27]` ніде не виставляється в 1.

### 3.7 Combine (`aX()` 2568-2626, `c(boolean)` 1912-2111)
```
3 клітинки рюкзака з id>100; sort; sumF = Σ f
немає рецепта → "Not possible."
res = result[start + C(dup)];  fQ = J(res)          ← Rare = 0 статів (баг)
fee = b(fQ)/4;  req = sungbo.col8 | shinki.col7;  p = (200-req)/12
success, якщо p >= C(101) → fQ = a(fQ, sumF/3); видалити 3 інгредієнти; результат у клітинку fO[2]
fail: q = (100-p)*10/(res<500 ? 15 : 12); якщо q >= C(101) → втратити fO[C(3)]
gold -= fee (і при успіху, і при провалі); автосейв
```

### 3.8 Атрибути (e.java 882-907)
`cM[1]`: 0 → `o+=5`, 1 → `q+=3`, 2 → `m++`, 3 → `n++`, потім `J--`. Рядки на екрані йдуть як `{o,q,m,n}` (1430), бонуси — `{u,v,s,t}` (1455).

### 3.9 Досвід і рівень
- `c.h()` (c.java 1616-1639): `i = dY << 1 + (ep^1)`. У Java `+` має вищий пріоритет, тож це `dY << (1+(ep^1))`: ×2 на Normal, ×4 на Hard.
- Там же `cz.F += dY` (Fame).
- Level-up (`e.n()` 2938-2973, `ag.H()` 3081-3097): `l++`, `J += 3`.

### 3.10 Дроп (`ar.P()` 2055-2079; спавн `ar.a(int,h)` 2017-2052; підбір `ar.i()` 1713-1728)
| cls | Хто (ar.ab() 1663-1690, 2010) | предмет | з них екіп. |
|---|---|---|---|
| 0 | рядовий (`h≥200`) | 5% | 10% |
| 1 | генерал (`cr==0`) | 10% | 30% |
| 2 | генерал, `cr!=0` **[guess: бос]** | 20% | 60% |
| 3 | руйнівний об'єкт | 5% | 1% |
| 4 | нагорода Visiting | 100% | 100% |

- Якщо предмет не випав: 25% шанс на золото, 20 або 40 (ar.java 2076).
- Тір екіп. за порогами `{69,44,24,9,0}`, кумулятивні таблиці `{0,0,33,77,100}` / `{5,30,55,80,100}` / `{30,60,90,100}` / `{40,80,100}` / `{80,100}`.
- id = `101 + tier + 5*C(20)`.
- Предмет лежить 75 тіків, радіус підбору 20 px.

### 3.11 Нагороди місії (`c.d(int)` 1516-1607)
- Успіх: `cz.g[dz.a−1] += 5` (кап 100), виставляються біти `dx`/`dy`.
- Кінець глави:
  - предмет `ef`: 502 (кінцівка 2) або з шансом 10% Normal тіру `min(Lv/20,4)`;
  - відкриття прихованої місії.
- Завжди: `E += h*150*(Hard?2:1)`, `ay()`, `dj=0`, автосейв.

### 3.12 MP скілу (`ar.e()` 743-756)
`base[id−12] + (W−1)*inc[id−12]`, де:
- base = {5,6,7,10,15,7,10,10,8,9,10,5,6,7,9,12,20,20,20};
- inc = {3,4,5,3,4,3,3,5,3,4,5,3,4,5,5,6,5,5,5}.

---

## 4. Сейв-дані (RMS)

### 4.1 Сховища
| Store | Розмір | Вміст | Код |
|---|---|---|---|
| `gamevil_pow_data` (#1) | 965 Б (буфер 2000) | прогрес | `ag.ar()` 2871-2961, `ag.U()` 2126-2214, `ag.aq()` 2862-2869 |
| `gamevil_pow_env` (#1) | 2 Б | `[0]` гучність `dg` (0..100, крок 25); `[1]` швидкість `dh` 0..4 (`ae.aQ`={250,180,120,90,50} мс) | `ag.G()/H()` 1174-1201 |
| `gamevil_pow_regist` (#1) | 28 Б | `[0..11]` пароль `as.l`, `[12..27]` UserID `as.m` | `m.b()/c()/d()` 276-318 |

### 4.2 `gamevil_pow_data` (LE; z = 11 Б {u16 id, u16 ATK, u16 DEF, u16 HP, u16 MP, u8 enchant})
| off | size | поле | значення |
|---|---|---|---|
| 0 | 2 | length | 965 |
| 2 | 8 | `cz.k` | ім'я, доповнене пробілами |
| 10 | 8 | — | не пишеться |
| 18 | 1 | `dj` | «посеред місії» (Continue відновлює місію, e.java 856-866) |
| 19 | 3 | `dk,dm,do` | лорд, місія, етап |
| 22 | 8 | `dw` | відкриті лорди (старт 35113052110447, ag.java 3225) |
| 30 | 8 | `dx` | лорди з завершеними місіями |
| 38 | 32 | `dy[8]` | біти місій (нижні 32 біти кожного) |
| 70 | 4 | `dY` | накопичений exp/fame |
| 74 | 4 | `ed` | кінцівки |
| 78 | 88 | `fn[0..1][44]` | запрошення генералів (id, стосунки), пари |
| 166 | 1 | `fo` | кількість |
| 167 | 275 | `fL[25]` | **асортимент Blacksmith** |
| 442 | 1 | `cq` | глава |
| 443 | 4 | x,y (u16) | позиція, вирівняна до 7×7 |
| 447 | 22 | `cz.g[22]` | стосунки 0..100 **[medium: лорди/сторони]** |
| 469 | 2 | `cz.h,i` | маршрут/оцінка кінцівки |
| 471 | 1 | `cz.l` | **рівень, 1 signed байт → Lv≥128 ламається** (ag.java 2171, 2908, 2246) |
| 472 | 12 | `m,n,o,p,q,r` | база ATK, DEF, HPmax, HP, MPmax, MP |
| 484 | 12 | `E,F,G` | золото, Fame, exp |
| 496 | 4 | `H,J` | вбивства, очки |
| 500 | 1 | `S` | Visiting дозволено |
| 501 | 24 | `V[5], W[19]` | клавіші скілів, рівні |
| 525 | 99 | `X[9]` | екіпіровка |
| 624 | 275 | `Y[25]` | рюкзак |
| 899 | 15 | `Z[5]` | пояс {u16 id, u8 count} |
| 914 | 3 | `aa[2], aB` | швидкі слоти, герой |
| 917 | 8 | `dW0−dV`, `eo` | час гри **[medium]**, мітка старту **[guess]** |
| 925 | 2 | `fR,fS` | фази синхронізації GL (`fS≠0` блокує Continue, e.java 843; у білді завжди 0) |
| 927 | 2 | `dH, ep` | лічильник **[guess]**, складність |
| 929 | 16 | — | нулі |
| 945 | 4 | `fq` | генерал, якому −5 стосунків при смерті **[medium]** (c.java 1757-1758) |
| 949 | 16 | — | 4×u32 нулі |

Локально **не** зберігаються: Warehouse і Safe (лише на сервері), прапорець звуку `df`.

### 4.3 Коли гра зберігає
- Нова гра (l.java 145).
- Кінець місії (c.java 1606), провал місії (c.java 1762).
- Пауза → Save (ar.java 202-207), лише якщо на карті немає ворогів.
- Екран Etc Save (e.java 917).
- Вихід з екранів 14–18 (1004-1012) і зі Skills (1096).
- Buy (2881), Sell (2904), Enchant/Combine.
- Visiting (l.java 293).
- Операції GL (`as.O()` 1064-1067 та 618/679/748/980).

### 4.4 Порівняння з портом
`game_state.gd` (261-297) зберігає лише `hero_index`, `difficulty_index`, `player_name`.

Немає: прогресу, економіки, предметів, місій, генералів, опцій, версії схеми, автосейву.

Рекомендація:
- JSON-дзеркало таблиці 4.2, плюс `warehouse[100]`, `safe_gold`, `market{}` і `schema_version`;
- опції — в окремому `env.json`;
- опційно — імпорт 965-байтного RMS-дампу.

---

## 5. Gamevil Live

### 5.1 Транспорт
- **Підключення:** `socket://bk:bl`.
  - `bk` = JAD `GAMEVIL_SERVER`, за замовчуванням `ur.gamevil.net`; у цій зламаній збірці — `gamehub.pro`.
  - `bl` = `GAMEVIL_PORT`, 28230 (ag.java 604-613; v.java 57-70).
- **Кадр** (u.java 73-99, b.java 30-46): `[u16 LE totalLen (з цими 2 Б)][payload]`.
  - Запит: `[u16 opcode][поля]` (as.java 463).
  - Відповідь: `[u16 opcode+1][u8 status (1=OK)][поля]`.
  - Числа LE, рядки — фіксовані поля з нулями.
- **Таймаут:** 30 с або BACK (as.java 415-438). Одночасно йде лише один запит.
- **[medium-high]** Обробник помилок отримує `gr`, але `gr` ніде не присвоюється статусом, а `m()` чекає `gr==1`. Найімовірніше, це артефакт декомпілятора: status-байт = `gr`, від'ємні значення — коди помилок.
- `u.e={0,1,117,126}` не використовується. Є відлагоджувальні `SEND/RECV DATA` у консоль.

### 5.2 Опкоди
| Req→Resp | Призначення | Запит | Відповідь |
|---|---|---|---|
| 530→531 | Логін/реєстрація | UserID[12], пароль[16], `"1501"`[4], u32 `gn`, u32 `go` | 2 Б, u8: 0 = зареєстровано (msg 48), 2 = Welcome back (44); помилки 1 (43), 3 (47); ID і пароль пишуться в RMS |
| 512→513 | Статус | — | u8 ht15 (оголошення), ht14 (продані лоти), ht13 (подарунки), u8 ?, 5×u32 ?, u8 **ht4 = податок %**, u8 ht5 **[guess: gift tax]** |
| 516→517 | Оголошення/рейтинг **[guess]** | те саме тіло, що 256 (fall-through) | 4×str[16]; u8 1 = ще є |
| 518→519 | Sale List | — | u8 n; {u16 id, u8 f, u32 price} |
| 520→521 | Gift List | — | u8 n≤5; {str[8] від кого, u16 id, u8 f, 4×u16}; u8 ht13 |
| 258→259 | Exp/Fame із сервера | — | u32 fame, u32 exp → `F+=`, `H(exp)`, fR=1, сейв |
| 260→261 | ACK | — | fR--; діалог 41 або 20 |
| 768→769 | Синхронізація інвентаря | u32 gold; u8 n; {u16 id, u16 serial, u8 f, 4×u16} | u32 safe `gy`; u8 ht6; склад {u16 id, u16 serial, u8 f, 4×u16} |
| 832→833 | Safe | u8 напрям (`ht15^1`), u32 сума | u32 E, u32 gy |
| 816→817 | Warehouse move | u8 ht7 (0 рюкзак→склад, 1 навпаки), u16 serial | u16 новий serial |
| 784→785 | Лоти за заточкою | u8 cat+1 (далі сміття fall-through) | 10×u8 → hu[15..6] |
| 786→787 | Сторінка лотів | u8 cat+1, u8 kind+1, u8 enchant, u32 курсор, u8, u16, u32 | n×{u32 listingId, u16 id, u32 price, u8 f, 4×u16} |
| 788→789 | Купити | u32 listingId, u8 dest, u16, u32 | u16 serial, u32 E, u32 gy |
| 800→801 | Виставити | u8 джерело, u16 serial, u32 ціна | msg 36 |
| 802→803 | Price Info | u8 cat+1, u8 kind+1, u32, u8 | ≤20×{u16 id, u32 price, u8 f, 4×u16} |
| 864→865 | Мої лоти | — | ≤20×{u32 id, u16 item, u32 price, u8 f, 4×u16} |
| 866→867 | Скасувати лот | u32 listingId, u8 dest | u16 serial; msg 40 |
| 256→257 | Save User Data | F, G, l, aB, тип зброї, m/n/o/q/J, s/t/u/v, dy[8], скіли {код `gG`, рівень, призначено}, ім'я[8], S, fn, dw, cq, g[22], h, i, ed | msg 18 |
| 262→263 | Load User Data | — | те саме → перезапис персонажа, сейв, msg 19 |

Коди помилок відображаються як `gamestr[n+15]` (`as.b()` 301-353, `l.d()` 506-598):

| Код | Повідомлення |
|---|---|
| −1 | Anonymous |
| −2 | number not available |
| −4 | No saved data |
| −11 | No more data / no items |
| −12 | sold out |
| −13 | canceled |
| −15 | need warehouse space |
| −16 | max 5 sales |
| −18 | gold out of range |
| −20 | network failed |
| −22 | can't give to yourself |
| −23 | monthly limit |
| −26 | abnormal data |
| −49 | «You can't use the ID.» |

### 5.3 Ланцюжок після входу (as.java 210-299, 1697-1756)
```
Connect? → 530 → 512 → [ht15] 516… → [ht14] 518 Sale List → [ht13] 520 Gift List
 → [fR==0] 258 → 260 | [fR!=0] 260 → 768 → меню GAMEVIL LIVE
BACK → as.ba(): bV=2, cM=[0,2]
```
- **Екрани `as.ho`** (`m.a()` 4-56): 1 список, 2 Safe, 3 ввід суми, 4 Backpack/Warehouse, 5 категорії, 6 види, 7 заточки, 8 лоти, 9 ціна, 10 Cancel, 11 Sale/Gift List, 12 очікування, 13 реєстрація.
- **Ввід:** `as.hp` → `t()` (1211-1269).

### 5.4 Що залежало від сервера
- Усе меню GL.
- Special/Rare, крім Combine.
- **504** (через це 62 рецепти і «усі генерали» офлайн недосяжні).
- Warehouse (+100) і Safe.
- Серверні Exp/Fame, бекап персонажа.

### 5.5 Офлайн-стратегія (рекомендація)
**«Local Live»:** меню й UX GL лишаються, сервер замінює інтерфейс `LiveBackend` з реалізацією `OfflineLiveBackend`. Дані бекенду лежать у сейві.
1. Без логіну та реєстрації (або одноразове «Offline mode»).
2. **Warehouse** (100) і **Safe** — локальні сховища, логіка як у 816/832.
3. **Buy** — NPC-ринок на seeded RNG, оновлення після кожної місії.
   - Структура як в оригіналі: категорія / kind (`gF`) / заточка / сторінки по 20.
   - Ціна = `b(z)` × коефіцієнт (Normal 1.2–2.0, Special 1.0–1.6, Rare 1.0–1.3 від `col6`).
   - **Обов'язково** продавати 502 і 504.
4. **Sell / Cancel** — до 5 лотів.
   - Після місії лот продається з імовірністю, що спадає з ростом `ціна / b(z)`.
   - Виручка мінус податок (10%, бо в Java `ht[4]` приходив із сервера) іде в Safe.
   - Проданий лот показується в Sale List.
5. Gift List — подарунки за глави, або вимкнути.
6. Management → локальний бекап-слот без предметів і золота, або приховати.
7. Exp/Fame із сервера (258–261) і оголошення (516) — вимкнути.

Мінімальний варіант: прибрати GL і видавати 504/Special/Rare іншими каналами. Справжній сервер не рекомендую: серверна логіка невідома.

---

## 6. Карта Java → відповідальність

### 6.1 Класи / методи
| Java (рядки) | Відповідальність |
|---|---|
| `n` (n.java) | персонаж `cz` |
| `z` | інстанс предмета |
| `d` (7-48) | колонкова таблиця .arr |
| `ai/t/ao` → `cX/cY/cZ` | дескриптори Normal/Special/Rare (`e.e()` 3465-3531) |
| `ag.az()` 3400-3412 | завантаження таблиць предметів |
| `ag.k()` 3286-3360 | видати предмет/консумабл/золото |
| `ag.J()` 3424-3457 | згенерувати інстанс (магазин/Combine) |
| `ag.ax/ay/I` 3362-3422 | асортимент Blacksmith |
| `ag.O()` 1759-1773 | бонуси й підсумкові стати |
| `ag.g/m/l` 867, 1401, 1383 | тип / reqLevel / опис спецпредметів |
| `ag.b(int,…)` 1293-1352, `e.a(z,…)` 3083-3206, `e.k()` 1595-1630 | бігучий рядок опису |
| `ag.a(z,z)` 2384, `ag.ag()` 2372, `ag.L()` 3530 | обмін, ущільнення, пошук |
| `ag.ar()/U()/aq()` 2871 / 2126 / 2862 | сейв / лоад / перевірка наявності |
| `ag.G()/H()` 1174-1201 | env |
| `ag.av()`+3221-3273, `ag.aw()` 3275 | нова гра |
| `ag.H(int)` 3081-3097 | застосувати exp |
| `ag.af()` 2321-2343 | рядки uimenu |
| `e.b()` 688-1000 | OK у меню, атрибути, екіп |
| `e.aF()` 1002-1109 | BACK + автосейв |
| `e.O/P/n/Q/d` 1429 / 1523 / 1632 / 1656 / 3022 | Attributes / Skills / Gear / Inventory / Assign Items |
| `e.aY/aZ/ba` 2694-2772 | ініціалізація сітки магазину |
| `e.aW()` 2453-2566 | ввід магазину |
| `e.bc/bd/be/aQ/a(z,n)` | купівля / продаж / перевірка / кидок заточки / приріст |
| `e.aX/b/S` 2568-2692 | Combine |
| `e.c(boolean)` 1912-2111 | підтвердження + анімація |
| `e.aV()` 2396-2451 | діалоги магазину |
| `e.b(z)/c(int)/m()` 2817 / 2774 / 2803 | ціна / назва / лічильники |
| `e.n()/p()` 2938 / 3547 | level-up / exp.arr |
| `e.o()` 3208-3282 | нагороди Visiting |
| `c.d(int)` 1516-1607 | кінець місії |
| `ar.P/a(int,h)/i/ab` | дроп |
| `ar.e()` 743, `ar.c()` 249 | MP скілу, швидкий слот |
| `l.d/e/a` 506 / 600 / 469 | діалоги |
| `as` (1-2165) | Gamevil Live |
| `m` (1-379) | рендер GL, RMS regist |
| `v/u/b/ab/s` | мережевий потік / writer / reader / парсер / callback |
| `at` | текстовий ввід UserID |

### 6.2 Ключові глобали
| Глобал | Значення |
|---|---|
| `cz.k,l` | ім'я, рівень |
| `cz.m,n,o,p,q,r` | база ATK, DEF, HPmax, HP, MPmax, MP |
| `cz.s,t,u,v` / `cz.w,x,y,z` | бонуси / підсумок |
| `cz.E,F,G,H,J` | золото, Fame, exp, вбивства, очки |
| `cz.K` | тип зброї |
| `cz.S` | Visiting |
| `cz.V[5], W[19]` | клавіші скілів (id 12..30), рівні |
| `cz.X[9],Y[25],Z[5],aa[2]` | екіп, рюкзак, пояс, швидкі слоти |
| `cz.aB, g[22], h, i` | герой, стосунки, кінцівка |
| `ag.fL[25]` | асортимент |
| `ag.fK[32]` | [0] режим, [3] видимі рядки, [4] усього рядків, [8] скрол, [9] колонка, [10] рядок, [14] режим ціни, [16] к-сть у рюкзаку, [17] у поясі, [18] курсор, [19] id під курсором, [20] код діалогу, [21] плата, [22] maxE/статус Combine, [23] результат, [24..25] іскра, [26] кадр анімації, [27] режим екіп. (завжди 0), [31] втрачений інгредієнт |
| `ag.fO[4], fP[3], fQ, fN` | вибір Combine, підсвітка, результат, `itemReinforce.png` |
| `ag.bH[3], cU/cV/cW` | таблиці / сирі байти |
| `ag.ct[0..3]` | tool / kibo / sungbo / shinki (imgui 48, 21, 46, 43) |
| `ag.ct[32], [39], [37..38], [19..20]` | gold, ui_equipbox, skill/skillgray, цифри |
| `ag.ep` | складність (0 Hard) |
| `ag.dg, dh, df` | гучність, швидкість, звук |
| `ag.fR, fS` | синхронізація GL |
| `ag.bi` | cheat |
| `as.gw/gx, gv, gy` | склад+serial'и, serial'и рюкзака, Safe |
| `as.gz/gA/gB/gC` | лоти, id, ціни, відправники |
| `as.gF[3][20]` | представники kind для GL-Buy |
| `as.gG[19]` | мапа кодів скілів |
| `as.gP,gQ,gR,gS,gT` | категорія, kind, заточка, сторінка, напрям |
| `as.ht[16]` | [4] податок, [5] gift tax, [6] к-сть на складі, [7] джерело, [13..15] прапорці |
| `as.hu, hv` | лоти по заточці; числовий ввід |
| `as.ho, hp, hn, hl, hm` | екран, ввід, заголовок, gamestr 2..13, gamestr 15..64 |
| `as.l, m, gn, go, gq, gp, gr` | пароль, ID, сесія, опкоди, статус |

---

## 7. Розбіжності поточного порту
1. Blacksmith: `game_menu.gd` 37 і `submenu_config.gd` 8 мають «Buy/Sell/Cancel Sell». Має бути **Buy / Sell / Enchant / Combine**.
2. Management без **Assign Items** (`game_menu.gd` 40, `submenu_config.gd` 11).
3. ETC = Save/Load (`game_menu.gd` 41, 276-284; `submenu_config.gd` 12). У Java це **Options / Help** і автосейв; ігрового «Load» не існує.
4. GL = «Coming Soon» (`game_menu.gd` 38, 268-270).
5. Дії Blacksmith і Management ведуть у `_show_coming_soon()` (`game_menu.gd` 266-275). Немає жодного екрана магазину, Gear, Inventory, Skills, Assign Items.
6. У `game_state.gd` (25-34) немає економічного стану; немає бази предметів і завантажувача .arr/.bin.
7. Сейв — 3 поля без версії та автосейву (`game_state.gd` 261-297).
8. `stats_screen.gd`:
   - порядок Atk/Def/HP/MP (рядки 7-8), а в Java **HP/MP/ATK/DEF**;
   - «Lv.1» захардкоджено (46);
   - немає +бонусів екіпіровки;
   - немає діалогу Yes/No зі скиданням;
   - не перевикористовується для level-up у Management.
9. `game_state.gd` 29-32: дефолти 1/1/5/3 виглядають як прирости. Справжня база 5/4/30/10 — у `main.gd` 19, там вона правильна.
10. Хибні документи:
    - `BLACKSMITH_SPEC.md` описує GL Trade як Blacksmith;
    - `DESIGN.md` 229, 368, 382-388;
    - `JAVA_REFERENCE.md` §1 (формат .scr), §7b (підписи меню), «as — сейв»;
    - `GAME_MENU_SPEC.md` §5 (ETC, Management).
11. `uimenu_strings.txt` і `gamestr_strings_full.txt` обрізані.
12. У копії немає PNG магазину та інвентаря: kibo, sungbo, shinki, tool, gold, itemReinforce, ui_equipbox, ui_level, ui_abbox, skill, skillgray, number*, netLoading0/1.
13. Щоб `.arr/.bin/.scr` читалися в експортованій збірці, їх треба додати в export-фільтр не-ресурсних файлів.

---

## 8. Невідоме / впевненість
| # | Питання | Впевненість |
|---|---|---|
| 1 | Rare з Combine отримує 0 статів (`J()` id−301) | висока, що так у байткоді; рекомендую виправити з прапорцем сумісності |
| 2 | status-байт = `gr` | medium-high |
| 3 | 516/517 = оголошення/рейтинг | low-medium |
| 4 | Поля 513, `ht[5]` = gift tax | low |
| 5 | Напрям Safe (`ht15==0`: зі Safe; `==1`: у Safe) | висока (as.java 1902-1910) |
| 6 | `cz.X[i]=null` при провалі (l.java 755) — баг або артефакт | medium; у порті очищати слот |
| 7 | Рівень 1 signed байт | висока |
| 8 | Податок продажу GL, ціни ринку | невідомо, потрібне дизайн-рішення |
| 9 | Кінцівка 2 → 502, кінцівка 3 потребує 502 (назви) | medium |
| 10 | Семантика `cz.g[22]`, `fq`, `dH`, `eo`, часу гри | medium/low |
| 11 | drop cls 2 = бос | guess |
| 12 | Відправка Gift у клієнті відсутня | висока |
| 13 | GL Save User Data без золота/предметів | висока |
| 14 | Заголовок exp.arr | невідомо, неважливо |

---

## 9. План порту (у порядку залежностей)
| # | Задача | Java refs | Done-критерії | Год |
|---|---|---|---|---|
| T1 | Перегенерувати .scr-рядки за count-заголовком; виправити документи | al.java 11-29; §0, §7 | uimenu = 60, gamestr = 71; документи узгоджені з §0 | 2 |
| T2 | **ItemDB**: kibo/sungbo/shinki/consumables/mixing → ресурс або рантайм-парсер (LE); export-фільтр | d.java; e.e(); §2 | 266 предметів і 149 рецептів = таблиці звіту (автотест) | 4 |
| T3 | Модель предметів/інвентаря: ItemInstance, рюкзак 25 (ущільнення), пояс 5×5, екіп 9 (`ae.aE`), `give_item`≡`k()`, `make_item`≡`J()`, ціна, reqLv, `O()` | ag 3286-3457, 1759, 867, 1401; e 2817 | юніт-тести §3.1/3.4/3.5 | 5 |
| T4 | PlayerState: рівень/exp/fame/gold/база/очки/скіли/швидкі слоти; ініціалізація нової гри | ag 3221-3284; e 2938, 3547 | нова гра як у Java; level-up +3 | 3 |
| T5 | Save v2: JSON-дзеркало §4.2 + версія + env; автосейви §4.3; міграція; опц. імпорт RMS | ag 2126-2214, 2871-2961, 1174-1201 | roundtrip без втрат; Continue; Lv>127 працює | 6 |
| T6 | Attributes: порядок HP/MP/ATK/DEF, бонуси, Lv/Fame, Yes/No зі скиданням | e 882-907, 1429-1469; l 193-200, 653-656 | поведінка як у Java | 3 |
| T7 | Gear + Inventory: лялька, сітка 5×5 зі скролом, опис, перевірка рівня, еліксири, зняття | e 758-764, 949-987, 1632-1692; ag 1293-1352 | стати оновлюються; 502/504 не вдягаються | 8 |
| T8 | Assign Items + Skills | e 3022-3058, 1523-1593, 922-947; ar 249-260, 743-756 | призначення працює в бою | 6 |
| T9 | Каркас Blacksmith (4 пункти, сітка, рамка золота, діалоги `aV`) | uimenu[39]; e 2694-2754, 2396-2451, 1804-1902 | 4 екрани, навігація як у Java | 5 |
| T10 | Buy/Sell + рестік `ax/ay/I` | e 2832-2905; ag 3362-3422; c 1604 | розподіл тірів (seeded-тест); ціни, ½ продажу | 4 |
| T11 | Enchant | e 2907-2936, 2113-2135, 2628-2668, 1912-2111 | Монте-Карло ±1% | 4 |
| T12 | Combine (+ рішення щодо бага Rare) | e 2568-2692, 1912-2111 | 149 рецептів; шанси за таблицею | 5 |
| T13 | Лут і нагороди (дроп, золото 20/40, нагорода місії, втрата екіп.) | ar 2017-2079, 1663-1728; c 1516-1607; l 744-760 | лут у бою та після місії | 4 |
| T14 | GL офлайн-база: меню, `LiveBackend`, Warehouse 100, Safe | as 1157-1176, 1787-1804, 1879-1968, 2095-2159; m 63-77, 320-378 | переміщення працює і зберігається | 6 |
| T15 | GL Trade-симуляція (Buy/Sell/Cancel/Price Info/Sale List; 502/504 у Rare) | as 1405-1626, 1806-1841, 2083-2093; m 79-147, 210-274 | 504 купується; лоти продаються | 12 |
| T16 | GL Management → локальний бекап або приховати | as 2137-2159, 476-527, 698-749 | працює або приховано | 2 |
| T17 | QA/баланс, регресія сейвів | — | звіт про баланс, регресій немає | 3 |

Разом ≈ 82 год. Порядок: T1 (паралельно) → T2 → T3 → T4 → T5 → (T6, T7, T8) → T9 → T10 → T11 → T12 → T13 → T14 → T15 → T16 → T17.