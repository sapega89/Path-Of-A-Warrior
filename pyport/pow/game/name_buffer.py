"""at.java - text input buffer for the hero name. Literal port."""


class NameBuffer:
    def __init__(self, paramString, paramInt1, paramInt2):  # at.java:12-18
        self.a = list(paramString)   # StringBuffer
        self.b = paramInt1           # max length
        self.c = 0
        self.d = ' '
        self.e = len(paramString)

    def b_I(self, paramInt):  # at.java:20-23
        if self.e + paramInt >= 0 and self.e + paramInt <= self.b - 1 and self.b_v() == self.e + paramInt:
            self.e += paramInt

    def a_v(self):  # at.java:25-28
        return "".join(self.a)

    def a_T(self, paramString):  # at.java:30-32
        self.a = list(paramString)

    def b_v(self):  # at.java:34-42
        return 0 if len(self.a) == 0 else len(self.a)

    def a_I(self, paramInt):  # at.java:44-70
        i = len(self.a) - 1
        if paramInt == -7 or paramInt == -8:
            if i >= 0:
                del self.a[i:]          # setLength(i)
                self.c = 0
                self.b_I(-1)
            else:
                return 1
        elif 97 <= paramInt <= 122 or 65 <= paramInt <= 90:
            c = chr(paramInt)
            if self.d != c:
                self.c = 0
            self.d = c
            self.c += 1
            if len(self.a) == self.e:
                self.a.append(c)
                self.c = 1
            elif len(self.a) < self.b:
                if len(self.a) != 0:
                    self.b_I(1)
                self.a.append(c)
        return 0
