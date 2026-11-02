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

Методи поки мають Java-імена; їхні нові імена додаються сюди з наступним кроком.
