"""Small Java data classes (h.java, z.java, n.java, ...). Generated once from the Java source;
edited by hand since. Java -> Python names: pyport/NAMES.md."""

class Point:  # h.java
    def __init__(self):
        self.a = 0  # h.java:2 short
        self.b = 0  # h.java:4 short


class Rect:  # ac.java
    def __init__(self, paramInt1=0, paramInt2=0, paramInt3=0, paramInt4=0):
        self.a = 0  # ac.java:2 int
        self.b = 0  # ac.java:4 int
        self.c = 0  # ac.java:6 int
        self.d = 0  # ac.java:8 int
        self.a = paramInt1  # constructor
        self.b = paramInt2  # constructor
        self.c = paramInt3  # constructor
        self.d = paramInt4  # constructor


class MapMode:  # aa.java
    def __init__(self):
        self.a = 0  # aa.java:2 byte
        self.b = 0  # aa.java:4 byte


class Item:  # z.java
    def __init__(self):
        self.a = 0  # z.java:2 short
        self.b = 0  # z.java:4 short
        self.c = 0  # z.java:6 short
        self.d = 0  # z.java:8 short
        self.e = 0  # z.java:10 short
        self.f = 0  # z.java:12 byte

    def a(self):  # z.java:15-22
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0


class QuickSlot:  # p.java
    def __init__(self):
        self.a = 0  # p.java:2 short
        self.b = 0  # p.java:4 short


class GearDef:  # ai.java
    def __init__(self):
        self.a = None  # ai.java:2 String
        self.b = 0  # ai.java:4 short
        self.c = 0  # ai.java:6 short
        self.d = 0  # ai.java:8 short
        self.e = 0  # ai.java:10 short
        self.f = 0  # ai.java:12 short


class TreasureDef:  # t.java
    def __init__(self):
        self.a = None  # t.java:2 String
        self.b = 0  # t.java:4 byte
        self.c = 0  # t.java:6 short
        self.d = 0  # t.java:8 byte
        self.e = 0  # t.java:10 short
        self.f = 0  # t.java:12 byte
        self.g = 0  # t.java:14 byte
        self.h = 0  # t.java:16 short


class RareDef:  # ao.java
    def __init__(self):
        self.a = None  # ao.java:2 String
        self.b = 0  # ao.java:4 byte
        self.c = 0  # ao.java:6 short
        self.d = 0  # ao.java:8 byte
        self.e = 0  # ao.java:10 short
        self.f = 0  # ao.java:12 byte
        self.g = 0  # ao.java:14 short


class MapData:  # o.java
    def __init__(self):
        self.a = None  # o.java:2 short[]
        self.b = None  # o.java:4 aj
        self.c = 0  # o.java:6 int
        self.d = 0  # o.java:8 int
        self.e = 0  # o.java:10 int
        self.f = 0  # o.java:12 int

    def a_v(self):  # o.java (final void a())
        self.a = None


class MapSize:  # aj.java
    def __init__(self):
        self.a = 0  # aj.java:2 short
        self.b = 0  # aj.java:4 short
        self.c = 0  # aj.java:6 short


class ActiveEffect:  # ad.java
    def __init__(self):
        self.a = 0  # ad.java:2 short
        self.b = 0  # ad.java:4 short
        self.c = Point()  # ad.java:6 h
        self.d = 0  # ad.java:8 short
        self.e = 0  # ad.java:10 short
        self.f = 0  # ad.java:12 short
        self.g = None  # ad.java:14 byte[]
        self.h = None  # ad.java:16 y[]


class GeneralDef:  # am.java
    def __init__(self):
        self.a = None  # am.java:2 String
        self.b = 0  # am.java:4 char
        self.c = 0  # am.java:6 char
        self.d = [0] * 4  # am.java:8 char[]
        self.e = 0  # am.java:10 char
        self.f = 0  # am.java:12 char
        self.g = 0  # am.java:14 char
        self.h = 0  # am.java:16 char
        self.i = 0  # am.java:18 char


class InfoBox:  # ak.java
    def __init__(self):
        self.a = 0  # ak.java:2 byte
        self.b = Rect(0, 0, 0, 0)  # ak.java:4 ac
        self.c = None  # ak.java:6 String
        self.d = 0  # ak.java:8 short


class FloatingText:  # w.java
    def __init__(self):
        self.a = 0  # w.java:2 short
        self.b = 0  # w.java:4 short
        self.c = ""  # w.java:6 String
        self.d = 0  # w.java:8 short
        self.e = 0  # w.java:10 short


class Lord:  # an.java
    def __init__(self):
        self.a = 0  # an.java:2 short
        self.b = 0  # an.java:4 short
        self.c = 0  # an.java:6 short
        self.d = 0  # an.java:8 short
        self.e = 0  # an.java:10 short
        self.f = 0  # an.java:12 short
        self.g = 0  # an.java:14 short
        self.h = 0  # an.java:16 short
        self.i = 0  # an.java:18 short
        self.j = 0  # an.java:20 short


class SpriteFrame:  # y.java
    def __init__(self):
        self.a = 0  # y.java:2 short
        self.b = 0  # y.java:4 short
        self.c = 0  # y.java:6 short
        self.d = 0  # y.java:8 short
        self.e = 0  # y.java:10 short
        self.f = 0  # y.java:12 short


class Arrow:  # f.java
    def __init__(self):
        self.a = 0  # f.java:2 byte
        self.b = [None] * 2  # f.java:4 h[]
        self.c = 0  # f.java:6 byte
        self.d = 0  # f.java:8 byte
        self.e = 0  # f.java:10 byte
        self.f = 0  # f.java:12 short
        self.g = 0  # f.java:14 byte
        self.b[0] = Point()  # constructor
        self.b[1] = Point()  # constructor


class SpawnSpot:  # i.java
    def __init__(self):
        self.a = 0  # i.java:2 char
        self.b = 0  # i.java:4 char
        self.c = 0  # i.java:6 char


class Breakable:  # r.java
    def __init__(self):
        self.a = 0  # r.java:2 short
        self.b = Point()  # r.java:4 h
        self.c = Point()  # r.java:6 h
        self.d = 0  # r.java:8 short
        self.e = 0  # r.java:10 short
        self.f = 0  # r.java:12 short
        self.g = 0  # r.java:14 short
        self.h = 0  # r.java:16 short


class Drop:  # a.java
    def __init__(self):
        self.a = 0  # a.java:4 short
        self.b = None  # a.java:6 h
        self.c = 0  # a.java:8 short
        self.d = 0  # a.java:10 short
        self.e = 0  # a.java:12 short
        self.f = 0  # a.java:14 short
        self.g = None  # a.java:16 Image


class ScriptSlot:  # ah.java
    def __init__(self):
        self.a = 0  # ah.java:2 int
        self.b = 0  # ah.java:4 short
        self.c = 0  # ah.java:6 short


class RoomCell:  # au.java
    def __init__(self):
        self.a = [0] * 4  # au.java:2 short[]
        self.b = 0  # au.java:4 short
        self.c = 0  # au.java:6 short
        self.d = 0  # au.java:8 short
        self.e = 0  # au.java:10 short
        self.f = 0  # au.java:12 short
        self.g = 0  # au.java:14 short
        self.h = 0  # au.java:16 short
        self.i = 0  # au.java:18 short
        self.j = 0  # au.java:20 short
        self.k = 0  # au.java:22 short
        self.l = 0  # au.java:24 short
        self.m = 0  # au.java:26 short
        self.n = 0  # au.java:28 short
        self.o = 0  # au.java:30 short


class Actor:  # ap.java
    def __init__(self):
        self.a = [None] * 2  # ap.java:4 h[]
        self.b = None  # ap.java:6 h
        self.c = 0  # ap.java:8 byte
        self.d = 0  # ap.java:10 byte
        self.e = [0] * 2  # ap.java:12 byte[]
        self.f = [0] * 2  # ap.java:14 int[]
        self.g = [0] * 2  # ap.java:16 byte[]
        self.h = 0  # ap.java:18 short
        self.i = 0  # ap.java:20 short
        self.j = 0  # ap.java:22 short
        self.k = 0  # ap.java:24 short
        self.l = 0  # ap.java:26 short
        self.m = 0  # ap.java:28 short
        self.n = 0  # ap.java:30 short
        self.o = 0  # ap.java:32 short
        self.p = 0  # ap.java:34 short
        self.q = 0  # ap.java:36 short
        self.r = 0  # ap.java:38 byte
        self.s = 0  # ap.java:40 byte
        self.t = 0  # ap.java:42 byte
        self.u = 0  # ap.java:44 byte
        self.v = None  # ap.java:46 h
        self.w = 0  # ap.java:48 byte
        self.x = 0  # ap.java:50 byte
        self.y = 0  # ap.java:52 byte
        self.z = 0  # ap.java:54 byte
        self.A = 0  # ap.java:56 byte
        self.B = None  # ap.java:58 short[][][]
        self.C = None  # ap.java:60 Image
        self.D = None  # ap.java:62 y[]
        self.a[0] = Point()  # constructor
        self.a[1] = Point()  # constructor
        self.b = Point()  # constructor
        self.v = Point()  # constructor


class Hero:  # n.java
    def __init__(self):
        self.a = [None] * 2  # n.java:4 h[]
        self.b = [None] * 2  # n.java:6 h[]
        self.c = 0  # n.java:8 int
        self.d = [0] * 2  # n.java:10 int[]
        self.e = [0] * 2  # n.java:12 int[]
        self.f = [0] * 2  # n.java:14 short[]
        self.g = [0] * 22  # n.java:16 short[]
        self.h = 0  # n.java:18 short
        self.i = 0  # n.java:20 short
        self.j = None  # n.java:22 h
        self.k = None  # n.java:24 String
        self.l = 0  # n.java:26 int
        self.m = 0  # n.java:28 int
        self.n = 0  # n.java:30 int
        self.o = 0  # n.java:32 int
        self.p = 0  # n.java:34 int
        self.q = 0  # n.java:36 int
        self.r = 0  # n.java:38 int
        self.s = 0  # n.java:40 int
        self.t = 0  # n.java:42 int
        self.u = 0  # n.java:44 int
        self.v = 0  # n.java:46 int
        self.w = 0  # n.java:48 int
        self.x = 0  # n.java:50 int
        self.y = 0  # n.java:52 int
        self.z = 0  # n.java:54 int
        self.A = 0  # n.java:56 int
        self.B = 0  # n.java:58 int
        self.C = 0  # n.java:60 int
        self.D = 0  # n.java:62 int
        self.E = 0  # n.java:64 int
        self.F = 0  # n.java:66 int
        self.G = 0  # n.java:68 int
        self.H = 0  # n.java:70 int
        self.I = 0  # n.java:72 int
        self.J = 0  # n.java:74 int
        self.K = 0  # n.java:76 int
        self.L = 0  # n.java:78 int
        self.M = 0  # n.java:80 int
        self.N = 0  # n.java:82 int
        self.O = 0  # n.java:84 int
        self.P = 0  # n.java:86 int
        self.Q = None  # n.java:88 h
        self.R = 0  # n.java:90 int
        self.S = 0  # n.java:92 int
        self.T = 0  # n.java:94 int
        self.U = 0  # n.java:96 int
        self.V = [0] * 5  # n.java:98 int[]
        self.W = [0] * 19  # n.java:100 int[]
        self.X = [None] * 9  # n.java:102 z[]
        self.Y = [None] * 25  # n.java:104 z[]
        self.Z = [None] * 5  # n.java:106 p[]
        self.aa = [0] * 2  # n.java:108 int[]
        self.ab = [None] * 31  # n.java:110 short[][][]
        self.ac = [None] * 8  # n.java:112 short[][]
        self.ad = [[0] * 4 for _ in range(8)]  # n.java:114 short[][]
        self.ae = [[0] * 2 for _ in range(8)]  # n.java:116 short[][]
        self.af = [[0] * 2 for _ in range(8)]  # n.java:118 short[][]
        self.ag = [[0] * 2 for _ in range(8)]  # n.java:120 short[][]
        self.ah = [[0] * 3 for _ in range(8)]  # n.java:122 short[][]
        self.ai = [[0] * 3 for _ in range(8)]  # n.java:124 short[][]
        self.aj = [[0] * 3 for _ in range(8)]  # n.java:126 short[][]
        self.ak = [[0] * 3 for _ in range(8)]  # n.java:128 short[][]
        self.al = [[0] * 7 for _ in range(8)]  # n.java:130 short[][]
        self.am = [None] * 8  # n.java:132 short[][]
        self.an = [None] * 8  # n.java:134 short[][]
        self.ao = [None] * 8  # n.java:136 short[][]
        self.ap = [None] * 8  # n.java:138 short[][]
        self.aq = [None] * 8  # n.java:140 short[][]
        self.ar = [None] * 8  # n.java:142 short[][]
        self.as_ = [None] * 8  # n.java:144 short[][]
        self.at = [None] * 8  # n.java:146 short[][]
        self.au = [None] * 8  # n.java:148 short[][]
        self.av = [None] * 8  # n.java:150 short[][]
        self.aw = [None] * 8  # n.java:152 short[][]
        self.ax = [None] * 8  # n.java:154 short[][]
        self.ay = [None] * 8  # n.java:156 short[][]
        self.az = [None] * 8  # n.java:158 short[][]
        self.aA = [None] * 8  # n.java:160 short[][]
        self.aB = 0  # n.java:162 int
        self.aC = None  # n.java:164 y[]
        self.aD = None  # n.java:166 y[]
        self.aE = None  # n.java:168 y[]
        self.aF = None  # n.java:170 y[]
        self.aG = None  # n.java:172 Image
        self.aH = None  # n.java:174 Image

    def a_v(self):  # n.java:130-144
        for b in range(9):
            self.X[b] = Item()
        for b in range(25):
            self.Y[b] = Item()
        for b in range(5):
            self.Z[b] = QuickSlot()
        for b in range(2):
            self.a[b] = Point()
        for b in range(2):
            self.b[b] = Point()
        self.j = Point()
        self.Q = Point()
