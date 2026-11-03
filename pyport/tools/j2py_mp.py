"""Java (CFR output of the POW Multiplayer jar) -> Python, for the literal port (PHASE_9 task 9.2).

    python pyport/tools/j2py_mp.py          # pyport/mp_java/*.java -> pyport/pow_mp/_gen/*.py

The SP port was translated by hand; the MP client (g.java alone is 6400 lines) goes through
this converter so that the Python stays line-for-line the Java. Generated files are not edited
by hand: hand-written replacements (the async main loop, sockets, sound) live in pow_mp/*.py.

What it does (only what CFR emits in this jar):
- every static field -> class attribute; unqualified names resolve: locals, own class
  fields, the interface `l` (constants), MIDP Canvas methods;
- overloaded methods get a signature suffix (a(Graphics,int,String) -> a_GIT); call sites are
  resolved by argument types inferred from declarations;
- int / long arithmetic with Java semantics where it matters: / % -> idiv / imod, >>> -> ushr,
  casts (byte) (short) (int) (char) -> i8 / i16 / i32 / & 0xFFFF; char = int code;
- ++ / -- / = / op= inside expressions -> helper calls (_inc, _set, ...);
- switch -> if/elif when no case falls through and no break is nested, else a `while True`
  block with a `_m` (matched) flag; labeled break / continue across Python loops -> exceptions;
- String concatenation -> _js(); String methods -> Python equivalents.
Every method keeps a `# g.java:LINE` comment.
"""
import pathlib
import re
import sys

import javalang
from javalang import parser as _jparser
from javalang import tree as T


class Paren(T.Primary):
    """(expr) inside an expression. javalang returns the inner expression and then overwrites
    its prefix operators / selectors with those of the parentheses, so `!(a && b)`, `a - (-b)`
    and `(long)(~x)` lose an operator. Keep the parentheses as a node instead."""
    attrs = ("expression",)


def _parse_primary_par(self):
    self.accept("(")
    e = self.parse_expression()
    self.accept(")")
    return Paren(expression=e)


_orig_primary = _jparser.Parser.parse_primary


def _parse_primary(self):
    if self.would_accept("("):
        return _parse_primary_par(self)
    return _orig_primary(self)


_jparser.Parser.parse_primary = _parse_primary

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "mp_java"
OUT = ROOT / "pow_mp" / "_gen"
PREP = pathlib.Path(__file__).resolve().parent / "j2py_mp_fix"

INTS = {"int", "short", "byte", "char", "long"}
PRIM_CODE = {"int": "I", "short": "S", "byte": "B", "char": "C", "long": "J", "boolean": "Z",
             "String": "T", "Graphics": "G", "Image": "M", "void": "v"}


def tcode(t):
    if t is None:
        return "v"
    name = t.name if hasattr(t, "name") else t
    dims = len(t.dimensions or []) if hasattr(t, "dimensions") else 0
    return "A" * dims + PRIM_CODE.get(name, "L" + name)


class Ty:
    """A Java type: name + array depth."""
    __slots__ = ("name", "dims")

    def __init__(self, name, dims=0):
        self.name, self.dims = name, dims

    @classmethod
    def of(cls, t):
        if t is None:
            return None
        return cls(t.name, len(t.dimensions or []))

    def elem(self):
        return Ty(self.name, self.dims - 1)

    def is_int(self):
        return self.dims == 0 and self.name in INTS

    def is_str(self):
        return self.dims == 0 and self.name == "String"

    def __repr__(self):
        return self.name + "[]" * self.dims


INT, LONG, BOOL, STR, CHAR, NULL = Ty("int"), Ty("long"), Ty("boolean"), Ty("String"), Ty("char"), Ty("null")


# ---------------------------------------------------------------------------------------
class ClassInfo:
    def __init__(self, decl, module, line_of, file):
        self.decl, self.name, self.module, self.file = decl, decl.name, module, file
        self.fields = {}      # name -> (Ty, static)
        self.methods = {}     # name -> [MethodDeclaration]
        self.line_of = line_of
        self.extends = decl.extends.name if getattr(decl, "extends", None) is not None and not isinstance(decl.extends, list) else None
        self.implements = [i.name for i in (getattr(decl, "implements", None) or [])]
        for f in decl.fields:
            for d in f.declarators:
                self.fields[d.name] = (Ty(f.type.name, len(f.type.dimensions or []) + len(d.dimensions or [])), "static" in f.modifiers or decl.__class__ is T.InterfaceDeclaration)
        for m in decl.methods:
            self.methods.setdefault(m.name, []).append(m)

    def pyname(self, m):
        """Java keeps fields and methods apart and has overloads; Python has one namespace:
        a method gets a signature suffix when its name is overloaded anywhere in the class
        family (g + its subclass m) or a field has the same name (g.x and g.x())."""
        sig = lambda md: "".join(tcode(p.type) for p in md.parameters) or "v"
        fam = family(self.name)
        sigs = {sig(md) for c in fam for md in c.methods.get(m.name, [])}
        clash = any(m.name in c.fields for c in fam) or any(
            m.name in CLASSES[i].fields for c in fam for i in c.implements if i in CLASSES)
        if len(sigs) == 1 and not clash:
            return m.name
        return m.name + "_" + sig(m)


CLASSES = {}
OVERLOADED_ANYWHERE = {}


def family(name):
    """The class, its superclasses and its subclasses (g and m share method names)."""
    root = name
    while root in CLASSES and CLASSES[root].extends in CLASSES and CLASSES[root].extends != "Canvas":
        root = CLASSES[root].extends
    out, todo = [], [root]
    while todo:
        n = todo.pop()
        if n in CLASSES:
            out.append(CLASSES[n])
            todo += [c.name for c in CLASSES.values() if c.extends == n]
    return out


def class_chain(name):
    while name in CLASSES:
        yield CLASSES[name]
        name = CLASSES[name].extends


def find_field(cls_name, field):
    for c in class_chain(cls_name):
        if field in c.fields:
            return c, c.fields[field]
        for itf in c.implements:
            if itf in CLASSES and field in CLASSES[itf].fields:
                return CLASSES[itf], CLASSES[itf].fields[field]
    return None, None


def find_methods(cls_name, name):
    out = []
    for c in class_chain(cls_name):
        for m in c.methods.get(name, []):
            out.append((c, m))
    return out


# MIDP / Java library types for inference
LIB_RET = {
    "getWidth": INT, "getHeight": INT, "getClipX": INT, "getClipY": INT, "getClipWidth": INT,
    "getClipHeight": INT, "length": INT, "currentTimeMillis": LONG, "nextInt": INT, "abs": INT,
    "substring": STR, "charAt": CHAR, "equals": BOOL, "getAppProperty": STR, "parseInt": INT,
    "getGraphics": Ty("Graphics"), "createImage": Ty("Image"), "getNumRecords": INT,
    "getRecord": Ty("byte", 1), "getBytes": Ty("byte", 1), "readUTF": STR, "trim": STR,
    "toCharArray": Ty("char", 1), "openRecordStore": Ty("RecordStore"), "valueOf": STR,
}
CANVAS = {"repaint", "serviceRepaints", "getWidth", "getHeight", "setFullScreenMode"}


def assignable(arg, par):
    if arg is None:
        return True
    if arg.name == "null":
        return par.dims > 0 or par.name not in INTS | {"boolean"}
    if arg.dims != par.dims:
        return False
    if arg.dims == 0 and arg.name in INTS and par.name in INTS:
        order = {"byte": 1, "short": 2, "char": 2, "int": 3, "long": 4}
        return order[arg.name] <= order[par.name] or arg.name == par.name
    return arg.name == par.name


# ---------------------------------------------------------------------------------------
class Brk(Exception):
    pass


class Conv:
    def __init__(self, ci):
        self.ci = ci
        self.out = []
        self.ind = 0
        self.locals = [{}]
        self.loops = []          # stack of ("loop"|"switch", label)
        self.exc = set()         # exception classes needed
        self.tmp = 0

    # --- helpers -------------------------------------------------------------
    def emit(self, s):
        self.out.append("    " * self.ind + s)

    def new_tmp(self, base="_t"):
        self.tmp += 1
        return "%s%d" % (base, self.tmp)

    def local_type(self, name):
        for scope in reversed(self.locals):
            if name in scope:
                return scope[name]
        return None

    def declare(self, name, ty):
        self.locals[-1][name] = ty

    def cname(self):
        return self.ci.name

    def qual(self, q):
        """A dotted qualifier ("g.ds", "m.fb", "k2") -> (python code, Ty)."""
        parts = q.split(".")
        head = parts[0]
        if len(parts) > 1 and self.qual_is_class(head, parts[1]):
            owner, f = find_field(head, parts[1])
            code, ty = "%s.%s" % (owner.name if owner else head, parts[1]), (f[0] if f else None)
            rest = parts[2:]
        else:
            code = self.name_expr(head)
            ty = self.local_type(head)
            if ty is None:
                f = find_field(self.cname(), head)[1]
                ty = f[0] if f else (Ty(head) if head in CLASSES else None)
            rest = parts[1:]
        for p_ in rest:
            _, f = find_field(ty.name, p_) if ty is not None else (None, None)
            code, ty = "%s.%s" % (code, p_), (f[0] if f else None)
        return code, ty

    def qual_is_class(self, q, member):
        """CFR writes `g.cY` for the class g even where a field named g exists (g.java has a
        Graphics g); i.java's `g.a(..)` is its field g (a font). A field wins only when its
        type has that member."""
        if q not in CLASSES:
            return False
        if self.local_type(q) is not None:
            return False
        owner, f = find_field(self.cname(), q)
        if f is None:
            return True
        if find_field(q, member)[1] or find_methods(q, member):
            ty = f[0]
            if ty.dims == 0 and ty.name in CLASSES and (find_field(ty.name, member)[1] or find_methods(ty.name, member)):
                return False     # both have it: the field (i.java's g.a(..))
            return True
        return False

    # --- types -------------------------------------------------------------------
    def type_of(self, e):
        if isinstance(e, Paren):
            t = self.type_of(e.expression)
            if e.prefix_operators and "!" in e.prefix_operators:
                return BOOL
            return self._apply_selectors(t, e.selectors) if e.selectors else t
        if isinstance(e, T.Literal):
            v = e.value
            if v.startswith('"'):
                return STR
            if v.startswith("'"):
                return CHAR
            if v in ("true", "false"):
                return BOOL
            if v == "null":
                return NULL
            if v.endswith(("L", "l")):
                return LONG
            return INT
        if isinstance(e, T.MemberReference):
            ty = self._member_type(e)
            return self._apply_selectors(ty, e.selectors)
        if isinstance(e, T.MethodInvocation):
            ty = self._call_type(e)
            return self._apply_selectors(ty, e.selectors)
        if isinstance(e, T.This):
            return Ty(self.cname()) if not e.selectors else self._apply_selectors(Ty(self.cname()), e.selectors)
        if isinstance(e, T.Cast):
            return Ty.of(e.type)
        if isinstance(e, T.BinaryOperation):
            op = e.operator
            if op in ("==", "!=", "<", ">", "<=", ">=", "&&", "||", "instanceof"):
                return BOOL
            a, b = self.type_of(e.operandl), self.type_of(e.operandr)
            if op == "+" and ((a and a.is_str()) or (b and b.is_str())):
                return STR
            if a and b and a.name == "boolean":
                return BOOL
            if (a and a.name == "long" and a.dims == 0) or (b and b.name == "long" and b.dims == 0 and op not in ("<<", ">>", ">>>")):
                return LONG
            return INT
        if isinstance(e, T.TernaryExpression):
            a = self.type_of(e.if_true)
            return a if a and a.name != "null" else self.type_of(e.if_false)
        if isinstance(e, T.Assignment):
            return self.type_of(e.expressionl)
        if isinstance(e, T.ArrayCreator):
            return Ty(e.type.name, len(e.dimensions))
        if isinstance(e, T.ClassCreator):
            return Ty(e.type.name)
        if isinstance(e, T.ArraySelector):
            return None
        return INT if getattr(e, "prefix_operators", None) or getattr(e, "postfix_operators", None) else None

    def _apply_selectors(self, ty, sels):
        for s in sels or []:
            if ty is None:
                return None
            if isinstance(s, T.ArraySelector):
                ty = ty.elem()
            elif isinstance(s, T.MemberReference):
                if s.member == "length" and ty.dims > 0:
                    ty = INT
                else:
                    _, f = find_field(ty.name, s.member)
                    ty = f[0] if f else None
            elif isinstance(s, T.MethodInvocation):
                ty = self._method_ret(ty.name, s)
        return ty

    def _member_type(self, e):
        q, m = e.qualifier, e.member
        if q and "." in q:
            _, qt = self.qual(q)
            if qt is not None and m == "length" and qt.dims > 0:
                return INT
            _, f = find_field(qt.name, m) if qt is not None else (None, None)
            return f[0] if f else None
        if q:
            if self.qual_is_class(q, m):
                _, f = find_field(q, m)
                return f[0] if f else None
            qt = self.local_type(q) or (find_field(self.cname(), q)[1] or (None,))[0]
            if qt is not None and m == "length" and qt.dims > 0:
                return INT
            if qt is not None:
                _, f = find_field(qt.name, m)
                return f[0] if f else None
            return None
        lt = self.local_type(m)
        if lt is not None:
            return lt
        _, f = find_field(self.cname(), m)
        return f[0] if f else None

    def _call_type(self, e):
        q = e.qualifier
        if q and "." in q:
            _, qt = self.qual(q)
            return self._method_ret(qt.name, e) if qt is not None else LIB_RET.get(e.member)
        if q in (None, "", "this") or q == self.cname():
            target = self.cname()
        elif self.qual_is_class(q, e.member):
            target = q
        else:
            qt = self.local_type(q) or (find_field(self.cname(), q)[1] or (None,))[0]
            target = qt.name if qt is not None else q
        return self._method_ret(target, e)

    def _method_ret(self, target, e):
        if target == "String":
            return LIB_RET.get(e.member)
        cands = find_methods(target, e.member)
        if cands:
            m = self.resolve(cands, e.arguments)[1]
            return Ty.of(m.return_type) if m.return_type else None
        return LIB_RET.get(e.member)

    def resolve(self, cands, args):
        ats = [self.type_of(a) for a in args]
        ok = [(c, m) for c, m in cands if len(m.parameters) == len(args)]
        best = [(c, m) for c, m in ok if all(assignable(a, Ty.of(p.type)) for a, p in zip(ats, m.parameters))]
        if len(best) > 1:      # exact match wins
            exact = [(c, m) for c, m in best if all(a is None or a.name == "null" or (a.name == p.type.name and a.dims == len(p.type.dimensions or []))
                                                    for a, p in zip(ats, m.parameters))]
            if exact:
                best = exact
        if not best:
            best = ok
        if not best:
            raise SystemExit("no overload for %s%r (%s)" % (cands[0][1].name, ats, self.cname()))
        if len(best) > 1:
            print("warning: ambiguous %s(%s) in %s -> first" % (cands[0][1].name, ats, self.cname()), file=sys.stderr)
        return best[0]

    # --- expressions ---------------------------------------------------------------
    def lvalue(self, e):
        """-> (kind, parts): ("local", name) | ("attr", objexpr, name) | ("index", arrexpr, idxexpr)."""
        if isinstance(e, T.MemberReference) and not e.selectors:
            if not e.qualifier:
                if self.local_type(e.member) is not None:
                    return ("local", e.member)
                owner, f = find_field(self.cname(), e.member)
                if f is None:
                    raise SystemExit("unknown name %s in %s" % (e.member, self.cname()))
                return ("attr", owner.name if f[1] else "self", e.member)
            if "." in e.qualifier:
                return ("attr", self.qual(e.qualifier)[0], e.member)
            if self.qual_is_class(e.qualifier, e.member):
                owner, f = find_field(e.qualifier, e.member)
                return ("attr", owner.name if owner else e.qualifier, e.member)
            return ("attr", self.name_expr(e.qualifier), e.member)
        if isinstance(e, (T.MemberReference, T.This)) and e.selectors:
            *head, last = e.selectors
            base = self.expr(self._strip_last(e))
            if isinstance(last, T.ArraySelector):
                return ("index", base, self.expr(last.index))
            return ("attr", base, last.member)
        raise SystemExit("lvalue? %r" % (e,))

    def _strip_last(self, e):
        import copy
        c = copy.copy(e)
        c.selectors = e.selectors[:-1]
        return c

    def lv_read(self, lv):
        if lv[0] == "local":
            return lv[1]
        if lv[0] == "attr":
            return "%s.%s" % (lv[1], lv[2])
        return "%s[%s]" % (lv[1], lv[2])

    def name_expr(self, name):
        if self.local_type(name) is not None:
            return name
        if name in CLASSES and find_field(self.cname(), name)[1] is None:
            return name
        owner, f = find_field(self.cname(), name)
        if f is not None:
            return "%s.%s" % (owner.name if f[1] else "self", name)
        return name

    def coerce(self, code, src, dst):
        """Value of type src stored into dst: narrowing (byte) etc. is NOT implicit in Java
        except compound assignment; nothing to do here."""
        return code

    def wrap_int(self, code, ty):
        if ty is None or ty.dims:
            return code
        return {"byte": "i8(%s)", "short": "i16(%s)", "char": "((%s) & 0xFFFF)", "int": "i32(%s)"}.get(ty.name, "%s") % code

    def expr(self, e):
        s = self._expr(e)
        if getattr(e, "postfix_operators", None) or getattr(e, "prefix_operators", None):
            return s
        return s

    def _expr(self, e):
        pre = list(getattr(e, "prefix_operators", None) or [])
        post = list(getattr(e, "postfix_operators", None) or [])
        if pre or post:
            import copy
            inner = copy.copy(e)
            inner.prefix_operators = []
            inner.postfix_operators = []
            if post:
                return self.incdec(inner, post[0], prefix=False)
            # prefix: apply innermost first
            ops = pre
            if ops[-1] in ("++", "--"):
                code = self.incdec(inner, ops[-1], prefix=True)
                ops = ops[:-1]
            else:
                code = self._expr(inner)
            for op in reversed(ops):
                if op == "!":
                    code = "(not %s)" % code
                elif op == "-":
                    code = "(-%s)" % code
                elif op == "~":
                    code = "(~%s)" % code
                elif op == "+":
                    pass
                else:
                    raise SystemExit("prefix %s" % op)
            return code
        if isinstance(e, T.Literal):
            v = e.value
            if v.startswith('"'):
                return v
            if v.startswith("'"):
                ch = eval(v.replace("\\u", "\\\\u")) if False else _char_lit(v)
                return str(ch)
            if v in ("true", "false"):
                return "True" if v == "true" else "False"
            if v == "null":
                return "None"
            is_long = v.endswith(("L", "l"))
            v = v.rstrip("Ll")
            if v.lower().startswith("0x"):
                n = int(v, 16)
                if not is_long and n > 0x7FFFFFFF:      # an int literal like 0xEDB88320 is negative
                    return str(n - (1 << 32))
                return v
            if v.endswith(("f", "F", "d", "D")):
                return v[:-1]
            if len(v) > 1 and v.startswith("0") and v.isdigit():
                return str(int(v, 8))
            return v
        if isinstance(e, T.MemberReference):
            if e.member == "length" and not e.selectors:
                qt = self.local_type(e.qualifier) if e.qualifier else None
                if qt is None and e.qualifier and e.qualifier not in CLASSES:
                    f = find_field(self.cname(), e.qualifier)[1]
                    qt = f[0] if f else None
                if qt is not None and qt.dims > 0:
                    return "len(%s)" % self.name_expr(e.qualifier)
            if e.qualifier and "." in e.qualifier:
                qc, qt = self.qual(e.qualifier)
                if e.member == "length" and qt is not None and qt.dims > 0 and not e.selectors:
                    return "len(%s)" % qc
                base = "%s.%s" % (qc, e.member)
                _, f = find_field(qt.name, e.member) if qt is not None else (None, None)
                bty = f[0] if f else None
            elif e.qualifier:
                if self.qual_is_class(e.qualifier, e.member):
                    owner, f = find_field(e.qualifier, e.member)
                    base = "%s.%s" % (owner.name if owner else e.qualifier, e.member)
                    bty = f[0] if f else None
                else:
                    base = "%s.%s" % (self.name_expr(e.qualifier), e.member)
                    bty = self._member_type(T.MemberReference(qualifier=e.qualifier, member=e.member, selectors=[]))
            else:
                base = self.name_expr(e.member)
                bty = self._member_type(T.MemberReference(qualifier=None, member=e.member, selectors=[]))
            return self.selectors(base, bty, e.selectors)
        if isinstance(e, T.This):
            return self.selectors("self", Ty(self.cname()), e.selectors)
        if isinstance(e, Paren):
            code = "(%s)" % self.expr(e.expression)
            return self.selectors(code, self.type_of(e.expression), e.selectors)
        if isinstance(e, T.SuperConstructorInvocation):
            return "super().__init__(%s)" % ", ".join(self.expr(a) for a in e.arguments)
        if isinstance(e, T.MethodInvocation):
            return self.call(e)
        if isinstance(e, T.Cast):
            inner = self.expr(e.expression)
            t = e.type.name
            if e.type.dimensions:
                return inner
            src = self.type_of(e.expression)
            if t == "byte":
                return "i8(%s)" % inner
            if t == "short":
                return "i16(%s)" % inner
            if t == "char":
                return "((%s) & 0xFFFF)" % inner
            if t == "int":
                return "i32(%s)" % inner if src is not None and src.name == "long" else inner
            if t == "long":
                return inner
            return inner
        if isinstance(e, T.BinaryOperation):
            return self.binop(e)
        if isinstance(e, T.TernaryExpression):
            return "(%s if %s else %s)" % (self.expr(e.if_true), self.expr(e.condition), self.expr(e.if_false))
        if isinstance(e, T.Assignment):
            return self.assign_expr(e)
        if isinstance(e, T.ArrayCreator):
            return self.new_array(e)
        if isinstance(e, T.ArrayInitializer):
            return "[%s]" % ", ".join(self.expr(x) for x in e.initializers)
        if isinstance(e, T.ClassCreator):
            n = e.type.name
            args = ", ".join(self.expr(a) for a in e.arguments)
            if n == "String":
                return "_jstring(%s)" % args
            return "%s(%s)" % (n, args)
        raise SystemExit("expr? %r" % (e,))

    def selectors(self, base, ty, sels):
        code = base
        for s in sels or []:
            if isinstance(s, T.ArraySelector):
                code = "%s[%s]" % (code, self.expr(s.index))
                ty = ty.elem() if ty else None
            elif isinstance(s, T.MemberReference):
                if s.member == "length" and ty is not None and ty.dims > 0:
                    code, ty = "len(%s)" % code, INT
                else:
                    code = "%s.%s" % (code, s.member)
                    _, f = find_field(ty.name, s.member) if ty else (None, None)
                    ty = f[0] if f else None
            elif isinstance(s, T.MethodInvocation):
                code, ty = self.method_on(code, ty, s)
        return code

    def method_on(self, obj, ty, m):
        args = [self.expr(a) for a in m.arguments]
        if ty is not None and ty.is_str():
            return self.string_method(obj, m.member, args, m.arguments), LIB_RET.get(m.member)
        if ty is not None and ty.name in CLASSES and find_methods(ty.name, m.member):
            c, md = self.resolve(find_methods(ty.name, m.member), m.arguments)
            return "%s.%s(%s)" % (obj, c.pyname(md), ", ".join(args)), Ty.of(md.return_type)
        return "%s.%s(%s)" % (obj, m.member, ", ".join(args)), LIB_RET.get(m.member)

    def string_method(self, obj, name, args, raw):
        if name == "length":
            return "len(%s)" % obj
        if name == "substring":
            return "%s[%s:%s]" % (obj, args[0], args[1] if len(args) > 1 else "")
        if name == "charAt":
            return "ord(%s[%s])" % (obj, args[0])
        if name == "equals":
            return "(%s == %s)" % (obj, args[0])
        if name == "getBytes":
            return "bytearray(%s.encode('latin-1', 'replace'))" % obj
        if name == "toCharArray":
            return "[ord(_c) for _c in %s]" % obj
        if name == "trim":
            return "_jtrim(%s)" % obj
        if name == "indexOf":
            return "%s.find(%s)" % (obj, args[0] if not (self.type_of(raw[0]) or INT).name == "char" else "chr(%s)" % args[0])
        raise SystemExit("String.%s" % name)

    def call(self, e):
        q = e.qualifier
        args = [self.expr(a) for a in e.arguments]
        name = e.member
        # library calls
        if q == "System":
            if name == "currentTimeMillis":
                code = "system.currentTimeMillis()"
            elif name == "gc":
                code = "None"
            elif name == "arraycopy":
                code = "_arraycopy(%s)" % ", ".join(args)
            else:
                raise SystemExit("System.%s" % name)
            return self.selectors(code, LIB_RET.get(name), e.selectors)
        if q in ("System.out",):
            code = "print(%s)" % ("_js(%s)" % args[0] if args else "")
            if name == "print":
                code = "print(%s, end='')" % ("_js(%s)" % args[0])
            return code
        if q == "Math" and name == "abs":
            return "abs(%s)" % args[0]
        if q == "Integer" and name == "parseInt":
            return "int(%s)" % args[0]
        if q == "Thread" and name == "sleep":
            return "system.sleep(%s)" % args[0]
        if q == "String" and name == "valueOf":
            return "_js(%s)" % args[0]
        if q in ("Image", "RecordStore", "Connector", "Manager"):
            return self.selectors("%s.%s(%s)" % (q, name, ", ".join(args)), LIB_RET.get(name), e.selectors)
        # own / other classes
        if q and "." in q:
            obj, qt = self.qual(q)
            if qt is not None and qt.is_str():
                return self.selectors(self.string_method(obj, name, args, e.arguments), LIB_RET.get(name), e.selectors)
            code, ty = self.method_on(obj, qt, e)
            return self.selectors(code, ty, e.selectors)
        if q in (None, "") or q == "this":
            target, obj = self.cname(), None
        elif self.qual_is_class(q, name):
            target, obj = q, q
        else:
            qt = self.local_type(q)
            if qt is None:
                f = find_field(self.cname(), q)[1]
                qt = f[0] if f else None
            if qt is not None and qt.is_str():
                return self.selectors(self.string_method(self.name_expr(q), name, args, e.arguments), LIB_RET.get(name), e.selectors)
            obj = self.name_expr(q)
            target = qt.name if qt is not None else None
        cands = find_methods(target, name) if target else []
        if cands:
            c, m = self.resolve(cands, e.arguments)
            py = c.pyname(m)
            static = "static" in m.modifiers
            if obj is None:
                obj = c.name if static else "self"
            elif obj in CLASSES and not static:
                obj = "self"          # g.foo() on an instance method inside g: the one instance
            code = "%s.%s(%s)" % (obj, py, ", ".join(args))
            return self.selectors(code, Ty.of(m.return_type), e.selectors)
        if obj is None:
            return self.selectors("self.%s(%s)" % (name, ", ".join(args)), LIB_RET.get(name), e.selectors)
        return self.selectors("%s.%s(%s)" % (obj, name, ", ".join(args)), LIB_RET.get(name), e.selectors)

    def binop(self, e):
        op = e.operator
        a, b = self.expr(e.operandl), self.expr(e.operandr)
        ta, tb = self.type_of(e.operandl), self.type_of(e.operandr)
        if op == "+" and ((ta and ta.is_str()) or (tb and tb.is_str())):
            return "_js(%s, %s)" % (self.str_part(a, ta), self.str_part(b, tb))
        if op == "&&":
            return "(%s and %s)" % (a, b)
        if op == "||":
            return "(%s or %s)" % (a, b)
        if op == "/":
            return "idiv(%s, %s)" % (a, b)
        if op == "%":
            return "imod(%s, %s)" % (a, b)
        if op == ">>>":
            if ta is not None and ta.name == "long":
                return "(((%s) & 0xFFFFFFFFFFFFFFFF) >> (%s))" % (a, b)
            return "ushr32(%s, %s)" % (a, b)
        if op == "<<":
            return "i32((%s) << (%s))" % (a, b)
        if op in ("&", "|", "^") and ta is not None and ta.name == "boolean":
            return "bool(%s %s %s)" % (a, op, b)
        if op == "instanceof":
            return "isinstance(%s, %s)" % (a, b)
        return "(%s %s %s)" % (a, op, b)

    def str_part(self, code, ty):
        if ty is not None and ty.name == "char" and ty.dims == 0:
            return "chr(%s)" % code
        return code

    def new_array(self, e):
        if e.initializer is not None:
            return self.expr(e.initializer)
        dims = [self.expr(d) if d is not None else None for d in e.dimensions]
        t = e.type.name
        fill = "0" if t in INTS else ("False" if t == "boolean" else "None")
        sized = [d for d in dims if d is not None]
        if len(dims) > len(sized):           # new int[n][] -> rows None
            fill_inner = "None"
        else:
            fill_inner = fill
        code = "[%s] * (%s)" % (fill_inner if len(sized) == 1 else fill, sized[-1])
        if len(sized) == 1:
            return "[%s] * (%s)" % (fill_inner, sized[0])
        for d in reversed(sized[:-1]):
            code = "[%s for _ in range(%s)]" % (code, d)
        return code

    def incdec(self, target, op, prefix):
        lv = self.lvalue(target)
        delta = "1" if op == "++" else "-1"
        ty = self.type_of(target)
        if lv[0] == "local":
            if prefix:
                return "(%s := %s)" % (lv[1], self.wrap_int("%s + %s" % (lv[1], delta), ty))
            return "((%s := %s) - %s)" % (lv[1], self.wrap_int("%s + %s" % (lv[1], delta), ty), delta)
        if lv[0] == "attr":
            return "_inc%s(%s, %r, %s)" % ("" if prefix else "_post", lv[1], lv[2], delta)
        return "_inci%s(%s, %s, %s)" % ("" if prefix else "_post", lv[1], lv[2], delta)

    def assign_value(self, e):
        """Right side of `=` / `op=` -> python code of the new value."""
        op = e.type
        rhs = self.expr(e.value)
        if op == "=":
            return rhs
        lv = self.lvalue(e.expressionl)
        cur = self.lv_read(lv)
        ty = self.type_of(e.expressionl)
        bop = op[:-1]
        if bop == "+" and ty is not None and ty.is_str():
            return "_js(%s, %s)" % (cur, self.str_part(rhs, self.type_of(e.value)))
        fake = T.BinaryOperation(operator=bop, operandl=e.expressionl, operandr=e.value)
        code = self.binop(fake)
        return self.wrap_int(code, ty) if ty is not None and ty.name in ("byte", "short", "char") else code

    def assign_expr(self, e):
        lv = self.lvalue(e.expressionl)
        val = self.assign_value(e)
        if lv[0] == "local":
            return "(%s := %s)" % (lv[1], val)
        if lv[0] == "attr":
            return "_set(%s, %r, %s)" % (lv[1], lv[2], val)
        return "_seti(%s, %s, %s)" % (lv[1], lv[2], val)

    # --- statements ------------------------------------------------------------------
    def stmt(self, s):
        line = s.position.line if getattr(s, "position", None) else None
        if isinstance(s, T.BlockStatement):
            if s.label:
                return self.labeled(s.label, s)
            self.block(s.statements)
        elif isinstance(s, T.LocalVariableDeclaration):
            for d in s.declarators:
                ty = Ty(s.type.name, len(s.type.dimensions or []) + len(d.dimensions or []))
                self.declare(d.name, ty)
                if d.initializer is None:
                    init = "0" if ty.is_int() else ("False" if ty.name == "boolean" and not ty.dims else "None")
                else:
                    init = self.expr(d.initializer)
                self.emit("%s = %s" % (d.name, init))
        elif isinstance(s, T.StatementExpression):
            if s.label:
                return self.labeled(s.label, s)
            self.expr_stmt(s.expression)
        elif isinstance(s, T.IfStatement):
            if s.label:
                return self.labeled(s.label, s)
            self.if_chain(s)
        elif isinstance(s, T.WhileStatement):
            self.loop_while(s, s.label)
        elif isinstance(s, T.DoStatement):
            self.loop_do(s, s.label)
        elif isinstance(s, T.ForStatement):
            self.loop_for(s, s.label)
        elif isinstance(s, T.SwitchStatement):
            if s.label:
                return self.labeled(s.label, s)
            self.switch(s, None)
        elif isinstance(s, T.ReturnStatement):
            self.emit("return" + (" " + self.expr(s.expression) if s.expression is not None else ""))
        elif isinstance(s, T.BreakStatement):
            self.jump("break", s.goto)
        elif isinstance(s, T.ContinueStatement):
            self.jump("continue", s.goto)
        elif isinstance(s, T.TryStatement):
            self.emit("try:")
            self.ind += 1
            n = len(self.out)
            self.block(s.block)
            if len(self.out) == n:
                self.emit("pass")
            self.ind -= 1
            for c in s.catches or []:
                self.emit("except Exception as %s:" % c.parameter.name)
                self.ind += 1
                self.locals.append({c.parameter.name: Ty("Exception")})
                n = len(self.out)
                self.block(c.block)
                if len(self.out) == n:
                    self.emit("pass")
                self.locals.pop()
                self.ind -= 1
            if s.finally_block:
                self.emit("finally:")
                self.ind += 1
                self.block(s.finally_block)
                self.ind -= 1
        elif isinstance(s, T.SynchronizedStatement):
            self.block(s.block)
        elif isinstance(s, T.ThrowStatement):
            self.emit("raise RuntimeError(%s)" % self.expr(s.expression))
        elif isinstance(s, T.Statement) and s.__class__ is T.Statement:
            self.emit("pass")
        else:
            raise SystemExit("stmt? %r line %s" % (s.__class__.__name__, line))

    def block(self, stmts):
        self.locals.append({})
        for s in stmts or []:
            self.stmt(s)
        self.locals.pop()

    def body(self, s):
        n = len(self.out)
        self.ind += 1
        if isinstance(s, T.BlockStatement) and not s.label:
            self.block(s.statements)
        elif s is None:
            pass
        else:
            self.locals.append({})
            self.stmt(s)
            self.locals.pop()
        if len(self.out) == n:
            self.emit("pass")
        self.ind -= 1

    def expr_stmt(self, e):
        pre = list(getattr(e, "prefix_operators", None) or [])
        post = list(getattr(e, "postfix_operators", None) or [])
        if (pre or post) and not isinstance(e, T.Assignment):
            import copy
            inner = copy.copy(e)
            inner.prefix_operators = []
            inner.postfix_operators = []
            op = (pre or post)[0]
            lv = self.lvalue(inner)
            ty = self.type_of(inner)
            cur = self.lv_read(lv)
            val = "%s %s 1" % (cur, "+" if op == "++" else "-")
            val = self.wrap_int(val, ty) if ty is not None and ty.name in ("byte", "short", "char") else val
            self.emit("%s = %s" % (cur, val))
            return
        if isinstance(e, T.Assignment):
            t0 = e.expressionl
            if (isinstance(t0, T.MemberReference) and not t0.qualifier and not t0.selectors
                    and re.match(r"^(var\d+_\d+|v\d+)$", t0.member) and self.local_type(t0.member) is None):
                self.locals[1 if len(self.locals) > 1 else 0][t0.member] = self.type_of(e.value) or INT
            # a = b = c  -> chain
            targets = [e.expressionl]
            v = e
            while isinstance(v.value, T.Assignment) and v.value.type == "=" and v.type == "=":
                v = v.value
                targets.append(v.expressionl)
            if len(targets) > 1:
                val = self.assign_value(v)
                tmp = self.new_tmp()
                self.emit("%s = %s" % (tmp, val))
                for t in reversed(targets):
                    self.emit("%s = %s" % (self.lv_read(self.lvalue(t)), tmp))
                return
            lv = self.lvalue(e.expressionl)
            self.emit("%s = %s" % (self.lv_read(lv), self.assign_value(e)))
            return
        self.emit(self.expr(e))

    def if_chain(self, s, kw="if"):
        self.emit("%s %s:" % (kw, self.cond(s.condition)))
        self.body(s.then_statement)
        el = s.else_statement
        if el is None:
            return
        if isinstance(el, T.IfStatement) and not el.label:
            self.if_chain(el, "elif")
        else:
            self.emit("else:")
            self.body(el)

    def cond(self, e):
        c = self.expr(e)
        if c.startswith("(") and c.endswith(")") and _balanced(c[1:-1]):
            c = c[1:-1]
        return c

    # --- loops / jumps ---------------------------------------------------------------
    def jump(self, kind, label):
        # innermost python loop = self.loops[-1]
        if label is None:
            if kind == "break":
                self.emit("break")
                return
            # continue: target = innermost java loop
            for i in range(len(self.loops) - 1, -1, -1):
                if self.loops[i][0] == "loop":
                    break
            if i == len(self.loops) - 1:
                self.emit("continue")
                return
            exc = "_Cont_%s" % self.loops[i][2]
            self.exc.add(exc)
            self.loops[i][3].add("cont")
            self.emit("raise %s()" % exc)
            return
        # labeled
        for i in range(len(self.loops) - 1, -1, -1):
            if self.loops[i][1] == label:
                break
        else:
            raise SystemExit("label %s not found" % label)
        if i == len(self.loops) - 1 and self.loops[i][0] in ("loop", "switch"):
            self.emit(kind)
            return
        if kind == "continue" and i == len(self.loops) - 1:
            self.emit("continue")
            return
        exc = "_%s_%s" % ("Brk" if kind == "break" else "Cont", self.loops[i][2])
        self.exc.add(exc)
        self.loops[i][3].add("brk" if kind == "break" else "cont")
        self.emit("raise %s()" % exc)

    def push_loop(self, kind, label):
        uid = "%s_%d" % (label or "L", len(self.out))
        entry = [kind, label, uid, set()]
        self.loops.append(entry)
        return entry

    def wrap_exc(self, entry, start):
        """Wrap emitted lines [start:] in try/except for labeled jumps out of nested loops."""
        if "brk" in entry[3]:
            body = self.out[start:]
            del self.out[start:]
            self.emit("try:")
            self.out.extend("    " + l for l in body)
            self.emit("except _Brk_%s:" % entry[2])
            self.emit("    pass")

    def loop_body_with_cont(self, entry, s):
        start = len(self.out)
        self.body(s)
        if "cont" in entry[3]:
            body = self.out[start:]
            del self.out[start:]
            self.ind += 1
            self.emit("try:")
            self.out.extend("    " + l for l in body)
            self.emit("except _Cont_%s:" % entry[2])
            self.emit("    pass")
            self.ind -= 1

    def loop_while(self, s, label):
        start = len(self.out)
        entry = self.push_loop("loop", label)
        self.emit("while %s:" % self.cond(s.condition))
        self.loop_body_with_cont(entry, s.body)
        self.loops.pop()
        self.wrap_exc(entry, start)

    def loop_do(self, s, label):
        start = len(self.out)
        entry = self.push_loop("loop", label)
        self.emit("while True:")
        # continue in a do-while jumps to the condition: use the exception form for it
        entry[3].add("cont_do")
        self.loop_body_with_cont(entry, s.body)
        self.ind += 1
        self.emit("if not (%s):" % self.cond(s.condition))
        self.emit("    break")
        self.ind -= 1
        self.loops.pop()
        self.wrap_exc(entry, start)

    def loop_for(self, s, label):
        ctl = s.control
        self.locals.append({})
        if ctl.init is not None:
            inits = ctl.init if isinstance(ctl.init, list) else [ctl.init]
            for i in inits:
                if isinstance(i, T.VariableDeclaration):
                    self.stmt(T.LocalVariableDeclaration(type=i.type, declarators=i.declarators, modifiers=set(), annotations=[]))
                else:
                    self.expr_stmt(i)
        start = len(self.out)
        entry = self.push_loop("loop", label)
        self.emit("while %s:" % (self.cond(ctl.condition) if ctl.condition is not None else "True"))
        entry[3].add("cont")    # continue must run the update: always through the exception
        self.loop_body_with_cont(entry, s.body)
        self.ind += 1
        for u in ctl.update or []:
            self.expr_stmt(u)
        self.ind -= 1
        self.loops.pop()
        self.wrap_exc(entry, start)
        self.locals.pop()

    def labeled(self, label, s):
        if isinstance(s, T.WhileStatement):
            return self.loop_while(s, label)
        if isinstance(s, T.DoStatement):
            return self.loop_do(s, label)
        if isinstance(s, T.ForStatement):
            return self.loop_for(s, label)
        if isinstance(s, T.SwitchStatement):
            return self.switch(s, label)
        # a labeled block: break label leaves it
        start = len(self.out)
        entry = self.push_loop("block", label)
        if isinstance(s, T.BlockStatement):
            self.block(s.statements)
        else:
            self.stmt(s)
        self.loops.pop()
        entry[3].add("brk") if any(("raise _Brk_%s()" % entry[2]) in l for l in self.out[start:]) else None
        self.wrap_exc(entry, start)

    # --- switch -----------------------------------------------------------------------
    def switch(self, s, label):
        groups = s.cases
        val = self.expr(s.expression)
        vty = self.type_of(s.expression)

        def labels(g):
            out = []
            for c in g.case:
                if isinstance(c, T.Literal) and c.value.startswith("'"):
                    out.append(str(_char_lit(c.value)))
                else:
                    out.append(self.expr(c))
            return out

        def is_default(g):
            return not g.case or any(c == "default" for c in g.case)

        simple = label is None and self._switch_simple(groups)
        tmp = self.new_tmp("_sw")
        self.emit("%s = %s" % (tmp, val))
        if simple:
            first = True
            default = None
            for g in groups:
                if is_default(g):
                    default = g
                    continue
                labs = labels(g)
                c = ("%s == %s" % (tmp, labs[0])) if len(labs) == 1 else ("%s in (%s)" % (tmp, ", ".join(labs)))
                self.emit("%s %s:" % ("if" if first else "elif", c))
                first = False
                self.case_body(g.statements, strip_break=True)
            if default is not None:
                if first:
                    self.emit("if True:")
                else:
                    self.emit("else:")
                self.case_body(default.statements, strip_break=True)
            return
        start = len(self.out)
        entry = self.push_loop("switch", label)
        all_labels = []
        for g in groups:
            if not is_default(g):
                all_labels += labels(g)
        mt = self.new_tmp("_m")
        self.emit("%s = False" % mt)
        self.emit("while True:")
        self.ind += 1
        for g in groups:
            conds = []
            labs = [] if is_default(g) else labels(g)
            if labs:
                conds.append(("%s == %s" % (tmp, labs[0])) if len(labs) == 1 else ("%s in (%s)" % (tmp, ", ".join(labs))))
            if is_default(g):
                conds.append("%s not in (%s)" % (tmp, ", ".join(all_labels) + ("," if len(all_labels) == 1 else "")) if all_labels else "True")
            self.emit("if %s or %s:" % (mt, " or ".join(conds)))
            self.ind += 1
            self.emit("%s = True" % mt)
            self.ind -= 1
            self.case_body(g.statements, strip_break=False)
        self.emit("break")
        self.ind -= 1
        self.loops.pop()
        self.wrap_exc(entry, start)

    def _switch_simple(self, groups):
        for i, g in enumerate(groups):
            st = _flatten(g.statements)
            if not st:
                if i == len(groups) - 1:
                    continue
                return False
            last = st[-1]
            if i < len(groups) - 1 and not isinstance(last, (T.BreakStatement, T.ReturnStatement, T.ContinueStatement, T.ThrowStatement)):
                return False
            if isinstance(last, T.BreakStatement) and last.goto:
                return False
            if isinstance(last, T.ContinueStatement):
                return False      # continue inside the if-chain is fine, but keep it simple
            # no break nested deeper (it would leave the switch)
            for node in st[:-1] if isinstance(last, T.BreakStatement) else st:
                if _has_break(node):
                    return False
        return True

    def case_body(self, stmts, strip_break):
        st = _flatten(stmts)
        if strip_break and st and isinstance(st[-1], T.BreakStatement) and not st[-1].goto:
            st = st[:-1]
        self.ind += 1
        n = len(self.out)
        self.locals.append({})
        for x in st:
            self.stmt(x)
        self.locals.pop()
        if len(self.out) == n:
            self.emit("pass")
        self.ind -= 1

    # --- methods --------------------------------------------------------------------------
    def method(self, m, ctor=False):
        static = "static" in m.modifiers
        params = [p.name for p in m.parameters]
        self.locals = [{p.name: Ty(p.type.name, len(p.type.dimensions or [])) for p in m.parameters}]
        self.loops = []
        line = m.position.line if m.position else 0
        name = "__init__" if ctor else self.ci.pyname(m)
        if static and not ctor:
            self.emit("@staticmethod")
            self.emit("def %s(%s):  # %s:%d" % (name, ", ".join(params), self.ci.file, line))
        else:
            self.emit("def %s(%s):  # %s:%d" % (name, ", ".join(["self"] + params), self.ci.file, line))
        self.ind += 1
        n = len(self.out)
        if ctor and self.ci.extends == "Canvas":
            self.emit("_Canvas.__init__(self)")
        if ctor:
            for fname, (ty, st) in self.ci.fields.items():
                if not st:
                    init = self.instance_inits.get(fname)
                    self.emit("self.%s = %s" % (fname, init if init is not None else _default(ty)))
        self.block(m.body)
        if len(self.out) == n:
            self.emit("pass")
        self.ind -= 1
        self.emit("")


def _default(ty):
    if ty.dims:
        return "None"
    if ty.name in INTS:
        return "0"
    if ty.name == "boolean":
        return "False"
    return "None"


def _flatten(stmts):
    """case bodies of CFR are often one {block}: unwrap it."""
    st = list(stmts or [])
    while len(st) == 1 and isinstance(st[0], T.BlockStatement) and not st[0].label:
        st = list(st[0].statements or [])
    return st


def _has_break(node):
    """A break that targets the switch (not inside a nested loop / switch)."""
    if isinstance(node, T.BreakStatement):
        return node.goto is None
    if isinstance(node, (T.WhileStatement, T.DoStatement, T.ForStatement, T.SwitchStatement)):
        return False
    for attr in getattr(node, "attrs", ()):
        v = getattr(node, attr, None)
        for c in (v if isinstance(v, list) else [v]):
            if isinstance(c, T.Node) and _has_break(c):
                return True
    return False


def _char_lit(v):
    body = v[1:-1]
    if body.startswith("\\u"):
        return int(body[2:], 16)
    if body.startswith("\\"):
        return ord({"n": "\n", "t": "\t", "r": "\r", "0": "\0", "'": "'", '"': '"', "\\": "\\"}[body[1]])
    return ord(body)


def _balanced(s):
    depth = 0
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


HEADER = '''"""GENERATED by pyport/tools/j2py_mp.py from pyport/mp_java/%(file)s - do not edit.

Hand-written parts that replace or complete this class: pow_mp/%(mod)s.py (when present).
"""
from pow_mp.rt import *  # noqa: F401,F403
%(imports)s

'''


def convert(java_file, classes_of_module):
    pass


import keyword as _kw


def _mangle(node):
    """Java names that are Python keywords (g.as, ...) get a trailing underscore."""
    def fix(v):
        if isinstance(v, str):
            parts = v.split(".")
            return ".".join(p + "_" if _kw.iskeyword(p) else p for p in parts)
        return v
    for _, n in node:
        for attr in ("name", "member", "qualifier", "goto"):
            if hasattr(n, attr) and isinstance(getattr(n, attr), str) and not isinstance(n, (T.ReferenceType, T.BasicType)):
                setattr(n, attr, fix(getattr(n, attr)))
    return node


def load(name, text):
    unit = _mangle(javalang.parse.parse(text))
    for t in unit.types:
        lines = text.split("\n")
        CLASSES[t.name] = ClassInfo(t, name, lines, name + ".java")
    return unit


def emit_class(ci, imports):
    cv = Conv(ci)
    decl = ci.decl
    base = ci.extends or "object"
    cv.emit("class %s(%s):" % (ci.name, "_Canvas" if base == "Canvas" else base))
    cv.ind += 1
    # static fields with constant initializers
    cv.instance_inits = {}
    for f in decl.fields:
        static = "static" in f.modifiers or decl.__class__ is T.InterfaceDeclaration
        for d in f.declarators:
            ty = Ty(f.type.name, len(f.type.dimensions or []) + len(d.dimensions or []))
            line = f.position.line if f.position else 0
            if static:
                init = _default(ty)
                if d.initializer is not None and not isinstance(d.initializer, (T.ArrayInitializer, T.ArrayCreator, T.ClassCreator)):
                    init = cv.expr(d.initializer)
                    d._done = True
                cv.emit("%s = %s  # %s:%d %s" % (d.name, init, ci.file, line, ty))
            else:
                if d.initializer is not None:
                    cv.instance_inits[d.name] = cv.expr(d.initializer)
    cv.emit("")
    ctors = list(decl.constructors) if hasattr(decl, "constructors") else []
    for c in ctors:
        cv.method(c, ctor=True)
    if not ctors and cv.instance_inits:
        cv.emit("def __init__(self):")
        for k, v in cv.instance_inits.items():
            cv.emit("    self.%s = %s" % (k, v))
        cv.emit("")
    for m in decl.methods:
        cv.method(m)
    cv.ind -= 1
    # static initializer: field initializers with arrays / objects + static {} blocks
    cv.emit("")
    cv.emit("def _static_init_%s():" % ci.name)
    cv.ind += 1
    cv.locals = [{}]
    n = len(cv.out)
    for f in decl.fields:
        static = "static" in f.modifiers or decl.__class__ is T.InterfaceDeclaration
        for d in f.declarators:
            if static and d.initializer is not None and not getattr(d, "_done", False):
                cv.emit("%s.%s = %s" % (ci.name, d.name, cv.expr(d.initializer)))
    for b in decl.body:
        if isinstance(b, list):          # static { ... } -> list of statements in javalang
            cv.block(b)
    if len(cv.out) == n:
        cv.emit("pass")
    cv.ind -= 1
    exc = "".join("class %s(BaseException):\n    pass\n\n\n" % x for x in sorted(cv.exc))
    return exc + "\n".join(cv.out) + "\n"


def main():
    names = ["l", "f", "i", "j", "k", "e", "d", "g", "m"]
    texts = {}
    for n in names:
        text = (SRC / (n + ".java")).read_text()
        if n == "g":
            text = prep_g(text)
        if n == "l":
            text = text.replace("public interface l {", "public class l {")
        texts[n] = text
    # MIDP stand-ins so that inference knows a few types
    stub = """
class Canvas { }
class Main { public String getAppProperty(String s) { return null; } }
class a { public a(String s) {} public void a() {} public short[] c; public short[] d; public byte[] e; public byte[] f; public byte[] g; public byte[] h; public byte a; }
class n { public static byte[] a(String s) { return null; } }
class h { public static short a; public static boolean j; public static int h; public static int i; public static boolean g;
  public h() {} public void a(String s, int p) {} public static void a() {} public void a(int n) {} public static void a(byte b) {}
  public static void b(int n) {} public static void b(String s, int n) {} public static void b() {} public void start() {} public static void a(g x) {} }
class c { public c(int a, int b, boolean x, boolean y) {} public void a() {} public void b() {} public void a(int v) {} public boolean a(String s, int n) { return true; } public void a(int n, boolean b) {} }
"""
    load("_stubs", stub)
    units = {n: load(n, texts[n]) for n in names}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "__init__.py").write_text('"""GENERATED by pyport/tools/j2py_mp.py: Python of pyport/mp_java (do not edit)."""\n')
    for n in names:
        ci = CLASSES[n]
        imports = "\n".join(sorted(
            "from pow_mp._gen.%s import %s" % (o, o) for o in names if o != n and re.search(r"\b%s\." % o, texts[n])
        ))
        body = emit_class(ci, imports)
        head = HEADER % {"file": n + ".java", "mod": n, "imports": ""}
        lazy = [o for o in names if o != n and re.search(r"\b%s\b" % o, body)]
        tail = "\n\ndef _late_imports():\n    global %s\n" % ", ".join(lazy) + "".join(
            "    from pow_mp._gen.%s import %s\n" % (o, o) for o in lazy) if lazy else "\n\ndef _late_imports():\n    pass\n"
        ext = ""
        if ci.extends and ci.extends in names:
            ext = "from pow_mp._gen.%s import %s\n" % (ci.extends, ci.extends)
        (OUT / (n + ".py")).write_text(head + ext + "\n" + body + tail)
        print("wrote", OUT / (n + ".py"))


def prep_g(text):
    """CFR output of g.java -> parseable Java: two GOTO regions restructured by hand
    (tools/j2py_mp_fix/*.java), two CFR side-effect bugs, the field named `do` (a keyword) -> do_."""
    lines = text.split("\n")

    def put(a, b, name):           # 1-based inclusive; padded so later line numbers stay
        new = (PREP / name).read_text().rstrip("\n").split("\n")
        assert len(new) <= b - a + 1
        lines[a - 1:b] = new + [""] * (b - a + 1 - len(new))
    put(3002, 3045, "g_3002_3045.java")
    put(1159, 1242, "g_1159_1242.java")
    # CFR moved `n6 *= 10` into the right side of `||` (g:4670, g:4683); the bytecode does it
    # on every pass before the test, otherwise 1 is drawn as "111" (javap g.b(Graphics,IIII)).
    bad = "if (++n7 % 3 != 0 || n4 / (n6 *= 10) <= 0) continue;"
    for ln in (4670, 4683):
        assert lines[ln - 1].strip() == bad, ln
        lines[ln - 1] = lines[ln - 1].replace(bad, "n6 *= 10; if (++n7 % 3 != 0 || n4 / n6 <= 0) continue;")
    # PORT-EXTRA heroes 4..9 (pow/game/heroes.py, pow_mp/faces.py): their face panels are
    # act24..35, not act 6/12 + face (act10, 11, 16, 17 are the CPU fighter's and the monster's)
    assert lines[5165 - 1].strip() == "cD = bZ[cL];"
    lines[5165 - 1] = lines[5165 - 1].replace("cD = bZ[cL];", "cD = bZ[cL] < 4 ? bZ[cL] : bZ[cL] + 14;")
    src = "\n".join(lines)
    src = re.sub(r'(?<![\w.])do(?=\s*[,;=)])', 'do_', src)
    src = re.sub(r'(?<=[(, ])do(?=,)', 'do_', src)
    return src.replace("Image do;", "Image do_;")


if __name__ == "__main__":
    main()
