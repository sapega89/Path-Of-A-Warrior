# Path of a Warrior — Godot 4

## Tech Stack

- **Main project:** Godot 4.5, GDScript, in `godot/client` (game and tests in one project). The
  game is offline: no server, the hero and the settings are saved on the computer
- **Data:** `python godot/tools/import_original.py` makes `godot/client/data` and
  `godot/client/assets/original` from the original files
- **Reference only:** `pyport/` (Python + pygame-ce) describes how the original game behaves. No new
  features go there; change it only when asked

## Project Context

`godot/README.md` describes the layout and how to run the game and the tests;
`docs/GODOT_PLAN.md` is the plan of the port. The code is moving to the usual Godot structure step
by step: what old code still breaks is counted in `godot/tools/standards_baseline.json` (see
"Checks" below). Every change follows the rules below, also when the code around it is still in the
old style.

## Rules: Godot structure

- A new screen is a scene: `screens/<name>/<name>_screen.tscn` with its `.gd` next to it. Its layout
  (containers, labels, buttons) lives in the `.tscn`, not in `Label.new()` / `add_child` code.
  Nodes the script needs are `%UniqueName` + `@onready var`. Code builds nodes only for lists whose
  length is known at run time (an inventory grid, a ranking), and then instances a small `.tscn`
  for one row or cell
- When a screen is changed for more than a small fix, move it to a scene in the same PR
- Every screen extends `BaseScreen` (`scripts/screens/base_screen.gd`): it takes the back key.
  A screen overrides `go_back()` when its back does more, `handles_back()` when the key is not
  back, and `_screen_input()` for its other keys; it never writes its own `_unhandled_input`
  with `ui_cancel`
- The hero is read with `Profile.load_or_new(path)` and saved with `save(path)`, where `path`
  is `BaseScreen.profile_path()` (`Profile.PATH`, user://hero.json, or a test's file); do not
  read `Router.params.profile_path` or write `user://` files by hand
- Styles come from `theme.tres` and theme type variations, not from `add_theme_*_override` in code
- Shared classes have a `class_name`; do not add `const X := preload("res://...gd")` for them
- Calls go down, signals go up: a child node never reaches its parent or siblings by path;
  autoloads only for state that is truly global
- Godot's own nodes and methods come before our own code for the same thing:
  - what the player clicks or taps is a `Button` / `TextureButton` with its `pressed` signal, not a
    picture drawn in `_draw` with hit tests by coordinates; a bar or an orb is a
    `ProgressBar` / `TextureProgressBar`
  - a change over time (a fade, a flash, a blink, text typed out) is a `Tween` or an
    `AnimationPlayer`, not a counter in `_process`; only `MapSim` keeps its own tick
  - input is read with `Input.is_action_just_pressed()` and the other `Input` / `InputEvent`
    methods, not with our copies of them
  - a pause is `get_tree().paused`, with `process_mode` on the nodes that keep running
- The objects of the world (the hero, an enemy, an effect, a prop) are scenes (`.tscn`) that code
  instances; code builds nodes only for what map data describes (the ground, the walls)
- Game logic stays in classes without nodes (`RefCounted`: map simulation, battle, rules), and
  scenes only show their state. Logic never touches nodes, the screen or input
- Folders by feature (`screens/gear/`, `world/hero/`), file names snake_case, node names PascalCase

## Rules: code quality

- SOLID / KISS / DRY / YAGNI in practice:
  - one class, one job; a file over ~600 lines or a function over ~50 lines is a sign to split
    it, and a new one is not allowed to grow past that
  - a long `match` / `if` chain over message or action types becomes a table of handlers
  - the same code in a third place becomes a shared function, scene or base class
  - no code "for later": no unused options, parameters, layers or abstractions
- Follow the official GDScript style guide, its code order too: signals, enums, consts, static
  vars, `@export` vars, vars, `@onready` vars, then the methods. `gdformat` and `gdlint`
  (gdtoolkit 4.5.0, config `godot/client/gdlintrc`) run in CI
- Type every variable, parameter and return value, with the class's own name (`Profile`,
  `MapSim`), not `RefCounted`, `Node` or `Variant` in its place; an array of one kind is typed
  (`Array[int]`)
- Names are ours and say what the thing does; comments explain what the code does now, not where
  it came from (no references to the original game's code or to `pyport`, no port markers)
- Magic numbers become named constants or data in `data/*.json`
- Do not modify existing working functionality unless explicitly asked; refactoring keeps the
  behaviour, the node names and the public fields the tests use

## Checks

`python godot/tools/check_standards.py` (run in CI) counts, file by file, what breaks the rules
above that gdlint does not see: untyped or `RefCounted` declarations, UI or world nodes built
with `.new()`, theme overrides in code, `pyport` in comments, `Router.params` read for the
hero's path, `preload` of a script, files over 600 lines, functions over 50 lines, the code order.
`godot/tools/standards_baseline.json` keeps the counts of the old code:

- new code adds nothing to them, so a feature never waits for old code to be cleaned
- a PR that cleans old code lowers them with `--update` in the same PR (CI asks for it)
- a line that has to break a line rule says why at its end: `# standards: allow <rule> (<why>)`

## Rules: tests and PRs

- Every behaviour change or new screen comes with a test in `godot/client/tests/test_*.gd`
- Before pushing: `godot --headless --path godot/client res://tests/runner.tscn` passes, and the
  run adds no new `ERROR` lines to the log; in `godot/client`:
  `gdformat --check scripts screens tests tools lab` and `gdlint scripts screens tests tools lab`;
  in the repo root: `python godot/tools/check_standards.py`
- `.uid` and `.import` files are committed, as Godot asks: they keep the ids that scenes refer to
  and the import settings of each asset. After adding a script, a shader or an asset, run the
  import (`godot --headless --path godot/client --import`) and commit the files it makes; CI
  fails when the import makes one that is not committed
- CI screenshots (`tools/shots.tscn`) must not change unless the change is meant to change them
- Small PRs: one screen group or one module at a time; do not mix a refactor with a new feature
- Behaviour changes the player asked for are documented in `godot/README.md`
- Changes to `pyport/`, when asked: run `python -m pytest` in `pyport/` before pushing
