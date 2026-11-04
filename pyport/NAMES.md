# Java → Python: імена

Порт починався дослівним (імена Java). Рефакторинг дає змістовні імена; ця таблиця зберігає зв'язок
з декомпільованою Java (гілка `java-reference`). Коментарі `# ag.java:FROM-TO` біля методів лишаються.

## Модулі одиночної гри (`pow/game`)

| Java | Python-модуль |
|---|---|
| `ag.java` | `pow/game/game_canvas.py` (`GameCanvas`: цикл, стани, клавіші, меню, вхід на карту), а решту методів розкладено на міксини: |
| `ag.java`: сейв і опції | `pow/game/canvas_save.py` (`SaveMixin`) |
| `ag.java`: предмети, рюкзак, магазин, стати героя | `pow/game/canvas_items.py` (`ItemsMixin`) |
| `ag.java`: таблиці текстів, перенос рядків, рядки з байтів | `pow/game/canvas_text.py` (`TextMixin`) |
| `ag.java`: примітиви малювання, рамки, числа, описи | `pow/game/canvas_draw.py` (`DrawMixin`) |
| `ag.java`: сюжет, діалоги, генерали, лорди | `pow/game/canvas_story.py` (`StoryMixin`) |
| `ag.java`: завантаження й звільнення картинок / спрайтів | `pow/game/canvas_assets.py` (`AssetsMixin`) |
| `System.arraycopy`, `(char)` байта | `pow/game/jutil.py` |
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
| — (PORT-EXTRA) | `pow/game/hero_classes.py` (базові стати 4 героїв, перерозподіл атрибутів) |

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
| `w` | `TargetInfo` | рамка з ім'ям, рівнем і HP ворога, якого б'є герой |
| `an` | `MissionDef` | місія: старт на карті, бос, генерал, нагорода, ліміт часу |
| `y` | `SpriteFrame` | шматок кадру спрайта (SP3) |
| `f` | `Arrow` | стріла лучника |
| `i` | `SpawnSpot` | вільна клітинка для появи ворога |
| `r` | `Breakable` | предмет на карті, що розбивається (бочка, ящик) |
| `a` | `Drop` | предмет, що випав на карті |
| `ah` | `ScriptSlot` | запис хеш-таблиці скриптів клітинок |
| `au` | `RoomCell` | комірка карти: слоти ворогів і параметри |
| `ap` | `Actor` | сутність на карті (ворог, герой, генерал) |
| `n` | `Hero` | герой: характеристики, інвентар, скіли |

## Поля

Java-ім'я поля → Python-ім'я. Коментар `# ag.java:N` біля поля і далі вказує на Java-рядок.
Поля `def` перейменовано на `defense`, `atk` на `attack` (бо `def` у Python ключове слово).

### GameCanvas (і GameFields)

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `bb` | `menus` | `bc` | `engine` | `bd` | `scene` |
| `be` | `live` | `bf` | `boot` | `bg` | `sound` |
| `bh` | `app_version` | `bi` | `cheat` | `bj` | `debug_keys` |
| `bk` | `live_host` | `bl` | `live_port` | `bm` | `more_games_url` |
| `bn` | `multiplay_url` | `bo` | `input_box` | `bp` | `in_live` |
| `bq` | `started` | `br` | `screen_g` | `bs` | `midlet` |
| `bt` | `thread` | `bu` | `font_white` | `bv` | `font_black` |
| `bw` | `font_orange` | `bx` | `font_gray` | `by` | `rng` |
| `bz` | `name_buf` | `bA` | `scr_ui` | `bB` | `scr_char` |
| `bC` | `scr_effect` | `bD` | `scr_tile` | `bE` | `scr_data` |
| `bF` | `scr_maps` | `bG` | `scr_gamestr` | `bH` | `item_tables` |
| `bI` | `scr_story` | `bJ` | `screen_w` | `bK` | `screen_h` |
| `bL` | `screen_cx` | `bM` | `screen_cy` | `bN` | `frame` |
| `bO` | `fill_color` | `bP` | `letter_cursor` | `bQ` | `pause_pending` |
| `bR` | `pause_pending_value` | `bS` | `paused` | `a` | `key_delay` |
| `b` | `key_lock` | `c` | `key_time` | `bT` | `tile_images` |
| `bU` | `softkey_bg` | `bV` | `state` | `bW` | `prev_state` |
| `bX` | `last_state` | `bY` | `view_size` | `bZ` | `canvas_size` |
| `ca` | `camera` | `cb` | `view_tiles` | `cc` | `view_offset` |
| `cd` | `view_tx` | `ce` | `view_ty` | `cf` | `room_origin` |
| `cg` | `map_id` | `ch` | `key` | `ci` | `key_pressed` |
| `cj` | `key_held` | `ck` | `redraw` | `cl` | `screen_fill` |
| `cm` | `exit_blink` | `cn` | `room_phase_timer` | `co` | `room_phase` |
| `cp` | `exit_dir` | `cq` | `chapter` | `cr` | `boss_fight` |
| `cs` | `dir_history` | `ct` | `images` | `cu` | `buffer_g` |
| `cv` | `title_press` | `cw` | `title_logo` | `cx` | `hud_frame` |
| `cy` | `anim_step` | `cz` | `hero` | `cA` | `breakables` |
| `cB` | `breakable_count` | `cC` | `drops` | `cD` | `drop_count` |
| `cE` | `map` | `cF` | `save_buf` | `cG` | `save_pos` |
| `cH` | `cell_scripts` | `cI` | `cell_script_next` | `cJ` | `tile_slots` |
| `cK` | `menu_anim` | `cL` | `menu_scroll` | `cM` | `menu` |
| `cN` | `menu_count` | `cO` | `menu_return` | `cP` | `menu_cursors` |
| `cQ` | `menu_tops` | `cR` | `map_mode` | `cS` | `popups` |
| `cT` | `popup_lines` | `cU` | `gear_data` | `cV` | `treasure_data` |
| `cW` | `rare_data` | `cX` | `gear_def` | `cY` | `treasure_def` |
| `cZ` | `rare_def` | `da` | `menu_part` | `db` | `view_x` |
| `dc` | `view_y` | `dd` | `view_cx` | `de` | `view_cy` |
| `df` | `sound_on` | `dg` | `volume` | `dh` | `speed` |
| `di` | `option_time` | `dj` | `save_flag` | `dk` | `lord` |
| `dl` | `lord_name` | `dm` | `mission` | `dn` | `mission_name` |
| `do` | `rooms_visited` | `dp` | `text_lines` | `dq` | `text_line_count` |
| `dr` | `lord_count` | `ds` | `lord_ids` | `dt` | `lord_names` |
| `du` | `lord_missions` | `dv` | `lord_mission_counts` | `dw` | `missions_done` |
| `dx` | `lords_done` | `dy` | `stats` | `dz` | `lords` |
| `dA` | `mission_names` | `dB` | `mission_portraits` | `dC` | `general` |
| `dD` | `text_width` | `dE` | `menu_items` | `dF` | `info_box` |
| `dG` | `talk_kind` | `dH` | `talk_count` | `dI` | `talk_line` |
| `dJ` | `talk_general` | `dK` | `talk_box` | `dL` | `talk_x` |
| `dM` | `talk_y` | `dN` | `talk_cursor_x` | `dO` | `talk_chars` |
| `dP` | `talk_row` | `dQ` | `talk_rows` | `dR` | `talk_side` |
| `dS` | `wait_ticks` | `dT` | `message` | `dU` | `effect` |
| `dV` | `play_time` | `dW` | `clock` | `dX` | `mission_seconds` |
| `dY` | `mission_exp` | `dZ` | `exp_bars` | `ea` | `exp_bar_step` |
| `eb` | `story_pages` | `ec` | `story_ending` | `ed` | `score` |
| `ee` | `story_id` | `ef` | `reward_item` | `eg` | `reward_skill` |
| `eh` | `story_fade` | `ei` | `menu_before_talk` | `ej` | `help_topic` |
| `ek` | `hero_picked_up` | `el` | `hero_effect_drawn` | `em` | `enemy_effect_drawn` |
| `en` | `enemy_trail_drawn` | `eo` | `live_time` | `ep` | `difficulty` |
| `eq` | `general_mark` | `er` | `boss_images` | `es` | `enemy_images` |
| `et` | `enemy_frames` | `eu` | `spawn_spots` | `ev` | `spawn_spot_count` |
| `ew` | `reachable` | `ex` | `actors` | `ey` | `actor_slots` |
| `ez` | `actor_count` | `eA` | `enemies_alive` | `eB` | `boss_spawned` |
| `eC` | `arrows` | `eD` | `waves` | `eE` | `dirty` |
| `eF` | `head_anim` | `eG` | `body_anim` | `eH` | `weapon_anim` |
| `eI` | `head_anims` | `eJ` | `body_anims` | `eK` | `weapon_anims` |
| `eL` | `char_anims` | `eM` | `sheet_x` | `eN` | `sheet_y` |
| `eO` | `cells` | `eP` | `cell` | `eQ` | `shadow_frames` |
| `eR` | `shadow_image` | `eS` | `hero_weapon_frames` | `eT` | `hero_body_frames` |
| `eU` | `trail_frames` | `eV` | `spark_frames` | `eW` | `skill_frames` |
| `eX` | `hero_fx_data` | `eY` | `hero_fx_frames` | `eZ` | `hero_fx_pos` |
| `fa` | `enemy_fx_data` | `fb` | `enemy_fx_frames` | `fc` | `enemy_fx_pos` |
| `fd` | `fire_data` | `fe` | `fire_frames` | `ff` | `fire_ticks` |
| `fg` | `hero_fx_count` | `fh` | `hero_fx_kind` | `fi` | `hero_fx_image` |
| `fj` | `hero_fx_parts` | `fk` | `enemy_fx_kind` | `fl` | `enemy_fx_image` |
| `fm` | `enemy_fx_parts` | `fn` | `generals` | `fo` | `general_count` |
| `fp` | `general_pages` | `fq` | `talk_points` | `fr` | `general_table` |
| `fs` | `visit_text` | `ft` | `general_name` | `fu` | `seal` |
| `fv` | `visit_row` | `fw` | `speech` | `fx` | `speech_x` |
| `fy` | `speech_y` | `fz` | `speech_w` | `fA` | `speech_pos` |
| `fB` | `speech_lines` | `fC` | `speech_done` | `fD` | `story_page` |
| `fE` | `story_picture` | `fF` | `visit_topic` | `fG` | `speech_line` |
| `fH` | `visit_general` | `fI` | `gift_kind` | `fJ` | `gift_level` |
| `fK` | `cursor` | `fL` | `shop` | `fM` | `tables_loaded` |
| `fN` | `sparkle` | `fO` | `combine_slots` | `fP` | `combine_pos` |
| `fQ` | `combine_result` | `fR` | `live_gifts` | `fS` | `live_saved` |
| `fT` | `menu_titles` | `fU` | `game_menu_items` | `fV` | `main_menu_items` |
| `fW` | `yes_no_items` | `fX` | `ok_items` | `fY` | `continue_items` |
| `fZ` | `pause_items` | `ga` | `help_items` | `gb` | `option_names` |
| `gc` | `on_off` | `gd` | `skill_names` | `ge` | `speed_names` |
| `gf` | `talk_lines` | `gg` | `painted` | `gh` | `running` |
| `gi` | `tick_start` | `gj` | `map_started` | `gk` | `ball_cover` |
| `gl` | `carousel_image` | `gm` | `carousel_row` |  |  |

### Point

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `x` | `b` | `y` |  |  |

### Rect

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `x` | `b` | `y` | `c` | `w` |
| `d` | `h` |  |  |  |  |

### MapMode

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `mode` | `b` | `sub` |  |  |

### Item

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `id` | `b` | `attack` | `c` | `defense` |
| `d` | `hp` | `e` | `mp` | `f` | `enchant` |

### QuickSlot

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `item` | `b` | `count` |  |  |

### GearDef

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `name` | `b` | `slot` | `c` | `bonus_stat` |
| `d` | `bonus` | `e` | `bonus_range` | `f` | `icon` |

### TreasureDef

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `name` | `b` | `slot` | `c` | `attack` |
| `d` | `defense` | `e` | `hp` | `f` | `mp` |
| `g` | `icon` | `h` | `level` |  |  |

### RareDef

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `name` | `b` | `slot` | `c` | `attack` |
| `d` | `defense` | `e` | `hp` | `f` | `mp` |
| `g` | `level` |  |  |  |  |

### MapData

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `data` | `b` | `size` | `c` | `layer_ground` |
| `d` | `layer_upper` | `e` | `layer_objects` | `f` | `layer_flags` |

### MapSize

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `w` | `b` | `h` | `c` | `extra` |

### ActiveEffect

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `item` | `b` | `step` | `c` | `pos` |
| `d` | `dir` | `e` | `slot` | `f` | `frame` |
| `g` | `frame_data` | `h` | `frames` |  |  |

### GeneralDef

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `name` | `b` | `look` | `c` | `side` |
| `d` | `skills` | `e` | `portrait` | `f` | `gift_table` |
| `g` | `attack` | `h` | `defense` | `i` | `hp` |

### InfoBox

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `shown` | `b` | `rect` | `c` | `text` |
| `d` | `text_x` |  |  |  |  |

### TargetInfo

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `shown` | `b` | `ticks` | `c` | `name` |
| `d` | `level` | `e` | `hp_bar` |  |  |

### MissionDef

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `id` | `b` | `start_x` | `c` | `start_y` |
| `d` | `tint` | `e` | `boss_type` | `f` | `general` |
| `g` | `reward` | `h` | `gold` | `i` | `time_limit` |
| `j` | `level_bonus` |  |  |  |  |

### SpriteFrame

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `src_x` | `b` | `src_y` | `c` | `w` |
| `d` | `h` | `e` | `ox` | `f` | `oy` |

### Arrow

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `active` | `b` | `pos` | `c` | `w` |
| `d` | `h` | `e` | `dir` | `f` | `attack` |
| `g` | `ticks` |  |  |  |  |

### SpawnSpot

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `tx` | `b` | `ty` | `c` | `dir` |

### Breakable

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `active` | `b` | `pos` | `c` | `tile` |
| `d` | `hp` | `e` | `break_ticks` | `f` | `image` |
| `g` | `kind` | `h` | `break_frame` |  |  |

### Drop

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `item` | `b` | `pos` | `c` | `ticks` |
| `d` | `frame` | `e` | `w` | `f` | `h` |
| `g` | `image` |  |  |  |  |

### ScriptSlot

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `offset` | `b` | `next` | `c` | `used` |

### RoomCell

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `exits` | `b` | `max_enemies` | `o` | `general` |
| `c` | `wave_0` | `d` | `wave_1` | `e` | `wave_2` |
| `f` | `wave_3` | `g` | `wave_4` | `h` | `wave_5` |
| `i` | `wave_6` | `j` | `wave_7` | `k` | `wave_8` |
| `l` | `wave_9` | `m` | `wave_10` | `n` | `wave_11` |

### Actor

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `pos` | `b` | `target` | `c` | `active` |
| `d` | `facing` | `e` | `dir` | `f` | `action` |
| `g` | `frame` | `h` | `type` | `i` | `level` |
| `j` | `attack` | `k` | `defense` | `l` | `max_hp` |
| `m` | `hp` | `n` | `attack_buff` | `o` | `defense_buff` |
| `p` | `attack_buff_ticks` | `q` | `defense_buff_ticks` | `r` | `alerted` |
| `s` | `think_ticks` | `t` | `hit_fx_kind` | `u` | `hit_fx_frame` |
| `v` | `hit_fx_pos` | `w` | `on_fire` | `x` | `fire_frame` |
| `y` | `skill_fx` | `z` | `skill_step` | `A` | `ai_mode` |
| `B` | `anims` | `C` | `image` | `D` | `frames` |

### Hero

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `pos` | `b` | `room_pos` | `c` | `facing` |
| `d` | `dir` | `e` | `action` | `f` | `frame` |
| `g` | `mission_progress` | `h` | `live_stat1` | `i` | `live_stat2` |
| `j` | `slide_target` | `k` | `name` | `l` | `level` |
| `m` | `base_attack` | `n` | `base_defense` | `o` | `base_hp` |
| `p` | `hp` | `q` | `base_mp` | `r` | `mp` |
| `s` | `gear_attack` | `t` | `gear_defense` | `u` | `gear_hp` |
| `v` | `gear_mp` | `w` | `attack` | `x` | `defense` |
| `y` | `max_hp` | `z` | `max_mp` | `A` | `attack_buff` |
| `B` | `defense_buff` | `C` | `attack_buff_ticks` | `D` | `defense_buff_ticks` |
| `E` | `gold` | `F` | `fame` | `G` | `exp` |
| `H` | `kills` | `I` | `kills_shown` | `J` | `stat_points` |
| `K` | `weapon_kind` | `L` | `sprite_frame` | `M` | `combo` |
| `N` | `idle_ticks` | `O` | `hit_fx_kind` | `P` | `hit_fx_frame` |
| `Q` | `hit_fx_pos` | `R` | `hurt_ticks` | `S` | `live_registered` |
| `T` | `on_fire` | `U` | `fire_frame` | `V` | `hotkeys` |
| `W` | `skill_levels` | `X` | `equipped` | `Y` | `backpack` |
| `Z` | `quick_slots` | `aa` | `quick_keys` | `ab` | `anims` |
| `ac` | `anim_0` | `ad` | `anim_1` | `ak` | `anim_2` |
| `ae` | `anim_3` | `af` | `anim_4` | `ag` | `anim_5` |
| `ah` | `anim_6` | `ai` | `anim_7` | `aj` | `anim_8` |
| `al` | `anim_9` | `am` | `anim_10` | `aA` | `anim_11` |
| `an` | `anim_12` | `ao` | `anim_13` | `ap` | `anim_14` |
| `aq` | `anim_15_19` | `ar` | `anim_20` | `as_` | `anim_21` |
| `at` | `anim_22` | `au` | `anim_23_24` | `av` | `anim_25` |
| `aw` | `anim_26_27` | `ax` | `anim_28` | `ay` | `anim_29` |
| `az` | `anim_30` | `aB` | `head` | `aC` | `head_frames` |
| `aD` | `head_frames2` | `aE` | `body_frames` | `aF` | `body_frames2` |
| `aG` | `head_image` | `aH` | `body_image` |  |  |

### Boot

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `logo` | `b` | `step` | `c` | `start_time` |

### Menus

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `mix_table` |  |  |  |  |

### Popups

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `from_gamestr` | `b` | `kind` | `b_` | `popup_id` |
| `d` | `timer` | `e` | `extra` | `f` | `extra_w` |
| `g` | `extra_h` | `h` | `height` | `i` | `line_count` |
| `j` | `popup_redraw` | `k` | `button` | `l` | `lines` |
| `m` | `arg1` | `n` | `arg2` | `o` | `arg3` |
| `p` | `arg4` | `q` | `answered` | `r` | `image` |
| `s` | `drawn` |  |  |  |  |

### Sound

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `players` | `b` | `requested` | `a_` | `music` |
| `d` | `last` | `e` | `last_time` | `f` | `min_gap` |

### Gfx

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `crc_table` | `b` | `g` | `c` | `saved_clip_x` |
| `d` | `saved_clip_y` | `e` | `saved_clip_w` | `f` | `saved_clip_h` |
| `g` | `clip_x` | `h` | `clip_y` | `i` | `clip_w` |
| `j` | `clip_h` | `k` | `font` |  |  |

### Font

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `image` | `b` | `glyph_w` | `c` | `glyph_h` |
| `d` | `space_w` | `e` | `plte_offset` |  |  |

### ScrTable

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `data` |  |  |  |  |

### ArrTable

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `widths` | `b` | `offsets` | `c` | `rows` |
| `d` | `row_size` |  |  |  |  |

### NameBuffer

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `chars` | `b` | `max_len` | `c` | `changed` |
| `d` | `last_char` | `e` | `cursor` |  |  |

### LiveAnswer

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `data` | `b` | `pos` |  |  |

### LiveNet

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `conn` | `d` | `listener` | `f` | `idle` |
| `g` | `unused` | `h` | `connected` | `i` | `running` |
| `j` | `connect_requested` | `m` | `waiting` | `k` | `host` |
| `l` | `port` |  |  |  |  |

### Midlet

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `display` | `b` | `canvas` | `c` | `started` |

### PlayerPool

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `players` | `e` | `count` | `j` | `volume` |
| `n` | `playing` | `p` | `looping` | `c` | `paused` |

### Live

| Java | Python | Java | Python | Java | Python |
|---|---|---|---|---|---|
| `a` | `screen` | `b` | `net` | `d` | `first_login` |
| `e` | `waiting` | `f` | `request_time` | `g` | `pending_request` |
| `h` | `answer_op` | `i` | `blink_count` | `j` | `anim_ticks` |
| `k` | `reg_step` | `l` | `password` | `m` | `user_id` |
| `n` | `reg_from_popup` | `o` | `inited` | `p` | `loading0` |
| `q` | `loading1` | `r` | `arrow_image` | `s` | `level_image` |
| `gn` | `session_id` | `go` | `session_new` | `gp` | `login_request` |
| `gq` | `request_in_flight` | `gr` | `answer_status` | `gs` | `answered` |
| `gt` | `close_target` | `gu` | `busy` | `gv` | `backpack_serials` |
| `gw` | `warehouse` | `gx` | `warehouse_serials` | `gy` | `safe_gold` |
| `gz` | `lots` | `gA` | `lot_ids` | `gB` | `prices` |
| `gC` | `gift_from` | `gD` | `list_kind` | `gE` | `blink` |
| `gF` | `kind_items` | `gG` | `category_codes` | `gH` | `in_answer` |
| `gI` | `list_items` | `gJ` | `list_count` | `gK` | `list_rows` |
| `gL` | `list_cursor` | `gM` | `list_top` | `gN` | `list_y` |
| `gO` | `list_w` | `gP` | `category` | `gQ` | `kind` |
| `gR` | `enchant` | `gS` | `page` | `gT` | `page_step` |
| `hi` | `shown_item` | `hj` | `selected_serial` | `hk` | `selected_slot` |
| `hl` | `titles` | `hm` | `live_strings` | `hn` | `title` |
| `ho` | `live_screen` | `hp` | `input_handler` | `hq` | `screen_redraw` |
| `hr` | `scroll` | `hs` | `scroll_step` | `ht` | `flags` |
| `hu` | `counts` | `hv` | `values` | `hw` | `category_names` |
| `gU` | `saved_0` | `gV` | `saved_1` | `gW` | `saved_2` |
| `gX` | `saved_3` | `gY` | `saved_4` | `gZ` | `saved_5` |
| `ha` | `saved_6` | `hb` | `saved_7` | `hc` | `saved_8` |
| `hd` | `saved_9` | `he` | `saved_10` | `hf` | `saved_11` |
| `hg` | `saved_12` | `hh` | `saved_13` |  |  |

## Методи

Java-ім'я методу (з суфіксом сигнатури, напр. `J_I` = `J(int)`) → Python-ім'я.
Методи MIDP (`paint`, `keyPressed`, `run`, `startApp` тощо) мають свої стандартні імена.

### GameCanvas

| Java | Python | Java | Python |
|---|---|---|---|
| `q_v` | `reset_globals` | `r_v` | `read_screen_size` |
| `s_v` | `init_game` | `t_v` | `handle_key` |
| `b_T` | `log` | `u_v` | `repaint_and_wait` |
| `f_I` | `sleep` | `a_Z` | `set_paused` |
| `b_Z` | `apply_pause` | `v_v` | `lock_keys` |
| `w_v` | `unlock_keys` | `x_v` | `free_images` |
| `a_IIT` | `draw_text_left` | `b_IIT` | `draw_text_centred` |
| `E_v` | `load_title_picture` | `F_v` | `load_menu_frames` |
| `G_v` | `load_options` | `H_v` | `save_options` |
| `I_v` | `clamp_menu_scroll` | `a_MIIIIII` | `draw_view_region` |
| `b_TI` | `split_field` | `c_IIT` | `draw_text` |
| `a_BB` | `u16` | `K_v` | `draw_view_background` |
| `c_III` | `fill_view` | `L_v` | `paint_state` |
| `a__I` | `play_sound` | `P_v` | `tick_state` |
| `Q_v` | `start_boot` | `t_I` | `key_down` |
| `d_T` | `load_image` | `R_v` | `gc` |
| `u_I` | `fill_screen` | `S_v` | `draw_title` |
| `a_TIIIIII` | `draw_image_file` | `T_v` | `tick_title` |
| `U_v` | `load_game` | `V_v` | `read_long` |
| `W_v` | `read_int` | `X_v` | `read_short` |
| `Y_v` | `read_byte` | `Z_v` | `read_item` |
| `aa_v` | `load_ui_images` | `v_I` | `load_data_file` |
| `w_I` | `open_menu` | `ad_v` | `load_menu_images` |
| `ae_v` | `free_menu_images` | `af_v` | `load_menu_texts` |
| `x_I` | `draw_menu_background` | `ag` | `compact_backpack` |
| `a_LzLz` | `swap_items` | `b_LzLz` | `copy_item` |
| `ah` | `free_hero_sprites` | `a_IIIIMII` | `draw_region` |
| `b_MIIIIII` | `draw_map_region` | `c_MIIIIII` | `draw_region_at` |
| `ai` | `stop_sound` | `aj` | `free_hero_images` |
| `ak` | `set_menu_items` | `ap` | `restore_menu_cursor` |
| `a_TII` | `draw_text_centred_at` | `b_TII` | `draw_text_at` |
| `c_TII` | `draw_view_text_centred` | `d_TII` | `draw_view_text` |
| `a_IIIIZ` | `draw_box` | `a_IIIIIIIZ` | `draw_frame_box` |
| `k_III` | `rgb` | `aq` | `has_save` |
| `as_` | `start_exit` | `at` | `draw_outro` |
| `a_ABII` | `read_utf` | `h_II` | `draw_softkeys` |
| `l_III` | `set_color` | `f_IIII` | `draw_line` |
| `aA` | `load_hero_images` | `K_I` | `load_frames` |
| `M_I` | `gamestr` | `N_I` | `key_digit` |
| `H_I` | `add_exp` | `e_T` | `trim_right` |
| `f_T` | `cut_at_control` | `g_T` | `cut_at_space` |
| `B_v` | `now` | `O_v` | `update_hero_stats` |
| `r_I` | `move_letter_cursor` | `f_II` | `draw_letter_grid` |
| `f_III` | `draw_arrow` | `g_II` | `rand_range` |
| `C_I` | `rand` | `d_IIII` | `draw_big_number` |
| `ar` | `save_game` | `a_J` | `write_long` |
| `E_I` | `write_int` | `F_I` | `write_short` |
| `G_I` | `write_byte` | `a_Lz` | `write_item` |
| `a_IIIIIII` | `draw_rect_outline` | `b_IIIIIII` | `draw_round_outline` |
| `c_IIIIIII` | `draw_selection` | `j_II` | `draw_dot` |
| `au` | `start_new_game` | `av` | `new_hero` |
| `aw` | `reset_base_stats` | `k_II` | `give_item` |
| `ax` | `reset_quick_items` | `ay` | `fill_shop` |
| `az` | `load_item_tables` | `I_I` | `item_tier` |
| `J_I` | `make_item` | `l_II` | `start_story` |
| `L_I` | `backpack_slot_of` | `M_v` | `tick_story` |
| `d_III` | `fill_screen_rgb` | `N_v` | `draw_story` |
| `q_I` | `draw_skip_key` | `a_B` | `char_width` |
| `b_ABII` | `word_wrap` | `a_AC` | `parse_int` |
| `d_II` | `edat_bytes` | `e_II` | `edat_string` |
| `e_III` | `draw_small_number` | `a_IIIIIMIII` | `draw_image_part` |
| `i_II` | `draw_empty_slot` | `e_IIII` | `draw_grey_frame` |
| `y_I` | `change_option` | `g_I` | `item_slot_type` |
| `a_LzZI` | `describe_shop_item` | `a_Lp` | `quick_slot_item` |
| `o_I` | `item_under_cursor` | `a_LacI` | `fill_rect` |
| `b_LacI` | `outline_rect` | `a_LacII` | `draw_filled_rect` |
| `s_I` | `digit_count` | `c_T` | `measure_text` |
| `i_III` | `draw_small_digit` | `J_v` | `draw_gold_box` |
| `b_IIIII` | `draw_description` | `j_I` | `describe_skill` |
| `k_I` | `describe_potion` | `l_I` | `special_suffix` |
| `m_I` | `set_item_name` | `c_IIII` | `draw_panel` |
| `b_III` | `draw_centred_box` | `c_II` | `draw_gold_amount` |
| `i_I` | `draw_hero_gold` | `h_III` | `draw_number_commas` |
| `n_I` | `format_thousands` | `b_B` | `u8` |
| `C_v` | `load_chapter_lords` | `D_v` | `load_mission_text` |
| `a_ABI` | `table_text` | `a_ABABII` | `append_bytes` |
| `a_ABIC` | `index_after` | `ac_v` | `free_hud` |
| `y_v` | `enter_map` | `z_v` | `load_effect_image` |
| `A_v` | `load_enemy_sprites` | `a_TI` | `load_recoloured` |
| `h_I` | `load_lord_map` | `ab_v` | `load_hud` |
| `g_III` | `draw_digit` | `D_I` | `decimal_digits` |
| `j_III` | `draw_clock` | `al_` | `free_map_images` |
| `am` | `start_dialogue` | `z_I` | `load_dialogue_line` |
| `an` | `start_dialogue_text` | `A_I` | `friendship` |
| `ao` | `next_speech_pos` | `B_I` | `set_general` |
| `p_I` | `random_general_skill` |  |  |

### Menus

| Java | Python | Java | Python |
|---|---|---|---|
| `a_I` | `draw_menu` | `a_v` | `menu_keys` |
| `m_II` | `menu_link` | `aB` | `key_up` |
| `aC` | `key_down_arrow` | `aD` | `key_left` |
| `aE` | `key_right` | `b_v` | `key_fire` |
| `aF` | `key_back` | `aG` | `free_carousel` |
| `c_v` | `enter_submenu` | `d_v` | `free_shop_images` |
| `e_v` | `draw_menu_frame` | `f_v` | `draw_list_menu` |
| `j_v` | `draw_options` | `l_v` | `draw_help_page` |
| `a_IIIZ` | `draw_page_number` | `P_I` | `draw_skills` |
| `k_v` | `draw_description_strip` | `n_II` | `draw_gear` |
| `Q_I` | `draw_inventory` | `d_I` | `draw_assign_items` |
| `g_IIII` | `draw_item_icon` | `a_IAzAI` | `draw_item_grid` |
| `a_IIIAz` | `draw_grid_item` | `a_IIZ` | `draw_grid_cell` |
| `a_IIII` | `draw_item_count_icon` | `aP` | `draw_shop_grid` |
| `c_Z` | `draw_blacksmith` | `aQ` | `roll_enchant` |
| `o_II` | `draw_sparkle` | `aR` | `draw_sparkles` |
| `aV` | `blacksmith_message` | `aW` | `blacksmith_keys` |
| `aX` | `combine_result_of` | `a_LzI` | `enchant_item` |
| `S_I` | `mix_entry` | `b_IIII` | `find_run` |
| `aY` | `enter_blacksmith` | `aZ` | `blacksmith_layout` |
| `ba` | `update_shop_cursor` | `c_I` | `item_name` |
| `bb` | `clear_combine` | `m_v` | `count_items` |
| `b_Lz` | `item_price` | `bc` | `buy_item` |
| `bd` | `sell_item` | `be` | `enchant_price` |
| `a_LzIIIIIZ` | `draw_shop_description` | `g_v` | `load_title_images` |
| `aJ` | `draw_main_menu` | `aK` | `draw_hero_choice` |
| `aL` | `draw_name_captions` | `aM` | `draw_name_box` |
| `O_I` | `draw_stat_sheet` | `b_I` | `draw_story_portraits` |
| `R_I` | `draw_speech_boxes` | `a_III` | `type_speech` |
| `aU` | `draw_difficulty` | `e_I` | `load_item_def` |
| `T_I` | `draw_stat_cursor` | `p_v` | `load_exp_table` |
| `bf_v` | `draw_game_menu` | `aH` | `draw_mission_text` |
| `aI` | `draw_briefing` | `h_v` | `draw_map_talk` |
| `i_v` | `tick_dialogue` | `aS` | `draw_briefing_boxes` |
| `aT` | `draw_map_talk_box` | `bi_v` | `load_lord_missions` |
| `aN` | `draw_generals` | `aO` | `tick_general_talk` |
| `bg_v` | `open_general_talk` | `a_II` | `load_greeting` |
| `b_II` | `add_friendship` | `o_v` | `general_gift` |
| `seal_list` | `seal_list` | `bh_v` | `load_general_table` |
| `n_v` | `draw_popup_extras` | `p_II` | `draw_exp_bar` |

### MapEngine

| Java | Python | Java | Python |
|---|---|---|---|
| `a_v` | `tick_map` | `b_I` | `draw_map` |
| `o_v` | `pause_menu_keys` | `c_I` | `assign_quick_potion` |
| `b_v` | `clamp_hero_hp_mp` | `Q_I` | `iabs` |
| `a_IIIIIIII` | `boxes_touch` | `c_LhLh` | `distance` |
| `d_v` | `spawn_next_enemy` | `e_I` | `skill_mp_cost` |
| `e_v` | `check_run` | `a_LhII` | `step_until_free` |
| `t_II` | `approach_zero` | `b_LhII` | `keep_in_room` |
| `X_I` | `leave_room` | `c_LhII` | `slide_corner` |
| `u_II` | `straighten_step` | `a_LhIIII` | `move` |
| `a_LhIII` | `blocked_by_actor` | `b_II` | `hero_hits_enemy` |
| `m_II` | `general_pick_skill` | `c_v` | `hero_hits_breakables` |
| `R_I` | `show_target_info` | `a_LhLhI` | `is_in_front` |
| `a_LhLh` | `dir4` | `b_LhLh` | `dir8` |
| `n_II` | `hero_strike_if_facing` | `o_II` | `general_strike_if_facing` |
| `p_II` | `breakable_hit_if_facing` | `q_II` | `hero_strike_if_near` |
| `r_II` | `general_strike_if_near` | `s_II` | `breakable_hit_if_near` |
| `S_I` | `strike_enemy` | `T_I` | `general_skill_hits_hero` |
| `U_I` | `hero_is_hit` | `V_I` | `set_enemy_on_fire` |
| `p_v` | `set_hero_on_fire` | `W_I` | `hit_breakable` |
| `d_I` | `hero_attack` | `f_v` | `turn_to_nearest` |
| `aB` | `nearest_enemy` | `Y_I` | `choose_enemy_action` |
| `a_Lh` | `dir_to_hero` | `Z_I` | `shoot_arrow` |
| `g_v` | `tick_enemies` | `aa_I` | `enemy_strikes_hero` |
| `ab_I` | `enemy_dies` | `h_v` | `sort_actors` |
| `i_v` | `pick_up_drops` | `j_v` | `tick_arrows` |
| `ac_I` | `hero_can_be_hit` | `ad_I` | `move_arrow` |
| `aC` | `end_tick` | `O_I` | `tick_mission_clock` |
| `k_v` | `scroll_room` | `a_III` | `draw_spark` |
| `a_IILy` | `draw_hero_weapon` | `a_II` | `draw_weapon_trail` |
| `l_v` | `draw_object_layer` | `m_v` | `draw_drops` |
| `a_ILh` | `drop_item` | `P_I` | `random_drop` |
| `aD` | `draw_quick_potions` | `n_v` | `draw_hud` |
| `aE` | `draw_message` |  |  |

### MapScene

`tick_scene` (`c.java:1643-2136`, `i_v`) розкладено на кроки (нові імена, у Java їх немає): `_erase_actors`,
`_held_direction`, `_read_action_key`, `_end_talk`, `_hold_to_move`, `_start_hero_action`, `_move_hero`,
`_hero_action_hits`; таблиці `buff_div` / `hit_frame` стали модульними `_BUFF_DIV` / `_HIT_FRAME`.

| Java | Python | Java | Python |
|---|---|---|---|
| `c_I` | `load_story_page` | `d_I` | `finish_mission` |
| `g_v` | `start_victory_talk` | `a_v` | `draw_hud_balls` |
| `a_IIII` | `mark_dirty` | `b_v` | `draw_hud_frame` |
| `c_v` | `draw_frame` | `j_v` | `draw_exit_arrows` |
| `k_v` | `draw_arrows` | `d_v` | `erase_arrows` |
| `l_v` | `draw_upper_layer` | `m_v` | `draw_effects` |
| `a_LyBII` | `draw_effect_frame` | `a_ALyABIII` | `draw_effect_frames` |
| `e_v` | `draw_actors` | `n_v` | `draw_breaking` |
| `_fm_from` | `set_enemy_fx_parts` | `e_I` | `draw_enemy` |
| `a_IILyI` | `draw_general_weapon` | `_fj_from` | `set_hero_fx_parts` |
| `o_v` | `draw_hero` | `g_IIII` | `run_cell_scripts` |
| `c_IIIII` | `run_cell_script` | `b_IIII` | `create_enemy` |
| `a_II` | `enemy_stats` | `p_v` | `reset_actors` |
| `h_IIII` | `find_reachable` | `b_II` | `flood_fill` |
| `a_I` | `load_rooms` | `f_v` | `hero_cell` |
| `aB` | `free_map` | `b_I` | `load_map` |
| `aC` | `reset_cell_scripts` | `a_III` | `cell_script_slot` |
| `a_IIIII` | `draw_tiles` | `h_v` | `make_exp_bars` |
| `i_v` | `tick_scene` | `aD` | `erase_breaking` |
| `m_III` | `erase_spark` | `aE` | `erase_exit_arrows` |
| `aF` | `erase_hero` | `m_II` | `erase_weapon_trail` |
| `aG` | `erase_enemies` | `O_I` | `erase_general_weapon` |
| `a_ALyI` | `frames_from` | `aH` | `erase_drops` |
| `aI` | `erase_hero_effects` | `aJ` | `erase_message` |
| `aK` | `erase_gold_and_clock` | `aL` | `draw_potion_effect` |

### Live

| Java | Python | Java | Python |
|---|---|---|---|
| `g_v` | `open_live` | `h_v` | `open_registration` |
| `i_v` | `tick_live` | `_i_end` | `_end_tick` |
| `b_I` | `show_error` | `j_v` | `draw_connecting` |
| `k_v` | `load_live_images` | `l_v` | `start_net` |
| `f_v` | `on_connected` | `c_I` | `ask_request` |
| `d_I` | `queue_request` | `m_v` | `check_answer` |
| `e_I` | `send_request` | `n_v` | `write_request` |
| `o_v` | `disconnect` | `e_v` | `on_connection_failed` |
| `_copy` | `_copy_item` | `a_Lab` | `on_answer` |
| `a_IILab` | `on_error_answer` | `p_v` | `clear_selected_lot` |
| `O_I` | `save_and_sync` | `aB_v` | `list_height` |
| `e_TII` | `set_list_items` | `P_I` | `list_keys` |
| `aC_v` | `clamp_list_scroll` | `aD_v` | `draw_list` |
| `aE_v` | `enter_live` | `aF_v` | `load_titles` |
| `aG_v` | `load_live_strings` | `aH_v` | `open_live_menu` |
| `aI_v` | `open_waiting` | `aJ` | `request_redraw` |
| `a_IIIZ` | `draw_item_cell` | `a_TIII` | `draw_text_centred_in` |
| `aK` | `draw_screen` | `c_TI` | `draw_caption_box` |
| `t_I` | `key_down` | `Q_I` | `registration_keys` |
| `R_I` | `sale_list_keys` | `S_I` | `cancel_sell_keys` |
| `T_I` | `price_info_keys` | `U_I` | `sell_pick_keys` |
| `V_I` | `sell_price_keys` | `W_I` | `buy_kind_keys` |
| `X_I` | `buy_enchant_keys` | `Y_I` | `buy_lots_keys` |
| `Z_I` | `buy_category_keys` | `aL_v` | `open_sell_price` |
| `aM_v` | `open_cancel_sell` | `aN_v` | `open_sale_list` |
| `aO_v` | `set_cancel_sell_grid` | `c_Z` | `restore_grid_cursor` |
| `aP_v` | `open_sell_grid` | `aQ_v` | `open_price_info` |
| `d_Z` | `open_buy_lots` | `aR_v` | `after_login` |
| `aS_v` | `sync_sale_list` | `aT_v` | `open_trade_list` |
| `aU_v` | `sync_gift_list` | `aV_v` | `sync_gifts` |
| `aW_v` | `sync_exp_fame` | `aX_v` | `sync_done` |
| `aa_I` | `trade_keys` | `ab_I` | `warehouse_keys` |
| `aY_v` | `open_buy_category` | `aZ_v` | `set_category_list` |
| `ac_I` | `grid_keys` | `a_IZ` | `draw_grid_cursor` |
| `ad_I` | `safe_keys` | `ba_v` | `leave_live` |
| `e_Z` | `save_grid_cursor` | `bb_v` | `open_warehouse` |
| `bc_v` | `set_backpack_grid` | `bd_v` | `set_warehouse_grid` |
| `a_IIZ` | `set_grid` | `f_Z` | `clamp_grid_cursor` |
| `be_v` | `selected_grid_item` | `bf_v` | `open_trade` |
| `ae_I` | `live_menu_keys` | `bg_v` | `open_safe` |
| `bh_v` | `open_management` | `af_I` | `management_keys` |
| `bi_v` | `drop_net` |  |  |

### LiveScreen

| Java | Python | Java | Python |
|---|---|---|---|
| `a_v` | `draw_live_screen` | `bj_v` | `draw_list_screen` |
| `bk_v` | `draw_safe` | `bl_v` | `draw_sell_price` |
| `bm_v` | `draw_cancel_sell` | `bn_v` | `draw_sale_list` |
| `bo_v` | `draw_waiting` | `bp_v` | `draw_registration` |
| `bq_v` | `draw_buy_categories` | `br_v` | `draw_buy_kinds` |
| `bs_v` | `draw_buy_enchants` | `bt_v` | `draw_buy_lots` |
| `b_v` | `is_registered` | `c_v` | `save_login` |
| `d_v` | `load_login` | `bu_v` | `draw_safe_amount` |
| `a_IIII` | `draw_input_box` | `bv_v` | `draw_grid` |

### Popups

| Java | Python | Java | Python |
|---|---|---|---|
| `a_v` | `reset` | `b_v` | `popup_keys` |
| `_timer` | `_tick_timer` | `c_v` | `draw_popup` |
| `b_I` | `draw_popup_frame` | `a_IIII` | `draw_tiled_back` |
| `O_I` | `draw_yes_no` | `c_I` | `draw_ok` |
| `a_T` | `show_text` | `d_I` | `show` |
| `d_v` | `show_bought` | `e_v` | `show_sold` |
| `e_I` | `setup_popup` |  |  |

### Boot

| Java | Python | Java | Python |
|---|---|---|---|
| `a_v` | `draw_boot` | `b_v` | `boot_keys` |
| `b_I` | `is_any_key` |  |  |

### Sound

| Java | Python | Java | Python |
|---|---|---|---|
| `a__I` | `play_sound` | `a_v` | `tick_sound` |
| `a_IZ` | `play_now` | `b_v` | `stop_all` |

### ArrTable

| Java | Python | Java | Python |
|---|---|---|---|
| `a_II` | `get_int` | `b_II` | `get_string` |
| `a_v` | `free` |  |  |

### Font

| Java | Python | Java | Python |
|---|---|---|---|
| `a_v` | `height` | `b_v` | `ascent` |
| `c_v` | `gap` | `a_CII` | `draw_char` |
| `b_C` | `glyph_index` | `a_C` | `char_width` |
| `a_ACII` | `chars_width` | `a_T` | `string_width` |

### Gfx

| Java | Python | Java | Python |
|---|---|---|---|
| `a_G` | `set_graphics` | `a_IIII` | `push_clip` |
| `a_v` | `pop_clip` | `a_MII` | `draw_image` |
| `a_MIII` | `draw_image_anchored` | `a_MIIIIII` | `draw_image_part` |
| `a_IIIII` | `draw_rect` | `b_IIIII` | `fill_rect` |
| `c_IIIII` | `draw_line` | `a_Lg` | `set_font` |
| `a_ACIIIII` | `draw_chars` | `a_TIII` | `draw_string` |
| `b_v` | `make_crc_table` | `a_ABII` | `crc32` |

### Hero

| Java | Python | Java | Python |
|---|---|---|---|
| `a_v` | `reset_inventory` |  |  |

### Item

| Java | Python | Java | Python |
|---|---|---|---|
| `a` | `clear` |  |  |

### LiveAnswer

| Java | Python | Java | Python |
|---|---|---|---|
| `a_v` | `read_s8` | `b_v` | `read_s16` |
| `c_v` | `read_s32` | `a_I` | `read_string` |

### LiveNet

| Java | Python | Java | Python |
|---|---|---|---|
| `a_TI` | `set_address` | `a_v` | `close` |
| `c_v` | `open` | `a_Ls` | `set_listener` |
| `a_I` | `begin_request` | `a_S` | `write_short` |
| `a_B` | `write_byte` | `b_I` | `write_int` |
| `a_Z` | `write_bool` | `b_TI` | `write_string` |
| `b_v` | `send_request` |  |  |

### MapData

| Java | Python | Java | Python |
|---|---|---|---|
| `a_v` | `free` |  |  |

### Midlet

| Java | Python | Java | Python |
|---|---|---|---|
| `startApp_123456` | `run_game` | `constructor_123456` | `construct` |

### NameBuffer

| Java | Python | Java | Python |
|---|---|---|---|
| `b_I` | `move_cursor` | `a_v` | `get_text` |
| `a_T` | `set_text` | `b_v` | `length` |
| `a_I` | `handle_key` |  |  |

### PlayerPool

| Java | Python | Java | Python |
|---|---|---|---|
| `a_v` | `close_all` | `a_TI` | `load` |
| `a_IZ` | `play` | `b_v` | `stop` |
| `g` | `stop_current` | `a_I` | `set_volume` |
| `c_v` | `pause` | `d_v` | `resume` |
| `e_v` | `tick` |  |  |

### ResReader

| Java | Python | Java | Python |
|---|---|---|---|
| `a` | `read` |  |  |

### ScrTable

| Java | Python | Java | Python |
|---|---|---|---|
| `a_I` | `get` | `a_v` | `free` |


### consts (ae.java)

Таблиці модуля `pow/game/consts.py`. Анімації героя названо за полем `Hero`, у яке їх кладе `tick_title` (`hero_anim_N` → `Hero.anim_N`); `fx_anim_N` — кадри ефекту для анімації героя N (і того самого ефекту ворога).

`t` → `softkey_labels`, `u` → `menu_parent`, `v` → `menu_sizes`, `w` → `tier_levels`, `x` → `tier_drop_odds`, `y` → `item_prices`, `z` → `help_topic_start`, `A` → `menu_music`, `B` → `hero_anim_0`, `C` → `hero_anim_1`, `D` → `hero_anim_2`, `E` → `hero_anim_9`, `F` → `hero_anim_3`, `G` → `hero_anim_4`, `H` → `hero_anim_5`, `I` → `hero_anim_6`, `J` → `hero_anim_7`, `K` → `hero_anim_8`, `L` → `hero_anim_10`, `M` → `hero_anim_11`, `N` → `hero_anim_12`, `O` → `hero_anim_13`, `P` → `hero_anim_14`, `Q` → `hero_anim_15_19`, `R` → `hero_anim_20`, `S` → `hero_anim_21`, `T` → `hero_anim_22`, `U` → `hero_anim_23_24`, `V` → `hero_anim_25`, `W` → `hero_anim_26_27`, `X` → `hero_anim_28`, `Y` → `hero_anim_29`, `Z` → `hero_anim_30`, `aa` → `head_anim_0`, `ab` → `head_anim_1`, `ac` → `head_anim_2`, `ad` → `head_anim_3`, `ae` → `body_anim_0`, `af` → `body_anim_1`, `ag` → `body_anim_2`, `ah` → `body_anim_3`, `ai` → `weapon_anim_1`, `aj` → `weapon_anim_2`, `ak` → `weapon_anim_3`, `al` → `fx_anim_15_16`, `am` → `fx_anim_17_19`, `an` → `fx_anim_21`, `ao` → `fx_fire`, `ap` → `fx_anim_24`, `aq` → `fx_anim_26_27`, `ar` → `fx_anim_27_end`, `as_` → `fx_anim_28`, `at` → `fx_anim_29`, `au` → `fx_anim_30`, `av` → `fx_item_10_11`, `aw` → `dir_dx8`, `ax` → `dir_dy8`, `ay` → `squad_offsets`, `az` → `squad_dirty_box`, `aA` → `front_dx`, `aB` → `front_dy`, `aC` → `skill_menu_ids`, `aD` → `skill_menu_index`, `aE` → `equip_slot_order`, `aF` → `hit_box_x`, `aG` → `hit_box_y`, `aH` → `hit_box_w`, `aI` → `hit_box_h`, `aJ` → `general_frame_flags`, `aK` → `weapon_reach`, `aL` → `general_reach`, `aM` → `tier_req_level`, `aN` → `potion_names`, `aO` → `potion_kinds`, `aP` → `potion_percents`, `aQ` → `speed_frame_ms`, `aR` → `stat_up_texts`, `aS` → `troop_names`, `aT` → `dir8_to_dir4`, `aU` → `skill_attack_div`, `aV` → `story_offsets`, `aW` → `menu_links`, `aX` → `difficulty_names`, `aY` → `mode_texts`, `aZ` → `yes_no_ok`, `ba` → `gift_kinds`

## Мультиплеєр (`pow_mp`)

Код клієнта мультиплеєра колись генерував `tools/j2py_mp.py` у `pow_mp/_gen`; тепер це звичайний код.
Java-джерела: `pyport/mp_java/*.java` у гілці `java-reference`.

| Java | Модуль | Клас | Що це |
|---|---|---|---|
| `g` | `pow_mp/mp_canvas.py` | `MpCanvas` | канвас: екрани, меню, бої |
| `g` (частина) | `pow_mp/mp_canvas_draw.py` | `DrawMixin` | примітиви: текст, прямокутники, лінії, половинки зображень, числа, рамки, кнопки |
| `g` (частина) | `pow_mp/mp_canvas_battle.py` | `BattleMixin` | бій: ходи, бійці й анімації, смуга таймінгу, шкода, HP, картки дій |
| `g` (частина) | `pow_mp/mp_canvas_net.py` | `NetMixin` | з'єднання: запити, відповіді `on_answer`, логін, розриви, помилки |
| `g` (частина) | `pow_mp/mp_canvas_input.py` | `InputMixin` | клавіші: меню, так/ні, попапи, сітка літер для імені й id |
| `g` (частина) | `pow_mp/mp_canvas_screens.py` | `ScreensMixin` | екрани поза боєм: фони, вікна, рекорди, атрибути, скіли, довідка, помилка |
| `g` (частина) | `pow_mp/mp_canvas_assets.py` | `AssetsMixin` | завантаження й звільнення зображень і спрайтів |
| `g` (частина) | `pow_mp/mp_canvas_options.py` | `OptionsMixin` | опції в RecordStore, текстові хелпери, музика й гучність |
| `m` | `pow_mp/mp_game.py` | `MpGame` | конкретний канвас (`m extends g`), музика меню |
| `l` | `pow_mp/consts.py` | `Consts` | таблиці констант (інтерфейс `l`) |
| `i` | `pow_mp/gfx.py` | `Gfx` | малювання, кліп, текст, CRC-32 |
| `j` | `pow_mp/font.py` | `Font` | бітмап-шрифт `0_font.png` |
| `f` | `pow_mp/draw.py` | `Draw` | малювання картинок і прямокутників на Graphics |
| `k` | `pow_mp/answer.py` | `Answer` | відповідь сервера, читання полів |
| `d` | `pow_mp/frame_reader.py` | `FrameReader` | читання кадру з потоку |
| `e` | `pow_mp/frame_writer.py` | `FrameWriter` | запис кадру запиту (не використовується: його замінив `NetThread`) |
| `a` | `pow_mp/sprite_frames.py` | `SpriteFrames` | кадри SP2 |
| `c` | `pow_mp/player_pool.py` | `PlayerPool` | пул програвачів звуку |
| `h` | `pow_mp/net_thread.py` | `NetThread` | мережевий потік |
| `n` | `pow_mp/res_reader.py` | `ResReader` | читання ресурсів |
| `Main` | `pow_mp/midlet.py` | `Midlet` | MIDlet |

### Поля й методи малих класів `pow_mp`

- **SpriteFrames**: `a` → `count`, `b` → `data`, `c` → `src_x`, `d` → `src_y`, `e` → `w`, `f` → `h`, `g` → `anchor_x`, `h` → `anchor_y`, `a_v` → `free`
- **Font**: `a` → `image`, `b` → `glyph_w`, `c` → `glyph_h`, `d` → `space_w`, `e` → `plte_offset`, `a_CII` → `draw_char`, `b_C` → `glyph_index`, `a_C` → `char_width`, `a_ACII` → `chars_width`, `a_T` → `string_width`
- **Gfx**: `a` → `crc_table`, `b` → `g`, `c` → `clip_x`, `d` → `clip_y`, `e` → `clip_w`, `f` → `clip_h`, `g` → `font`, `a_G` → `set_graphics`, `a_MIIIIII` → `draw_image_part`, `a_IIIII` → `fill_rect`, `a_Lj` → `set_font`, `a_ACIIIII` → `draw_chars`, `a_TIII` → `draw_string`, `a_GTIII` → `draw_string_on`, `a_v` → `make_crc_table`, `a_ABII` → `crc32`
- **Draw**: `a_GMIII` → `draw_image`, `a_GMIIIIII` → `draw_image_part`, `a_GIIIII` → `draw_rect`, `a_GIIIIII` → `draw_frame`, `b_GIIIII` → `fill_rect`, `a_GIIII` → `draw_hline`, `b_GIIII` → `draw_vline`, `c_GIIIII` → `draw_line_color`, `c_GIIII` → `draw_line`
- **Answer**: `a` → `data`, `b` → `pos`, `a_v` → `read_s8`, `b_v` → `read_s16`, `c` → `read_s32`, `a_I` → `read_string`
- **FrameReader**: `a` → `stream`, `b` → `length`, `c` → `header`, `a_v` → `close`, `b_v` → `read_frame`
- **FrameWriter**: `a` → `stream`, `b` → `buf`, `c` → `length`, `d` → `frame`, `e` → `unused`, `a_v` → `close`, `a_I` → `write_short`, `a_B` → `write_byte`, `b_I` → `write_int`, `a_TI` → `write_string`, `b_v` → `send`
- **MpGame**: `fb` → `players`, `fc` → `requested_music`, `fd` → `music`, `v_I` → `request_music`, `ak_v` → `tick_music`, `b_IZ` → `play_music`, `ag_v` → `stop_music`
- **Midlet**: `a` → `display`, `b` → `canvas`, `c` → `started`
- **PlayerPool**: `a_TI` → `load`, `a_IZ` → `play`, `a_v` → `stop`, `a_I` → `set_volume`, `b` → `tick`
- **ResReader**: `a` → `read`
- **NetThread**: `a` → `last_opcode`, `b` → `conn`, `e` → `game`, `g` → `free`, `h` → `idle_frames`, `i` → `unused`, `j` → `connected`, `k` → `running`, `l` → `connect_requested`, `m` → `host`, `n` → `port`, `a_TI` → `set_address`, `a_v` → `close`, `a_Lg` → `set_game`, `a_I` → `begin`, `a_B` → `write_byte`, `b_I` → `write_int`, `b_TI` → `write_string`, `b_v` → `send`

### MpCanvas (g.java)

Довгі `paint_screen` (`g.java:474`), `handle_key` (`g.java:2661`) і `on_answer` (`g.java:1888`) були одним
ланцюгом `if/elif` за станом або опкодом. Тепер кожна гілка — окремий метод, а метод бере його з таблиці:
`_PAINT_BY_STATE` → `_paint_<екран>`, `_KEYS_BY_STATE` → `_keys_<екран>`, `_ANSWER_BY_OPCODE` → `_on_<відповідь>`
(номер стану чи опкоду — у коментарі біля `def`). `step_turn_anim` (`g.java:4176`) так само розкладено на
`_anim_after_*` за видом анімації, що закінчилась.

Так само в одиночній грі: `Live.on_answer` (`as.java:601-990`) бере `_on_<відповідь>` з `_ANSWER_BY_OPCODE`,
`Menus.key_fire` (`e.java:688-1000`) — `_fire_<меню>` з `_FIRE_BY_MENU`.

Імена взято з коду та протоколу (`pow_server/messages.py`). Поля, які гра читає з
відповіді, але ніде не використовує, звуться `profile_unused*` / `profile_cr`; `popup_line1..5`
у Java ніде не присвоюються.

Поля: `a` → `app_version`, `b` → `game`, `e` → `screen_g`, `f` → `buffer`, `g` → `buffer_g`, `h` → `rng`, `i` → `user_id`, `j` → `password`, `l` → `midlet`, `m` → `key`, `n` → `font_white`, `o` → `font_orange`, `p` → `font_gray`, `q` → `font_green`, `r` → `server_host`, `s` → `server_port`, `t` → `game_ver`, `x` → `popup_shown`, `y` → `popup_cursor`, `z` → `popup_kind`, `C` → `letter_cursor`, `H` → `pause_request`, `I` → `music_to_resume`, `J` → `paused`, `N` → `login_time`, `Y` → `rank_names`, `Z` → `rank_ranks`, `aa` → `rank_values`, `ac` → `my_ranks`, `ad` → `my_rank_value`, `ae` → `rank_kind`, `am` → `volume`, `an` → `speed`, `ao` → `invitation_saved`, `ap` → `invitation`, `ar` → `face`, `as_` → `level`, `at` → `wins`, `au` → `losses`, `av` → `hp`, `aw` → `weapon`, `ax` → `fame`, `ay` → `exp`, `az` → `gold`, `aA` → `duel_grade`, `aB` → `mission_grade`, `aC` → `attr_hp`, `aD` → `attr_hp_bonus`, `aE` → `attr_mp`, `aF` → `attr_mp_bonus`, `aG` → `attr_attack`, `aH` → `attr_attack_bonus`, `aI` → `attr_defense`, `aJ` → `attr_defense_bonus`, `aN` → `notices_left`, `aP` → `stage_count`, `aQ` → `stage`, `aT` → `turn_record_count`, `aU` → `battle_won`, `aV` → `reward_gold`, `aW` → `reward_grade`, `aX` → `reward_fame`, `aY` → `reward_exp`, `aZ` → `reward_rank`, `bf` → `skill_count`, `bg` → `leaving_slot`, `bh` → `my_slot`, `by` → `room_bg`, `bz` → `room_mode`, `bD` → `skill_slot_count`, `bE` → `skill_slots`, `bG` → `input_text`, `bH` → `stage_title`, `bI` → `loot`, `bK` → `hp_bar_w`, `bM` → `fighter_name`, `bN` → `fighter_quote_start`, `bO` → `fighter_quote_win`, `bP` → `fighter_alt_name`, `bQ` → `fighter_present`, `bR` → `fighter_slot`, `bS` → `fighter_level`, `bT` → `fighter_wins`, `bU` → `fighter_losses`, `bV` → `fighter_max_hp`, `bW` → `fighter_hp`, `bX` → `fighter_mp`, `bY` → `fighter_weapon`, `bZ` → `fighter_face`, `ca` → `fighter_kind`, `cb` → `turn_actions`, `cf` → `fighter_hp_target`, `cg` → `fighter_mp_target`, `ch` → `fighter_hp_step`, `ci` → `fighter_mp_step`, `cj` → `fighter_hp_delta`, `ck` → `fighter_x`, `cl` → `fighter_y`, `cn` → `fighter_frame`, `co` → `fighter_blink`, `cp` → `fighter_status`, `cq` → `fighter_status_ticks`, `cs` → `key_in`, `ct` → `cur_slot`, `cE` → `name`, `cF` → `quote_start`, `cG` → `quote_win`, `cH` → `skill_levels`, `cI` → `skill_costs`, `cJ` → `turn_hps`, `cK` → `turn_bytes`, `cL` → `loop_i`, `cM` → `loop_j`, `cN` → `loop_k`, `cO` → `box_x`, `cP` → `box_y`, `cQ` → `canvas_w`, `cR` → `canvas_h`, `cS` → `screen_w`, `cT` → `screen_h`, `cU` → `draw_x`, `cV` → `draw_y`, `cW` → `center_x`, `cX` → `center_y`, `cY` → `state`, `cZ` → `prev_state`, `da` → `state_ticks`, `db` → `skill_cursor`, `dd` → `mpic_images`, `de` → `face_images`, `df` → `ui_images`, `dg` → `act_images`, `dh` → `number_images`, `di` → `arrow_images`, `dj` → `bg_images`, `dk` → `border_v_image`, `dl` → `back_image`, `dm` → `border_h_image`, `dn` → `titlebox_image`, `do_` → `menu_icon_image`, `dp` → `title_image`, `dq` → `press_image`, `dr` → `gamevil_image`, `dt` → `softkey_image`, `dP` → `net`, `dQ` → `request_opcode`, `dR` → `answer_status`, `dS` → `logo_y`, `dT` → `thread`, `dU` → `cursor_stack`, `dV` → `state_stack`, `dW` → `stack_depth`, `dY` → `painted`, `ea` → `disconnecting`, `ec` → `pending_state`, `ed` → `text_lines`, `ee` → `frame_start`

Методи: `a_T` → `log`, `a_v` → `init_screen`, `b_T` → `load_image`, `a_J` → `sleep`, `a_I` → `request_pause`, `b_v` → `apply_pause`, `c_v` → `main_loop`, `d_v` → `paint_screen`, `a_GIITI` → `draw_text_centred_on`, `a_IITI` → `draw_text_centred`, `b_GIITI` → `draw_text_left_on`, `b_IITI` → `draw_text_left`, `a_GTIIII` → `draw_text_colored`, `a_IIIII` → `draw_rect`, `b_IIIII` → `fill_rect`, `a_GIIIII` → `fill_rect_on`, `a_GI` → `set_color`, `b_GIIIII` → `draw_line_color`, `a_GIIII` → `draw_line`, `a_GIII` → `draw_dot`, `a_IIM` → `draw_image`, `a_GIIM` → `draw_image_on`, `e_v` → `draw_buffer`, `c_I` → `send_request`, `f_v` → `load_ui_images`, `g_v` → `load_ui_images2`, `h_v` → `load_menu_images`, `i_v` → `free_battle_images`, `a_Lk` → `on_answer`, `f_I` → `handle_key`, `j_v` → `update_bars`, `k_v` → `reset_turn`, `l_v` → `login`, `m_v` → `connect`, `n_v` → `disconnect`, `o_v` → `on_disconnect`, `g_I` → `on_net_error`, `c_GIIIII` → `draw_box`, `h_I` → `place_fighter`, `i_I` → `set_state`, `K_v` → `save_options`, `L_v` → `load_options`, `a_ABII` → `read_utf`, `c_T` → `cut_at_control`, `d_T` → `trim_right`, `k_I` → `push_state`, `l_I` → `reset_state_stack`, `N_v` → `pop_state`, `m_I` → `pop_states`, `O_v` → `free_frame_images`, `n_I` → `load_bg`, `a_AMTI` → `load_numbered_image`, `b_AMTI` → `load_named_image`, `a_AMALaT` → `load_sprite`, `a_AMALaTI` → `load_sprite_dir`, `c_GIIII` → `draw_panel`, `a_II` → `draw_letter_grid`, `p_I` → `letter_grid_keys`, `b_II` → `draw_letter_grid_space`, `q_I` → `letter_grid_space_keys`, `s_I` → `start_music`, `t_I` → `start_sound`, `u_I` → `queue_music`, `ah_v` → `get_volume`, `ai_v` → `volume_down`, `aj_v` → `volume_up`, `b_GIIII` → `draw_number`, `M_v` → `draw_popup`, `j_I` → `popup_keys`, `S_v` → `check_invite_timeout`, `J_v` → `clear_fighters`, `W_v` → `draw_background`, `n_G` → `draw_back_tiles`, `d_GIIII` → `draw_border_v`, `e_GIIII` → `draw_border_h`, `l_G` → `draw_window_bg`, `ag_v` → `stop_music`

Поля бою, анімації, спрайтів і дрібних вікон: `c` → `title`, `d` → `timer_ticks`, `k` → `menu_size`, `u` → `wait_started`, `v` → `wait_start_time`, `w` → `painting_blocked`, `A` → `password_login`, `B` → `quote_step`, `D` → `exit_prompt`, `E` → `exit_cursor`, `F` → `exit_prompt_time`, `G` → `exit_asked`, `K` → `loop_started`, `L` → `connecting`, `M` → `logo_time`, `O` → `room_dirty`, `P` → `relogin_to_menu`, `Q` → `anim_frame`, `R` → `anim_length`, `S` → `attacker`, `T` → `target`, `U` → `target2`, `V` → `target_reaction`, `W` → `target2_reaction`, `X` → `damage_tick`, `ab` → `rank_list_kind`, `af` → `rank_list_state`, `ag` → `popup_line1`, `ah` → `popup_line2`, `ai` → `popup_line3`, `aj` → `popup_line4`, `ak` → `popup_line5`, `al` → `popup_style`, `aq` → `skip_error_screen`, `aK` → `profile_cr`, `aL` → `profile_unused1`, `aM` → `profile_unused2`, `aR` → `round_no`, `aS` → `hit_score`, `ba` → `choose_secs`, `bb` → `allies_alive`, `bc` → `enemies_alive`, `bd` → `notice_kind`, `be` → `help_page`, `bi` → `slot_found`, `bj` → `hud_dirty`, `bk` → `show_record`, `bl` → `run_dx`, `bm` → `run_dy`, `bn` → `draw_mirrored`, `bo` → `saved_anim_frame`, `bp` → `skill_id`, `bq` → `skill_taken`, `br` → `number_negative`, `bs` → `skill_ready`, `bt` → `bar_shown`, `bu` → `msg_first_line`, `bv` → `help_first_line`, `bw` → `msg_copy_line`, `bx` → `card_half`, `bA` → `target_cursor`, `bB` → `chosen_action`, `bC` → `turn_rec`, `bF` → `notice_lines`, `bJ` → `tmp`, `bL` → `stage_text`, `cc` → `fighter_anim`, `cd` → `fighter_anim_tick`, `ce` → `fighter_anim_len`, `cm` → `fighter_fx_frame`, `cr` → `fighter_cr`, `cu` → `stat_value`, `cv` → `loading_msg`, `cw` → `error_msg`, `cx` → `win_x`, `cy` → `win_y`, `cz` → `bar_speed`, `cA` → `bar_x`, `cB` → `skill_order`, `cC` → `anim_id`, `cD` → `card_face`, `dc` → `tick_ms`, `ds` → `logo_image`, `du` → `body_images`, `dv` → `body_frames`, `dw` → `head_images`, `dx` → `head_frames`, `dy` → `weapon_images`, `dz` → `weapon_frames`, `dA` → `sword_images`, `dB` → `sword_frames`, `dC` → `effect_images`, `dD` → `effect_frames`, `dE` → `effect3_frames`, `dF` → `shadow_images`, `dG` → `shadow_frames`, `dH` → `monster_images`, `dI` → `monster_frames`, `dJ` → `mon_weapon_images`, `dK` → `mon_weapon_frames`, `dL` → `mon_effect_images`, `dM` → `mon_effect_frames`, `dN` → `mon_sword_images`, `dO` → `mon_sword_frames`, `dX` → `relogin`, `dZ` → `ping_misses`, `eb` → `ping_off`, `aO` → `notice_page`

Методи бою, анімації й вікон: `a_G` → `draw_menu_cursor`, `b_I` → `set_timer`, `b_IIM` → `draw_right_half`, `b_GIIM` → `draw_right_half_on`, `a_GIIIM` → `draw_right_half_h`, `a_IIMZ` → `draw_right_aligned`, `a_GIIMII` → `draw_left_half_row`, `b_GIIIM` → `draw_right_half_row1`, `c_IIM` → `draw_left_half`, `c_GIIM` → `draw_left_half_on`, `c_GIIIM` → `draw_left_half_h`, `d_I` → `menu_keys`, `e_I` → `yes_no_keys`, `p_v` → `show_error_screen`, `q_v` → `menu_select`, `r_v` → `draw_notice`, `s_v` → `draw_turn_fighters`, `t_v` → `draw_fighter_hit`, `u_v` → `draw_fighter_evade`, `v_v` → `draw_fighter_dying`, `w_v` → `draw_fighter_run`, `x_v` → `draw_fighter_anim`, `b_G` → `draw_fighter_idle`, `b_GI` → `draw_quotes`, `y_v` → `draw_fighter_record`, `c_G` → `draw_fighters`, `d_G` → `draw_target_marker`, `z_v` → `draw_stage_intro`, `A_v` → `start_timing_bar`, `e_G` → `draw_timing_bar`, `f_G` → `draw_timing_cursor`, `B_v` → `start_timing`, `C_v` → `stop_timing`, `a_GAMALaI` → `draw_sprite_frame`, `c_GI` → `draw_fighter`, `a_IZ` → `draw_fighter_effects`, `D_v` → `step_turn_anim`, `E_v` → `next_turn_record`, `F_v` → `update_reactions`, `G_v` → `start_reaction`, `H_v` → `draw_stage_complete`, `I_v` → `draw_damage`, `g_G` → `draw_hp_bars`, `b_GIII` → `draw_number1_on`, `c_GIII` → `draw_number2_on`, `d_GIII` → `draw_number3_on`, `e_GIII` → `draw_damage_number`, `a_III` → `draw_number5`, `f_GIII` → `draw_number0_on`, `b_III` → `draw_number0`, `c_III` → `draw_number1`, `d_III` → `draw_number0_b`, `e_III` → `draw_number1_b`, `h_G` → `draw_skill_menu`, `P_v` → `draw_battle_result`, `Q_v` → `tick_status_effects`, `R_v` → `draw_action_cards`, `i_G` → `draw_round`, `j_G` → `draw_action_pad`, `d_GI` → `draw_battle_prompt`, `T_v` → `draw_help`, `U_v` → `draw_menu_icons`, `V_v` → `load_status_effect`, `e_GI` → `draw_status_effect`, `X_v` → `noop`, `Y_v` → `draw_hp_bar_frames`, `o_I` → `draw_hp_bar_frame`, `k_G` → `draw_window`, `a_GTIIIIZZ` → `draw_button`, `m_G` → `draw_battle_hud`, `o_G` → `draw_options_bg`, `Z_v` → `draw_records`, `aa_v` → `draw_attributes`, `p_G` → `draw_skills_bg`, `ab_v` → `draw_skill_slots`, `ac_v` → `draw_exp_fame_gold`, `q_G` → `draw_quote_bg`, `r_G` → `draw_quote_prompt`, `s_G` → `draw_name_prompt`, `t_G` → `draw_input_line`, `u_G` → `draw_name_confirm`, `v_G` → `draw_exit_confirm`, `ad_v` → `draw_error`, `w_G` → `draw_challenge_bg`, `f_GI` → `draw_user_id_prompt`, `ae_v` → `draw_loading`, `af_v` → `draw_waiting`, `c_II` → `draw_softkeys`, `r_I` → `draw_ok_button`

### Consts (mp_java/l.java)

`ef` → `speed_frame_ms`, `eg` → `anim_first_frame`, `eh` → `anim_length`, `ei` → `eff2_behind_pose1`, `ej` → `eff2_behind_pose2`, `ek` → `bare_weapon_behind_pose2`, `el` → `weapon_behind_pose0`, `em` → `weapon_behind_pose1`, `en` → `weapon_behind_pose2`, `eo` → `mon_weapon_behind`, `ep` → `anim_steps`, `eq` → `ui_dx`, `er` → `ui_dy`, `es` → `act_dx`, `et` → `act_dy`, `eu` → `ui_dx2`, `ev` → `ui_dy2`, `ew` → `help_pages`, `ex` → `help_controls`, `ey` → `help_controls_lines`, `ez` → `help_menu`, `eA` → `help_menu_lines`, `eB` → `help_duel`, `eC` → `help_duel_lines`, `eD` → `help_mission`, `eE` → `help_mission_lines`, `eF` → `help_about`, `eG` → `help_about_lines`, `eH` → `help_network`, `eI` → `help_network_lines`, `eJ` → `skill_info`, `eK` → `skill_names`, `eL` → `grades`, `eM` → `main_menu`, `eN` → `duel_menu`, `eO` → `mission_menu`, `eP` → `character_menu`, `eQ` → `help_topics`, `eR` → `rank_menu`, `eS` → `rank_view_menu`, `eT` → `softkeys`, `eU` → `input_prompts`, `eV` → `login_texts`, `eW` → `option_texts`, `eX` → `texts`, `eY` → `error_lines`, `eZ` → `error_line_counts`, `fa` → `loading_texts`

