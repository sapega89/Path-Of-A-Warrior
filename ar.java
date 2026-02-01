public final class ar extends ag {
  public ar() {
    super(ag.bs);
  }
  
  public final void a() {
    if (ag.cS.b != 0) {
      ag.cS.b();
      L();
    } else if (ag.cR.a != 0) {
      o();
      L();
    } else {
      ag.bd.i();
      L();
      aC();
      if (!this.gj) {
        O(1);
        return;
      } 
    } 
    O(0);
  }
  
  public final void b(int paramInt) {
    if (paramInt == 1) {
      K();
      for (byte b = 0; b < 9; b++) {
        for (byte b1 = 0; b1 < 9; b1++)
          ag.eE[b][b1] = 1; 
      } 
      ag.bd.c();
      if (ag.cR.a != 0) {
        ag.cS.b(170);
        switch (ag.cR.a) {
          case 1:
            ag.bb.f();
            break;
          case 2:
            ag.bb.d(0);
            ag.bb.k();
            break;
          case 3:
            ag.bb.j();
            break;
          case 4:
            ag.bb.l();
            break;
        } 
      } 
      if (ag.cS.b != 0) {
        ag.cS.c();
        ag.bb.n();
      } 
      return;
    } 
    if (paramInt == 2)
      return; 
    if (ag.cS.b != 0) {
      if (ag.cS.j != 0)
        ag.cS.c(); 
      ag.bb.n();
      return;
    } 
    if (ag.cR.a != 0) {
      if (ag.cR.b != 0) {
        switch (ag.cR.a) {
          case 1:
            ag.cS.b(170);
            ag.bb.f();
            break;
          case 2:
            ag.bb.d(1);
            break;
          case 3:
            ag.cS.b(170);
            ag.bb.j();
            break;
          case 4:
            ag.cS.b(170);
            ag.bb.l();
            break;
        } 
        ag.cR.b = 0;
      } 
      if (ag.cR.a == 2) {
        ag.bb.k();
        return;
      } 
    } else {
      ag.bd.c();
    } 
  }
  
  private void o() {
    byte[] arrayOfByte1 = { 0, 3, 0, 2, 4, 0, 0 };
    byte[] arrayOfByte2 = { 0, 3, 0, 5, 3, 0, 0 };
    switch (ag.ch) {
      case -1:
      case 50:
        switch (ag.cR.a) {
          case 1:
          case 3:
            ag.cM[1] = ag.cM[1] - 1;
            if (ag.cM[1] - 1 < 0)
              ag.cM[1] = ag.cN - 1; 
            if (ag.cM[1] == 1 && ag.cR.a == 3 && !ag.df)
              ag.cM[1] = 0; 
            if (ag.cM[1] == 2 && ag.cR.a == 1 && (ag.ez > 0 || ag.cr != 0 || ag.eD[0] != 0))
              ag.cM[1] = ag.cM[1] - 1; 
            ag.I();
            ag.cR.b = 1;
            break;
        } 
        return;
      case -2:
      case 56:
        switch (ag.cR.a) {
          case 1:
          case 3:
            ag.cM[1] = ag.cM[1] + 1;
            if (ag.cM[1] + 1 >= ag.cN)
              ag.cM[1] = 0; 
            if (ag.cM[1] == 1 && ag.cR.a == 3 && !ag.df)
              ag.cM[1] = 2; 
            if (ag.cM[1] == 2 && ag.cR.a == 1 && (ag.ez > 0 || ag.cr != 0 || ag.eD[0] != 0))
              ag.cM[1] = ag.cM[1] + 1; 
            ag.I();
            ag.cR.b = 1;
            break;
        } 
        return;
      case -3:
      case 52:
        switch (ag.cR.a) {
          case 2:
          case 4:
            ag.cM[1] = ag.cM[1] - 1;
            if (ag.cM[1] - 1 < 0)
              ag.cM[1] = ag.cN - 1; 
            ag.cR.b = 1;
            break;
          case 3:
            y(0);
            ag.cR.b = 1;
            break;
        } 
        return;
      case -4:
      case 54:
        switch (ag.cR.a) {
          case 2:
          case 4:
            ag.cM[1] = ag.cM[1] + 1;
            if (ag.cM[1] + 1 >= ag.cN)
              ag.cM[1] = 0; 
            ag.cR.b = 1;
            break;
          case 3:
            y(1);
            ag.cR.b = 1;
            break;
        } 
        return;
      case 42:
        switch (ag.cR.a) {
          case 2:
            ag.ck = c(0);
            break;
        } 
        return;
      case 35:
        switch (ag.cR.a) {
          case 2:
            ag.ck = c(1);
            break;
        } 
        return;
      case -5:
      case 53:
        if (ag.cM[0] == 10 && ag.cM[1] == 4) {
          ag.cM[0] = 5;
          ag.cM[1] = 3;
          ag.bW = ag.bV;
          ag.bV = 2;
          ag.bb.b();
          return;
        } 
        if (ag.cR.a == 1) {
          if (arrayOfByte1[ag.cM[1]] != 0) {
            ag.cR.a = arrayOfByte1[ag.cM[1]];
            ag.cN = arrayOfByte2[ag.cM[1]];
            ag.ck = 1;
            ag.cP[0] = (short)ag.cM[1];
            ag.cQ[0] = (short)ag.cM[2];
            ag.cM[1] = 0;
            ag.ej = 3;
            return;
          } 
          switch (ag.cM[1]) {
            case 2:
              if (ag.ez > 0 || ag.cr != 0 || ag.eD[0] != 0) {
                ag.cS.e(7);
                break;
              } 
              if (ar() != 0)
                ag.cS.e(0); 
              break;
            case 0:
              ag.ck = 1;
              ag.ct[10] = null;
              ag.ct[17] = null;
              ag.cR.a = 0;
              a_(-1);
              break;
            case 5:
              ag.cS.e(5);
              break;
            case 6:
              ag.cS.e(28);
              ag.ck = 1;
              break;
          } 
          return;
        } 
        if (ag.cR.a == 3) {
          y(1);
          ag.cR.b = 1;
          return;
        } 
        break;
      case -7:
        ag.ck = 1;
        if (ag.cR.a == 1) {
          ag.ct[10] = null;
          ag.ct[17] = null;
          ag.cR.a = 0;
          a_(-1);
          return;
        } 
        ag.cR.a = 1;
        ag.cM[1] = ag.cP[0];
        ag.cM[2] = ag.cQ[0];
        ag.cN = 7;
        break;
    } 
  }
  
  static int c(int paramInt) {
    if ((ag.cz.Z[ag.cM[1]]).a != 0 && ag.cz.aa[paramInt] != ag.cM[1]) {
      if (ag.cM[1] == ag.cz.aa[paramInt + 1 & 0x1]) {
        int i = ag.cz.aa[paramInt];
        ag.cz.aa[paramInt] = ag.cz.aa[paramInt + 1 & 0x1];
        ag.cz.aa[paramInt + 1 & 0x1] = i;
      } else {
        ag.cz.aa[paramInt] = (byte)ag.cM[1];
      } 
      return 1;
    } 
    return 0;
  }
  
  static void b() {
    if (ag.cz.p > ag.cz.y)
      ag.cz.p = ag.cz.y; 
    if (ag.cz.r > ag.cz.z)
      ag.cz.r = ag.cz.z; 
  }
  
  private static int Q(int paramInt) {
    return (paramInt < 0) ? -paramInt : paramInt;
  }
  
  private boolean a(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, int paramInt6, int paramInt7, int paramInt8) {
    int i = (paramInt3 + paramInt7) / 2;
    int j = (paramInt4 + paramInt8) / 2;
    int k = paramInt1 + paramInt3 / 2 - paramInt5 + paramInt7 / 2;
    int m = paramInt2 + paramInt4 / 2 - paramInt6 + paramInt8 / 2;
    int n = Q(k);
    int i1 = Q(m);
    return (n < i && i1 < j);
  }
  
  private void b(int paramInt1, int paramInt2) {
    int i;
    (ag.ex[paramInt1]).t = 1;
    if (paramInt2 > -1) {
      (ag.ex[paramInt1]).e[0] = (ag.ex[paramInt1]).d = b((ag.ex[paramInt1]).a[0], ag.cz.a[0]);
    } else {
      (ag.ex[paramInt1]).e[0] = (ag.ex[paramInt1]).d = b((ag.ex[paramInt1]).a[0], ag.dU.c);
    } 
    switch (paramInt2) {
      case 3:
      case 4:
      case 5:
      case 6:
      case 7:
      case 8:
        (ag.ex[paramInt1]).m = (short)((ag.ex[paramInt1]).m - (((i = ag.cz.w + ag.cz.A - (ag.ex[paramInt1]).k - (ag.ex[paramInt1]).o) > 0) ? i : 1));
        break;
      case 12:
      case 13:
      case 14:
      case 20:
      case 21:
      case 22:
      case 23:
      case 24:
      case 25:
      case 26:
      case 27:
      case 28:
      case 29:
      case 30:
        (ag.ex[paramInt1]).m = (short)((ag.ex[paramInt1]).m - (((i = ag.cz.w + ag.cz.A + ag.cz.w * ag.cz.W[paramInt2 - 12] / ae.aU[paramInt2 - 12] - (ag.ex[paramInt1]).k - (ag.ex[paramInt1]).o) > 0) ? i : 1));
        break;
      case -2:
        (ag.ex[paramInt1]).A = 2;
        (ag.ex[paramInt1]).m = (short)((ag.ex[paramInt1]).m - ((ag.cz.l << 1 > 50) ? 50 : (ag.cz.l << 1)));
        a_(4);
        break;
      case -1:
        (ag.ex[paramInt1]).m = (short)((ag.ex[paramInt1]).m - ((ag.cz.l > 30) ? 30 : ag.cz.l));
        a_(3);
        break;
    } 
    if ((ag.ex[paramInt1]).m < 1) {
      (ag.ex[paramInt1]).m = 0;
      (ag.ex[paramInt1]).g[0] = 3;
    } else {
      (ag.ex[paramInt1]).g[0] = 0;
    } 
    R(paramInt1);
    (ag.ex[paramInt1]).v = (ag.ex[paramInt1]).a[0];
    (ag.ex[paramInt1]).u = -1;
    (ag.ex[paramInt1]).f[0] = 2;
    if ((ag.ex[paramInt1]).h < 200 && C(1000) < 150 && (ag.ex[paramInt1]).m > 0)
      m(paramInt1, 1); 
  }
  
  private void m(int paramInt1, int paramInt2) {
    (ag.ex[paramInt1]).f[0] = (byte)(6 + ag.dC.d[C(4)] - 1);
    if ((ag.ex[paramInt1]).f[0] < 6 && (ag.ex[paramInt1]).f[0] > 21) {
      (ag.ex[paramInt1]).f[0] = 1;
    } else {
      switch ((ag.ex[paramInt1]).f[0]) {
        case 9:
        case 10:
          if ((ag.ex[paramInt1]).z > 3) {
            (ag.ex[paramInt1]).f[0] = 1;
            break;
          } 
          if ((ag.ex[paramInt1]).l >> 1 > (ag.ex[paramInt1]).m) {
            (ag.ex[paramInt1]).z = (byte)((ag.ex[paramInt1]).z + 1);
            break;
          } 
          (ag.ex[paramInt1]).f[0] = 1;
          break;
        case 11:
        case 12:
        case 13:
          if (paramInt2 != 0)
            (ag.ex[paramInt1]).f[0] = 1; 
          break;
      } 
    } 
    (ag.ex[paramInt1]).e[0] = (ag.ex[paramInt1]).d = a((ag.ex[paramInt1]).a[0], ag.cz.a[0]);
  }
  
  final void c() {
    h h = new h();
    for (byte b = 0; b < ag.cB; b++) {
      if ((ag.cA[b]).a != 0 && (ag.cA[b]).d > 0)
        switch (ag.cz.e[0]) {
          case 13:
            if (a((ag.cz.a[0]).a + ae.aF[ag.cz.d[0] >> 1], (ag.cz.a[0]).b + ae.aG[ag.cz.d[0] >> 1], ae.aH[ag.cz.d[0] >> 1], ae.aI[ag.cz.d[0] >> 1], (ag.cA[b]).b.a - 8, (ag.cA[b]).b.b - 8, 18, 18))
              W(b); 
            break;
          case 22:
            if (a(ag.cz.a[0], (ag.cA[b]).b, ag.cz.d[0]) != 0)
              s(b, ae.aK[ag.cz.K]); 
            break;
          case 23:
          case 24:
            s(b, 45);
            break;
          case 25:
            if ((ag.cz.d[0] + (ag.cz.f[0] >> 1 << 1) & 0x7) == a(ag.cz.a[0], (ag.cA[b]).b))
              s(b, ae.aK[ag.cz.K]); 
            break;
          case 26:
          case 27:
            h.a = (short)((ag.cz.a[0]).a + ae.aA[ag.cz.d[0] >> 1]);
            h.b = (short)((ag.cz.a[0]).b + ae.aB[ag.cz.d[0] >> 1]);
            if (c(h, (ag.cA[b]).b) <= 35)
              W(b); 
            break;
          case 28:
          case 29:
          case 30:
            W(b);
            break;
          default:
            p(b, ae.aK[ag.cz.K]);
            break;
        }  
    } 
  }
  
  private static void R(int paramInt) {
    ag.dT.a = 1;
    ag.dT.b = 10;
    ag.dT.d = (ag.ex[paramInt]).i;
    ag.dT.e = (short)((ag.ex[paramInt]).m * 60 / (ag.ex[paramInt]).l);
    if ((ag.ex[paramInt]).h < 200) {
      ag.dT.c = ag.dC.a;
      return;
    } 
    ag.dT.e = (short)(ag.dT.e >> 1);
    ag.dT.c = ae.aS[(ag.ex[paramInt]).h - 201];
  }
  
  private static byte a(h paramh1, h paramh2, int paramInt) {
    switch (paramInt) {
      case 2:
        if (paramh1.a > paramh2.a)
          return 1; 
        break;
      case 6:
        if (paramh1.a < paramh2.a)
          return 1; 
        break;
      case 0:
        if (paramh1.b < paramh2.b)
          return 1; 
        break;
      case 4:
        if (paramh1.b > paramh2.b)
          return 1; 
        break;
    } 
    return 0;
  }
  
  private static byte a(h paramh1, h paramh2) {
    int i = paramh2.a - paramh1.a;
    int j;
    return ((j = paramh2.b - paramh1.b) > i) ? ((j > -i) ? 0 : 2) : ((j > -i) ? 6 : 4);
  }
  
  private static byte b(h paramh1, h paramh2) {
    int i = paramh2.a - paramh1.a;
    int j = paramh2.b - paramh1.b;
    return (i + i < j) ? ((i + i > -j) ? 0 : ((-i < j + j) ? 1 : ((i < j + j) ? 2 : 3))) : ((i + i < -j) ? 4 : ((-i > j + j) ? 5 : ((i > j + j) ? 6 : 7)));
  }
  
  private static int c(h paramh1, h paramh2) {
    int j = paramh1.a - paramh2.a;
    int k = paramh1.b - paramh2.b;
    int m = j * j + k * k;
    j = (j < 0) ? -j : j;
    k = (k < 0) ? -k : k;
    int i;
    for (i = (j > k) ? j : k; i * i < m; i += 2);
    if (--i * i < m)
      i++; 
    return i;
  }
  
  private void n(int paramInt1, int paramInt2) {
    if (ag.cz.d[0] == a(ag.cz.a[0], (ag.ex[paramInt1]).a[0]))
      q(paramInt1, paramInt2); 
  }
  
  private void o(int paramInt1, int paramInt2) {
    if ((ag.ex[paramInt1]).e[0] == a((ag.ex[paramInt1]).a[0], ag.cz.a[0]))
      r(paramInt1, paramInt2); 
  }
  
  private void p(int paramInt1, int paramInt2) {
    if (ag.cz.d[0] == a(ag.cz.a[0], (ag.cA[paramInt1]).b))
      s(paramInt1, paramInt2); 
  }
  
  private void q(int paramInt1, int paramInt2) {
    if (c(ag.cz.a[0], (ag.ex[paramInt1]).a[0]) <= paramInt2)
      S(paramInt1); 
  }
  
  private void r(int paramInt1, int paramInt2) {
    if (c(ag.cz.a[0], (ag.ex[paramInt1]).a[0]) <= paramInt2)
      T(paramInt1); 
  }
  
  private void s(int paramInt1, int paramInt2) {
    if (c(ag.cz.a[0], (ag.cA[paramInt1]).b) <= paramInt2)
      W(paramInt1); 
  }
  
  private void S(int paramInt) {
    h h = new h();
    if ((ag.ex[paramInt]).f[0] > 5)
      return; 
    b(paramInt, ag.cz.e[0]);
    if (ag.cz.M > 1 && ag.cz.e[0] < 12)
      (ag.ex[paramInt]).A = 1; 
    switch (ag.cz.e[0]) {
      case 12:
        ag.cz.f[0] = 5;
        (ag.ex[paramInt]).A = 2;
        break;
      case 14:
      case 22:
        (ag.ex[paramInt]).A = 2;
        break;
      case 20:
        (ag.ex[paramInt]).t = (byte)(C(2) + 1);
        (ag.ex[paramInt]).A = 0;
        break;
      case 21:
        (ag.ex[paramInt]).A = 5;
        break;
      case 24:
        (ag.ex[paramInt]).A = 5;
      case 23:
        V(paramInt);
        break;
      case 25:
        (ag.ex[paramInt]).A = 2;
      case 27:
        (ag.ex[paramInt]).A = 5;
      case 26:
        (ag.ex[paramInt]).t = 2;
        h.a = (short)((ag.cz.a[0]).a + ae.aA[ag.cz.d[0] >> 1]);
        h.b = (short)((ag.cz.a[0]).b + ae.aB[ag.cz.d[0] >> 1]);
        (ag.ex[paramInt]).e[0] = (ag.ex[paramInt]).d = b((ag.ex[paramInt]).a[0], h);
        break;
      case 29:
        V(paramInt);
        break;
    } 
    if ((ag.ex[paramInt]).A != 0);
    a_(16);
  }
  
  private void T(int paramInt) {
    switch ((ag.ex[paramInt]).f[0]) {
      case 6:
        (ag.ex[paramInt]).g[0] = 5;
        ag.cz.R = 2;
        break;
      case 8:
      case 16:
        ag.cz.R = 2;
        break;
      case 14:
        ag.cz.O = C(2) + 1;
        break;
      case 15:
        ag.cz.R = 5;
        break;
      case 18:
        ag.cz.R = 5;
      case 17:
        p();
        break;
      case 19:
        ag.cz.R = 2;
        p();
        break;
      case 21:
        ag.cz.R = 5;
      case 20:
        ag.cz.O = 2;
        break;
    } 
    U(paramInt);
  }
  
  private void U(int paramInt) {
    if (paramInt > -1) {
      int i;
      ag.cz.d[0] = ag.cz.c = b(ag.cz.a[0], (ag.ex[paramInt]).a[0]);
      switch ((ag.ex[paramInt]).f[0]) {
        case 6:
        case 7:
        case 8:
        case 14:
        case 15:
        case 16:
        case 17:
        case 18:
        case 19:
        case 20:
        case 21:
          i = ((i = (ag.ex[paramInt]).j + (ag.ex[paramInt]).n + (ag.ex[paramInt]).j / ae.aU[(ag.ex[paramInt]).f[0] - 6] - ag.cz.x - ag.cz.B) > 0) ? i : 1;
          if (ag.cz.p > i) {
            ag.cz.p -= i;
            break;
          } 
          ag.cz.p = 0;
          break;
        default:
          i = ((i = (ag.ex[paramInt]).j + (ag.ex[paramInt]).n - ag.cz.x - ag.cz.B) > 0) ? i : 1;
          if (ag.cz.p > i) {
            ag.cz.p -= i;
            break;
          } 
          ag.cz.p = 0;
          break;
      } 
    } else {
      ag.cz.d[0] = ag.cz.c = ((ag.eC[paramInt + 3]).e << 1) + 4 & 0x7;
      int i;
      byte b = ((i = (ag.eC[paramInt + 3]).f - ag.cz.x - ag.cz.B) > 0) ? i : 1;
      if (ag.cz.p > b) {
        ag.cz.p -= b;
      } else {
        ag.cz.p = 0;
      } 
    } 
    if (paramInt > -1)
      R(paramInt); 
    ag.cz.Q = ag.cz.a[0];
    ag.cz.O = 1;
    ag.cz.P = -1;
    ag.cz.f[0] = 0;
    ag.cz.e[0] = 9;
    if (ag.cz.R != 0) {
      a_(4);
    } else {
      a_(16);
    } 
    if (ag.cz.p < 1) {
      ag.cz.p = 0;
      ag.cz.e[0] = 10;
    } 
  }
  
  private void V(int paramInt) {
    (ag.ex[paramInt]).w = 1;
    (ag.ex[paramInt]).x = 0;
    ag.ff = 7;
    a_(13);
    if (ag.fd == null) {
      ag.fe = K(60);
      ag.fd = new byte[ae.ao.length];
      for (byte b = 0; b < ae.ao.length; b++)
        ag.fd[b] = ae.ao[b]; 
    } 
  }
  
  private void p() {
    ag.cz.T = 1;
    ag.cz.U = 0;
    a_(13);
    if (ag.eX == null) {
      ag.eY = K(60);
      ag.eX = ae.ao;
    } 
  }
  
  private void W(int paramInt) {
    (ag.cA[paramInt]).d = (short)((ag.cA[paramInt]).d - ag.cz.w + ag.cz.A);
    a_(3);
    (ag.cA[paramInt]).h = 2;
    if ((ag.cA[paramInt]).d < 1) {
      (ag.cA[paramInt]).e = 12;
      int i = (ag.cA[paramInt]).c.b * ag.cE.b.a + (ag.cA[paramInt]).c.a;
      ag.cE.a[ag.cE.e + i] = 0;
    } 
  }
  
  final void d(int paramInt) {
    h h = new h();
    for (byte b = 0; b < ag.ez; b++) {
      short s = ag.ey[b];
      if ((ag.ex[s]).m > 0 && (ag.ex[s]).r != 0 && (ag.ex[s]).f[0] < 6)
        switch (paramInt) {
          case 0:
            switch (ag.cz.e[0]) {
              case 13:
                if (a((ag.cz.a[0]).a + ae.aF[ag.cz.d[0] >> 1], (ag.cz.a[0]).b + ae.aG[ag.cz.d[0] >> 1], ae.aH[ag.cz.d[0] >> 1], ae.aI[ag.cz.d[0] >> 1], ((ag.ex[s]).a[0]).a - 8, ((ag.ex[s]).a[0]).b - 8, 17, 17)) {
                  b(s, ag.cz.e[0]);
                  a_(3);
                } 
                break;
              case 22:
                if (a(ag.cz.a[0], (ag.ex[s]).a[0], ag.cz.d[0]) != 0)
                  q(s, ae.aK[ag.cz.K]); 
                break;
              case 23:
              case 24:
                q(s, 45);
                break;
              case 25:
                if ((ag.cz.d[0] + (ag.cz.f[0] >> 1 << 1) & 0x7) == a(ag.cz.a[0], (ag.ex[s]).a[0]))
                  q(s, ae.aK[ag.cz.K]); 
                break;
              case 26:
              case 27:
                h.a = (short)((ag.cz.a[0]).a + ae.aA[ag.cz.d[0] >> 1]);
                h.b = (short)((ag.cz.a[0]).b + ae.aB[ag.cz.d[0] >> 1]);
                if (c(h, (ag.ex[s]).a[0]) <= 35)
                  S(s); 
                break;
              case 28:
              case 29:
              case 30:
                S(s);
                break;
            } 
            n(s, ae.aK[ag.cz.K]);
            break;
          case -2:
          case -1:
            if (c(ag.dU.c, (ag.ex[s]).a[0]) <= 35) {
              b(s, ag.dU.a);
              a_(4);
            } 
            break;
        }  
    } 
  }
  
  final void d() {
    if (ag.eA < (ag.eO[ag.eP]).b) {
      switch (ag.eD[0]) {
        case 0:
          return;
      } 
      if ((ag.eD[0] >= 200 || ag.eB == 0) && ag.ev != 0) {
        int i = C(ag.ev);
        ag.bd.b(ag.eD[0], (ag.eu[i]).a, (ag.eu[i]).b, (ag.eu[i]).c);
        ag.eD[1] = (short)(ag.eD[1] - 1);
        if (ag.eD[1] < 1)
          for (byte b = 0; b < 12; b++)
            ag.eD[b] = ag.eD[b + 2];  
      } 
    } 
  }
  
  static int e(int paramInt) {
    byte[] arrayOfByte1 = { 
        5, 6, 7, 10, 15, 7, 10, 10, 8, 9, 
        10, 5, 6, 7, 9, 12, 20, 20, 20 };
    byte[] arrayOfByte2 = { 
        3, 4, 5, 3, 4, 3, 3, 5, 3, 4, 
        5, 3, 4, 5, 5, 6, 5, 5, 5 };
    int i = 0;
    if (paramInt >= 12 && paramInt <= 30)
      i = arrayOfByte1[paramInt - 12] + (ag.cz.W[paramInt - 12] - 1) * arrayOfByte2[paramInt - 12]; 
    if (i > ag.cz.r)
      return 0; 
    ag.cz.r -= i;
    return i;
  }
  
  static int e() {
    if (ag.cs[0] > -1) {
      if (ag.dh >= 3)
        return (ag.cs[0] == ag.cs[1] || ag.cs[0] == ag.cs[2] || ag.cs[0] == ag.cs[3]) ? 1 : 0; 
      if (ag.cs[0] == ag.cs[1] || ag.cs[0] == ag.cs[2])
        return 1; 
    } 
    return 0;
  }
  
  final int a(h paramh, int paramInt1, int paramInt2) {
    int[] arrayOfInt1 = new int[2];
    int[] arrayOfInt2 = new int[2];
    int[] arrayOfInt3 = new int[2];
    while (true) {
      byte b2 = 0;
      switch (paramInt2) {
        case 2:
          arrayOfInt2[0] = (paramh.b - 20) / 27;
          arrayOfInt2[1] = (paramh.b + 6) / 27;
          arrayOfInt1[1] = (paramh.a + paramInt1 - 12) / 27;
          arrayOfInt1[0] = (paramh.a + paramInt1 - 12) / 27;
          break;
        case 6:
          arrayOfInt2[0] = (paramh.b - 20) / 27;
          arrayOfInt2[1] = (paramh.b + 6) / 27;
          arrayOfInt1[1] = (paramh.a + paramInt1 + 12) / 27;
          arrayOfInt1[0] = (paramh.a + paramInt1 + 12) / 27;
          break;
        case 4:
          arrayOfInt1[0] = (paramh.a - 12) / 27;
          arrayOfInt1[1] = (paramh.a + 12) / 27;
          arrayOfInt2[1] = (paramh.b + paramInt1 - 20) / 27;
          arrayOfInt2[0] = (paramh.b + paramInt1 - 20) / 27;
          break;
        case 0:
          arrayOfInt1[0] = (paramh.a - 12) / 27;
          arrayOfInt1[1] = (paramh.a + 12) / 27;
          arrayOfInt2[1] = (paramh.b + paramInt1 + 6) / 27;
          arrayOfInt2[0] = (paramh.b + paramInt1 + 6) / 27;
          break;
      } 
      for (byte b1 = 0; b1 < 2; b1++) {
        arrayOfInt3[b1] = arrayOfInt2[b1] * ag.cE.b.a + arrayOfInt1[b1];
        if ((ag.cE.a[Math.min(ag.cE.f + arrayOfInt3[b1], ag.cE.a.length - 1)] & 0x1) != 0 || ag.cE.a[Math.min(ag.cE.e + arrayOfInt3[b1], ag.cE.a.length - 1)] != 0)
          b2++; 
      } 
      if (b2 != 0) {
        int[] arrayOfInt;
        paramInt1 = (arrayOfInt = t(b2, paramInt1))[1];
        if (0 == paramInt1)
          return 0; 
        continue;
      } 
      return paramInt1;
    } 
  }
  
  private static int[] t(int paramInt1, int paramInt2) {
    if (paramInt1 > 0) {
      paramInt1--;
    } else if (paramInt1 < 0) {
      paramInt1++;
    } 
    if (paramInt2 > 0) {
      paramInt2--;
    } else if (paramInt2 < 0) {
      paramInt2++;
    } 
    int[] arrayOfInt;
    (arrayOfInt = new int[2])[0] = paramInt1;
    arrayOfInt[1] = paramInt2;
    return arrayOfInt;
  }
  
  final int[] b(h paramh, int paramInt1, int paramInt2) {
    short[] arrayOfShort = { 
        18, 144, 270, 396, 522, 648, 774, 900, 1026, 1152, 
        1278 };
    for (byte b = 0; b < 11; b++)
      arrayOfShort[b] = (short)(arrayOfShort[b] * 3 / 2); 
    h h1;
    (h1 = new h()).a = (short)(paramh.a + paramInt1);
    h1.b = (short)(paramh.b + paramInt2);
    if (h1.a < arrayOfShort[ag.cf.a] + 12) {
      paramInt1 = arrayOfShort[ag.cf.a] + 12 - paramh.a;
      if (ag.co == 1)
        X(2); 
    } else if (h1.a > arrayOfShort[ag.cf.a + 1] - 12) {
      paramInt1 = arrayOfShort[ag.cf.a + 1] - 12 - paramh.a;
      if (ag.co == 1)
        X(4); 
    } 
    if (h1.b < arrayOfShort[ag.cf.b] + 10) {
      paramInt2 = arrayOfShort[ag.cf.b] + 10 - paramh.b;
      if (ag.co == 1)
        X(3); 
    } else if (h1.b > arrayOfShort[ag.cf.b + 1] + 10) {
      paramInt2 = arrayOfShort[ag.cf.b + 1] + 10 - paramh.b;
      if (ag.co == 1)
        X(1); 
    } 
    int[] arrayOfInt;
    (arrayOfInt = new int[2])[0] = paramInt1;
    arrayOfInt[1] = paramInt2;
    return arrayOfInt;
  }
  
  private static void X(int paramInt) {
    if (ag.cn < 0 && (ag.eO[ag.eP]).a[paramInt - 1] != 0) {
      ag.cp = (short)paramInt;
      switch (paramInt) {
        case 1:
          ag.eP = (short)(ag.eP + ag.cE.b.a / 7);
          break;
        case 2:
          ag.eP = (short)(ag.eP - 1);
          break;
        case 3:
          ag.eP = (short)(ag.eP - ag.cE.b.a / 7);
          break;
        case 4:
          ag.eP = (short)(ag.eP + 1);
          break;
      } 
      for (byte b = 0; b < 4; b++)
        ag.ct[21 + b] = null; 
      ag.cm = 0;
    } 
  }
  
  static int c(h paramh, int paramInt1, int paramInt2) {
    byte b;
    int i;
    byte b1 = 0;
    int j = paramh.a / 27;
    int k = paramh.b / 27;
    int m = j + k * ag.cE.b.a;
    int[] arrayOfInt1 = { 0, 0 };
    int[] arrayOfInt2 = { 1, 1 };
    h h1 = null;
    if (paramInt2 == -1) {
      h1 = ag.cz.j;
    } else {
      h1 = (ag.ex[paramInt2]).b;
    } 
    switch (paramInt1) {
      case 0:
      case 6:
        b1 = 1;
        break;
      case 2:
      case 4:
        b1 = -1;
        break;
    } 
    switch (paramInt1) {
      case 0:
      case 4:
        i = m + ag.cE.b.a * b1;
        if (0 == (ag.cE.a[ag.cE.f + i] & 0x1) && 0 == ag.cE.a[ag.cE.e + i]) {
          h1.b = 0;
          int n = j * 27 + 8;
          if (paramh.a > n) {
            if (paramh.a - n > 3) {
              h1.a = -3;
            } else {
              h1.a = (short)(n - paramh.a);
            } 
          } else if (n - paramh.a > 3) {
            h1.a = 3;
          } else {
            h1.a = (short)(n - paramh.a);
          } 
          return 8;
        } 
        for (b = 1; b < 6; b++) {
          if (j + b < ag.cE.b.a) {
            i = m + b;
            if (0 == (ag.cE.a[ag.cE.f + i] & 0x1) && 0 == ag.cE.a[ag.cE.e + i] && arrayOfInt2[0] != 0) {
              i = m + b + ag.cE.b.a * b1;
              if (0 == (ag.cE.a[ag.cE.f + i] & 0x1) && 0 == ag.cE.a[ag.cE.e + i])
                arrayOfInt1[0] = 1; 
            } else {
              arrayOfInt2[0] = 0;
            } 
          } 
          if (j - b > -1) {
            i = m - b;
            if (0 == (ag.cE.a[ag.cE.f + i] & 0x1) && 0 == ag.cE.a[ag.cE.e + i] && arrayOfInt2[1] != 0) {
              i = m - b + ag.cE.b.a * b1;
              if (0 == (ag.cE.a[ag.cE.f + i] & 0x1) && 0 == ag.cE.a[ag.cE.e + i])
                arrayOfInt1[1] = 1; 
            } else {
              arrayOfInt2[1] = 0;
            } 
          } 
          if (arrayOfInt1[0] != 0 && arrayOfInt1[1] != 0)
            return (paramh.a - j * 27 > 8) ? 6 : 2; 
          if (arrayOfInt1[0] != 0)
            return 6; 
          if (arrayOfInt1[1] != 0)
            return 2; 
        } 
        break;
      case 2:
      case 6:
        i = m + b1;
        if (0 == (ag.cE.a[ag.cE.f + i] & 0x1) && 0 == ag.cE.a[ag.cE.e + i]) {
          h1.a = 0;
          int n = k * 27 + 20;
          if (paramh.b > n) {
            if (paramh.b - n > 4) {
              h1.b = -4;
            } else {
              h1.b = (short)(n - paramh.b);
            } 
          } else if (n - paramh.b > 4) {
            h1.b = 4;
          } else {
            h1.b = (short)(n - paramh.b);
          } 
          return 8;
        } 
        for (b = 1; b < 6; b++) {
          if (k + b < ag.cE.b.b) {
            i = m + b * ag.cE.b.a;
            if (0 == (ag.cE.a[ag.cE.f + i] & 0x1) && 0 == ag.cE.a[ag.cE.e + i] && arrayOfInt2[0] != 0) {
              i = m + b * ag.cE.b.a + b1;
              if (0 == (ag.cE.a[ag.cE.f + i] & 0x1) && 0 == ag.cE.a[ag.cE.e + i])
                arrayOfInt1[0] = 1; 
            } else {
              arrayOfInt2[0] = 0;
            } 
          } 
          if (k - b > -1) {
            i = m - b * ag.cE.b.a;
            if (0 == (ag.cE.a[ag.cE.f + i] & 0x1) && 0 == ag.cE.a[ag.cE.e + i] && arrayOfInt2[1] != 0) {
              i = m - b * ag.cE.b.a + b1;
              if (0 == (ag.cE.a[ag.cE.f + i] & 0x1) && 0 == ag.cE.a[ag.cE.e + i])
                arrayOfInt1[1] = 1; 
            } else {
              arrayOfInt2[1] = 0;
            } 
          } 
          if (arrayOfInt1[0] != 0 && arrayOfInt1[1] != 0)
            return (paramh.b - k * 27 > 8) ? 0 : 4; 
          if (arrayOfInt1[0] != 0)
            return 0; 
          if (arrayOfInt1[1] != 0)
            return 4; 
        } 
        break;
    } 
    return -1;
  }
  
  private static int u(int paramInt1, int paramInt2) {
    byte[][] arrayOfByte = { { 
          0, 1, 1, 2, 3, 4, 4, 5, 6, 7, 
          7, 8, 8, 9, 10, 10, 11 }, { 
          0, 2, 3, 4, 6, 7, 8, 9, 11, 13, 
          14, 16, 17, 18, 20, 21, 23 } };
    return (paramInt1 < 0) ? -arrayOfByte[paramInt2][Math.min(16, -paramInt1)] : arrayOfByte[paramInt2][Math.min(16, paramInt1)];
  }
  
  final int a(h paramh, int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    h h1;
    int i = 0;
    int j = 0;
    if (paramInt3 == 8) {
      if (paramInt4 < 0) {
        paramInt1 = ag.cz.j.a;
        paramInt2 = ag.cz.j.b;
      } else {
        paramInt1 = (ag.ex[paramInt4]).b.a;
        paramInt2 = (ag.ex[paramInt4]).b.b;
      } 
    } else {
      if (paramInt1 > 0) {
        i = a(paramh, paramInt1, 6);
      } else if (paramInt1 < 0) {
        i = a(paramh, paramInt1, 2);
      } 
      if (paramInt2 > 0) {
        j = a(paramh, paramInt2, 0);
      } else if (paramInt2 < 0) {
        j = a(paramh, paramInt2, 4);
      } 
    } 
    switch (paramInt3) {
      case 2:
      case 6:
        if (0 == i)
          return -1; 
        break;
      case 0:
      case 4:
        if (0 == j)
          return -1; 
        break;
      case 1:
        if (i != 0 && j != 0)
          break; 
        if (i != 0) {
          paramInt3 = 2;
          i = a(paramh, u(paramInt1, 1), 2);
          break;
        } 
        if (j != 0) {
          paramInt3 = 0;
          j = a(paramh, u(paramInt2, 1), 0);
          break;
        } 
        return -1;
      case 3:
        if (i != 0 && j != 0)
          break; 
        if (i != 0) {
          paramInt3 = 2;
          i = a(paramh, u(paramInt1, 1), 2);
          break;
        } 
        if (j != 0) {
          paramInt3 = 4;
          j = a(paramh, u(paramInt2, 1), 4);
          break;
        } 
        return -1;
      case 5:
        if (i != 0 && j != 0)
          break; 
        if (i != 0) {
          paramInt3 = 6;
          i = a(paramh, u(paramInt1, 1), 6);
          break;
        } 
        if (j != 0) {
          paramInt3 = 4;
          j = a(paramh, u(paramInt2, 1), 4);
          break;
        } 
        return -1;
      case 7:
        if (i != 0 && j != 0)
          break; 
        if (i != 0) {
          paramInt3 = 6;
          i = a(paramh, u(paramInt1, 1), 6);
          break;
        } 
        if (j != 0) {
          paramInt3 = 0;
          j = a(paramh, u(paramInt2, 1), 0);
          break;
        } 
        return -1;
      case 8:
        h1 = null;
        if (paramInt4 == -1) {
          h1 = ag.cz.j;
        } else {
          h1 = (ag.ex[paramInt4]).b;
        } 
        i = h1.a;
        j = h1.b;
        if (h1.a > 0) {
          paramInt3 = 6;
          break;
        } 
        if (h1.a < 0) {
          paramInt3 = 2;
          break;
        } 
        if (h1.b > 0) {
          paramInt3 = 0;
          break;
        } 
        if (h1.b < 0)
          paramInt3 = 4; 
        break;
    } 
    int[] arrayOfInt;
    i = (arrayOfInt = b(paramh, i, j))[0];
    j = arrayOfInt[1];
    if (i != 0 || j != 0) {
      i = (arrayOfInt = a(paramh, i, j, paramInt4))[0];
      j = arrayOfInt[1];
      if (i == 0 && j == 0)
        return 9; 
    } 
    paramh.a = (short)(paramh.a + i);
    paramh.b = (short)(paramh.b + j);
    return paramInt3;
  }
  
  private int[] a(h paramh, int paramInt1, int paramInt2, int paramInt3) {
    byte b = 0;
    h h1;
    (h1 = new h()).a = (short)(paramh.a + paramInt1);
    h1.b = (short)(paramh.b + paramInt2);
    if (paramInt3 > -1) {
      int i = c(h1, ag.cz.a[0]);
      int j = c(paramh, ag.cz.a[0]);
      if (i < j && i < 20)
        while (Q(h1.a - (ag.cz.a[0]).a) <= 27 && Q(h1.b - (ag.cz.a[0]).b) <= 27) {
          t(paramInt1, paramInt2);
          h1.a = (short)(paramh.a + paramInt1);
          h1.b = (short)(paramh.b + paramInt2);
          if (++b > 16)
            break; 
        }  
    } else {
      for (byte b1 = 0; b1 < ag.ez; b1++) {
        short s = ag.ey[b1];
        if ((ag.ex[s]).f[0] != 3) {
          int i = c(h1, (ag.ex[s]).a[0]);
          int j = c(paramh, (ag.ex[s]).a[0]);
          if (i < j && i < 20) {
            b = 0;
            while (Q(h1.a - ((ag.ex[s]).a[0]).a) <= 27 && Q(h1.b - ((ag.ex[s]).a[0]).b) <= 27) {
              t(paramInt1, paramInt2);
              h1.a = (short)(paramh.a + paramInt1);
              h1.b = (short)(paramh.b + paramInt2);
              if (++b > 16)
                break; 
            } 
          } 
        } 
      } 
    } 
    int[] arrayOfInt;
    (arrayOfInt = new int[2])[0] = paramInt1;
    arrayOfInt[1] = paramInt2;
    return arrayOfInt;
  }
  
  final void f() {
    int i;
    if (ag.ep != 0 && (i = aB()) > -1)
      ag.cz.d[0] = ag.cz.c = a(ag.cz.a[0], (ag.ex[i]).a[0]); 
  }
  
  private int aB() {
    short s = -1;
    int i = 0;
    int j = 50;
    for (byte b = 0; b < ag.ez; b++) {
      short s1 = ag.ey[b];
      if (j > (i = c((ag.ex[s1]).a[0], ag.cz.a[0])) && (ag.ex[s1]).m > 0) {
        j = i;
        s = s1;
      } 
    } 
    return s;
  }
  
  private void Y(int paramInt) {
    byte b;
    byte[] arrayOfByte = { -2, -1, 0, 0, 0, 0, 1, 2 };
    int i;
    if ((i = c(ag.cz.a[0], (ag.ex[paramInt]).a[0])) < 90) {
      b = 1;
    } else {
      b = 0;
    } 
    (ag.ex[paramInt]).g[0] = 0;
    int j = C(1000);
    byte b1 = a((ag.ex[paramInt]).a[0]);
    switch ((ag.ex[paramInt]).h) {
      case 201:
      case 203:
        if (j < 150 + b * 300) {
          (ag.ex[paramInt]).f[0] = 0;
          (ag.ex[paramInt]).e[0] = (ag.ex[paramInt]).d = (byte)(b1 + arrayOfByte[j & 0x7] & 0x7);
          return;
        } 
        if (j < 850 - b * 100) {
          if (b != 0) {
            if (i <= 45 && ag.cz.e[0] != 9 && ag.cz.e[0] != 10 && ag.cz.e[0] < 12) {
              (ag.ex[paramInt]).f[0] = 1;
              (ag.ex[paramInt]).e[0] = (ag.ex[paramInt]).d = a((ag.ex[paramInt]).a[0], ag.cz.a[0]);
              U(paramInt);
              return;
            } 
            (ag.ex[paramInt]).f[0] = 0;
            (ag.ex[paramInt]).e[0] = (ag.ex[paramInt]).d = (byte)(b1 + arrayOfByte[j & 0x7] & 0x7);
            return;
          } 
          (ag.ex[paramInt]).f[0] = 0;
          (ag.ex[paramInt]).e[0] = (ag.ex[paramInt]).d = (byte)((ag.ex[paramInt]).e[0] + arrayOfByte[j & 0x7] & 0x7);
          return;
        } 
        (ag.ex[paramInt]).f[0] = 0;
        if (b != 0) {
          (ag.ex[paramInt]).e[0] = (ag.ex[paramInt]).d = (byte)(j & 0x7);
          return;
        } 
        (ag.ex[paramInt]).e[0] = (ag.ex[paramInt]).d = (byte)((ag.ex[paramInt]).e[0] + arrayOfByte[j & 0x7] & 0x7);
        return;
      case 202:
        (ag.ex[paramInt]).f[0] = 1;
        (ag.ex[paramInt]).s = 15;
        Z(paramInt);
        return;
    } 
    if (j < 150) {
      m(paramInt, 0);
      return;
    } 
    if (j < 350) {
      if (i <= 60 && (ag.cz.e[0] != 9 || ag.cz.f[0] >= 6) && ag.cz.e[0] != 10 && ag.cz.e[0] < 12) {
        (ag.ex[paramInt]).f[0] = 1;
        (ag.ex[paramInt]).e[0] = (ag.ex[paramInt]).d = a((ag.ex[paramInt]).a[0], ag.cz.a[0]);
        return;
      } 
    } else {
      (ag.ex[paramInt]).e[0] = (ag.ex[paramInt]).d = b1;
    } 
  }
  
  private static byte a(h paramh) {
    int i = (ag.cz.a[0]).a - paramh.a;
    int j = (ag.cz.a[0]).b - paramh.b;
    return (i > 27) ? ((j > 27) ? 7 : ((j < -27) ? 5 : 6)) : ((i < -27) ? ((j > 27) ? 1 : ((j < -27) ? 3 : 2)) : ((j > 0) ? 0 : 4));
  }
  
  private static void Z(int paramInt) {
    byte[] arrayOfByte1 = { -1, -15, -1, 5 };
    byte[] arrayOfByte2 = { -5, -13, -30, -13 };
    int i = (ag.ex[paramInt]).e[0] >> 1;
    for (byte b = 0; b < 3; b++) {
      if ((ag.eC[b]).a == 0) {
        (ag.eC[b]).a = 1;
        ((ag.eC[b]).b[1]).a = (short)(((ag.ex[paramInt]).a[0]).a + arrayOfByte1[i]);
        ((ag.eC[b]).b[1]).b = (short)(((ag.ex[paramInt]).a[0]).b + arrayOfByte2[i]);
        (ag.eC[b]).e = (byte)i;
        (ag.eC[b]).g = 0;
        (ag.eC[b]).f = (ag.ex[paramInt]).j;
        if ((i & 0x1) != 0) {
          (ag.eC[b]).c = 11;
          (ag.eC[b]).d = 2;
          return;
        } 
        (ag.eC[b]).c = 2;
        (ag.eC[b]).d = 11;
        return;
      } 
    } 
  }
  
  final void g() {
    byte[] arrayOfByte = { 20, 20, 25 };
    int i = 0;
    for (byte b = 0; b < ag.ez; b++) {
      short s1 = ag.ey[b];
      (ag.ex[s1]).f[0] = Math.min((ag.ex[s1]).f[0], ((ag.ex[s1]).B[(ag.ex[s1]).e[0]]).length - 1);
      (ag.ex[s1]).g[0] = (byte)((ag.ex[s1]).g[0] + 1);
      (ag.ex[s1]).s = (byte)((ag.ex[s1]).s - 1);
      short s2 = (ag.ex[s1]).B[(ag.ex[s1]).e[0]][(ag.ex[s1]).f[0]][(ag.ex[s1]).g[0]];
      if ((ag.ex[s1]).p > 0 && ((ag.ex[s1]).p = (short)((ag.ex[s1]).p - 1)) < 1)
        (ag.ex[s1]).n = 0; 
      if ((ag.ex[s1]).q > 0 && ((ag.ex[s1]).q = (short)((ag.ex[s1]).q - 1)) < 1)
        (ag.ex[s1]).o = 0; 
      if ((ag.ex[s1]).f[0] == 3) {
        if (s2 > 200) {
          ab(s1);
          if (ag.eA < 1 && 0 == ag.eD[0] && (ag.ex[s1]).h != 202)
            if (ag.cr != 0) {
              ag.co = 4;
              ag.cn = 22;
            } else {
              ag.co = 3;
              ag.cn = 5;
            }  
        } 
      } else {
        if (s2 > 200) {
          if ((ag.ex[s1]).m < 1) {
            (ag.ex[s1]).f[0] = 3;
          } else {
            (ag.ex[s1]).f[0] = 0;
          } 
          (ag.ex[s1]).g[0] = 0;
          if ((ag.ex[s1]).h < 200) {
            ag.fb = null;
            ag.fa = null;
          } 
        } 
        if ((ag.ex[s1]).s < 1) {
          (ag.ex[s1]).r = 1;
          (ag.ex[s1]).s = 6;
          if ((ag.ex[s1]).f[0] == 0)
            Y(s1); 
        } 
        if ((ag.ex[s1]).h != 202) {
          int j = (ag.ex[s1]).d;
          if ((ag.ex[s1]).r != 0) {
            int m = 0;
            int k = m;
            switch ((ag.ex[s1]).f[0]) {
              case 0:
                k = ae.aw[j];
                m = ae.ax[j];
                break;
              case 1:
              case 4:
              case 5:
                k = ae.aw[(ag.ex[s1]).e[0]] / 3;
                m = ae.ax[(ag.ex[s1]).e[0]] / 3;
                break;
              case 6:
                if ((ag.ex[s1]).g[0] > 2 && (ag.ex[s1]).g[0] < 6) {
                  k = ae.aw[(ag.ex[s1]).e[0]] << 2;
                  m = ae.ax[(ag.ex[s1]).e[0]] << 2;
                } 
                break;
              case 7:
                if ((ag.ex[s1]).g[0] > 4 && (ag.ex[s1]).g[0] < 8) {
                  k = ae.aw[(ag.ex[s1]).e[0]] << 2;
                  m = ae.ax[(ag.ex[s1]).e[0]] << 2;
                  if (k > 0) {
                    k = a((ag.ex[s1]).a[0], k, 6);
                  } else if (k < 0) {
                    k = a((ag.ex[s1]).a[0], k, 2);
                  } 
                  if (m > 0) {
                    m = a((ag.ex[s1]).a[0], m, 0);
                  } else if (m < 0) {
                    m = a((ag.ex[s1]).a[0], m, 4);
                  } 
                  int[] arrayOfInt;
                  k = (arrayOfInt = b((ag.ex[s1]).a[0], k, m))[0];
                  m = arrayOfInt[1];
                  ((ag.ex[s1]).a[0]).a = (short)(((ag.ex[s1]).a[0]).a + k);
                  ((ag.ex[s1]).a[0]).b = (short)(((ag.ex[s1]).a[0]).b + m);
                } else {
                  break;
                } 
              case 8:
                if ((ag.ex[s1]).g[0] > 0 && (ag.ex[s1]).g[0] < 9) {
                  k = ae.aw[(ag.ex[s1]).e[0]];
                  m = ae.ax[(ag.ex[s1]).e[0]];
                } 
                break;
              case 14:
                if (0 == ((ag.ex[s1]).g[0] & 0x1)) {
                  k = ae.aw[(ag.ex[s1]).e[0]];
                  m = ae.ax[(ag.ex[s1]).e[0]];
                } 
                break;
              case 2:
                if ((ag.ex[s1]).A > 0) {
                  (ag.ex[s1]).A = (byte)((ag.ex[s1]).A - 1);
                  j = j + 4 & 0x7;
                  k = ae.aw[j] << 2;
                  m = ae.ax[j] << 2;
                  break;
                } 
                if ((ag.ex[s1]).g[0] == 1) {
                  j = (ag.ex[s1]).d + 4 & 0x7;
                  k = ae.aw[j] * 3 / 4;
                  m = ae.ax[j] * 3 / 4;
                  break;
                } 
              default:
                k = m = 0;
                break;
            } 
            if (k != 0 || m != 0) {
              if ((ag.ex[s1]).h == 203) {
                h[] arrayOfH = (ag.ex[s1]).a;
                switch (j) {
                  case 3:
                    (arrayOfH[0]).a = (short)((arrayOfH[0]).a - 10);
                    (arrayOfH[1]).a = (short)((arrayOfH[1]).a - 10);
                    break;
                  case 1:
                    (arrayOfH[0]).a = (short)((arrayOfH[0]).a - 10);
                    (arrayOfH[1]).a = (short)((arrayOfH[1]).a - 10);
                    (arrayOfH[0]).b = (short)((arrayOfH[0]).b + 10);
                    (arrayOfH[1]).b = (short)((arrayOfH[1]).b + 10);
                    break;
                  case 2:
                    (arrayOfH[0]).a = (short)((arrayOfH[0]).a - 10);
                    (arrayOfH[1]).a = (short)((arrayOfH[1]).a - 10);
                    break;
                  case 0:
                    (arrayOfH[0]).b = (short)((arrayOfH[0]).b + 10);
                    (arrayOfH[1]).b = (short)((arrayOfH[1]).b + 10);
                    break;
                  case 5:
                    (arrayOfH[0]).a = (short)((arrayOfH[0]).a + 10);
                    (arrayOfH[1]).a = (short)((arrayOfH[1]).a + 10);
                    break;
                  case 7:
                    (arrayOfH[0]).a = (short)((arrayOfH[0]).a + 10);
                    (arrayOfH[1]).a = (short)((arrayOfH[1]).a + 10);
                    (arrayOfH[0]).b = (short)((arrayOfH[0]).b + 10);
                    (arrayOfH[1]).b = (short)((arrayOfH[1]).b + 10);
                    break;
                  case 6:
                    (arrayOfH[0]).a = (short)((arrayOfH[0]).a + 10);
                    (arrayOfH[1]).a = (short)((arrayOfH[1]).a + 10);
                    break;
                } 
                i = a(arrayOfH[0], k, m, j, s1);
                switch (j) {
                  case 3:
                    (arrayOfH[0]).a = (short)((arrayOfH[0]).a + 10);
                    (arrayOfH[1]).a = (short)((arrayOfH[1]).a + 10);
                    break;
                  case 1:
                    (arrayOfH[0]).a = (short)((arrayOfH[0]).a + 10);
                    (arrayOfH[1]).a = (short)((arrayOfH[1]).a + 10);
                    (arrayOfH[0]).b = (short)((arrayOfH[0]).b - 10);
                    (arrayOfH[1]).b = (short)((arrayOfH[1]).b - 10);
                    break;
                  case 2:
                    (arrayOfH[0]).a = (short)((arrayOfH[0]).a + 10);
                    (arrayOfH[1]).a = (short)((arrayOfH[1]).a + 10);
                    break;
                  case 0:
                    (arrayOfH[0]).b = (short)((arrayOfH[0]).b - 10);
                    (arrayOfH[1]).b = (short)((arrayOfH[1]).b - 10);
                    break;
                  case 5:
                    (arrayOfH[0]).a = (short)((arrayOfH[0]).a - 10);
                    (arrayOfH[1]).a = (short)((arrayOfH[1]).a - 10);
                    break;
                  case 7:
                    (arrayOfH[0]).a = (short)((arrayOfH[0]).a - 10);
                    (arrayOfH[1]).a = (short)((arrayOfH[1]).a - 10);
                    (arrayOfH[0]).b = (short)((arrayOfH[0]).b - 10);
                    (arrayOfH[1]).b = (short)((arrayOfH[1]).b - 10);
                    break;
                  case 6:
                    (arrayOfH[0]).a = (short)((arrayOfH[0]).a - 10);
                    (arrayOfH[1]).a = (short)((arrayOfH[1]).a - 10);
                    break;
                } 
              } else {
                i = a((ag.ex[s1]).a[0], k, m, j, s1);
              } 
              switch ((ag.ex[s1]).f[0]) {
                case 0:
                  switch (j) {
                    case 0:
                    case 2:
                    case 4:
                    case 6:
                      if (i == -1 && (i = c((ag.ex[s1]).a[0], (ag.ex[s1]).d, s1)) != -1)
                        a((ag.ex[s1]).a[0], ae.aw[i], ae.ax[i], i, s1); 
                      break;
                  } 
                  break;
              } 
            } 
            switch ((ag.ex[s1]).f[0]) {
              case 1:
              case 4:
              case 5:
                if ((ag.ex[s1]).g[0] == 1)
                  aa(s1); 
                break;
              case 6:
                if ((ag.ex[s1]).g[0] > 2 && (ag.ex[s1]).g[0] < 6)
                  aa(s1); 
                break;
              case 7:
                if ((ag.ex[s1]).g[0] > 4 && (ag.ex[s1]).g[0] < 8)
                  aa(s1); 
                break;
              case 8:
                switch ((ag.ex[s1]).g[0]) {
                  case 2:
                  case 4:
                  case 6:
                  case 8:
                    aa(s1);
                    break;
                } 
                break;
              case 9:
              case 10:
                if ((ag.ex[s1]).g[0] == 11) {
                  (ag.ex[s1]).m = (short)((ag.ex[s1]).m + (ag.ex[s1]).l * (((ag.ex[s1]).f[0] == 9) ? 20 : 50) / 100);
                  if ((ag.ex[s1]).m > (ag.ex[s1]).l)
                    (ag.ex[s1]).m = (ag.ex[s1]).l; 
                } 
                break;
              case 11:
              case 12:
              case 13:
                if ((ag.ex[s1]).g[0] == 11) {
                  if ((ag.ex[s1]).f[0] != 12) {
                    (ag.ex[s1]).n = (short)((ag.ex[s1]).j / arrayOfByte[(ag.ex[s1]).f[0] - 11]);
                    if ((ag.ex[s1]).n < 1)
                      (ag.ex[s1]).n = 1; 
                    (ag.ex[s1]).p = 50;
                  } 
                  if ((ag.ex[s1]).f[0] != 11) {
                    (ag.ex[s1]).o = (short)((ag.ex[s1]).k / arrayOfByte[(ag.ex[s1]).f[0] - 11]);
                    if ((ag.ex[s1]).o < 1)
                      (ag.ex[s1]).o = 1; 
                    (ag.ex[s1]).q = 50;
                  } 
                } 
                break;
              case 14:
                if (((ag.ex[s1]).g[0] & 0x1) != 0)
                  aa(s1); 
                break;
              case 15:
                if ((ag.ex[s1]).g[0] == 5)
                  aa(s1); 
                break;
              case 16:
                if ((ag.ex[s1]).g[0] == 6)
                  aa(s1); 
                break;
              case 17:
              case 18:
                if ((ag.ex[s1]).g[0] == 5)
                  aa(s1); 
                break;
              case 19:
                if (((ag.ex[s1]).g[0] & 0x1) != 0)
                  aa(s1); 
                break;
              case 20:
              case 21:
                if ((ag.ex[s1]).g[0] == 8)
                  aa(s1); 
                break;
            } 
          } else {
            ((ag.ex[s1]).a[0]).a = (short)(((ag.ex[s1]).a[0]).a + ae.aw[j]);
            ((ag.ex[s1]).a[0]).b = (short)(((ag.ex[s1]).a[0]).b + ae.ax[j]);
          } 
        } else {
          (ag.ex[s1]).e[0] = (ag.ex[s1]).d = a((ag.ex[s1]).a[0], ag.cz.a[0]);
        } 
      } 
    } 
  }
  
  private void aa(int paramInt) {
    h h = new h();
    if (ag.cz.e[0] != 9 && ag.cz.e[0] != 10) {
      if (ag.cz.e[0] < 12) {
        switch ((ag.ex[paramInt]).f[0]) {
          case 7:
            if (a(((ag.ex[paramInt]).a[0]).a + ae.aF[(ag.ex[paramInt]).e[0] >> 1], ((ag.ex[paramInt]).a[0]).b + ae.aG[(ag.ex[paramInt]).e[0] >> 1], ae.aH[(ag.ex[paramInt]).e[0] >> 1], ae.aI[(ag.ex[paramInt]).e[0] >> 1], (ag.cz.a[0]).a - 8, (ag.cz.a[0]).b - 8, 17, 17)) {
              U(paramInt);
              return;
            } 
            return;
          case 16:
            if (a((ag.ex[paramInt]).a[0], ag.cz.a[0], (ag.ex[paramInt]).e[0]) != 0) {
              r(paramInt, ae.aL[ag.dC.c]);
              return;
            } 
            return;
          case 17:
          case 18:
            r(paramInt, 45);
            return;
          case 19:
            if (((ag.ex[paramInt]).e[0] + ((ag.ex[paramInt]).g[0] >> 1 << 1) & 0x7) == a((ag.ex[paramInt]).a[0], ag.cz.a[0])) {
              r(paramInt, ae.aL[ag.dC.c]);
              return;
            } 
            return;
          case 20:
          case 21:
            h.a = (short)(((ag.ex[paramInt]).a[0]).a + ae.aA[(ag.ex[paramInt]).e[0] >> 1]);
            h.b = (short)(((ag.ex[paramInt]).a[0]).b + ae.aB[(ag.ex[paramInt]).e[0] >> 1]);
            if (c(h, ag.cz.a[0]) <= 35) {
              T(paramInt);
              return;
            } 
            return;
        } 
        o(paramInt, ae.aL[ag.dC.c]);
        return;
      } 
    } else if (ag.cz.e[0] == 9) {
      switch ((ag.ex[paramInt]).f[0]) {
        case 8:
        case 14:
          o(paramInt, ae.aL[ag.dC.c]);
          return;
        case 20:
        case 21:
          h.a = (short)(((ag.ex[paramInt]).a[0]).a + ae.aA[ag.cz.d[0] >> 1]);
          h.b = (short)(((ag.ex[paramInt]).a[0]).b + ae.aB[ag.cz.d[0] >> 1]);
          if (c(h, ag.cz.a[0]) <= 35)
            T(paramInt); 
          break;
      } 
    } 
  }
  
  private void ab(int paramInt) {
    for (byte b = 0; b < ag.ez; b++) {
      if (ag.ey[b] == paramInt) {
        if ((ag.ex[paramInt]).h < 200) {
          if (ag.cr != 0) {
            b1 = 2;
          } else {
            b1 = 1;
          } 
          ag.dY += (ag.ex[paramInt]).i << 1;
          if (ag.dC.c != ag.cz.K)
            ag.ct[40 + ag.dC.c] = null; 
          ag.er[1] = null;
          for (byte b2 = 3; b2 < 9; b2++)
            ag.et[b2] = null; 
          ag.eB = 0;
        } else {
          b1 = 0;
          ag.dY += (ag.ex[paramInt]).i;
        } 
        a(b1, (ag.ex[paramInt]).a[0]);
        if ((ag.ex[paramInt]).h == 203) {
          ag.cz.H += 3;
        } else {
          ag.cz.H++;
        } 
        for (byte b1 = b; b1 < 6; b1++)
          ag.ey[b1] = ag.ey[b1 + 1]; 
        (ag.ex[paramInt]).c = 0;
        ag.ez = (short)(ag.ez - 1);
        if ((ag.ex[paramInt]).h != 202)
          ag.eA = (short)(ag.eA - 1); 
        return;
      } 
    } 
  }
  
  static void h() {
    if (ag.ez != 0)
      for (byte b = 0; b < ag.ez - 1; b++) {
        for (int i = b + 1; i < ag.ez; i++) {
          if (((ag.ex[ag.ey[b]]).a[0]).b > ((ag.ex[ag.ey[i]]).a[0]).b) {
            short s = ag.ey[b];
            ag.ey[b] = ag.ey[i];
            ag.ey[i] = s;
          } 
        } 
      }  
  }
  
  final void i() {
    for (byte b = 0; b < ag.cD; b++) {
      if ((ag.cC[b]).a != 0) {
        if (c(ag.cz.a[0], (ag.cC[b]).b) < 20 && k((ag.cC[b]).a, 1) != 0) {
          ag.ek = 1;
          if ((ag.cC[b]).a > 100 && (ag.cC[b]).a < 10000) {
            ag.bb.e((ag.cC[b]).a);
            ag.cS.e(13);
          } 
          (ag.cC[b]).a = 0;
        } 
        (ag.cC[b]).c = (short)((ag.cC[b]).c - 1);
        if ((ag.cC[b]).c < 1)
          (ag.cC[b]).a = 0; 
      } 
    } 
  }
  
  final void j() {
    for (byte b = 0; b < 3; b++) {
      if ((ag.eC[b]).a != 0) {
        ((ag.eC[b]).b[1]).a = ((ag.eC[b]).b[0]).a;
        ((ag.eC[b]).b[1]).b = ((ag.eC[b]).b[0]).b;
        if (a(((ag.eC[b]).b[0]).a, ((ag.eC[b]).b[0]).b + 8, (ag.eC[b]).c, (ag.eC[b]).d, (ag.cz.a[0]).a - 12, (ag.cz.a[0]).b - 20, 17, 18)) {
          if (ag.cz.e[0] < 12) {
            ag.bd.d();
            (ag.eC[b]).a = 0;
            U(b - 3);
          } else {
            ac(b);
          } 
        } else {
          ac(b);
        } 
      } 
    } 
  }
  
  private void ac(int paramInt) {
    switch (ag.cz.e[1]) {
      case 26:
      case 27:
        if (ag.cz.f[1] > 1 && ag.cz.f[1] < 9)
          return; 
        break;
      case 28:
        if (ag.cz.f[1] > 3)
          return; 
        break;
      case 29:
        if (ag.cz.f[1] > 6)
          return; 
        break;
      case 30:
        if (ag.cz.f[1] > 3 && ag.cz.f[1] < 15)
          return; 
        break;
    } 
    ad(paramInt);
  }
  
  private static void ad(int paramInt) {
    if (((ag.eC[paramInt]).g = (byte)((ag.eC[paramInt]).g + 1)) > 22) {
      (ag.eC[paramInt]).a = 0;
      return;
    } 
    switch ((ag.eC[paramInt]).e) {
      case 0:
        ((ag.eC[paramInt]).b[0]).b = (short)(((ag.eC[paramInt]).b[0]).b + 12);
        return;
      case 1:
        ((ag.eC[paramInt]).b[0]).a = (short)(((ag.eC[paramInt]).b[0]).a - 12);
        return;
      case 2:
        ((ag.eC[paramInt]).b[0]).b = (short)(((ag.eC[paramInt]).b[0]).b - 12);
        return;
      case 3:
        ((ag.eC[paramInt]).b[0]).a = (short)(((ag.eC[paramInt]).b[0]).a + 12);
        break;
    } 
  }
  
  private void aC() {
    ag.cz.a[1] = ag.cz.a[0];
    ag.cz.b[1] = ag.cz.b[0];
    ag.cz.d[1] = ag.cz.d[0];
    ag.cz.d[0] = ag.cz.c;
    ag.cz.e[1] = ag.cz.e[0];
    ag.cz.f[1] = ag.cz.f[0];
    ag.cz.N++;
    ag.ek = 0;
    if (ag.cz.C > 0) {
      if (--ag.cz.C < 1)
        ag.cz.A = 0; 
      ag.ek = 1;
    } 
    if (ag.cz.D > 0) {
      if (--ag.cz.D < 1)
        ag.cz.B = 0; 
      ag.ek = 1;
    } 
    ag.cs[4] = ag.cs[3];
    ag.cs[3] = ag.cs[2];
    ag.cs[2] = ag.cs[1];
    ag.cs[1] = ag.cs[0];
    ag.cs[0] = -1;
    ag.cl = 0;
    ag.fh = 0;
    if (ag.fd != null) {
      ag.ff = (short)(ag.ff - 1);
      if (ag.ff < 0) {
        ag.fe = null;
        ag.fd = null;
      } 
    } 
    byte b;
    for (b = 0; b < ag.ez; b++) {
      short s = ag.ey[b];
      (ag.ex[s]).a[1] = (ag.ex[s]).a[0];
      (ag.ex[s]).e[1] = (ag.ex[s]).e[0];
      (ag.ex[s]).f[1] = (ag.ex[s]).f[0];
      (ag.ex[s]).g[1] = (ag.ex[s]).g[0];
    } 
    if (ag.cz.e[0] == 28 || ag.cz.e[0] == 29 || ag.cz.e[0] == 30) {
      if (ag.co != 0)
        ag.cn = 0; 
      return;
    } 
    if (ag.co != 0) {
      if (ag.cn < 1) {
        switch (ag.co) {
          case 1:
            if (ag.cp != 0) {
              ag.bV = 4;
              ag.co = 0;
              ag.cm = 1;
            } 
            if (0 == ag.cn) {
              ag.cm = 2;
              for (b = 0; b < 4; b++) {
                if ((ag.eO[ag.eP]).a[b] != 0)
                  ag.ct[21 + b] = d(ag.bA.a(17 + b)); 
              } 
              ag.cn = (short)(ag.cn - 1);
              return;
            } 
            break;
          case 2:
            ag.cS.e(8);
            ag.co = 0;
            return;
          case 3:
            ag.cS.e(9);
            ag.co = 0;
            return;
          case 4:
            ag.cS.e(10);
            ag.co = 0;
            break;
        } 
        return;
      } 
      ag.cn = (short)(ag.cn - 1);
      if (ag.co == 3 && ag.cn == 0 && ag.bg != null)
        ag.ai(); 
    } 
  }
  
  final void O(int paramInt) {
    ag.dW[0] = ag.B();
    if (paramInt == 0 || ag.dW[0] - ag.dW[1] > 1000L) {
      ag.dV += ag.dW[0] - ag.dW[1];
    } else {
      long l;
      ag.dX = (int)((l = ag.dW[0] - ag.dV) / 1000L);
    } 
    ag.dW[1] = ag.dW[0];
  }
  
  final void k() {
    switch (ag.cp) {
      case 1:
        ag.ce += 7;
        ag.cm = (short)(ag.cm + 6);
        ag.bd.a(ag.cb.a, ag.cb.b, ag.cd, ag.ce, 0);
        break;
      case 2:
        ag.cd -= 7;
        ag.cm = (short)(ag.cm + 6);
        ag.bd.a(ag.cb.a, ag.cb.b, ag.cd, ag.ce, 0);
        break;
      case 3:
        ag.ce -= 7;
        ag.cm = (short)(ag.cm + 6);
        ag.bd.a(ag.cb.a, ag.cb.b, ag.cd, ag.ce, 0);
        break;
      case 4:
        ag.cd += 7;
        ag.cm = (short)(ag.cm + 6);
        ag.bd.a(ag.cb.a, ag.cb.b, ag.cd, ag.ce, 0);
        break;
    } 
    a(ag.ct[7], ag.db, ag.dc, ag.bY.a, ag.bY.b, ag.cc.a, ag.cc.b);
    int[] arrayOfInt = b(ag.cz.a[0], 0, 0);
    (ag.cz.a[0]).a = (short)((ag.cz.a[0]).a + arrayOfInt[0]);
    (ag.cz.a[0]).b = (short)((ag.cz.a[0]).b + arrayOfInt[1]);
    ag.bd.e();
    if (ag.cm > 1)
      a_(-1); 
    if (ag.cm > 6) {
      ag.bV = 3;
      ag.ck = 1;
      ag.cp = 0;
      ag.do = (short)(ag.do + 1);
      ag.co = 2;
      ag.cn = 1;
      A();
    } 
    ag.cm = (short)(ag.cm + 1);
  }
  
  final void a(int paramInt1, int paramInt2, int paramInt3) {
    b(ag.ct[43], paramInt2 - (ag.eV[paramInt1]).e, paramInt3 - (ag.eV[paramInt1]).f, (ag.eV[paramInt1]).c, (ag.eV[paramInt1]).d, (ag.eV[paramInt1]).a, (ag.eV[paramInt1]).b);
  }
  
  final void a(int paramInt1, int paramInt2, y paramy) {
    b(ag.ct[40 + ag.cz.K], paramInt1 - paramy.e, paramInt2 - paramy.f, paramy.c, paramy.d, paramy.a, paramy.b);
    c.a((ag.cz.a[0]).a - paramy.e, (ag.cz.a[0]).b - paramy.f, paramy.c, paramy.d);
  }
  
  final void a(int paramInt1, int paramInt2) {
    h h;
    int i;
    if (paramInt1 > -1) {
      h = (ag.ex[paramInt1]).a[0];
      if ((ag.ex[paramInt1]).f[0] == 19) {
        i = (ag.ex[paramInt1]).e[0] + ((ag.ex[paramInt1]).g[0] >> 1 << 1) & 0x7;
      } else {
        i = (ag.ex[paramInt1]).e[0];
      } 
    } else {
      h = ag.cz.a[0];
      if (ag.cz.e[0] == 25) {
        i = ag.cz.d[0] + (ag.cz.f[0] >> 1 << 1) & 0x7;
      } else {
        i = ag.cz.d[0];
      } 
    } 
    int j = (i >> 1) * 6 + (paramInt2 << 1);
    int k = h.a - ag.ca.a;
    int m = h.b - ag.ca.b;
    for (byte b = 0; b < 2; b++) {
      b(ag.ct[42], k - (ag.eU[j]).e, m - (ag.eU[j]).f, (ag.eU[j]).c, (ag.eU[j]).d, (ag.eU[j]).a, (ag.eU[j]).b);
      c.a(h.a - (ag.eU[j]).e, h.b - (ag.eU[j]).f, (ag.eU[j]).c, (ag.eU[j]).d);
      j++;
    } 
  }
  
  final void l() {
    for (byte b = 0; b < ag.cb.a; b++) {
      for (byte b1 = 0; b1 < ag.cb.b; b1++) {
        if (ag.eE[b1][b] != 0) {
          int i = (ag.ce + b1) * ag.cE.b.a + ag.cd + b;
          if (ag.cE.a[ag.cE.e + i] != 0) {
            int j = ag.cJ[ag.cE.a[ag.cE.e + i] - 1] - 1;
            b(ag.bT[j], (ag.cd + b) * 27 - ag.ca.a, (ag.ce + b1) * 27 - ag.ca.b, 27, 27, 0, 0);
          } 
        } 
      } 
    } 
  }
  
  final void m() {
    byte b;
    for (b = 0; b < ag.cD; b++) {
      if ((ag.cC[b]).a != 0) {
        b((ag.cC[b]).g, (ag.cC[b]).b.a - ag.ca.a - ((ag.cC[b]).e >> 1), (ag.cC[b]).b.b - ag.ca.b - ((ag.cC[b]).f >> 1), (ag.cC[b]).e, (ag.cC[b]).f, (ag.cC[b]).e * (ag.cC[b]).d, 0);
        c.a((ag.cC[b]).b.a - ((ag.cC[b]).e >> 1), (ag.cC[b]).b.b - ((ag.cC[b]).f >> 1), (ag.cC[b]).e, (ag.cC[b]).f);
      } 
    } 
    for (b = 0; b < ag.cB; b++) {
      if ((ag.cA[b]).a != 0 && (ag.cA[b]).e != 0) {
        (ag.cA[b]).e = (short)((ag.cA[b]).e - 1);
        if (((ag.cA[b]).e & 0x2) != 0) {
          b(ag.bT[(ag.cA[b]).f], (ag.cA[b]).c.a * 27 - ag.ca.a, (ag.cA[b]).c.b * 27 - ag.ca.b, 27, 27, 0, 0);
        } else {
          int i = (ag.cA[b]).c.a * 27 - ag.ca.a;
          int j = (ag.cA[b]).c.b * 27 - ag.ca.b;
          if (ag.ct[7] != null && i + ag.cc.a >= 0) {
            if (i + ag.cc.a > ag.ct[7].getWidth())
              return; 
            b(ag.ct[7], i, j, 27, 27, i + ag.cc.a, j + ag.cc.b);
          } else {
            break;
          } 
        } 
        if (0 == (ag.cA[b]).e) {
          a(3, (ag.cA[b]).b);
          (ag.cA[b]).a = 0;
        } 
      } 
    } 
  }
  
  private void a(int paramInt, h paramh) {
    short s1 = paramh.a;
    short s2;
    if ((s2 = paramh.b) <= ag.ca.b + 27 || s2 >= ag.ca.b + 162 || s1 <= ag.ca.a + 27 || s1 >= ag.ca.a + 162)
      return; 
    short s3;
    if ((s3 = P(paramInt)) != 0) {
      int i = s2 / 27 * ag.cE.b.a + s1 / 27;
      if (0 == (ag.cE.a[ag.cE.f + i] & 0x1)) {
        byte b;
        for (b = 0; b < 10 && (ag.cC[b]).a != 0; b++);
        if (b > 9)
          return; 
        (ag.cC[b]).a = s3;
        if ((ag.cC[b]).b == null)
          (ag.cC[b]).b = new h(); 
        (ag.cC[b]).b.a = s1;
        (ag.cC[b]).b.b = s2;
        (ag.cC[b]).c = 75;
        (ag.cC[b]).e = (ag.cC[b]).f = 28;
        if (s3 > 10000) {
          (ag.cC[b]).g = ag.ct[32];
          (ag.cC[b]).d = 0;
          (ag.cC[b]).e = (short)ag.ct[32].getWidth();
          (ag.cC[b]).f = (short)ag.ct[32].getHeight();
        } else if (s3 > 100) {
          (ag.cC[b]).g = ag.ct[0];
          (ag.cC[b]).d = 11;
        } else {
          (ag.cC[b]).g = ag.ct[0];
          (ag.cC[b]).d = (short)(s3 - 1);
        } 
        if (b >= ag.cD)
          ag.cD = (short)(ag.cD + 1); 
      } 
    } 
  }
  
  final short P(int paramInt) {
    byte[] arrayOfByte1 = { 5, 10, 20, 5, 100 };
    byte[] arrayOfByte2 = { 10, 30, 60, 1, 100 };
    byte[] arrayOfByte3 = { 69, 44, 24, 9, 0 };
    byte[][] arrayOfByte = { { 0, 0, 33, 77, 100 }, { 5, 30, 55, 80, 100 }, { 30, 60, 90, 100, 100 }, { 40, 80, 100, 100, 100 }, { 80, 100, 100, 100, 100 } };
    if (C(100) < arrayOfByte1[paramInt]) {
      int i;
      if ((i = C(100)) < arrayOfByte2[paramInt]) {
        for (byte b = 0; b < 5; b++) {
          if (ag.cz.l > arrayOfByte3[b]) {
            i = C(100);
            for (byte b1 = 0; b1 < 5; b1++) {
              if (i < arrayOfByte[b][b1])
                return (short)(101 + b1 + 5 * C(20)); 
            } 
          } 
        } 
      } else {
        return (short)(C(11) + 1);
      } 
    } else if (C(100) < 25) {
      return (short)(10020 + (ag.ep ^ 0x1) * 20);
    } 
    return 0;
  }
  
  private void aD() {
    for (byte b = 0; b < 2; b++) {
      if ((ag.cz.Z[ag.cz.aa[b]]).a != 0) {
        ag.a(ag.dd + (2 * b - 1) * (44 + 28 * (1 - b) + 0), ag.bZ.b - 33 - 0 - 17, 28, 28, ag.ct[0], ((ag.cz.Z[ag.cz.aa[b]]).a - 1) * 28, 0);
        ag.a(ag.dd + (2 * b - 1) * (38 + 11 * (1 - b) + 0), ag.bZ.b - 16 - 0 - 17, 11, 12, ag.ct[20], 98, 0);
        h((ag.cz.Z[ag.cz.aa[b]]).b, ag.dd + (2 * b - 1) * (28 + 10 * b + 0), ag.bZ.b - 18 - 0 - 17);
      } 
    } 
  }
  
  final void n() {
    ag.bd.a();
    if (ag.dT.a != 0) {
      aE();
    } else {
      h(ag.cz.I, ag.bY.a - 4 - 7, 20);
    } 
    aD();
    j(0, 5, ag.dX);
    if (ag.bV == 3 && ag.cS.b == 0) {
      if (ag.cR.a != 0) {
        ag.h(-1, 9);
        return;
      } 
      ag.h(-1, 1);
    } 
  }
  
  private void aE() {
    ag.dD = ag.c(ag.dT.c);
    int i = ag.bY.a - ag.bu.a(ag.dT.c.toCharArray(), 0, ag.dT.c.length()) - 8;
    x.a(ag.bv);
    ag.d(ag.dT.c, i, 3);
    ag.d(ag.dT.c, i - 1, 2);
    ag.d(ag.dT.c, i + 1, 2);
    ag.d(ag.dT.c, i, 1);
    x.a(ag.bu);
    ag.d(ag.dT.c, i, 2);
    ag.dD = ag.s(ag.dT.d);
    b(ag.ct[31], ag.bY.a - ag.ct[31].getWidth() - 27 - 5 - 7, 2 + ag.bu.a(), ag.ct[31].getWidth(), ag.ct[31].getHeight(), 0, 0);
    a(ag.dT.d, ag.bY.a - 15, 1 + ag.bu.a() + 17, 9, 12, ag.ct[20], 0, 0, -1);
    if (ag.dT.e > 0) {
      ac ac;
      ag.a(ac = new ac(ag.bY.a - 62 + ag.db - 7, 2 + ag.bu.a() + 12 + ag.dc, (ag.dT.e > 62) ? 62 : ag.dT.e, 7), ag.k(0, 0, 0));
      ac.b++;
      ac.d = 5;
      ac.a++;
      ac.c -= 2;
      ag.a(ac, ag.k(107, 0, 0));
      ac.b++;
      ac.d = 3;
      ag.a(ac, ag.k(181, 0, 0));
      ac.b++;
      ac.d = 1;
      ag.a(ac, ag.k(255, 73, 0));
    } 
    c.a(ag.ca.a + 170, ag.ca.b, 68, 40);
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\ar.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */