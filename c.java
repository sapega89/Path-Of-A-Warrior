import javax.microedition.lcdui.Image;

public final class c extends ag {
  public c() {
    super(ag.bs);
  }
  
  final void a() {
    int[] arrayOfInt = { 35 * ag.cz.p / ag.cz.y, 35 * ag.cz.r / ag.cz.z };
    int[][] arrayOfInt1 = { { 4, ag.bZ.b - 61 }, { 201, ag.bZ.b - 61 } };
    if (ag.gk == null)
      ag.gk = d("ball_black"); 
    for (byte b = 0; b < 2; b++) {
      if (arrayOfInt[b] != 0)
        arrayOfInt[b] = (arrayOfInt[b] < 3) ? 3 : arrayOfInt[b]; 
      ag.a(arrayOfInt1[b][0], arrayOfInt1[b][1], ag.gk.getWidth(), ag.gk.getHeight() - arrayOfInt[b], ag.gk, 0, 0);
    } 
  }
  
  static void a(int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    int j = paramInt1 / 27 - ag.cd;
    int k = paramInt2 / 27 - ag.ce;
    int m = (paramInt1 + paramInt3 - 1) / 27 - ag.cd;
    int n = (paramInt2 + paramInt4 - 1) / 27 - ag.ce;
    if (j < 0)
      j = 0; 
    if (k < 0)
      k = 0; 
    if (m > ag.cb.a - 1)
      m = ag.cb.a - 1; 
    if (n > ag.cb.b - 1)
      n = ag.cb.b - 1; 
    for (int i = j; i <= m; i++) {
      for (int i1 = k; i1 <= n; i1++)
        ag.eE[i1][i] = 1; 
    } 
  }
  
  final void b() {
    ag.a(0, 0, ag.cx[1].getWidth(), ag.cx[1].getHeight(), ag.cx[1], 0, 0);
    ag.a(ag.bZ.a - ag.cx[1].getWidth(), 0, ag.cx[1].getWidth(), ag.cx[1].getHeight(), ag.cx[1], 0, 0);
    ag.a(0, 2, 120, 25, ag.cx[3], 0, 0);
    ag.a(ag.bZ.a - 120, 2, 120, 25, ag.cx[4], 1, 0);
    ag.a(ag.bZ.a / 2 - 120, ag.bZ.b - 61, 120, 61, ag.cx[0], 0, 0);
    ag.a(ag.bZ.a / 2, ag.bZ.b - 61, 120, 61, ag.cx[2], 0, 0);
  }
  
  final void c() {
    if (0 == ag.cl)
      ag.bc.l(); 
    for (byte b = 0; b < 81; b++)
      ag.eE[b / 9][b % 9] = 0; 
    if (0 == ag.cl)
      ag.bc.m(); 
    e();
    m();
    if (0 == ag.cl)
      l(); 
    k();
    b();
    ag.bc.n();
    if (ag.co == 1)
      j(); 
  }
  
  private void j() {
    int[] arrayOfInt1 = { ag.dd - 9, 5, ag.dd - 9, ag.bY.a - 31 };
    int[] arrayOfInt2 = { ag.bY.b - 31, ag.de - 13, 5, ag.de - 13 };
    if (ag.cn < 1) {
      ag.cm = (short)(ag.cm + 1);
      if ((ag.cm & 0x2) != 0)
        for (byte b = 0; b < 4; b++) {
          if ((ag.eO[ag.eP]).a[b] != 0 && ag.ct[21 + b] != null) {
            b(ag.ct[21 + b], arrayOfInt1[b], arrayOfInt2[b], ag.ct[21 + b].getWidth(), ag.ct[21 + b].getHeight(), 0, 0);
            a(ag.ca.a + arrayOfInt1[b], ag.ca.b + arrayOfInt2[b], ag.ct[21 + b].getWidth(), ag.ct[21 + b].getHeight());
          } 
        }  
    } 
  }
  
  private void k() {
    ac ac = new ac(0, 0, 0, 0);
    for (byte b = 0; b < 3; b++) {
      if ((ag.eC[b]).a != 0) {
        ac.a = (short)(((ag.eC[b]).b[0]).a - ag.ca.a + ag.db);
        ac.b = (short)(((ag.eC[b]).b[0]).b - ag.ca.b + ag.dc) - 8;
        ac.c = (ag.eC[b]).c;
        ac.d = (ag.eC[b]).d;
        ag.a(ac, ag.k(245, 206, 116));
        ac.c--;
        ac.d--;
        ag.a(ac, ag.k(240, 142, 53));
        ac.c++;
        ac.d++;
        a(((ag.eC[b]).b[0]).a, ((ag.eC[b]).b[0]).b, (ag.eC[b]).c, (ag.eC[b]).d);
        boolean bool = false;
        if (ac.a < ag.db) {
          ac.c = ag.db - ac.a;
          if (ac.c > 0)
            bool = true; 
        } 
        if (ac.b < ag.dc) {
          ac.d = ag.dc - ac.b;
          if (ac.d > 0)
            bool = true; 
        } 
        if (ac.a + ac.c >= ag.bY.a + ag.db) {
          ac.a = ag.bY.a + ag.db;
          ac.c = ag.db;
          bool = true;
        } 
        if (ac.b + ac.d >= ag.bY.b + ag.dc) {
          ac.b = ag.bY.b + ag.dc;
          ac.d = ag.dc;
          bool = true;
        } 
        if (bool) {
          ag.a(ac, 0);
          a(((ag.eC[b]).b[0]).a, ((ag.eC[b]).b[0]).b, (ag.eC[b]).c, (ag.eC[b]).d);
        } 
      } 
    } 
  }
  
  final void d() {
    for (byte b = 0; b < 3; b++) {
      if ((ag.eC[b]).a != 0) {
        byte b1;
        byte b2;
        int i = ((ag.eC[b]).b[1]).a - ag.ca.a;
        int j = ((ag.eC[b]).b[1]).b - ag.ca.b - 8;
        if (((ag.eC[b]).e & 0x1) != 0) {
          b1 = 11;
          b2 = 3;
        } else {
          b1 = 3;
          b2 = 11;
        } 
        b(ag.ct[7], i, j, b1, b2, i + ag.cc.a, j + ag.cc.b);
      } 
    } 
  }
  
  private void l() {
    for (byte b = 0; b < ag.cb.a; b++) {
      for (byte b1 = 0; b1 < ag.cb.b; b1++) {
        if (ag.eE[b1][b] != 0) {
          int i = (ag.ce + b1) * ag.cE.b.a + ag.cd + b;
          if ((ag.cE.a[ag.cE.f + i] & 0x2) != 0 && ag.cE.a[ag.cE.d + i] - 1 >= 0) {
            int j = ag.cJ[ag.cE.a[ag.cE.d + i] - 1] - 1;
            b(ag.bT[j], (ag.cd + b) * 27 - ag.ca.a, (ag.ce + b1) * 27 - ag.ca.b, 27, 27, 0, 0);
          } 
        } 
      } 
    } 
  }
  
  private void m() {
    byte[] arrayOfByte1 = { 3, -10, 10 };
    byte[] arrayOfByte2 = { -6, 0, 5 };
    if (ag.fh == 3) {
      int i = (ag.cz.a[0]).a - ag.ca.a;
      int j = (ag.cz.a[0]).b - ag.ca.b;
      switch (ag.cz.e[0]) {
        case 27:
          if (ag.cz.f[0] == 9) {
            i += ae.aA[ag.cz.d[1] >> 1];
            j += ae.aB[ag.cz.d[1] >> 1];
          } 
          break;
        case 28:
        case 29:
        case 30:
          i = ag.dd;
          j = ag.de + 11;
          break;
      } 
      byte[] arrayOfByte = new byte[ag.fg];
      System.arraycopy(ag.eX, ag.eZ, arrayOfByte, 0, ag.fg);
      a(ag.fj, arrayOfByte, ag.fg, i, j);
      for (byte b = 0; b < ag.fg; b++)
        a((ag.cz.a[0]).a - (ag.fj[b]).e, (ag.cz.a[0]).b - (ag.fj[b]).f, (ag.fj[b]).c, (ag.fj[b]).d); 
      ag.fg = 1;
    } 
    if (ag.dU.a != 0) {
      byte b2;
      byte[] arrayOfByte;
      byte b1 = 2;
      switch (ag.dU.a) {
        case -2:
          arrayOfByte = ae.ar;
          b2 = 63;
          ag.dU.f = ag.dU.b;
          break;
        case -1:
          arrayOfByte = ae.ao;
          b2 = 60;
          ag.dU.f = ag.dU.b;
          b1 = 0;
          break;
        case 10:
        case 11:
          arrayOfByte = ae.av;
          b2 = 67;
          if (ag.dU.b > 0) {
            ag.dU.f = (short)(ag.dU.b - 1 + (ag.dU.d << 2));
            break;
          } 
          return;
        default:
          arrayOfByte = ae.am;
          b2 = 58;
          ag.dU.f = (short)(ag.dU.b + 4);
          break;
      } 
      if (ag.dU.g == null) {
        ag.dU.g = arrayOfByte;
        ag.dU.h = K(b2);
      } 
      while (b1 < 3) {
        int i = ag.dU.c.a - ag.ca.a;
        int j = ag.dU.c.b - ag.ca.b;
        if (ag.dU.a == -1) {
          i += arrayOfByte1[b1];
          j += arrayOfByte2[b1];
        } 
        a(ag.dU.h[ag.dU.f], ag.dU.g[ag.dU.f], i, j);
        a(ag.dU.c.a - (ag.dU.h[ag.dU.f]).e, ag.dU.c.b - (ag.dU.h[ag.dU.f]).f, (ag.dU.h[ag.dU.f]).c, (ag.dU.h[ag.dU.f]).d);
        b1++;
      } 
    } 
  }
  
  private void a(y paramy, byte paramByte, int paramInt1, int paramInt2) {
    y[] arrayOfY = new y[1];
    byte[] arrayOfByte = new byte[1];
    arrayOfY[0] = paramy;
    arrayOfByte[0] = paramByte;
    a(arrayOfY, arrayOfByte, 1, paramInt1, paramInt2);
  }
  
  private void a(y[] paramArrayOfy, byte[] paramArrayOfbyte, int paramInt1, int paramInt2, int paramInt3) {
    byte b1 = 0;
    Image image = null;
    for (byte b = 0; b < paramInt1; b++) {
      if (paramArrayOfbyte[b] != b1 && (b1 = paramArrayOfbyte[b]) != 0)
        image = d(ag.bC.a(b1 - 27)); 
      if (b1 != 0)
        b(image, paramInt2 - (paramArrayOfy[b]).e, paramInt3 - (paramArrayOfy[b]).f, image.getWidth(), image.getHeight(), 0, 0); 
    } 
  }
  
  final void e() {
    boolean bool = true;
    ag.cz.L = ag.cz.ab[ag.cz.e[0]][ag.cz.d[0]][ag.cz.f[0]];
    for (byte b = 0; b < ag.ez; b++) {
      short s = ag.ey[b];
      if (bool && (ag.cz.a[0]).b < ((ag.ex[s]).a[0]).b) {
        o();
        bool = false;
      } 
      e(s);
    } 
    if (bool)
      o(); 
    n();
  }
  
  private void n() {
    for (byte b = 0; b < ag.cB; b++) {
      if ((ag.cA[b]).a != 0 && (ag.cA[b]).h != 0) {
        int i = (ag.cA[b]).b.a - ag.ca.a;
        int j = (ag.cA[b]).b.b - ag.ca.b;
        int k;
        if ((k = 2 - (ag.cA[b]).h) <= 3 && k >= 0) {
          if (ag.ct[43] == null)
            return; 
          ag.bc.a(k, i, j);
          a((ag.cA[b]).b.a - (ag.eV[k]).e, (ag.cA[b]).b.b - (ag.eV[k]).f, (ag.eV[k]).c, (ag.eV[k]).d);
        } else {
          break;
        } 
      } 
    } 
  }
  
  private void e(int paramInt) {
    int k = 0;
    int m = 0;
    byte[] arrayOfByte = null;
    (ag.ex[paramInt]).f[0] = Math.min((ag.ex[paramInt]).f[0], ((ag.ex[paramInt]).B[(ag.ex[paramInt]).e[0]]).length - 1);
    int i = ((ag.ex[paramInt]).a[0]).a - ag.ca.a;
    int j = ((ag.ex[paramInt]).a[0]).b - ag.ca.b;
    short s = (ag.ex[paramInt]).B[(ag.ex[paramInt]).e[0]][(ag.ex[paramInt]).f[0]][(ag.ex[paramInt]).g[0]];
    if ((ag.ex[paramInt]).h > 200) {
      if (s < 100)
        if ((ag.ex[paramInt]).h == 203) {
          for (byte b = 0; b < 3; b++)
            b((ag.ex[paramInt]).C, i - ((ag.ex[paramInt]).D[s]).e + ae.ay[ae.aT[(ag.ex[paramInt]).e[0]]][b][0], j - ((ag.ex[paramInt]).D[s]).f + ae.ay[ae.aT[(ag.ex[paramInt]).e[0]]][b][1], ((ag.ex[paramInt]).D[s]).c, ((ag.ex[paramInt]).D[s]).d, ((ag.ex[paramInt]).D[s]).a, ((ag.ex[paramInt]).D[s]).b); 
          a(((ag.ex[paramInt]).a[0]).a - ((ag.ex[paramInt]).D[s]).e + ae.az[ae.aT[(ag.ex[paramInt]).e[1]]][0], ((ag.ex[paramInt]).a[0]).b - ((ag.ex[paramInt]).D[s]).f + ae.az[ae.aT[(ag.ex[paramInt]).e[1]]][1], ((ag.ex[paramInt]).D[s]).c + ae.az[ae.aT[(ag.ex[paramInt]).e[1]]][2], ((ag.ex[paramInt]).D[s]).d + ae.az[ae.aT[(ag.ex[paramInt]).e[1]]][3]);
        } else {
          if ((ag.ex[paramInt]).h == 202) {
            (ag.ex[paramInt]).C = ag.es[1];
            (ag.ex[paramInt]).D = ag.et[1];
          } 
          b((ag.ex[paramInt]).C, i - ((ag.ex[paramInt]).D[s]).e, j - ((ag.ex[paramInt]).D[s]).f, ((ag.ex[paramInt]).D[s]).c, ((ag.ex[paramInt]).D[s]).d, ((ag.ex[paramInt]).D[s]).a, ((ag.ex[paramInt]).D[s]).b);
          a(((ag.ex[paramInt]).a[0]).a - ((ag.ex[paramInt]).D[s]).e, ((ag.ex[paramInt]).a[0]).b - ((ag.ex[paramInt]).D[s]).f, ((ag.ex[paramInt]).D[s]).c, ((ag.ex[paramInt]).D[s]).d);
        }  
    } else {
      int n;
      y[] arrayOfY1;
      y[] arrayOfY2;
      y[] arrayOfY3;
      if ((ag.ex[paramInt]).f[0] < 6) {
        int i1;
        n = (i1 = (ag.dC.c != '\000') ? 1310732 : 1053711) >> s & 0x1;
        arrayOfY1 = ag.et[4];
        arrayOfY2 = ag.et[3];
        arrayOfY3 = ag.et[5];
      } else {
        byte b = (ag.dC.c != '\000') ? 2 : 3;
        n = ae.aJ[(s >> 5 << 2) + b] >> (s & 0x1F) & 0x1;
        arrayOfY1 = ag.et[7];
        arrayOfY2 = ag.et[6];
        arrayOfY3 = ag.et[8];
      } 
      switch ((ag.ex[paramInt]).f[0]) {
        case 6:
          if ((ag.ex[paramInt]).g[0] > 2 && (ag.ex[paramInt]).g[0] < 6) {
            ag.fk = 1;
            ag.fl = ag.ct[44];
            k = (ag.ex[paramInt]).e[0] + ((ag.ex[paramInt]).g[0] & 0x1);
            ag.fm = new y[(m = ag.eW.length) - k];
            for (byte b = 0; b < ag.fm.length; b++)
              ag.fm[b] = ag.eW[k + b]; 
          } 
          break;
        case 7:
          if ((ag.ex[paramInt]).g[0] > 4 && (ag.ex[paramInt]).g[0] < 8) {
            ag.fk = 1;
            ag.fl = ag.ct[44];
            k = (ag.ex[paramInt]).e[0] + ((ag.ex[paramInt]).g[0] & 0x1);
            ag.fm = new y[(m = ag.eW.length) - k];
            for (byte b = 0; b < ag.fm.length; b++)
              ag.fm[b] = ag.eW[k + b]; 
          } 
          break;
        case 8:
          if ((ag.ex[paramInt]).g[0] > 0 && (ag.ex[paramInt]).g[0] < 9) {
            ag.fk = 1;
            ag.fl = ag.ct[44];
            k = (ag.ex[paramInt]).e[0] + ((ag.ex[paramInt]).g[0] & 0x1);
            ag.fm = new y[(m = ag.eW.length) - k];
            for (byte b = 0; b < ag.fm.length; b++)
              ag.fm[b] = ag.eW[k + b]; 
          } 
          break;
        case 9:
        case 10:
          if ((ag.ex[paramInt]).g[0] > 3) {
            if ((ag.ex[paramInt]).g[0] == 4) {
              ag.fb = K(57);
              ag.fa = ae.al;
            } 
            ag.fk = 2;
            ag.fl = null;
            ag.fc = (short)((ag.ex[paramInt]).g[0] - 4);
            ag.fm = new y[ag.fb.length - ag.fc];
            for (byte b = 0; b < ag.fm.length; b++)
              ag.fm[b] = ag.fb[ag.fc + b]; 
          } 
          break;
        case 11:
        case 12:
        case 13:
          if ((ag.ex[paramInt]).g[0] > 3 && (ag.ex[paramInt]).g[0] < 10) {
            if ((ag.ex[paramInt]).g[0] == 4) {
              ag.fb = K(58);
              ag.fa = ae.am;
            } 
            ag.fk = 2;
            ag.fl = null;
            ag.fc = (short)((ag.ex[paramInt]).g[0] - 4);
            ag.fm = new y[ag.fb.length - ag.fc];
            for (byte b = 0; b < ag.fm.length; b++)
              ag.fm[b] = ag.fb[ag.fc + b]; 
          } 
          break;
        case 15:
          if ((ag.ex[paramInt]).g[0] == 5 || (ag.ex[paramInt]).g[0] == 6) {
            if ((ag.ex[paramInt]).g[0] == 5) {
              ag.fb = K(59);
              ag.fa = ae.an;
            } 
            ag.fk = 1;
            ag.fl = null;
            ag.fc = (short)((ag.ex[paramInt]).g[0] - 5);
            ag.fm = new y[ag.fb.length - ag.fc];
            for (byte b = 0; b < ag.fm.length; b++)
              ag.fm[b] = ag.fb[ag.fc + b]; 
          } 
          break;
        case 16:
          if ((ag.ex[paramInt]).g[0] > 1 && (ag.ex[paramInt]).g[0] < 6) {
            ag.fk = 1;
            ag.fl = ag.ct[44];
            k = (ag.ex[paramInt]).g[0] & 0x1;
            ag.fm = new y[(m = ag.eW.length) - k];
            for (byte b = 0; b < ag.fm.length; b++)
              ag.fm[b] = ag.eW[k + b]; 
          } 
          break;
        case 17:
          if ((ag.ex[paramInt]).g[0] == 5 || (ag.ex[paramInt]).g[0] == 6) {
            ag.fk = 1;
            ag.fl = ag.ct[44];
            k = (ag.ex[paramInt]).g[0] - 5;
            ag.fm = new y[(m = ag.eW.length) - k];
            for (byte b = 0; b < ag.fm.length; b++)
              ag.fm[b] = ag.eW[k + b]; 
          } 
          break;
        case 18:
          if ((ag.ex[paramInt]).g[0] == 5 || (ag.ex[paramInt]).g[0] == 6) {
            if ((ag.ex[paramInt]).g[0] == 5) {
              ag.fb = K(61);
              ag.fa = ae.ap;
            } 
            ag.fk = 1;
            ag.fl = null;
            ag.fc = (short)((ag.ex[paramInt]).g[0] - 5);
            ag.fm = new y[ag.fb.length - ag.fc];
            for (byte b = 0; b < ag.fm.length; b++)
              ag.fm[b] = ag.fb[ag.fc + b]; 
          } 
          break;
        case 21:
          if ((ag.ex[paramInt]).g[0] == 9) {
            ag.fb = K(63);
            ag.fa = ae.ar;
            ag.fc = 2;
            ag.fk = 2;
            ag.fm = new y[ag.fb.length - 1];
            for (byte b = 0; b < ag.fm.length; b++)
              ag.fm[b] = ag.fb[1 + b]; 
          } 
        case 20:
          if ((ag.ex[paramInt]).g[0] > 1 && (ag.ex[paramInt]).g[0] < 9) {
            if ((ag.ex[paramInt]).g[0] == 2) {
              ag.fb = K(62);
              ag.fa = ae.aq;
            } 
            ag.fk = 2;
            ag.fl = null;
            ag.fc = (short)((ag.ex[paramInt]).g[0] - 2 + ((ag.ex[paramInt]).e[0] >> 1) * 7);
            ag.fm = new y[ag.fb.length - ag.fc];
            for (byte b = 0; b < ag.fm.length; b++)
              ag.fm[b] = ag.fb[ag.fc + b]; 
          } 
          break;
      } 
      if (s < 180)
        b(ag.eq, i - (arrayOfY2[s]).e + (arrayOfY2[s]).c / 2 - 13, j - (arrayOfY2[s]).f + (arrayOfY2[s]).d - 5, ag.eq.getWidth(), ag.eq.getHeight(), 0, 0); 
      if (ag.fk == 1) {
        if (ag.fl != null) {
          b(ag.fl, i - (ag.fm[0]).e, j - (ag.fm[0]).f, (ag.fm[0]).c, (ag.fm[0]).d, (ag.fm[0]).a, (ag.fm[0]).b);
        } else {
          (arrayOfByte = new byte[1])[0] = ag.fa[ag.fc];
          a(ag.fm, arrayOfByte, 1, i, j);
        } 
        a(((ag.ex[paramInt]).a[0]).a - (ag.fm[0]).e, ((ag.ex[paramInt]).a[0]).b - (ag.fm[0]).f, (ag.fm[0]).c, (ag.fm[0]).d);
      } 
      ag.em = 0;
      ag.en = 0;
      if (s < 180) {
        if ((ag.ex[paramInt]).q > 0 || (ag.ex[paramInt]).p > 0)
          ag.em = 1; 
        if (ag.em == 1) {
          int i1 = ag.bN % 3;
          b(ag.eR, i - (ag.eQ[i1]).e, j - (ag.eQ[i1]).f + 3, (ag.eQ[i1]).c, (ag.eQ[i1]).d, (ag.eQ[i1]).a, (ag.eQ[i1]).b);
          ag.en = 1;
        } 
        if (n != 0)
          a(i, j, arrayOfY3[s], paramInt); 
        b(ag.cz.aH, i - (arrayOfY2[s]).e, j - (arrayOfY2[s]).f, (arrayOfY2[s]).c, (arrayOfY2[s]).d, (arrayOfY2[s]).a, (arrayOfY2[s]).b);
        b(ag.er[1], i - (arrayOfY1[s]).e, j - (arrayOfY1[s]).f, (arrayOfY1[s]).c, (arrayOfY1[s]).d, (arrayOfY1[s]).a, (arrayOfY1[s]).b);
        a(((ag.ex[paramInt]).a[0]).a - (arrayOfY2[s]).e, ((ag.ex[paramInt]).a[0]).b - (arrayOfY2[s]).f, (arrayOfY2[s]).c, (arrayOfY2[s]).d);
        if (0 == n)
          a(i, j, arrayOfY3[s], paramInt); 
        if (ag.em == 1) {
          int i1 = 3 + ag.bN % 3;
          b(ag.eR, i - (ag.eQ[i1]).e, j - (ag.eQ[i1]).f + 3, (ag.eQ[i1]).c, (ag.eQ[i1]).d, (ag.eQ[i1]).a, (ag.eQ[i1]).b);
          ag.en = 1;
        } 
      } 
      (ag.ex[paramInt]).y = -1;
      if ((ag.ex[paramInt]).f[0] < 6) {
        if (s > 8 && s < 16 && (s & 0x1) != 0) {
          (ag.ex[paramInt]).y = (byte)C(3);
          ag.bc.a(paramInt, (ag.ex[paramInt]).y);
        } 
      } else {
        switch ((ag.ex[paramInt]).f[0]) {
          case 6:
            if ((ag.ex[paramInt]).g[0] > 2 && (ag.ex[paramInt]).g[0] < 6)
              (ag.ex[paramInt]).y = 1; 
            break;
          case 7:
            if ((ag.ex[paramInt]).g[0] > 4 && (ag.ex[paramInt]).g[0] < 8)
              (ag.ex[paramInt]).y = 1; 
            break;
          case 8:
            switch ((ag.ex[paramInt]).g[0]) {
              case 2:
              case 4:
              case 6:
              case 8:
                (ag.ex[paramInt]).y = 1;
                break;
            } 
            break;
          case 14:
            if (((ag.ex[paramInt]).g[0] & 0x1) == 0)
              (ag.ex[paramInt]).y = (byte)C(3); 
            break;
          case 15:
            if ((ag.ex[paramInt]).g[0] == 5)
              (ag.ex[paramInt]).y = 2; 
            break;
          case 16:
            if ((ag.ex[paramInt]).g[0] == 6)
              (ag.ex[paramInt]).y = 2; 
            break;
          case 19:
            if (((ag.ex[paramInt]).g[0] & 0x1) != 0)
              (ag.ex[paramInt]).y = 2; 
            break;
        } 
        if ((ag.ex[paramInt]).y > -1 && (ag.ex[paramInt]).y < 100)
          ag.bc.a(paramInt, (ag.ex[paramInt]).y); 
      } 
      if (ag.fk == 2) {
        if ((ag.ex[paramInt]).f[0] == 21 && (ag.ex[paramInt]).g[0] == 9) {
          i += ae.aA[(ag.ex[paramInt]).e[1] >> 1];
          j += ae.aB[(ag.ex[paramInt]).e[1] >> 1];
        } 
        (arrayOfByte = new byte[1])[0] = ag.fa[ag.fc];
        a(ag.fm, arrayOfByte, 1, i, j);
        a(((ag.ex[paramInt]).a[0]).a - (ag.fm[0]).e, ((ag.ex[paramInt]).a[0]).b - (ag.fm[0]).f, (ag.fm[0]).c, (ag.fm[0]).d);
      } 
    } 
    if ((ag.ex[paramInt]).w != 0) {
      a(ag.fe[(ag.ex[paramInt]).x], ag.fd[(ag.ex[paramInt]).x], i, j);
      a(((ag.ex[paramInt]).a[0]).a - (ag.fe[(ag.ex[paramInt]).x]).e, ((ag.ex[paramInt]).a[0]).b - (ag.fe[(ag.ex[paramInt]).x]).f, (ag.fe[(ag.ex[paramInt]).x]).c, (ag.fe[(ag.ex[paramInt]).x]).d);
    } 
    if ((ag.ex[paramInt]).t != 0) {
      (ag.ex[paramInt]).u = (byte)((ag.ex[paramInt]).u + 1);
      if ((ag.ex[paramInt]).u > 1) {
        (ag.ex[paramInt]).t = 0;
        return;
      } 
      i = (ag.ex[paramInt]).v.a - ag.ca.a;
      j = (ag.ex[paramInt]).v.b - ag.ca.b;
      int n = (ag.ex[paramInt]).u + ((ag.ex[paramInt]).t - 1 << 1);
      ag.bc.a(n, i, j);
      a((ag.ex[paramInt]).v.a - (ag.eV[n]).e, (ag.ex[paramInt]).v.b - (ag.eV[n]).f, (ag.eV[n]).c, (ag.eV[n]).d);
    } 
  }
  
  private void a(int paramInt1, int paramInt2, y paramy, int paramInt3) {
    b(ag.ct[40 + ag.dC.c], paramInt1 - paramy.e, paramInt2 - paramy.f, paramy.c, paramy.d, paramy.a, paramy.b);
    a(((ag.ex[paramInt3]).a[0]).a - paramy.e, ((ag.ex[paramInt3]).a[0]).b - paramy.f, paramy.c, paramy.d);
  }
  
  private void o() {
    int k;
    y[] arrayOfY1;
    y[] arrayOfY2;
    y[] arrayOfY3;
    byte b;
    int m = -1;
    int n = 0;
    int i1 = 0;
    byte[] arrayOfByte = null;
    if (ag.cz.e[0] < 12) {
      long l;
      k = (int)((l = (ag.cz.K != 0) ? Long.parseLong("5789684072952") : Long.parseLong("8263870709823")) >> ag.cz.L & 0x1L);
      if (ag.cz.L > 11 && ag.cz.L < 36 && (ag.cz.L & 0x1) != 0)
        m = (ag.cz.L - 12 & 0xFFFE) % 6 >> 1; 
      arrayOfY1 = ag.cz.aC;
      arrayOfY2 = ag.cz.aE;
      arrayOfY3 = ag.eS[ag.cz.K];
    } else {
      byte b1 = (ag.cz.K != 0) ? 0 : 1;
      k = ae.aJ[(ag.cz.L >> 5 << 2) + b1] >> (ag.cz.L & 0x1F) & 0x1;
      arrayOfY1 = ag.cz.aD;
      arrayOfY2 = ag.cz.aF;
      arrayOfY3 = ag.eT[ag.cz.K];
      boolean bool = false;
    } 
    switch (ag.cz.e[0]) {
      case 2:
        ag.fh = 1;
        ag.fi = ag.ct[44];
        n = ag.cz.d[0] + (ag.cz.f[0] & 0x1);
        ag.fj = new y[(i1 = ag.eW.length) - n];
        for (b = 0; b < ag.fj.length; b++)
          ag.fj[b] = ag.eW[n + b]; 
        if (ag.cz.f[0] == 1)
          a_(7); 
        break;
      case 12:
        if (ag.cz.f[0] > 2 && ag.cz.f[0] < 6) {
          m = 1;
          ag.fh = 1;
          ag.fi = ag.ct[44];
          n = ag.cz.d[0] + (ag.cz.f[0] & 0x1);
          ag.fj = new y[(i1 = ag.eW.length) - n];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eW[n + b1]; 
        } 
        break;
      case 13:
        if (ag.cz.f[0] > 4 && ag.cz.f[0] < 8) {
          m = 1;
          ag.fh = 1;
          ag.fi = ag.ct[44];
          n = ag.cz.d[0] + (ag.cz.f[0] & 0x1);
          ag.fj = new y[(i1 = ag.eW.length) - n];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eW[n + b1]; 
        } 
        break;
      case 14:
        if (ag.cz.f[0] > 0 && ag.cz.f[0] < 9) {
          if (0 == (ag.cz.f[0] & 0x1))
            m = 1; 
          ag.fh = 1;
          ag.fi = ag.ct[44];
          n = ag.cz.d[0] + (ag.cz.f[0] & 0x1);
          ag.fj = new y[(i1 = ag.eW.length) - n];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eW[n + b1]; 
        } 
        break;
      case 15:
      case 16:
        if (ag.cz.f[0] > 3) {
          if (ag.eX == null) {
            ag.eY = K(57);
            ag.eX = ae.al;
          } 
          ag.fh = 2;
          ag.fi = null;
          ag.eZ = (short)(ag.cz.f[0] - 4);
          ag.fj = new y[ag.eY.length - ag.eZ];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eY[ag.eZ + b1]; 
        } 
        break;
      case 17:
      case 18:
      case 19:
        if (ag.cz.f[0] > 3 && ag.cz.f[0] < 10) {
          if (ag.eX == null) {
            ag.eY = K(58);
            ag.eX = ae.am;
          } 
          ag.fh = 3;
          ag.fi = null;
          ag.eZ = (short)(ag.cz.f[0] - 4);
          ag.fj = new y[ag.eY.length - ag.eZ];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eY[ag.eZ + b1]; 
        } 
        break;
      case 20:
        if ((ag.cz.f[0] & 0x1) != 0)
          m = ag.cz.M; 
        break;
      case 21:
        if (ag.cz.f[0] == 5 || ag.cz.f[0] == 6) {
          if (ag.cz.f[0] == 5) {
            m = 2;
            ag.eY = K(59);
            ag.eX = ae.an;
          } 
          ag.fh = 1;
          ag.fi = null;
          ag.eZ = (short)(ag.cz.f[0] - 5);
          ag.fj = new y[ag.eY.length - ag.eZ];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eY[ag.eZ + b1]; 
        } 
        break;
      case 22:
        if (ag.cz.f[0] > 1 && ag.cz.f[0] < 6) {
          ag.fh = 1;
          ag.fi = ag.ct[44];
          n = ag.cz.f[0] & 0x1;
          ag.fj = new y[(i1 = ag.eW.length) - n];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eW[n + b1]; 
          break;
        } 
        if (ag.cz.f[0] == 6)
          m = 2; 
        break;
      case 23:
        if (ag.cz.f[0] == 5 || ag.cz.f[0] == 6) {
          ag.fh = 1;
          ag.fi = ag.ct[44];
          n = ag.cz.f[0] - 5;
          ag.fj = new y[(i1 = ag.eW.length) - n];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eW[n + b1]; 
        } 
        break;
      case 24:
        if (ag.cz.f[0] == 5 || ag.cz.f[0] == 6) {
          if (ag.eX == null) {
            ag.eY = K(61);
            ag.eX = ae.ap;
          } 
          ag.fh = 1;
          ag.fi = null;
          ag.eZ = (short)(ag.cz.f[0] - 5);
          ag.fj = new y[ag.eY.length - 1];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eY[1 + b1]; 
        } 
        break;
      case 25:
        if ((ag.cz.f[0] & 0x1) != 0)
          m = 2; 
        break;
      case 27:
        if (ag.cz.f[0] == 9) {
          ag.eY = K(63);
          ag.eX = ae.ar;
          ag.fh = 3;
          ag.eZ = 1;
          ag.fj = new y[ag.eY.length - 1];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eY[1 + b1]; 
        } 
      case 26:
        if (ag.cz.f[0] > 1 && ag.cz.f[0] < 9) {
          if (ag.eX == null) {
            ag.eY = K(62);
            ag.eX = ae.aq;
          } 
          ag.fh = 3;
          ag.fi = null;
          ag.eZ = (short)(ag.cz.f[0] - 2 + (ag.cz.d[0] >> 1) * 7);
          ag.fj = new y[ag.eY.length - ag.eZ];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eY[ag.eZ + b1]; 
        } 
        break;
      case 28:
        if (ag.cz.f[0] > 3 && ag.cz.f[0] < 22) {
          if (ag.eX == null) {
            ag.eY = K(64);
            ag.eX = ae.as;
          } 
          ag.fh = 3;
          ag.fi = null;
          if (ag.cz.f[0] > 9) {
            ag.eZ = (short)((ag.cz.f[0] - 10) * 3 + 6);
            ag.fg = 3;
          } else {
            ag.eZ = (short)(ag.cz.f[0] - 4);
          } 
          ag.fj = new y[ag.eY.length - ag.eZ];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eY[ag.eZ + b1]; 
        } 
        break;
      case 29:
        if (ag.cz.f[0] > 6 && ag.cz.f[0] < 22) {
          if (ag.eX == null) {
            ag.eY = K(65);
            ag.eX = ae.at;
          } 
          ag.fh = 3;
          ag.fi = null;
          ag.eZ = (short)(ag.cz.f[0] - 7);
          ag.fj = new y[ag.eY.length - ag.eZ];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eY[ag.eZ + b1]; 
        } 
        break;
      case 30:
        if (ag.cz.f[0] > 3 && ag.cz.f[0] < 9) {
          if (ag.eX == null) {
            ag.eY = K(66);
            ag.eX = ae.au;
          } 
          ag.fh = 3;
          ag.fi = null;
          ag.eZ = (short)((ag.cz.f[0] - 4) * 5);
          ag.fj = new y[ag.eY.length - ag.eZ];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eY[ag.eZ + b1]; 
          ag.fg = 5;
          break;
        } 
        if (ag.cz.f[0] > 12 && ag.cz.f[0] < 15) {
          if (ag.cz.f[0] == 13) {
            ag.eY = K(63);
            ag.eX = ae.ar;
          } 
          ag.fh = 3;
          ag.fi = null;
          ag.eZ = (short)((ag.cz.f[0] - 13) * 5 + 2);
          ag.fj = new y[ag.eY.length - ag.eZ];
          for (byte b1 = 0; b1 < ag.fj.length; b1++)
            ag.fj[b1] = ag.eY[ag.eZ + b1]; 
          ag.fg = 3;
        } 
        break;
    } 
    int i = (ag.cz.a[0]).a - ag.ca.a;
    int j = (ag.cz.a[0]).b - ag.ca.b;
    b(ag.eq, i - (arrayOfY2[ag.cz.L]).e + (arrayOfY2[ag.cz.L]).c / 2 - 13, j - (arrayOfY2[ag.cz.L]).f + (arrayOfY2[ag.cz.L]).d - 5, ag.eq.getWidth(), ag.eq.getHeight(), 0, 0);
    if (ag.fh == 1) {
      if (ag.fi != null) {
        b(ag.fi, i - (ag.fj[0]).e, j - (ag.fj[0]).f, (ag.fj[0]).c, (ag.fj[0]).d, (ag.fj[0]).a, (ag.fj[0]).b);
      } else {
        arrayOfByte = new byte[ag.eX.length - ag.eZ];
        System.arraycopy(ag.eX, ag.eZ, arrayOfByte, 0, ag.eX.length - ag.eZ);
        a(ag.fj, arrayOfByte, 1, i, j);
      } 
      a((ag.cz.a[0]).a - (ag.fj[0]).e, (ag.cz.a[0]).b - (ag.fj[0]).f, (ag.fj[0]).c, (ag.fj[0]).d);
    } 
    if (ag.ek == 1) {
      int i2 = ag.bN % 3;
      b(ag.eR, i - (ag.eQ[i2]).e, j - (ag.eQ[i2]).f + 3, (ag.eQ[i2]).c, (ag.eQ[i2]).d, (ag.eQ[i2]).a, (ag.eQ[i2]).b);
      ag.el = 1;
    } 
    if (m > -1)
      if (18 == (ag.cz.d[0] >> 1) * 6 + (m << 1)) {
        ag.bc.a(-1, m);
      } else if (ag.cz.d[0] == 4 && ag.cz.e[0] != 25) {
        ag.bc.a(-1, m);
      }  
    if (k != 0)
      ag.bc.a(i, j, arrayOfY3[ag.cz.L]); 
    b(ag.cz.aH, i - (arrayOfY2[ag.cz.L]).e, j - (arrayOfY2[ag.cz.L]).f, (arrayOfY2[ag.cz.L]).c, (arrayOfY2[ag.cz.L]).d, (arrayOfY2[ag.cz.L]).a, (arrayOfY2[ag.cz.L]).b);
    b(ag.cz.aG, i - (arrayOfY1[ag.cz.L]).e, j - (arrayOfY1[ag.cz.L]).f, (arrayOfY1[ag.cz.L]).c, (arrayOfY1[ag.cz.L]).d, (arrayOfY1[ag.cz.L]).a, (arrayOfY1[ag.cz.L]).b);
    a((ag.cz.a[0]).a - (arrayOfY1[ag.cz.L]).e, (ag.cz.a[0]).b - (arrayOfY1[ag.cz.L]).f, (arrayOfY1[ag.cz.L]).c, (arrayOfY1[ag.cz.L]).d);
    a((ag.cz.a[0]).a - (arrayOfY2[ag.cz.L]).e, (ag.cz.a[0]).b - (arrayOfY2[ag.cz.L]).f, (arrayOfY2[ag.cz.L]).c, (arrayOfY2[ag.cz.L]).d);
    if (0 == k)
      ag.bc.a(i, j, arrayOfY3[ag.cz.L]); 
    if (m > -1)
      if (ag.cz.e[0] == 25) {
        ag.bc.a(-1, m);
      } else if (18 != (ag.cz.d[0] >> 1) * 6 + (m << 1) && ag.cz.d[0] != 4) {
        ag.bc.a(-1, m);
      }  
    if (ag.ek == 1) {
      int i2 = 3 + ag.bN % 3;
      b(ag.eR, i - (ag.eQ[i2]).e, j - (ag.eQ[i2]).f + 3, (ag.eQ[i2]).c, (ag.eQ[i2]).d, (ag.eQ[i2]).a, (ag.eQ[i2]).b);
    } 
    if (ag.fh == 2) {
      arrayOfByte = new byte[ag.eX.length - ag.eZ];
      System.arraycopy(ag.eX, ag.eZ, arrayOfByte, 0, ag.eX.length - ag.eZ);
      a(ag.fj, arrayOfByte, 1, i, j);
      a((ag.cz.a[0]).a - (ag.fj[0]).e, (ag.cz.a[0]).b - (ag.fj[0]).f, (ag.fj[0]).c, (ag.fj[0]).d);
    } else if (ag.cz.T != 0) {
      arrayOfByte = new byte[ag.eX.length - ag.eZ];
      System.arraycopy(ag.eX, ag.eZ, arrayOfByte, 0, ag.eX.length - ag.eZ);
      y[] arrayOfY = new y[ag.eY.length - ag.cz.U];
      for (byte b1 = 0; b1 < ag.eY.length - ag.cz.U; b1++)
        arrayOfY[b1] = ag.eY[ag.cz.U + b1]; 
      a(arrayOfY, arrayOfByte, 1, i, j);
      a((ag.cz.a[0]).a - (ag.eY[ag.cz.U]).e, (ag.cz.a[0]).b - (ag.eY[ag.cz.U]).f, (ag.eY[ag.cz.U]).c, (ag.eY[ag.cz.U]).d);
    } 
    if (ag.cz.O != 0) {
      ag.cz.P++;
      if (ag.cz.P > 1) {
        ag.cz.O = 0;
        return;
      } 
      int i2 = ag.cz.P;
      i = ag.cz.Q.a - ag.ca.a;
      j = ag.cz.Q.b - ag.ca.b;
      ag.bc.a(i2, i, j);
      a(ag.cz.Q.a - (ag.eV[i2]).e, ag.cz.Q.b - (ag.eV[i2]).f, (ag.eV[i2]).c, (ag.eV[i2]).d);
    } 
  }
  
  private void g(int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    for (byte b = 0; b < paramInt4; b++) {
      for (byte b1 = 0; b1 < paramInt3; b1++) {
        int i = paramInt1 + b1 + paramInt2 + b & 0x7;
        while ((ag.cH[i]).c != 0) {
          int j;
          int k;
          if ((j = ag.cE.a[(ag.cH[i]).a] & 0xFF) == paramInt1 + b1 && (k = ag.cE.a[(ag.cH[i]).a + 1] & 0xFF) == paramInt2 + b) {
            int m = (ag.cH[i]).a;
            short s = (short)((s = (short)(ag.cE.a[m + 2] & 0xFF | (ag.cE.a[m + 3] & 0xFF) << 8)) + 4);
            int n = 4;
            do {
            
            } while ((n += c(ag.cE.a[m + n], ag.cE.a[m + n + 1], ag.cE.a[m + n + 2], j, k)) < s);
            break;
          } 
          i = (ag.cH[i]).b;
          if (0 == i)
            break; 
        } 
      } 
    } 
  }
  
  private int c(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5) {
    switch (paramInt1) {
      case 0:
        if (ag.dm == paramInt2 - 1)
          b(paramInt3 + 200, paramInt4, paramInt5, 4); 
        return 3;
    } 
    return 0;
  }
  
  final void b(int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    int i;
    byte[] arrayOfByte1 = { 0, -56, 0, 56, 0 };
    byte[] arrayOfByte2 = { 56, 0, -56, 0, 0 };
    byte b;
    for (b = 0; b < ag.ez && 0 != (ag.ex[b]).c; b++);
    (ag.ex[b]).c = 1;
    ((ag.ex[b]).a[1]).a = (short)(paramInt2 * 27 + 12 + arrayOfByte1[paramInt4]);
    ((ag.ex[b]).a[1]).b = (short)(paramInt3 * 27 + 20 + arrayOfByte2[paramInt4]);
    (ag.ex[b]).b.a = (ag.ex[b]).b.b = 0;
    (ag.ex[b]).e[1] = (ag.ex[b]).d = (byte)((paramInt4 << 1) + 4 & 0x7);
    (ag.ex[b]).e[0] = (ag.ex[b]).d = (byte)((paramInt4 << 1) + 4 & 0x7);
    (ag.ex[b]).f[1] = 0;
    (ag.ex[b]).f[0] = 0;
    (ag.ex[b]).g[1] = 0;
    (ag.ex[b]).g[0] = 0;
    if (paramInt1 == 201 && ag.g(0, 2) != 0)
      paramInt1 = 203; 
    (ag.ex[b]).h = (short)paramInt1;
    (ag.ex[b]).s = 14;
    (ag.ex[b]).r = 0;
    (ag.ex[b]).t = 0;
    (ag.ex[b]).A = 0;
    (ag.ex[b]).z = 0;
    (ag.ex[b]).w = 0;
    (ag.ex[b]).y = 0;
    (ag.ex[b]).n = 0;
    (ag.ex[b]).o = 0;
    (ag.ex[b]).p = 0;
    (ag.ex[b]).q = 0;
    switch (paramInt1) {
      case 202:
        (ag.ex[b]).r = 1;
        (ag.ex[b]).s = 15;
      case 201:
        if (paramInt1 == 203) {
          i = 0;
        } else {
          i = paramInt1 - 201;
        } 
        (ag.ex[b]).B = ag.eL[i];
        (ag.ex[b]).C = ag.es[i];
        (ag.ex[b]).D = ag.et[i];
        a(paramInt1 - 201, b);
        break;
      case 203:
        if (paramInt1 == 203) {
          i = 0;
        } else {
          i = paramInt1 - 201;
        } 
        (ag.ex[b]).B = ag.eL[i];
        (ag.ex[b]).C = ag.es[i];
        (ag.ex[b]).D = ag.et[i];
        a(paramInt1 - 201, b);
        break;
      default:
        if ((ag.dz[ag.dm]).e == paramInt1)
          ag.cr = 1; 
        ag.eB = 1;
        ag.dG = 1;
        ag.dJ = (short)paramInt1;
        B(paramInt1);
        am();
        ag.ck = 1;
        ag.bV = 5;
        a(4, b);
        (ag.ex[b]).B = ag.eK;
        if (ag.ct[40 + ag.dC.c] == null)
          ag.ct[40 + ag.dC.c] = d(ag.bB.a(42 + ag.dC.c)); 
        if (ag.er[1] == null)
          ag.er[1] = d(ag.bB.a(50 + ag.dC.b - 1)); 
        ag.et[3] = K(68);
        ag.et[4] = K(70 + ag.dC.b - 1);
        ag.et[5] = K(88 + (ag.dC.c << 2));
        ag.et[6] = K(69);
        ag.et[7] = K(76 + ag.dC.b - 1);
        ag.et[8] = K(90 + (ag.dC.c << 2));
        (ag.ex[b]).C = ag.cz.aH;
        (ag.ex[b]).D = ag.et[2];
        ag.eD[1] = 1;
        break;
    } 
    ag.ey[ag.ez] = (short)b;
    ag.ez = (short)(ag.ez + 1);
    if (paramInt1 != 202)
      ag.eA = (short)(ag.eA + 1); 
  }
  
  private void a(int paramInt1, int paramInt2) {
    int[] arrayOfInt1 = { 100, 100, 150 };
    int[] arrayOfInt2 = { 3, 2, 3 };
    int[] arrayOfInt3 = { 7, 5, 7 };
    if (paramInt1 == 4) {
      (ag.ex[paramInt2]).i = (short)(ag.cz.l + ag.eD[1]);
      (ag.ex[paramInt2]).j = (short)((ag.dC.g + (ag.ex[paramInt2]).i - 1) * 6 / 5);
      (ag.ex[paramInt2]).k = (short)((ag.dC.h + (ag.ex[paramInt2]).i - 1) * 6 / 5);
      (ag.ex[paramInt2]).m = (ag.ex[paramInt2]).l = (short)(ag.dC.i + ((ag.ex[paramInt2]).i - 1) * 3);
      return;
    } 
    if (ag.cz.l < 21) {
      int i;
      (ag.ex[paramInt2]).i = ((i = ag.cz.l + ag.g(0, 5) - 2) > 0) ? (short)i : 1;
    } else if (ag.cz.l < 41) {
      (ag.ex[paramInt2]).i = (short)(ag.cz.l + C(9) - 3);
    } else {
      (ag.ex[paramInt2]).i = (short)(ag.cz.l + C(16) - 5);
    } 
    (ag.ex[paramInt2]).j = (short)((arrayOfInt2[paramInt1] + (ag.ex[paramInt2]).i) * arrayOfInt1[paramInt1] / 100);
    (ag.ex[paramInt2]).k = (short)((ag.ex[paramInt2]).i - 1);
    (ag.ex[paramInt2]).m = (ag.ex[paramInt2]).l = (short)(arrayOfInt3[paramInt1] + 3 * (ag.ex[paramInt2]).i);
  }
  
  private static void p() {
    ag.ez = 0;
    ag.eA = 0;
    for (byte b = 0; b < 7; b++) {
      if (ag.ex[b] == null)
        ag.ex[b] = new ap(); 
      (ag.ex[b]).c = 0;
    } 
  }
  
  private void h(int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    int i = paramInt3 / 27;
    int j = paramInt4 / 27;
    if (i < paramInt1) {
      i = paramInt1;
    } else if (i > paramInt1 + 6) {
      i = paramInt1 + 6;
    } 
    if (j < paramInt2) {
      j = paramInt2;
    } else if (j > paramInt2 + 6) {
      j = paramInt2 + 6;
    } 
    byte b;
    for (b = 0; b < 7; b++) {
      for (byte b1 = 0; b1 < 7; b1++)
        ag.ew[b][b1] = 0; 
    } 
    for (b = 0; b < 7; b++) {
      for (byte b1 = 0; b1 < 7; b1++) {
        int k = paramInt1 + b + (paramInt2 + b1) * ag.cE.b.a;
        if ((ag.cE.a[ag.cE.f + k] & 0x1) != 0)
          ag.ew[b][b1] = -1; 
      } 
    } 
    b(i - paramInt1, j - paramInt2);
  }
  
  private void b(int paramInt1, int paramInt2) {
    byte[] arrayOfByte1 = { 0, -1, 0, 1 };
    byte[] arrayOfByte2 = { 1, 0, -1, 0 };
    ag.ew[paramInt1][paramInt2] = 1;
    for (byte b = 0; b < 4; b++) {
      if (paramInt1 + arrayOfByte1[b] > -1 && paramInt1 + arrayOfByte1[b] < 7 && paramInt2 + arrayOfByte2[b] > -1 && paramInt2 + arrayOfByte2[b] < 7 && 0 == ag.ew[paramInt1 + arrayOfByte1[b]][paramInt2 + arrayOfByte2[b]])
        b(paramInt1 + arrayOfByte1[b], paramInt2 + arrayOfByte2[b]); 
    } 
  }
  
  final void a(int paramInt) {
    int j = ag.cE.b.a / 7 * ag.cE.b.b / 7;
    byte[] arrayOfByte = ag.v(paramInt - 1);
    int i = 20 + j * ag.dm * 19;
    for (byte b = 0; b < j; b++) {
      if (ag.eO[b] == null)
        ag.eO[b] = new au(); 
      (ag.eO[b]).a[0] = ag.b(arrayOfByte[i]);
      (ag.eO[b]).a[1] = ag.b(arrayOfByte[i + 1]);
      (ag.eO[b]).a[2] = ag.b(arrayOfByte[i + 2]);
      (ag.eO[b]).a[3] = ag.b(arrayOfByte[i + 3]);
      (ag.eO[b]).b = ag.b(arrayOfByte[i + 4]);
      (ag.eO[b]).c = ag.b(arrayOfByte[i + 5]);
      (ag.eO[b]).d = ag.b(arrayOfByte[i + 6]);
      (ag.eO[b]).e = ag.b(arrayOfByte[i + 7]);
      (ag.eO[b]).f = ag.b(arrayOfByte[i + 8]);
      (ag.eO[b]).g = ag.b(arrayOfByte[i + 9]);
      (ag.eO[b]).h = ag.b(arrayOfByte[i + 10]);
      (ag.eO[b]).i = ag.b(arrayOfByte[i + 11]);
      (ag.eO[b]).j = ag.b(arrayOfByte[i + 12]);
      (ag.eO[b]).k = ag.b(arrayOfByte[i + 13]);
      (ag.eO[b]).l = ag.b(arrayOfByte[i + 14]);
      (ag.eO[b]).m = ag.b(arrayOfByte[i + 15]);
      (ag.eO[b]).n = ag.b(arrayOfByte[i + 16]);
      (ag.eO[b]).o = ag.b(arrayOfByte[i + 18]);
      i += 19;
    } 
  }
  
  static void f() {
    (ag.cz.b[0]).a = (short)((ag.cz.a[0]).a / 27);
    (ag.cz.b[0]).b = (short)(((ag.cz.a[0]).b - 6) / 27);
  }
  
  private static void aB() {
    if (ag.cE != null)
      ag.cE.a(); 
  }
  
  final o b(int paramInt) {
    o o = new o();
    int i = 0;
    int k = 0;
    aB();
    byte[] arrayOfByte;
    k = (arrayOfByte = j.a("/" + ag.bF.a(paramInt - 1))).length;
    o.a = new short[k];
    byte b;
    for (b = 0; b < k; b++)
      o.a[b] = (short)(arrayOfByte[b] & 0xFF); 
    if (o.b == null)
      o.b = new aj(); 
    o.b.a = o.a[0];
    o.b.b = o.a[1];
    o.b.c = o.a[2];
    i = 3 + o.b.c;
    o.c = i;
    int j = o.b.b * o.b.a;
    i += j;
    o.d = i;
    i += j;
    o.e = i;
    i += j;
    o.f = i;
    aC();
    i += j;
    if (k > i) {
      short s = o.a[i++];
      i += 2;
      for (b = 0; b < s; b++) {
        short s1 = o.a[i];
        short s2 = o.a[i + 1];
        int m = o.a[i + 2] & 0xFF | o.a[i + 3] << 8 & 0xFF00;
        a(i, s1, s2);
        i = i + 4 + m;
      } 
    } 
    return o;
  }
  
  private static void aC() {
    ag.cI = 8;
    for (byte b = 0; b < 50; b++) {
      if (ag.cH[b] == null)
        ag.cH[b] = new ah(); 
      (ag.cH[b]).c = 0;
    } 
  }
  
  private static void a(int paramInt1, int paramInt2, int paramInt3) {
    int i = paramInt2 + paramInt3 & 0x7;
    if (ag.cH[i] == null)
      ag.cH[i] = new ah(); 
    if ((ag.cH[i]).c != 0) {
      while ((ag.cH[i]).b != 0)
        i = (ag.cH[i]).b; 
      (ag.cH[ag.cI]).c = 1;
      (ag.cH[ag.cI]).a = paramInt1;
      (ag.cH[ag.cI]).b = 0;
      ag.cI = (short)(ag.cI + 1);
      (ag.cH[i]).b = ag.cI;
      return;
    } 
    (ag.cH[i]).c = 1;
    (ag.cH[i]).a = paramInt1;
    (ag.cH[i]).b = 0;
  }
  
  final void a(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5) {
    x.a(ag.cu);
    ag.cB = 0;
    byte b1;
    for (b1 = 0; b1 < ag.cA.length; b1++) {
      if (ag.cA[b1] == null)
        ag.cA[b1] = new r(); 
      (ag.cA[b1]).a = 0;
    } 
    for (b1 = 0; b1 < 3; b1++) {
      if (ag.eC[b1] == null)
        ag.eC[b1] = new f(); 
      (ag.eC[b1]).a = 0;
    } 
    ag.cD = 0;
    for (b1 = 0; b1 < 10; b1++) {
      if (ag.cC[b1] == null)
        ag.cC[b1] = new a(); 
      (ag.cC[b1]).a = 0;
    } 
    ag.ca.a = (short)(ag.cd * 27 + ag.cc.a);
    ag.ca.b = (short)(ag.ce * 27 + ag.cc.b);
    ag.cf.a = (short)(ag.cd / 7);
    ag.cf.b = (short)(ag.ce / 7);
    for (byte b2 = 0; b2 < 2; b2++) {
      int k = 0;
      for (byte b = 0; b < 'ð'; b++)
        ag.cJ[b] = 0; 
      ag.ct[4] = null;
      if (ag.bT != null) {
        for (b1 = 0; b1 < ag.bT.length; b1++)
          ag.bT[b1] = null; 
        ag.bT = null;
        ag.R();
      } 
      for (b1 = 0; b1 < paramInt2; b1++) {
        int m = (paramInt4 + b1) * ag.cE.b.a + paramInt3;
        for (byte b3 = 0; b3 < paramInt1; b3++) {
          if (b2 != 0) {
            if ((ag.cE.a[ag.cE.f + m + b3] & 0x2) != 0 && ag.cE.a[ag.cE.d + m + b3] != 0 && 0 == ag.cJ[ag.cE.a[ag.cE.d + m + b3] - 1])
              ag.cJ[ag.cE.a[ag.cE.d + m + b3] - 1] = (short)++k; 
            if (ag.cE.a[ag.cE.e + m + b3] != 0) {
              if (0 == ag.cJ[ag.cE.a[ag.cE.e + m + b3] - 1]) {
                ag.cJ[ag.cE.a[ag.cE.e + m + b3] - 1] = (short)++k;
                ag.cJ[ag.cE.a[ag.cE.e + m + b3]] = (short)++k;
              } 
              if (paramInt5 != 0) {
                ag.cE.a[ag.cE.e + m + b3] = 0;
              } else {
                if (ag.cA.length <= ag.cB) {
                  r[] arrayOfR = new r[ag.cA.length * 2];
                  System.arraycopy(ag.cA, 0, arrayOfR, 0, ag.cA.length);
                  ag.cA = arrayOfR;
                } 
                if (ag.cA[ag.cB] == null)
                  ag.cA[ag.cB] = new r(); 
                (ag.cA[ag.cB]).a = 1;
                (ag.cA[ag.cB]).c.a = (short)(paramInt3 + b3);
                (ag.cA[ag.cB]).c.b = (short)(paramInt4 + b1);
                (ag.cA[ag.cB]).b.a = (short)((ag.cA[ag.cB]).c.a * 27 + 12);
                (ag.cA[ag.cB]).b.b = (short)((ag.cA[ag.cB]).c.b * 27 + 20);
                (ag.cA[ag.cB]).g = ag.cE.a[ag.cE.e + m + b3];
                switch ((ag.cA[ag.cB]).g) {
                  case 101:
                  case 113:
                    (ag.cA[ag.cB]).d = 41;
                    break;
                  default:
                    (ag.cA[ag.cB]).d = 21;
                    break;
                } 
                (ag.cA[ag.cB]).e = 0;
                (ag.cA[ag.cB]).f = ag.cJ[ag.cE.a[ag.cE.e + m + b3] - 1];
                (ag.cA[ag.cB]).h = 0;
                ag.cB = (short)(ag.cB + 1);
              } 
            } 
          } else {
            if (ag.cE.a[ag.cE.c + m + b3] != 0 && 0 == ag.cJ[ag.cE.a[ag.cE.c + m + b3] - 1])
              ag.cJ[ag.cE.a[ag.cE.c + m + b3] - 1] = (short)++k; 
            if (ag.cE.a[ag.cE.d + m + b3] != 0 && 0 == ag.cJ[ag.cE.a[ag.cE.d + m + b3] - 1])
              ag.cJ[ag.cE.a[ag.cE.d + m + b3] - 1] = (short)++k; 
          } 
        } 
      } 
      boolean bool = false;
      if (ag.bT != null) {
        int m = ag.bT.length;
        while (b1 < m) {
          ag.bT[0] = null;
          b1++;
        } 
        ag.bT = null;
      } 
      ag.R();
      ag.bT = new Image[k];
      for (b1 = 0; b1 < 15; b1++) {
        int m = b1 << 4;
        for (byte b3 = 0; b3 < 16; b3++) {
          if (ag.cJ[m + b3] != 0)
            ag.bT[ag.cJ[m + b3] - 1] = d(ag.bD.a(0 + b1) + "_" + ((b3 >= 9) ? "" : "0") + (b3 + 1)); 
        } 
      } 
      x.a(ag.cu);
      if (0 == b2)
        for (b1 = 0; b1 < paramInt2; b1++) {
          for (byte b3 = 0; b3 < paramInt1; b3++) {
            k = (paramInt4 + b1) * ag.cE.b.a + paramInt3 + b3;
            int m;
            if (ag.cE.a[ag.cE.c + k] != 0 && (m = ag.cJ[ag.cE.a[ag.cE.c + k] - 1] - 1) >= 0)
              ag.c(ag.bT[m], 0, 0, b3 * 27, b1 * 27, 27, 27); 
            if (ag.cE.a[ag.cE.d + k] != 0 && (m = ag.cJ[ag.cE.a[ag.cE.d + k] - 1] - 1) >= 0)
              ag.c(ag.bT[m], 0, 0, b3 * 27, b1 * 27, 27, 27); 
          } 
        }  
    } 
    ag.ct[4] = null;
    if (ag.bV == 4 && ag.cm < 7) {
      x.a(ag.br);
      return;
    } 
    byte[] arrayOfByte1 = { 0, 0, 0, 6 };
    byte[] arrayOfByte2 = { 6, 0, 0, 0 };
    byte[] arrayOfByte3 = { 1, -1, -1, 1 };
    ag.eP = (short)((ag.ce + 4) / 7 * ag.cE.b.a / 7 + (ag.cd + 4) / 7);
    p();
    for (b1 = 0; b1 < 14; b1++)
      ag.eD[b1] = 0; 
    if (0 == paramInt5) {
      ag.eD[0] = (ag.eO[ag.eP]).c;
      ag.eD[1] = (ag.eO[ag.eP]).d;
      ag.eD[2] = (ag.eO[ag.eP]).e;
      ag.eD[3] = (ag.eO[ag.eP]).f;
      ag.eD[4] = (ag.eO[ag.eP]).g;
      ag.eD[5] = (ag.eO[ag.eP]).h;
      ag.eD[6] = (ag.eO[ag.eP]).i;
      ag.eD[7] = (ag.eO[ag.eP]).j;
      ag.eD[8] = (ag.eO[ag.eP]).k;
      ag.eD[9] = (ag.eO[ag.eP]).l;
      ag.eD[10] = (ag.eO[ag.eP]).m;
      ag.eD[11] = (ag.eO[ag.eP]).n;
    } 
    ag.ev = 0;
    int i = (ag.cd + 2) / 7 * 7 + 1;
    int j = (ag.ce + 2) / 7 * 7 + 1;
    ag.bd.h(i, j, (ag.cz.a[0]).a, (ag.cz.a[0]).b);
    for (b1 = 0; b1 < 4; b1++) {
      if ((ag.eO[ag.eP]).a[b1] != 0) {
        int k = i + arrayOfByte1[b1];
        int m = j + arrayOfByte2[b1];
        for (byte b = 0; b < 7; b++) {
          if ((b1 & 0x1) != 0) {
            if (ag.ew[k - i][b] == 1) {
              int n = k + (m + b) * ag.cE.b.a;
              if (0 == ag.cE.a[ag.cE.e + n]) {
                n += arrayOfByte3[b1];
                if ((ag.cE.a[ag.cE.f + n] & 0x1) == 0 && ag.cE.a[ag.cE.e + n] == 0) {
                  if (ag.eu[ag.ev] == null)
                    ag.eu[ag.ev] = new i(); 
                  (ag.eu[ag.ev]).a = (char)k;
                  (ag.eu[ag.ev]).b = (char)(m + b);
                  (ag.eu[ag.ev]).c = (char)b1;
                  ag.ev = (short)(ag.ev + 1);
                } 
              } 
            } 
          } else if (ag.ew[b][m - j] == 1) {
            int n = k + b + m * ag.cE.b.a;
            if (0 == ag.cE.a[ag.cE.e + n]) {
              n += arrayOfByte3[b1] * ag.cE.b.a;
              if ((ag.cE.a[ag.cE.f + n] & 0x1) == 0 && ag.cE.a[ag.cE.e + n] == 0) {
                if (ag.eu[ag.ev] == null)
                  ag.eu[ag.ev] = new i(); 
                (ag.eu[ag.ev]).a = (char)(k + b);
                (ag.eu[ag.ev]).b = (char)m;
                (ag.eu[ag.ev]).c = (char)b1;
                ag.ev = (short)(ag.ev + 1);
              } 
            } 
          } 
        } 
      } 
    } 
    if (paramInt5 != 0) {
      ag.co = 1;
      ag.cn = 5;
    } else {
      ag.bd.g(ag.cd / 7 * 7 + 1, ag.ce / 7 * 7 + 1, 7, 7);
    } 
    for (b1 = 0; b1 < 9; b1++) {
      for (byte b = 0; b < 9; b++)
        ag.eE[b1][b] = 1; 
    } 
    x.a(ag.br);
  }
  
  final void c(int paramInt) {
    char[] arrayOfChar = new char[10];
    char c1 = Character.MIN_VALUE;
    String str = ag.bI.a(ag.eb[0] + paramInt);
    if ((ag.ec == 0 && paramInt < ag.eb[1] - ag.eb[0]) || (ag.ec != 0 && paramInt >= ag.eb[1] - ag.eb[0])) {
      a_(0);
      String str1 = "";
      if (str.charAt(0) > '/' && str.charAt(0) < ':') {
        ag.gf[0] = "";
        if (0 == ag.ee && paramInt == 2) {
          ag.fE = 0;
          str1 = ag.M(1);
        } else {
          byte b;
          for (b = 0; b < 10; b++) {
            if (str.charAt(b) == '|') {
              arrayOfChar[b] = Character.MIN_VALUE;
              break;
            } 
            arrayOfChar[b] = str.charAt(b);
          } 
          ag.fE = ag.a(arrayOfChar);
          ag.dD = str.length() - b;
          str1 = str.substring(b + 1, str.length());
        } 
        ag.fw[0] = str1;
        ag.fG = 0;
        ag.fA[0] = 0;
      } else {
        if (ag.ec != 0 && 0 == (paramInt & 0x1)) {
          ag.fG = 0;
        } else {
          ag.fG = 1;
        } 
        ag.gf[ag.fG] = str1;
        if (ag.ec != 0 && 0 == (paramInt & 0x1)) {
          str1 = "[Master] " + str;
        } else {
          str1 = "[" + ag.cz.k + "] " + str;
        } 
        ag.fw[ag.fG] = str1;
        ag.fA[ag.fG] = 0;
        return;
      } 
    } else {
      byte b;
      if (paramInt == ag.eb[2] - ag.eb[0]) {
        int i = 0;
        int j = 0;
        int k = 0;
        int m = 0;
        byte b1;
        for (b1 = 0; b1 < 'á'; b1++) {
          if ((ag.dy[b1 >> 5] & (1 << (b1 & 0x1F))) != 0L)
            i++; 
        } 
        for (b = 0; b < 45; b++) {
          if (b < 24 && (ag.ed & 1 << b) != 0)
            k++; 
          if (0L == (0x1FEF64FF7E6FL & 1L << b))
            for (b1 = 0; b1 < 5; b1++) {
              int n = b * 5 + b1;
              if ((ag.dy[n >> 5] & (1 << (n & 0x1F))) != 0L)
                j++; 
            }  
        } 
        i = i * 100 / 102;
        j = j * 100 / 18;
        k = k * 100 / 24;
        m = ag.fo * 100 / 44;
        ag.dp[0][0] = "Mission";
        ag.dp[0][1] = "Accomplished";
        ag.dp[0][2] = "" + i + " %";
        ag.dp[0][3] = "Hidden Mission";
        ag.dp[0][4] = "Accomplished";
        ag.dp[0][5] = "" + j + " %";
        ag.dp[0][6] = "Ending Collected";
        ag.dp[0][7] = "" + k + " %";
        ag.dp[0][8] = "Warrior Collected";
        ag.dp[0][9] = "" + m + " %";
        ag.dp[0][10] = "Total Accomplished";
        ag.dp[0][11] = "" + (i + j + k + m >> 2) + " %";
        ag.dq[0] = 11;
        ag.fG = 1;
        ag.fA[0] = ag.bY.b;
        ag.fC[0] = 0;
        return;
      } 
      a_(2);
      ag.gf[1] = "";
      ag.gf[0] = "";
      if (ag.ec != 0) {
        b = -1;
        if (paramInt != 0) {
          c1 = '\n';
        } else {
          c1 = '\001';
        } 
      } else if (0 == ag.ee && paramInt == 5) {
        c1 = Character.MIN_VALUE;
        b = -1;
        str = ag.M(0);
      } else {
        for (b = 0; b < 10; b++) {
          if (str.charAt(b) == '|') {
            arrayOfChar[b] = Character.MIN_VALUE;
            break;
          } 
          arrayOfChar[b] = str.charAt(b);
        } 
        c1 = (char)(ag.a(arrayOfChar) - 1);
      } 
      String str1 = str.substring(b + 1, str.length());
      b(str1.getBytes(), 200, 0);
      ag.ct[35] = d(ag.bA.a(2 + c1));
      ag.fA[0] = ag.bY.b;
      ag.fA[0] = 230;
      ag.fC[0] = 0;
      ag.fG = 0;
      ag.eh = 0;
    } 
  }
  
  final void d(int paramInt) {
    int[] arrayOfInt = { 
        0, 0, 0, 0, 0, 0, 11, 8, 0, 15, 
        15, 20, 17, 19, 19, 0, 30, 22, 35, 38, 
        39, 33, 33, 44 };
    if (paramInt != 0) {
      ag.cz.g[(ag.dz[ag.dm]).a - 1] = (short)(ag.cz.g[(ag.dz[ag.dm]).a - 1] + 5);
      if (ag.cz.g[(ag.dz[ag.dm]).a - 1] > 100)
        ag.cz.g[(ag.dz[ag.dm]).a - 1] = 100; 
      ag.dx |= 1L << ag.ds[ag.dk] - 1;
      int i = (ag.ds[ag.dk] - 1) * 5 + ag.dm;
      ag.dy[i >> 5] = ag.dy[i >> 5] | (1 << (i & 0x1F));
    } 
    ag.cq = (byte)ag.ds[ag.dk];
    if ((ag.dz[ag.dm]).f < 200 && paramInt != 0) {
      g();
    } else {
      int i;
      if (paramInt != 0) {
        i = (ag.dz[ag.dm]).f - 200;
      } else {
        i = (ag.dz[ag.dm]).g - 200;
      } 
      ag.ck = 1;
      ac();
      w(2);
      ag.dE = ag.fU;
      ag.cO = 0;
      if (i != 3 || 0 != ag.L(502))
        ag.ed |= 1 << i; 
      if (0 == i) {
        byte b = 0;
        int j = ag.cz.g[1];
        if (ag.cz.g[0] + ag.cz.g[15] > j) {
          j = ag.cz.g[0] + ag.cz.g[15];
          b = 1;
        } 
        if (ag.cz.g[2] + ag.cz.g[10] + ag.cz.g[14] > j) {
          j = ag.cz.g[2] + ag.cz.g[10] + ag.cz.g[14];
          b = 2;
        } 
        if ((j = (j - 20) / 10) > 8) {
          j = 8;
        } else if (j < 0) {
          j = 0;
        } 
        ag.cz.h = (short)b;
        ag.cz.i = (short)j;
      } 
      ag.cq = (byte)arrayOfInt[i];
      if (0 == ag.cq)
        for (byte b = 0; b < 22; b++)
          ag.cz.g[b] = 0;  
      if (i == 2) {
        ag.ef = 502;
      } else if (C(10) != 0) {
        ag.ef = 0;
      } else {
        ag.ef = (short)(101 + ((ag.cz.l / 20 > 4) ? (4 + 5 * C(20)) : (ag.cz.l / 20 + 5 * C(20))));
      } 
      byte b2 = 0;
      ag.eg = 0;
      byte b1;
      for (b1 = 0; b1 < 45; b1++) {
        if (0L == (ag.dw & 1L << b1))
          b2++; 
      } 
      if (b2 != 0) {
        int j = C(b2);
        byte b = 0;
        for (b1 = 0; b1 < 45; b1++) {
          if (0L == (ag.dw & 1L << b1)) {
            if (j == b) {
              ag.dw |= 1L << b1;
              ag.eg = (short)(b1 + 1);
              break;
            } 
            b++;
          } 
        } 
      } 
      if (ag.ef != 0 && 0 == k(ag.ef, 1))
        ag.ef = 0; 
      l(i, 1);
    } 
    if (ag.fo != 0)
      ag.cz.S = 1; 
    ag.cz.E += (ag.dz[ag.dm]).h * 150 * (1 + (ag.ep ^ 0x1));
    ay();
    ag.dj = 0;
    ar();
  }
  
  final void g() {
    ag.dG = 2;
    ag.bV = 5;
    am();
    ag.ck = 1;
  }
  
  static void h() {
    int[] arrayOfInt = null;
    int i = 0;
    arrayOfInt = ag.bb.p();
    ag.cz.F += ag.dY;
    ag.dZ[0] = (short)(int)(ag.cz.G * 100L / arrayOfInt[0]);
    for (byte b = 0; b < 2; b++) {
      if (b != 0 && ag.dX < (ag.dz[ag.dm]).i)
        ag.dY += (((ag.dz[ag.dm]).i - ag.dX) / (ag.dz[ag.dm]).i / 10 + 1) * ag.dY / 20; 
      i = ag.dY << 1 + (ag.ep ^ 0x1);
      int j = 0;
      for (byte b1 = 0; b1 < 10; b1++) {
        j += arrayOfInt[b1];
        if (ag.cz.G + i < j) {
          int k = arrayOfInt[b1] - j + ag.cz.G + i;
          ag.dZ[b + 1] = (short)(k * 100 / arrayOfInt[b1] + b1 * 100);
          if (ag.dZ[b + 1] < b1 * 100 + 1)
            ag.dZ[b + 1] = (short)(b1 * 100 + 1); 
          if (b == 1)
            ag.cz.G = k; 
          break;
        } 
      } 
    } 
    ag.ea = 0;
  }
  
  final void i() {
    byte[] arrayOfByte1 = { 20, 20, 25 };
    byte[] arrayOfByte2 = { 
        0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 5, 6, 5, 5 };
    int i = -1;
    int j = 0;
    boolean bool = true;
    int k = 0;
    int m = 0;
    aD();
    aF();
    aG();
    aH();
    aI();
    aK();
    aL();
    if (ag.co == 1)
      aE(); 
    switch (ag.cj) {
      case -1:
      case 50:
        i = 4;
        break;
      case -3:
      case 52:
        i = 2;
        break;
      case -4:
      case 54:
        i = 6;
        break;
      case -2:
      case 56:
        i = 0;
        break;
    } 
    switch (ag.ch) {
      case 49:
        j = ag.cz.V[0];
        break;
      case 51:
        j = ag.cz.V[1];
        break;
      case 55:
        j = ag.cz.V[2];
        break;
      case 57:
        j = ag.cz.V[3];
        break;
      case 48:
        j = ag.cz.V[4];
        break;
      case -5:
      case 53:
        j = 3;
        break;
      case 35:
      case 42:
        if (0 == ag.dU.a && ag.cz.e[0] < 10) {
          ag.dU.a = (ag.cz.Z[ag.cz.aa[(ag.ch == 42) ? 0 : 1]]).a;
          if (ag.dU.a > 9) {
            if (ag.cz.e[0] > 1) {
              ag.dU.a = 0;
              break;
            } 
            ag.cz.e[0] = 11;
          } else if (ag.dU.a != 0) {
            a_(8);
          } 
          ag.dU.e = (short)ag.cz.aa[(ag.ch == 42) ? 0 : 1];
          ag.dU.b = 0;
          ag.dU.c.a = (ag.cz.a[0]).a;
          ag.dU.c.b = (ag.cz.a[0]).b;
          ag.dU.d = (short)ae.aT[ag.cz.d[0]];
        } 
        break;
      case -7:
        if (ag.bg != null) {
          a_(-1);
          ag.ai();
        } 
        ag.af();
        ag.cR.a = 1;
        ag.cR.b = 0;
        ag.cM[0] = 10;
        ag.cM[2] = 0;
        ag.cM[1] = 0;
        ag.cN = 7;
        ag.dE = ag.fZ;
        ag.ck = 1;
        ag.ct[10] = d(ag.bA.a(59));
        ag.ct[17] = d(ag.bA.a(27));
        break;
    } 
    if (ag.dU.a > 0) {
      if (ag.dU.a > 9) {
        ag.cz.f[0] = ag.dU.b;
        return;
      } 
    } else {
      ag.bc.d();
      ag.cz.f[0] = (short)(ag.cz.f[0] + 1);
      ag.cs[0] = i;
      if (ag.cz.ab[ag.cz.e[0]][ag.cz.d[0]][ag.cz.f[0]] > 200) {
        if (ag.cz.e[0] == 2) {
          ag.cs[4] = -1;
          ag.cs[3] = -1;
          ag.cs[2] = -1;
          ag.cs[1] = -1;
          ag.cs[0] = -1;
          i = -1;
        } else if (ag.cz.e[0] == 10) {
          ag.cz.f[0] = 10;
          if (ag.fq != 0)
            e.b(ag.fq, -5); 
          ag.cS.e(22);
          ag.dj = 0;
          ar();
          return;
        } 
        ag.cz.f[0] = 0;
        ag.eY = null;
        ag.eX = null;
        if (ag.cz.e[0] != 1)
          ag.cz.e[0] = 0; 
      } 
      if (ag.cz.e[0] < 2) {
        if (i > -1)
          if (ar.e() != 0) {
            ag.cz.e[0] = 2;
            ag.cz.f[0] = 0;
            ag.cz.d[0] = ag.cz.c = i;
            if (ag.bg != null)
              ag.ai(); 
          } else if (ag.cz.c == i) {
            ag.cz.e[0] = ag.cz.e[0] + 1 & 0x1;
            ag.cz.f[0] = 0;
          } else {
            ag.cz.d[0] = ag.cz.c = i;
            ag.cz.e[0] = 1;
            ag.cz.f[0] = 0;
          }  
        if (j == 3) {
          if (ag.cz.N < 7) {
            ag.cz.M = (ag.cz.M + 1) % 3;
          } else {
            ag.cz.M = 0;
          } 
          ag.cz.N = 0;
          ag.cz.e[0] = 3 + ag.cz.M + (ag.cz.K ^ 0x1) * 3;
          ag.cz.f[0] = 0;
          ag.cz.d[0] = ag.cz.c = ae.aT[ag.cz.c] << 1;
        } else if (j > 0 && ar.e(j) != 0) {
          ag.cz.d[0] = ag.cz.c = ae.aT[ag.cz.c] << 1;
          ag.cz.e[0] = j;
          ag.cz.f[0] = 0;
          switch (ag.cz.e[0]) {
            case 15:
            case 16:
            case 21:
            case 22:
            case 23:
            case 24:
            case 25:
              a_(11);
              break;
          } 
        } 
      } 
      int n = ag.cz.c;
      switch (ag.cz.e[0]) {
        case 1:
          k = ae.aw[n];
          m = ae.ax[n];
          break;
        case 2:
          k = ae.aw[n] << 2;
          m = ae.ax[n] << 2;
          break;
        case 3:
        case 4:
        case 5:
        case 6:
        case 7:
        case 8:
          k = ae.aw[n] / 3;
          m = ae.ax[n] / 3;
          break;
        case 12:
          if (ag.cz.f[0] > 2 && ag.cz.f[0] < 6) {
            k = ae.aw[n] << 2;
            m = ae.ax[n] << 2;
          } 
          break;
        case 13:
          if (ag.cz.f[0] > 4 && ag.cz.f[0] < 8) {
            k = ae.aw[n] << 2;
            m = ae.ax[n] << 2;
            if (k > 0) {
              k = ag.bc.a(ag.cz.a[0], k, 6);
            } else if (k < 0) {
              k = ag.bc.a(ag.cz.a[0], k, 2);
            } 
            if (m > 0) {
              m = ag.bc.a(ag.cz.a[0], m, 0);
            } else if (m < 0) {
              m = ag.bc.a(ag.cz.a[0], m, 4);
            } 
            int[] arrayOfInt;
            k = (arrayOfInt = ag.bc.b(ag.cz.a[0], k, m))[0];
            m = arrayOfInt[1];
            (ag.cz.a[0]).a = (short)((ag.cz.a[0]).a + k);
            (ag.cz.a[0]).b = (short)((ag.cz.a[0]).b + m);
          } else {
            break;
          } 
        case 14:
          if (ag.cz.f[0] > 0 && ag.cz.f[0] < 9) {
            k = ae.aw[n];
            m = ae.ax[n];
          } 
          break;
        case 10:
          if (ag.cz.f[0] < 10)
            (ag.cz.a[0]).a = (short)((ag.cz.a[0]).a + (((ag.cz.f[0] & 0x1) != 0) ? -1 : 1)); 
          break;
        case 20:
          if (0 == (ag.cz.f[0] & 0x1)) {
            k = ae.aw[n];
            m = ae.ax[n];
          } 
          break;
        case 9:
          if (ag.cz.R > 0) {
            ag.cz.R--;
            n = ag.cz.c + 4 & 0x7;
            k = ae.aw[n] << 2;
            m = ae.ax[n] << 2;
            break;
          } 
          if (ag.cz.f[0] == 1) {
            n = ag.cz.c + 4 & 0x7;
            k = ae.aw[n] * 3 / 4;
            m = ae.ax[n] * 3 / 4;
            break;
          } 
        default:
          k = m = 0;
          break;
      } 
      if (k != 0 || m != 0) {
        i = ag.bc.a(ag.cz.a[0], k, m, n, -1);
        switch (ag.cz.e[0]) {
          case 1:
            switch (ag.cz.c) {
              case 0:
              case 2:
              case 4:
              case 6:
                k = ae.aw[i];
                m = ae.ax[i];
                if (i == -1 && (i = ar.c(ag.cz.a[0], ag.cz.d[0], -1)) != -1 && (i = ag.bc.a(ag.cz.a[0], k, m, i, -1)) > -1 && i < 8)
                  ag.cz.d[0] = i; 
                break;
              case 1:
              case 3:
              case 5:
              case 7:
                if (i != -1 && i != 9)
                  ag.cz.d[0] = i; 
                break;
            } 
            break;
        } 
      } 
      switch (ag.cz.e[0]) {
        case 3:
        case 4:
        case 5:
        case 6:
        case 7:
        case 8:
          if (ag.cz.f[0] == arrayOfByte2[ag.cz.e[0]])
            ag.bc.f(); 
        case 21:
        case 22:
        case 23:
        case 24:
          if (ag.cz.f[0] == arrayOfByte2[ag.cz.e[0]]) {
            switch (ag.cz.e[0]) {
              case 3:
              case 4:
              case 6:
              case 7:
                a_(15);
                break;
              case 5:
              case 8:
              case 21:
              case 22:
                a_(16);
                break;
              case 23:
              case 24:
                a_(9);
                break;
            } 
            ag.bc.d(0);
            ag.bc.c();
          } 
          break;
        case 12:
          if (ag.cz.f[0] > 2 && ag.cz.f[0] < 6) {
            if (ag.cz.f[0] == 3)
              a_(7); 
            ag.bc.d(0);
            ag.bc.c();
          } 
          break;
        case 13:
          if (ag.cz.f[0] > 4 && ag.cz.f[0] < 8) {
            if (ag.cz.f[0] == 5)
              a_(7); 
            ag.bc.d(0);
            ag.bc.c();
          } 
          break;
        case 14:
          switch (ag.cz.f[0]) {
            case 2:
            case 4:
            case 6:
            case 8:
              a_(15);
              ag.bc.d(0);
              ag.bc.c();
              break;
          } 
          break;
        case 15:
        case 16:
          if (ag.cz.f[0] == 11) {
            a_(8);
            if (ag.cz.e[0] == 15) {
              ag.cz.p += ag.cz.y * (4 + ag.cz.W[3]) / 25;
            } else {
              ag.cz.p += ag.cz.y * (9 + ag.cz.W[4]) / 20;
            } 
            ar.b();
          } 
          break;
        case 17:
        case 18:
        case 19:
          if (ag.cz.f[0] == 11) {
            if (ag.cz.e[0] != 18) {
              ag.cz.A = ag.cz.w * ag.cz.W[ag.cz.e[0] - 12] / arrayOfByte1[ag.cz.e[0] - 17];
              if (ag.cz.A < 1)
                ag.cz.A = 1; 
              if (ag.cz.W[ag.cz.e[0] - 12] < 4) {
                ag.cz.C = 50;
              } else if (ag.cz.W[ag.cz.e[0] - 12] < 8) {
                ag.cz.C = 100;
              } else {
                ag.cz.C = 150;
              } 
            } 
            if (ag.cz.e[0] != 17) {
              ag.cz.B = ag.cz.x * ag.cz.W[ag.cz.e[0] - 12] / arrayOfByte1[ag.cz.e[0] - 17];
              if (ag.cz.B < 1)
                ag.cz.B = 1; 
              if (ag.cz.W[ag.cz.e[0] - 12] < 4) {
                ag.cz.D = 50;
                break;
              } 
              if (ag.cz.W[ag.cz.e[0] - 12] < 8) {
                ag.cz.D = 100;
                break;
              } 
              ag.cz.D = 150;
            } 
            break;
          } 
          if (ag.cz.f[0] == 4)
            a_(12); 
          break;
        case 20:
          if ((ag.cz.f[0] & 0x1) != 0) {
            a_(15);
            if (ag.cz.f[0] == 1 || ag.cz.f[0] == 5 || ag.cz.f[0] == 9) {
              ag.cz.M = 0;
            } else {
              ag.cz.M = 2;
            } 
            ag.bc.d(0);
            ag.bc.c();
          } 
          break;
        case 25:
          if ((ag.cz.f[0] & 0x1) != 0) {
            a_(9);
            ag.bc.d(0);
            ag.bc.c();
          } 
          break;
        case 26:
        case 27:
          if (ag.cz.f[0] == 8) {
            if (ag.cz.e[0] == 27)
              a_(9); 
            ag.bc.d(0);
            ag.bc.c();
          } 
          if (ag.cz.f[0] > 1 && ag.cz.f[0] < 9) {
            if (ag.cz.f[0] == 2)
              a_(13); 
            bool = false;
          } 
          break;
        case 28:
          if (ag.cz.f[0] == 22) {
            ag.bc.d(0);
            ag.bc.c();
            ag.ck = 1;
            break;
          } 
          if (ag.cz.f[0] > 3) {
            bool = false;
            ag.ck = 1;
            ag.cl = 1;
            switch (ag.cz.f[0]) {
              case 6:
                a_(13);
                break;
            } 
          } 
          break;
        case 29:
          if (ag.cz.f[0] == 22) {
            ag.bc.d(0);
            ag.bc.c();
            ag.ck = 1;
            break;
          } 
          if (ag.cz.f[0] > 6) {
            if (ag.cz.f[0] == 7)
              a_(14); 
            bool = false;
            ag.ck = 1;
            if (ag.cz.f[0] == 12 || ag.cz.f[0] == 16) {
              ag.cl = 2;
              break;
            } 
            ag.cl = 1;
          } 
          break;
        case 30:
          if (ag.cz.f[0] > 3) {
            switch (ag.cz.f[0]) {
              case 4:
                a_(11);
                break;
              case 13:
                a_(9);
                break;
            } 
            if (ag.cz.f[0] < 15) {
              bool = false;
              ag.cl = 1;
            } 
            ag.ck = 1;
            if (ag.cz.f[0] == 9 || ag.cz.f[0] == 11) {
              ag.cl = 2;
              break;
            } 
            if (ag.cz.f[0] == 15) {
              ag.bc.d(0);
              ag.bc.c();
            } 
          } 
          break;
      } 
      if (bool) {
        ag.bc.j();
        ag.bd.d();
        ag.bc.i();
        ag.bc.g();
        ar.h();
      } 
      f();
    } 
  }
  
  private void aD() {
    for (byte b = 0; b < ag.cB; b++) {
      if ((ag.cA[b]).a != 0 && (ag.cA[b]).h != 0) {
        int i = (ag.cA[b]).b.a - ag.ca.a;
        int j = (ag.cA[b]).b.b - ag.ca.b;
        int k = 2 - (ag.cA[b]).h;
        (ag.cA[b]).h = (short)((ag.cA[b]).h - 1);
        m(k, i, j);
      } 
    } 
  }
  
  private void m(int paramInt1, int paramInt2, int paramInt3) {
    b(ag.ct[7], paramInt2 - (ag.eV[paramInt1]).e, paramInt3 - (ag.eV[paramInt1]).f, (ag.eV[paramInt1]).c, (ag.eV[paramInt1]).d, paramInt2 - (ag.eV[paramInt1]).e + ag.cc.a, paramInt3 - (ag.eV[paramInt1]).f + ag.cc.b);
  }
  
  private void aE() {
    int[] arrayOfInt1 = { ag.dd - 9, 5, ag.dd - 9, ag.bY.a - 31 };
    int[] arrayOfInt2 = { ag.bY.b - 31, ag.de - 13, 5, ag.de - 13 };
    if (ag.cn < 1 && (ag.cm & 0x2) != 0)
      for (byte b = 0; b < 4; b++) {
        if ((ag.eO[ag.eP]).a[b] != 0 && ag.ct[21 + b] != null)
          b(ag.ct[7], arrayOfInt1[b], arrayOfInt2[b], ag.ct[21 + b].getWidth(), ag.ct[21 + b].getHeight(), arrayOfInt1[b] + ag.cc.a, arrayOfInt2[b] + ag.cc.b); 
      }  
  }
  
  private void aF() {
    y[] arrayOfY1;
    y[] arrayOfY2;
    y[] arrayOfY3;
    if (ag.cz.e[1] < 12) {
      arrayOfY1 = ag.cz.aC;
      arrayOfY2 = ag.cz.aE;
      arrayOfY3 = ag.eS[ag.cz.K];
    } else {
      arrayOfY1 = ag.cz.aD;
      arrayOfY2 = ag.cz.aF;
      arrayOfY3 = ag.eT[ag.cz.K];
    } 
    int i = (ag.cz.a[1]).a - ag.ca.a;
    int j = (ag.cz.a[1]).b - ag.ca.b;
    b(ag.ct[7], i - (arrayOfY1[ag.cz.L]).e, j - (arrayOfY1[ag.cz.L]).f, (arrayOfY1[ag.cz.L]).c, (arrayOfY1[ag.cz.L]).d, i - (arrayOfY1[ag.cz.L]).e + ag.cc.a, j - (arrayOfY1[ag.cz.L]).f + ag.cc.b);
    b(ag.ct[7], i - (arrayOfY2[ag.cz.L]).e, j - (arrayOfY2[ag.cz.L]).f, (arrayOfY2[ag.cz.L]).c, (arrayOfY2[ag.cz.L]).d, i - (arrayOfY2[ag.cz.L]).e + ag.cc.a, j - (arrayOfY2[ag.cz.L]).f + ag.cc.b);
    b(ag.ct[7], i - (arrayOfY2[ag.cz.L]).e + (arrayOfY2[ag.cz.L]).c / 2 - 13, j - (arrayOfY2[ag.cz.L]).f + (arrayOfY2[ag.cz.L]).d - 5, 27, 11, i - (arrayOfY2[ag.cz.L]).e + ag.cc.a + (arrayOfY2[ag.cz.L]).c / 2 - 13, j - (arrayOfY2[ag.cz.L]).f + ag.cc.b + (arrayOfY2[ag.cz.L]).d - 5);
    b(ag.ct[7], i - (arrayOfY3[ag.cz.L]).e, j - (arrayOfY3[ag.cz.L]).f, (arrayOfY3[ag.cz.L]).c, (arrayOfY3[ag.cz.L]).d, i - (arrayOfY3[ag.cz.L]).e + ag.cc.a, j - (arrayOfY3[ag.cz.L]).f + ag.cc.b);
    if (ag.ek == 1 || ag.el == 1) {
      int k = (ag.bN - 1) % 3;
      b(ag.ct[7], i - (ag.eQ[k]).e, j - (ag.eQ[k]).f - 18, 40, 50, i - (ag.eQ[k]).e + ag.cc.a, j - (ag.eQ[k]).f + ag.cc.b - 18);
      ag.el = 0;
    } 
    if (ag.cz.e[1] < 12) {
      int k;
      if (ag.cz.L > 11 && ag.cz.L < 36 && ((k = ag.cz.L - 12) & 0x1) != 0) {
        k &= 0xFFFE;
        m(-1, k % 6 >> 1);
      } 
    } else {
      int k = -1;
      switch (ag.cz.e[1]) {
        case 12:
          if (ag.cz.f[1] > 2 && ag.cz.f[1] < 6)
            k = 1; 
          break;
        case 13:
          if (ag.cz.f[1] > 4 && ag.cz.f[1] < 8)
            k = 1; 
          break;
        case 14:
          switch (ag.cz.f[1]) {
            case 2:
            case 4:
            case 6:
            case 8:
              k = 1;
              break;
          } 
          break;
        case 20:
          if ((ag.cz.f[1] & 0x1) != 0)
            k = ag.cz.M; 
          break;
        case 21:
          if (ag.cz.f[1] == 5)
            k = 2; 
          break;
        case 22:
          if (ag.cz.f[1] == 6)
            k = 2; 
          break;
        case 25:
          if ((ag.cz.f[1] & 0x1) != 0)
            k = 2; 
          break;
      } 
      if (k > -1)
        m(-1, k); 
    } 
    if (ag.cz.T != 0) {
      b(ag.ct[7], i - (ag.eY[ag.cz.U]).e, j - (ag.eY[ag.cz.U]).f, (ag.eY[ag.cz.U]).c, (ag.eY[ag.cz.U]).d, i - (ag.eY[ag.cz.U]).e + ag.cc.a, j - (ag.eY[ag.cz.U]).f + ag.cc.b);
      ag.cz.U++;
      if (ag.cz.U > 5)
        ag.cz.T = 0; 
    } 
    if (ag.cz.O != 0 && ag.cz.P > -1) {
      i = ag.cz.Q.a - ag.ca.a;
      j = ag.cz.Q.b - ag.ca.b;
      int k = ag.cz.P;
      m(k, i, j);
    } 
  }
  
  private void m(int paramInt1, int paramInt2) {
    h h;
    int i;
    if (paramInt1 > -1) {
      h = (ag.ex[paramInt1]).a[1];
      if ((ag.ex[paramInt1]).f[1] == 19) {
        i = (ag.ex[paramInt1]).e[1] + ((ag.ex[paramInt1]).g[1] >> 1 << 1) & 0x7;
      } else {
        i = (ag.ex[paramInt1]).e[1];
      } 
    } else {
      h = ag.cz.a[1];
      if (ag.cz.e[1] == 25) {
        i = ag.cz.d[1] + (ag.cz.f[1] >> 1 << 1) & 0x7;
      } else {
        i = ag.cz.d[1];
      } 
    } 
    int j = (i >> 1) * 6 + (paramInt2 << 1);
    int k = h.a - ag.ca.a;
    int m = h.b - ag.ca.b;
    for (byte b = 0; b < 2; b++) {
      b(ag.ct[7], k - (ag.eU[j]).e, m - (ag.eU[j]).f, (ag.eU[j]).c, (ag.eU[j]).d, k - (ag.eU[j]).e + ag.cc.a, m - (ag.eU[j]).f + ag.cc.b);
      j++;
    } 
  }
  
  private void aG() {
    for (byte b = 0; b < ag.ez; b++) {
      short s1 = ag.ey[b];
      (ag.ex[s1]).f[0] = Math.min((ag.ex[s1]).f[0], ((ag.ex[s1]).B[(ag.ex[s1]).e[0]]).length - 1);
      short s2 = (ag.ex[s1]).B[(ag.ex[s1]).e[1]][(ag.ex[s1]).f[1]][(ag.ex[s1]).g[1]];
      int i = ((ag.ex[s1]).a[1]).a - ag.ca.a;
      int j = ((ag.ex[s1]).a[1]).b - ag.ca.b;
      if ((ag.ex[s1]).h > 200) {
        if (s2 < 180)
          if ((ag.ex[s1]).h == 203) {
            b(ag.ct[7], i - ((ag.ex[s1]).D[s2]).e + ae.az[ae.aT[(ag.ex[s1]).e[1]]][0], j - ((ag.ex[s1]).D[s2]).f + ae.az[ae.aT[(ag.ex[s1]).e[1]]][1], ((ag.ex[s1]).D[s2]).c + ae.az[ae.aT[(ag.ex[s1]).e[1]]][2], ((ag.ex[s1]).D[s2]).d + ae.az[ae.aT[(ag.ex[s1]).e[1]]][3], i - ((ag.ex[s1]).D[s2]).e + ag.cc.a + ae.az[ae.aT[(ag.ex[s1]).e[1]]][0], j - ((ag.ex[s1]).D[s2]).f + ag.cc.b + ae.az[ae.aT[(ag.ex[s1]).e[1]]][1]);
          } else {
            b(ag.ct[7], i - ((ag.ex[s1]).D[s2]).e, j - ((ag.ex[s1]).D[s2]).f, ((ag.ex[s1]).D[s2]).c, ((ag.ex[s1]).D[s2]).d, i - ((ag.ex[s1]).D[s2]).e + ag.cc.a, j - ((ag.ex[s1]).D[s2]).f + ag.cc.b);
          }  
      } else {
        y[] arrayOfY1;
        y[] arrayOfY2;
        y[] arrayOfY3;
        if ((ag.ex[s1]).f[1] < 6) {
          arrayOfY2 = ag.et[3];
          arrayOfY1 = ag.et[4];
          arrayOfY3 = ag.et[5];
        } else {
          arrayOfY2 = ag.et[6];
          arrayOfY1 = ag.et[7];
          arrayOfY3 = ag.et[8];
        } 
        if (s2 < 180) {
          b(ag.ct[7], i - (arrayOfY2[s2]).e + (arrayOfY2[s2]).c / 2 - 13, j - (arrayOfY2[s2]).f + (arrayOfY2[s2]).d - 4, 27, 11, i - (arrayOfY2[s2]).e + ag.cc.a + (arrayOfY2[s2]).c / 2 - 13, j - (arrayOfY2[s2]).f + ag.cc.b + (arrayOfY2[s2]).d - 5);
          if (ag.em == 1 || ag.en == 1) {
            int k = (ag.bN - 1) % 3;
            b(ag.ct[7], i - (ag.eQ[k]).e, j - (ag.eQ[k]).f - 18, 40, 50, i - (ag.eQ[k]).e + ag.cc.a, j - (ag.eQ[k]).f + ag.cc.b - 18);
            ag.en = 0;
          } 
        } else {
          b(ag.ct[7], i - (arrayOfY2[20]).e + (arrayOfY2[20]).c / 2 - 9, j - (arrayOfY2[20]).f + (arrayOfY2[20]).d - 4, 18, 7, i - (arrayOfY2[20]).e + ag.cc.a + (arrayOfY2[20]).c / 2 - 9, j - (arrayOfY2[20]).f + ag.cc.b + (arrayOfY2[20]).d - 4);
        } 
        if (s2 < 180) {
          b(ag.ct[7], i - (arrayOfY1[s2]).e, j - (arrayOfY1[s2]).f, (arrayOfY1[s2]).c, (arrayOfY1[s2]).d, i - (arrayOfY1[s2]).e + ag.cc.a, j - (arrayOfY1[s2]).f + ag.cc.b);
          b(ag.ct[7], i - (arrayOfY2[s2]).e, j - (arrayOfY2[s2]).f, (arrayOfY2[s2]).c, (arrayOfY2[s2]).d, i - (arrayOfY2[s2]).e + ag.cc.a, j - (arrayOfY2[s2]).f + ag.cc.b);
          b(ag.ct[7], i - (arrayOfY3[s2]).e, j - (arrayOfY3[s2]).f, (arrayOfY3[s2]).c, (arrayOfY3[s2]).d, i - (arrayOfY3[s2]).e + ag.cc.a, j - (arrayOfY3[s2]).f + ag.cc.b);
        } 
        O(s1);
        if ((ag.ex[s1]).y > -1 && (ag.ex[s1]).y < 100)
          m(s1, (ag.ex[s1]).y); 
      } 
      if ((ag.ex[s1]).w != 0) {
        b(ag.ct[7], i - (ag.fe[(ag.ex[s1]).x]).e, j - (ag.fe[(ag.ex[s1]).x]).f, (ag.fe[(ag.ex[s1]).x]).c, (ag.fe[(ag.ex[s1]).x]).d, i - (ag.fe[(ag.ex[s1]).x]).e + ag.cc.a, j - (ag.fe[(ag.ex[s1]).x]).f + ag.cc.b);
        (ag.ex[s1]).x = (byte)((ag.ex[s1]).x + 1);
        if ((ag.ex[s1]).x > 5)
          (ag.ex[s1]).w = 0; 
      } 
      if ((ag.ex[s1]).t != 0 && (ag.ex[s1]).u > -1) {
        i = (ag.ex[s1]).v.a - ag.ca.a;
        j = (ag.ex[s1]).v.b - ag.ca.b;
        int k = (ag.ex[s1]).u + ((ag.ex[s1]).t - 1 << 1);
        m(k, i, j);
      } 
    } 
  }
  
  private static y[] a(y[] paramArrayOfy, int paramInt) {
    int i;
    y[] arrayOfY = new y[(i = paramArrayOfy.length) - paramInt];
    for (byte b = 0; b < arrayOfY.length; b++)
      arrayOfY[b] = paramArrayOfy[paramInt + b]; 
    return arrayOfY;
  }
  
  private void O(int paramInt) {
    h h = (ag.ex[paramInt]).a[1];
    ag.fk = 0;
    switch ((ag.ex[paramInt]).f[1]) {
      case 6:
        if ((ag.ex[paramInt]).g[1] > 2 && (ag.ex[paramInt]).g[1] < 6) {
          ag.fk = 1;
          ag.fj = a(ag.eW, (ag.ex[paramInt]).e[1] + ((ag.ex[paramInt]).g[1] & 0x1));
        } 
        break;
      case 7:
        if ((ag.ex[paramInt]).g[1] > 4 && (ag.ex[paramInt]).g[1] < 8) {
          ag.fk = 1;
          ag.fj = a(ag.eW, (ag.ex[paramInt]).e[1] + ((ag.ex[paramInt]).g[1] & 0x1));
        } 
        break;
      case 8:
        if ((ag.ex[paramInt]).g[1] > 0 && (ag.ex[paramInt]).g[1] < 9) {
          ag.fk = 1;
          ag.fj = a(ag.eW, (ag.ex[paramInt]).e[1] + ((ag.ex[paramInt]).g[1] & 0x1));
        } 
        break;
      case 9:
      case 10:
        if ((ag.ex[paramInt]).g[1] > 3) {
          ag.fk = 1;
          ag.fj = a(ag.fb, (ag.ex[paramInt]).g[1] - 4);
        } 
        break;
      case 11:
      case 12:
      case 13:
        if ((ag.ex[paramInt]).g[1] > 3 && (ag.ex[paramInt]).g[1] < 10) {
          ag.fk = 3;
          ag.fj = a(ag.fb, (ag.ex[paramInt]).g[1] - 4);
        } 
        break;
      case 15:
      case 18:
        if ((ag.ex[paramInt]).g[1] == 5 || (ag.ex[paramInt]).g[1] == 6) {
          ag.fk = 1;
          ag.fj = a(ag.fb, (ag.ex[paramInt]).g[1] - 5);
        } 
        break;
      case 16:
        if ((ag.ex[paramInt]).g[1] > 1 && (ag.ex[paramInt]).g[1] < 6) {
          ag.fk = 1;
          ag.fj = a(ag.eW, (ag.ex[paramInt]).g[1] & 0x1);
        } 
        break;
      case 17:
        if ((ag.ex[paramInt]).g[1] == 5 || (ag.ex[paramInt]).g[1] == 6) {
          ag.fk = 1;
          ag.fj = a(ag.eW, (ag.ex[paramInt]).g[1] - 5);
        } 
        break;
      case 21:
        if ((ag.ex[paramInt]).g[1] == 9) {
          ag.fk = 3;
          ag.fj = a(ag.fb, 1);
          h.a = (short)(h.a + ae.aA[(ag.ex[paramInt]).e[1] >> 1]);
          h.b = (short)(h.b + ae.aB[(ag.ex[paramInt]).e[1] >> 1]);
        } 
      case 20:
        if ((ag.ex[paramInt]).g[1] > 1 && (ag.ex[paramInt]).g[1] < 9) {
          ag.fk = 3;
          ag.fj = a(ag.fb, (ag.ex[paramInt]).g[1] - 2 + ((ag.ex[paramInt]).e[1] >> 1) * 7);
        } 
        break;
    } 
    if (ag.fk != 0) {
      int i = h.a - ag.ca.a;
      int j = h.b - ag.ca.b;
      ag.fk = 0;
      b(ag.ct[7], i - (ag.fj[0]).e - 8, j - (ag.fj[0]).f - 8, (ag.fj[0]).c + 16, (ag.fj[0]).d + 16, i - (ag.fj[0]).e - 8 + ag.cc.a, j - (ag.fj[0]).f - 8 + ag.cc.b);
    } 
  }
  
  private void aH() {
    for (byte b = 0; b < ag.cD; b++) {
      if ((ag.cC[b]).a != 0)
        b(ag.ct[7], (ag.cC[b]).b.a - ag.ca.a - ((ag.cC[b]).e >> 1), (ag.cC[b]).b.b - ag.ca.b - ((ag.cC[b]).f >> 1), (ag.cC[b]).e, (ag.cC[b]).f, (ag.cC[b]).b.a - ag.ca.a - ((ag.cC[b]).e >> 1) + ag.cc.a, (ag.cC[b]).b.b - ag.ca.b - ((ag.cC[b]).f >> 1) + ag.cc.b); 
    } 
  }
  
  private void aI() {
    h h;
    (h = new h()).a = (ag.cz.a[1]).a;
    h.b = (ag.cz.a[1]).b;
    ag.fh = 0;
    switch (ag.cz.e[1]) {
      case 2:
        ag.fh = 1;
        ag.fj = a(ag.eW, ag.cz.d[1] + (ag.cz.f[1] & 0x1));
        break;
      case 12:
        if (ag.cz.f[1] > 2 && ag.cz.f[1] < 6) {
          ag.fh = 1;
          ag.fj = a(ag.eW, ag.cz.d[1] + (ag.cz.f[1] & 0x1));
        } 
        break;
      case 13:
        if (ag.cz.f[1] > 4 && ag.cz.f[1] < 8) {
          ag.fh = 1;
          ag.fj = a(ag.eW, ag.cz.d[1] + (ag.cz.f[1] & 0x1));
        } 
        break;
      case 14:
        if (ag.cz.f[1] > 0 && ag.cz.f[1] < 9) {
          ag.fh = 1;
          ag.fj = a(ag.eW, ag.cz.d[1] + (ag.cz.f[1] & 0x1));
        } 
        break;
      case 15:
      case 16:
        if (ag.cz.f[1] > 3) {
          ag.fh = 1;
          ag.fj = a(ag.eY, ag.cz.f[1] - 4);
        } 
        break;
      case 17:
      case 18:
      case 19:
        if (ag.cz.f[1] > 3 && ag.cz.f[1] < 10) {
          ag.fh = 3;
          ag.fj = a(ag.eY, ag.cz.f[1] - 4);
        } 
        break;
      case 21:
      case 24:
        if (ag.cz.f[1] == 5 || ag.cz.f[1] == 6) {
          ag.fh = 1;
          ag.fj = a(ag.eY, ag.cz.f[1] - 5);
        } 
        break;
      case 22:
        if (ag.cz.f[1] > 1 && ag.cz.f[1] < 6) {
          ag.fh = 1;
          ag.fj = a(ag.eW, ag.cz.f[1] & 0x1);
        } 
        break;
      case 23:
        if (ag.cz.f[1] == 5 || ag.cz.f[1] == 6) {
          ag.fh = 1;
          ag.fj = a(ag.eW, ag.cz.f[1] - 5);
        } 
        break;
      case 27:
        if (ag.cz.f[1] == 9) {
          ag.fh = 3;
          ag.fj = a(ag.eY, 1);
          h.a = (short)(h.a + ae.aA[ag.cz.d[1] >> 1]);
          h.b = (short)(h.b + ae.aB[ag.cz.d[1] >> 1]);
        } 
      case 26:
        if (ag.cz.f[1] > 1 && ag.cz.f[1] < 9) {
          ag.fh = 3;
          ag.fj = a(ag.eY, ag.cz.f[1] - 2 + (ag.cz.d[1] >> 1) * 7);
        } 
        break;
    } 
    if (ag.fh != 0) {
      int i = h.a - ag.ca.a;
      int j = h.b - ag.ca.b;
      for (byte b = 0; b < ag.fg; b++)
        b(ag.ct[7], i - (ag.fj[b]).e - 8, j - (ag.fj[b]).f - 8, (ag.fj[b]).c + 16, (ag.fj[b]).d + 16, i - (ag.fj[b]).e + ag.cc.a - 8, j - (ag.fj[b]).f + ag.cc.b - 8); 
      ag.fh = 0;
      ag.fg = 1;
    } 
  }
  
  private void aJ() {
    int i = (g.b() + g.c()) * ag.dT.c.length() + 3;
    b(ag.ct[7], ag.bY.a - i - 7, 0, i + 7, 40, ag.bY.a - i + ag.cc.a - 7, ag.cc.b);
    a(ag.ca.a + ag.bY.a - i - 7, ag.ca.b, i + 7, 40);
    ag.dT.b = (short)(ag.dT.b - 1);
    if (ag.dT.b < 1)
      ag.dT.a = 0; 
  }
  
  private void aK() {
    if (ag.dT.a != 0) {
      aJ();
    } else {
      int i = ag.D(ag.cz.I) * 10 + 1;
      b(ag.ct[7], ag.bY.a - 3 - i - 7, 1, i + 7, 29, ag.bY.a - 3 - i + ag.cc.a - 7, 1 + ag.cc.b);
      a(ag.ca.a + ag.bY.a - 3 - i - 7, ag.ca.b + 1, i + 7, 29);
      if (ag.cz.H > ag.cz.I)
        ag.cz.I++; 
    } 
    b(ag.ct[7], 0, 0, 60, 20, ag.cc.a, ag.cc.b);
    a(ag.ca.a, ag.ca.b, 60, 20);
  }
  
  private void aL() {
    byte[] arrayOfByte1 = { 
        2, 10, 100, 2, 2, 2, 2, 2, 2, 2, 
        2, 2, 100, 100 };
    short[] arrayOfShort = { 63, 60 };
    byte[] arrayOfByte2 = { 1, 1, 1, 2, 2, 2, 3, 3, 3 };
    byte[] arrayOfByte3 = { 30, 60, 100, 30, 60, 100, 30, 60, 100 };
    if (ag.dU.a != 0) {
      if (ag.dU.a <= 9 || ag.dU.b != 0) {
        int i = ag.dU.c.a - (ag.dU.h[ag.dU.f]).e - ag.ca.a;
        int j = ag.dU.c.b - (ag.dU.h[ag.dU.f]).f - ag.ca.b;
        short s1 = (ag.dU.h[ag.dU.f]).c;
        short s2 = (ag.dU.h[ag.dU.f]).d;
        if (ag.dU.a < 0)
          if (ag.dU.a == -1) {
            i -= 10;
            j -= 6;
            s1 = (short)(s1 + 20);
            s2 = (short)(s2 + 11);
            if (ag.dU.b == 1 || ag.dU.b == 4 || ag.dU.b == 7)
              ag.bc.d(ag.dU.a); 
          } else if (ag.dU.b == 1) {
            ag.bc.d(ag.dU.a);
          }  
        b(ag.ct[7], i, j, s1, s2, i + ag.cc.a, j + ag.cc.b);
      } 
      ag.dU.b = (short)(ag.dU.b + 1);
      if (ag.dU.a > 9 && ag.dU.b > 4) {
        a_(9);
        ag.dU.g = null;
        ag.dU.h = K(arrayOfShort[ag.dU.a - 10]);
        ag.dU.c.a = (short)(ag.dU.c.a + ae.aA[ag.dU.d]);
        ag.dU.c.b = (short)(ag.dU.c.b + ae.aB[ag.dU.d]);
        ag.dU.a = (short)(ag.dU.a - 12);
        ag.dU.b = 0;
      } 
      if (ag.dU.b >= arrayOfByte1[ag.dU.a + 2]) {
        if (ag.dU.a > 0) {
          if ((arrayOfByte2[ag.dU.a - 1] & 0x1) != 0)
            ag.cz.p += ag.cz.y * arrayOfByte3[ag.dU.a - 1] / 100; 
          if ((arrayOfByte2[ag.dU.a - 1] & 0x2) != 0)
            ag.cz.r += ag.cz.z * arrayOfByte3[ag.dU.a - 1] / 100; 
          ar.b();
        } 
        k(0, 0);
        ag.dU.a = 0;
        ag.dU.g = null;
        ag.dU.h = null;
      } 
    } 
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\c.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */