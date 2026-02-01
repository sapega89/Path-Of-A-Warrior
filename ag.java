import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.util.Random;
import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;
import javax.microedition.rms.RecordStore;

public class ag extends Canvas implements Runnable, ae {
  public static e bb = null;
  
  public static ar bc = null;
  
  public static c bd = null;
  
  public static as be = null;
  
  public static af bf = null;
  
  public static k bg = null;
  
  public static String bh;
  
  public static boolean bi;
  
  public static boolean bj;
  
  public static String bk;
  
  public static int bl;
  
  public static String bm;
  
  public static String bn;
  
  public static ac bo = new ac(0, 0, 0, 0);
  
  public static boolean bp = false;
  
  public static boolean bq = false;
  
  public static Graphics br;
  
  public static Main bs;
  
  public static Thread bt = null;
  
  public static g bu = null;
  
  public static g bv = null;
  
  public static g bw = null;
  
  public static g bx = null;
  
  public static Random by;
  
  public static at bz;
  
  public static al bA;
  
  public static al bB;
  
  public static al bC;
  
  public static al bD;
  
  public static al bE;
  
  public static al bF;
  
  public static al bG;
  
  public static d[] bH = new d[3];
  
  public static al bI;
  
  public static int bJ;
  
  public static int bK;
  
  public static int bL;
  
  public static int bM;
  
  public static int bN = 0;
  
  public static int bO = 0;
  
  public static int bP = 0;
  
  public static boolean bQ = false;
  
  public static boolean bR = false;
  
  public static boolean bS = false;
  
  private static int a = 0;
  
  private static boolean b = false;
  
  public static long c;
  
  public static Image[] bT = new Image[1];
  
  public static Image bU;
  
  public static int bV;
  
  public static int bW = -1;
  
  public static int bX = -1;
  
  public static h bY = new h();
  
  public static h bZ = new h();
  
  public static h ca = new h();
  
  public static h cb = new h();
  
  public static h cc = new h();
  
  public static int cd;
  
  public static int ce;
  
  public static h cf = new h();
  
  public static int cg;
  
  public static int ch = -999;
  
  public static int ci = -999;
  
  public static int cj;
  
  public static int ck;
  
  public static int cl;
  
  public static short cm;
  
  public static short cn;
  
  public static short co;
  
  public static short cp;
  
  public static byte cq;
  
  public static byte cr;
  
  public static int[] cs = new int[5];
  
  public static Image[] ct = new Image[45];
  
  public static Graphics cu;
  
  public static Image cv;
  
  public static Image cw;
  
  public static Image[] cx = new Image[6];
  
  public static int cy;
  
  public static n cz = new n();
  
  public static r[] cA = new r[15];
  
  public static short cB;
  
  public static a[] cC = new a[10];
  
  public static short cD;
  
  public static o cE = new o();
  
  public static byte[] cF = new byte[2000];
  
  public static int cG;
  
  public static ah[] cH = new ah[50];
  
  public static short cI;
  
  public static short[] cJ = new short[240];
  
  public static short cK;
  
  public static short cL;
  
  public static int[] cM = new int[4];
  
  public static int cN;
  
  public static int cO;
  
  public static short[] cP = new short[30];
  
  public static short[] cQ = new short[30];
  
  public static aa cR = new aa();
  
  public static l cS = new l();
  
  public static String[] cT = new String[2];
  
  public static byte[] cU;
  
  public static byte[] cV;
  
  public static byte[] cW;
  
  public static ai cX = new ai();
  
  public static t cY = new t();
  
  public static ao cZ = new ao();
  
  public static int da;
  
  public static short db;
  
  public static short dc;
  
  public static int dd;
  
  public static int de;
  
  public static boolean df = false;
  
  public static short dg;
  
  public static short dh;
  
  public static long di;
  
  public static short dj;
  
  public static short dk;
  
  public static String dl;
  
  public static short dm;
  
  public static String dn;
  
  public static short do;
  
  public static String[][] dp = new String[2][120];
  
  public static byte[] dq = new byte[2];
  
  public static int dr;
  
  public static short[] ds = new short[6];
  
  public static String[] dt = new String[6];
  
  public static short[] du = new short[6];
  
  public static short[] dv = new short[6];
  
  public static long dw;
  
  public static long dx;
  
  public static long[] dy = new long[8];
  
  public static an[] dz = new an[5];
  
  public static String[] dA = new String[5];
  
  public static short[] dB = new short[5];
  
  public static am dC = new am();
  
  public static int dD;
  
  public static String[] dE;
  
  public static ak dF = new ak();
  
  public static short dG;
  
  public static short dH;
  
  public static short dI;
  
  public static short dJ;
  
  public static short dK;
  
  public static short[] dL = new short[2];
  
  public static short[] dM = new short[2];
  
  public static short dN;
  
  public static short dO;
  
  public static short dP;
  
  public static short dQ;
  
  public static short dR;
  
  public static short dS;
  
  public static w dT = new w();
  
  public static ad dU = new ad();
  
  public static long dV;
  
  public static long[] dW = new long[2];
  
  public static int dX;
  
  public static int dY;
  
  public static short[] dZ = new short[3];
  
  public static short ea;
  
  public static int[] eb = new int[3];
  
  public static short ec;
  
  public static int ed;
  
  public static short ee;
  
  public static short ef;
  
  public static short eg;
  
  public static short eh;
  
  public static short ei;
  
  public static short ej;
  
  public static short ek;
  
  public static short el = 0;
  
  public static short em = 0;
  
  public static short en = 0;
  
  public static long eo;
  
  public static short ep;
  
  public static Image eq;
  
  public static Image[] er = new Image[2];
  
  public static Image[] es = new Image[2];
  
  public static y[][] et = new y[9][];
  
  public static i[] eu = new i[28];
  
  public static short ev;
  
  public static short[][] ew = new short[7][7];
  
  public static ap[] ex = new ap[7];
  
  public static short[] ey = new short[7];
  
  public static short ez;
  
  public static short eA;
  
  public static short eB;
  
  public static f[] eC = new f[3];
  
  public static short[] eD = new short[14];
  
  public static short[][] eE = new short[9][9];
  
  public static short[][][] eF = new short[8][4][];
  
  public static short[][][] eG = new short[8][4][];
  
  public static short[][][] eH = new short[8][22][];
  
  public static short[][][] eI = new short[8][][];
  
  public static short[][][] eJ = new short[8][][];
  
  public static short[][][] eK = new short[8][][];
  
  public static short[][][][] eL = new short[4][][][];
  
  public static int eM;
  
  public static int eN;
  
  public static au[] eO = new au[20];
  
  public static short eP;
  
  public static y[] eQ;
  
  public static Image eR;
  
  public static y[][] eS = new y[2][];
  
  public static y[][] eT = new y[2][];
  
  public static y[] eU;
  
  public static y[] eV;
  
  public static y[] eW;
  
  public static byte[] eX;
  
  public static y[] eY;
  
  public static short eZ;
  
  public static byte[] fa;
  
  public static y[] fb;
  
  public static short fc;
  
  public static byte[] fd;
  
  public static y[] fe;
  
  public static short ff;
  
  public static short fg;
  
  public static short fh;
  
  public static Image fi;
  
  public static y[] fj;
  
  public static short fk;
  
  public static Image fl;
  
  public static y[] fm;
  
  public static short[][] fn = new short[3][45];
  
  public static short fo;
  
  public static short[] fp = new short[2];
  
  public static int fq;
  
  public static d fr;
  
  public static al fs;
  
  public static String ft;
  
  public static short fu;
  
  public static short fv;
  
  public static String[] fw = new String[2];
  
  public static int[] fx = new int[2];
  
  public static int[] fy = new int[2];
  
  public static int[] fz = new int[2];
  
  public static int[] fA = new int[2];
  
  public static int[] fB = new int[2];
  
  public static int[] fC = new int[2];
  
  public static int fD;
  
  public static int fE;
  
  public static int fF;
  
  public static short fG;
  
  public static short fH;
  
  public static short fI;
  
  public static short fJ;
  
  public static int[] fK = new int[32];
  
  public static z[] fL = new z[25];
  
  public static boolean[] fM = new boolean[16];
  
  public static Image fN;
  
  public static int[] fO = new int[4];
  
  public static h[] fP = new h[3];
  
  public static z fQ = new z();
  
  public static short fR;
  
  public static short fS;
  
  public static String[] fT = new String[30];
  
  public static String[] fU = new String[1];
  
  public static String[] fV = new String[6];
  
  public static String[] fW = new String[1];
  
  public static String[] fX = new String[1];
  
  public static String[] fY = new String[1];
  
  public static String[] fZ = new String[1];
  
  public static String[] ga = new String[1];
  
  public static String[] gb = new String[4];
  
  public static String[] gc = new String[2];
  
  public static String[] gd = new String[7];
  
  public static String[] ge = new String[5];
  
  public static String[] gf = new String[5];
  
  public static boolean gg = false;
  
  public static boolean gh = true;
  
  public static long gi;
  
  public boolean gj = false;
  
  public static Image gk = null;
  
  public static Image gl = null;
  
  public static int gm = 0;
  
  public ag(Main paramMain) {
    bs = paramMain;
    setFullScreenMode(true);
    r();
  }
  
  public static void q() {
    cg = 1;
    ch = -999;
    ck = 1;
    cq = 0;
    cs[4] = -1;
    cs[3] = -1;
    cs[2] = -1;
    cs[1] = -1;
    cs[0] = -1;
  }
  
  public final void r() {
    bJ = getWidth();
    bK = getHeight();
    bL = bJ / 2;
    bM = bK / 2;
  }
  
  public final void s() {
    r();
    bu = new g("/0_font.png", 8, 17, 9, 16777215);
    bv = new g("/0_font.png", 8, 17, 9, 0);
    bw = new g("/0_font.png", 8, 17, 9, 16400640);
    bx = new g("/0_font.png", 8, 17, 9, 6579300);
    bA = new al("/imgui.scr");
    bE = new al("/edat.scr");
    bF = new al("/mdat_QVGA.scr");
    bB = new al("/imgchar.scr");
    bC = new al("/imgeff.scr");
    bD = new al("/imgtile.scr");
    bG = new al("/gamestr.scr");
    q();
    try {
      bh = bs.getAppProperty("MIDlet-Version");
    } catch (Exception exception) {
      bh = "";
    } 
    try {
      bk = bs.getAppProperty("GAMEVIL_SERVER");
    } catch (Exception exception) {
      bk = "ur.gamevil.net";
    } 
    try {
      bl = Integer.parseInt(bs.getAppProperty("GAMEVIL_PORT"));
    } catch (Exception exception) {
      bl = 28230;
    } 
    try {
      bm = bs.getAppProperty("GAMEVIL_MOREGAMES");
    } catch (Exception exception) {
      bm = "http://usaapp1.gamevil.net/moregames/index2.php?bid=POW_";
    } 
    try {
      bn = bs.getAppProperty("GAMEVIL_MULTIPLAY");
    } catch (Exception exception) {
      bn = "http://ur.gamevil.net/moregames/pow_multiplayer.php";
    } 
    try {
      if (bs.getAppProperty("GAMEVIL_CHEAT").equals("TRUE")) {
        bi = true;
      } else {
        bi = false;
      } 
    } catch (Exception exception) {
      bi = false;
    } 
    bj = false;
    bZ.a = (short)bJ;
    bZ.b = (short)bK;
    bY.a = (short)bJ;
    bY.b = (short)bK;
    db = 0;
    dc = 0;
    dd = bY.a >> 1;
    de = bY.b >> 1;
    if (bK % 2 == 1)
      de++; 
    x();
    bV = 0;
    ck = 1;
    dr = 0;
    G();
    cz.a();
    by = new Random();
    bU = d("softbg");
    bg = new k(bs);
    be = new as();
    as.a = new m();
    bb = new e();
    bc = new ar();
    bd = new c();
  }
  
  public void keyPressed(int paramInt) {
    t(paramInt);
  }
  
  public final void t() {
    if (ch == -999)
      return; 
    if (bS) {
      if (ch == -5 || ch == 53)
        a(false); 
      ch = -999;
      return;
    } 
    switch (bV) {
      case 0:
        if (bf != null) {
          bf.b();
          return;
        } 
        break;
      case 11:
        if (!as.gu)
          be.t(ch); 
        break;
    } 
  }
  
  public static void b(String paramString) {
    System.out.println(" " + paramString);
  }
  
  public synchronized void paint(Graphics paramGraphics) {
    gg = false;
    br = paramGraphics;
    x.a(paramGraphics);
    if (bS) {
      x.b(0, 0, bJ, bK, 0);
      cS.b(10);
      x.a(bu);
      int j = de - 5 - 10;
      x.a("RESUME", bL, j + dc + 7, 1);
      gg = true;
      return;
    } 
    P();
    gg = true;
  }
  
  public void run() {
    s();
    gi = System.currentTimeMillis();
    while (gh) {
      try {
        gi = System.currentTimeMillis();
        if (bS) {
          t();
          repaint(0, 0, bJ, bK);
          serviceRepaints();
          ch = -999;
          if (bQ) {
            b(bR);
            bQ = false;
          } 
          f(100);
          continue;
        } 
        if (bX != bV) {
          ch = -999;
        } else {
          ch = ci;
        } 
        ci = -999;
        if (++bN < 0)
          bN = 0; 
        if (a > 0)
          a--; 
        t();
        if (bg != null)
          bg.a(); 
        u();
        be.i();
        ch = -999;
        if (bQ) {
          b(bR);
          bQ = false;
        } 
        long l1 = System.currentTimeMillis();
        int j;
        if ((j = ((bV == 3) ? ae.aQ[dh] : ae.aQ[2]) - (int)(l1 - gi)) > 20) {
          f(j);
        } else {
          f(20);
        } 
        if (bN > 2)
          bq = true; 
        bX = bV;
      } catch (Exception exception) {
        b("--run:" + exception);
      } 
    } 
  }
  
  public final void u() {
    repaint();
    serviceRepaints();
    while (!gg)
      f(20); 
  }
  
  public static void f(int paramInt) {
    try {
      Thread.yield();
      Thread.sleep(paramInt);
      return;
    } catch (Exception exception) {
      return;
    } 
  }
  
  public void hideNotify() {
    a(true);
  }
  
  public void showNotify() {
    a(true);
  }
  
  public final void a(boolean paramBoolean) {
    if (paramBoolean && bV == 3) {
      this.gj = true;
    } else if (!paramBoolean) {
      this.gj = false;
    } 
    if (bS == paramBoolean || b || a > 0)
      return; 
    if (!Main.c || !bq)
      return; 
    bQ = true;
    bR = paramBoolean;
  }
  
  public final void b(boolean paramBoolean) {
    bS = paramBoolean;
    if (bS) {
      ch = -999;
      if (bg != null) {
        k.a.c();
        return;
      } 
    } else {
      f(300);
      ck = 1;
      if (be != null)
        as.aJ(); 
      k.a.d();
      if (bV == 2 && cM[0] == 4)
        ck = 2; 
    } 
  }
  
  public static void v() {
    b = true;
  }
  
  public static void w() {
    b = false;
    a = 3;
  }
  
  static void x() {
    byte b;
    for (b = 0; b < 2; b++)
      er[b] = null; 
    for (b = 0; b < 9; b++)
      et[b] = null; 
    for (b = 0; b < ct.length; b++)
      ct[b] = null; 
    eT[1] = null;
    eT[0] = null;
    eS[1] = null;
    eS[0] = null;
    eU = null;
    eR = null;
    eV = null;
    eW = null;
    eY = null;
    fb = null;
    fe = null;
    cE.a = null;
    dU.g = null;
    dU.h = null;
    cz.aC = cz.aE = null;
    cz.aG = null;
    cz.aH = null;
    cU = cW = cV = null;
    ep = 0;
    cS.b = 0;
    dh = 2;
    for (b = 0; b < 30; b++) {
      cP[b] = 0;
      cQ[b] = 0;
    } 
    cX = new ai();
    cY = new t();
    cZ = new ao();
  }
  
  static byte g(int paramInt) {
    bb.e(paramInt);
    return (paramInt < 100) ? 1 : ((paramInt < 300) ? (byte)cX.b : ((paramInt < 500) ? cY.b : cZ.b));
  }
  
  final void y() {
    boolean bool;
    cz.K = g((cz.X[0]).a);
    ai();
    ah();
    bb.d();
    ab();
    bY.a = 240;
    bY.b = 243;
    db = 0;
    dc = 16;
    bV = 3;
    co = 2;
    cn = 1;
    cr = 0;
    cl = 0;
    fq = 0;
    if (dj != 0) {
      bool = true;
    } else {
      (cz.a[1]).a = (short)((dz[dm]).b * 27 + 12);
      (cz.a[1]).b = (short)((dz[dm]).c * 27 + 20);
      do = 1;
      dY = 0;
      bool = false;
    } 
    cz.d[1] = cz.c = 0;
    cz.d[0] = cz.c = 0;
    cz.e[1] = 0;
    cz.e[0] = 0;
    cz.f[1] = 0;
    cz.f[0] = 0;
    cz.O = 0;
    cz.N = 20;
    cz.L = 0;
    cz.T = 0;
    cz.H = 0;
    cz.I = 0;
    cz.A = 0;
    cz.B = 0;
    cz.C = 0;
    cz.D = 0;
    cz.R = 0;
    O();
    if (bi) {
      cz.E = 500000;
      cz.y = 2000;
      cz.p = 2000;
      cz.o = 2000;
      cz.m = 2000;
      cz.w = 2000;
      cz.n = 2000;
      cz.x = 2000;
      cz.z = 2000;
      cz.r = 2000;
      cz.q = 2000;
    } 
    fh = 0;
    fg = 1;
    cR.a = 0;
    dT.a = 0;
    dU.a = 0;
    ek = 0;
    eB = 0;
    eX = null;
    fa = null;
    fd = null;
    for (byte b = 0; b < 2; b++) {
      if (et[b] == null)
        et[b] = K(82 + b); 
    } 
    h(bool);
    A();
    eS[cz.K] = K(87 + (cz.K << 2));
    cz.aD = K(51 + cz.aB);
    cz.aF = K(46);
    eT[cz.K] = K(89 + (cz.K << 2));
    ct[40 + cz.K] = d(bB.a(42 + cz.K));
    eU = K(86);
    z();
    eQ = K(98);
    eR = d(bC.a(44));
    eV = K(55);
    ct[43] = d(bC.a(0));
    eW = K(56);
    ct[44] = d(bC.a(1));
    ct[31] = d(bA.a(52));
    eq = d(bB.a(45));
    dW[1] = B();
    dW[0] = B();
    dV = dW[0] - dV;
    dW[1] = B();
    dV = dW[0] = B();
    dj = 1;
    dX = 0;
  }
  
  final void z() {
    ct[42] = d(bC.a(2));
  }
  
  final void A() {
    int[] arrayOfInt = { 56, 57 };
    for (byte b = 0; b < arrayOfInt.length; b++) {
      if ((dz[dm]).d != 0) {
        es[b] = null;
        et[b] = null;
        es[b] = a(bB.a(arrayOfInt[b]), (dz[dm]).d);
      } else {
        es[b] = null;
        et[b] = null;
        es[b] = d(bB.a(arrayOfInt[b]));
      } 
      if (et[b] == null)
        et[b] = K(82 + b); 
    } 
  }
  
  static Image a(String paramString, int paramInt) {
    Image image = null;
    String str;
    byte[] arrayOfByte = j.a(str = "/" + paramString + ".png");
    if (paramInt == 0)
      return image = Image.createImage(arrayOfByte, 0, arrayOfByte.length); 
    int[][][] arrayOfInt = { { { 236, 211, 197 }, { 205, 143, 128 }, { 129, 81, 69 }, { 104, 60, 49 }, { 79, 39, 29 } }, { { 226, 205, 178 }, { 196, 179, 152 }, { 180, 142, 122 }, { 135, 111, 47 }, { 93, 73, 49 } }, { { 174, 225, 242 }, { 101, 156, 195 }, { 61, 102, 139 }, { 43, 78, 115 }, { 45, 45, 84 } }, { { 162, 199, 159 }, { 135, 156, 119 }, { 86, 123, 98 }, { 33, 98, 63 }, { 51, 51, 51 } } };
    int m = arrayOfByte.length;
    int i1 = 0;
    int j;
    for (j = 0; j <= m - 4; j++) {
      if (arrayOfByte[j] == 80 && arrayOfByte[j + 1] == 76 && arrayOfByte[j + 2] == 84 && arrayOfByte[j + 3] == 69) {
        i1 = j;
        break;
      } 
    } 
    int i2 = arrayOfByte[i1 - 1] & 0xFF | arrayOfByte[i1 - 2] << 8 & 0xFF00;
    for (byte b = 0; b < 5; b++) {
      for (j = i1 + 4; j <= i1 + i2 - 3; j++) {
        if (arrayOfByte[j] == (byte)(arrayOfInt[0][b][0] & 0xFF) && arrayOfByte[j + 1] == (byte)(arrayOfInt[0][b][1] & 0xFF) && arrayOfByte[j + 2] == (byte)(arrayOfInt[0][b][2] & 0xFF)) {
          arrayOfByte[j] = (byte)(arrayOfInt[paramInt][b][0] & 0xFF);
          arrayOfByte[j + 1] = (byte)(arrayOfInt[paramInt][b][1] & 0xFF);
          arrayOfByte[j + 2] = (byte)(arrayOfInt[paramInt][b][2] & 0xFF);
          break;
        } 
      } 
    } 
    long l1 = x.a(arrayOfByte, i1, i2 + 4);
    arrayOfByte[i1 + i2 + 4] = (byte)(int)(l1 >> 24L & 0xFFL);
    arrayOfByte[i1 + i2 + 5] = (byte)(int)(l1 >> 16L & 0xFFL);
    arrayOfByte[i1 + i2 + 6] = (byte)(int)(l1 >> 8L & 0xFFL);
    arrayOfByte[i1 + i2 + 7] = (byte)(int)(l1 & 0xFFL);
    return image = Image.createImage(arrayOfByte, 0, arrayOfByte.length);
  }
  
  final void h(int paramInt) {
    d(0, 0, 0);
    a(ct[34], bZ.a / 2 - ct[34].getWidth() / 2, bZ.b / 2 - ct[34].getHeight() / 2, ct[34].getWidth(), ct[34].getHeight(), 0, 0);
    ck = 1;
    c.f();
    cd = ((cz.b[0]).a - 1) / 7 * 7 + 4 - (cb.a >> 1);
    ce = ((cz.b[0]).b - 1) / 7 * 7 + 4 - (cb.b >> 1);
    (cz.b[1]).a = (cz.b[0]).a;
    (cz.b[1]).b = (cz.b[0]).b;
    cE = bd.b(cg);
    bd.a(ds[dk]);
    bd.a(cb.a, cb.b, cd, ce, paramInt);
  }
  
  static long B() {
    return System.currentTimeMillis();
  }
  
  final void C() {
    int j = 0;
    byte[] arrayOfByte = v(48);
    j = 38 * cq + 40;
    dr = 0;
    for (byte b = 0; b < 6; b++) {
      ds[b] = (short)arrayOfByte[j + b];
      if (ds[b] > 0) {
        int m = 38 * ds[b] + 10;
        byte b1;
        for (b1 = 0; b1 < 30 && arrayOfByte[m + b1] != 0; b1++);
        dt[b] = a(arrayOfByte, m, m + b1);
        du[b] = (short)arrayOfByte[m + 36];
        dv[b] = (short)arrayOfByte[m + 37];
        dr++;
      } 
    } 
    cN = dr;
    dE = dt;
  }
  
  final void D() {
    dn = dA[dm];
    byte[] arrayOfByte1 = v(56);
    byte[] arrayOfByte2 = a(arrayOfByte1, du[dk] + dm);
    byte b;
    for (b = 0; b < arrayOfByte2.length && arrayOfByte2[b] != 0; b++);
    byte[] arrayOfByte3 = new byte[b];
    System.arraycopy(arrayOfByte2, 0, arrayOfByte3, 0, b);
    b(arrayOfByte3, 190, 0);
  }
  
  final byte[] a(byte[] paramArrayOfbyte, int paramInt) {
    int[] arrayOfInt1 = new int[110];
    byte[] arrayOfByte1 = new byte[1500];
    byte[] arrayOfByte2 = new byte[1500];
    byte[] arrayOfByte3 = new byte[1500];
    char[] arrayOfChar = new char[3];
    byte b1 = 0;
    int[] arrayOfInt2 = { 0, 0 };
    int[] arrayOfInt3 = { 0, 0 };
    int j = paramArrayOfbyte[0] & 0xFF | paramArrayOfbyte[1] << 8 & 0xFF00;
    byte b2;
    for (b2 = 0; b2 < j + 1; b2++)
      arrayOfInt1[b2] = paramArrayOfbyte[2 + b2 * 2] & 0xFF | paramArrayOfbyte[2 + b2 * 2 + 1] << 8 & 0xFF00; 
    System.arraycopy(paramArrayOfbyte, arrayOfInt1[paramInt], arrayOfByte1, 0, arrayOfInt1[paramInt + 1] - arrayOfInt1[paramInt]);
    arrayOfChar[2] = Character.MIN_VALUE;
    arrayOfChar[1] = Character.MIN_VALUE;
    arrayOfChar[0] = Character.MIN_VALUE;
    for (b2 = 0; b2 < 3 && arrayOfByte1[b2] >= 48 && arrayOfByte1[b2] <= 57; b2++) {
      arrayOfChar[b2] = (char)arrayOfByte1[b2];
      b1++;
    } 
    if (b1 != 0) {
      arrayOfInt3[0] = b1 + 1;
      arrayOfInt2[0] = b1 + 1;
      int m = a(arrayOfChar);
      System.arraycopy(paramArrayOfbyte, arrayOfInt1[m], arrayOfByte2, 0, arrayOfInt1[m + 1] - arrayOfInt1[m]);
    } else {
      System.arraycopy(arrayOfByte1, 0, arrayOfByte2, 0, 1500);
    } 
    while (arrayOfByte2[arrayOfInt3[1]] != 0) {
      if (arrayOfByte2[arrayOfInt3[1]] == 40) {
        arrayOfByte3 = a(arrayOfByte3, arrayOfByte2, arrayOfInt2[1], arrayOfInt3[1]);
        arrayOfInt2[1] = arrayOfInt3[1] + 1;
        if (b1 != 0) {
          arrayOfInt3[1] = a(arrayOfByte2, arrayOfInt3[1], ')');
          arrayOfInt2[1] = a(arrayOfByte2, arrayOfInt3[1], ')');
          arrayOfInt3[0] = a(arrayOfByte1, arrayOfInt3[0], '|');
          arrayOfByte3 = a(arrayOfByte3, arrayOfByte1, arrayOfInt2[0], arrayOfInt3[0] - 1);
          arrayOfInt2[0] = arrayOfInt3[0];
          continue;
        } 
        arrayOfInt3[1] = a(arrayOfByte2, arrayOfInt3[1], ')');
        arrayOfByte3 = a(arrayOfByte3, arrayOfByte2, arrayOfInt2[1], arrayOfInt3[1] - 1);
        arrayOfInt2[1] = arrayOfInt3[1];
        continue;
      } 
      arrayOfInt3[1] = arrayOfInt3[1] + 1;
    } 
    return arrayOfByte3 = a(arrayOfByte3, arrayOfByte2, arrayOfInt2[1], arrayOfInt3[1]);
  }
  
  static byte[] a(byte[] paramArrayOfbyte1, byte[] paramArrayOfbyte2, int paramInt1, int paramInt2) {
    byte b;
    for (b = 0; b < paramArrayOfbyte1.length && paramArrayOfbyte1[b] != 0; b++);
    System.arraycopy(paramArrayOfbyte2, paramInt1, paramArrayOfbyte1, b, paramInt2 - paramInt1);
    return paramArrayOfbyte1;
  }
  
  static int a(byte[] paramArrayOfbyte, int paramInt, char paramChar) {
    byte b;
    for (b = 0; paramArrayOfbyte[paramInt + b] != paramChar && paramArrayOfbyte[paramInt + b] != 0; b++) {
      if ((paramArrayOfbyte[paramInt + b] & 0x80) != 0) {
        b += 2;
        continue;
      } 
    } 
    return paramInt + b + 1;
  }
  
  static void a(int paramInt1, int paramInt2, String paramString) {
    if (paramString != null)
      x.a(paramString, paramInt1, paramInt2, 0); 
  }
  
  public static void b(int paramInt1, int paramInt2, String paramString) {
    if (paramString != null)
      x.a(paramString, paramInt1, paramInt2, 1); 
  }
  
  final void E() {
    if (ct[30] == null) {
      ct[30] = Image.createImage(240, 320);
      Graphics graphics = ct[30].getGraphics();
      for (byte b = 0; b < 4; b++) {
        Image image = d("title_" + (b + 1));
        graphics.drawImage(image, 0, 80 * b, 20);
      } 
    } 
  }
  
  final void F() {
    cy = 0;
    while (cy < 4) {
      ct[26 + cy] = d(bA.a(73 + cy));
      cy++;
    } 
    ad();
  }
  
  static void G() {
    byte[] arrayOfByte = new byte[2];
    try {
      RecordStore recordStore;
      if ((recordStore = RecordStore.openRecordStore("gamevil_pow_env", false)) == null || recordStore.getNumRecords() < 1)
        return; 
      cG = (arrayOfByte = recordStore.getRecord(1)).length;
    } catch (Exception exception) {}
    if (cG >= 2) {
      dg = (short)arrayOfByte[0];
      dh = (short)arrayOfByte[1];
    } 
  }
  
  static void H() {
    byte[] arrayOfByte;
    (arrayOfByte = new byte[2])[0] = (byte)dg;
    arrayOfByte[1] = (byte)dh;
    try {
      RecordStore recordStore;
      if ((recordStore = RecordStore.openRecordStore("gamevil_pow_env", true)).getNumRecords() == 0)
        recordStore.addRecord(arrayOfByte, 0, arrayOfByte.length); 
      recordStore.setRecord(1, arrayOfByte, 0, arrayOfByte.length);
      return;
    } catch (Exception exception) {
      return;
    } 
  }
  
  static void I() {
    if (cM[1] < cM[2]) {
      cM[2] = cM[1];
      return;
    } 
    if (cM[1] > cM[2] + 4)
      cM[2] = cM[1] - 4; 
  }
  
  final void a(Image paramImage, int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, int paramInt6) {
    a(paramInt1, paramInt2, paramInt3, paramInt4, paramImage, paramInt5, paramInt6);
  }
  
  static String b(String paramString, int paramInt) {
    if (paramString == null)
      return null; 
    boolean bool = false;
    int j = 0;
    byte b1 = 0;
    byte b2 = 0;
    paramString = paramString + "|";
    for (byte b3 = 0; b3 < paramString.length(); b3++) {
      if (paramString.charAt(b3) == '|')
        b2++; 
      if (!bool && b2 == paramInt) {
        if (b2 == 0) {
          j = b3;
        } else {
          j = b3 + 1;
        } 
        bool = true;
      } else if (bool && b2 == paramInt + 1) {
        b1 = b3;
        break;
      } 
    } 
    return paramString.substring(j, b1);
  }
  
  static void c(int paramInt1, int paramInt2, String paramString) {
    x.a(paramString, paramInt1, paramInt2, 0);
  }
  
  final void c(int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    a(paramInt1 + 1, paramInt2 + 1, paramInt3 - 2, paramInt4 - 2, 0, 0, 10000536, true);
  }
  
  final int b(int paramInt1, int paramInt2, int paramInt3) {
    int j = 240 - paramInt2 >> 1;
    c(j, paramInt1, paramInt2, paramInt3);
    return j;
  }
  
  final void c(int paramInt1, int paramInt2) {
    int j = b(paramInt2, 200, 22);
    byte b = 0;
    int i1 = paramInt1;
    do {
      b++;
    } while ((i1 /= 10) > 0);
    j += 100;
    int m = b * 7 + (b - 1) / 3 * 4 + 12 + 3;
    j -= m >> 1;
    paramInt2 += 6;
    h(paramInt1, j + m + 10, paramInt2);
    b(ct[32], dd - 69, paramInt2 - 5, ct[32].getWidth(), ct[32].getHeight(), 0, 0);
  }
  
  final void i(int paramInt) {
    c(cz.E, paramInt);
  }
  
  static short a(byte paramByte1, byte paramByte2) {
    return (short)(paramByte1 & 0xFF | (paramByte2 & 0xFF) << 8);
  }
  
  final void J() {
    short[] arrayOfShort = { 7, 14, 21, 32, 39, 46, 57, 64, 71, 82 };
    int j = cz.E;
    a(dd - 70, de - 80 + dc, 140, 22, false);
    byte b;
    for (b = 0; b < 9; b++) {
      j /= 10;
      if (0 == j)
        break; 
    } 
    d(cz.E, dd + (arrayOfShort[b] >> 1) + 16 - db, de - 76, 0);
    b(ct[32], dd - 69 - db, de - 80, ct[32].getWidth(), ct[32].getHeight(), 0, 0);
  }
  
  final void b(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5) {
    short s1 = 0;
    short s2 = 0;
    short s3 = 0;
    short s4 = 0;
    short s5 = 0;
    short s6 = 0;
    String str = "";
    dF.b.a = paramInt2;
    dF.b.b = paramInt3;
    dF.b.c = paramInt4;
    dF.b.d = paramInt5;
    dF.c = "";
    if (paramInt1 > 999)
      if (paramInt1 < 1100) {
        s6 = m((cz.X[paramInt1 - 1000]).a);
        s1 = (cz.X[paramInt1 - 1000]).b;
        s2 = (cz.X[paramInt1 - 1000]).c;
        s3 = (cz.X[paramInt1 - 1000]).d;
        s4 = (cz.X[paramInt1 - 1000]).e;
        s5 = (short)(cz.X[paramInt1 - 1000]).f;
        str = l((cz.X[paramInt1 - 1000]).a);
      } else if (paramInt1 < 1200) {
        s6 = m((cz.Y[paramInt1 - 1100]).a);
        s1 = (cz.Y[paramInt1 - 1100]).b;
        s2 = (cz.Y[paramInt1 - 1100]).c;
        s3 = (cz.Y[paramInt1 - 1100]).d;
        s4 = (cz.Y[paramInt1 - 1100]).e;
        s5 = (short)(cz.Y[paramInt1 - 1100]).f;
        str = l((cz.Y[paramInt1 - 1100]).a);
      } else if (paramInt1 < 2000) {
        dF.c = k((cz.Z[paramInt1 - 1200]).a);
      } else {
        dF.c = j(paramInt1 - 2000);
      }  
    if (dF.c != "") {
      if (str != "")
        dF.c += str; 
      if (s1 != 0)
        dF.c += " / ATK+" + s1; 
      if (s2 != 0)
        dF.c += " / DEF+" + s2; 
      if (s3 != 0)
        dF.c += " / HP+" + s3; 
      if (s4 != 0)
        dF.c += " / MP+" + s4; 
      if (s5 != 0)
        dF.c += " / Enchanted Lv" + s5; 
      if (s6 != 0)
        dF.c += " / Available at Lv" + s6; 
      dD = c(dF.c);
      if (dD > paramInt4 - 2) {
        dF.a = 1;
        dF.d = (short)(paramInt2 + 20);
        return;
      } 
      dF.a = 0;
      dF.d = (short)(paramInt2 + 1);
    } 
  }
  
  final String j(int paramInt) {
    String str1 = "";
    paramInt -= 12;
    if (paramInt < 0 || paramInt > 18)
      return str1; 
    byte[] arrayOfByte;
    String str2 = a(arrayOfByte = d(54, paramInt), 0, arrayOfByte.length);
    if (cz.W[paramInt] != 0) {
      arrayOfByte = d(54, paramInt + 19);
      str1 = str2 + " / Lv" + cz.W[paramInt] + " " + a(arrayOfByte, 0, arrayOfByte.length);
    } else {
      str1 = str2 + " / (Not Available)";
    } 
    return str1;
  }
  
  final String k(int paramInt) {
    String str = "";
    if (--paramInt < 0 || paramInt > 10)
      return str; 
    if (paramInt < 9) {
      str = ae.aN[paramInt] + " / Recover " + ae.aP[paramInt % 3] + "% of total " + ae.aO[paramInt / 3];
    } else {
      byte[] arrayOfByte = d(54, 24 + paramInt);
      str = ae.aN[paramInt] + " / " + a(arrayOfByte, 0, arrayOfByte.length);
    } 
    return str;
  }
  
  static String l(int paramInt) {
    switch (paramInt) {
      case 434:
        return " / Hp 5 Increased";
      case 435:
        return " / MP 3 Increased";
      case 436:
        return " / DEF 1 Increased";
      case 437:
        return " / ATK 1 Increased";
      case 502:
        return " / Catherine's scarf";
      case 504:
        return " / all General Visiting";
    } 
    return "";
  }
  
  static short m(int paramInt) {
    bb.e(paramInt);
    if (paramInt > 500) {
      dF.c = cZ.a;
      return cZ.g;
    } 
    if (paramInt > 300) {
      dF.c = cY.a;
      return cY.h;
    } 
    if (paramInt > 100) {
      dF.c = cX.a;
      return (short)ae.aM[paramInt % 5];
    } 
    return 0;
  }
  
  final void K() {
    switch (cl) {
      case 0:
        c(0, 0, 0);
        a(ct[7], db, dc, bY.a, bY.b, cc.a, cc.b);
        return;
      case 1:
        c(0, 0, 0);
        return;
      case 2:
        c(255, 255, 255);
        break;
    } 
  }
  
  final void c(int paramInt1, int paramInt2, int paramInt3) {
    x.b(db, dc, bY.a, bY.b, k(paramInt1, paramInt2, paramInt3));
  }
  
  static String n(int paramInt) {
    String str;
    int j;
    int[] arrayOfInt = new int[j = (str = Integer.toString(paramInt)).length()];
    for (byte b1 = 0; b1 < j; b1++) {
      arrayOfInt[j - b1 - 1] = paramInt % 10;
      paramInt /= 10;
    } 
    str = "";
    for (byte b2 = 0; b2 < j; b2++) {
      str = str + arrayOfInt[b2];
      if (j % 3 == (b2 + 1) % 3 && b2 != j - 1)
        str = str + ","; 
    } 
    return str;
  }
  
  static void a(z paramz, boolean paramBoolean, int paramInt) {
    dF.a();
    bb.a(paramz, 0, 0, 200, 22, paramInt, paramBoolean);
  }
  
  static z a(p paramp) {
    z z1;
    (z1 = new z()).a();
    z1.a = paramp.a;
    z1.b = paramp.b;
    return z1;
  }
  
  final z o(int paramInt) {
    z z1 = new z();
    if (paramInt == -1)
      paramInt = fK[18]; 
    switch (fK[0]) {
      case 0:
        z1 = fL[paramInt];
        break;
      case 1:
        if (paramInt < 5) {
          z1 = a(cz.Z[paramInt]);
          break;
        } 
        z1 = cz.Y[paramInt - 5];
        break;
      case 2:
      case 3:
        if (fK[27] == 0) {
          z1 = cz.Y[paramInt];
          break;
        } 
        z1 = cz.X[paramInt];
        break;
    } 
    return z1;
  }
  
  final int p(int paramInt) {
    byte b;
    for (b = 0; b < 4 && Character.MIN_VALUE != dC.d[b]; b++);
    if (paramInt != 0) {
      char c1 = Character.MIN_VALUE;
      do {
      
      } while ((c1 = dC.d[C(b)]) > '\020');
      return c1;
    } 
    return dC.d[C(b)];
  }
  
  static void a(ac paramac, int paramInt) {
    if (paramac != null)
      x.b(paramac.a, paramac.b, paramac.c, paramac.d, paramInt); 
  }
  
  static void b(ac paramac, int paramInt) {
    if (paramac != null)
      x.a(paramac.a, paramac.b, paramac.c, paramac.d, paramInt); 
  }
  
  static void a(ac paramac, int paramInt1, int paramInt2) {
    x.b(paramac.a, paramac.b, paramac.c, paramac.d, paramInt2);
    x.a(paramac.a, paramac.b, paramac.c, paramac.d, paramInt1);
  }
  
  final void L() {
    if (ck == 1) {
      byte b;
      ck = 0;
      switch (bV) {
        case 12:
          at();
        case 0:
          Q();
        case 2:
          bb.a(1);
        case 3:
          bc.b(1);
        case 4:
          bc.k();
        case 5:
          K();
          for (b = 0; b < 81; b++)
            eE[b / 9][b % 9] = 1; 
          bd.c();
          bb.h();
        case 6:
        case 8:
        case 9:
          return;
        case 10:
          if ((ec == 0 && fD < eb[1] - eb[0]) || (ec != 0 && fD >= eb[1] - eb[0])) {
            bb.e();
            x.a(bu);
            if (ec != 0) {
              b("Prologue", 2 - dc, 9);
            } else {
              b("Epilogue", 2 - dc, 9);
            } 
            bb.b(fE);
            if (fA[0] > 0)
              e.a(0, 0, 1); 
            if (fA[1] > 0)
              e.a(1, 0, 1); 
            q(1);
          } else {
            N();
          } 
          if (cS.b != 0)
            cS.c(); 
          break;
      } 
      return;
    } 
    if (ck == 2) {
      switch (bV) {
        case 2:
          bb.a(2);
          return;
      } 
      return;
    } 
    switch (bV) {
      case 0:
        Q();
        return;
      case 2:
        bb.a(0);
        return;
      case 3:
        bc.b(0);
        return;
      case 4:
        bc.k();
        bc.n();
        return;
      case 5:
        bb.i();
        return;
      case 6:
        return;
      case 8:
        return;
      case 9:
        return;
      case 10:
        if (cS.b != 0)
          if (cS.j != 0) {
            cS.c();
            return;
          }  
        M();
    } 
  }
  
  final void M() {
    if (dS > 0) {
      dS = (short)(dS - 1);
      if (ch != -999 && dS > 3)
        dS = 3; 
      if (0 == dS) {
        fD++;
        if (fD < eb[2] - eb[0]) {
          bd.c(fD);
        } else if (0 == ec && cO == 0 && fD == eb[2] - eb[0]) {
          if (ef != 0 || eg != 0)
            cS.e(27); 
          bd.c(fD);
        } else {
          bI.a();
          bI = null;
          gf[1] = "";
          gf[0] = "";
          F();
          cM[0] = cO;
          ct[35] = null;
          ct[35] = null;
          ap();
          if (cM[0] == 0)
            cM[1] = 0; 
          bV = 2;
          cL = 0;
          cK = 0;
        } 
        ck = 1;
      } 
    } else if ((0 == ec && fD < eb[1] - eb[0]) || (ec != 0 && fD >= eb[1] - eb[0])) {
      e.a(fG, fA[fG], 0);
      if (fw[fG].length() <= fA[fG])
        if (ch != -999) {
          dS = 0;
        } else {
          dS = 15;
        }  
    } else {
      N();
      eh = (short)(eh + 1);
      switch (fG) {
        case 0:
          if (eh > 3) {
            fG = (short)(fG + 1);
            eh = 0;
          } 
          break;
        case 2:
          if (eh > 4)
            dS = 3; 
          break;
        case 1:
          fA[0] = fA[0] - 2;
          if (fA[0] < -28) {
            fA[0] = fA[0] + 22;
            fC[0] = fC[0] + 1;
            if (dq[0] < fC[0])
              if (fD == eb[2] - eb[0]) {
                dS = 3;
              } else {
                fG = (short)(fG + 1);
              }  
            eh = 1;
          } 
          break;
      } 
    } 
    if (ch == -6) {
      dS = 1;
      if (ec != 0) {
        if (fD >= eb[1] - eb[0]) {
          fD = 100;
          return;
        } 
      } else if (fD < eb[1] - eb[0]) {
        fD = eb[1] - eb[0] - 1;
      } 
    } 
  }
  
  final void d(int paramInt1, int paramInt2, int paramInt3) {
    x.b(0, 0, bZ.a, bZ.b, k(paramInt1, paramInt2, paramInt3));
  }
  
  final void N() {
    int j;
    int m;
    d(0, 0, 0);
    switch (fG) {
      case 0:
      case 2:
        if (eh > 0 && eh < 4)
          b(ct[35], dd - (ct[35].getWidth() >> 1), de - (ct[35].getHeight() >> 1), ct[35].getWidth(), ct[35].getHeight(), 0, 0); 
        break;
      case 1:
        m = fA[0];
        if (fD != eb[2] - eb[0])
          b(ct[35], dd - (ct[35].getWidth() >> 1), de - (ct[35].getHeight() >> 1), ct[35].getWidth(), ct[35].getHeight(), 0, 0); 
        for (j = fC[0]; j <= dq[0] && m <= 230; j++) {
          char c1;
          if (m > de + 72) {
            c1 = 255 - (m - de + 72 << 4);
          } else if (m < de - 72) {
            c1 = 255 - (de - 72 - m << 4);
          } else {
            c1 = 'ÿ';
          } 
          x.a(bv);
          b(dp[0][j], m + 1, 30);
          a(dp[0][j], m - 1, 1);
          if (c1 == 'ÿ') {
            x.a(bu);
          } else if (c1 == '\000') {
            x.a(bv);
          } else {
            x.a(bx);
          } 
          b(dp[0][j], m, 30);
          m += 22;
        } 
        break;
    } 
    q(2);
  }
  
  final void q(int paramInt) {
    h(0, -1);
  }
  
  final byte[] d(int paramInt1, int paramInt2) {
    return e(paramInt1, paramInt2).getBytes();
  }
  
  static String e(int paramInt1, int paramInt2) {
    String str = null;
    al al1;
    str = (al1 = new al("/" + bE.a(paramInt1))).a(paramInt2);
    al1.a();
    return str;
  }
  
  static int c(String paramString) {
    return bu.a(paramString);
  }
  
  static void O() {
    cz.s = cz.t = cz.u = cz.v = 0;
    for (byte b = 0; b < 9; b++) {
      if ((cz.X[b]).a != 0) {
        cz.s += (cz.X[b]).b;
        cz.t += (cz.X[b]).c;
        cz.u += (cz.X[b]).d;
        cz.v += (cz.X[b]).e;
      } 
    } 
    cz.w = cz.m + cz.s;
    cz.x = cz.n + cz.t;
    cz.y = cz.p = cz.o + cz.u;
    cz.z = cz.r = cz.q + cz.v;
  }
  
  public static int r(int paramInt) {
    int j = paramInt;
    if (paramInt != -7 && paramInt != -5 && paramInt != 53)
      if (paramInt == -1 || paramInt == 50) {
        bP = (bP + 28 - 14) % 28;
      } else if (paramInt == -2 || paramInt == 56) {
        bP = (bP + 28 + 14) % 28;
      } else if (paramInt == -3 || paramInt == 52) {
        bP = (bP + 28 - 1) % 28;
      } else if (paramInt == -4 || paramInt == 54) {
        bP = (bP + 28 + 1) % 28;
        if (bP == 27)
          bP = 0; 
      }  
    if (bP == 27)
      bP = 26; 
    return j;
  }
  
  public static void f(int paramInt1, int paramInt2) {
    int j = bL - 71;
    String[] arrayOfString = { 
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", 
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", 
        "U", "V", "W", "X", "Y", "Z", "OK" };
    x.b(j, paramInt2, 142, 34, 0);
    x.b(j + 123, paramInt2 + 18, 19, 15, 255);
    if (bN % 4 < 2)
      if (paramInt1 == 26) {
        x.b(j + 123, paramInt2 + 18, 19, 15, 16711680);
      } else {
        x.b(j + 2 + 10 * paramInt1 % 14, paramInt2 + 1 + 17 * paramInt1 / 14, 10, 15, 16711680);
      }  
    x.a(bu);
    for (byte b = 0; b < arrayOfString.length; b++) {
      byte b1;
      if (b == 8) {
        b1 = 1;
      } else if (b == 26) {
        b1 = 1;
      } else {
        b1 = 0;
      } 
      x.a(arrayOfString[b], j + 3 + b % 14 * 10 + b1, paramInt2 + 17 * b / 14, 0);
    } 
  }
  
  static int s(int paramInt) {
    int[] arrayOfInt = { 10, 100, 1000, 10000 };
    for (byte b = 0; b < 4 && paramInt >= arrayOfInt[b]; b++);
    return b + 1;
  }
  
  final void e(int paramInt1, int paramInt2, int paramInt3) {
    a(paramInt1, paramInt2, paramInt3, 9, 12, ct[20], 0, 0, 0);
  }
  
  final void a(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, Image paramImage, int paramInt6, int paramInt7, int paramInt8) {
    if (paramInt1 < 0 || paramImage == null)
      return; 
    paramInt2 -= paramInt4;
    if (paramInt1 > 0) {
      while (paramInt1 > 0) {
        a(paramInt2, paramInt3, paramInt4, paramInt5, paramImage, paramInt6 + paramInt4 * paramInt1 % 10, paramInt7);
        paramInt1 /= 10;
        paramInt2 -= paramInt4 + paramInt8;
      } 
      return;
    } 
    a(paramInt2, paramInt3, paramInt4, paramInt5, paramImage, paramInt6, paramInt7);
  }
  
  final void f(int paramInt1, int paramInt2, int paramInt3) {
    byte b1;
    byte b2;
    byte b3;
    byte b4;
    switch (paramInt1) {
      case 0:
        b3 = b4 = 0;
        b1 = 10;
        b2 = 16;
        break;
      case 1:
        b3 = 9;
        b4 = 0;
        b1 = 10;
        b2 = 16;
        break;
      case 2:
        b3 = 20;
        b4 = 0;
        b1 = 16;
        b2 = 10;
        break;
      case 3:
        b3 = 20;
        b4 = 9;
        b1 = 16;
        b2 = 10;
        break;
      default:
        return;
    } 
    a(paramInt2 + db, paramInt3 + dc, b1, b2, ct[17], b3, b4);
  }
  
  void a_(int paramInt) {
    if (bg != null)
      bg.a_(paramInt); 
  }
  
  final void P() {
    switch (bV) {
      case 12:
        L();
        if (System.currentTimeMillis() - c > 3000L) {
          bs.destroyApp(true);
          bs.notifyDestroyed();
        } 
        return;
      case 0:
        L();
        break;
      case 2:
        if (bg != null && cM[0] < 29 && k.a_ != ae.A[cM[0]] && cM[0] != 20 && !bp)
          a_(ae.A[cM[0]]); 
        if (cS.b != 0) {
          cS.b();
        } else {
          bb.a();
        } 
        L();
        break;
      case 3:
        bc.a();
        break;
      case 4:
        L();
        bc.O(0);
        break;
      case 5:
        L();
        bc.O(0);
        break;
      case 10:
        if (cS.b != 0)
          cS.b(); 
        L();
        break;
      case 11:
        if (be != null)
          as.aK(); 
        break;
    } 
    if (be != null && as.gu)
      be.j(); 
    cj = -999;
  }
  
  static void Q() {
    if (bf == null)
      bf = new af(); 
    bf.a();
  }
  
  void t(int paramInt) {
    if (paramInt == -10)
      return; 
    if (bS) {
      ch = paramInt;
      return;
    } 
    ci = paramInt;
    switch (paramInt) {
      case -4:
      case -3:
      case -2:
      case -1:
      case 50:
      case 52:
      case 54:
      case 56:
        cj = paramInt;
        break;
    } 
  }
  
  public final Image d(String paramString) {
    R();
    String str = "/" + paramString + ".png";
    Image image = null;
    try {
      image = Image.createImage(str);
    } catch (Throwable throwable) {
      System.out.println("======== createMixImage failuer :" + paramString);
      return null;
    } 
    R();
    return image;
  }
  
  public static void R() {
    System.gc();
  }
  
  public static void u(int paramInt) {
    x.b(0, 0, bJ, bK, paramInt);
  }
  
  final void S() {
    if (ct[30] == null)
      return; 
    a(0, 0, bZ.a, bZ.b, ct[30], 0, 0);
    if (cv == null)
      cv = d(bA.a(36)); 
    a(dd - 66 + db, bZ.b - 20, 132, 14, cv, 0, 0);
    if (cw == null)
      cw = d(bA.a(42)); 
    if (bN % 6 < 3 && bV == 0)
      a(dd - 55 + db, bZ.b - 60, 110, 14, cw, 0, 0); 
  }
  
  final void a(String paramString, int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, int paramInt6) {
    Image image = null;
    if ((image = d(paramString)) != null)
      a(paramInt1, paramInt2, paramInt3, paramInt4, image, paramInt5, paramInt6); 
  }
  
  final void T() {
    for (byte b = 0; b < 8; b++) {
      cz.ac[b] = ae.B[ae.aT[b]];
      cz.ad[b] = ae.C[ae.aT[b]];
      cz.ak[b] = ae.D[ae.aT[b]];
      cz.al[b] = ae.E[ae.aT[b]];
      cz.ae[b] = ae.F[ae.aT[b]];
      cz.af[b] = ae.G[ae.aT[b]];
      cz.ag[b] = ae.H[ae.aT[b]];
      cz.ah[b] = ae.I[ae.aT[b]];
      cz.ai[b] = ae.J[ae.aT[b]];
      cz.aj[b] = ae.K[ae.aT[b]];
      cz.am[b] = ae.L;
      cz.aA[b] = ae.M[ae.aT[b]];
      cz.an[b] = ae.N[ae.aT[b]];
      cz.ao[b] = ae.O[ae.aT[b]];
      cz.ap[b] = ae.P[ae.aT[b]];
      cz.aq[b] = ae.Q;
      cz.ar[b] = ae.R[ae.aT[b]];
      cz.as[b] = ae.S[ae.aT[b]];
      cz.at[b] = ae.T[ae.aT[b]];
      cz.au[b] = ae.U;
      cz.av[b] = ae.V[ae.aT[b]];
      cz.aw[b] = ae.W[ae.aT[b]];
      cz.ax[b] = ae.X;
      cz.ay[b] = ae.Y;
      cz.az[b] = ae.Z;
      eF[b][0] = ae.aa[ae.aT[b]];
      eF[b][1] = ae.ab[ae.aT[b]];
      eF[b][2] = ae.ac[ae.aT[b]];
      eF[b][3] = ae.ad[ae.aT[b]];
      eI[b] = eF[b];
      eG[b][0] = ae.ae[ae.aT[b]];
      eG[b][1] = ae.af[ae.aT[b]];
      eG[b][2] = ae.ag[ae.aT[b]];
      eG[b][3] = ae.ah[ae.aT[b]];
      eJ[b] = eG[b];
      eH[b][0] = ae.aa[ae.aT[b]];
      eH[b][1] = ae.ai[ae.aT[b]];
      eH[b][2] = ae.aj[ae.aT[b]];
      eH[b][3] = ae.ak;
      eH[b][4] = ae.ai[ae.aT[b]];
      eH[b][5] = ae.ai[ae.aT[b]];
      eH[b][6] = ae.N[ae.aT[b]];
      eH[b][7] = ae.O[ae.aT[b]];
      eH[b][8] = ae.P[ae.aT[b]];
      eH[b][9] = ae.Q;
      eH[b][10] = ae.Q;
      eH[b][11] = ae.Q;
      eH[b][12] = ae.Q;
      eH[b][13] = ae.Q;
      eH[b][14] = ae.R[ae.aT[b]];
      eH[b][15] = ae.S[ae.aT[b]];
      eH[b][16] = ae.T[ae.aT[b]];
      eH[b][17] = ae.U;
      eH[b][18] = ae.U;
      eH[b][19] = ae.V[ae.aT[b]];
      eH[b][20] = ae.W[ae.aT[b]];
      eH[b][21] = ae.W[ae.aT[b]];
      eK[b] = eH[b];
    } 
    eL[0] = eI;
    eL[1] = eJ;
    eL[2] = eI;
    eL[3] = eK;
    cz.ab[0] = cz.ac;
    cz.ab[1] = cz.ad;
    cz.ab[2] = cz.ak;
    cz.ab[3] = cz.ae;
    cz.ab[4] = cz.af;
    cz.ab[5] = cz.ag;
    cz.ab[6] = cz.ah;
    cz.ab[7] = cz.ai;
    cz.ab[8] = cz.aj;
    cz.ab[9] = cz.al;
    cz.ab[10] = cz.am;
    cz.ab[11] = cz.aA;
    cz.ab[12] = cz.an;
    cz.ab[13] = cz.ao;
    cz.ab[14] = cz.ap;
    cz.ab[15] = cz.aq;
    cz.ab[16] = cz.aq;
    cz.ab[17] = cz.aq;
    cz.ab[18] = cz.aq;
    cz.ab[19] = cz.aq;
    cz.ab[20] = cz.ar;
    cz.ab[21] = cz.as;
    cz.ab[22] = cz.at;
    cz.ab[23] = cz.au;
    cz.ab[24] = cz.au;
    cz.ab[25] = cz.av;
    cz.ab[26] = cz.aw;
    cz.ab[27] = cz.aw;
    cz.ab[28] = cz.ax;
    cz.ab[29] = cz.ay;
    cz.ab[30] = cz.az;
    bY.a = 240;
    bY.b = 243;
    cb.a = (short)(bY.a / 27 + ((bY.a % 27 > 0) ? 1 : 0));
    cb.a = (short)(cb.a + (((cb.a & 0x1) > 0) ? 0 : 1));
    cb.b = (short)(bY.b / 27 + ((bY.b % 27 > 0) ? 1 : 0));
    cb.b = (short)(cb.b + (((cb.b & 0x1) > 0) ? 0 : 1));
    cc.a = (short)(cb.a * 27 - bY.a >> 1);
    cc.b = (short)(cb.b * 27 - bY.b >> 1);
    bY.a = bZ.a;
    bY.b = bZ.b;
    db = 0;
    dc = 0;
    aa();
    q();
    a_(-1);
    dj = 0;
    w(0);
    cM[0] = 5;
    cN = 10;
    cS.e = 0;
    U();
    bV = 2;
    if (!aq())
      cM[1] = 1; 
  }
  
  final void U() {
    cG = 0;
    try {
      RecordStore recordStore;
      if ((recordStore = RecordStore.openRecordStore("gamevil_pow_data", false)) == null || recordStore.getNumRecords() < 1)
        return; 
      cF = recordStore.getRecord(1);
      cG = cF[0] & 0xFF | cF[1] << 8 & 0xFF00;
    } catch (Exception exception) {}
    if (cG != 0) {
      byte[] arrayOfByte1 = new byte[16];
      byte b2 = 0;
      for (b2 = 0; b2 < 8 && cF[2 + b2] != 32; b2++);
      byte[] arrayOfByte2 = new byte[b2];
      byte b1;
      for (b1 = 0; b1 < b2; b1++)
        arrayOfByte2[b1] = cF[2 + b1]; 
      cz.k = a(arrayOfByte2, 0, b2);
      dj = (short)cF[18];
      cG = 19;
      dk = (short)Y();
      dm = (short)Y();
      do = (short)Y();
      dw = V();
      dx = V();
      for (b1 = 0; b1 < 8; b1++)
        dy[b1] = W(); 
      dY = W();
      ed = W();
      for (b1 = 0; b1 < 44; b1++) {
        fn[0][b1] = (short)Y();
        fn[1][b1] = (short)Y();
      } 
      fo = (short)Y();
      for (b1 = 0; b1 < 25; b1++)
        fL[b1] = Z(); 
      cq = Y();
      (cz.a[0]).a = X();
      (cz.a[0]).b = X();
      (cz.a[0]).a = (short)(((cz.a[0]).a / 27 / 7 * 7 + 4) * 27 + 8);
      (cz.a[0]).b = (short)(((cz.a[0]).b / 27 / 7 * 7 + 4) * 27 + 8);
      for (b1 = 0; b1 < 22; b1++)
        cz.g[b1] = (short)Y(); 
      cz.h = (short)Y();
      cz.i = (short)Y();
      cz.l = Y();
      cz.m = X();
      cz.n = X();
      cz.o = X();
      cz.p = X();
      cz.q = X();
      cz.r = X();
      cz.E = W();
      if (bi)
        cz.E = 555000; 
      cz.F = W();
      cz.G = W();
      cz.H = X();
      cz.J = X();
      cz.S = Y();
      for (b1 = 0; b1 < 5; b1++)
        cz.V[b1] = Y(); 
      for (b1 = 0; b1 < 19; b1++)
        cz.W[b1] = Y(); 
      for (b1 = 0; b1 < 9; b1++)
        cz.X[b1] = Z(); 
      for (b1 = 0; b1 < 25; b1++)
        cz.Y[b1] = Z(); 
      for (b1 = 0; b1 < 5; b1++) {
        (cz.Z[b1]).a = X();
        (cz.Z[b1]).b = (short)Y();
      } 
      cz.aa[0] = Y();
      cz.aa[1] = Y();
      cz.aB = Y();
      dV = W();
      eo = W();
      fR = (short)Y();
      fS = (short)Y();
      dH = (short)Y();
      ep = (short)Y();
      for (b1 = 0; b1 < 16; b1++)
        arrayOfByte1[b1] = Y(); 
      fq = W();
      for (b1 = 0; b1 < 4; b1++)
        W(); 
    } 
    ag();
  }
  
  static long V() {
    long l1 = 0L;
    long l2 = 0L;
    l1 = cF[cG + 0] & 0xFFL | (cF[cG + 1] << 8) & 0xFF00L | (cF[cG + 2] << 16) & 0xFF0000L | (cF[cG + 3] << 24) & 0xFF000000L;
    l2 = cF[cG + 4];
    l1 |= l2 << 32L & 0xFF00000000L;
    l2 = cF[cG + 5];
    l1 |= l2 << 40L & 0xFF0000000000L;
    l2 = cF[cG + 6];
    l1 |= l2 << 48L & 0xFF000000000000L;
    l2 = cF[cG + 7];
    l1 |= l2 << 56L & 0xFF00000000000000L;
    cG += 8;
    return l1;
  }
  
  static int W() {
    int j = 0;
    j = cF[cG] & 0xFF | cF[cG + 1] << 8 & 0xFF00 | cF[cG + 2] << 16 & 0xFF0000 | cF[cG + 3] << 24 & 0xFF000000;
    cG += 4;
    return j;
  }
  
  static short X() {
    short s = 0;
    s = (short)(cF[cG] & 0xFF | cF[cG + 1] << 8 & 0xFF00);
    cG += 2;
    return s;
  }
  
  static byte Y() {
    byte b = (byte)(cF[cG] & 0xFF);
    cG++;
    return b;
  }
  
  final z Z() {
    z z1;
    (z1 = new z()).a = X();
    z1.b = X();
    z1.c = X();
    z1.d = X();
    z1.e = X();
    z1.f = Y();
    return z1;
  }
  
  final void aa() {
    ct[34] = d(bA.a(22));
    ct[19] = d(bA.a(24));
    ct[20] = d(bA.a(25));
    ct[0] = d(bA.a(48));
    ct[32] = d(bA.a(37));
  }
  
  final void ab() {
    int[] arrayOfInt = { 79, 61, 82, 78, 83, 81 };
    for (byte b = 0; b < 6; b++)
      cx[b] = d(bA.a(arrayOfInt[b])); 
  }
  
  final void ac() {
    for (byte b = 0; b < 6; b++)
      cx[b] = null; 
    R();
  }
  
  public static byte[] v(int paramInt) {
    return j.a("/" + bE.a(paramInt));
  }
  
  final void w(int paramInt) {
    ah();
    ae();
    if (ct[7] == null)
      ct[7] = Image.createImage(bZ.a, bZ.b); 
    cu = ct[7].getGraphics();
    dj = 0;
    cM[2] = 0;
    cM[1] = 0;
    cS.b = 0;
    cU = v(47);
    cW = v(49);
    cV = v(51);
    af();
    ct[17] = d(bA.a(27));
    x(paramInt);
    ag();
  }
  
  final void ad() {
    ct[1] = d(bA.a(21));
    ct[2] = d(bA.a(46));
    ct[3] = d(bA.a(43));
    fN = d(bA.a(38));
  }
  
  final void ae() {
    ct[1] = null;
    ct[2] = null;
    ct[3] = null;
    fN = null;
    R();
  }
  
  static void af() {
    al al1 = new al("/" + bE.a(69));
    for (byte b = 0; b < 30; b++) {
      fT[b] = al1.a(b);
      if (b < 7)
        gd[b] = al1.a(b + 48); 
      if (b < 6)
        fV[b] = al1.a(b + 30); 
      if (b < 5)
        ge[b] = al1.a(b + 55); 
      if (b < 4)
        gb[b] = al1.a(b + 42); 
      if (b < 2)
        gc[b] = al1.a(b + 46); 
    } 
    fU[0] = al1.a(36);
    fW[0] = al1.a(37);
    ga[0] = al1.a(38);
    fX[0] = al1.a(39);
    fY[0] = al1.a(40);
    fZ[0] = al1.a(41);
    al1.a();
  }
  
  final void x(int paramInt) {
    if (paramInt == 1)
      return; 
    x.a(cu);
    ct[11] = d(bA.a(60));
    ct[12] = d(bA.a(61));
    ct[16] = d(bA.a(63));
    ct[9] = d(bA.a(59));
    int j = ct[9].getWidth();
    int m = ct[9].getHeight();
    byte b;
    for (b = 0; b * m < bZ.b + m; b++) {
      for (byte b1 = 0; b1 < 4; b1++)
        c(ct[9], 0, 0, (b & 0x1) * -31 + b1 * j, b * m, j, m); 
    } 
    for (b = 0; b < 4; b++)
      c(ct[12], 0, 0, (bZ.a - ct[12].getWidth()) * b / 2, bZ.b / 2 * b % 2, ct[12].getWidth(), ct[12].getHeight()); 
    for (b = 0; b < 4; b++)
      c(ct[11], 0, 0, bZ.a / 2 * b % 2, (bZ.b - ct[11].getHeight()) * b / 2, ct[11].getWidth(), ct[11].getHeight()); 
    c(ct[16], 0, 0, (bZ.a >> 1) - ct[16].getWidth() / 2, 0, ct[16].getWidth(), ct[16].getHeight());
    ct[11] = null;
    ct[12] = null;
    ct[16] = null;
    ct[9] = null;
    x.a(br);
  }
  
  final void ag() {
    for (byte b = 0; b < 24; b++) {
      if ((cz.Y[b]).a == 0)
        for (int j = b + 1; j < 25; j++) {
          if ((cz.Y[j]).a != 0) {
            a(cz.Y[b], cz.Y[j]);
            break;
          } 
        }  
    } 
  }
  
  final void a(z paramz1, z paramz2) {
    z z1;
    b(z1 = new z(), paramz1);
    b(paramz1, paramz2);
    b(paramz2, z1);
  }
  
  static void b(z paramz1, z paramz2) {
    paramz1.a = paramz2.a;
    paramz1.b = paramz2.b;
    paramz1.c = paramz2.c;
    paramz1.d = paramz2.d;
    paramz1.e = paramz2.e;
    paramz1.f = paramz2.f;
  }
  
  final void ah() {
    eS[0] = null;
    eS[1] = null;
    cz.aD = null;
    cz.aF = null;
    eT[0] = null;
    eT[1] = null;
    ct[40] = null;
    ct[41] = null;
    if (bT != null) {
      for (byte b1 = 0; b1 < bT.length; b1++)
        bT[b1] = null; 
      bT = null;
    } 
    eU = null;
    ct[42] = null;
    eV = null;
    ct[43] = null;
    eR = null;
    eQ = null;
    eW = null;
    ct[44] = null;
    ct[31] = null;
    fe = null;
    eY = null;
    er[1] = null;
    byte b;
    for (b = 0; b < 2; b++)
      es[b] = null; 
    for (b = 0; b < 9; b++)
      et[b] = null; 
    eq = null;
    bY.a = bZ.a;
    bY.b = bZ.b;
    db = 0;
    dc = 0;
  }
  
  public static void a(int paramInt1, int paramInt2, int paramInt3, int paramInt4, Image paramImage, int paramInt5, int paramInt6) {
    x.a(paramImage, paramInt1, paramInt2, paramInt3, paramInt4, paramInt5, paramInt6);
  }
  
  public final void b(Image paramImage, int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, int paramInt6) {
    int i1;
    if ((i1 = paramInt2) > 0)
      i1 = 0; 
    int i2;
    if ((i2 = bY.b - paramInt2 - paramInt4) > 0)
      i2 = 0; 
    int j;
    if ((j = paramInt1) > 0)
      j = 0; 
    int m;
    if ((m = bY.a - paramInt1 - paramInt3) > 0)
      m = 0; 
    if (paramInt4 + i1 + i2 > 0 && paramInt3 + j + m > 0)
      a(paramInt1 + db - j, paramInt2 - i1 + dc, paramInt3 + j + m, paramInt4 + i1 + i2, paramImage, paramInt5 - j, paramInt6 - i1); 
  }
  
  public static void c(Image paramImage, int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, int paramInt6) {
    x.a(paramImage, paramInt3, paramInt4, paramInt5, paramInt6, paramInt1, paramInt2);
  }
  
  static void ai() {
    k.b();
  }
  
  static void aj() {
    cz.aC = null;
    cz.aE = null;
    cz.aG = null;
    cz.aH = null;
  }
  
  final void y(int paramInt) {
    switch (cM[1]) {
      case 0:
        df = !df;
        if (df) {
          a_(8);
          break;
        } 
        ai();
        break;
      case 1:
        if (paramInt == 1) {
          dg = (short)(dg + 25);
          if (dg > 100)
            dg = 0; 
        } else if (paramInt == 0) {
          dg = (short)(dg - 25);
          if (dg < 0 || dg > 100)
            dg = 100; 
        } 
        if (dg == 0) {
          df = false;
          ai();
          break;
        } 
        if (dg > 0) {
          df = true;
          if (System.currentTimeMillis() - di > 300L) {
            di = System.currentTimeMillis();
            a_(8);
          } 
        } 
        break;
      case 2:
        if (paramInt != 0) {
          dh = (short)(dh + 1);
          if (dh > 4)
            dh = 0; 
          break;
        } 
        dh = (short)(dh - 1);
        if (dh < 0)
          dh = 4; 
        break;
    } 
    H();
  }
  
  static void ak() {
    switch (cM[0]) {
      case 0:
        dE = fU;
        return;
      case 1:
        cN = dr;
        dE = dt;
        return;
      case 2:
        cN = dv[dk];
        dE = dA;
        return;
      case 7:
        cz.k = null;
        return;
      case 10:
        dE = fW;
        return;
      case 13:
        dE = fY;
        ct[39] = null;
        break;
    } 
  }
  
  final void al() {
    aj();
    ct[4] = null;
    if (bT != null) {
      for (byte b1 = 0; b1 < bT.length; b1++)
        bT[b1] = null; 
      bT = null;
    } 
    ct[9] = null;
    ct[11] = null;
    ct[12] = null;
    ct[16] = null;
    bb.d();
    byte b;
    for (b = 0; b < 5; b++)
      ct[35 + b] = null; 
    for (b = 0; b < 4; b++)
      ct[21 + b] = null; 
    bY.a = bZ.a;
    bY.b = bZ.b;
    db = 0;
    dc = 0;
  }
  
  final void am() {
    dK = 0;
    dP = 0;
    dQ = 0;
    dR = 0;
    dS = 0;
    ao();
    an();
    if (dI < 200)
      z(dI); 
  }
  
  final void z(int paramInt) {
    byte[] arrayOfByte1 = null;
    String str1 = "";
    int[] arrayOfInt = new int[60];
    String[] arrayOfString = new String[2];
    short s = dR;
    if ((dK & 0x1) != 0) {
      switch (dG) {
        case 0:
          str1 = dA[dm];
          break;
        case 2:
          if (cr != 0) {
            B((dz[dm]).f);
          } else {
            B((eO[eP]).o);
          } 
        case 1:
          str1 = dC.a;
          break;
      } 
    } else {
      str1 = cz.k;
    } 
    byte[] arrayOfByte2;
    int j = (arrayOfByte2 = arrayOfByte1 = v(57 + dG))[0] & 0xFF | arrayOfByte2[1] << 8 & 0xFF00;
    byte b1;
    for (b1 = 0; b1 < j + 1; b1++)
      arrayOfInt[b1] = arrayOfByte2[2 + b1 * 2] & 0xFF | arrayOfByte2[2 + b1 * 2 + 1] << 8 & 0xFF00; 
    arrayOfString[0] = a(arrayOfByte2, arrayOfInt[paramInt], arrayOfInt[paramInt + 1]);
    arrayOfString[1] = "[" + str1 + "] ";
    dD = arrayOfString[0].length();
    int m = 0;
    for (b1 = 0; b1 < dD; b1++) {
      if (arrayOfString[0].charAt(b1) == '&') {
        if (m != b1) {
          int i1 = arrayOfString[1].length();
          System.arraycopy(arrayOfString, m, arrayOfString[1], i1, b1 - m);
          b("=========================check this 96430jfds");
        } 
        arrayOfString[1] = arrayOfString[1] + str1;
        m = b1 + 1;
      } 
    } 
    String str2 = "";
    for (byte b2 = 0; b2 < arrayOfString[0].length(); b2++) {
      if (arrayOfString[0].charAt(b2) != '&')
        str2 = str2 + arrayOfString[0].charAt(b2); 
    } 
    arrayOfString[0] = str2;
    if (m < dD)
      arrayOfString[1] = arrayOfString[1] + arrayOfString[0]; 
    b(arrayOfString[1].getBytes(), 150, s);
  }
  
  final void an() {
    int j;
    switch (dG) {
      case 0:
        if (dH > 10) {
          dH = 11;
          dI = (short)(g(0, 18) + 10 << 1);
          return;
        } 
        dI = (short)(dH - 1 << 1);
        return;
      case 1:
        j = 0;
        e.b(dJ, -5);
        dI = 21;
        return;
      case 2:
        if (cr != 0) {
          j = (dz[dm]).f;
        } else {
          j = (eO[eP]).o;
        } 
        if (0 == j) {
          ck = 1;
          w(2);
          F();
          cM[0] = 0;
          cN = ae.v[cM[0]];
          dE = fU;
          dI = 200;
          bV = 2;
          cL = 0;
          cK = 0;
          return;
        } 
        e.b(j, 5);
        fq = j;
        if ((j = A(j)) >= 100)
          j = 95; 
        dI = (short)(j / 10 * 5);
        break;
    } 
  }
  
  static int A(int paramInt) {
    byte b;
    for (b = 0; b < fo && fn[0][b] != paramInt; b++);
    return (b == fo) ? 0 : fn[1][b];
  }
  
  static void ao() {
    dK = (short)(dK + 1);
    if (dG != 0) {
      dL[dR] = 60;
      dM[dR] = (short)(bY.b - 39);
    } else if ((dK & 0x1) != 0) {
      dL[dR] = (short)(dd - 60 + 15 + 2);
      dM[dR] = (short)(de - 64);
    } else {
      dL[dR] = (short)(dd - 60 + -40 + 2);
      dM[dR] = (short)(de - 73 + 107 + 2);
    } 
    dO = 0;
    dN = dL[dR];
  }
  
  final void B(int paramInt) {
    byte[] arrayOfByte = null;
    int j = 0;
    arrayOfByte = v(46);
    j = 23 * (paramInt - 1) + 14;
    dC.a = "";
    byte b;
    for (b = 0; b < 11 && arrayOfByte[j + b] != 0; b++);
    dC.a = a(arrayOfByte, j, j + b);
    dC.b = (char)arrayOfByte[j + 11];
    dC.c = (char)arrayOfByte[j + 11 + 2];
    dC.d[0] = (char)arrayOfByte[j + 11 + 3];
    dC.d[1] = (char)arrayOfByte[j + 11 + 4];
    dC.d[2] = (char)arrayOfByte[j + 11 + 5];
    dC.d[3] = (char)arrayOfByte[j + 11 + 6];
    dC.e = (char)arrayOfByte[j + 11 + 7];
    dC.f = (char)arrayOfByte[j + 11 + 8];
    dC.g = (char)arrayOfByte[j + 11 + 9];
    dC.h = (char)arrayOfByte[j + 11 + 10];
    dC.i = (char)arrayOfByte[j + 11 + 11];
    dC.c = (char)(dC.c + 1 & 0x1);
  }
  
  static void ap() {
    cN = ae.v[cM[0]];
    cM[1] = cP[cM[0]];
    cM[2] = cQ[cM[0]];
    ck = 1;
  }
  
  public static int g(int paramInt1, int paramInt2) {
    return paramInt1 + Math.abs(by.nextInt() % (Math.abs(--paramInt2 - paramInt1) + 1));
  }
  
  public final int C(int paramInt) {
    return g(0, paramInt);
  }
  
  public static void a(String paramString, int paramInt1, int paramInt2) {
    paramInt1 += 2;
    x.a(paramString, dd + db + paramInt2, paramInt1 + dc, 1);
  }
  
  public final void b(String paramString, int paramInt1, int paramInt2) {
    a(paramString, paramInt1, 0);
  }
  
  public static void c(String paramString, int paramInt1, int paramInt2) {
    x.a(paramString, paramInt1 + db, paramInt2 + dc, 1);
  }
  
  static void d(String paramString, int paramInt1, int paramInt2) {
    x.a(paramString, paramInt1 + db, paramInt2 + dc, 0);
  }
  
  final void a(int paramInt1, int paramInt2, int paramInt3, int paramInt4, boolean paramBoolean) {
    a(paramInt1, paramInt2, paramInt3, paramInt4, 0, 5263440, 16777215, paramBoolean);
  }
  
  static void a(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, int paramInt6, int paramInt7, boolean paramBoolean) {
    ac ac1 = new ac(0, 0, 0, 0);
    if (paramBoolean) {
      ac1.a = paramInt1 - 2;
      ac1.c = paramInt3 + 4;
      ac1.b = paramInt2 - 1;
      ac1.d = paramInt4 + 2;
      x.a(ac1.a, ac1.b, ac1.c, ac1.d, paramInt7);
      ac1.a++;
      ac1.c -= 2;
      ac1.b--;
      ac1.d += 2;
      x.a(ac1.a, ac1.b, ac1.c, ac1.d, paramInt7);
    } 
    ac1.a = paramInt1 - 1;
    ac1.c = paramInt3 + 2;
    ac1.b = paramInt2;
    ac1.d = paramInt4;
    x.a(ac1.a, ac1.b, ac1.c, ac1.d, paramInt6);
    ac1.a++;
    ac1.c -= 2;
    ac1.b--;
    ac1.d += 2;
    x.a(ac1.a, ac1.b, ac1.c, ac1.d, paramInt6);
    ac1.b++;
    ac1.d -= 2;
    x.b(ac1.a, ac1.b, ac1.c, ac1.d, paramInt5);
  }
  
  final void g(int paramInt1, int paramInt2, int paramInt3) {
    b(ct[19], paramInt2, paramInt3, 10, 14, 10 * paramInt1, 0);
  }
  
  final void h(int paramInt1, int paramInt2, int paramInt3) {
    byte b = 0;
    do {
      if (!b || b % 3 != 0)
        continue; 
      paramInt2 -= 4;
      a(paramInt2, paramInt3, 5, 14, ct[19], 100, 0);
      paramInt2 -= 10;
      a(paramInt2, paramInt3, 10, 14, ct[19], paramInt1 % 10 * 10, 0);
      ++b;
    } while ((paramInt1 /= 10) > 0);
  }
  
  final int d(int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    if (paramInt4 != 0) {
      byte b1 = 0;
      int m = paramInt1 / 10;
      paramInt2 += 9;
      while (m > 0) {
        m /= 10;
        b1++;
        paramInt2 += 9;
        if (b1 % 3 == 0)
          paramInt2 += 4; 
      } 
    } 
    int j = paramInt2;
    byte b = 0;
    while (true) {
      if (b % 3 == 0 && b != 0) {
        paramInt2 -= 4;
        b(ct[19], paramInt2, paramInt3, 5, 14, 100, 0);
      } 
      paramInt2 -= 9;
      b(ct[19], paramInt2, paramInt3, 10, 14, paramInt1 % 10 * 10, 0);
      b++;
      if ((paramInt1 /= 10) <= 0)
        return j; 
    } 
  }
  
  final void i(int paramInt1, int paramInt2, int paramInt3) {
    b(ct[20], paramInt1, paramInt2, 9, 12, paramInt3 * 9, 0);
  }
  
  static int D(int paramInt) {
    byte b = 1;
    for (int j = 10; paramInt >= j; j *= 10)
      b++; 
    return b;
  }
  
  final void j(int paramInt1, int paramInt2, int paramInt3) {
    int[] arrayOfInt1 = { 0, 9, 25, 34 };
    int[] arrayOfInt2 = { paramInt3 / 600 % 10, paramInt3 / 60 % 10, paramInt3 % 60 / 10, paramInt3 % 10 };
    for (byte b = 0; b < 4; b++)
      g(arrayOfInt2[b], paramInt1 + arrayOfInt1[b] + 10, paramInt2); 
    b(ct[19], paramInt1 + 20 + 10, paramInt2, 4, 14, 115, 0);
  }
  
  static int k(int paramInt1, int paramInt2, int paramInt3) {
    int j = 0;
    return j = (paramInt1 & 0xFF) << 16 | (paramInt2 & 0xFF) << 8 | paramInt3 & 0xFF;
  }
  
  static boolean aq() {
    try {
      RecordStore recordStore;
      return !((recordStore = RecordStore.openRecordStore("gamevil_pow_data", true)).getNumRecords() == 0);
    } catch (Exception exception) {
      return false;
    } 
  }
  
  final int ar() {
    boolean bool;
    char[] arrayOfChar = new char[16];
    byte[] arrayOfByte = cz.k.getBytes();
    byte b;
    for (b = 0; b < 8; b++) {
      if (b < arrayOfByte.length) {
        cF[2 + b] = arrayOfByte[b];
      } else {
        cF[2 + b] = 32;
      } 
    } 
    cF[18] = (byte)dj;
    cG = 19;
    G(dk);
    G(dm);
    G(do);
    a(dw);
    a(dx);
    for (b = 0; b < 8; b++)
      E((int)dy[b]); 
    E(dY);
    E(ed);
    for (b = 0; b < 44; b++) {
      G(fn[0][b]);
      G(fn[1][b]);
    } 
    G(fo);
    for (b = 0; b < 25; b++)
      a(fL[b]); 
    G(cq);
    F(((cd + 2) / 7 * 7 + 4) * 27);
    F(((ce + 2) / 7 * 7 + 4) * 27);
    for (b = 0; b < 22; b++)
      G(cz.g[b]); 
    G(cz.h);
    G(cz.i);
    G(cz.l);
    F(cz.m);
    F(cz.n);
    F(cz.o);
    F(cz.p);
    F(cz.q);
    F(cz.r);
    E(cz.E);
    E(cz.F);
    E(cz.G);
    F(cz.H);
    F(cz.J);
    G(cz.S);
    for (b = 0; b < 5; b++)
      G(cz.V[b]); 
    for (b = 0; b < 19; b++)
      G(cz.W[b]); 
    for (b = 0; b < 9; b++)
      a(cz.X[b]); 
    for (b = 0; b < 25; b++)
      a(cz.Y[b]); 
    for (b = 0; b < 5; b++) {
      F((cz.Z[b]).a);
      G((cz.Z[b]).b);
    } 
    G(cz.aa[0]);
    G(cz.aa[1]);
    G(cz.aB);
    E((int)(dW[0] - dV));
    E((int)eo);
    G(fR);
    G(fS);
    G(dH);
    G(ep);
    for (b = 0; b < 16; b++)
      G(arrayOfChar[b]); 
    E(fq);
    for (b = 0; b < 4; b++)
      E(0); 
    cF[0] = (byte)(cG & 0xFF);
    cF[1] = (byte)(cG >> 8 & 0xFF);
    try {
      RecordStore recordStore;
      if ((recordStore = RecordStore.openRecordStore("gamevil_pow_data", true)).getNumRecords() == 0)
        recordStore.addRecord(cF, 0, cF.length); 
      recordStore.setRecord(1, cF, 0, cF.length);
    } catch (Exception exception) {}
    if (aq()) {
      bool = true;
    } else {
      bool = false;
    } 
    return bool;
  }
  
  static void a(long paramLong) {
    cF[cG] = (byte)(int)(paramLong & 0xFFL);
    cF[cG + 1] = (byte)(int)(paramLong >> 8L & 0xFFL);
    cF[cG + 2] = (byte)(int)(paramLong >> 16L & 0xFFL);
    cF[cG + 3] = (byte)(int)(paramLong >> 24L & 0xFFL);
    cF[cG + 4] = (byte)(int)(paramLong >> 32L & 0xFFL);
    cF[cG + 5] = (byte)(int)(paramLong >> 40L & 0xFFL);
    cF[cG + 6] = (byte)(int)(paramLong >> 48L & 0xFFL);
    cF[cG + 7] = (byte)(int)(paramLong >> 56L & 0xFFL);
    cG += 8;
  }
  
  static void E(int paramInt) {
    cF[cG] = (byte)(paramInt & 0xFF);
    cF[cG + 1] = (byte)(paramInt >> 8 & 0xFF);
    cF[cG + 2] = (byte)(paramInt >> 16 & 0xFF);
    cF[cG + 3] = (byte)(paramInt >> 24 & 0xFF);
    cG += 4;
  }
  
  static void F(int paramInt) {
    cF[cG] = (byte)(paramInt & 0xFF);
    cF[cG + 1] = (byte)(paramInt >> 8 & 0xFF);
    cG += 2;
  }
  
  static void G(int paramInt) {
    cF[cG] = (byte)(paramInt & 0xFF);
    cG++;
  }
  
  final void a(z paramz) {
    F(paramz.a);
    F(paramz.b);
    F(paramz.c);
    F(paramz.d);
    F(paramz.e);
    G(paramz.f);
  }
  
  final void as() {
    bV = 12;
    ck = 1;
    dr = 0;
    ai();
    c = System.currentTimeMillis();
  }
  
  final void at() {
    if (bN == 2 || bN == 5)
      ai(); 
    u(0);
    Image image;
    int j = (image = d(bA.a(0))).getWidth();
    a(bL - j / 2, bM - 10, j, 20, image, 0, 0);
    a(bL - j / 2, bK - 24, j, 22, image, 0, 20);
  }
  
  public static int a(byte paramByte) {
    int j;
    return j = bu.a((char)paramByte);
  }
  
  public static String a(byte[] paramArrayOfbyte, int paramInt1, int paramInt2) {
    int j = paramInt1;
    int m = paramInt2;
    String str = null;
    try {
      int i1;
      byte[] arrayOfByte;
      (arrayOfByte = new byte[(i1 = m - j) + 2])[0] = (byte)(i1 >> 8 & 0xFF);
      arrayOfByte[1] = (byte)(i1 & 0xFF);
      System.arraycopy(paramArrayOfbyte, j, arrayOfByte, 2, i1);
      ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(arrayOfByte, 0, arrayOfByte.length);
      DataInputStream dataInputStream;
      str = (dataInputStream = new DataInputStream(byteArrayInputStream)).readUTF();
      byteArrayInputStream.close();
      dataInputStream.close();
    } catch (Exception exception) {}
    return str;
  }
  
  static void h(int paramInt1, int paramInt2) {
    if (cS.b != 0)
      return; 
    int j = bU.getWidth();
    int m = bU.getHeight();
    String str = "";
    if (paramInt1 != -1) {
      x.a(bu);
      x.a(bU, 0, bK - m);
      int i1;
      int i2;
      if ((i2 = (i1 = (str + ae.t[paramInt1]).length() * 10) + 4 - bU.getWidth()) > 0) {
        x.b(j - 8, bK - m + 2, 8, 13, 0);
        x.a(bU, i2, bK - m);
        x.b(i2, bK - m + 2, 8, 13, 0);
        x.a(str + ae.t[paramInt1], (j + i2) / 2, bK - m, 1);
      } else {
        x.a(str + ae.t[paramInt1], j / 2, bK - m, 1);
      } 
    } 
    if (paramInt2 != -1) {
      x.a(bu);
      x.a(bU, bJ - j - 0, bK - m);
      int i1;
      int i2;
      if ((i2 = (i1 = (str + ae.t[paramInt2]).length() * 10) + 15 - bU.getWidth()) > 0) {
        x.b(bJ - j - 0, bK - m + 2, 8, 13, 0);
        x.a(bU, bJ - j - i2 - 0, bK - m);
        x.b(bJ - i2 - 0 - 8, bK - m + 2, 8, 13, 0);
        x.a(str + ae.t[paramInt2], bJ - (j + i2) / 2 - 0, bK - m, 1);
        return;
      } 
      x.a(str + ae.t[paramInt2], bJ - j / 2 - 0, bK - m, 1);
    } 
  }
  
  static int H(int paramInt) {
    int[] arrayOfInt = new int[10];
    byte b = 0;
    paramInt += cz.G;
    while (true) {
      int j;
      if ((j = b % 10) == 0)
        arrayOfInt = bb.p(); 
      if (paramInt < (j = arrayOfInt[j])) {
        cz.G = paramInt;
        return b;
      } 
      paramInt -= j;
      cz.l++;
      cz.J += 3;
      b++;
    } 
  }
  
  final int b(byte[] paramArrayOfbyte, int paramInt1, int paramInt2) {
    int j = 0;
    int m = 0;
    int i1 = 0;
    int i2 = 0;
    byte b = 0;
    dq[paramInt2] = 0;
    dp[paramInt2] = new String[120];
    for (j = 0; j <= paramArrayOfbyte.length; j++) {
      if (j != paramArrayOfbyte.length) {
        i2 += a(paramArrayOfbyte[j]);
        if ((paramArrayOfbyte[j] == 32 || paramArrayOfbyte[j] == 124) && i2 - a(paramArrayOfbyte[j]) >= paramInt1) {
          if (i1 < m)
            i1 = j; 
          dp[paramInt2][b] = a(paramArrayOfbyte, m, i1);
          b++;
          j = (m = i1 + 1) - 1;
          i2 = 0;
        } else if (paramArrayOfbyte[j] == 32) {
          i1 = j;
        } else if (paramArrayOfbyte[j] == 124) {
          dp[paramInt2][b] = a(paramArrayOfbyte, m, j);
          b++;
          m = i1 = j + 1;
          i2 = 0;
        } 
      } else if (i2 > paramInt1) {
        dp[paramInt2][b] = a(paramArrayOfbyte, m, i1);
        dp[paramInt2][++b] = a(paramArrayOfbyte, i1 + 1, j);
        b++;
      } else if (i1 != paramArrayOfbyte.length - 1) {
        dp[paramInt2][b] = a(paramArrayOfbyte, m, j);
        b++;
      } 
    } 
    if (b >= 1)
      dq[paramInt2] = (byte)(b - 1); 
    return 1;
  }
  
  final void a(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, int paramInt6, int paramInt7) {
    l(paramInt5, paramInt6, paramInt7);
    f(paramInt1, paramInt2, paramInt1 + paramInt3 - 1, paramInt2);
    f(paramInt1, paramInt2 + 1, paramInt1, paramInt2 + paramInt4 - 1);
    f(paramInt1 + paramInt3 - 1, paramInt2, paramInt1 + paramInt3 - 1, paramInt2 + paramInt4 - 1);
    f(paramInt1 + 1, paramInt2 + paramInt4 - 1, paramInt1 + paramInt3 - 2, paramInt2 + paramInt4 - 1);
  }
  
  static String e(String paramString) {
    int j;
    int m;
    for (m = (j = paramString.length()) - 1; m >= 0 && paramString.charAt(m) == ' '; m--);
    return (m == 0) ? "" : paramString.substring(0, m + 1);
  }
  
  static String f(String paramString) {
    byte b = 0;
    int j = paramString.length();
    for (b = 0; b < j && paramString.charAt(b) >= ' '; b++);
    return (b == 0) ? "" : paramString.substring(0, b);
  }
  
  static String g(String paramString) {
    byte b = 0;
    int j = paramString.length();
    for (b = 0; b < j && paramString.charAt(b) != ' '; b++);
    return (b == 0) ? "" : paramString.substring(0, b);
  }
  
  final void i(int paramInt1, int paramInt2) {
    ac ac1 = new ac(paramInt1 + 1, paramInt2 + 1, 28, 28);
    b(paramInt1, paramInt2, 30, 30, 80, 80, 80);
    x.b(ac1.a, ac1.b, ac1.c, ac1.d, 0);
  }
  
  final void e(int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    ac ac1 = new ac(paramInt1 + 1, paramInt2 + 1, paramInt3 - 2, paramInt4 - 2);
    b(paramInt1, paramInt2, paramInt3, paramInt4, 152, 152, 152);
    x.b(ac1.a, ac1.b, ac1.c, ac1.d, 0);
  }
  
  final void b(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, int paramInt6, int paramInt7) {
    l(paramInt5, paramInt6, paramInt7);
    f(paramInt1 + 1, paramInt2, paramInt1 + paramInt3 - 2, paramInt2);
    f(paramInt1, paramInt2 + 1, paramInt1, paramInt2 + paramInt4 - 2);
    f(paramInt1 + paramInt3 - 1, paramInt2 + 1, paramInt1 + paramInt3 - 1, paramInt2 + paramInt4 - 2);
    f(paramInt1 + 1, paramInt2 + paramInt4 - 1, paramInt1 + paramInt3 - 2, paramInt2 + paramInt4 - 1);
  }
  
  final void c(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, int paramInt6, int paramInt7) {
    l(paramInt5, paramInt6, paramInt7);
    f(paramInt1 + 1, paramInt2, paramInt1 + paramInt3 - 2, paramInt2);
    f(paramInt1, paramInt2 + 1, paramInt1, paramInt2 + paramInt4 - 2);
    f(paramInt1 + paramInt3 - 1, paramInt2 + 1, paramInt1 + paramInt3 - 1, paramInt2 + paramInt4 - 2);
    f(paramInt1 + 1, paramInt2 + paramInt4 - 1, paramInt1 + paramInt3 - 2, paramInt2 + paramInt4 - 1);
    j(paramInt1 + 1, paramInt2 + 1);
    j(paramInt1 + paramInt3 - 2, paramInt2 + 1);
    j(paramInt1 + 1, paramInt2 + paramInt4 - 2);
    j(paramInt1 + paramInt3 - 2, paramInt2 + paramInt4 - 2);
  }
  
  final void l(int paramInt1, int paramInt2, int paramInt3) {
    bO = k(paramInt1, paramInt2, paramInt3);
  }
  
  static void f(int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    x.c(paramInt1, paramInt2, paramInt3, paramInt4, bO);
  }
  
  final void j(int paramInt1, int paramInt2) {
    f(paramInt1, paramInt2, paramInt1 + 1, paramInt2 + 1);
  }
  
  final void au() {
    bb.c();
    cM[0] = 29;
    cN = ae.v[cM[0]];
    cM[1] = 1;
    cz.aB = 0;
    av();
  }
  
  final void av() {
    dj = 0;
    dH = 0;
    dw = 35113052110447L;
    dx = 0L;
    ed = 0;
    cq = 0;
    cz.aB = 0;
    cz.k = "";
    byte b;
    for (b = 0; b < 45; b++) {
      fn[1][b] = 0;
      fn[0][b] = 0;
    } 
    fo = 0;
    for (b = 0; b < 8; b++)
      dy[b] = 0L; 
    cz.l = 1;
    aw();
    cz.F = 0;
    cz.E = 0;
    cz.G = 0;
    cz.S = 0;
    for (b = 0; b < 22; b++)
      cz.g[b] = 0; 
    cz.h = 0;
    cz.i = 0;
    for (b = 0; b < 5; b++) {
      cz.V[b] = 0;
      (cz.Z[b]).a = 0;
      (cz.Z[b]).b = 0;
    } 
    for (b = 0; b < 19; b++)
      cz.W[b] = 0; 
    cz.W[0] = 1;
    cz.W[5] = 1;
    cz.V[0] = 12;
    cz.V[1] = 17;
    if (bi) {
      for (b = 0; b < 19; b++)
        cz.W[b] = 1; 
      cz.W[18] = 1;
    } 
    for (b = 0; b < 9; b++)
      cz.X[b].a(); 
    for (b = 0; b < 25; b++)
      cz.Y[b].a(); 
    k(116, 0);
    a(cz.X[0], cz.Y[0]);
    cz.aa[0] = 0;
    cz.aa[1] = 1;
  }
  
  static void aw() {
    cz.m = 5;
    cz.n = 4;
    cz.o = 30;
    cz.p = 30;
    cz.q = 10;
    cz.r = 10;
    cz.J = 5;
    ck = 1;
  }
  
  final int k(int paramInt1, int paramInt2) {
    byte b = 0;
    if (paramInt1 < 100) {
      if (paramInt2 != 0) {
        byte b1 = -1;
        for (b = 0; b < 5; b++) {
          if ((cz.Z[b]).a == paramInt1) {
            if ((cz.Z[b]).b > 4)
              return 0; 
            break;
          } 
          if (0 == (cz.Z[b]).a && b1 < 0)
            b1 = b; 
        } 
        if (b1 > -1 && b > 4)
          b = b1; 
        if (b > 4)
          return 0; 
      } else {
        if (((cz.Z[dU.e]).b = (short)((cz.Z[dU.e]).b - 1)) < 1)
          (cz.Z[dU.e]).a = 0; 
        return 1;
      } 
    } else if (paramInt1 < 10000) {
      for (b = 0; b < 25 && 0 != (cz.Y[b]).a; b++);
      if (b > 24)
        return 0; 
      (cz.Y[b]).a = (short)paramInt1;
      (cz.Y[b]).b = 0;
      (cz.Y[b]).c = 0;
      (cz.Y[b]).d = 0;
      (cz.Y[b]).e = 0;
      (cz.Y[b]).f = 0;
    } 
    if (paramInt1 < 10000)
      bb.e(paramInt1); 
    if (paramInt1 < 100) {
      (cz.Z[b]).a = (short)paramInt1;
      (cz.Z[b]).b = (short)((cz.Z[b]).b + 1);
    } else if (paramInt1 < 300) {
      short s;
      if (paramInt2 != 0) {
        s = (short)(cX.d + C(cX.e + 1));
      } else {
        s = cX.d;
      } 
      switch (cX.c) {
        case 0:
          (cz.Y[b]).b = s;
          break;
        case 1:
          (cz.Y[b]).c = s;
          break;
        case 2:
          (cz.Y[b]).d = s;
          break;
        case 3:
          (cz.Y[b]).e = s;
          break;
      } 
    } else if (paramInt1 < 500) {
      (cz.Y[b]).b = cY.c;
      (cz.Y[b]).c = (short)cY.d;
      (cz.Y[b]).d = cY.e;
      (cz.Y[b]).e = (short)cY.f;
    } else if (paramInt1 < 10000) {
      (cz.Y[b]).b = cZ.c;
      (cz.Y[b]).c = (short)cZ.d;
      (cz.Y[b]).d = cZ.e;
      (cz.Y[b]).e = (short)cZ.f;
    } else {
      cz.E += paramInt1 - 10000;
    } 
    return 1;
  }
  
  static void ax() {
    for (byte b = 0; b < 8; b++) {
      if (fL[b] == null)
        fL[b] = new z(); 
    } 
    (fL[0]).a = 1;
    (fL[1]).a = 2;
    (fL[2]).a = 3;
    (fL[3]).a = 4;
    (fL[4]).a = 5;
    (fL[5]).a = 6;
    (fL[6]).a = 10;
    (fL[7]).a = 11;
  }
  
  final void ay() {
    int[] arrayOfInt = new int[17];
    az();
    byte b;
    for (b = 0; b < 17; b++)
      arrayOfInt[b] = 101 + 5 * g(0, 20) + I(g(0, 100)); 
    for (b = 16; b > 0; b--) {
      boolean bool = false;
      for (byte b1 = 0; b1 < b; b1++) {
        if (arrayOfInt[b1] > arrayOfInt[b1 + 1]) {
          int j = arrayOfInt[b1];
          arrayOfInt[b1] = arrayOfInt[b1 + 1];
          arrayOfInt[b1 + 1] = j;
          bool = true;
        } 
      } 
      if (!bool)
        break; 
    } 
    for (b = 0; b < 17; b++)
      fL[8 + b] = J(arrayOfInt[b]); 
  }
  
  static boolean az() {
    int[] arrayOfInt = { 47, 51, 49 };
    if (!fM[1]) {
      for (byte b = 0; b < 3; b++) {
        if (bH[b] == null)
          bH[b] = new d("/" + bE.a(arrayOfInt[b])); 
        if (bH[b] == null)
          return false; 
      } 
      fM[1] = true;
    } 
    return true;
  }
  
  static int I(int paramInt) {
    int m = 0;
    byte b;
    for (b = 0; b < 5 && cz.l >= ae.w[b]; b++);
    int j = ae.x[b - 1];
    for (b = 0; b < 4 && paramInt >= (m += j & 0xFF); b++)
      j >>= 8; 
    return b;
  }
  
  final z J(int paramInt) {
    z z1 = new z();
    int[] arrayOfInt = new int[5];
    z1.a = (short)paramInt;
    z1.f = 0;
    if (paramInt < 300) {
      for (byte b = 0; b < 3; b++)
        arrayOfInt[b] = bH[0].a(paramInt - 101, 2 + b); 
      if (arrayOfInt[0] == 0) {
        z1.b = (short)(arrayOfInt[1] + C(arrayOfInt[2]));
      } else if (arrayOfInt[0] == 1) {
        z1.c = (short)(arrayOfInt[1] + C(arrayOfInt[2]));
      } else if (arrayOfInt[0] == 2) {
        z1.d = (short)(arrayOfInt[1] + C(arrayOfInt[2]));
      } else if (arrayOfInt[0] == 3) {
        z1.e = (short)(arrayOfInt[1] + C(arrayOfInt[2]));
      } 
    } else if (paramInt < 500) {
      for (byte b = 0; b < 4; b++)
        arrayOfInt[b] = bH[1].a(paramInt - 301, 2 + b); 
      z1.b = (short)arrayOfInt[0];
      z1.c = (short)arrayOfInt[1];
      z1.d = (short)arrayOfInt[2];
      z1.e = (short)arrayOfInt[3];
    } else {
      for (byte b = 0; b < 4; b++)
        arrayOfInt[b] = bH[2].a(paramInt - 301, 2 + b); 
      z1.b = (short)arrayOfInt[0];
      z1.c = (short)arrayOfInt[1];
      z1.d = (short)arrayOfInt[2];
      z1.e = (short)arrayOfInt[3];
    } 
    return z1;
  }
  
  final void aA() {
    aj();
    cz.aG = d(bB.a(46 + cz.aB));
    cz.aC = K(47 + cz.aB);
    cz.aH = d(bB.a(44));
    cz.aE = K(45);
  }
  
  final y[] K(int paramInt) {
    byte b1 = 1;
    byte[] arrayOfByte;
    y[] arrayOfY = new y[(arrayOfByte = j.a("/" + bF.a(paramInt)))[0] & 0xFF];
    for (byte b2 = 0; b2 < (arrayOfByte[0] & 0xFF); b2++) {
      arrayOfY[b2] = new y();
      (arrayOfY[b2]).a = a(arrayOfByte[b1], arrayOfByte[b1 + 1]);
      (arrayOfY[b2]).b = a(arrayOfByte[b1 + 2], arrayOfByte[b1 + 3]);
      (arrayOfY[b2]).c = a(arrayOfByte[b1 + 4], arrayOfByte[b1 + 5]);
      (arrayOfY[b2]).d = a(arrayOfByte[b1 + 6], arrayOfByte[b1 + 7]);
      (arrayOfY[b2]).e = a(arrayOfByte[b1 + 8], arrayOfByte[b1 + 9]);
      (arrayOfY[b2]).f = a(arrayOfByte[b1 + 10], arrayOfByte[b1 + 11]);
      b1 += 12;
    } 
    return arrayOfY;
  }
  
  static short b(byte paramByte) {
    return (short)(paramByte & 0xFF);
  }
  
  final void l(int paramInt1, int paramInt2) {
    byte b;
    ee = (short)paramInt1;
    if (paramInt1 < 100) {
      ec = 0;
      b = 64 + paramInt1 / 6;
      for (byte b1 = 0; b1 < 3; b1++)
        eb[b1] = ae.aV[(paramInt1 << 1) + b1] - ae.aV[paramInt1 / 6 * 12]; 
      if (paramInt1 == 3 && paramInt2 != 0 && 0 == L(502)) {
        eb[2] = 0;
        eb[1] = 0;
        eb[0] = 0;
        cq = 4;
      } 
      fE = -1;
    } else {
      ec = 1;
      b = 63;
      eb[0] = 0;
      eb[1] = 2;
      eb[2] = 13;
      fE = 0;
      dE = fU;
      cO = 0;
    } 
    if (bI == null)
      bI = new al("/" + bE.a(b)); 
    gf[1] = "";
    gf[0] = "";
    fA[1] = 0;
    fA[0] = 0;
    fD = 0;
    dS = 0;
    fG = 0;
    bd.c(fD);
    if (0 == ec)
      x(1); 
    bV = 10;
    a_(2);
    ck = 1;
  }
  
  static int L(int paramInt) {
    for (byte b = 0; b < 25; b++) {
      if ((cz.Y[b]).a == paramInt)
        return b + 1; 
    } 
    return 0;
  }
  
  static String M(int paramInt) {
    return bG.a(paramInt);
  }
  
  static int a(char[] paramArrayOfchar) {
    String str = "";
    for (byte b = 0; b < paramArrayOfchar.length && paramArrayOfchar[b] >= '0' && paramArrayOfchar[b] <= '9'; b++)
      str = str + paramArrayOfchar[b]; 
    return Integer.parseInt(str);
  }
  
  public static int N(int paramInt) {
    switch (paramInt) {
      case 48:
        return 0;
      case 49:
        return 1;
      case 50:
        return 2;
      case 51:
        return 3;
      case 52:
        return 4;
      case 53:
        return 5;
      case 54:
        return 6;
      case 55:
        return 7;
      case 56:
        return 8;
      case 57:
        return 9;
    } 
    return -1;
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\ag.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */