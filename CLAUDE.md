# Path of a Warrior — Python

## Tech Stack

- **Language:** Python 3 + pygame-ce (`pyport/`)
- **Target resolution:** 240×320 (QVGA), scaled by `POW_SCALE`
- **Tile size:** 27×27 px
- **Server (Live, multiplayer, saves):** `pyport/pow_server` (WebSocket / TCP)

## Project Context

"Path of a Warrior": the single-player campaign and the multiplayer screens are one game with one
engine (`pyport/pow/game`, the multiplayer screens in `pyport/pow/game/online` run as a state of
`GameCanvas`). `pyport/README.md` describes the game, its options and how to run it;
`docs/plans/one_engine_plan.md` is the plan that merged the two parts. The history of the port
(the J2ME original, the Godot attempt) is in git and in `docs/analysis`; the code does not refer
to it.

## Rules

- New code goes into `pyport/` (Python); every module, class and name is ours and named for what
  it does
- Comments explain what the code does now, not where it came from: no references to the
  original game's code, no port markers
- Behaviour changes the player asked for are documented in `pyport/README.md`; an option that
  keeps the old behaviour (`POW_...` in `config.py`) only when the old one is still wanted
  (`tools/shot.py` sets the options so that the baseline screenshots stay)
- Code for the Godot version goes into `godot/` (`godot/README.md`, `docs/GODOT_PLAN.md`): step 1
  there is to move the game over as it is, a 3D world with the original 2D sprites;
  `python godot/tools/import_original.py` makes its data. Godot tests:
  `godot --headless --path godot/client res://tests/runner.tscn` (also in CI)
- Do not modify existing working functionality unless explicitly asked
- Run `python -m pytest` in `pyport/` before pushing
