"""Checks the Godot client's code against the rules of CLAUDE.md that gdlint does not see.

Each rule counts its violations in each file of the game's code (scripts, screens).
standards_baseline.json keeps the counts of the code as it is: a change may lower them and never
raise them, and a file that is not in it has none. So new code follows the rules from its first
line, and old code is cleaned up step by step. An old file or function already too long may still
take a feature's lines; a new one may not be too long. Run from the repo root, with gdtoolkit
4.5.0 installed:

    python godot/tools/check_standards.py           # the check CI runs
    python godot/tools/check_standards.py --update  # writes the lower counts after a clean-up

A line that has to break a line rule says why at its end: `# standards: allow <rule> (<why>)`.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "client"
DIRS = ("scripts", "screens")
BASELINE = Path(__file__).with_name("standards_baseline.json")
MAX_FILE_LINES = 600
MAX_FUNCTION_LINES = 50

CONTROLS = (
    "Control|Label|RichTextLabel|Button|TextureButton|CheckBox|CheckButton|OptionButton|"
    "MenuButton|LinkButton|LineEdit|TextEdit|SpinBox|HSlider|VSlider|ProgressBar|"
    "TextureProgressBar|TextureRect|ColorRect|NinePatchRect|Panel|PanelContainer|Container|"
    "BoxContainer|VBoxContainer|HBoxContainer|GridContainer|FlowContainer|HFlowContainer|"
    "VFlowContainer|MarginContainer|CenterContainer|ScrollContainer|AspectRatioContainer|"
    "TabContainer|SubViewportContainer|ItemList|Tree"
)
WORLD_NODES = (
    "Node2D|Node3D|Sprite2D|Sprite3D|AnimatedSprite2D|AnimatedSprite3D|MeshInstance3D|"
    "MultiMeshInstance3D|Camera2D|Camera3D|DirectionalLight3D|OmniLight3D|SpotLight3D|"
    "WorldEnvironment|GPUParticles2D|GPUParticles3D|CPUParticles2D|CPUParticles3D|Label3D|"
    "Decal|StaticBody3D|CharacterBody3D|Area3D|CollisionShape3D|AnimationPlayer|SubViewport|"
    "Line2D|Polygon2D|Timer"
)

# A rule that counts lines: its pattern, and the fix it asks for.
LINE_RULES = {
    "weak_type": (
        re.compile(r"(?::|->)\s*RefCounted\b|\[RefCounted\]"),
        "type it with the class's own name (Profile, MapSim, ...), not RefCounted",
    ),
    "ui_in_code": (
        re.compile(rf"\b(?:{CONTROLS})\.new\("),
        "put the layout in the .tscn; a list instances a small .tscn for one row or cell",
    ),
    "nodes_in_code": (
        re.compile(rf"\b(?:{WORLD_NODES})\.new\("),
        "make the object a .tscn and instance it (code builds only what map data describes)",
    ),
    "theme_in_code": (
        re.compile(r"\badd_theme_\w+_override\(|\bStyleBox(?:Flat|Texture|Line|Empty)\.new\("),
        "take the style from theme.tres and a theme type variation",
    ),
    "pyport_ref": (
        re.compile(r"pyport", re.IGNORECASE),
        "say what the code does now, not where it came from",
    ),
    "profile_path_param": (
        re.compile(r"\.get\(\s*\"profile_path\""),
        "read the hero's path with BaseScreen.profile_path()",
    ),
    "script_preload": (
        re.compile(r"preload\(\s*\"res://[^\"]+\.gd\"\s*\)"),
        "give the class a class_name and use that name",
    ),
}
OTHER_RULES = {
    "untyped": "type every variable, parameter and return value",
    "long_file": f"keep a new file under {MAX_FILE_LINES} lines: split it",
    "long_function": f"keep a new function under {MAX_FUNCTION_LINES} lines: split it",
    "code_order": (
        "order as the GDScript style guide: signals, enums, consts, static vars, @export vars, "
        "vars, @onready vars, then the methods"
    ),
}

ALLOW = re.compile(r"#\s*standards:\s*allow\s+([a-z_, ]+)")
UNTYPED_VAR = re.compile(r"^\s*(?:@\w+(?:\([^)]*\))?\s+)*(?:static\s+)?var\s+\w+\s*(?:=(?!=)|$)")
FUNC_START = re.compile(r"^\s*(?:static\s+)?func\s+\w+\s*\(")
TOP_FUNC = re.compile(r"^(?:static\s+)?func\s+(\w+)")


def code_part(line: str) -> str:
    """The line without its comment (a # inside a string is kept)."""
    quote = ""
    for i, ch in enumerate(line):
        if quote:
            if ch == quote and line[i - 1] != "\\":
                quote = ""
        elif ch in "\"'":
            quote = ch
        elif ch == "#":
            return line[:i]
    return line


def allowed(line: str, rule: str) -> bool:
    m = ALLOW.search(line)
    return m is not None and rule in re.split(r"[ ,]+", m.group(1))


def split_top_level(text: str) -> list[str]:
    """Splits a parameter list at the commas outside brackets and strings."""
    parts, depth, quote, current = [], 0, "", ""
    for ch in text:
        if quote:
            if ch == quote:
                quote = ""
        elif ch in "\"'":
            quote = ch
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(current)
            current = ""
            continue
        current += ch
    if current.strip():
        parts.append(current)
    return parts


def untyped_lines(lines: list[str]) -> list[int]:
    """Lines with a variable, a parameter or a named function's return value without a type."""
    found = []
    i = 0
    while i < len(lines):
        line = lines[i]
        code = code_part(line)
        if UNTYPED_VAR.match(code) and not allowed(line, "untyped"):
            found.append(i + 1)
        if FUNC_START.match(code):
            start, signature, depth = i, "", 0
            while True:
                part = code_part(lines[i])
                signature += part + " "
                depth += part.count("(") - part.count(")")
                if depth <= 0 or i + 1 >= len(lines):
                    break
                i += 1
            head = signature[signature.index("(") + 1 :]
            close = 0
            depth = 1
            for close, ch in enumerate(head):
                depth += {"(": 1, ")": -1}.get(ch, 0)
                if depth == 0:
                    break
            params, rest = head[:close], head[close + 1 :]
            untyped_param = any(":" not in p for p in split_top_level(params) if p.strip())
            if (untyped_param or "->" not in rest) and not allowed(lines[start], "untyped"):
                found.append(start + 1)
        i += 1
    return found


def long_functions(lines: list[str]) -> int:
    """How many of the file's functions are over MAX_FUNCTION_LINES code lines."""
    total = 0
    starts = [i for i, line in enumerate(lines) if TOP_FUNC.match(line)]
    for i in starts:
        end = len(lines)
        for j in range(i + 1, len(lines)):
            line = lines[j]
            if line and not line[0].isspace() and not line.startswith("#"):
                end = j
                break
        body = [x for x in lines[i:end] if x.strip() and not x.strip().startswith("#")]
        total += len(body) > MAX_FUNCTION_LINES
    return total


def order_problems(text: str) -> int:
    try:
        from gdtoolkit.linter import DEFAULT_CONFIG, lint_code
    except ImportError:
        sys.exit("check_standards: needs gdtoolkit (pip install gdtoolkit==4.5.0)")
    problems = lint_code(text, DEFAULT_CONFIG)
    return sum(1 for p in problems if p.name == "class-definitions-order")


def measure() -> tuple[dict[str, dict[str, int]], dict[tuple[str, str], list[int]]]:
    """The counts of every rule per file, and the lines where the line rules matched."""
    counts: dict[str, dict[str, int]] = {r: {} for r in [*LINE_RULES, *OTHER_RULES]}
    where: dict[tuple[str, str], list[int]] = {}
    files = sorted(p for d in DIRS for p in (ROOT / d).rglob("*.gd"))
    for path in files:
        name = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        lines = text.split("\n")
        for rule, (pattern, _fix) in LINE_RULES.items():
            hits = []
            for n, line in enumerate(lines, 1):
                target = line if rule == "pyport_ref" else code_part(line)
                if pattern.search(target) and not allowed(line, rule):
                    hits.append(n)
            if hits:
                where[(rule, name)] = hits
                counts[rule][name] = len(hits)
        untyped = untyped_lines(lines)
        if untyped:
            where[("untyped", name)] = untyped
            counts["untyped"][name] = len(untyped)
        if len(text.rstrip("\n").split("\n")) > MAX_FILE_LINES:
            counts["long_file"][name] = 1
        long = long_functions(lines)
        if long:
            counts["long_function"][name] = long
        order = order_problems(text)
        if order:
            counts["code_order"][name] = order
    return counts, where


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--update", action="store_true", help="write the counts as the baseline")
    args = parser.parse_args()
    counts, where = measure()
    if args.update:
        BASELINE.write_text(json.dumps(counts, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"check_standards: wrote {BASELINE.name}")
        return 0
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    fixes = {rule: fix for rule, (_p, fix) in LINE_RULES.items()} | OTHER_RULES
    worse, better = [], []
    for rule, per_file in counts.items():
        allowed_counts = baseline.get(rule, {})
        for name in sorted(set(per_file) | set(allowed_counts)):
            now, was = per_file.get(name, 0), allowed_counts.get(name, 0)
            if now > was:
                lines = where.get((rule, name), [])
                at = f" (lines {', '.join(map(str, lines))})" if lines else ""
                worse.append(f"  {name}: {rule} {now}, allowed {was}{at}\n    -> {fixes[rule]}")
            elif now < was:
                better.append(f"  {name}: {rule} {now}, baseline {was}")
    if worse:
        print("check_standards: new code breaks the rules of CLAUDE.md:")
        print("\n".join(worse))
    if better:
        print("check_standards: old code got better; lower the baseline in the same PR with")
        print("  python godot/tools/check_standards.py --update")
        print("\n".join(better))
    if worse or better:
        return 1
    left = sum(len(per_file) for per_file in counts.values())
    print(f"check_standards: OK (old code: {left} rule / file pairs still in the baseline)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
