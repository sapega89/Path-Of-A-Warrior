# Path of a Warrior — Godot Port

## Tech Stack

- **Engine:** Godot 4.5
- **Language:** GDScript
- **Target resolution:** 240×320 (QVGA)
- **Tile size:** 27×27 px

## Project Context

This is a Godot 4.5 port of the original J2ME mobile game "Path of a Warrior".
The decompiled Java source files (*.java) in the project root serve as reference for the port.
`JAVA_REFERENCE.md` explains what each Java class does.

## Rules

- All new code must be written in **GDScript** for **Godot 4.5**
- Do not use deprecated Godot 3.x APIs
- Do not modify existing working functionality unless explicitly asked
- Before implementing anything — analyze the original Java source first
- **Prefer scenes over scripts:** build everything as `.tscn` scenes first; attach a script only when logic cannot be expressed through the scene structure alone
- If a scene can work without a script — it must work without a script
- **Break work into tasks:** before implementing, always decompose into discrete tasks using TaskCreate; mark each task in_progress when starting and completed when done
- **Visual first:** if a part of the UI can be built as a static scene (layout, colors, nodes) — build it first, wire up logic after
