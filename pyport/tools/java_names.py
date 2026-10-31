"""Print the Python name for every method of the given Java classes.

Naming rule (see pyport/README.md):
  * a Java method keeps its name when that name is unique in the class
    (together with its superclass ag for e/l/af/k) and is not also a field name;
  * otherwise it gets a signature suffix: name_<sig>, where each parameter maps to
    I int, H short, B byte, C char, J long, Z boolean, T String, M Image,
    G Graphics, A<x> for arrays (AB = byte[], AC = char[], AI = int[]), L<cls> other class;
    no parameters -> v.
  * Python keywords get a trailing underscore (as -> as_, do -> do_).

Usage: python pyport/tools/java_names.py ag e l af
"""
import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
METH = re.compile(r"^  (?:(?:public|private|protected|static|final|synchronized)\s+)*([\w\[\]]+)\s+(\w+)\(([^)]*)\)\s*\{")
FIELD = re.compile(r"^  (?:(?:public|private|protected|static|final)\s+)*[\w\[\]]+\s+(\w+)\s*(?:=|;)")
# ag and every class that extends it share ONE namespace (overrides must keep one name).
FAMILY = ["ag", "e", "l", "af", "k", "c", "ar", "as"]
LETTER = {"int": "I", "short": "H", "byte": "B", "char": "C", "long": "J", "boolean": "Z",
          "String": "T", "Image": "M", "Graphics": "G"}


def sig(params: str) -> str:
    params = params.strip()
    if not params:
        return "v"
    out = []
    for p in params.split(","):
        t = p.strip().split()[0]
        if t.endswith("[]"):
            base = t.rstrip("[]")
            out.append("A" + LETTER.get(base, base)[0] if base in LETTER else "A" + base)
        else:
            out.append(LETTER.get(t, "L" + t))
    return "".join(out)


def parse(cls):
    meths, fields = [], set()
    for n, line in enumerate((ROOT / f"{cls}.java").read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        m = METH.match(line)
        if m and m.group(1) not in ("new", "return", "public", "private", "protected", "static", "final"):
            meths.append((m.group(2), sig(m.group(3)), n))
            continue
        f = FIELD.match(line)
        if f:
            fields.add(f.group(1))
    return meths, fields


def names(cls):
    meths, fields = parse(cls)
    allm = list(meths)
    if cls in FAMILY:
        for other in FAMILY:
            if other != cls:
                sm, sf = parse(other)
                allm += sm
                fields |= sf
    count = collections.Counter(n for n, _, _ in {(a, b, 0) for a, b, _ in allm})
    res = []
    for name, s, line in meths:
        py = name if count[name] == 1 and name not in fields else f"{name}_{s}"
        import keyword
        if keyword.iskeyword(py):
            py += "_"
        res.append((f"{cls}.java:{line}", f"{name}({s})", py))
    return res


if __name__ == "__main__":
    for c in sys.argv[1:]:
        for row in names(c):
            print(*row)
