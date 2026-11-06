# Path of a Warrior — Python Port

## Tech Stack

- **Language:** Python 3 + pygame-ce (`pyport/`); browser build via pygbag
- **Target resolution:** 240×320 (QVGA)
- **Tile size:** 27×27 px
- **Multiplayer / Live server:** `pyport/pow_server` (WebSocket / TCP)

## Project Context

This is a Python port of the original J2ME mobile game "Path of a Warrior" (and its
Multiplayer jar). The decompiled Java sources it was ported from were removed from the tree;
they stay in git in the branch `java-reference` (e.g. `git show origin/java-reference:ag.java`,
`git show origin/java-reference:pyport/mp_java/g.java`). `JAVA_REFERENCE.md` explains what each Java
class does, and
`pyport/README.md` describes the port, its fixes and how to run it.
The earlier Godot port and the J2ME emulator files were removed; the Godot audit stays in
`docs/analysis/05_godot_audit.md`.

## Rules

- New code goes into `pyport/` (Python), or into `godot/` for the Godot version
  (`godot/README.md`, `docs/GODOT_PLAN.md`): step 1 there is to move the game over as it is,
  3D world with the original 2D sprites; `python godot/tools/import_original.py` makes its data.
  Godot tests: `godot --headless --path godot/client res://tests/runner.tscn` (also in CI)
- Before implementing anything — analyze the original Java source first (branch `java-reference`)
- Keep the Java behaviour; the Java classes may be split into modules/mixins by
  responsibility (keep the `# file.java:FROM-TO` comments). Mark deliberate changes (`PORT-EXTRA`,
  `DECOMP_FIX`, `ORIG_BUG`) as `pyport/README.md` does
- Names are being refactored from the obfuscated Java ones to meaningful ones;
  `pyport/NAMES.md` maps every Java name to its Python name. Keep the `# file.java:FROM-TO`
  comments and add new names to `NAMES.md`
- Do not modify existing working functionality unless explicitly asked
- Run `python -m pytest` in `pyport/` before pushing
