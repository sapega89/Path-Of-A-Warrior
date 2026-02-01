import javax.microedition.lcdui.Image;

class as extends ag implements s {
  public static m a = null;
  
  public static v b;
  
  public static boolean d = true;
  
  public static boolean e = false;
  
  public static long f;
  
  public static int g = -1;
  
  public static int h;
  
  public static int i;
  
  public static int j = 0;
  
  public static int k;
  
  public static String l;
  
  public static String m;
  
  public static boolean n = false;
  
  public static boolean o;
  
  public static Image p;
  
  public static Image q;
  
  public static Image r;
  
  public static Image s;
  
  public static int gn = (int)(System.currentTimeMillis() / 10000L);
  
  public static int go;
  
  public static int gp;
  
  public static int gq;
  
  public static int gr;
  
  public static boolean gs = false;
  
  public static int gt = -1;
  
  public static boolean gu = false;
  
  public static short[] gv = null;
  
  public static z[] gw = new z[100];
  
  public static short[] gx = null;
  
  public static int gy;
  
  public static z[] gz = new z[20];
  
  public static int[] gA = new int[20];
  
  public static int[] gB = new int[20];
  
  public static String[] gC = new String[5];
  
  public static short gD;
  
  public static boolean gE = false;
  
  public static final int[][] gF = new int[][] { { 
        116, 121, 126, 101, 106, 111, 131, 136, 156, 161, 
        181, 146, 151, 0, 0, 0, 0, 0, 0, 0 }, { 
        331, 324, 322, 301, 308, 302, 341, 350, 357, 363, 
        370, 380, 415, 0, 0, 0, 0, 0, 0, 0 }, { 
        501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 
        511, 512, 513, 514, 515, 516, 517, 518, 0, 0 } };
  
  public static final byte[] gG = new byte[] { 
      3, 4, 5, 9, 10, 11, 12, 13, 6, 7, 
      8, 14, 15, 16, 17, 18, 19, 20, 21 };
  
  public static boolean gH = false;
  
  public static String[] gI = new String[8];
  
  public static int gJ;
  
  public static int gK;
  
  public static int gL;
  
  public static int gM;
  
  public static int gN;
  
  public static short gO;
  
  public static short gP;
  
  public static short gQ;
  
  public static short gR;
  
  public static byte gS;
  
  public static byte gT;
  
  public static short gU;
  
  public static short gV;
  
  public static short gW;
  
  public static short gX;
  
  public static short gY;
  
  public static short gZ;
  
  public static short ha;
  
  public static short hb;
  
  public static short hc;
  
  public static short hd;
  
  public static short he;
  
  public static short hf;
  
  public static short hg;
  
  public static short hh;
  
  public static int hi;
  
  public static int hj;
  
  public static int hk;
  
  public static String[] hl = new String[12];
  
  public static String[] hm = new String[50];
  
  public static String hn = "";
  
  public static int ho;
  
  public static int hp;
  
  public static boolean hq = false;
  
  public static short hr;
  
  public static short hs;
  
  public static short[] ht = new short[16];
  
  public static int[] hu = new int[16];
  
  public static int[] hv = new int[16];
  
  public static final String[] hw = new String[] { "Normal Items", "Special Items", "Rare Items" };
  
  public as() {
    super(ag.bs);
    if (gv == null)
      gv = new short[25]; 
    if (gx == null)
      gx = new short[100]; 
  }
  
  final void g() {
    o = true;
    if (m.b()) {
      n = false;
      a.d();
      ag.cS.d(2);
      gt = 2;
      return;
    } 
    h();
  }
  
  final void h() {
    ag.bp = true;
    ag.ai();
    hn = "Registration";
    ho = 13;
    hp = 18;
    k = 1;
    ag.bP = 0;
    aJ();
    ag.bV = 11;
    l = "";
    m = "";
    ag.bz = null;
    ag.bz = new at("", 12, 10);
    k();
    aJ();
  }
  
  public final void i() {
    if (g != -1)
      d(g); 
    if (ag.cS.q) {
      ag.cS.q = false;
      int i = gt;
      gt = -1;
      short s1 = ag.cS.k;
      switch (i) {
        case 3:
          ba();
          aJ();
          break;
        case 2:
          if (s1 == 0) {
            ag.bp = true;
            ag.ai();
            k();
            aE();
            aI();
            c(512);
            break;
          } 
          ba();
          aJ();
          break;
        case 7:
          if (ht[15] > 0) {
            c(516);
            break;
          } 
          aS();
          break;
        case 8:
          aX();
          break;
        case 9:
          if (s1 == 0) {
            boolean bool = false;
            if (ht[14] == 1) {
              for (byte b = 0; b < 9; b++) {
                if ((ag.cz.X[b]).a > 0) {
                  bool = true;
                  break;
                } 
              } 
              if (bool) {
                ag.cS.d(33);
                break;
              } 
            } 
            hr = 0;
            if (ht[14] == 0) {
              c(256);
              break;
            } 
            c(262);
          } 
          break;
        case 10:
          if (s1 == 0) {
            if (ag.fK[16] < 25) {
              ht[7] = 0;
              hr = 0;
              c(788);
              break;
            } 
            ag.cS.d(12);
            gt = 11;
          } 
          break;
        case 11:
          if (s1 == 0) {
            ht[7] = 1;
            hr = 0;
            c(788);
          } 
          break;
        case 14:
          if (s1 == 0) {
            hr = 0;
            c(866);
            hq = true;
          } 
          break;
      } 
    } 
    if (e)
      m(); 
  }
  
  static void b(int paramInt) {
    byte b = 0;
    switch (paramInt) {
      case -1:
        b = 21;
        break;
      case -2:
        b = 22;
        break;
      case -4:
        b = 23;
        break;
      case -12:
        b = 24;
        break;
      case -13:
        b = 25;
        break;
      case -15:
        b = 26;
        break;
      case -16:
        b = 27;
        break;
      case -18:
        b = 28;
        break;
      case -20:
        b = 29;
        break;
      case -22:
        b = 30;
        break;
      case -23:
        b = 31;
        break;
      case -26:
        b = 7;
        gt = 3;
        break;
      case -11:
        b = (gS > 0) ? 10 : 8;
        break;
      case -49:
        b = 54;
        break;
      default:
        b = -1;
        break;
    } 
    if (b != -1)
      ag.cS.d(b); 
  }
  
  public final void j() {
    ag.cS.b(96);
    int i = ag.de - 20 - 10;
    int j = p.getWidth();
    int k = p.getHeight();
    ag.a((ag.bJ - j) / 2, i, j, k, p, 0, 0);
    ag.a((ag.bJ - j) / 2, i, j * ag.bN % 6 / 5, k, q, 0, 0);
    x.a(ag.bu);
    x.a("Connecting...", ag.bJ / 2, i + 50, 1);
  }
  
  public final void k() {
    try {
      if (p == null)
        p = Image.createImage("/netLoading0.png"); 
      if (q == null)
        q = Image.createImage("/netLoading1.png"); 
      if (r == null)
        r = Image.createImage("/ui_arrow2.png"); 
      if (s == null)
        s = Image.createImage("/ui_level.png"); 
    } catch (Exception exception) {}
    l();
  }
  
  public static void l() {
    if (b == null) {
      b = new v();
      b.setPriority(5);
      b.start();
    } 
  }
  
  public final void f() {
    n();
  }
  
  public final void c(int paramInt) {
    gr = 0;
    ag.v();
    gu = true;
    g = paramInt;
  }
  
  public final void d(int paramInt) {
    g = -1;
    gp = 0;
    if (!v.h) {
      gp = paramInt;
      gq = 530;
    } else {
      gq = paramInt;
    } 
    f = System.currentTimeMillis();
    e = false;
    e(gq);
    aJ();
    e = true;
  }
  
  public final void m() {
    if (gs) {
      if (!gH) {
        ag.w();
        e = false;
        gu = false;
        aJ();
      } 
    } else if (v.m && !gH && (ag.ch == -7 || System.currentTimeMillis() > f + 30000L)) {
      gr = -1;
      if (b != null) {
        b.a();
        bi();
        ag.R();
      } 
      gu = false;
      a(gq + 1, gr, (ab)null);
      aJ();
    } 
    if (gr == 1 && gq == 530 && gp != 530) {
      gq = gp;
      c(gq);
    } 
  }
  
  public final void e(int paramInt) {
    gq = paramInt;
    if (!v.h) {
      if (b == null)
        l(); 
      v.a(this);
      b.a(ag.bk, ag.bl);
    } else {
      n();
    } 
    gs = false;
  }
  
  public final synchronized void n() {
    byte b1;
    byte b;
    byte b2;
    byte b3;
    byte b4;
    byte b5;
    byte b6;
    byte b7;
    gr = 0;
    b.a(gq);
    switch (gq) {
      case 530:
        v.b(m, 12);
        v.b(l, 16);
        v.b("1501", 4);
        v.b(gn);
        go = (int)(System.currentTimeMillis() / 10000L);
        v.b(go);
        break;
      case 516:
      
      case 256:
        v.b(ag.cz.F);
        v.b(ag.cz.G);
        v.a((short)ag.cz.l);
        v.a((byte)ag.cz.aB);
        v.a((byte)(ag.g((ag.cz.X[0]).a) ^ 0x1));
        v.a((short)ag.cz.m);
        v.a((short)ag.cz.n);
        v.a((short)ag.cz.o);
        v.a((short)ag.cz.q);
        v.a((short)ag.cz.J);
        ag.O();
        v.a((short)ag.cz.s);
        v.a((short)ag.cz.t);
        v.a((short)ag.cz.u);
        v.a((short)ag.cz.v);
        for (b1 = 0; b1 < 8; b1++)
          v.b((int)ag.dy[b1]); 
        b = 0;
        for (b2 = 0; b2 < ag.cz.W.length; b2++) {
          if (ag.cz.W[b2] > 0)
            b = (byte)(b + 1); 
        } 
        v.a(b);
        for (b3 = 0; b3 < ag.cz.W.length; b3++) {
          if (ag.cz.W[b3] > 0) {
            v.a(gG[b3]);
            v.a((byte)ag.cz.W[b3]);
            boolean bool = false;
            for (byte b8 = 0; b8 < 4; b8++) {
              if (ag.cz.V[b8] - 12 == b3) {
                bool = true;
                break;
              } 
            } 
            v.a(bool);
          } 
        } 
        v.b(ag.cz.k, 8);
        v.a(!(ag.cz.S == 0));
        v.a((byte)(ag.fo & 0xFF));
        for (b4 = 0; b4 < ag.fo; b4++) {
          v.a((byte)(ag.fn[0][b4] & 0xFF));
          v.a((byte)(ag.fn[1][b4] & 0xFF));
        } 
        v.b((int)(ag.dw & 0xFFFFFFFFL));
        v.b((int)(ag.dw >> 32L & 0xFFFFFFFFL));
        v.a(ag.cq);
        for (b5 = 0; b5 < 22; b5++)
          v.a((byte)(ag.cz.g[b5] & 0xFF)); 
        v.a((byte)(ag.cz.h & 0xFF));
        v.a((byte)(ag.cz.i & 0xFF));
        v.b(ag.ed);
        break;
      case 768:
        v.b(ag.cz.E);
        e.m();
        v.a(b6 = (byte)ag.fK[16]);
        for (b7 = 0; b7 < 25; b7++) {
          if ((ag.cz.Y[b7]).a > 0) {
            v.a((ag.cz.Y[b7]).a);
            gv[b7] = (short)(b7 + 1);
            v.a(gv[b7]);
            v.a((ag.cz.Y[b7]).f);
            v.a((ag.cz.Y[b7]).b);
            v.a((ag.cz.Y[b7]).c);
            v.a((ag.cz.Y[b7]).d);
            v.a((ag.cz.Y[b7]).e);
          } 
        } 
        break;
      case 832:
        v.a((byte)(ht[15] ^ 0x1));
        v.b(hv[14]);
        break;
      case 816:
        v.a((byte)ht[7]);
        v.a((short)hj);
        break;
      case 784:
        v.a((byte)(gP + 1));
      case 786:
        v.a((byte)(gP + 1));
        v.a((byte)(gQ + 1));
        v.a((byte)gR);
      case 788:
        v.b(gA[ag.fK[18]]);
      case 800:
        v.a((byte)ht[7]);
        v.a((short)hj);
        v.b(hv[14]);
        break;
      case 802:
        v.a((byte)(gP + 1));
        v.a((byte)(gQ + 1));
      case 866:
        v.b(gA[hk]);
        v.a((byte)((ag.fK[16] < 25) ? 0 : 1));
        break;
    } 
    b.b();
  }
  
  public final void o() {
    v.h = false;
    if (b != null) {
      b.a();
      bi();
    } 
    if (ag.bV == 11) {
      gt = 3;
      ag.cS.d(29);
    } 
    gu = false;
    e = false;
    ag.f(300);
  }
  
  public final void e() {
    if (b != null) {
      b.a();
      bi();
    } 
    gs = true;
  }
  
  public final void a(ab paramab) {
    gH = true;
    v.m = false;
    short s1 = paramab.b();
    byte b = paramab.a();
    h = s1;
    if (b == 1) {
      byte b1;
      byte b2;
      byte b3;
      byte b4;
      byte b5;
      byte b6;
      int i;
      switch (s1) {
        case 531:
          gn = go;
          ar();
          paramab.a();
          paramab.a();
          if (((b6 = paramab.a()) == 0 || b6 == 2) && n) {
            m.c();
            if (b6 == 0) {
              ag.cS.d(48);
            } else if (b6 == 2) {
              ag.cS.d(44);
            } 
            gt = 2;
            n = false;
          } 
          break;
        case 513:
          ht[15] = (short)paramab.a();
          ht[14] = (short)paramab.a();
          ht[13] = (short)paramab.a();
          paramab.a();
          paramab.c();
          paramab.c();
          paramab.c();
          paramab.c();
          paramab.c();
          ht[4] = (short)paramab.a();
          ht[5] = (short)paramab.a();
          aR();
          aJ();
          break;
        case 517:
          ag.cS.m = ag.e(ag.f(paramab.a(16)));
          ag.cS.n = ag.e(ag.f(paramab.a(16)));
          ag.cS.o = ag.e(ag.f(paramab.a(16)));
          ag.cS.p = ag.e(ag.f(paramab.a(16)));
          ag.cS.d(53);
          gt = 7;
          if (paramab.a() == 1) {
            ht[15] = (short)(ht[15] + 1);
            break;
          } 
          ht[15] = 0;
          break;
        case 519:
          for (b1 = 0; b1 < 20; b1++) {
            if (gz[b1] == null)
              gz[b1] = new z(); 
            gz[b1].a();
            gB[b1] = 0;
          } 
          b5 = paramab.a();
          for (b1 = 0; b1 < b5; b1++) {
            (gz[b1]).a = paramab.b();
            (gz[b1]).f = paramab.a();
            gB[b1] = paramab.c();
          } 
          gD = 0;
          aT();
          break;
        case 261:
          ag.fR = (short)(ag.fR - 1);
          if (ag.fR == 0) {
            ar();
            if (hv[15] == 0 && hv[14] == 0) {
              if (d) {
                ag.cS.d(20);
              } else {
                ag.cS.q = true;
              } 
            } else {
              ag.cS.m = "" + hv[14];
              ag.cS.n = "" + hv[15];
              ag.cS.o = "" + hv[13];
              ag.cS.d(41);
            } 
            gt = 8;
            break;
          } 
          ag.fR = 0;
          aV();
          break;
        case 263:
          ag.cz.F = paramab.c();
          ag.cz.G = paramab.c();
          ag.cz.l = paramab.b() & 0xFF;
          ag.cz.aB = paramab.a();
          ag.cz.K = paramab.a();
          ag.cz.m = paramab.b();
          ag.cz.n = paramab.b();
          ag.cz.o = paramab.b();
          ag.cz.q = paramab.b();
          ag.cz.J = paramab.b();
          for (b1 = 0; b1 < ag.cz.W.length; b1++)
            ag.cz.W[b1] = 0; 
          for (b1 = 0; b1 < ag.cz.V.length; b1++)
            ag.cz.V[b1] = 0; 
          b4 = paramab.a();
          b1 = 0;
          b2 = 0;
          while (b1 < b4) {
            byte b8 = paramab.a();
            byte b7;
            for (b7 = 0; b7 < 19 && gG[b7] != b8; b7++);
            ag.cz.W[b7] = paramab.a();
            if ((b8 = paramab.a()) == 1)
              ag.cz.V[b2++] = b7 + 12; 
            b1++;
          } 
          for (b1 = 0; b1 < 8; b1++)
            ag.dy[b1] = paramab.c(); 
          ag.cz.k = ag.g(ag.f(paramab.a(8)));
          ag.cz.S = paramab.a();
          for (b1 = 0; b1 < 45; b1++) {
            ag.fn[0][b1] = 0;
            ag.fn[1][b1] = 0;
          } 
          ag.fo = (short)paramab.a();
          for (b1 = 0; b1 < ag.fo; b1++) {
            ag.fn[0][b1] = (short)paramab.a();
            ag.fn[1][b1] = (short)paramab.a();
          } 
          i = paramab.c();
          ag.dw = paramab.c();
          ag.dw <<= 32L;
          ag.dw |= i;
          ag.cq = paramab.a();
          for (b1 = 0; b1 < 22; b1++)
            ag.cz.g[b1] = (short)paramab.a(); 
          ag.cz.h = (short)paramab.a();
          ag.cz.i = (short)paramab.a();
          ag.ed = paramab.c();
          ar();
          ag.cS.d(19);
          break;
        case 257:
          ag.cS.d(18);
          break;
        case 769:
          gy = paramab.c();
          for (b1 = 0; b1 < 100; b1++) {
            if (gw[b1] == null)
              gw[b1] = new z(); 
            gw[b1].a();
          } 
          ht[6] = (short)(paramab.a() & 0xFF);
          for (b1 = 0; b1 < gw.length; b1++)
            gw[b1].a(); 
          for (b1 = 0; b1 < ht[6]; b1++) {
            (gw[b1]).a = paramab.b();
            gx[b1] = paramab.b();
            (gw[b1]).f = paramab.a();
            (gw[b1]).b = paramab.b();
            (gw[b1]).c = paramab.b();
            (gw[b1]).d = paramab.b();
            (gw[b1]).e = paramab.b();
          } 
          aH();
          break;
        case 833:
          ag.cz.E = paramab.c();
          gy = paramab.c();
          break;
        case 817:
          if (ht[7] == 0) {
            gK = 100;
            ag.fK[16] = ag.fK[16] - 1;
            ht[6] = (short)(ht[6] + 1);
            for (b1 = 0; b1 < gK && (gw[b1]).a != 0; b1++);
            (gw[b1]).a = (ag.cz.Y[ag.fK[18]]).a;
            (gw[b1]).b = (ag.cz.Y[ag.fK[18]]).b;
            (gw[b1]).c = (ag.cz.Y[ag.fK[18]]).c;
            (gw[b1]).d = (ag.cz.Y[ag.fK[18]]).d;
            (gw[b1]).e = (ag.cz.Y[ag.fK[18]]).e;
            (gw[b1]).f = (ag.cz.Y[ag.fK[18]]).f;
            ag.cz.Y[ag.fK[18]].a();
            gx[b1] = paramab.b();
            gv[ag.fK[18]] = 0;
          } else {
            gK = 25;
            ht[6] = (short)(ht[6] - 1);
            ag.fK[16] = ag.fK[16] + 1;
            for (b1 = 0; b1 < gK && (ag.cz.Y[b1]).a != 0; b1++);
            (ag.cz.Y[b1]).a = (gw[ag.fK[18]]).a;
            (ag.cz.Y[b1]).b = (gw[ag.fK[18]]).b;
            (ag.cz.Y[b1]).c = (gw[ag.fK[18]]).c;
            (ag.cz.Y[b1]).d = (gw[ag.fK[18]]).d;
            (ag.cz.Y[b1]).e = (gw[ag.fK[18]]).e;
            (ag.cz.Y[b1]).f = (gw[ag.fK[18]]).f;
            gw[ag.fK[18]].a();
            gv[b1] = paramab.b();
            gx[ag.fK[18]] = 0;
          } 
          O(0);
          aJ();
          break;
        case 785:
          b1 = 0;
          for (b3 = 15; b1 < 10; b3--) {
            hu[b3] = paramab.a();
            b1++;
          } 
          aM();
          break;
        case 521:
          for (b1 = 0; b1 < 5; b1++) {
            if (gz[b1] == null)
              gz[b1] = new z(); 
            gz[b1].a();
            gC[b1] = "";
          } 
          b5 = paramab.a();
          for (b1 = 0; b1 < b5; b1++) {
            gC[b1] = ag.f(paramab.a(8));
            (gz[b1]).a = paramab.b();
            (gz[b1]).f = paramab.a();
            (gz[b1]).b = paramab.b();
            (gz[b1]).c = paramab.b();
            (gz[b1]).d = paramab.b();
            (gz[b1]).e = paramab.b();
          } 
          ht[13] = (short)paramab.a();
          gD = 1;
          aT();
          break;
        case 787:
          for (b1 = 0; b1 < 20; b1++) {
            if (gz[b1] == null)
              gz[b1] = new z(); 
            gz[b1].a();
            gA[b1] = 0;
            gB[b1] = 0;
          } 
          b4 = paramab.a();
          for (b1 = 0; b1 < b4; b1++) {
            gA[b1] = paramab.c();
            (gz[b1]).a = paramab.b();
            gB[b1] = paramab.c();
            (gz[b1]).f = paramab.a();
            (gz[b1]).b = paramab.b();
            (gz[b1]).c = paramab.b();
            (gz[b1]).d = paramab.b();
            (gz[b1]).e = paramab.b();
          } 
          gS = (byte)(gS + gT);
          aN();
          break;
        case 789:
          gK = 25;
          ag.fK[16] = ag.fK[16] + 1;
          for (b1 = 0; b1 < gK && (ag.cz.Y[b1]).a != 0; b1++);
          (ag.cz.Y[b1]).a = (gz[ag.fK[18]]).a;
          (ag.cz.Y[b1]).b = (gz[ag.fK[18]]).b;
          (ag.cz.Y[b1]).c = (gz[ag.fK[18]]).c;
          (ag.cz.Y[b1]).d = (gz[ag.fK[18]]).d;
          (ag.cz.Y[b1]).e = (gz[ag.fK[18]]).e;
          (ag.cz.Y[b1]).f = (gz[ag.fK[18]]).f;
          p();
          gv[b1] = paramab.b();
          ag.cz.E = paramab.c();
          gy = paramab.c();
          O(0);
          ag.cS.d(35);
          break;
        case 801:
          if (ht[7] == 0) {
            ag.cz.Y[hk].a();
            gv[hk] = 0;
            ag.fK[16] = ag.fK[16] - 1;
          } else {
            gw[hk].a();
            gx[hk] = 0;
            ht[6] = (short)(ht[6] - 1);
          } 
          O(0);
          ag.cS.d(36);
          aP();
          break;
        case 803:
          for (b1 = 0; b1 < 20; b1++) {
            if (gz[b1] == null)
              gz[b1] = new z(); 
            gz[b1].a();
            gA[b1] = 0;
            gB[b1] = 0;
          } 
          if ((b4 = paramab.a()) > 20)
            b4 = 20; 
          for (b1 = 0; b1 < b4; b1++) {
            (gz[b1]).a = paramab.b();
            gB[b1] = paramab.c();
            (gz[b1]).f = paramab.a();
            (gz[b1]).b = paramab.b();
            (gz[b1]).c = paramab.b();
            (gz[b1]).d = paramab.b();
            (gz[b1]).e = paramab.b();
          } 
          aO();
          ho = 8;
          hp = 10;
          hn = hl[6];
          aJ();
          break;
        case 865:
          for (b1 = 0; b1 < 20; b1++) {
            if (gz[b1] == null)
              gz[b1] = new z(); 
            gz[b1].a();
            gA[b1] = 0;
            gB[b1] = 0;
          } 
          if ((b4 = paramab.a()) > 20)
            b4 = 20; 
          for (b1 = 0; b1 < b4; b1++) {
            gA[b1] = paramab.c();
            (gz[b1]).a = paramab.b();
            gB[b1] = paramab.c();
            (gz[b1]).f = paramab.a();
            (gz[b1]).b = paramab.b();
            (gz[b1]).c = paramab.b();
            (gz[b1]).d = paramab.b();
            (gz[b1]).e = paramab.b();
          } 
          d(false);
          break;
        case 867:
          if (ht[7] == 0) {
            gK = 25;
            ht[6] = (short)(ht[6] - 1);
            ag.fK[16] = ag.fK[16] + 1;
            for (b1 = 0; b1 < gK && (ag.cz.Y[b1]).a != 0; b1++);
            (ag.cz.Y[b1]).a = (gz[hk]).a;
            (ag.cz.Y[b1]).b = (gz[hk]).b;
            (ag.cz.Y[b1]).c = (gz[hk]).c;
            (ag.cz.Y[b1]).d = (gz[hk]).d;
            (ag.cz.Y[b1]).e = (gz[hk]).e;
            (ag.cz.Y[b1]).f = (gz[hk]).f;
            gz[hk].a();
            p();
            gv[b1] = paramab.b();
          } else {
            gK = 100;
            ag.fK[16] = ag.fK[16] - 1;
            ht[6] = (short)(ht[6] + 1);
            for (b1 = 0; b1 < gK && (gw[b1]).a != 0; b1++);
            (gw[b1]).a = (gz[hk]).a;
            (gw[b1]).b = (gz[hk]).b;
            (gw[b1]).c = (gz[hk]).c;
            (gw[b1]).d = (gz[hk]).d;
            (gw[b1]).e = (gz[hk]).e;
            (gw[b1]).f = (gz[hk]).f;
            gz[hk].a();
            p();
            gx[b1] = paramab.b();
          } 
          O(0);
          ag.cS.d(40);
          break;
        case 259:
          hv[15] = paramab.c();
          hv[14] = paramab.c();
          hv[13] = ag.H(hv[14]);
          ag.cz.F += hv[15];
          ag.fR = 1;
          ar();
          aW();
          break;
      } 
    } else {
      a(h, gr, paramab);
    } 
    gH = false;
    v.m = true;
    gs = true;
  }
  
  final void a(int paramInt1, int paramInt2, ab paramab) {
    byte b;
    switch (paramInt1) {
      case 531:
        if (paramab == null) {
          b(paramInt2);
          gt = 3;
          return;
        } 
        paramab.a();
        paramab.a();
        if ((b = paramab.a()) == 1) {
          ag.cS.d(43);
          return;
        } 
        if (b == 3 && paramInt2 != -49) {
          ag.cS.d(47);
          return;
        } 
        b(paramInt2);
        gt = 3;
        return;
      case 513:
        if (paramInt2 == -1) {
          b(paramInt2);
          gt = 3;
          return;
        } 
        b(paramInt2);
        gt = 3;
        return;
      case 517:
        aS();
        return;
      case 519:
        aU();
        return;
      case 521:
        aV();
        return;
      case 259:
        aX();
        return;
      case 261:
        aX();
        return;
      case 769:
        b(paramInt2);
        gt = 3;
        return;
      case 789:
        b(paramInt2);
        return;
      case 867:
        if (paramInt2 == -12)
          p(); 
      case 801:
      case 817:
      case 833:
      case 849:
        O(0);
        break;
    } 
    b(paramInt2);
  }
  
  static void p() {
    gz[hk].a();
    gB[hk] = 0;
    gA[hk] = 0;
  }
  
  final void O(int paramInt) {
    ag.fS = (short)paramInt;
    ar();
  }
  
  static int aB() {
    return 32 * gK - 12;
  }
  
  static void e(String paramString, int paramInt1, int paramInt2) {
    int i = 0;
    byte b = 0;
    int j = 0;
    for (b = 0; b < paramString.length(); b++) {
      if (paramString.charAt(b) == '|') {
        gI[i] = paramString.substring(j, b);
        j = b + 1;
        i++;
      } 
    } 
    if (i == 0)
      return; 
    gJ = (short)i;
    gK = (short)(i = (paramInt2 + 12) / 32);
    if (gK > gJ)
      gK = gJ; 
    gN = (short)(paramInt1 + (paramInt2 - 32 * gK - 12 >> 1));
    gM = gL = 0;
  }
  
  final int P(int paramInt) {
    int i = -1;
    if (paramInt == -1 || paramInt == -2 || paramInt == 50 || paramInt == 56) {
      if (paramInt == -1 || paramInt == 50) {
        if (--gL < 0)
          gL = (short)(gJ - 1); 
      } else if (++gL >= gJ) {
        gL = 0;
      } 
      aC();
      i = -2;
    } else if (paramInt == -5 || paramInt == 53) {
      i = gL;
    } 
    return i;
  }
  
  static void aC() {
    if (gM > gL) {
      gM = gL;
      return;
    } 
    if (gL - gM >= gK)
      gM = gL - gK + 1; 
  }
  
  final void aD() {
    int i = gN;
    byte b = 0;
    for (int j = gM; b < gK; j++) {
      if (j == gL) {
        ag.a(45, i, 150, 20, ag.k(0, 0, 0), ag.k(255, 255, 255), ag.k(0, 0, 0), true);
        x.a(ag.bw);
      } else {
        ag.a(46, i + 1, 148, 18, ag.k(0, 0, 0), ag.k(80, 80, 80), ag.k(0, 0, 0), true);
        x.a(ag.bu);
      } 
      ag.b(120, i + 1, gI[j]);
      i += 32;
      b++;
    } 
  }
  
  final void aE() {
    aF();
    aG();
    ag.az();
    ag.bV = 11;
    gO = ag.bY.a;
  }
  
  final boolean aF() {
    for (byte b = 0; b < 12; b++)
      hl[b] = ag.M(2 + b); 
    return true;
  }
  
  final boolean aG() {
    for (byte b = 0; b < 50; b++)
      hm[b] = ag.M(15 + b); 
    return true;
  }
  
  final void aH() {
    String str;
    e(str = "Trade|Warehouse|Safe|Management|", 20, 255);
    gL = gU;
    gM = gV;
    aC();
    hp = 2;
    ho = 1;
    hn = hl[2];
    hr = 0;
    hs = 10;
    if (o && d) {
      o = false;
      ag.cS.m = l;
      ag.cS.n = m;
      ag.cS.d(49);
    } 
    aJ();
    d = false;
  }
  
  final void aI() {
    hp = 17;
    ho = 12;
    hn = hl[2];
    j = 0;
    aJ();
  }
  
  static void aJ() {
    hq = true;
  }
  
  static void a(int paramInt1, int paramInt2, int paramInt3, boolean paramBoolean) {
    ag.bb.a(paramInt2, paramInt3, paramBoolean);
    if (paramInt1 > 0)
      ag.bb.a(paramInt1, paramInt2, paramInt3, 0); 
  }
  
  static void a(String paramString, int paramInt1, int paramInt2, int paramInt3) {
    x.a(paramString, paramInt1 + paramInt3 / 2, paramInt2, 1);
  }
  
  static void aK() {
    a.a();
  }
  
  final void c(String paramString, int paramInt) {
    x.a(ag.bu);
    b(paramInt, 200, 22);
    if (paramString != "")
      b(paramString, paramInt + 1 - ag.dc, 0); 
  }
  
  final void t(int paramInt) {
    int i = paramInt;
    if (ag.cS.b != 0) {
      ag.cS.b();
      ag.ch = -999;
      aJ();
      return;
    } 
    ag.ch = -999;
    switch (hp) {
      case 1:
        R(i);
        return;
      case 2:
        ae(i);
        return;
      case 3:
        aa(i);
        return;
      case 4:
        Z(i);
        return;
      case 5:
        W(i);
        return;
      case 6:
        X(i);
        return;
      case 7:
        Y(i);
        return;
      case 8:
        U(i);
        return;
      case 9:
        V(i);
        return;
      case 10:
        T(i);
        return;
      case 13:
        S(i);
        return;
      case 14:
        ab(i);
        return;
      case 15:
        ad(i);
        return;
      case 16:
        af(i);
        return;
      case 17:
        return;
      case 18:
        Q(i);
        break;
    } 
  }
  
  final void Q(int paramInt) {
    if (k == 0) {
      int i = l.length();
      if (paramInt == -7) {
        if (i > 0) {
          l = l.substring(0, i - 1);
        } else {
          k = 1;
          aJ();
        } 
        if (i == 10) {
          aJ();
          return;
        } 
      } else if (paramInt == -6) {
        if (i >= 4) {
          gE = true;
          n = true;
          c(530);
          return;
        } 
      } else {
        int j;
        if ((j = ag.N(paramInt)) != -1 && i < 12)
          l += "" + j; 
        return;
      } 
    } else if (k == 1) {
      if (ag.bz.a().length() == 0 && paramInt == -7) {
        ba();
        return;
      } 
      int i;
      if ((i = ag.r(paramInt)) == -7) {
        ag.bz.a(-8);
        return;
      } 
      if (i == -5 || i == 53) {
        if (ag.bP == 26 && ag.bz.a().length() >= 4) {
          if (ag.bz.a().length() != 0) {
            m = ag.bz.a();
            ag.bz.a(m);
            k = 0;
            aJ();
            return;
          } 
        } else {
          ag.bz.a(65 + ag.bP);
          return;
        } 
      } else if (i == -6 && ag.bz.a().length() >= 4 && ag.bz.a().length() != 0) {
        m = ag.bz.a();
        ag.bz.a(m);
        k = 0;
        aJ();
      } 
    } 
  }
  
  final void R(int paramInt) {
    switch (paramInt) {
      case -3:
        if (hk > 0) {
          hk--;
        } else {
          hk = 4;
        } 
        aJ();
        return;
      case -4:
        if (hk < 4) {
          hk++;
        } else {
          hk = 0;
        } 
        aJ();
        return;
      case -8:
      case -5:
        if (gD == 0) {
          aU();
          return;
        } 
        aV();
        break;
    } 
  }
  
  final void S(int paramInt) {
    switch (paramInt) {
      case -7:
        bf();
        return;
      case -5:
      case 53:
        if ((gz[hk]).a > 0) {
          hi = (gz[hk]).a;
          ht[7] = (ag.fK[16] < 25) ? 0 : 1;
          ag.cS.m = e.c((gz[hk]).a);
          ag.cS.d(39);
          gt = 14;
          return;
        } 
        break;
      case -3:
      case 52:
        if (hk > 0) {
          hk--;
        } else {
          hk = 4;
        } 
        aJ();
        return;
      case -4:
      case 54:
        if (hk < 4) {
          hk++;
        } else {
          hk = 0;
        } 
        aJ();
        break;
    } 
  }
  
  final void T(int paramInt) {
    switch (paramInt) {
      case -7:
        aQ();
        return;
    } 
    a(paramInt, false);
  }
  
  final void U(int paramInt) {
    z z1;
    switch (paramInt) {
      case -7:
        bf();
        return;
      case -5:
      case 53:
        if ((z1 = be()).a > 0) {
          if (z1.a >= 434 && z1.a <= 437) {
            ag.cS.d(13);
            return;
          } 
          hi = z1.a;
          gR = (short)z1.f;
          hk = ag.fK[18];
          if (z1.a > 500) {
            gP = 2;
            gQ = (short)(z1.a - 501);
          } else if (z1.a > 300) {
            gP = 1;
            gQ = (short)ag.bH[1].a(z1.a - 301, 7);
          } else {
            gP = 0;
            gQ = (short)ag.bH[0].a(z1.a - 101, 7);
          } 
          hv[13] = 0;
          hv[14] = 0;
          e(true);
          aQ();
          return;
        } 
        return;
    } 
    ac(paramInt);
  }
  
  final void V(int paramInt) {
    int i;
    boolean bool = true;
    switch (paramInt) {
      case 48:
      case 49:
      case 50:
      case 51:
      case 52:
      case 53:
      case 54:
      case 55:
      case 56:
      case 57:
        if ((i = ag.N(paramInt)) >= 0 && i <= 9 && hv[13] < 9) {
          hv[14] = hv[14] * 10;
          hv[14] = hv[14] + i;
          if (hv[14] > 0)
            hv[13] = hv[13] + 1; 
        } 
        break;
      case -7:
        if (hv[13] > 0) {
          hv[14] = hv[14] / 10;
          hv[13] = hv[13] - 1;
          break;
        } 
        aP();
        break;
      case -5:
        if (hv[14] > 0) {
          c(800);
          hr = 0;
          break;
        } 
        bool = false;
        break;
      case -6:
        c(802);
        hr = 0;
        break;
      default:
        bool = false;
        break;
    } 
    if (bool)
      aJ(); 
  }
  
  final void W(int paramInt) {
    switch (paramInt) {
      case -7:
        aY();
        return;
      case -5:
      case 53:
        if (gF[gP][ag.fK[18]] != 0) {
          e(false);
          hi = gF[gP][ag.fK[18]];
          gQ = (short)ag.fK[18];
          if (gP == 2) {
            gR = 0;
            gS = 0;
            gT = 1;
            c(786);
          } else {
            gR = 0;
            c(784);
          } 
          hr = 0;
          aJ();
          return;
        } 
        return;
    } 
    a(paramInt, false);
  }
  
  final void X(int paramInt) {
    boolean bool = true;
    switch (paramInt) {
      case -7:
        aL();
      case -3:
      case 52:
        gR = (short)((gR > 0) ? (gR - 1) : 9);
        break;
      case -4:
      case 54:
        gR = (short)((gR < 9) ? (gR + 1) : 0);
        break;
      case -2:
      case -1:
      case 50:
      case 56:
        gR = (short)(gR + ((gR > 4) ? -5 : 5));
        break;
      case -5:
      case 53:
        if (hu[15 - gR] > 0) {
          gS = 0;
          gT = 1;
          c(786);
          hr = 0;
          break;
        } 
        ag.cS.d(8);
        break;
      default:
        bool = false;
        break;
    } 
    if (bool)
      aJ(); 
  }
  
  final void Y(int paramInt) {
    int i;
    switch (paramInt) {
      case -7:
        if (gP == 2) {
          aL();
          return;
        } 
        hr = 0;
        c(784);
        break;
      case -5:
      case 53:
        ag.fK[19] = (gz[ag.fK[18]]).a;
        if ((gz[ag.fK[18]]).a != 0) {
          if (gB[ag.fK[18]] > ag.cz.E) {
            ag.cS.d(11);
            return;
          } 
          if (ag.fK[16] >= 25) {
            ag.cS.d(12);
            return;
          } 
          hk = ag.fK[18];
          ag.cS.m = "" + gB[ag.fK[18]];
          ag.cS.d(34);
          gt = 10;
          return;
        } 
        return;
      default:
        if ((i = a(paramInt, false)) != 0) {
          if (i < 0) {
            if (gS > 1) {
              gT = -1;
              hr = 0;
              c(786);
              break;
            } 
            ag.cS.d(9);
            break;
          } 
          gT = 1;
          hr = 0;
          c(786);
          break;
        } 
        return;
    } 
    aJ();
  }
  
  final void Z(int paramInt) {
    if (paramInt == -7) {
      bf();
      return;
    } 
    int i;
    if ((i = P(paramInt)) >= 0 && i <= 2) {
      gW = (short)gL;
      gX = (short)gM;
      gP = (short)i;
      e(true);
      aL();
      return;
    } 
    if (i == -2)
      aJ(); 
  }
  
  final void aL() {
    c(false);
    ho = 6;
    hp = 5;
    aJ();
  }
  
  final void aM() {
    ho = 7;
    hp = 6;
    aJ();
  }
  
  final void aN() {
    aO();
    ho = 8;
    hp = 7;
    aJ();
  }
  
  final void aO() {
    a(4, 2, true);
  }
  
  final void c(boolean paramBoolean) {
    ht[7] = hf;
    gP = ha;
    if (paramBoolean) {
      a((ht[7] == 0) ? 5 : 20, 3, false);
    } else {
      a((gP == 2) ? 4 : 3, 3, false);
    } 
    ag.fK[10] = hb;
    ag.fK[9] = hc;
    ag.fK[18] = hd;
    ag.fK[8] = he;
    hv[5] = hg;
    hv[6] = hh;
  }
  
  final void aP() {
    c(true);
    hp = 8;
    ho = 4;
    hn = hl[5];
    aJ();
  }
  
  final void aQ() {
    ho = 9;
    hp = 9;
    hn = hl[5];
    aJ();
  }
  
  final void d(boolean paramBoolean) {
    if (paramBoolean) {
      hr = 0;
      gS = 0;
      c(864);
    } else {
      hk = 0;
      hp = 13;
      ho = 10;
      hn = hl[8];
    } 
    aJ();
  }
  
  final void aR() {
    hr = (short)(hr + hs);
    if (ht[15] == 1 && d) {
      c(516);
      aJ();
      return;
    } 
    aS();
  }
  
  final void aS() {
    hr = (short)(hr + hs);
    if (ht[14] == 1) {
      c(518);
      aJ();
      return;
    } 
    aU();
  }
  
  final void aT() {
    hk = 0;
    hp = 1;
    ho = 11;
    hn = (gD == 0) ? hl[0] : hl[1];
    aJ();
  }
  
  final void aU() {
    hr = (short)(hr + hs);
    if (ht[13] == 1) {
      c(520);
      aJ();
      return;
    } 
    aV();
  }
  
  final void aV() {
    hr = (short)(hr + hs);
    if (ag.fR == 0) {
      c(258);
      aJ();
      return;
    } 
    ag.fR = 2;
    aW();
  }
  
  final void aW() {
    hr = (short)(hr + hs);
    c(260);
    aJ();
  }
  
  final void aX() {
    hr = (short)(hr + hs);
    c(768);
    aJ();
  }
  
  final void aa(int paramInt) {
    if (paramInt == -7) {
      aH();
      return;
    } 
    int i;
    if ((i = P(paramInt)) >= 0) {
      gW = (short)gL;
      gX = (short)gM;
      switch (i) {
        case 0:
          gY = gZ = 0;
          aY();
          return;
        case 1:
          e(true);
          aP();
          return;
        case 2:
          e(true);
          d(true);
          return;
      } 
      return;
    } 
    if (i == -2)
      aJ(); 
  }
  
  final void ab(int paramInt) {
    z z1;
    switch (paramInt) {
      case -7:
        aH();
        return;
      case -5:
      case 53:
        if ((z1 = be()).a > 0) {
          c(816);
          hr = 0;
          aJ();
          return;
        } 
        return;
    } 
    ac(paramInt);
  }
  
  final void aY() {
    aZ();
    hp = 4;
    ho = 5;
    hn = hl[4];
    aJ();
  }
  
  final void aZ() {
    String str;
    e(str = "Normal Items|Special Items|Rare Items|", 20, 255);
    gL = gY;
    gM = gZ;
    aC();
    int i = 32 + aB();
    i = 20 + (255 - i >> 1);
    hv[15] = i;
    gN = i + 22 + 10;
  }
  
  final void ac(int paramInt) {
    if (paramInt == -6) {
      if (ht[7] == 1) {
        bc();
        aJ();
        return;
      } 
      if (ht[7] == 0) {
        bd();
        aJ();
        return;
      } 
    } else {
      a(paramInt, true);
    } 
  }
  
  final int a(int paramInt, boolean paramBoolean) {
    int i = 1;
    switch (paramInt) {
      case -1:
      case 50:
        ag.fK[10] = ag.fK[10] - 1;
        break;
      case -2:
      case 56:
        ag.fK[10] = ag.fK[10] + 1;
        break;
      case -3:
      case 52:
        ag.fK[9] = ag.fK[9] - 1;
        if (ag.fK[9] - 1 < 0) {
          ag.fK[9] = 4;
          ag.fK[10] = ag.fK[10] - 1;
        } 
        break;
      case -4:
      case 54:
        ag.fK[9] = ag.fK[9] + 1;
        if (ag.fK[9] + 1 >= 5) {
          ag.fK[9] = 0;
          ag.fK[10] = ag.fK[10] + 1;
        } 
        break;
      default:
        i = 0;
        break;
    } 
    if (i && (i = f(paramBoolean)) == 0)
      aJ(); 
    return i;
  }
  
  final void ad(int paramInt) {
    boolean bool = true;
    if (ht[14] == 0) {
      switch (paramInt) {
        case -4:
        case -3:
          ht[15] = (short)(ht[15] ^ 0x1);
          break;
        case -1:
        case 50:
          ht[15] = 0;
          break;
        case -2:
        case 56:
          ht[15] = 1;
          break;
        case -7:
          aH();
          ag.ct[22] = null;
          ag.ct[24] = null;
          break;
        case -5:
        case 53:
          if (ht[15] == 0) {
            hv[15] = gy;
            if (gy == 0)
              ag.cS.d(14); 
          } else {
            hv[15] = ag.cz.E;
            if (ag.cz.E == 0)
              ag.cS.d(15); 
          } 
          if (hv[15] > 0) {
            ht[14] = 1;
            hv[14] = 0;
            ho = 3;
            aJ();
          } 
          break;
        default:
          bool = false;
          break;
      } 
    } else {
      int i;
      switch (paramInt) {
        case 48:
        case 49:
        case 50:
        case 51:
        case 52:
        case 53:
        case 54:
        case 55:
        case 56:
        case 57:
          if ((i = ag.N(paramInt)) != -1) {
            hv[14] = hv[14] * 10;
            hv[14] = hv[14] + i;
            if (hv[14] > hv[15])
              hv[14] = hv[15]; 
          } 
          break;
        case -7:
          if (hv[14] > 0) {
            hv[14] = hv[14] / 10;
            break;
          } 
          ht[14] = 0;
          ho = 2;
          aJ();
          break;
        case -5:
          if (hv[14] > 0) {
            c(832);
            ht[14] = 0;
            ho = 2;
            aJ();
            break;
          } 
          bool = false;
          break;
        default:
          bool = false;
          break;
      } 
    } 
    if (bool)
      aJ(); 
  }
  
  public final void ba() {
    ag.bV = 2;
    o();
    ag.ck = 1;
    ag.cM[0] = 0;
    ag.cM[1] = 2;
    ag.cS.a = 0;
    ag.bp = false;
  }
  
  static void e(boolean paramBoolean) {
    ha = gP;
    if (paramBoolean) {
      hb = 0;
      hc = 0;
      hd = 0;
      he = 0;
      hf = 0;
      hg = 0;
      hh = 0;
      return;
    } 
    hf = ht[7];
    hb = (short)ag.fK[10];
    hc = (short)ag.fK[9];
    hd = (short)ag.fK[18];
    he = (short)ag.fK[8];
    hg = (short)hv[5];
    hh = (short)hv[6];
  }
  
  final void bb() {
    bc();
    hp = 14;
    ho = 4;
    hn = hl[9];
    aJ();
  }
  
  final void bc() {
    ht[7] = 0;
    a(5, 3, true);
  }
  
  final void bd() {
    ht[7] = 1;
    a(20, 3, true);
  }
  
  final void a(int paramInt1, int paramInt2, boolean paramBoolean) {
    ag.fK[3] = paramInt2;
    ag.fK[6] = 32 * paramInt2 - 4 + 2;
    ag.fK[4] = paramInt1;
    ag.fK[7] = 32 * paramInt1 - 4 + 2;
    char c = '';
    if (paramInt2 < paramInt1) {
      c += '\b';
      ag.fK[11] = 1;
      ag.fK[13] = ag.fK[6] * (ag.fK[6] - 2) * 10;
      ag.fK[13] = (ag.fK[13] / ag.fK[7] + 9) / 10;
    } else {
      ag.fK[11] = 0;
    } 
    ag.fK[5] = 240 - c >> 1;
    ag.fK[12] = ag.fK[5] + 156 + 4;
    ag.fK[26] = -1;
    ag.fK[27] = 0;
    if (paramBoolean) {
      ag.fK[8] = 0;
      ag.fK[10] = 0;
      ag.fK[9] = 0;
      f(true);
    } 
  }
  
  static int f(boolean paramBoolean) {
    if (ag.fK[10] < 0) {
      if (paramBoolean) {
        ag.fK[10] = ag.fK[4] - 1;
      } else {
        ag.fK[10] = hv[5];
        ag.fK[9] = hv[6];
        return -1;
      } 
    } else if (ag.fK[10] >= ag.fK[4]) {
      if (paramBoolean) {
        ag.fK[10] = 0;
      } else {
        ag.fK[10] = hv[5];
        ag.fK[9] = hv[6];
        return 1;
      } 
    } 
    hv[5] = ag.fK[10];
    hv[6] = ag.fK[9];
    if (ag.fK[10] < ag.fK[8]) {
      ag.fK[8] = ag.fK[10];
    } else if (ag.fK[10] >= ag.fK[8] + ag.fK[3]) {
      ag.fK[8] = ag.fK[10] - ag.fK[3] + 1;
    } 
    ag.fK[18] = ag.fK[10] * 5 + ag.fK[9];
    return 0;
  }
  
  static z be() {
    if (ht[7] == 0) {
      hj = gv[ag.fK[18]];
      return ag.cz.Y[ag.fK[18]];
    } 
    hj = gx[ag.fK[18]];
    return gw[ag.fK[18]];
  }
  
  final void bf() {
    String str;
    e(str = "Buy Item|Sell Item|Cancel Sell|", 26, 243);
    gL = gW;
    gM = gX;
    aC();
    hp = 3;
    ho = 1;
    hn = hl[3];
    aJ();
  }
  
  final void ae(int paramInt) {
    if (paramInt == -7) {
      ba();
      if (ag.fS == 0)
        return; 
    } else {
      int i;
      if ((i = P(paramInt)) >= 0) {
        gU = (short)gL;
        gV = (short)gM;
        switch (i) {
          case 0:
            gW = gX = 0;
            bf();
            return;
          case 1:
            e(true);
            bb();
            return;
          case 2:
            bg();
            return;
          case 3:
            bh();
            return;
        } 
        return;
      } 
      if (i == -2)
        aJ(); 
    } 
  }
  
  final void bg() {
    ht[15] = 0;
    ht[14] = 0;
    hp = 15;
    ho = 2;
    hn = hl[10];
    aJ();
  }
  
  final void bh() {
    String str;
    e(str = "Save User Data|Load User Data|", 26, 243);
    hp = 16;
    hn = hl[11];
    aJ();
  }
  
  final void af(int paramInt) {
    if (paramInt == -7) {
      aH();
      return;
    } 
    int i;
    if ((i = P(paramInt)) >= 0 && i <= 1) {
      ht[14] = (short)i;
      ag.cS.d((i == 0) ? 16 : 17);
      gt = 9;
      return;
    } 
    if (i == -2)
      aJ(); 
  }
  
  public static void bi() {
    v.i = false;
    b = null;
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\as.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */