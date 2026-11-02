# Path of a Warrior — Python Port

## Tech Stack

- **Language:** Python 3 + pygame-ce (`pyport/`); browser build via pygbag
- **Target resolution:** 240×320 (QVGA)
- **Tile size:** 27×27 px
- **Multiplayer / Gamevil Live server:** `pyport/pow_server` (WebSocket / TCP)

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

- New code goes into `pyport/` (Python)
- Before implementing anything — analyze the original Java source first (branch `java-reference`)
- Literal port: keep the Java structure and names; mark deliberate changes (`PORT-EXTRA`,
  `DECOMP_FIX`, `ORIG_BUG`) as `pyport/README.md` does
- Do not modify existing working functionality unless explicitly asked
- Run `python -m pytest` in `pyport/` before pushing
