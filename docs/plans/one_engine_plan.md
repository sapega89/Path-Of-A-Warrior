# Один рушій: мультиплеєр всередині одиночної гри

Статус: **чернетка на узгодження** (2026-11-05). Нічого з цього ще не зроблено.

## Мета

Одна гра, один рушій (`GameCanvas`, один цикл `run`, один `Midlet`, один дисплей, одна обробка
клавіш, звуку й мережі). Код мультиплеєра **переноситься без змін у поведінці**: усе, що
`MpCanvas` малював, малює той самий код, але викликаний з циклу одиночної гри. Жодного
перемальовування на віджети одиночної гри, жодних змін у вигляді. Наприкінці каталог `pow/game/online/` і
`mp_main.py` зникають, їхні модулі живуть у `pow/game/online/`.

**Критерій приймання кожного PR:** еталонні скріншоти мультиплеєра (`shots/mp_*`, сценарії
`mp_*.keys`) збігаються піксель у піксель з тим, що малює об'єднаний рушій; еталони одиночної
гри не змінюються. Сервер (`pow_server`) і протокол не змінюються.

## Що є зараз

| Частина | Рядків | Що містить |
|---|---|---|
| `pow/game` (одиночна, `ag.java` та ін.) | 16 100 | карта, бій у реальному часі, меню, Gamevil Live |
| `pow.game.online` (мультиплеєр, `g.java` та ін.) | 8 000 | 49 станів `MpCanvas`: меню, персонаж, рейтинг, орден, чат, дуель; свої `font/gfx/draw/image` |
| `pow_server` | 4 000 | обидва протоколи, бій дуелі, ордени, чат |
| `res_mp` | 202 файли | спрайти бійців, тла, обличчя, UI, звуки мультиплеєра |

PR #58 поклав обидві гри в один процес **по черзі**: одиночна зупиняється, модулі `pow.game`
стираються, стартує `MpCanvas` зі своїм циклом, після її Exit одиночна стартує з Main Menu
заново. Нагороди бою (1032) клієнт дописує сирими байтами в сейв (`sp_bridge.add_rewards`) без
level-up і без повідомлення; Gamevil Live потім каже «нема збережених Exp/Fame» (попап 20), бо
дивиться в інше місце (запит 258).

## Порядок: чотири PR у dev, кожен сам по собі робочий

```
PR 0  Trade: сітка видів над софт-клавішами, опис без біжучого рядка        (злито: #66)
PR 1  Один Midlet: MP як екран тієї ж гри, нагороди героєві, без попапу й outro (злито: #67)
PR 2  Один цикл: MpCanvas працює всередині GameCanvas.run, код переїжджає в pow/game/online/ (цей PR)
PR 3  Прибирання: mp_main.py, mp_shot.py, web --mp, sp_bridge сирими байтами, документація
```

Після PR 1 усі чотири скарги закриті (нагороди, вікно виходу, реклама, «Exp/Fame не
перенеслись»). PR 2 і 3 міняють лише структуру коду; гравець різниці не бачить.

---

## PR 1. Один Midlet: мультиплеєр як екран тієї ж гри

**Мета.** Game Menu → Gamevil Live → **Multiplayer** → гра → Exit → назад у меню Gamevil Live, той
самий герой у пам'яті, нагороди застосовані з level-up і попапом. Жодного перезапуску одиночної
гри, попапу «Would you like to exit?», outro з логотипом.

**Зміни.**
1. `pow/game/live.py open_live_menu`, `live_menu_keys`: пункт `Multiplayer` (Trade | Warehouse |
   Safe | Multiplayer). `pow/game/menus.py`: пункт Multiplayer у Main Menu прибрати (**D1**).
2. `pow/game/game_canvas.py run`: вихід із циклу зі станом у пам'яті (`GameCanvas.suspended`) і
   `resume()` без `init_game`. Звук: `stop_sound` перед виходом, музика поточного стану після.
3. `main.py`: цикл «одиночна → (призупинена) MP → одиночна продовжує». `fresh_games()` стирає лише
   `pow.game.online.*` (статичні поля чисті на кожен вхід, як у jar); `pow.game` не чіпає. У PR 2 це зникне.
4. `pow/game/online/mp_canvas_input.py`, `mp_canvas.py`: Exit у головному меню MP без попапу; стан 300
   (`_paint_outro`, `outro.png`, 30 кадрів) пропускається — одразу назад.
5. **Нагороди.** 1032 (`net_thread._port_extra_in`): замість сирих байтів у сейв — `(gold, fame,
   exp, loot)` у пам'яті (`sp_bridge.pending`). Після повернення: `hero.gold += gold`, `hero.fame +=
   fame`, `GameCanvas.add_exp(exp)` (штатний level-up, `ag.H`), лут через наявний `add_item`,
   `save_game()`, попап 41 «Exp N / Fame M / Level L» (той, що показував Gamevil Live після 259).
   Попап 20 «нема збережених Exp/Fame» при `Online.enabled()` не показувати; 258/260 лишаються
   для `POW_ALWAYS_ONLINE=0`.
6. Outro одиночної гри при Exit (`start_exit`, стан 12, `draw_outro`) і лого на старті
   (`af.java`, 2.5 с) прибрано зовсім, без прапорців (рішення гравця); еталони title / mouse перезняті.
7. Сервер: без змін. Один акаунт (PR #63) уже дає вхід у MP без екрана логіну.

**Java.** `ag.java:708-760` (цикл), `ag.java:3003-3019` (outro), `as.java:1157-1176` (меню Gamevil
Live), `as.java:1746-1756` і попап 41 у `l.java` (Exp/Fame), `g.java` стан 300, `h.java:84-110`.

**Тести.** `tests/test_one_game.py` (suspend → resume зберігає стан; 1032 → pending → `add_exp`
робить level-up і попап 41; Exit MP без попапу й outro). Сценарій `live_multiplayer.keys` з
еталонами; `multiplayer N NAME BACK` у `shot.py` під новий шлях. Усі `test_mp_*` лишаються.

**Ризики.** Мапа клавіш MP (цифровий ряд у чаті) відновлювати при поверненні; заголовок вікна;
з'єднання Live під час сеансу MP (сервер уже тримає обидві сесії одного акаунта).

---

## PR 2. Один цикл: MpCanvas всередині GameCanvas.run, код переїжджає

**Мета.** Немає другого циклу, другого `Midlet` і другого `Canvas`. `MpCanvas` стає набором
модулів під `pow/game/online/`, які `GameCanvas` викликає у своєму циклі, поки гравець у розділі
Multiplayer. Малювання, стани (0…300), поля й методи — **ті самі, перенесені як є**, з
коментарями `# g.java:FROM-TO`.

**Як саме.**
1. `GameCanvas.state = 13` («online», PORT-EXTRA) — у цьому стані `run` замість `handle_key` /
   `repaint` / `tick_live` викликає `online.tick(key)` і `online.paint()`: це `MpCanvas.main_loop`
   (`g.java c_v`) розкладений на «один кадр» без власного `while`. Темп кадру — той, що мав MP.
2. Клавіші: `GameCanvas.handle_key` у стані 13 передає код у `online.handle_key` (`g.java f_I`).
   Мапа цифрового ряду для чату (`canvas.KEYMAP`) вмикається при вході в стан 13 і повертається
   при виході — те, що зараз робить `main.py`.
3. Мережа: `NetThread.tick()` викликається з того ж місця циклу, де `tick_live()`; транспорт і
   `pow_server` без змін.
4. Звук: `pow/game/online/game.py` → `pow/game/online/sound.py`, грає через той самий `pow/midp/media`.
5. Ресурси: `res_mp/` лишається каталогом ресурсів розділу (`config.MP_RES_ROOT`); завантажувач
   `online/assets.py` = `mp_canvas_assets.py` як є. Злиття в `res/` — не потрібне.
6. Переїзд файлів (git mv, лише імпорти й назви класів):

   | було | стає |
   |---|---|
   | `pow/game/online/mp_canvas.py` + `mp_canvas_*.py` | `pow/game/online/canvas.py` + `online/*.py` (той самий поділ на mixin-и) |
   | `pow/game/online/net_thread.py`, `net/` | `pow/game/online/net.py`, транспорт лишається в `pow/game/online/net/` → `pow/midp/transport.py` (його вже використовує Gamevil Live) |
   | `pow/game/online/font.py`, `gfx.py`, `draw.py`, `image.py` | `pow/game/online/` як є (інший формат шрифту й малювання, ніж у `pow/game/font.py`; не зливати, щоб не змінити піксель) |
   | `pow/game/online/sp_bridge.py` | `pow/game/online/bridge.py`: хвіст 262 будується з `GameCanvas.hero` у пам'яті замість розбору 965-байтного сейва |
   | `pow/game/online/midlet.py`, `mp_game.py` | видаляються (Midlet один; `Game` → частина `online/canvas.py`) |
   | `pow/game/online/consts.py`, `answer.py`, `frame_*`, `rt.py`, `sprite_frames.py`, `player_pool.py`, `res_reader.py` | `pow/game/online/…` як є |

7. `pow/game/online/` після цього порожній, лишається до PR 3 тільки `mp_main.py` як тонка обгортка для
   старих сценаріїв `mp_shot.py` (щоб порівняти еталони до/після).

**Критерій.** Сценарії `mp_login … mp_order_menus` (12 штук) ганяються через `shot.py` в
об'єднаному рушії і дають ті самі кадри, що їхні еталони з `mp_shot.py`. Еталони одиночної гри
без змін.

**Java.** `g.java c_v` (цикл), `f_I` (клавіші), `d_v` (paint), `h.java` (мережа).

**Як зроблено.** Файли переїхали без перейменувань (`pow/game/online/mp_canvas*.py` тощо), транспорт у
`pow/midp/transport.py`; `online_session.py` (стан 13, `enter` / `frame` / `leave`), один кадр = `online/game.py frame`.
Статичні поля `MpCanvas` і далі чистяться перезавантаженням модулів `pow.game.online` при кожному
вході (`online_session._fresh`): простіше й надійніше за ручний `reset()`. Титул «press any key»
лишається (гравцеві подобається).

---

## PR 3. Прибирання

- Браузерна збірка більше не потрібна (рішення гравця): прибрати pygbag (`build_web.py`,
  `web-src`, `test_web_build.py`, розділ README), лишити лише гайд і енциклопедію
  (`web/guide.html`, `web/encyclopedia.html`, `gen_encyclopedia.py`).
- Видалити `mp_main.py`, `tools/mp_shot.py` (сценарії `mp_*.keys` уже йдуть через `shot.py`),
  `build_web.py --mp` і сторінку `web-mp-src`; `tests/test_mp_client.py` → сценарії в
  `test_screens.py`.
- `README.md`, `NAMES.md` (§MpCanvas → `pow/game/online/`), `JAVA_REFERENCE.md` (`g.java` → де
  тепер), `docs/analysis`.

---

## Рішення, які потрібні від тебе

| # | Питання | Рекомендація |
|---|---|---|
| D1 | Де вхід: пункт **Multiplayer у меню Gamevil Live** чи окремий пункт Game Menu? | у Gamevil Live: це і є «онлайн» частина, акаунт той самий |
| D3 | «Multiplayer Exp / Fame» і рейтинг на сервері (`mp_exp`, `mp_fame`) лишити окремою статистикою для Ranking, а рівень/Exp героя — одиночні? | так; у Records, як зараз, показуються обидва |
| D4 | `mp_main.py` і браузерну збірку `--mp` видаляти в PR 3, а не раніше? | так, старі еталони потрібні для порівняння в PR 2 |
| D5 | Outro одиночної гри | вирішено: прибрано зовсім, разом із лого на старті |

(D2 про арт і D6 про PR 0 знято: арт лишається мультиплеєрний як є; PR 0 уже відкритий, #66.)

## Що не входить

- Будь-які зміни у вигляді екранів мультиплеєра чи одиночної гри.
- Зміна механіки дуелі (бій на карті проти інших гравців) — окремий план.
- Зміни сервера.
- Godot (`docs/analysis/05_godot_audit.md`, PR #64) — не зачіпається.
