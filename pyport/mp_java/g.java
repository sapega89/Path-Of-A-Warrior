/*
 * Decompiled with CFR 0.152.
 * 
 * Could not load the following classes:
 *  javax.microedition.lcdui.Canvas
 *  javax.microedition.lcdui.Graphics
 *  javax.microedition.lcdui.Image
 *  javax.microedition.rms.RecordStore
 */
import java.io.ByteArrayInputStream;
import java.io.DataInputStream;
import java.util.Random;
import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;
import javax.microedition.rms.RecordStore;

/*
 * Illegal identifiers - consider using --renameillegalidents true
 */
public class g
extends Canvas
implements Runnable,
l {
    public static String a;
    public static m b;
    public static String c;
    public static int d;
    public static Graphics e;
    public static Image f;
    public static Graphics g;
    public static Random h;
    public static String i;
    public static String j;
    public static int k;
    public static Main l;
    public static int m;
    public static j n;
    public static j o;
    public static j p;
    public static j q;
    public static String r;
    public static int s;
    public static String t;
    public static boolean u;
    public static long v;
    public static boolean w;
    public static boolean x;
    public static int y;
    public static int z;
    public static boolean A;
    public static int B;
    public static int C;
    public static boolean D;
    public static int E;
    public static long F;
    public static boolean G;
    public static int H;
    public static int I;
    public static boolean J;
    public static boolean K;
    public static boolean L;
    public static long M;
    public static long N;
    public static boolean O;
    public static boolean P;
    public static int Q;
    public static int R;
    public static int S;
    public static int T;
    public static int U;
    public static int V;
    public static int W;
    public static int X;
    public static String[] Y;
    public static int[] Z;
    public static int[] aa;
    public static int ab;
    public static int[] ac;
    public static int ad;
    public static byte ae;
    public static int af;
    public static String ag;
    public static String ah;
    public static String ai;
    public static String aj;
    public static String ak;
    public static int al;
    public static int am;
    public static int an;
    public static int ao;
    public static int ap;
    public static boolean aq;
    public static byte ar;
    public static int as;
    public static int at;
    public static int au;
    public static int av;
    public static int aw;
    public static int ax;
    public static int ay;
    public static int az;
    public static int aA;
    public static int aB;
    public static int aC;
    public static int aD;
    public static int aE;
    public static int aF;
    public static int aG;
    public static int aH;
    public static int aI;
    public static int aJ;
    public static int aK;
    public static int aL;
    public static int aM;
    public static byte aN;
    public static int aO;
    public static int aP;
    public static int aQ;
    public static int aR;
    public static int aS;
    public static int aT;
    public static int aU;
    public static int aV;
    public static byte aW;
    public static int aX;
    public static int aY;
    public static int aZ;
    public static int ba;
    public static int bb;
    public static int bc;
    public static int bd;
    public static int be;
    public static int bf;
    public static int bg;
    public static byte bh;
    public static boolean bi;
    public static boolean bj;
    public static boolean bk;
    public static int bl;
    public static int bm;
    public static boolean bn;
    public static int bo;
    public static int bp;
    public static boolean bq;
    public static boolean br;
    public static boolean bs;
    public static boolean bt;
    public static int bu;
    public static int bv;
    public static boolean bw;
    public static boolean bx;
    public static int by;
    public static byte bz;
    public static int bA;
    public static int bB;
    public static int bC;
    public static int bD;
    public static byte[] bE;
    public static String[] bF;
    public static String bG;
    public static String bH;
    public static String bI;
    public static int bJ;
    public static int bK;
    public static String bL;
    public static String[] bM;
    public static String[] bN;
    public static String[] bO;
    public static String[] bP;
    public static boolean[] bQ;
    public static int[] bR;
    public static int[] bS;
    public static int[] bT;
    public static int[] bU;
    public static int[] bV;
    public static int[] bW;
    public static int[] bX;
    public static int[] bY;
    public static byte[] bZ;
    public static int[] ca;
    public static int[] cb;
    public static int[] cc;
    public static int[] cd;
    public static int[] ce;
    public static int[] cf;
    public static int[] cg;
    public static int[] ch;
    public static int[] ci;
    public static int[] cj;
    public static int[] ck;
    public static int[] cl;
    public static int[] cm;
    public static int[] cn;
    public static int[] co;
    public static int[] cp;
    public static int[] cq;
    public static int[] cr;
    public static int cs;
    public static int ct;
    public static int cu;
    public static int cv;
    public static int cw;
    public static int cx;
    public static int cy;
    public static int cz;
    public static int cA;
    public static byte[] cB;
    public static int cC;
    public static int cD;
    public static String cE;
    public static String cF;
    public static String cG;
    public static int[] cH;
    public static int[] cI;
    public static int[] cJ;
    public static byte[] cK;
    public static int cL;
    public static int cM;
    public static int cN;
    public static int cO;
    public static int cP;
    public static int cQ;
    public static int cR;
    public static int cS;
    public static int cT;
    public static int cU;
    public static int cV;
    public static int cW;
    public static int cX;
    public static int cY;
    public static int cZ;
    public static int da;
    public static int db;
    public static int dc;
    public static Image[] dd;
    public static Image[] de;
    public static Image[] df;
    public static Image[] dg;
    public static Image[] dh;
    public static Image[] di;
    public static Image[] dj;
    public static Image dk;
    public static Image dl;
    public static Image dm;
    public static Image dn;
    public static Image do;
    public static Image dp;
    public static Image dq;
    public static Image dr;
    public static Image ds;
    public static Image dt;
    public static Image[] du;
    public static a[] dv;
    public static Image[][] dw;
    public static a[][] dx;
    public static Image[][] dy;
    public static a[][] dz;
    public static Image[][] dA;
    public static a[][] dB;
    public static Image[][] dC;
    public static a[][] dD;
    public static a[] dE;
    public static Image[] dF;
    public static a[] dG;
    public static Image[] dH;
    public static a[] dI;
    public static Image[] dJ;
    public static a[] dK;
    public static Image[] dL;
    public static a[] dM;
    public static Image[] dN;
    public static a[] dO;
    public static h dP;
    public static int dQ;
    public static int dR;
    public static int dS;
    public static Thread dT;
    public static int[] dU;
    public static int[] dV;
    public static int dW;
    public static boolean dX;
    public static boolean dY;
    public static int dZ;
    public static boolean ea;
    public static boolean eb;
    public static int ec;
    public static String[] ed;
    public static long ee;

    public static void a(String string) {
        System.out.println(string);
    }

    public g(Main main) {
        l = main;
        this.setFullScreenMode(true);
    }

    public final void a() {
        g.dV[0] = 1;
        cS = cQ = this.getWidth();
        cT = cR = this.getHeight();
        try {
            a = l.getAppProperty("MIDlet-Version");
            r = l.getAppProperty("GAMEVIL_SERVER");
            s = Integer.parseInt(l.getAppProperty("GAMEVIL_PORT"));
            t = l.getAppProperty("GAMEVIL_GAME_VER");
        }
        catch (Exception exception) {
            a = "";
            r = "64.14.246.182";
            s = 28200;
            t = "0111";
        }
        f = Image.createImage((int)cQ, (int)cR);
        g = f.getGraphics();
        cW = cQ / 2;
        cX = cR / 2;
        bK = cQ / 2 - 28 - 3;
        int n2 = 0;
        while (n2 < 4) {
            g.bP[n2] = "";
            ++n2;
        }
        n = new j("/0_font.png", 5, 11, 6, 0xFFFFFF);
        o = new j("/0_font.png", 5, 11, 6, 16400640);
        p = new j("/0_font.png", 5, 11, 6, 0x646464);
        q = new j("/0_font.png", 5, 11, 6, 0x41FF41);
        this.f();
        this.L();
        b = new m(l);
        g.X();
        g.i(0);
    }

    public final Image b(String string) {
        Image image = null;
        try {
            image = Image.createImage((String)string);
        }
        catch (Exception exception) {
            g.a("--------createImage err:" + exception);
        }
        return image;
    }

    public static void a(Graphics graphics) {
        int n2 = 80 / k;
        if (n2 > 30) {
            n2 = 30;
        } else if (n2 < 19) {
            n2 = 19;
        }
        int n3 = 0;
        if (cY == 162 || cY == 163 || cY == 164) {
            n3 = 15;
        } else if (cY == 10) {
            n3 = 40;
        }
        f.a(graphics, do, (cQ - n2 * (k - 1) - 11) / 2 + n2 * dU[dW], cX + 6 + n3, 12, 15, 0, 0);
    }

    public synchronized void paint(Graphics graphics) {
        e = graphics;
        i.a(graphics);
        if (w) {
            dY = true;
            return;
        }
        this.d();
        if (graphics.getClipX() > 0) {
            graphics.setClip(0, 0, cQ, cR);
        }
        dY = true;
    }

    static void a(long l2) {
        if (l2 > 0L) {
            try {
                Thread.sleep(l2);
                return;
            }
            catch (Exception exception) {}
        }
    }

    public static void a(int n2) {
        H = n2;
    }

    public final void b() {
        if (!K || L) {
            H = 0;
            return;
        }
        if (H != 0 && H == 1 != J) {
            if (H == 1) {
                J = true;
                if (b != null) {
                    I = m.fd;
                    this.ag();
                }
            } else if (H == 2) {
                J = false;
                if (b != null && I != -1) {
                    this.t(I);
                }
            }
        }
        H = 0;
    }

    public void run() {
        g g2 = this;
        synchronized (g2) {
            this.a();
        }
        this.c();
        g.a(250L);
    }

    final void c() {
        ee = System.currentTimeMillis();
        while (true) {
            ee = System.currentTimeMillis();
            if (J) {
                if (m != -999) {
                    this.f(m);
                    m = -999;
                }
                dY = false;
                this.repaint();
                g.a(250L);
            } else {
                long l2;
                int n2;
                if (m != -999) {
                    this.f(m);
                    m = -999;
                }
                dY = false;
                this.repaint();
                this.serviceRepaints();
                while (!dY) {
                    g.a(10L);
                }
                if (b != null) {
                    if (cY >= 10 && cY <= 89 && cY != 88 && !J || cY == 1 || cY == 6 || cY == 7) {
                        this.s(1);
                    }
                    b.ak();
                }
                if (cZ == cY && da < 25000) {
                    ++da;
                }
                if (da >= 25000) {
                    da = 100;
                }
                if ((n2 = l.ef[an] - (int)((l2 = System.currentTimeMillis()) - ee)) > 20) {
                    g.a((long)n2);
                } else {
                    g.a(20L);
                }
            }
            this.b();
            K = true;
        }
    }

    /*
     * Unable to fully structure code
     */
    final void d() {
        if (g.dY) {
            return;
        }
        if (g.cY != 3 && g.cY != 10000) {
            g.L = false;
        }
        if (g.J) {
            f.b(g.e, 0, 0, g.cS, g.cT, 0);
            this.c(g.e, g.cW, g.cX, 100, 29, 0);
            this.a(g.e, l.eX[2], g.cW, g.cX - 6, 1, 0xFFFFFF);
            return;
        }
        if (h.j && !g.eb) {
            if (h.h > 100) {
                h.h = 0;
                this.c(39327);
                if (++g.dZ > 20) {
                    g.dZ = 0;
                    g.cw = 13;
                    g.x = false;
                    this.o();
                }
            } else {
                ++h.h;
            }
        }
        if (!g.D) {
            if (g.d == 1) {
                g.d = 0;
                if (g.cY == 97) {
                    if ((g.cA += g.cz) > g.cW - 44 + 72 + g.cz) {
                        g.cA = g.cW - 44 + 72 + g.cz;
                    } else {
                        g.b(1);
                    }
                } else {
                    if (--g.ba == 0) {
                        g.bB = 1;
                        g.cA = g.cW - 44 + 72 + g.cz;
                        this.C();
                    }
                    g.b(10 - g.an);
                }
            } else if (g.d > 0) {
                --g.d;
            }
        }
        g.cZ = g.cY;
        block1 : switch (g.cY) {
            case 0: {
                if (g.da < 2) {
                    g.da = 2;
                    try {
                        g.ds = this.b("/gamevillogo.png");
                        g.dt = this.b("/softbg.png");
                        g.dS = (g.cR - (g.ds.getHeight() + 12)) / 2;
                        g.ds.getHeight();
                        g.ds.getWidth();
                    }
                    catch (Exception v0) {}
                    g.M = System.currentTimeMillis();
                    f.b(g.g, 0, 0, g.cQ, g.cR, 0xFFFFFF);
                }
                this.e();
                f.a(g.e, g.ds, g.cQ / 2, g.dS, 17);
                if (System.currentTimeMillis() - g.M <= 3000L) break;
                g.ds = null;
                g.cY = 5;
                return;
            }
            case 161: {
                if (g.da < 2) {
                    g.da = 2;
                    g.c = l.eM[5];
                    g.k = 3;
                    this.U();
                }
                this.e();
                this.a(g.e, l.eR[g.dU[g.dW]], g.cW - 43, g.cX - 19, 86, 17, false, true);
                g.a(g.e);
                this.c(-1, 1);
                return;
            }
            case 162: 
            case 163: 
            case 164: {
                if (g.da < 2) {
                    g.da = 2;
                    g.c = l.eR[g.cY - 162];
                    g.k = 2;
                    this.U();
                    g.cO = g.cQ - 96 >> 1;
                    g.c(g.g, g.cO, g.cX - 54, 96, 15);
                    this.a(g.g, g.i, g.cQ / 2 + 4, g.cX + 2 - 54, 1, 0xFFFFFF);
                    g.c(g.g, g.cO, g.cX + 14 - 54, 96, 15);
                    this.a(g.g, l.eX[4], g.cO + 3, g.cX + 14 + 2 - 54, 0, 0xFFFFFF);
                    g.b(g.g, g.cO + 96 - 7, g.cX + 14 + 3 - 54, g.ac[g.ae], 0);
                    switch (g.cY) {
                        case 162: {
                            var1_1 = l.eR[0];
                            break;
                        }
                        default: {
                            var1_1 = l.eX[3];
                        }
                    }
                    g.c(g.g, g.cO, g.cX + 28 - 54, 96, 15);
                    this.a(g.g, var1_1, g.cO + 3, g.cX + 28 + 2 - 54, 0, 0xFFFFFF);
                    g.b(g.g, g.cO + 96 - 7, g.cX + 28 + 3 - 54, g.ad, 0);
                }
                this.e();
                this.a(g.e, l.eS[g.dU[g.dW]], g.cW - 43, g.cX - 19 + 15, 86, 17, false, true);
                g.a(g.e);
                this.c(-1, 1);
                return;
            }
            case 170: 
            case 171: {
                if (g.da < 2) {
                    g.da = 2;
                    g.c = l.eS[g.cY - 170];
                    this.l(g.g);
                    var1_2 = g.cQ - 110 >> 1;
                    var2_7 = g.cR >> 1;
                    switch (g.af) {
                        case 162: {
                            var3_14 = l.eR[0];
                            break;
                        }
                        case 163: {
                            var3_14 = l.eX[3];
                            break;
                        }
                        default: {
                            var3_14 = l.eX[3];
                        }
                    }
                    var4_16 = 0;
                    while (var4_16 < 3) {
                        this.a(g.g, g.Y[var4_16], g.cW, var2_7 - 65 + 45 * var4_16, 1, 0xFFFFFF);
                        g.c(g.g, var1_2, var2_7 - 52 + 45 * var4_16, 110, 15);
                        g.c(g.g, var1_2, var2_7 - 38 + 45 * var4_16, 110, 15);
                        this.a(g.g, l.eX[4], var1_2 + 3, var2_7 - 52 + 2 + 45 * var4_16, 0, 0xFFFFFF);
                        g.b(g.g, var1_2 + 110 - 7, var2_7 - 52 + 2 + 1 + 45 * var4_16, g.Z[var4_16], 0);
                        this.a(g.g, var3_14, var1_2 + 3, var2_7 - 38 + 2 + 45 * var4_16, 0, 0xFFFFFF);
                        g.b(g.g, var1_2 + 110 - 7, var2_7 - 38 + 2 + 1 + 45 * var4_16, g.aa[var4_16], 0);
                        ++var4_16;
                    }
                }
                this.e();
                this.c(-1, 1);
                return;
            }
            case 90: {
                if (g.O) {
                    this.W();
                    this.Y();
                    g.O = false;
                }
                if (g.da < 2) {
                    g.da = 2;
                    g.bk = false;
                }
                if (g.bj) {
                    if (g.ca[g.ct] == 0) {
                        g.bk = true;
                    }
                    this.m(g.g);
                    g.bj = false;
                }
                this.e();
                this.c(g.e);
                if (g.bk) {
                    this.y();
                    break;
                }
                this.af();
                return;
            }
            case 91: {
                this.e();
                this.c(g.e);
                this.z();
                if (g.da != 1500 / g.dc) break;
                this.c(1038);
                return;
            }
            case 92: {
                if (g.da < 2) {
                    g.da = 2;
                }
                this.e();
                this.c(g.e);
                if (g.da >= 500 / g.dc && g.da < 1500 / g.dc) {
                    this.b(g.e, 0);
                } else if (g.da >= 1500 / g.dc) {
                    this.b(g.e, 1);
                }
                if (g.da != 2500 / g.dc) break;
                g.aR = 0;
                g.i(93);
                return;
            }
            case 93: {
                if (g.da < 2) {
                    g.X();
                    g.da = 2;
                    ++g.aR;
                    if (g.bb == 0 || g.bc == 0 || g.bW[0] == 0) {
                        g.i(103);
                    } else {
                        g.Q();
                    }
                } else if (g.da == 1000 / g.dc) {
                    this.c(1025);
                }
                this.e();
                this.c(g.e);
                if (g.aR > 0 && g.aR < 100 && g.bb != 0 && g.bc != 0 && g.bW[0] != 0) {
                    this.i(g.e);
                    this.d(g.e, 2);
                    this.S();
                }
                return;
            }
            case 94: {
                if (g.da < 2) {
                    g.da = 2;
                    g.bt = false;
                }
                this.e();
                if (g.D) {
                    g.dZ = 1;
                    --g.da;
                    this.c(g.e, g.cW, g.cX, 120, 100, 0);
                    this.a(g.e, g.cW, g.cX - 21 - 10, l.eX[60], 0xFFFFFF);
                    this.a(g.e, g.cW, g.cX - 21 + 2, l.eX[61], 0xFFFFFF);
                    this.a(g.e, g.cW, g.cX - 21 + 14, l.eX[62], 0xFFFFFF);
                    var1_3 = (int)(15L - (System.currentTimeMillis() - g.F) / 1000L);
                    this.a(g.e, g.cW, g.cX - 21 + 30, l.eX[63] + "   ", 0xFFFFFF);
                    this.a(g.e, g.cW + 35, g.cX - 21 + 30, "" + var1_3, 16400640);
                    var2_8 = 0;
                    while (var2_8 < 2) {
                        if (g.E == var2_8) {
                            this.a(g.e, l.eX[40 + var2_8], g.cW - 28 + var2_8 * 55, g.cX + 28, 1, 0xFFFFFF);
                            this.c(g.e, g.cW - 42 + var2_8 * 55, g.cX + 25, 29, 14, 3);
                        } else {
                            this.c(g.e, g.cW - 42 + var2_8 * 55, g.cX + 25, 29, 14, 2);
                            this.a(g.e, l.eX[40 + var2_8], g.cW - 28 + var2_8 * 55, g.cX + 28, 1, 0x646464);
                        }
                        ++var2_8;
                    }
                    if (var1_3 > 0) break;
                    g.D = false;
                    break;
                }
                this.c(g.e);
                g.j(g.e);
                this.d(g.e, 0);
                return;
            }
            case 95: {
                if (g.da < 2) {
                    g.da = 2;
                    g.db = 0;
                }
                this.e();
                this.c(g.e);
                this.h(g.e);
                this.d(g.e, 1);
                return;
            }
            case 96: {
                if (g.da < 2) {
                    g.da = 2;
                    switch (g.bB) {
                        case 9: 
                        case 10: {
                            g.bA = 0;
                            if (g.bb > 1) break;
                            this.B();
                            return;
                        }
                        case 0: 
                        case 3: 
                        case 4: 
                        case 5: 
                        case 6: 
                        case 7: {
                            g.cL = 1;
                            while (g.cL < 4) {
                                if (g.bQ[g.cL] && g.bR[g.cL] % 2 != g.bR[0] % 2) {
                                    g.bA = g.cL;
                                    break;
                                }
                                ++g.cL;
                            }
                            if (g.bc > 1) break;
                        }
                        default: {
                            this.B();
                        }
                    }
                }
                this.e();
                this.c(g.e);
                g.j(g.e);
                this.d(g.e);
                this.d(g.e, 1);
                return;
            }
            case 97: {
                this.e();
                if (g.da < 2) {
                    g.da = 2;
                    if (g.bB > 2) {
                        this.c(g.e);
                        g.j(g.e);
                        this.C();
                        return;
                    }
                    this.c(g.e);
                    g.j(g.e);
                    g.A();
                    this.e(g.e);
                    this.f(g.e);
                    return;
                }
                if (g.da > 0) {
                    this.c(g.e);
                    g.j(g.e);
                    this.e(g.e);
                    this.f(g.e);
                    return;
                }
                this.c(g.e);
                g.j(g.e);
                this.e(g.e);
                this.f(g.e);
                return;
            }
            case 98: {
                this.e();
                if (g.da < 2) {
                    g.da = 2;
                    this.c(g.e);
                    g.j(g.e);
                    this.e(g.e);
                    if (g.bB <= 2 && g.bt) {
                        this.f(g.e);
                    }
                } else if (g.da == 4) {
                    this.c(g.e);
                    g.j(g.e);
                    this.e(g.e);
                    this.c(1027);
                } else {
                    this.c(g.e);
                    g.j(g.e);
                    if (g.da < 4) {
                        this.e(g.e);
                    }
                }
                if (g.da < 4) break;
                this.d(g.e, 2);
                this.S();
                return;
            }
            case 99: {
                this.e();
                if (g.da < 2) {
                    g.da = 2;
                }
                this.c(g.e);
                this.R();
                if (g.da < 4) {
                    return;
                }
                g.bC = 0;
                this.E();
                return;
            }
            case 100: {
                this.e();
                this.c(g.e);
                this.c(g.e, g.cW, g.cX - 25, 80, 20, 0);
                this.a(g.e, g.cW, g.cX - 6 - 25, l.eX[8], 0xFFFFFF);
                if (g.da < 2) {
                    g.da = 2;
                    return;
                }
                if (g.da != 1000 / g.dc) break;
                g.i(93);
                return;
            }
            case 101: {
                this.e();
                this.c(g.e);
                this.k();
                g.i(102);
                return;
            }
            case 102: {
                this.e();
                this.s();
                this.R();
                this.I();
                ++g.Q;
                this.D();
                return;
            }
            case 103: {
                this.e();
                this.c(g.e);
                if (g.da >= 2) break;
                g.da = 2;
                this.c(1025);
                return;
            }
            case 104: {
                this.e();
                if (g.da < 2) {
                    g.da = 2;
                    g.du[0] = null;
                    g.du[1] = null;
                    var1_4 = 0;
                    while (var1_4 < 3) {
                        if (g.dv[var1_4] != null) {
                            g.dv[var1_4].a();
                        }
                        g.dv[var1_4] = null;
                        ++var1_4;
                    }
                    var1_4 = 0;
                    while (var1_4 < 10) {
                        g.dw[var1_4][0] = null;
                        g.dw[var1_4][1] = null;
                        var2_9 = 0;
                        while (var2_9 < 3) {
                            if (g.dx[var1_4][var2_9] != null) {
                                g.dx[var1_4][var2_9].a();
                            }
                            g.dx[var1_4][var2_9] = null;
                            ++var2_9;
                        }
                        ++var1_4;
                    }
                    var1_4 = 0;
                    while (var1_4 < 2) {
                        g.dy[var1_4][0] = null;
                        g.dy[var1_4][1] = null;
                        var2_9 = 0;
                        while (var2_9 < 3) {
                            if (g.dz[var1_4][var2_9] != null) {
                                g.dz[var1_4][var2_9].a();
                            }
                            g.dz[var1_4][var2_9] = null;
                            ++var2_9;
                        }
                        ++var1_4;
                    }
                    g.X();
                }
                if (g.da < 1000 / g.dc) {
                    this.c(g.e);
                    this.H();
                    return;
                }
                if (g.da == 1000 / g.dc) {
                    this.c(g.e);
                    g.cL = 1;
                    while (g.cL < 4) {
                        if (g.bQ[g.cL] && g.bR[g.cL] % 2 != g.bR[0] % 2) {
                            g.bQ[g.cL] = false;
                        }
                        ++g.cL;
                    }
                    g.bc = 0;
                    this.c(1036);
                    g.cL = 0;
                    while (g.cL < 4) {
                        g.cp[g.cL] = 99;
                        g.cq[g.cL] = 0;
                        ++g.cL;
                    }
                    g.i(90);
                    g.O = true;
                    return;
                }
                this.c(g.e);
                return;
            }
            case 105: {
                this.e();
                if (g.da < 5) {
                    g.da = 5;
                    this.i();
                    if (g.aU == 1) {
                        this.t(5);
                    } else {
                        this.t(4);
                    }
                }
                if (g.da < 1500 / g.dc) {
                    g.g(g.e);
                    this.c(g.e);
                    this.b(g.e, 2);
                    return;
                }
                if (g.da < 1500 / g.dc) break;
                g.g(g.e);
                this.c(g.e);
                this.P();
                return;
            }
            case 10: {
                if (g.da < 2) {
                    g.da = 2;
                    var1_5 = 0;
                    while (var1_5 < g.de.length) {
                        g.de[var1_5] = null;
                        ++var1_5;
                    }
                    this.i();
                    g.c = l.eX[9];
                    g.k = 6;
                    this.U();
                }
                this.e();
                f.a(g.e, g.dd[g.dU[g.dW]], g.cW - 40, g.cX - 59, 0);
                this.a(g.e, l.eM[g.dU[g.dW]], g.cW - 39, g.cX + 21, 78, 17, false, true);
                g.a(g.e);
                if (g.x) {
                    this.v(g.e);
                    break;
                }
                this.c(5, 2);
                return;
            }
            case 11: {
                if (g.da < 2) {
                    g.da = 2;
                    g.c = l.eM[0];
                    g.k = 3;
                    this.U();
                }
                f.a(g.e, g.f, 0, 0, 0);
                this.a(g.e, l.eN[g.dU[g.dW]], g.cW - 39, g.cX - 19, 78, 17, false, true);
                g.a(g.e);
                this.c(-1, 1);
                return;
            }
            case 12: {
                if (g.da < 2) {
                    g.da = 2;
                    g.c = l.eM[1];
                    g.k = 2;
                    this.U();
                }
                this.e();
                this.a(g.e, l.eO[g.dU[g.dW]], g.cW - 45, g.cX - 19, 90, 17, false, true);
                g.a(g.e);
                this.c(-1, 1);
                return;
            }
            case 16: {
                if (g.da < 2) {
                    g.da = 2;
                    g.c = l.eM[2];
                    g.k = 6;
                    this.U();
                }
                this.e();
                this.a(g.e, l.eP[g.dU[g.dW]], g.cW - 45, g.cX - 19, 90, 17, false, true);
                g.a(g.e);
                this.c(-1, 1);
                return;
            }
            case 20: {
                if (g.da < 2) {
                    g.da = 2;
                    g.k = 2;
                    this.w(g.g);
                }
                this.e();
                g.cL = 0;
                while (g.cL < 2) {
                    if (g.dU[g.dW] == g.cL) {
                        this.c(g.e, g.cW - 56, g.cX - 16 + g.cL * 20, 111, 14, 3);
                        this.a(g.e, l.eX[38 + g.cL], g.cS / 2, g.cX - 15 + g.cL * 20, 1, 0xFFFFFF);
                    }
                    ++g.cL;
                }
                this.c(-1, 1);
                return;
            }
            case 21: {
                var1_6 = g.cX - 48;
                if (g.da < 2) {
                    g.da = 2;
                    g.C = 0;
                    g.bG = "";
                    this.f(g.g, var1_6);
                }
                this.e();
                this.a(g.e, g.cW, var1_6 + 61, g.bG, 0x41FF41);
                g.a(g.C, var1_6 + 75);
                if (g.da % 4 < 2) {
                    var2_10 = g.n.a(g.bG);
                    if (g.bG.length() == 12) {
                        var2_10 -= g.n.a("A") * 2;
                    }
                    g.b(g.e, g.cW + var2_10 / 2, var1_6 + 71, g.cW + var2_10 / 2 + 4, var1_6 + 71, 0xFFFFFF);
                }
                if (g.bG.length() == 0) {
                    this.c(4, 1);
                    break;
                }
                this.c(4, 3);
                return;
            }
            case 80: {
                if (g.da < 2) {
                    g.da = 2;
                    g.c = l.eP[0];
                }
                this.Z();
                this.c(-1, 1);
                return;
            }
            case 81: {
                if (g.da < 2) {
                    g.da = 2;
                    g.c = l.eP[1];
                }
                this.aa();
                this.c(-1, 1);
                return;
            }
            case 82: {
                if (g.da < 2) {
                    g.da = 2;
                    g.c = l.eP[2];
                    this.p(g.g);
                }
                this.e();
                this.ab();
                this.c(-1, 1);
                return;
            }
            case 83: {
                if (g.da < 2) {
                    g.da = 2;
                    g.c = l.eP[3];
                }
                this.ac();
                this.c(-1, 1);
                return;
            }
            case 84: {
                if (g.da < 2) {
                    g.C = 0;
                    g.da = 2;
                    g.c = l.eP[4];
                    this.q(g.g);
                }
                this.e();
                this.r(g.e);
                if (g.bG.length() == 0) {
                    this.c(4, 1);
                    break;
                }
                this.c(4, 3);
                return;
            }
            case 88: {
                if (g.da < 2) {
                    g.da = 2;
                    g.c = l.eM[3];
                    g.k = 3;
                    this.o(g.g);
                }
                this.e();
                g.cL = 0;
                while (g.cL < 3) {
                    if (g.dU[g.dW] != g.cL) ** GOTO lbl606
                    this.a(g.e, l.eW[g.cL], g.cW - 28, g.cX - 15 + g.cL * 19, 1, 0xFFFFFF);
                    switch (g.cL) {
                        case 0: {
                            this.a(g.e, l.eW[3 + g.an], g.cW + 33, g.cX - 15, 1, 0xFFFFFF);
                            break;
                        }
                        case 1: {
                            v1 = this;
                            v2 = g.e;
                            v3 = l.eW;
                            v4 = 8;
                            v5 = g.ap;
                            ** GOTO lbl599
                        }
                        case 2: {
                            if (g.ah() > 0) {
                                var2_11 = 0;
                                while (var2_11 < g.ah()) {
                                    f.b(g.e, g.cW + 21 + 5 * var2_11, g.cX - 13 + g.cL * 19, 3, 8, 0xFFFFFF);
                                    ++var2_11;
                                }
                                break;
                            }
                            v1 = this;
                            v2 = g.e;
                            v3 = l.eW;
                            v4 = 6;
                            v5 = g.ah() > 0 ? 0 : 1;
lbl599:
                            // 2 sources

                            v1.a(v2, v3[v4 + v5], g.cW + 33, g.cX - 15 + g.cL * 19, 1, 0xFFFFFF);
                        }
                    }
                    this.c(g.e, g.cW - 58, g.cX - 16 + g.cL * 19, 61, 14, 3);
                    this.c(g.e, g.cW + 13, g.cX - 16 + g.cL * 19, 39, 14, 3);
                    if (g.da % 4 < 2) {
                        g.c(g.cW + 6, g.cX - 13 + g.cL * 19, g.di[1]);
                        g.b(g.cW + 59, g.cX - 13 + g.cL * 19, g.di[1]);
                    }
                    ** GOTO lbl631
lbl606:
                    // 1 sources

                    switch (g.cL) {
                        case 0: {
                            this.a(g.e, l.eW[3 + g.an], g.cW + 33, g.cX - 15, 1, 0x646464);
                            break;
                        }
                        case 1: {
                            v6 = this;
                            v7 = g.e;
                            v8 = l.eW;
                            v9 = 8;
                            v10 = g.ap;
                            ** GOTO lbl630
                        }
                        case 2: {
                            if (g.ah() > 0) {
                                var2_11 = 0;
                                while (var2_11 < g.ah()) {
                                    f.b(g.e, g.cW + 21 + 5 * var2_11, g.cX - 13 + g.cL * 19, 3, 8, 0x646464);
                                    ++var2_11;
                                }
                                break;
                            }
                            v6 = this;
                            v7 = g.e;
                            v8 = l.eW;
                            v9 = 6;
                            v10 = g.ah() > 0 ? 0 : 1;
lbl630:
                            // 2 sources

                            v6.a(v7, v8[v9 + v10], g.cW + 33, g.cX - 15 + g.cL * 19, 1, 0x646464);
                        }
                    }
lbl631:
                    // 5 sources

                    ++g.cL;
                }
                this.c(-1, 1);
                return;
            }
            case 7: {
                if (g.da < 2) {
                    g.da = 2;
                    g.c = l.eX[64];
                    this.k(g.g);
                }
                this.e();
                this.c(g.e, g.cW, g.cX, 112, 48, 0);
                this.a(g.e, g.cW, g.cX - 18, l.eX[64] + "!", 0xFFFFFF);
                this.a(g.e, g.cW, g.cX - 6, g.i, 0xFFFFFF);
                this.r(g.cX + 9);
                return;
            }
            case 6: {
                if (g.da < 2) {
                    g.da = 2;
                    g.c = l.eX[18];
                    this.k(g.g);
                }
                this.r();
                return;
            }
            case 3: {
                this.e();
                if (g.da > 20000 / g.dc) {
                    g.cw = 7;
                    this.o();
                    return;
                }
                this.ae();
                return;
            }
            case 10000: {
                this.e();
                if (g.da == 1) {
                    this.m();
                }
                if (g.da > 20000 / g.dc) {
                    g.cw = 7;
                    this.o();
                    return;
                }
                this.ae();
                return;
            }
            case 4: {
                this.e();
                this.ad();
                if (g.x) {
                    this.v(g.e);
                    break;
                }
                if (g.cw == 7 || g.cw == 1) {
                    this.c(5, 2);
                }
                return;
            }
            case 5: {
                f.b(g.e, 0, 0, g.cQ, g.cR, 0);
                this.c(g.e, g.cW, g.cX, 120, 100, 0);
                this.a(g.e, g.cW, g.cX - 21 - 10, l.eX[35], 0xFFFFFF);
                this.a(g.e, g.cW, g.cX - 21 + 5, l.eX[36], 0xFFFFFF);
                g.cL = 0;
                while (g.cL < 2) {
                    if (g.dU[g.dW] == g.cL) {
                        this.a(g.e, l.eX[40 + g.cL], g.cW - 28 + g.cL * 55, g.cX + 28, 1, 0xFFFFFF);
                        this.c(g.e, g.cW - 42 + g.cL * 55, g.cX + 25, 29, 14, 3);
                    } else {
                        this.c(g.e, g.cW - 42 + g.cL * 55, g.cX + 25, 29, 14, 2);
                        this.a(g.e, l.eX[40 + g.cL], g.cW - 28 + g.cL * 55, g.cX + 28, 1, 0x646464);
                    }
                    ++g.cL;
                }
                return;
            }
            case 1: {
                if (g.da < 2) {
                    g.da = 2;
                    var2_12 = (g.cT - 320) / 2;
                    var3_15 = 0;
                    while (var3_15 < 4) {
                        g.dp = this.b("/title_" + (var3_15 + 1) + ".png");
                        f.a(g.g, g.dp, g.cW - g.dp.getWidth() / 2, var2_12 + 80 * var3_15, 0);
                        g.dp = null;
                        ++var3_15;
                    }
                    if (g.dr == null) {
                        g.dr = this.b("/gamevil.png");
                    }
                    f.a(g.g, g.dr, g.cQ / 2, g.cR - 1, 33);
                    if (g.dq == null) {
                        g.dq = this.b("/press.png");
                    }
                }
                this.e();
                if (g.da % 4 >= 2) break;
                f.a(g.e, g.dq, g.cQ / 2, g.cR - 27, 33);
                return;
            }
            case 2: {
                if (g.da < 2) {
                    g.da = 2;
                    g.bG = "";
                    this.i();
                    g.c = l.eV[0];
                    this.l(g.g);
                }
                this.e();
                this.M();
                return;
            }
            case 160: {
                this.e();
                switch (g.al) {
                    case 0: {
                        g.bJ = g.ag.length();
                        this.c(g.e, g.cW, g.cX, g.bJ * 7 + 6, 45, 0);
                        this.a(g.cW, g.cX - 13, g.ag, 16400640);
                        this.a(g.cW, g.cX + 2, g.ah, 16400640);
                        break block1;
                    }
                    case 1: {
                        this.c(g.e, g.cW, g.cX, 120, 100, 0);
                        this.a(g.e, g.cW, g.cX - 21 - 10, g.ag, 16400640);
                        this.a(g.e, g.cW, g.cX - 21 + 5, g.ah, 16400640);
                        this.a(g.e, g.cW, g.cX - 21 + 20, l.eX[19], 16400640);
                        g.cL = 0;
                        while (g.cL < 2) {
                            if (g.dU[g.dW] == g.cL) {
                                this.a(g.e, l.eX[40 + g.cL], g.cW - 28 + g.cL * 55, g.cX + 28, 1, 16400640);
                                this.c(g.e, g.cW - 42 + g.cL * 55, g.cX + 25, 29, 14, 3);
                            } else {
                                this.c(g.e, g.cW - 42 + g.cL * 55, g.cX + 25, 29, 14, 2);
                                this.a(g.e, l.eX[40 + g.cL], g.cW - 28 + g.cL * 55, g.cX + 28, 1, 0xFFFFFF);
                            }
                            ++g.cL;
                        }
                        break block1;
                    }
                    case 2: {
                        this.c(g.e, g.cW, g.cX, 120, 100, 0);
                        this.a(g.e, g.cW, g.cX - 26 - 10, g.ag, 16400640);
                        this.a(g.e, g.cW, g.cX - 26 + 5, g.ah, 16400640);
                        this.a(g.e, g.cW, g.cX - 26 + 20, g.ai, 16400640);
                        this.a(g.e, g.cW, g.cX - 26 + 35, g.aj, 16400640);
                        this.a(g.e, g.cW, g.cX - 26 + 50, g.ak, 16400640);
                    }
                    default: {
                        return;
                    }
                }
            }
            case 300: {
                if (g.da < 2) {
                    g.da = 2;
                    g.n();
                    this.ag();
                    g.ds = this.b("/outro.png");
                }
                f.b(g.e, 0, 0, g.cS, g.cT, 0);
                var2_13 = g.ds.getWidth();
                i.a(g.ds, g.cW - var2_13 / 2, g.cX - 10, var2_13, 19, 0, 0);
                i.a(g.ds, g.cW - var2_13 / 2, g.cT - 26, var2_13, 23, 0, 19);
                if (g.da <= 30) break;
                g.l.destroyApp(true);
                g.l.notifyDestroyed();
                return;
            }
            case 87: {
                if (g.da < 2) {
                    g.da = 2;
                    g.c = l.eM[4];
                    g.k = 6;
                    this.U();
                }
                this.e();
                this.a(g.e, l.eQ[g.dU[g.dW]], g.cW - 39, g.cX - 19, 78, 17, false, true);
                g.a(g.e);
                this.c(-1, 1);
                return;
            }
            case 89: {
                if (g.da < 2) {
                    g.da = 2;
                    g.be = 0;
                }
                this.T();
                this.c(-1, 1);
                return;
            }
            case 85: {
                if (g.da < 2) {
                    g.da = 2;
                    switch (g.cY) {
                        case 85: {
                            g.c = l.eP[5];
                        }
                    }
                    this.s(g.g);
                }
                this.e();
                this.t(g.e);
                if (g.bG.length() == 0) {
                    this.c(4, 1);
                    break;
                }
                this.c(4, 3);
                return;
            }
            case 86: {
                if (g.da < 2) {
                    g.da = 2;
                    g.k = 2;
                }
                this.e();
                this.t(g.e);
                this.u(g.e);
            }
        }
    }

    static void b(int n2) {
        d = n2;
    }

    final void a(Graphics graphics, int n2, int n3, String string, int n4) {
        this.a(graphics, string, n2, n3, 1, n4);
    }

    final void a(int n2, int n3, String string, int n4) {
        this.a(e, string, n2, n3, 1, n4);
    }

    final void b(Graphics graphics, int n2, int n3, String string, int n4) {
        this.a(graphics, string, n2, n3, 0, n4);
    }

    final void b(int n2, int n3, String string, int n4) {
        this.a(e, string, n2, n3, 0, n4);
    }

    final void a(Graphics graphics, String string, int n2, int n3, int n4, int n5) {
        switch (n5) {
            case 0xFFFFFF: {
                i.a(n);
                break;
            }
            case 16400640: {
                i.a(o);
                break;
            }
            case 0x646464: {
                i.a(p);
                break;
            }
            case 0x41FF41: {
                i.a(q);
                break;
            }
            default: {
                g.a("=======================drawString: No Color:" + n5);
            }
        }
        i.a(graphics, string, n2, n3, n4);
    }

    static void a(int n2, int n3, int n4, int n5, int n6) {
        f.a(e, n2, n3, n4, n5, n6);
    }

    static void b(int n2, int n3, int n4, int n5, int n6) {
        f.b(e, n2, n3, n4, n5, n6);
    }

    static void a(Graphics graphics, int n2, int n3, int n4, int n5, int n6) {
        f.b(graphics, n2, n3, n4, n5, n6);
    }

    static void a(Graphics graphics, int n2) {
        graphics.setColor(n2);
    }

    static void b(Graphics graphics, int n2, int n3, int n4, int n5, int n6) {
        f.c(graphics, n2, n3, n4, n5, n6);
    }

    static void a(Graphics graphics, int n2, int n3, int n4, int n5) {
        f.c(graphics, n2, n3, n4, n5);
    }

    static void a(Graphics graphics, int n2, int n3, int n4) {
        f.b(graphics, n2, n3, 1, 1, n4);
    }

    public static void a(int n2, int n3, Image image) {
        f.a(e, image, n2, n3, 0);
    }

    public static void a(Graphics graphics, int n2, int n3, Image image) {
        f.a(graphics, image, n2, n3, 0);
    }

    public static void b(int n2, int n3, Image image) {
        int n4 = image.getWidth() / 2 + 1;
        int n5 = image.getHeight();
        f.a(e, image, n2 - n4, n3, n4, n5, n4 - 1, 0);
    }

    public static void b(Graphics graphics, int n2, int n3, Image image) {
        int n4 = image.getWidth() / 2 + 1;
        int n5 = image.getHeight();
        f.a(graphics, image, n2 - n4, n3, n4, n5, n4 - 1, 0);
    }

    public static void a(Graphics graphics, int n2, int n3, int n4, Image image) {
        int n5 = image.getWidth() / 2 + 1;
        f.a(graphics, image, n2 - n5, n3, n5, n4, n5 - 1, 0);
    }

    public static void a(int n2, int n3, Image image, boolean bl) {
        if (bl) {
            int n4 = image.getWidth() / 2 + 1;
            int n5 = image.getHeight();
            f.a(e, image, n2 - n4, n3, n4, n5, n4 - 1, 0);
            return;
        }
        f.a(e, image, n2 - image.getWidth(), n3, 0);
    }

    public static void a(Graphics graphics, int n2, int n3, Image image, int n4, int n5) {
        int n6 = image.getWidth() / 2 + 1;
        f.a(graphics, image, n2, n3, n6, n4, 0, n4 * n5);
    }

    public static void b(Graphics graphics, int n2, int n3, int n4, Image image) {
        int n5 = image.getWidth() / 2 + 1;
        f.a(graphics, image, n2 - n5, n3, n5, n4, n5 - 1, n4);
    }

    public static void c(int n2, int n3, Image image) {
        int n4 = image.getWidth() / 2 + 1;
        int n5 = image.getHeight();
        f.a(e, image, n2, n3, n4, n5, 0, 0);
    }

    public static void c(Graphics graphics, int n2, int n3, Image image) {
        int n4 = image.getWidth() / 2 + 1;
        int n5 = image.getHeight();
        f.a(graphics, image, n2, n3, n4, n5, 0, 0);
    }

    public static void c(Graphics graphics, int n2, int n3, int n4, Image image) {
        int n5 = image.getWidth() / 2 + 1;
        f.a(graphics, image, n2, n3, n5, n4, 0, 0);
    }

    public final void e() {
        f.a(e, f, 0, 0, 0);
        if (cY >= 90 && cY <= 105) {
            g.g(e);
        }
    }

    public final void c(int n2) {
        if (n2 == 262 || n2 == 278) {
            N = System.currentTimeMillis();
        }
        if (h.j && (System.currentTimeMillis() - N) / 1000L > 45L) {
            dZ = 0;
            cw = 13;
            x = false;
            this.o();
            N = System.currentTimeMillis();
            return;
        }
        N = System.currentTimeMillis();
        dR = 0;
        dQ = n2;
        dP.a(dQ);
        switch (dQ) {
            case 1300: {
                h.a((byte)(ae + 1));
                break;
            }
            case 1293: {
                h.a((byte)ab);
                h.b(1);
                break;
            }
            case 256: {
                h.b(i, 12);
                h.b(t, 4);
                break;
            }
            case 262: {
                h.b(i, 12);
                h.b(t, 4);
                break;
            }
            case 278: {
                h.b(i, 12);
                h.b(j, 16);
                h.b(t, 4);
                break;
            }
            case 512: {
                h.a(bz);
                break;
            }
            case 1291: {
                cM = 0;
                cL = 0;
                while (cL < 4) {
                    if (cH[cB[cL] - 3] != 99) {
                        h.a(cB[cL]);
                        ++cM;
                    }
                    ++cL;
                }
                cL = cM;
                while (cL < 4) {
                    h.a((byte)99);
                    ++cL;
                }
                break;
            }
            case 1280: {
                h.b(bG, 8);
                break;
            }
            case 258: {
                h.b(aO);
                break;
            }
            case 1027: {
                h.a((byte)bR[bA]);
                h.a((byte)bB);
                h.a((byte)aS);
                break;
            }
            case 1282: 
            case 1284: {
                h.b(bG, 20);
                break;
            }
            case 768: {
                h.a(bz);
                h.b(bG, 12);
                break;
            }
            case 288: {
                break;
            }
            case 290: {
                h.b(ap);
            }
        }
        h.b();
    }

    public final void f() {
        g.df[2] = this.b("/ui2.png");
        g.df[3] = this.b("/ui3.png");
        g.df[15] = this.b("/ui15.png");
        g.df[16] = this.b("/ui16.png");
        g.df[17] = this.b("/ui17.png");
        g.df[18] = this.b("/ui18.png");
        g.df[19] = this.b("/ui19.png");
        int n2 = 0;
        while (n2 < 6) {
            g.dg[n2] = this.b("/act" + n2 + ".png");
            ++n2;
        }
        g.di[1] = this.b("/menuarrow1.png");
        int n3 = 0;
        while (n3 < 8) {
            g.dh[n3] = this.b("/gnum" + n3 + ".png");
            ++n3;
        }
        this.h();
    }

    final void g() {
        g.df[34] = this.b("/ui34.png");
        g.df[35] = this.b("/ui35.png");
        g.df[36] = this.b("/ui36.png");
        g.df[37] = this.b("/ui37.png");
        g.df[38] = this.b("/ui38.png");
        g.df[48] = this.b("/ui48.png");
        g.df[49] = this.b("/ui49.png");
        g.df[52] = this.b("/ui52.png");
        g.df[53] = this.b("/ui53.png");
    }

    final void h() {
        int n2 = 0;
        while (n2 < 6) {
            if (dd[n2] == null) {
                g.dd[n2] = this.b("/mpic" + n2 + ".png");
            }
            ++n2;
        }
        if (dm == null) {
            dm = this.b("/ui_borderh.png");
        }
        if (dk == null) {
            dk = this.b("/ui_borderv.png");
        }
        if (dn == null) {
            dn = this.b("/ui_titlebox.png");
        }
        if (dl == null) {
            dl = this.b("/ui_back.png");
        }
        if (do == null) {
            do = this.b("/ui_menuicon.png");
        }
    }

    final void i() {
        int n2;
        g.du[0] = null;
        g.du[1] = null;
        int n3 = 0;
        while (n3 < 3) {
            if (dv[n3] != null) {
                dv[n3].a();
            }
            g.dv[n3] = null;
            ++n3;
        }
        n3 = 0;
        while (n3 < 10) {
            g.dw[n3][0] = null;
            g.dw[n3][1] = null;
            n2 = 0;
            while (n2 < 3) {
                if (dx[n3][n2] != null) {
                    dx[n3][n2].a();
                }
                g.dx[n3][n2] = null;
                ++n2;
            }
            ++n3;
        }
        n3 = 0;
        while (n3 < 2) {
            g.dy[n3][0] = null;
            g.dy[n3][1] = null;
            n2 = 0;
            while (n2 < 3) {
                if (dz[n3][n2] != null) {
                    dz[n3][n2].a();
                }
                g.dz[n3][n2] = null;
                ++n2;
            }
            ++n3;
        }
        n3 = 0;
        while (n3 < 2) {
            g.dA[n3][0] = null;
            g.dA[n3][1] = null;
            n2 = 0;
            while (n2 < 3) {
                if (dB[n3][n2] != null) {
                    dB[n3][n2].a();
                }
                g.dB[n3][n2] = null;
                ++n2;
            }
            ++n3;
        }
        n3 = 0;
        while (n3 < 2) {
            g.dC[n3][0] = null;
            g.dC[n3][1] = null;
            n2 = 0;
            while (n2 < 3) {
                if (dD[n3][n2] != null) {
                    dD[n3][n2].a();
                }
                g.dD[n3][n2] = null;
                ++n2;
            }
            ++n3;
        }
        g.dF[0] = null;
        g.dF[1] = null;
        n3 = 0;
        while (n3 < 3) {
            if (dG[n3] != null) {
                dG[n3].a();
            }
            g.dG[n3] = null;
            ++n3;
        }
        g.dH[0] = null;
        g.dH[1] = null;
        if (dI[0] != null) {
            dI[0].a();
        }
        g.dI[0] = null;
        g.dJ[0] = null;
        g.dJ[1] = null;
        if (dK[0] != null) {
            dK[0].a();
        }
        g.dK[0] = null;
        g.dL[0] = null;
        g.dL[1] = null;
        if (dM[0] != null) {
            dM[0].a();
        }
        g.dM[0] = null;
        g.dN[0] = null;
        g.dN[0] = null;
        if (dO[0] != null) {
            dO[0].a();
        }
        g.dO[0] = null;
        n3 = 2;
        while (n3 < dg.length) {
            g.dg[n3] = null;
            ++n3;
        }
        g.df[34] = null;
        g.df[35] = null;
        g.df[36] = null;
        g.df[37] = null;
        g.df[38] = null;
        g.df[48] = null;
        g.df[49] = null;
        g.df[52] = null;
        g.df[53] = null;
        g.X();
        if (di[1] == null) {
            g.di[1] = this.b("/menuarrow1.png");
        }
        this.h();
    }

    public final void a(k k2) {
        u = false;
        if (J || H == 1) {
            cw = 7;
            x = false;
            g.n();
            g.b(-1);
            this.k(4);
            return;
        }
        if (h.a == 280) {
            cw = 17;
            x = false;
            g.n();
            this.k(4);
            return;
        }
        if (!h.j) {
            return;
        }
        short s = k2.b();
        byte by = k2.a();
        dR = by;
        block0 : switch (s) {
            case 279: {
                if (dR == 1) {
                    g.K();
                    this.o();
                    cv = 0;
                    A = false;
                    g.i(10000);
                    return;
                }
                byte by2 = k2.a();
                this.o();
                if (by2 == 0) {
                    z = 0;
                    cw = 14;
                } else if (by2 == 1) {
                    z = 1;
                    cw = 15;
                } else {
                    z = 0;
                    cw = 0;
                }
                this.k(4);
                return;
            }
            case 263: {
                switch (dR) {
                    case 1: {
                        cE = k2.a(8);
                        ar = k2.a();
                        as = k2.b();
                        at = k2.c();
                        au = k2.c();
                        av = k2.b();
                        k2.b();
                        k2.b();
                        aw = k2.a();
                        g.bE[0] = k2.a();
                        g.bE[1] = k2.a();
                        g.bE[2] = k2.a();
                        g.bE[3] = k2.a();
                        bD = 0;
                        cL = 0;
                        while (cL < 4) {
                            if (bE[cL] != 99) {
                                ++bD;
                            }
                            ++cL;
                        }
                        cF = g.d(k2.a(20));
                        cG = g.d(k2.a(20));
                        cL = 0;
                        while (cL < 11) {
                            g.cI[g.cL] = k2.a();
                            ++cL;
                        }
                        aK = k2.a();
                        aL = k2.a();
                        aM = k2.a();
                        if (aL < 0) {
                            aL = 0;
                        }
                        if (aM < 0) {
                            aM = 0;
                        }
                        aN = k2.a();
                        k2.a(8);
                        k2.a(8);
                        k2.a();
                        k2.a();
                        k2.a();
                        dp = null;
                        dq = null;
                        dr = null;
                        g.X();
                        if (dX) {
                            if (P) {
                                this.l(7);
                                return;
                            }
                            this.l(10);
                            return;
                        }
                        if (aN > 0) {
                            aO = 1;
                            this.c(258);
                            return;
                        }
                        aN = 0;
                        this.l(7);
                        return;
                    }
                    case -2: {
                        cw = 1;
                        this.o();
                        return;
                    }
                    case -9: {
                        cw = 8;
                        this.o();
                        return;
                    }
                }
                cw = 7;
                x = false;
                g.n();
                this.k(4);
                return;
            }
            case 1286: {
                switch (bz) {
                    case 0: 
                    case 1: {
                        g.i(11);
                        break block0;
                    }
                    case 2: {
                        g.i(12);
                    }
                }
                return;
            }
            case 1301: {
                switch (dR) {
                    case 1: {
                        g.ac[g.ae] = k2.c();
                        ad = k2.c();
                        this.k(161 + dU[dW] + 1);
                        break block0;
                    }
                    case -1: {
                        cw = 0;
                        this.k(4);
                    }
                }
                return;
            }
            case 1294: {
                switch (dR) {
                    case 1: {
                        int n2 = k2.a();
                        int n3 = 0;
                        while (n3 < n2) {
                            g.Z[n3] = k2.c();
                            g.Y[n3] = k2.a(12);
                            g.aa[n3] = k2.c();
                            ++n3;
                        }
                        this.k(170 + dU[dW]);
                        break block0;
                    }
                    case -1: {
                        cw = 0;
                        this.k(4);
                    }
                }
                return;
            }
            case 259: {
                switch (dR) {
                    case 1: {
                        int n4 = 0;
                        while (n4 < 4) {
                            g.bF[n4] = k2.a(16);
                            ++n4;
                        }
                        aN = k2.a();
                        bd = 1;
                        g.i(6);
                        return;
                    }
                }
                cw = 0;
                this.k(4);
                return;
            }
            case 513: {
                switch (dR) {
                    case 1: {
                        g.by = k2.a();
                        bh = k2.a();
                        bz = k2.a();
                        k2.a();
                        w = true;
                        this.O();
                        w = false;
                        O = true;
                        return;
                    }
                }
                cw = 0;
                switch (dR) {
                    case -11: {
                        cw = 8;
                    }
                }
                this.k(4);
                return;
            }
            case 769: {
                switch (dR) {
                    case 1: {
                        g.by = k2.a();
                        bh = k2.a();
                        bz = k2.a();
                        k2.a();
                        w = true;
                        this.O();
                        w = false;
                        O = true;
                        return;
                    }
                }
                switch (dR) {
                    case -3: {
                        cw = 2;
                        break;
                    }
                    case -4: {
                        cw = 3;
                        break;
                    }
                    case -5: {
                        cw = 4;
                        break;
                    }
                    case -12: {
                        cw = 9;
                        break;
                    }
                    case -16: {
                        cw = 18;
                        break;
                    }
                    default: {
                        cw = 0;
                    }
                }
                this.k(4);
                return;
            }
            case 770: {
                switch (dR) {
                    case 1: {
                        x = false;
                        g.by = k2.a();
                        bh = k2.a();
                        bz = k2.a();
                        k2.a();
                        w = true;
                        this.O();
                        w = false;
                        O = true;
                        return;
                    }
                }
                cw = 0;
                this.k(4);
                return;
            }
            case 514: {
                switch (dR) {
                    case 1: {
                        cL = 0;
                        while (cL < 4) {
                            if (!bQ[cL]) {
                                ct = cL;
                                break;
                            }
                            ++cL;
                        }
                        g.bQ[g.ct] = true;
                        g.bR[g.ct] = k2.a();
                        if (bR[ct] % 2 == bR[0] % 2) {
                            ++bb;
                        } else {
                            ++bc;
                        }
                        g.bM[g.ct] = k2.a(8);
                        g.bS[g.ct] = k2.b();
                        g.bT[g.ct] = k2.c();
                        g.bU[g.ct] = k2.c();
                        g.bW[g.ct] = k2.b();
                        g.bV[g.ct] = bW[ct];
                        g.bY[g.ct] = k2.a();
                        g.bZ[g.ct] = k2.a();
                        if (bZ[ct] == 10) {
                            g.bZ[g.ct] = 0;
                            g.ca[g.ct] = 2;
                        } else if (bZ[ct] < 10) {
                            g.ca[g.ct] = 0;
                        } else {
                            int n5 = ct;
                            bZ[n5] = (byte)(bZ[n5] - 30);
                            g.ca[g.ct] = 1;
                        }
                        g.bN[g.ct] = k2.a(20);
                        g.bO[g.ct] = k2.a(20);
                        g.cr[g.ct] = k2.a();
                        g.bP[g.ct] = k2.a(8);
                        g.bX[g.ct] = 0;
                        g.h(ct);
                        g.co[g.ct] = Math.abs(h.nextInt()) % 4;
                        g.cp[g.ct] = 99;
                        g.cq[g.ct] = 0;
                        bj = true;
                        if (cY != 4) break block0;
                        g.i(90);
                        O = true;
                        return;
                    }
                }
                cw = 0;
                this.k(4);
                return;
            }
            case 1024: {
                switch (dR) {
                    case 1: {
                        g.i(92);
                    }
                }
                return;
            }
            case 1026: {
                switch (dR) {
                    case 1: {
                        bB = 99;
                        g.b(10 - an);
                        ba = 10;
                        G = false;
                        g.i(94);
                    }
                }
                return;
            }
            case 1028: {
                switch (dR) {
                    case 1: {
                        cL = 0;
                        while (cL < 4) {
                            bi = false;
                            cM = 0;
                            while (cM < 4) {
                                if (bQ[cM] && bR[cM] == cL) {
                                    ct = cM;
                                    bi = true;
                                    break;
                                }
                                ++cM;
                            }
                            if (bi) {
                                g.cb[g.ct] = k2.a();
                            } else {
                                bJ = k2.a();
                            }
                            ++cL;
                        }
                        aT = k2.a();
                        cL = 0;
                        while (cL < aT) {
                            g.cK[0 + g.cL] = k2.a();
                            g.cK[4 + g.cL] = k2.a();
                            g.cJ[0 + g.cL] = k2.b();
                            g.cK[8 + g.cL] = k2.a();
                            g.cK[12 + g.cL] = k2.a();
                            g.cK[16 + g.cL] = k2.a();
                            g.cJ[4 + g.cL] = k2.b();
                            g.cK[20 + g.cL] = k2.a();
                            g.cK[24 + g.cL] = k2.a();
                            g.cK[28 + g.cL] = k2.a();
                            ++cL;
                        }
                        k2.a();
                        cL = 0;
                        while (cL < aT) {
                            if (cK[24 + cL] == 1) {
                                g.cK[32 + g.cL] = k2.a();
                                g.cK[36 + g.cL] = k2.a();
                                g.cJ[8 + g.cL] = k2.b();
                                g.cK[40 + g.cL] = k2.a();
                            }
                            ++cL;
                        }
                        g.i(99);
                    }
                }
                return;
            }
            case 1031: {
                switch (dR) {
                    case 1: {
                        g.by = k2.a();
                        g.i(104);
                    }
                }
                return;
            }
            case 1032: {
                switch (dR) {
                    case 1: {
                        aU = k2.a();
                        if (bz != 2) {
                            if (aU == 1) {
                                ++at;
                            } else {
                                ++au;
                            }
                        }
                        aV = k2.b();
                        aW = k2.a();
                        aX = k2.b();
                        aY = k2.b();
                        bI = k2.a(15);
                        aZ = k2.c();
                        k2.a();
                        k2.c();
                        k2.a();
                        g.i(105);
                    }
                }
                return;
            }
            case 1037: {
                switch (dR) {
                    case 1: {
                        bH = k2.a(14);
                        aP = k2.a();
                        aQ = k2.a();
                        g.i(91);
                    }
                }
                return;
            }
            case 1035: {
                switch (dR) {
                    case 1: {
                        bg = k2.a();
                        cL = 0;
                        while (cL < 4) {
                            if (bQ[cL] && bR[cL] == bg) {
                                ct = cL;
                                break;
                            }
                            ++cL;
                        }
                        g.bQ[g.ct] = false;
                        if (bW[ct] == 0) break;
                        if (bR[ct] % 2 == bR[0] % 2) {
                            --bb;
                            break block0;
                        }
                        --bc;
                    }
                }
                return;
            }
            case 1281: {
                switch (dR) {
                    case 1: {
                        cE = bG;
                        this.m(2);
                        return;
                    }
                    case -6: {
                        cw = 6;
                        this.k(4);
                        return;
                    }
                    case -49: {
                        cw = 5;
                        this.k(4);
                        return;
                    }
                    case -15: {
                        cw = 5;
                        this.k(4);
                        return;
                    }
                }
                cw = 0;
                this.k(4);
                return;
            }
            case 1283: {
                this.k(84);
                switch (dR) {
                    case 1: {
                        cF = bG;
                        C = 0;
                        bG = cG;
                        B = 1;
                        return;
                    }
                    case -49: {
                        cw = 5;
                        this.k(4);
                        return;
                    }
                }
                cw = 0;
                this.k(4);
                return;
            }
            case 1285: {
                switch (dR) {
                    case 1: {
                        cG = bG;
                        this.N();
                        return;
                    }
                    case -49: {
                        cw = 5;
                        this.k(4);
                        return;
                    }
                }
                cw = 0;
                this.k(4);
                return;
            }
            case 1288: {
                switch (dR) {
                    case 1: {
                        aC = k2.b();
                        aD = k2.b();
                        aE = k2.b();
                        aF = k2.b();
                        aG = k2.b();
                        aH = k2.b();
                        aI = k2.b();
                        aJ = k2.b();
                        this.k(81);
                        return;
                    }
                }
                cw = 0;
                this.k(4);
                return;
            }
            case 1290: {
                switch (dR) {
                    case 1: {
                        cL = 0;
                        while (cL < 11) {
                            g.cH[g.cL] = 99;
                            ++cL;
                        }
                        bf = k2.a();
                        cL = 0;
                        while (cL < bf) {
                            bp = k2.a();
                            g.cH[g.bp - 3] = k2.a();
                            ++cL;
                        }
                        cL = 0;
                        while (cL < bD) {
                            g.cB[g.cL] = bE[cL];
                            ++cL;
                        }
                        while (cL < 4) {
                            cM = 0;
                            while (cM < 11) {
                                bq = false;
                                cN = 0;
                                while (cN < cL) {
                                    if (cB[cN] == 3 + cM) {
                                        bq = true;
                                        break;
                                    }
                                    ++cN;
                                }
                                if (!bq) {
                                    g.cB[g.cL] = (byte)(3 + cM);
                                    break;
                                }
                                ++cM;
                            }
                            ++cL;
                        }
                        this.k(82);
                        return;
                    }
                }
                cw = 0;
                this.k(4);
                return;
            }
            case 1292: {
                switch (dR) {
                    case 1: {
                        cM = 0;
                        cL = 0;
                        while (cL < 4) {
                            if (cH[cB[cL] - 3] != 99) {
                                g.bE[g.cM] = cB[cL];
                                ++cM;
                            }
                            ++cL;
                        }
                        bD = cM;
                        cL = cM;
                        while (cL < 4) {
                            g.bE[g.cM] = 99;
                            ++cL;
                        }
                        this.N();
                        return;
                    }
                }
                cw = 0;
                this.k(4);
                return;
            }
            case 1297: {
                switch (dR) {
                    case 1: {
                        ax = k2.c();
                        aA = k2.c();
                        aB = k2.c();
                        this.k(80);
                        return;
                    }
                }
                cw = 0;
                this.k(4);
                return;
            }
            case 1299: {
                switch (dR) {
                    case 1: {
                        ay = k2.c();
                        ax = k2.c();
                        az = k2.c();
                        this.k(83);
                        return;
                    }
                }
                cw = 0;
                this.k(4);
                return;
            }
            case 1536: {
                switch (dR) {
                    case 1: {
                        bd = k2.a();
                        int n6 = 0;
                        while (n6 < 4) {
                            g.bF[n6] = k2.a(16);
                            ++n6;
                        }
                        aN = 0;
                        g.i(6);
                    }
                }
                return;
            }
            case 289: {
                if (dR == 1) {
                    ap = ao = k2.c();
                    this.k(88);
                    return;
                }
                cw = 0;
                this.k(4);
                return;
            }
            case 291: {
                if (dR == 1) {
                    this.N();
                    return;
                }
                cw = 0;
                this.k(4);
            }
        }
    }

    public final void d(int n2) {
        if (da < 2) {
            return;
        }
        if (n2 == -3 || n2 == -1) {
            if (dU[dW] > 0) {
                int n3 = dW;
                dU[n3] = dU[n3] - 1;
            } else {
                g.dU[g.dW] = k - 1;
            }
        } else if (n2 == -4 || n2 == -2) {
            if (dU[dW] < k - 1) {
                int n4 = dW;
                dU[n4] = dU[n4] + 1;
            } else {
                g.dU[g.dW] = 0;
            }
        }
        if (n2 == -5) {
            this.q();
        }
    }

    public final void e(int n2) {
        if (da < 2) {
            return;
        }
        if (n2 == -3 || n2 == -1) {
            if (dU[dW] > 0) {
                int n3 = dW;
                dU[n3] = dU[n3] - 1;
            } else {
                g.dU[g.dW] = 1;
            }
        } else if (n2 == -4 || n2 == -2) {
            if (dU[dW] < 1) {
                int n4 = dW;
                dU[n4] = dU[n4] + 1;
            } else {
                g.dU[g.dW] = 0;
            }
        }
        if (n2 == -5) {
            this.q();
            return;
        }
        if (n2 == -7) {
            if (cY == 160 && al != 1) {
                return;
            }
            g.dU[g.dW] = 1;
            this.q();
        }
    }

    public void keyPressed(int n2) {
        if (n2 == -32 || n2 == -33) {
            return;
        }
        m = n2;
        if (J) {
            if (m == -5) {
                g.a(2);
            }
            m = -999;
        }
    }

    /*
     * Unable to fully structure code
     */
    public final void f(int var1_1) {
        g.dZ = 0;
        g.cs = var1_1;
        block0 : switch (g.cY) {
            case 161: {
                if (g.cs == -7) {
                    this.N();
                    return;
                }
            }
            case 11: 
            case 12: 
            case 16: 
            case 87: 
            case 162: 
            case 163: 
            case 164: {
                if (g.cs == -7) {
                    this.N();
                    return;
                }
                this.d(g.cs);
                return;
            }
            case 170: 
            case 171: {
                if (g.cs != -7 && g.cs != -5) break;
                this.N();
                return;
            }
            case 6: {
                if (g.aN > 0) {
                    ++g.aO;
                    this.c(258);
                    return;
                }
                if (g.bd == 1) {
                    this.l(7);
                    return;
                }
                if (g.bd != 9) break;
                g.i(300);
                return;
            }
            case 7: {
                g.k = 2;
                g.P = false;
                this.l(10);
                return;
            }
            case 10: {
                if (g.x) {
                    if (g.cs == -3 || g.cs == -4) {
                        g.y = (g.y + 1) % 2;
                        return;
                    }
                    if (g.cs != -5) break;
                    if (g.y == 0) {
                        g.i(300);
                        return;
                    }
                    g.x = false;
                    return;
                }
                if (g.cs == -6) {
                    g.n();
                    g.z = 0;
                    g.P = true;
                    g.C = 0;
                    this.k(2);
                    return;
                }
                if (g.cs == -7) {
                    g.x = true;
                    g.y = 1;
                    return;
                }
                this.d(g.cs);
                return;
            }
            case 80: 
            case 81: 
            case 83: {
                if (g.cs != -5 && g.cs != -7) break;
                this.N();
                return;
            }
            case 82: {
                if (g.cs == -1) {
                    if (g.dU[g.dW] > 0) {
                        v0 = g.dW;
                        g.dU[v0] = g.dU[v0] - 1;
                    } else {
                        g.dU[g.dW] = 3;
                    }
                } else if (g.cs == -2) {
                    if (g.dU[g.dW] < 3) {
                        v1 = g.dW;
                        g.dU[v1] = g.dU[v1] + 1;
                    } else {
                        g.dU[g.dW] = 0;
                    }
                } else if (g.cs == -3) {
                    block47: do {
                        if (g.cB[g.dU[g.dW]] > 3) {
                            v2 = g.dU[g.dW];
                            g.cB[v2] = (byte)(g.cB[v2] - 1);
                        } else {
                            g.cB[g.dU[g.dW]] = 13;
                        }
                        g.bq = false;
                        g.cL = 0;
                        while (g.cL < 4) {
                            if (g.cL != g.dU[g.dW] && g.cB[g.dU[g.dW]] == g.cB[g.cL]) {
                                g.bq = true;
                                continue block47;
                            }
                            ++g.cL;
                        }
                    } while (g.bq);
                } else if (g.cs == -4) {
                    block49: do {
                        if (g.cB[g.dU[g.dW]] < 13) {
                            v3 = g.dU[g.dW];
                            g.cB[v3] = (byte)(g.cB[v3] + 1);
                        } else {
                            g.cB[g.dU[g.dW]] = 3;
                        }
                        g.bq = false;
                        g.cL = 0;
                        while (g.cL < 4) {
                            if (g.cL != g.dU[g.dW] && g.cB[g.dU[g.dW]] == g.cB[g.cL]) {
                                g.bq = true;
                                continue block49;
                            }
                            ++g.cL;
                        }
                    } while (g.bq);
                }
                if (g.cs != -5 && g.cs != -7) break;
                this.q();
                return;
            }
            case 84: {
                if (g.cs == -7) {
                    if (g.bG.length() == 0) {
                        if (g.B == 0) {
                            this.N();
                            return;
                        }
                        --g.B;
                        return;
                    }
                    g.bG = g.bG.substring(0, g.bG.length() - 1);
                    return;
                }
                if (g.cs == -5 || g.cs == -6) {
                    if (g.bG.length() == 0) {
                        if (g.C >= 26) break;
                        g.bG = g.bG + (char)(65 + g.C);
                        return;
                    }
                    if (g.bG.length() > 20) break;
                    if (g.C < 26) {
                        if (g.bG.length() >= 20) break;
                        g.bG = g.bG + (char)(97 + g.C);
                        return;
                    }
                    if (g.C == 26) {
                        if (g.bG.length() >= 20) break;
                        g.bG = g.bG + ' ';
                        return;
                    }
                    if (g.C != 27) break;
                    g.cv = 5;
                    g.bG = g.d(g.bG);
                    if (g.B == 0) {
                        this.c(1282);
                    } else {
                        this.c(1284);
                    }
                    g.i(3);
                    return;
                }
                g.q(g.cs);
                return;
            }
            case 85: {
                if (g.cs == -7) {
                    if (g.bG.length() == 0) {
                        this.N();
                        return;
                    }
                    g.bG = g.bG.substring(0, g.bG.length() - 1);
                    return;
                }
                if (g.cs == -5 || g.cs == -6) {
                    if (g.bG.length() == 0) {
                        if (g.C >= 26) break;
                        g.bG = g.bG + (char)(65 + g.C);
                        return;
                    }
                    if (g.bG.length() > 8) break;
                    if (g.C < 26) {
                        if (g.bG.length() >= 8) break;
                        g.bG = g.bG + (char)(97 + g.C);
                        return;
                    }
                    if (g.C != 26) break;
                    this.k(86);
                    return;
                }
                g.p(g.cs);
                return;
            }
            case 88: {
                if (g.cs == -1) {
                    if (g.dU[g.dW] > 0) {
                        v4 = g.dW;
                        g.dU[v4] = g.dU[v4] - 1;
                        return;
                    }
                    g.dU[g.dW] = 2;
                    return;
                }
                if (g.cs == -2) {
                    if (g.dU[g.dW] < 2) {
                        v5 = g.dW;
                        g.dU[v5] = g.dU[v5] + 1;
                        return;
                    }
                    g.dU[g.dW] = 0;
                    return;
                }
                if (g.cs == -3 || g.cs == -4) {
                    this.q();
                    return;
                }
                if (g.cs == -5) {
                    g.cs = -4;
                    this.q();
                    return;
                }
                if (g.cs != -7) break;
                g.K();
                if (g.ap != g.ao) {
                    g.cv = 1;
                    g.i(3);
                    this.c(290);
                    return;
                }
                this.N();
                this.t(1);
                return;
            }
            case 89: {
                if (g.cs == -3) {
                    if (g.be > 0) {
                        --g.be;
                        return;
                    }
                    g.be = l.ew[g.dU[g.dW - 1]] - 1;
                    return;
                }
                if (g.cs == -4 || g.cs == -5) {
                    if (g.be < l.ew[g.dU[g.dW - 1]] - 1) {
                        ++g.be;
                        return;
                    }
                    g.be = 0;
                    return;
                }
                if (g.cs != -7) break;
                this.N();
                return;
            }
            case 20: {
                if (g.cs == -7) {
                    this.N();
                    return;
                }
                this.d(g.cs);
                return;
            }
            case 21: {
                if (g.cs == -5 || g.cs == -6) {
                    if (g.bG.length() > 12) break;
                    if (g.C < 26) {
                        if (g.bG.length() >= 12) break;
                        g.bG = g.bG + (char)(65 + g.C);
                        return;
                    }
                    if (g.C != 26 || g.bG.length() < 4) break;
                    switch (g.bz) {
                        case 0: {
                            g.cv = 2;
                            break;
                        }
                        case 1: {
                            g.cv = 4;
                            break;
                        }
                        case 2: {
                            g.cv = 4;
                        }
                    }
                    g.cv = 0;
                    this.c(768);
                    g.i(3);
                    return;
                }
                if (var1_1 == -7) {
                    if (g.bG.length() == 0) {
                        this.N();
                        return;
                    }
                    g.bG = g.bG.substring(0, g.bG.length() - 1);
                    return;
                }
                g.p(var1_1);
                return;
            }
            case 94: {
                if (g.D) {
                    if (g.cs == -3 || g.cs == -4) {
                        g.E = (g.E + 1) % 2;
                        return;
                    }
                    if (g.cs != -5) break;
                    if (g.E == 0) {
                        g.P = false;
                        g.n();
                        g.b(-1);
                        g.cv = 0;
                        g.A = false;
                        g.i(10000);
                        return;
                    }
                    g.D = false;
                    return;
                }
                g.bB = 99;
                if (g.cs != -1) ** GOTO lbl276
                g.bB = 2;
                ** GOTO lbl297
lbl276:
                // 1 sources

                if (g.cs != -3) ** GOTO lbl279
                g.bB = 1;
                ** GOTO lbl297
lbl279:
                // 1 sources

                if (g.cs != -4) ** GOTO lbl282
                g.bB = 0;
                ** GOTO lbl297
lbl282:
                // 1 sources

                if (g.cs != -2) ** GOTO lbl292
                if (g.bD <= 0) ** GOTO lbl297
                g.cN = 0;
                while (g.cN < g.bD) {
                    if (g.bX[0] < g.cI[g.bE[g.cN] - 3]) ** GOTO lbl289
                    g.bB = 20;
                    ** GOTO lbl297
lbl289:
                    // 1 sources

                    ++g.cN;
                }
                ** GOTO lbl297
lbl292:
                // 1 sources

                if (g.cs == -7 && !g.G) {
                    g.G = true;
                    g.D = true;
                    g.E = 1;
                    g.F = System.currentTimeMillis();
                }
lbl297:
                // 9 sources

                if (g.bB == 20) {
                    g.i(95);
                    return;
                }
                if (g.bB == 99) break;
                g.i(96);
                return;
            }
            case 95: {
                if (g.cs == -1) {
                    g.db = g.db > 0 ? --g.db : g.bD - 1;
                } else if (g.cs == -2) {
                    g.db = g.db < g.bD - 1 ? ++g.db : 0;
                }
                if (g.cs == -5) {
                    if (g.bX[0] < g.cI[g.bE[g.db] - 3]) break;
                    g.bB = g.bE[g.db];
                    g.i(96);
                    return;
                }
                if (g.cs != -7) break;
                g.bB = 99;
                g.i(94);
                return;
            }
            case 96: {
                if (g.cs == -1 || g.cs == -2) {
                    switch (g.bB) {
                        case 9: 
                        case 10: {
                            g.cL = 0;
                            while (g.cL < 4) {
                                if (g.bQ[g.cL] && g.bR[g.cL] % 2 == g.bR[g.bA] % 2 && g.bR[g.cL] != g.bR[g.bA]) {
                                    g.bA = g.cL;
                                    break block0;
                                }
                                ++g.cL;
                            }
                            break block0;
                        }
                        case 0: 
                        case 3: 
                        case 4: 
                        case 5: 
                        case 6: 
                        case 7: {
                            g.cL = 1;
                            while (g.cL < 4) {
                                if (g.bQ[g.cL] && g.bR[g.cL] % 2 == g.bR[g.bA] % 2 && g.bR[g.cL] != g.bR[g.bA]) {
                                    g.bA = g.cL;
                                    break block0;
                                }
                                ++g.cL;
                            }
                        }
                        default: {
                            return;
                        }
                    }
                }
                if (g.cs == -5) {
                    this.B();
                    return;
                }
                if (g.cs != -7) break;
                switch (g.bB) {
                    case 3: 
                    case 4: 
                    case 5: 
                    case 6: 
                    case 7: 
                    case 9: 
                    case 10: {
                        g.i(95);
                        return;
                    }
                }
                g.i(94);
                return;
            }
            case 97: {
                if (g.da <= 0 || g.cs != -5) break;
                this.C();
                return;
            }
            case 105: {
                if (g.da <= 1000 / g.dc || g.cs != -5) break;
                this.l(10);
                switch (g.bz) {
                    case 0: {
                        this.k(11);
                        break block0;
                    }
                    case 1: {
                        this.k(11);
                        g.dU[g.dW] = 1;
                        break block0;
                    }
                    case 2: {
                        g.dU[g.dW] = 1;
                        this.k(12);
                    }
                }
                return;
            }
            case 4: {
                if (g.x) {
                    if (g.cs == -3 || g.cs == -4) {
                        g.y = (g.y + 1) % 2;
                        return;
                    }
                    if (g.cs != -5) break;
                    if (g.y == 0) {
                        g.i(300);
                        return;
                    }
                    g.x = false;
                    g.y = 1;
                    return;
                }
                if (g.cs == -6) {
                    if (g.cw != 7 && g.cw != 1) break;
                    g.n();
                    g.z = 0;
                    g.P = true;
                    g.i(2);
                    g.x = false;
                    return;
                }
                if (g.cs == -7) {
                    if (g.cw != 7 && g.cw != 1) break;
                    g.x = true;
                    g.y = 1;
                    return;
                }
                if (g.cs != -5) break;
                if (!h.j) {
                    if (g.cw == 14 || g.cw == 15 || g.cw == 16) {
                        this.N();
                        return;
                    }
                    if (g.cw == 17) {
                        g.z = 0;
                        g.P = true;
                        this.k(2);
                        return;
                    }
                    if (g.cw != 1) {
                        g.cv = 0;
                        g.i(10000);
                        return;
                    }
                    this.l(1);
                    return;
                }
                if (g.ec > -1) {
                    this.k(g.ec);
                    g.ec = -1;
                    return;
                }
                switch (g.dV[g.dW - 1]) {
                    case 105: {
                        return;
                    }
                    case 86: {
                        this.m(2);
                        return;
                    }
                }
                this.N();
                return;
            }
            case 5: {
                if (g.cs == -3 || g.cs == -4) {
                    g.dU[g.dW] = (g.dU[g.dW] + 1) % 2;
                    return;
                }
                if (g.cs != -5) break;
                if (g.dU[g.dW] == 0) {
                    if (g.am == 0) {
                        g.am = 4;
                    }
                } else {
                    g.am = 0;
                }
                g.K();
                g.i(1);
                this.s(1);
                return;
            }
            case 1: {
                if (g.da <= 3) break;
                if (g.i.equals("")) {
                    g.z = 0;
                    this.k(2);
                    return;
                }
                if (g.cw == 1) {
                    g.i(4);
                    return;
                }
                g.cv = 0;
                g.A = false;
                g.i(10000);
                return;
            }
            case 2: {
                this.j(g.cs);
                return;
            }
            case 86: 
            case 160: {
                this.e(g.cs);
            }
        }
    }

    static void j() {
        g.cj[g.cL] = cf[cL] - bW[cL];
        g.ch[g.cL] = cj[cL] / 5;
        if (ch[cL] == 0) {
            if (cf[cL] > bW[cL]) {
                g.ch[g.cL] = 1;
            } else if (cf[cL] < bW[cL]) {
                g.ch[g.cL] = -1;
            }
        }
        g.ci[g.cL] = (cg[cL] - bX[cL]) / 5;
        if (ci[cL] == 0) {
            if (cg[cL] > bX[cL]) {
                g.ci[g.cL] = 1;
                return;
            }
            if (cg[cL] < bX[cL]) {
                g.ci[g.cL] = -1;
            }
        }
    }

    final void k() {
        Q = 0;
        U = -1;
        X = -1;
        cL = 0;
        while (cL < 4) {
            if (bQ[cL]) {
                g.cc[g.cL] = 0;
                g.cd[g.cL] = 0;
                g.ce[g.cL] = 0;
                g.cj[g.cL] = 0;
                if (bR[cL] == cK[0 + bC]) {
                    S = cL;
                    g.cf[g.cL] = cJ[0 + bC];
                    g.cg[g.cL] = cK[8 + bC];
                    g.j();
                }
                if (bR[cL] == cK[12 + bC]) {
                    T = cL;
                    g.cf[g.cL] = cJ[4 + bC];
                    g.cg[g.cL] = cK[20 + bC];
                    g.j();
                    switch (cK[16 + bC]) {
                        case 1: {
                            if (cb[T] == 1) {
                                V = 4;
                                break;
                            }
                            V = 1;
                            break;
                        }
                        case 2: {
                            V = 5;
                        }
                    }
                }
                if (cK[24 + bC] > 0 && bR[cL] == cK[32 + bC]) {
                    U = cL;
                    g.cf[g.cL] = cJ[8 + bC];
                    g.cg[g.cL] = cK[40 + bC];
                    g.j();
                    switch (cK[36 + bC]) {
                        case 1: {
                            if (cb[U] == 1) {
                                W = 4;
                                break;
                            }
                            W = 1;
                            break;
                        }
                        case 2: {
                            W = 5;
                        }
                    }
                }
            }
            ++cL;
        }
        switch (cK[4 + bC]) {
            case 3: 
            case 4: 
            case 5: 
            case 6: 
            case 7: 
            case 8: {
                g.cc[g.S] = 8;
                break;
            }
            case 2: 
            case 9: 
            case 10: {
                g.cc[g.S] = 12;
                break;
            }
            case 11: 
            case 12: 
            case 13: {
                g.cc[g.S] = 13;
                break;
            }
            case 0: {
                g.cc[g.S] = 2;
                bl = (cQ - 67 - 42) / l.eh[cc[S]];
                bm = bz == 0 ? 0 : (bR[S] / 2 == cK[12 + bC] / 2 ? 0 : (bR[S] / 2 == 0 ? 46 / l.eh[cc[S]] : -46 / l.eh[cc[S]]));
            }
        }
        R = l.eh[cc[S]];
    }

    public final void l() {
        if (A) {
            this.c(278);
            return;
        }
        this.c(262);
    }

    public final void m() {
        eb = false;
        if (!h.j) {
            if (dP == null) {
                dP = new h();
                dP.setPriority(10);
                dP.start();
            }
            h.a(this);
            L = true;
            dP.a(r, s);
        }
    }

    public static void n() {
        ea = true;
        h.j = false;
        h.k = false;
        g.a(400L);
        if (dP != null) {
            h.a();
        }
        dP = null;
        dX = true;
        g.b(-1);
        g.a(100L);
    }

    public final void o() {
        g.n();
        if (cw > -1) {
            this.p();
        }
    }

    final void p() {
        if (aq) {
            aq = false;
            return;
        }
        g.i(4);
    }

    public final void g(int n2) {
        if (!ea) {
            cw = n2 < 10 ? 7 : n2;
            this.o();
        }
        ea = false;
    }

    public void hideNotify() {
        this.ag();
        g.a(1);
    }

    public void showNotify() {
        g.a(1);
    }

    public final void c(Graphics graphics, int n2, int n3, int n4, int n5, int n6) {
        int n7 = 0x525152;
        int n8 = 0xFFFFFF;
        switch (n6) {
            case 0: 
            case 7: {
                if (n4 % 2 == 1) {
                    ++n4;
                }
                if (n5 % 2 == 1) {
                    ++n5;
                }
                cx = n2 - n4 / 2;
                cy = n3 - n5 / 2;
                if (n6 == 0) {
                    f.b(graphics, cx, cy, n4, n5, 0);
                }
                f.a(graphics, cx + 1, cy + 1, n4 - 2, n5 - 2, 0xADAAAD);
                g.c(graphics, cx + l.eq[2], cy + l.er[2], df[2]);
                g.b(graphics, cx + n4 + l.eq[2], cy + l.er[2], df[2]);
                g.c(graphics, cx + l.eq[3], cy + n5 - 2 - 5 + l.er[3], df[3]);
                g.b(graphics, cx + n4 + l.eq[3], cy + n5 - 2 - 5 + l.er[3], df[3]);
                return;
            }
            case 1: {
                g.a(graphics, n2, n3, n4, n5, 0);
                g.a(graphics, 0xBDBABD);
                g.a(graphics, n2 + 14, n3, n2 + n4 - 14 - 1, n3);
                g.a(graphics, n2 + 14, n3 + n5 - 1, n2 + n4 - 14 - 1, n3 + n5 - 1);
                g.a(graphics, 0x949A94);
                g.a(graphics, n2 + 1, n3, n2 + 13, n3);
                g.a(graphics, n2 + n4 - 14, n3, n2 + n4 - 2, n3);
                g.a(graphics, n2 + 1, n3 + n5 - 1, n2 + 13, n3 + n5 - 1);
                g.a(graphics, n2 + n4 - 14, n3 + n5 - 1, n2 + n4 - 2, n3 + n5 - 1);
                g.a(graphics, 0xADAAAD);
                g.a(graphics, n2 + 5, n3, n2 + 8, n3);
                g.a(graphics, n2 + n4 - 9, n3, n2 + n4 - 6, n3);
                g.a(graphics, n2 + 5, n3 + n5 - 1, n2 + 8, n3 + n5 - 1);
                g.a(graphics, n2 + n4 - 9, n3 + n5 - 1, n2 + n4 - 6, n3 + n5 - 1);
                g.a(graphics, 0x949A94);
                g.a(graphics, n2, n3 + 1, n2, n3 + n5 - 2);
                g.a(graphics, n2 + n4 - 1, n3 + 1, n2 + n4 - 1, n3 + n5 - 2);
                g.a(graphics, 0xADAAAD);
                g.a(graphics, n2, n3 + 4, n2, n3 + n5 - 5);
                g.a(graphics, n2 + n4 - 1, n3 + 4, n2 + n4 - 1, n3 + n5 - 5);
                return;
            }
            case 3: {
                g.a(graphics, n8);
                g.a(graphics, n2, n3 - 1, n2 + n4 - 1, n3 - 1);
                g.a(graphics, n2, n3 + n5, n2 + n4 - 1, n3 + n5);
                g.a(graphics, n2 - 1, n3, n2 - 1, n3 + n5 - 1);
                g.a(graphics, n2 + n4, n3, n2 + n4, n3 + n5 - 1);
                g.a(graphics, n2, n3, n8);
                g.a(graphics, n2 + n4 - 1, n3, n8);
                g.a(graphics, n2, n3 + n5 - 1, n8);
                g.a(graphics, n2 + n4 - 1, n3 + n5 - 1, n8);
                return;
            }
        }
        f.b(graphics, n2, n3 + 1, 1, n5 - 2, n7);
        f.b(graphics, n2 + n4 - 1, n3 + 1, 1, n5 - 2, n7);
        cM = 1;
        while (cM < n4 - 1) {
            f.b(graphics, n2 + cM, n3, 1, n5, n7);
            f.b(graphics, n2 + cM, n3 + 1, 1, n5 - 2, 0);
            ++cM;
        }
    }

    public final void q() {
        block0 : switch (cY) {
            case 160: {
                switch (al) {
                    case 1: {
                        if (dU[dW] == 0) {
                            cv = 5;
                            g.i(3);
                            break block0;
                        }
                        this.o();
                        g.i(1);
                        break block0;
                    }
                    case 0: 
                    case 2: {
                        this.o();
                        g.i(1);
                    }
                }
                return;
            }
            case 161: {
                ae = (byte)dU[dW];
                cv = 1;
                g.i(3);
                this.c(1300);
                return;
            }
            case 162: 
            case 163: 
            case 164: {
                af = cY;
                ab = (dV[dW] - 162 + 1) * 10 + dU[dW] + 1;
                cv = 1;
                g.i(3);
                this.c(1293);
                return;
            }
            case 10: {
                switch (dU[dW]) {
                    case 0: {
                        this.k(11);
                        break block0;
                    }
                    case 1: {
                        this.k(12);
                        break block0;
                    }
                    case 2: {
                        this.k(16);
                        break block0;
                    }
                    case 3: {
                        cv = 1;
                        g.i(3);
                        this.c(288);
                        break block0;
                    }
                    case 4: {
                        this.k(87);
                        break block0;
                    }
                    case 5: {
                        this.k(161);
                    }
                }
                return;
            }
            case 11: {
                switch (dU[dW]) {
                    case 0: {
                        bz = 0;
                        cv = 2;
                        g.i(3);
                        this.c(512);
                        break block0;
                    }
                    case 1: {
                        bz = 1;
                        cv = 2;
                        g.i(3);
                        this.c(512);
                        break block0;
                    }
                    case 2: {
                        this.k(20);
                        break block0;
                    }
                    case 3: {
                        this.k(87);
                        break block0;
                    }
                    case 4: {
                        this.k(161);
                    }
                }
                return;
            }
            case 12: {
                switch (dU[dW]) {
                    case 0: {
                        bz = (byte)2;
                        cv = 3;
                        g.i(3);
                        this.c(512);
                        break block0;
                    }
                    case 1: {
                        bz = (byte)2;
                        this.k(21);
                        break block0;
                    }
                    case 2: {
                        this.k(87);
                        break block0;
                    }
                    case 3: {
                        this.k(161);
                    }
                }
                return;
            }
            case 16: {
                switch (dU[dW]) {
                    case 0: {
                        cv = 1;
                        g.i(3);
                        this.c(1296);
                        break block0;
                    }
                    case 1: {
                        cv = 1;
                        g.i(3);
                        this.c(1287);
                        break block0;
                    }
                    case 2: {
                        cv = 1;
                        g.i(3);
                        this.c(1289);
                        break block0;
                    }
                    case 3: {
                        cv = 1;
                        g.i(3);
                        this.c(1298);
                        break block0;
                    }
                    case 4: {
                        C = 0;
                        B = 0;
                        bG = cF;
                        this.k(84);
                        break block0;
                    }
                    case 5: {
                        C = 0;
                        bG = cE;
                        this.k(85);
                    }
                }
                return;
            }
            case 82: {
                cv = 5;
                g.i(3);
                this.c(1291);
                return;
            }
            case 84: {
                return;
            }
            case 86: {
                switch (dU[dW]) {
                    case 0: {
                        cv = 5;
                        g.i(3);
                        this.c(1280);
                        break block0;
                    }
                    case 1: {
                        this.m(1);
                    }
                }
                return;
            }
            case 88: {
                switch (dU[dW]) {
                    case 0: {
                        if (cs == -4) {
                            if (++an <= 2) break;
                            an = 0;
                            break block0;
                        }
                        if (cs != -3 || --an >= 0) break;
                        an = 2;
                        break block0;
                    }
                    case 1: {
                        if (cs != -3 && cs != -4) break;
                        ap = (ap + 1) % 2;
                        break block0;
                    }
                    case 2: {
                        if (cs == -3) {
                            this.ai();
                            break block0;
                        }
                        if (cs != -4) break;
                        this.aj();
                    }
                }
                return;
            }
            case 87: {
                this.k(89);
                return;
            }
            case 20: {
                switch (dU[dW]) {
                    case 0: {
                        bz = 0;
                        break;
                    }
                    case 1: {
                        bz = 1;
                    }
                }
                this.k(21);
            }
        }
    }

    final void r() {
        this.e();
        this.c(e, cW, cX, 116, 76, 0);
        int n2 = 0;
        while (n2 < 4) {
            this.a(e, cW, cX - 31 + 12 * n2, bF[n2], 0xFFFFFF);
            ++n2;
        }
        this.r(cX + 22);
    }

    final void s() {
        cL = 0;
        while (cL < 4) {
            if (bQ[cL] && cL != S) {
                switch (cc[cL]) {
                    case 0: {
                        this.b(e);
                        break;
                    }
                    case 1: 
                    case 4: {
                        this.t();
                        break;
                    }
                    case 5: {
                        this.u();
                        break;
                    }
                    case 6: {
                        this.v();
                        break;
                    }
                    default: {
                        this.x();
                    }
                }
            }
            ++cL;
        }
        cL = S;
        switch (cc[S]) {
            case 2: 
            case 28: {
                this.w();
                return;
            }
            case 6: {
                this.v();
                return;
            }
        }
        this.x();
    }

    final void t() {
        cC = cc[cL];
        if (ca[cL] == 2) {
            cC += 21;
        }
        g.cn[g.cL] = l.eg[cC];
        int n2 = cL;
        ck[n2] = ck[n2] - 2;
        g.cm[g.cL] = -1;
        this.c(e, cL);
    }

    final void u() {
        cC = ca[cL] == 2 ? 26 : 5;
        g.cn[g.cL] = l.eg[cC];
        if (cd[cL] == 0) {
            int n2 = cL;
            ck[n2] = ck[n2] - 6;
            this.t(3);
        } else if (cd[cL] == 1) {
            int n3 = cL;
            ck[n3] = ck[n3] - 2;
        }
        g.cm[g.cL] = -1;
        this.c(e, cL);
    }

    final void v() {
        cC = ca[cL] == 2 ? 27 : 6;
        g.cn[g.cL] = l.eg[cC] + Q;
        g.cm[g.cL] = -1;
        this.c(e, cL);
    }

    final void w() {
        g.cn[g.cL] = ca[cL] == 2 ? l.eg[23] : l.eg[2];
        int n2 = cL;
        ck[n2] = ck[n2] + bl;
        int n3 = cL;
        cl[n3] = cl[n3] + bm;
        g.cm[g.cL] = -1;
        this.c(e, cL);
    }

    final void x() {
        cC = cc[cL];
        if (ca[cL] == 2 && cC == 3) {
            cC = 24;
        }
        if (cC == 12 && Q >= 4) {
            bo = Q;
            Q = 4;
        }
        g.cn[g.cL] = l.eg[cC] + Q;
        bJ = l.ep[cC][3 * Q + 1];
        int n2 = cL;
        ck[n2] = ck[n2] + ((bJ & 0x80) > 0 ? -1 : 1) * (bJ & 0x7F);
        bJ = l.ep[cC][3 * Q + 2];
        int n3 = cL;
        cl[n3] = cl[n3] + ((bJ & 0x80) > 0 ? -1 : 1) * (bJ & 0x7F);
        this.c(e, cL);
        if (cC == 12 && Q >= 4) {
            Q = bo;
        }
    }

    final void b(Graphics graphics) {
        if (bW[cL] > 0) {
            if ((cY == 104 || cY == 105) && ca[cL] != 2 && aU == 1) {
                if (da < 3) {
                    g.cn[g.cL] = l.eg[cC] + da;
                    int n2 = cL;
                    ck[n2] = ck[n2] + ((bJ & 0x80) > 0 ? -1 : 1) * (bJ & 0x7F);
                    int n3 = cL;
                    cl[n3] = cl[n3] + ((bJ & 0x80) > 0 ? -1 : 1) * (bJ & 0x7F);
                }
            } else {
                if (da % 4 == co[cL]) {
                    g.cn[g.cL] = da / 4 % 2;
                }
                if (cn[cL] != 0 && cn[cL] != 1) {
                    g.cn[g.cL] = 0;
                }
            }
        } else {
            g.cn[g.cL] = l.eg[6] + 1;
        }
        g.cm[g.cL] = -1;
        if (cc[S] == 12 && cL == T && Q >= 4) {
            g.cm[g.cL] = 10 + Q - 4;
        }
        this.c(graphics, cL);
    }

    final void b(Graphics graphics, int n2) {
        cL = 0;
        while (cL < 4) {
            block4: {
                block5: {
                    if (!bQ[cL]) break block4;
                    if (bR[cL] % 2 == n2) break block5;
                    if (n2 != 2) break block4;
                    boolean bl = aU == 1 ? bR[cL] % 2 == bR[0] : bR[cL] % 2 != bR[0];
                    if (!bl) break block4;
                }
                this.c(graphics, bR[cL] % 2 == 0 ? 0 : cQ - 60, bR[cL] / 2 == 0 ? 12 : cR - 12 - 15, 60, 15, 1);
                this.a(bR[cL] % 2 == 0 ? 30 : cQ - 30, bR[cL] / 2 == 0 ? 14 : cR - 12 - 15 + 2, bM[cL], 16400640);
                cO = cW;
                cP = bR[cL] / 2 == 0 ? 38 : cR - 12 - 15 - 11;
                this.c(graphics, cO, cP, cQ, 22, 0);
                this.a(cO, cP - 5, n2 == 2 ? bO[cL] : bN[cL], 0xFFFFFF);
            }
            ++cL;
        }
    }

    final void y() {
        this.c(e, cW, cX, 78, 86, 0);
        this.a(e, cW, cX - 34, bM[ct], 0xFFFFFF);
        this.a(e, cW, cX - 20, l.eX[27] + "." + bS[ct], 0xFFFFFF);
        this.f(e, cW + 22, cX + 12, bT[ct]);
        this.b(e, cW - 27, cX + 11, l.eX[49], 0xFFFFFF);
        this.f(e, cW + 22, cX + 24, bU[ct]);
        this.b(e, cW - 27, cX + 23, l.eX[50], 0xFFFFFF);
    }

    final void c(Graphics graphics) {
        cL = 0;
        while (cL < 4) {
            if (bQ[cL]) {
                this.b(graphics);
            }
            ++cL;
        }
    }

    final void d(Graphics graphics) {
        if (bR[bA] % 2 == 0) {
            this.a(graphics, 30, bR[bA] / 2 == 0 ? 14 : cR - 12 - 15 + 2, bP[bA].length() == 0 || aR % 2 == 0 ? bM[bA] : bP[bA], 16400640);
            if (da % 2 == 0) {
                g.c(graphics, l.eq[48], (bR[bA] / 2 == 0 ? 19 : cR - 19) + l.er[48], 12, df[48]);
                return;
            }
            g.a(graphics, l.eq[48] + 1, (bR[bA] / 2 == 0 ? 19 : cR - 19) + l.er[48], df[48], 12, 1);
            return;
        }
        this.a(graphics, cQ - 30, bR[bA] / 2 == 0 ? 14 : cR - 12 - 15 + 2, bP[bA].length() == 0 || aR % 2 == 0 ? bM[bA] : bP[bA], 16400640);
        if (da % 2 == 0) {
            g.a(graphics, cQ - (1 + l.eq[48]), (bR[bA] / 2 == 0 ? 19 : cR - 19) + l.er[48], 12, df[48]);
            return;
        }
        g.b(graphics, cQ - (2 + l.eq[48]), (bR[bA] / 2 == 0 ? 19 : cR - 19) + l.er[48], 12, df[48]);
    }

    final void z() {
        this.c(e, cW, cX, 102, 86, 0);
        this.a(cW, cX - 30, bH, 0xFFFFFF);
        this.a(cW, cX - 15, l.eX[26] + aQ + "/" + aP, 0xFFFFFF);
        cL = 1;
        while (cL < 4) {
            if (bQ[cL]) {
                if (bR[cL] == 1) {
                    this.a(cW - 24, cX + 4, bM[cL], 0xFFFFFF);
                    this.b(cW + 4, cX + 4, l.eX[27] + "" + bS[cL], 0xFFFFFF);
                } else if (bR[cL] == 3) {
                    this.a(cW - 24, cX + 20, bM[cL], 0xFFFFFF);
                    this.b(cW + 4, cX + 20, l.eX[27] + "" + bS[cL], 0xFFFFFF);
                }
            }
            ++cL;
        }
    }

    static void A() {
        bJ = Math.abs(h.nextInt()) % 3;
        switch (bJ) {
            case 0: {
                cz = 4;
                break;
            }
            case 1: {
                cz = 8;
                break;
            }
            default: {
                cz = 5;
            }
        }
        g.b(1);
        cA = cW - 44;
        bt = true;
    }

    final void e(Graphics graphics) {
        if (bt) {
            int n2 = cX;
            if (bz == 0) {
                n2 = cT - 26;
            }
            this.c(graphics, cW, n2 + 3, 110, 38, 0);
            f.a(graphics, df[35], cW - 44 + l.eq[35], n2 + l.er[35], 0);
            f.a(graphics, df[36], cW - 44 + l.eq[36], n2 + l.er[36], 0);
            f.a(graphics, df[37], cW - 44 + l.eq[37], n2 + l.er[37], 0);
        }
    }

    final void f(Graphics graphics) {
        int n2 = cX;
        if (bz == 0) {
            n2 = cT - 26;
        }
        if (cY == 98) {
            if (aS == 100) {
                f.a(graphics, df[52], cW - 44 + 72 + l.eq[52], n2 + l.er[52], 0);
                this.t(0);
            } else if (aS == 20) {
                f.a(graphics, df[53], cW - 44 + 72 + l.eq[53], n2 + l.er[53], 0);
            } else {
                f.a(graphics, df[49], cA - 20 + l.eu[35], n2 - 11 + l.ev[35], 0);
                this.t(0);
            }
        }
        if (da % 2 == 0) {
            f.a(graphics, df[38], cW - 44 + 72 + l.eq[38], n2 + l.er[38], 0);
        }
        f.a(graphics, df[34], cA + l.eq[34], n2 + l.er[34], 0);
        if (cY == 97 && cA > cW - 44 + 72) {
            this.C();
        }
    }

    final void B() {
        d = 0;
        g.i(97);
    }

    final void C() {
        d = 0;
        if (bB > 2) {
            aS = 0;
        } else {
            if ((cz == 6 || cz == 7) && Math.abs(cW - 44 + 72 - cA) <= cz / 2) {
                cA = cW - 44 + 72;
            }
            aS = cA < cW - 44 + 72 ? 20 + cA - cW + 44 : (cA == cW - 44 + 72 ? 100 : 20);
        }
        g.i(98);
    }

    static void a(Graphics graphics, Image[] imageArray, a[] aArray, int n2) {
        a a2 = aArray[0];
        int n3 = 0;
        if (n2 >= 400) {
            n3 = n2 - 400;
        } else if (n2 >= 300) {
            n3 = n2 - 300;
        } else if (n2 >= 200) {
            n3 = n2 - 200;
            a2 = aArray[2];
        } else if (n2 >= 100) {
            n3 = n2 - 100;
            a2 = aArray[1];
        } else {
            n3 = n2;
        }
        if (bn) {
            f.a(graphics, imageArray[1], cQ - (cU - a2.g[n3] + a2.e[n3]), cV - a2.h[n3], a2.e[n3], a2.f[n3], a2.c[n3], a2.d[n3]);
            return;
        }
        f.a(graphics, imageArray[0], cU - a2.g[n3], cV - a2.h[n3], a2.e[n3], a2.f[n3], a2.c[n3], a2.d[n3]);
    }

    final void c(Graphics graphics, int n2) {
        int n3;
        bn = bR[n2] % 2 != 0;
        cU = ck[n2];
        cV = cl[n2];
        this.a(n2, true);
        if (ca[n2] != 2) {
            this.a(dF, dG, "sprshadow");
            g.a(graphics, dF, dG, cn[n2]);
        }
        boolean bl = false;
        if (ca[n2] == 2) {
            bl = l.eo[cn[n2] % 100];
            if (bl) {
                this.a(dJ, dK, "spr_wp_mon", 0);
                g.a(graphics, dJ, dK, cn[n2]);
            }
        } else {
            n3 = cn[n2] / 100;
            if (bY[n2] == 0) {
                if (n3 == 2) {
                    bl = l.ek[cn[n2] % 100];
                }
            } else {
                bl = n3 == 1 ? l.em[cn[n2] % 100] : (n3 == 2 ? l.en[cn[n2] % 100] : l.el[cn[n2] % 100]);
            }
            if (bl) {
                this.a(dy[bY[n2]], dz[bY[n2]], "sprwp" + (bY[n2] + 1));
                g.a(graphics, dy[bY[n2]], dz[bY[n2]], cn[n2]);
            }
        }
        if (ca[n2] == 2) {
            this.a(dH, dI, "spr_mon", 0);
            g.a(graphics, dH, dI, cn[n2]);
        } else {
            this.a(dF, dG, "sprshadow");
            g.a(graphics, dF, dG, cn[n2]);
            this.a(du, dv, "sprbody");
            g.a(graphics, du, dv, cn[n2]);
        }
        n3 = 0;
        if (ca[n2] != 2) {
            if (ca[n2] == 0) {
                n3 = bZ[n2];
            }
            this.a(dw[n3], dx[n3], "sprhead" + (n3 + 1));
            g.a(graphics, dw[n3], dx[n3], cn[n2]);
        }
        if (bQ[n2] && cY != 105) {
            switch (cp[n2]) {
                case 11: {
                    this.V();
                    g.e(graphics, 0);
                    break;
                }
                case 12: {
                    this.V();
                    g.e(graphics, 1);
                    break;
                }
                case 13: {
                    this.V();
                    g.e(graphics, 2);
                }
            }
        }
        if (!bl) {
            if (ca[n2] == 2) {
                this.a(dJ, dK, "spr_wp_mon", 0);
                g.a(graphics, dJ, dK, cn[n2]);
            } else {
                this.a(dy[bY[n2]], dz[bY[n2]], "sprwp" + (bY[n2] + 1));
                g.a(graphics, dy[bY[n2]], dz[bY[n2]], cn[n2]);
            }
        }
        this.a(n2, false);
    }

    final void a(int n2, boolean bl) {
        if (ca[n2] == 2) {
            if (!bl) {
                this.a(dN, dO, "spr_sword_mon", 0);
                g.a(e, dN, dO, cn[n2]);
                this.a(dL, dM, "spr_eff_mon", 0);
                g.a(e, dL, dM, cn[n2]);
                return;
            }
        } else {
            int n3;
            boolean bl2;
            if (!bl) {
                this.a(dA[bY[n2]], dB[bY[n2]], "sprsword" + (bY[n2] + 1));
                g.a(e, dA[bY[n2]], dB[bY[n2]], cn[n2]);
                this.a(dC[0], dD[0], "spreff1");
                g.a(e, dC[0], dD[0], cn[n2]);
            }
            if (bl == (bl2 = (n3 = cn[n2] / 100) == 1 ? l.ei[cn[n2] % 100] : (n3 == 2 ? l.ej[cn[n2] % 100] : false))) {
                this.a(dC[1], dD[1], "spreff2");
                g.a(e, dC[1], dD[1], cn[n2]);
            }
        }
    }

    final void D() {
        if (X >= 5) {
            X = -1;
            cL = 0;
            while (cL < 4) {
                if (bQ[cL] && (cL == S || cL == T || cL == U)) {
                    if (bW[cL] != cf[cL]) {
                        g.bW[g.cL] = cf[cL];
                    }
                    if (bX[cL] != cg[cL]) {
                        g.bX[g.cL] = cg[cL];
                    }
                }
                ++cL;
            }
        }
        if (Q >= R) {
            Q = 0;
            switch (cc[S]) {
                case 2: 
                case 17: 
                case 18: 
                case 19: {
                    g.ck[g.S] = cQ - 67;
                    g.cl[g.S] = cX + 65;
                    if (bz != 0) {
                        int n2 = S;
                        cl[n2] = cl[n2] + (cK[12 + bC] / 2 == 0 ? -1 : 1) * 23;
                    }
                    switch (cK[4 + bC]) {
                        case 3: {
                            g.cc[g.S] = 9;
                            break;
                        }
                        case 4: {
                            g.cc[g.S] = 10;
                            break;
                        }
                        case 5: {
                            g.cc[g.S] = 11;
                            break;
                        }
                        case 6: {
                            g.cc[g.S] = 14;
                            break;
                        }
                        case 7: {
                            g.cc[g.S] = 15;
                            break;
                        }
                        case 0: {
                            g.cc[g.S] = 3;
                        }
                    }
                    break;
                }
                case 8: {
                    switch (cK[4 + bC]) {
                        case 3: 
                        case 4: 
                        case 5: {
                            g.cc[g.S] = 2;
                            bl = (cQ - 67 - 42) / l.eh[cc[S]];
                            if (bz == 0) {
                                bm = 0;
                                break;
                            }
                            if (bR[S] / 2 == cK[12 + bC] / 2) {
                                bm = 0;
                                break;
                            }
                            if (bR[S] / 2 == 0) {
                                bm = 46 / l.eh[cc[S]];
                                break;
                            }
                            bm = -46 / l.eh[cc[S]];
                            break;
                        }
                        case 6: 
                        case 7: {
                            if (bz == 0) {
                                g.cc[g.S] = 17;
                                break;
                            }
                            if (cK[12 + bC] / 2 == cK[0 + bC] / 2) {
                                g.cc[g.S] = 17;
                                break;
                            }
                            if (cK[12 + bC] / 2 == 1) {
                                g.cc[g.S] = 18;
                                break;
                            }
                            g.cc[g.S] = 19;
                            break;
                        }
                        case 8: {
                            g.cc[g.S] = 20;
                        }
                    }
                    break;
                }
                case 20: {
                    switch (cK[4 + bC]) {
                        case 8: {
                            g.cc[g.S] = 16;
                        }
                    }
                    break;
                }
                case 3: 
                case 9: 
                case 10: 
                case 11: 
                case 14: 
                case 15: 
                case 16: {
                    if (cK[28 + bC] == 3 && bR[S] == cK[0 + bC]) {
                        bJ = S;
                        S = T;
                        T = bJ;
                        g.cc[g.S] = 3;
                        V = 1;
                        break;
                    }
                    X = 0;
                    if (cK[28 + bC] == 3) {
                        bJ = S;
                        S = T;
                        T = bJ;
                        g.cc[g.T] = 0;
                        g.h(T);
                    }
                    g.cc[g.S] = 28;
                    bl = (42 - ck[S]) / l.eh[cc[S]];
                    if (bz == 0) {
                        bm = 0;
                        break;
                    }
                    if (bR[S] / 2 == cK[12 + bC] / 2) {
                        bm = 0;
                        break;
                    }
                    if (bR[S] / 2 == 0) {
                        bm = -46 / l.eh[cc[S]];
                        break;
                    }
                    bm = 46 / l.eh[cc[S]];
                    break;
                }
                case 12: 
                case 13: 
                case 28: {
                    g.h(S);
                    bJ = -1;
                    cL = 0;
                    while (cL < 4) {
                        if (bQ[cL]) {
                            if (cc[S] == 13 && bR[S] % 2 == bR[cL] % 2) {
                                g.cp[g.cL] = cK[4 + bC];
                                g.cq[g.cL] = 3;
                            }
                            if (bW[cL] == 0 && cj[cL] != 0) {
                                bJ = cL;
                                g.cc[g.bJ] = 6;
                                if (bR[cL] % 2 == bR[0] % 2) {
                                    --bb;
                                } else {
                                    --bc;
                                }
                            }
                        }
                        ++cL;
                    }
                    if (bJ > 0) {
                        if (cc[S] != 6) {
                            g.cc[g.S] = 0;
                        }
                        S = bJ;
                        break;
                    }
                    ++bC;
                    this.E();
                    break;
                }
                case 6: {
                    ++bC;
                    this.E();
                }
            }
            R = l.eh[cc[S]];
        }
        if (cc[S] != 6) {
            this.F();
        }
    }

    final void E() {
        if (aT == 0) {
            g.i(100);
            return;
        }
        if (bC < aT) {
            g.i(101);
            return;
        }
        g.i(93);
    }

    /*
     * Enabled force condition propagation
     * Lifted jumps to return sites
     */
    final void F() {
        if (cc[S] != 12 && cc[S] != 13 && cK[28 + bC] != 3) {
            if (T != -1 && cc[T] != 0) {
                int n2 = T;
                cd[n2] = cd[n2] + 1;
                if (cd[T] >= ce[T]) {
                    g.cc[g.T] = 0;
                    g.h(T);
                }
            }
            if (U != -1 && cc[U] != 0) {
                int n3 = U;
                cd[n3] = cd[n3] + 1;
                if (cd[U] >= ce[U]) {
                    g.cc[g.U] = 0;
                    g.h(U);
                }
            }
        }
        switch (cc[S]) {
            case 3: 
            case 9: 
            case 10: 
            case 11: 
            case 14: {
                switch (V) {
                    case 1: 
                    case 4: {
                        if (cc[S] == 11 && Q == 17) {
                            this.G();
                            g.ce[g.T] = 3;
                            return;
                        }
                        if (Q % 2 != 1) return;
                        if (cc[S] == 11 && Q > 10) return;
                        this.G();
                        g.ce[g.T] = 2;
                        return;
                    }
                    case 5: {
                        if (cK[28 + bC] == 3) {
                            if (Q != 0) return;
                            g.cc[g.T] = 5;
                            g.cd[g.T] = 0;
                            g.ce[g.T] = R;
                            return;
                        } else {
                            if (Q % 2 != 1) return;
                            this.G();
                            g.ce[g.T] = 2;
                        }
                    }
                    default: {
                        return;
                    }
                }
            }
            case 15: {
                switch (V) {
                    case 1: 
                    case 4: {
                        if (Q != 2) return;
                        this.G();
                        g.ce[g.T] = 4;
                    }
                }
                return;
            }
            case 16: {
                switch (V) {
                    case 1: 
                    case 4: {
                        if (Q != 8) return;
                        this.G();
                        g.ce[g.T] = 3;
                        if (U == -1) return;
                        g.cc[g.U] = W;
                        g.cd[g.U] = 0;
                        g.ce[g.U] = 3;
                    }
                }
                return;
            }
            case 12: {
                if (Q != 4) return;
                X = 0;
                this.t(6);
                if (cK[4 + bC] == 2) return;
                return;
            }
            case 13: {
                if (Q == 4 && cK[4 + bC] == 13) {
                    cL = 0;
                    while (cL < 4) {
                        ++cL;
                    }
                    this.t(5);
                    return;
                }
                if (Q == 7) {
                    cL = 0;
                    while (cL < 4) {
                        ++cL;
                    }
                    this.t(5);
                    return;
                }
                if (Q != 5) return;
                X = 0;
            }
        }
    }

    final void G() {
        g.cc[g.T] = V;
        g.cd[g.T] = 0;
        if (cc[S] == 16 || cc[S] == 15) {
            this.t(2);
            return;
        }
        this.t(0);
    }

    final void H() {
        this.c(e, cW, cX, 88, 72, 0);
        this.a(e, cW, cX - 20, bH, 0xFFFFFF);
        bL = l.eX[26] + " " + aQ;
        this.a(e, cW, cX - 4, bL, 0xFFFFFF);
        this.a(e, cW, cX + 12, l.eX[28], 0xFFFFFF);
    }

    final void I() {
        if (X < 0) {
            return;
        }
        cL = 0;
        while (cL < 4) {
            if (bQ[cL] && (cL == S || cL == T || cL == U)) {
                if (bW[cL] != cf[cL]) {
                    int n2 = cL;
                    bW[n2] = bW[n2] + ch[cL];
                    if (bW[cL] < 0) {
                        g.bW[g.cL] = 0;
                    }
                }
                if (bX[cL] != cg[cL]) {
                    int n3 = cL;
                    bX[n3] = bX[n3] + ci[cL];
                    if (bX[cL] < 0) {
                        g.bX[g.cL] = 0;
                    }
                }
                if (cj[cL] != 0) {
                    boolean bl = bn = bR[cL] % 2 != 0;
                    if (!bn) {
                        this.e(e, ck[cL], cl[cL] - 40 - 2 * X, cj[cL]);
                    } else {
                        this.e(e, cQ - ck[cL], cl[cL] - 40 - 2 * X, cj[cL]);
                    }
                }
            }
            ++cL;
        }
        g.g(e);
        cL = 0;
        while (cL < 4) {
            if (bQ[cL] && (cL == S || cL == T || cL == U) && bW[cL] == 0) {
                g.bW[g.cL] = 1;
            }
            ++cL;
        }
        ++X;
    }

    public static void g(Graphics graphics) {
        cL = 0;
        while (cL < 4) {
            if (bQ[cL]) {
                int n2;
                int n3 = bW[cL] * bK / bV[cL];
                if (n3 == 0 && bW[cL] > 0) {
                    n3 = 1;
                }
                int n4 = bR[cL] % 2 == 0 ? 28 : cQ - 28 - bK;
                int n5 = bR[cL] / 2 == 0 ? 0 : cR - 3 - 6;
                --n3;
                if (bW[cL] > 0) {
                    if (bR[cL] % 2 == 0) {
                        f.a(graphics, n4, n5, n3, 0xB50000);
                        f.a(graphics, n4, n5 + 1, n3, 0xFF0000);
                        f.a(graphics, n4, n5 + 2, n3, 0xB50000);
                    } else {
                        n2 = bK - n3;
                        f.a(graphics, n4 + n2, n5, n3, 0xB50000);
                        f.a(graphics, n4 + n2, n5 + 1, n3, 0xFF0000);
                        f.a(graphics, n4 + n2, n5 + 2, n3, 0xB50000);
                    }
                }
                if ((n3 = bX[cL] * bK / 100) == 0 && bX[cL] > 0) {
                    n3 = 1;
                }
                n4 = bR[cL] % 2 == 0 ? 28 : cQ - 28 - bK;
                n5 = bR[cL] / 2 == 0 ? 6 : cR - 3;
                --n3;
                if (bX[cL] > 0) {
                    if (bR[cL] % 2 == 0) {
                        f.a(graphics, n4, n5, n3, 3223675);
                        f.a(graphics, n4, n5 + 1, n3, 9216734);
                        f.a(graphics, n4, n5 + 2, n3, 3223675);
                    } else {
                        n2 = bK - n3;
                        f.a(graphics, n4 + n2, n5, n3, 3223675);
                        f.a(graphics, n4 + n2, n5 + 1, n3, 9216734);
                        f.a(graphics, n4 + n2, n5 + 2, n3, 3223675);
                    }
                }
            }
            ++cL;
        }
    }

    public static void J() {
        cL = 0;
        while (cL < 4) {
            g.bQ[g.cL] = false;
            ++cL;
        }
        bb = 0;
        bc = 0;
    }

    final void b(Graphics graphics, int n2, int n3, int n4) {
        g.b(graphics, n2, n3, n4, 1);
    }

    final void c(Graphics graphics, int n2, int n3, int n4) {
        g.b(graphics, n2, n3, n4, 2);
    }

    final void d(Graphics graphics, int n2, int n3, int n4) {
        g.b(graphics, n2, n3, n4, 3);
    }

    final void e(Graphics graphics, int n2, int n3, int n4) {
        g.b(graphics, n2, n3, n4, 4);
    }

    final void a(int n2, int n3, int n4) {
        g.b(e, n2, n3, n4, 5);
    }

    final void f(Graphics graphics, int n2, int n3, int n4) {
        g.b(graphics, n2, n3, n4, 0);
    }

    final void b(int n2, int n3, int n4) {
        g.b(e, n2, n3, n4, 0);
    }

    final void c(int n2, int n3, int n4) {
        g.b(e, n2, n3, n4, 1);
    }

    final void d(int n2, int n3, int n4) {
        g.b(e, n2, n3, n4, 0);
    }

    final void e(int n2, int n3, int n4) {
        g.b(e, n2, n3, n4, 1);
    }

    public static void b(Graphics graphics, int n2, int n3, int n4, int n5) {
        int n6 = 1;
        int n7 = 0;
        switch (n5) {
            case 0: 
            case 1: 
            case 7: {
                while (n4 / n6 > 0 || n6 == 1) {
                    int n8 = n4 % (n6 * 10) / n6;
                    f.a(graphics, dh[n5], n2, n3, 5, 8, n8 * 5, 0);
                    n2 -= 6;
                    if (++n7 % 3 != 0 || n4 / (n6 *= 10) <= 0) continue;
                    f.a(graphics, dh[n5], n2 += 2, n3 + 5, 2, 3, 50, 5);
                    n2 -= 6;
                }
                return;
            }
            case 5: {
                f.a(graphics, dh[6], n2 - 3, n3 - 1, 3, 10, 7, 0);
                n2 -= 9;
                while (n4 / n6 > 0 || n6 == 1) {
                    int n9 = n4 % (n6 * 10) / n6;
                    f.a(graphics, dh[n5], n2, n3, 5, 8, n9 * 5, 16);
                    n2 -= 6;
                    if (++n7 % 3 != 0 || n4 / (n6 *= 10) <= 0) continue;
                    f.b(graphics, n2 += 2, n3 + 6, 1, 3, 65280);
                    n2 -= 6;
                }
                f.a(graphics, dh[6], n2 - 2, n3 - 1, 7, 10, 0, 0);
                return;
            }
            case 2: {
                while (n4 / n6 > 0 || n6 == 1) {
                    int n10 = n4 % (n6 * 10) / n6;
                    f.a(graphics, dh[n5], n2, n3, 7, 11, n10 * 7, 0);
                    n2 -= 8;
                    n6 *= 10;
                }
                return;
            }
            case 3: {
                while (n4 / n6 > 0 || n6 == 1) {
                    int n11 = n4 % (n6 * 10) / n6;
                    f.a(graphics, dh[n5], n2, n3, 12, 13, n11 * 12, 0);
                    n2 -= 12;
                    n6 *= 10;
                }
                return;
            }
            case 4: {
                if (n4 < 0) {
                    n4 = -n4;
                    br = true;
                } else {
                    br = false;
                }
                while (n4 / n6 > 0 || n6 == 1) {
                    int n12 = n4 % (n6 * 10) / n6;
                    f.a(graphics, dh[n5], n2, n3, 6, 10, n12 * 6, br ? 10 : 0);
                    n2 -= 7;
                    n6 *= 10;
                }
                break;
            }
        }
    }

    public static void h(int n2) {
        g.ck[n2] = 42;
        g.cl[n2] = cX + 65;
        if (bz != 0) {
            int n3 = n2;
            cl[n3] = cl[n3] + (bR[n2] / 2 == 0 ? -1 : 1) * 23;
        }
    }

    public static void i(int n2) {
        cY = n2;
        da = 0;
    }

    public static void K() {
        byte[] byArray = new byte[28];
        int n2 = 0;
        while (n2 < byArray.length) {
            byArray[n2] = 0;
            ++n2;
        }
        byArray[0] = (byte)an;
        byArray[1] = (byte)am;
        byte[] byArray2 = i.getBytes();
        n2 = 0;
        while (n2 < byArray2.length) {
            byArray[2 + n2] = byArray2[n2];
            ++n2;
        }
        byArray2 = j.getBytes();
        n2 = 0;
        while (n2 < byArray2.length) {
            byArray[14 + n2] = byArray2[n2];
            ++n2;
        }
        try {
            RecordStore recordStore = RecordStore.openRecordStore((String)"pow_mp_save", (boolean)true);
            if (recordStore.getNumRecords() == 0) {
                recordStore.addRecord(byArray, 0, byArray.length);
            }
            recordStore.setRecord(1, byArray, 0, byArray.length);
            return;
        }
        catch (Exception exception) {
            return;
        }
    }

    public final boolean L() {
        byte[] byArray = new byte[28];
        an = 0;
        am = 4;
        i = "";
        j = "";
        try {
            RecordStore recordStore = RecordStore.openRecordStore((String)"pow_mp_save", (boolean)false);
            if (recordStore == null || recordStore.getNumRecords() < 1) {
                return false;
            }
            byArray = recordStore.getRecord(1);
        }
        catch (Exception exception) {}
        if (byArray.length >= 28) {
            an = byArray[0];
            am = byArray[1];
            i = g.c(g.a(byArray, 2, 14));
            j = g.c(g.a(byArray, 14, 28));
            return true;
        }
        return false;
    }

    public static String a(byte[] byArray, int n2, int n3) {
        int n4 = n2;
        int n5 = n3;
        String string = null;
        try {
            int n6 = n5 - n4;
            byte[] byArray2 = new byte[n6 + 2];
            byte[] byArray3 = byArray2;
            byArray2[0] = (byte)(n6 >> 8 & 0xFF);
            byArray3[1] = (byte)(n6 & 0xFF);
            System.arraycopy(byArray, n4, byArray3, 2, n6);
            ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(byArray3, 0, byArray3.length);
            DataInputStream dataInputStream = new DataInputStream(byteArrayInputStream);
            string = dataInputStream.readUTF();
            byteArrayInputStream.close();
            dataInputStream.close();
        }
        catch (Exception exception) {}
        return string;
    }

    static String c(String string) {
        int n2 = 0;
        int n3 = string.length();
        n2 = 0;
        while (n2 < n3) {
            if (string.charAt(n2) < ' ') break;
            ++n2;
        }
        if (n2 == 0) {
            return "";
        }
        return string.substring(0, n2);
    }

    final void M() {
        int n2 = 0;
        switch (z) {
            case 0: {
                if (x) {
                    this.v(e);
                    return;
                }
                n2 = cX - 57;
                int n3 = 0;
                while (n3 < 7) {
                    this.a(e, cW, n2 + 12 * n3, l.eV[1 + n3], 0xFFFFFF);
                    ++n3;
                }
                f.b(e, cW - 40, n2 + 86, 80, 13, 0);
                f.a(e, cW - 40, n2 + 86, 80, 13, 0x646464);
                this.a(e, cW, n2 + 52 + 35, bG, 0x41FF41);
                g.a(C, n2 + 64 + 35);
                if (da % 4 < 2) {
                    int n4 = n.a(bG);
                    if (bG.length() == 12) {
                        n4 -= n.a("A") * 2;
                    }
                    g.b(e, cW + n4 / 2, n2 + 62 + 35, cW + n4 / 2 + 4, n2 + 62 + 35, 0xFFFFFF);
                }
                if (bG.length() == 0) {
                    this.c(4, 2);
                    break;
                }
                this.c(4, 3);
                return;
            }
            case 1: {
                n2 = cX - 45;
                int n5 = 0;
                while (n5 < 5) {
                    this.a(e, cW, n2 + 12 * n5, l.eV[8 + n5], 0xFFFFFF);
                    ++n5;
                }
                f.b(e, cW - 40, n2 + 63, 80, 13, 0);
                f.a(e, cW - 40, n2 + 63, 80, 13, 0x646464);
                this.a(e, cW, n2 + 64, j, 0x41FF41);
                if (j.length() >= 4) {
                    this.c(0, 3);
                    return;
                }
                if (j.length() > 0) {
                    this.c(-1, 3);
                    return;
                }
                this.c(-1, 1);
            }
        }
    }

    final void j(int n2) {
        switch (z) {
            case 0: {
                if (x) {
                    if (cs == -3 || cs == -4) {
                        y = (y + 1) % 2;
                        return;
                    }
                    if (cs != -5) break;
                    if (y == 0) {
                        g.i(300);
                        return;
                    }
                    x = false;
                    return;
                }
                i.length();
                boolean bl = false;
                if (n2 == -7) {
                    if (bG.length() == 0) {
                        x = true;
                        return;
                    }
                    bG = bG.substring(0, bG.length() - 1);
                    return;
                }
                if (cs == -5 || cs == -6) {
                    if (bG.length() > 12) break;
                    if (C < 26) {
                        if (bG.length() >= 12) break;
                        bG = bG + (char)(65 + C);
                        return;
                    }
                    if (C != 26 || bG.length() < 4) break;
                    i = bG;
                    z = 1;
                    j = "";
                    return;
                }
                g.p(cs);
                return;
            }
            case 1: {
                int n3 = j.length();
                int n4 = -1;
                switch (n2) {
                    case 48: {
                        n4 = 0;
                        break;
                    }
                    case 49: {
                        n4 = 1;
                        break;
                    }
                    case 50: {
                        n4 = 2;
                        break;
                    }
                    case 51: {
                        n4 = 3;
                        break;
                    }
                    case 52: {
                        n4 = 4;
                        break;
                    }
                    case 53: {
                        n4 = 5;
                        break;
                    }
                    case 54: {
                        n4 = 6;
                        break;
                    }
                    case 55: {
                        n4 = 7;
                        break;
                    }
                    case 56: {
                        n4 = 8;
                        break;
                    }
                    case 57: {
                        n4 = 9;
                    }
                }
                if (n2 == -7) {
                    if (n3 > 0) {
                        j = j.substring(0, n3 - 1);
                        return;
                    }
                    z = 0;
                    C = 0;
                    return;
                }
                if (n4 != -1) {
                    if (n3 >= 12) break;
                    j = j + "" + n4;
                    return;
                }
                if (n2 != -6 || n3 < 4) break;
                cv = 0;
                A = true;
                g.i(10000);
            }
        }
    }

    public final void k(int n2) {
        if (n2 != dV[dW]) {
            g.dU[++g.dW] = 0;
            g.dV[g.dW] = n2;
        }
        g.i(n2);
    }

    public final void l(int n2) {
        if (n2 == 10) {
            dX = true;
        }
        dW = 0;
        g.dU[0] = 0;
        g.dV[0] = n2;
        g.i(n2);
    }

    public final void N() {
        if (dW > 0) {
            g.i(dV[--dW]);
        }
    }

    public final void m(int n2) {
        if (dW >= n2) {
            g.i(dV[dW -= n2]);
        }
    }

    public final void O() {
        dm = null;
        dk = null;
        dn = null;
        dl = null;
        do = null;
        int n2 = 0;
        while (n2 < 6) {
            g.dd[n2] = null;
            ++n2;
        }
        g.di[1] = null;
        g.X();
        this.g();
        g.J();
        g.bR[0] = bh;
        g.bM[0] = cE;
        g.bS[0] = as;
        g.bT[0] = at;
        g.bU[0] = au;
        g.bW[0] = av;
        g.bV[0] = bW[0];
        g.bX[0] = 0;
        g.bY[0] = aw;
        g.bZ[0] = ar;
        g.bN[0] = cF;
        g.bO[0] = cG;
        g.cr[0] = aK;
        g.bQ[0] = true;
        ++bb;
        g.h(0);
        g.co[0] = Math.abs(h.nextInt()) % 4;
        g.cp[0] = 99;
        g.cq[0] = 0;
        bj = false;
        aR = 0;
        D = false;
        this.k(90);
        this.ag();
        O = true;
    }

    public final void h(Graphics graphics) {
        this.c(graphics, cW, cX - 26, 110, 60, 0);
        f.b(graphics, cW - 51, cX - 51 + db * 12, 102, 12, 12956683);
        cL = 0;
        while (cL < bD) {
            if (bX[0] < cI[bE[cL] - 3]) {
                this.a(graphics, cW, cX - 51 + cL * 12, l.eK[bE[cL] - 3], 0x646464);
                if (bE[cL] != 9 && bE[cL] == 10) {
                    // empty if block
                }
            } else {
                this.a(graphics, cW, cX - 51 + cL * 12, l.eK[bE[cL] - 3], 0xFFFFFF);
            }
            ++cL;
        }
    }

    final void P() {
        switch (bz) {
            case 0: 
            case 1: {
                int n2 = cX - 62;
                this.c(e, cW, cX, 102, 124, 0);
                this.a(e, cW, n2 + 5, bM[0], 0xFFFFFF);
                String string = aU == 1 ? l.eX[5] : l.eX[6];
                this.a(e, string, cW, n2 + 19, 1, 16400640);
                this.a(e, l.eX[49], cW - 42, n2 + 35, 0, 0xFFFFFF);
                this.f(e, cW + 36, n2 + 36, at);
                this.a(e, l.eX[50], cW - 42, n2 + 50, 0, 0xFFFFFF);
                this.f(e, cW + 36, n2 + 51, au);
                this.a(e, l.eX[29], cW - 42, n2 + 70, 0, 0xFFFFFF);
                this.b(e, cW + 36, n2 + 71, aV);
                this.a(e, l.eR[0], cW - 42, n2 + 83, 0, 0xFFFFFF);
                this.b(e, cW + 36, n2 + 84, aX);
                this.a(e, l.eX[4], cW - 42, n2 + 96, 0, 0x41FF41);
                this.f(e, cW + 36, n2 + 97, aZ);
                this.r(n2 + 109);
                return;
            }
            case 2: {
                int n3 = cX - 62;
                this.c(e, cW, cX, 102, 124, 0);
                this.a(e, cW, n3 + 3, bM[0], 0xFFFFFF);
                if (aU == 1) {
                    this.a(e, cW, n3 + 15, l.eL[aW], 16400640);
                } else {
                    this.a(e, cW, n3 + 15, l.eX[31], 16400640);
                }
                this.a(e, l.eX[29], cW - 34, n3 + 30, 0, 0xFFFFFF);
                this.b(e, cW + 30, n3 + 31, aV);
                this.a(e, l.eX[32], cW - 34, n3 + 42, 0, 0xFFFFFF);
                this.b(e, cW + 30, n3 + 43, aY);
                this.a(e, l.eR[0], cW - 34, n3 + 54, 0, 0xFFFFFF);
                this.b(e, cW + 30, n3 + 55, aX);
                if (!bI.equals("NONE")) {
                    this.a(e, cW, n3 + 69, bI, 0xFFFFFF);
                    this.a(e, cW, n3 + 81, l.eX[33] + "!!!", 0xFFFFFF);
                }
                this.a(e, l.eX[4], cW - 34, n3 + 96, 0, 0x41FF41);
                this.b(e, cW + 30, n3 + 97, aZ);
                this.r(n3 + 109);
            }
        }
    }

    static void Q() {
        cL = 0;
        while (cL < 4) {
            if (bQ[cL]) {
                switch (cp[cL]) {
                    case 11: 
                    case 12: 
                    case 13: {
                        int n2 = cL;
                        cq[n2] = cq[n2] - 1;
                        if (cq[cL] > 0) break;
                        g.cp[g.cL] = 99;
                    }
                }
            }
            ++cL;
        }
    }

    final void R() {
        cO = 0;
        if (da == 0) {
            cO = -40;
        } else if (da == 1) {
            cO = -20;
        }
        cL = 0;
        while (cL < 4) {
            if (bQ[cL] && bW[cL] > 0 && (cY == 99 || cL == S || cL == T || cL == U)) {
                cP = bz == 0 ? 27 : (bR[cL] / 2 == 0 ? 27 : cR - 27 - 23);
                switch (ca[cL]) {
                    case 0: {
                        cD = bZ[cL];
                        bx = true;
                        break;
                    }
                    case 1: {
                        cD = 4;
                        bx = false;
                        break;
                    }
                    case 2: {
                        cD = 5;
                        bx = false;
                    }
                }
                if (cY == 99) {
                    bJ = cb[cL];
                } else if (cL == S) {
                    bJ = cK[4 + bC];
                } else if (cL == T) {
                    bJ = cK[16 + bC];
                } else if (cL == U) {
                    bJ = cK[36 + bC];
                }
                if (bR[cL] % 2 == 0) {
                    f.a(e, cO, cP, 60, 23, 0);
                    f.a(e, cO + 1, cP + 1, 58, 21, 16769990);
                    switch (bJ) {
                        case 0: 
                        case 3: 
                        case 4: 
                        case 5: 
                        case 6: 
                        case 7: 
                        case 8: {
                            this.a(dg, "act", 0);
                            this.a(dg, "act", 6 + cD);
                            g.c(cO + l.es[0], cP + l.et[0], dg[0]);
                            g.c(cO + l.es[6 + cD], cP + l.et[6 + cD], dg[6 + cD]);
                            break;
                        }
                        default: {
                            this.a(dg, "act", 1);
                            this.a(dg, "act", 12 + cD);
                            g.c(cO + l.es[1], cP + l.et[1], dg[1]);
                            g.c(cO + l.es[12 + cD], cP + l.et[12 + cD], dg[12 + cD]);
                        }
                    }
                    bJ = bJ > 2 ? 3 : bJ;
                    this.a(dg, "act", 2 + bJ);
                    g.a(cO + 60 - 19 + l.es[2 + bJ], 0 + cP + l.et[2 + bJ], dg[2 + bJ]);
                } else {
                    g.a(cQ - cO - 60, cP, 60, 23, 0);
                    g.a(cQ - cO - 60 + 1, cP + 1, 58, 21, 16769990);
                    switch (bJ) {
                        case 0: 
                        case 3: 
                        case 4: 
                        case 5: 
                        case 6: 
                        case 7: 
                        case 8: {
                            this.a(dg, "act", 6 + cD);
                            g.b(cQ - (cO + l.es[0]), cP + l.et[0], dg[0]);
                            g.a(cQ - (cO + l.es[6 + cD]), cP + l.et[6 + cD], dg[6 + cD], bx);
                            break;
                        }
                        default: {
                            this.a(dg, "act", 12 + cD);
                            g.b(cQ - (cO + l.es[1]), cP + l.et[1], dg[1]);
                            g.a(cQ - (cO + l.es[12 + cD]), cP + l.et[12 + cD], dg[12 + cD], bx);
                        }
                    }
                    bJ = bJ > 2 ? 3 : bJ;
                    this.a(dg, "act", 2 + bJ);
                    g.a(cQ - cO - 60 + 10 + l.es[2 + bJ], 0 + cP + l.et[2 + bJ], dg[2 + bJ]);
                }
            }
            ++cL;
        }
    }

    final void i(Graphics graphics) {
        if (aR < 10) {
            f.a(graphics, dh[3], cW - 33, cX - 31, 52, 13, 120, 0);
            this.d(graphics, cW + 21, cX - 31, aR);
            return;
        }
        f.a(graphics, dh[3], cW - 39, cX - 31, 52, 13, 120, 0);
        this.d(graphics, cW + 27, cX - 31, aR);
    }

    static void j(Graphics graphics) {
        cO = cW;
        cP = cX - 40;
        if (bz == 0) {
            cP -= 6;
        }
        f.a(graphics, df[17], cO - 12, cP, 0);
        f.a(graphics, df[16], cO - 36 - 1, cP + 16, 0);
        f.a(graphics, df[15], cO + 12 + 1, cP + 16, 0);
        bs = false;
        if (bD > 0) {
            cN = 0;
            while (cN < bD) {
                if (bX[0] >= cI[bE[cN] - 3]) {
                    bs = true;
                }
                ++cN;
            }
        }
        f.a(graphics, df[18 + (bs ? 0 : 1)], cO - 12, cP + 30, 0);
        if (bB != 99) {
            int n2;
            int n3;
            if (bB == 0) {
                n3 = cO + 12 + 1;
                n2 = cP + 16;
            } else if (bB == 1) {
                n3 = cO - 36 - 1;
                n2 = cP + 16;
            } else if (bB == 2) {
                n3 = cO - 12;
                n2 = cP;
            } else {
                n3 = cO - 12;
                n2 = cP + 30;
            }
            f.a(graphics, n3 - 1, n2 - 1, 24, 24, 15721306);
            f.a(graphics, n3, n2, 23, 23, 15721306);
        }
    }

    public final void d(Graphics graphics, int n2) {
        int n3 = 0;
        if (bz == 0) {
            n3 = 25;
        }
        switch (n2) {
            case 0: {
                if (ba > 5) {
                    this.c(graphics, cW, cX + 28 + n3, 120, 27, 0);
                    this.a(cW, cX + 17 + n3, l.eX[0], 0xFFFFFF);
                    this.a(cW, cX + 28 + n3, l.eX[1], G ? 0x646464 : 0xFFFFFF);
                    return;
                }
                this.c(graphics, cW, cX + 28 + n3, 26, 26, 0);
                this.c(graphics, cW - 4, cX + 22 + n3, ba);
                return;
            }
            case 1: {
                this.c(graphics, cW, cX + 28 + n3, 120, 27, 0);
                this.a(cW, cX + 23 + n3, l.eX[17], 0xFFFFFF);
                return;
            }
            case 2: {
                String string = "";
                if (da % 4 == 1) {
                    string = ".";
                } else if (da % 4 == 2) {
                    string = "..";
                } else if (da % 4 == 3) {
                    string = "...";
                }
                this.c(graphics, cW, cX + 28 + n3, 80, 24, 0);
                this.b(cW - 30, cX + 23 + n3, l.eX[7] + string, 0xFFFFFF);
            }
        }
    }

    public final void S() {
        if (u) {
            if ((v - System.currentTimeMillis()) / 1000L >= 80L) {
                u = false;
                cw = 13;
                x = false;
                g.n();
                g.b(-1);
                this.k(4);
                return;
            }
        } else {
            u = true;
            v = System.currentTimeMillis();
        }
    }

    final void T() {
        int n2 = cX - 57;
        this.k(e);
        g.b(cW - 52 - 7, n2 - 2, 118, 123, 0);
        g.a(cW - 52 - 7, n2 - 2, 118, 123, 0x949694);
        g.b(cW - 52 - 6, n2 - 1, 116, 13, 0x313431);
        bv = 0;
        cL = 0;
        while (cL < be) {
            switch (dU[dW - 1]) {
                case 0: {
                    bv += l.ey[cL];
                    break;
                }
                case 1: {
                    bv += l.eA[cL];
                    break;
                }
                case 2: {
                    bv += l.eC[cL];
                    break;
                }
                case 3: {
                    bv += l.eE[cL];
                    break;
                }
                case 4: {
                    bv += l.eG[cL];
                    break;
                }
                case 5: {
                    bv += l.eI[cL];
                }
            }
            ++cL;
        }
        switch (dU[dW - 1]) {
            case 0: {
                this.a(cW, n2, l.ex[bv], 0xFFFFFF);
                bJ = l.ey[be];
                break;
            }
            case 1: {
                this.a(cW, n2, l.ez[bv], 0xFFFFFF);
                bJ = l.eA[be];
                break;
            }
            case 2: {
                this.a(cW, n2, l.eB[bv], 0xFFFFFF);
                bJ = l.eC[be];
                break;
            }
            case 3: {
                this.a(cW, n2, l.eD[bv], 0xFFFFFF);
                bJ = l.eE[be];
                break;
            }
            case 4: {
                this.a(cW, n2, l.eF[bv], 0xFFFFFF);
                bJ = l.eG[be];
                break;
            }
            case 5: {
                this.a(cW, n2, l.eH[bv], 0xFFFFFF);
                bJ = l.eI[be];
            }
        }
        cL = 1;
        while (cL < bJ) {
            switch (dU[dW - 1]) {
                case 0: {
                    this.b(cW - 56, n2 + cL * 12 + 1, l.ex[bv + cL], 0xFFFFFF);
                    break;
                }
                case 1: {
                    this.b(cW - 56, n2 + cL * 12 + 1, l.ez[bv + cL], 0xFFFFFF);
                    break;
                }
                case 2: {
                    this.b(cW - 56, n2 + cL * 12 + 1, l.eB[bv + cL], 0xFFFFFF);
                    break;
                }
                case 3: {
                    this.b(cW - 56, n2 + cL * 12 + 1, l.eD[bv + cL], 0xFFFFFF);
                    break;
                }
                case 4: {
                    this.a(cW, n2 + cL * 17 + 9, l.eF[bv + cL], 0xFFFFFF);
                    if (cL != 3) break;
                    this.a(cW, n2 + cL * 17 + 9, "v" + a, 0xFFFFFF);
                    break;
                }
                case 5: {
                    this.b(cW - 56, n2 + cL * 12 + 1, l.eH[bv + cL], 0xFFFFFF);
                }
            }
            ++cL;
        }
        if (l.ew[dU[dW - 1]] > 1) {
            this.a(cW, n2 + 72 + 38, be + 1 + "/" + l.ew[dU[dW - 1]], 0xFFFFFF);
            g.c(cW - 35, n2 + 72 + 39, di[1]);
            g.b(cW + 35, n2 + 72 + 39, di[1]);
        }
    }

    public final void U() {
        this.l(g);
        int n2 = 80 / k;
        if (n2 > 30) {
            n2 = 30;
        } else if (n2 < 19) {
            n2 = 19;
        }
        int n3 = 0;
        if (cY == 162 || cY == 163 || cY == 164) {
            n3 = 15;
        } else if (cY == 10) {
            n3 = 40;
        }
        cL = 0;
        while (cL < k) {
            f.a(g, do, (cQ - n2 * (k - 1) - 11) / 2 + n2 * cL, cX + 6 + n3, 12, 15, 12, 0);
            ++cL;
        }
    }

    public final void V() {
        if (bn) {
            this.b(dC[1], "spreff2_r", 1);
        } else {
            this.b(dC[1], "spreff2", 0);
        }
        if (dE[0] == null) {
            g.dE[0] = new a("/spreff3.SP2");
        }
    }

    public static void e(Graphics graphics, int n2) {
        int n3 = n2 * 2 + da % 2;
        if (bn) {
            f.a(graphics, dC[1][1], cQ - (cU - g.dE[0].g[n3] + g.dE[0].e[n3]), cV - g.dE[0].h[n3], g.dE[0].e[n3], g.dE[0].f[n3], g.dE[0].c[n3], g.dE[0].d[n3]);
            return;
        }
        f.a(graphics, dC[1][0], cU - g.dE[0].g[n3], cV - g.dE[0].h[n3], g.dE[0].e[n3], g.dE[0].f[n3], g.dE[0].c[n3], g.dE[0].d[n3]);
    }

    public final void a(Image[] imageArray, String string, int n2) {
        if (imageArray[n2] == null) {
            imageArray[n2] = this.b("/" + string + n2 + ".png");
        }
    }

    public final void b(Image[] imageArray, String string, int n2) {
        if (imageArray[n2] == null) {
            imageArray[n2] = this.b("/" + string + ".png");
        }
    }

    public final void a(Image[] imageArray, a[] aArray, String string) {
        this.a(imageArray, aArray, string, 1);
    }

    public final void a(Image[] imageArray, a[] aArray, String string, int n2) {
        if (bn) {
            if (imageArray[1] == null) {
                imageArray[1] = this.b("/" + string + "_r.png");
            }
        } else if (imageArray[0] == null) {
            imageArray[0] = this.b("/" + string + ".png");
        }
        if (aArray[0] == null) {
            if (n2 == 0) {
                aArray[0] = new a("/" + string + ".SP2");
                return;
            }
            if (n2 == 1) {
                aArray[0] = new a("/" + string + "_basic.SP2");
                aArray[1] = new a("/" + string + "_skill1.SP2");
                aArray[2] = new a("/" + string + "_skill2.SP2");
            }
        }
    }

    public final void W() {
        int n2;
        int n3 = 0;
        f.b(g, 0, 0, cQ, cR, 0);
        n3 = cT / 2 - 95;
        int n4 = cS / 30 + 1;
        int n5 = by >> 6 & 3;
        switch (n5) {
            case 0: {
                this.n(4);
                this.n(5);
                this.n(6);
                this.n(7);
                this.n(8);
                f.b(g, 0, 0, cQ, n3 + 1, 11257599);
                n2 = 0;
                while (n2 < n4) {
                    g.a(g, 30 * n2, n3, dj[4]);
                    g.a(g, 30 * n2, n3 + 30, dj[5]);
                    ++n2;
                }
                g.a(g, cS - dj[6].getWidth(), n3 - 2 - dj[6].getHeight(), dj[6]);
                g.a(g, 18, n3 - 30, dj[7]);
                g.a(g, 52, n3 - 15, dj[8]);
                break;
            }
            case 1: {
                this.n(9);
                this.n(10);
                this.n(11);
                this.n(12);
                this.n(13);
                f.b(g, 0, 0, cQ, n3 + 1, 1645890);
                n2 = 0;
                while (n2 < n4) {
                    g.a(g, 30 * n2, n3, dj[9]);
                    g.a(g, 30 * n2, n3 + 30, dj[10]);
                    ++n2;
                }
                g.a(g, cS - dj[6].getWidth(), n3 - 2 - dj[6].getHeight(), dj[11]);
                g.a(g, 18, n3 - 30, dj[12]);
                g.a(g, 52, n3 - 15, dj[13]);
            }
        }
        int n6 = by >> 4 & 3;
        this.n(14 + n6);
        n2 = 0;
        while (n2 < n4) {
            g.a(g, 30 * n2, n3 + 83, dj[14 + n6]);
            ++n2;
        }
        int n7 = by & 3;
        int n8 = 0;
        int[] nArray = new int[]{3, 8, -8, 16};
        this.n(0 + n7);
        n8 = n3 + nArray[n7];
        g.a(g, 0, n8, dj[0 + n7]);
        n2 = 0;
        while (n2 < dj.length) {
            g.dj[n2] = null;
            ++n2;
        }
        g.X();
    }

    public static void X() {
        System.gc();
    }

    public final void n(int n2) {
        if (dj[n2] == null) {
            g.dj[n2] = this.b("/gamebg" + n2 + ".png");
        }
    }

    public final void Y() {
        f.b(g, 0, 0, cQ, 12, 0);
        g.o(0);
        int n2 = 0;
        f.a(g, 28, 4, bK - 1, 8429760);
        f.a(g, 28, 10, bK - 1, 8429760);
        f.a(g, 31, 4, bK - 1 - 6, 0x808080);
        f.a(g, 31, 10, bK - 1 - 6, 0x808080);
        n2 = 28 + bK;
        f.b(g, n2, 0, 10, 0x808080);
        f.b(g, n2, 3, 1, 8429760);
        f.b(g, n2, 4, 1, 0);
        f.b(g, n2, 5, 1, 8429760);
        f.b(g, n2, 9, 1, 8429760);
        g.o(1);
        n2 = cQ - 28 - bK + 1;
        f.a(g, n2, 4, bK - 1, 8429760);
        f.a(g, n2, 10, bK - 1, 8429760);
        f.a(g, n2 + 3, 4, bK - 1 - 6, 0x808080);
        f.a(g, n2 + 3, 10, bK - 1 - 6, 0x808080);
        n2 = cQ - 28 - 1 - bK;
        f.b(g, n2, 0, 10, 0x808080);
        f.b(g, n2, 3, 1, 8429760);
        f.b(g, n2, 4, 1, 0);
        f.b(g, n2, 5, 1, 8429760);
        f.b(g, n2, 9, 1, 8429760);
        if (bz != 0) {
            f.b(g, 0, cR - 12, cQ, 12, 0);
            g.o(2);
            f.a(g, 28, cR - 5, bK - 1, 8429760);
            f.a(g, 28, cR - 11, bK - 1, 8429760);
            f.a(g, 31, cR - 5, bK - 6, 0x808080);
            f.a(g, 31, cR - 11, bK - 6, 0x808080);
            n2 = 28 + bK + 1;
            f.b(g, n2 - 1, cR - 9, 9, 0x808080);
            f.b(g, n2 - 1, cR - 4, 1, 8429760);
            f.b(g, n2 - 1, cR - 5, 1, 0);
            f.b(g, n2 - 1, cR - 6, 1, 8429760);
            f.b(g, n2 - 1, cR - 10, 1, 8429760);
            g.o(3);
            n2 = cQ - 28 - bK + 1;
            f.a(g, n2, cR - 5, bK - 1, 8429760);
            f.a(g, n2, cR - 11, bK - 1, 8429760);
            f.a(g, n2 + 3, cR - 5, bK - 1 - 6, 0x808080);
            f.a(g, n2 + 3, cR - 11, bK - 1 - 6, 0x808080);
            n2 = cQ - 28 - 1 - bK;
            f.b(g, n2, cR - 9, 10, 0x808080);
            f.b(g, n2, cR - 4, 1, 8429760);
            f.b(g, n2, cR - 5, 1, 0);
            f.b(g, n2, cR - 6, 1, 8429760);
            f.b(g, n2, cR - 10, 1, 8429760);
        }
    }

    public static void o(int n2) {
        int n3 = n2 % 2 == 0 ? 28 : cQ - 28 - 1 - bK + 2;
        int n4 = n2 / 2 == 0 ? 0 : cR - 3 - 6;
        int n5 = 0;
        while (n5 < 2) {
            if (n5 == 1) {
                n4 += 6;
            }
            f.a(g, n3, n4, bK - 1, 0x808080);
            f.a(g, n3, n4 + 1, bK - 1, 0xFFFFFF);
            f.a(g, n3, n4 + 2, bK - 1, 0xC0C0C0);
            ++n5;
        }
    }

    final void k(Graphics graphics) {
        this.l(graphics);
    }

    public final void l(Graphics graphics) {
        int n2;
        int n3;
        int n4;
        g.n(graphics);
        if (cR <= 144) {
            n4 = 78 - (144 - cR) / 2;
            n3 = cR - 18 - n4;
            f.a(graphics, dk, 0, 5, 5, 8, 0, 0);
            f.a(graphics, dk, 0, 13, 5, n4, 0, 8 + (78 - n4));
            f.a(graphics, dk, 0, 13 + n4, 5, n3, 0, 134 - n3);
            n2 = cQ - 5;
            f.a(graphics, dk, n2, 5, 5, 8, 5, 0);
            f.a(graphics, dk, n2, 13, 5, n4, 5, 8 + (78 - n4));
            f.a(graphics, dk, n2, 13 + n4, 5, n3, 5, 134 - n3);
        } else {
            n4 = (cR - 144) / 2;
            n3 = cR - 144 - n4;
            f.a(graphics, dk, 0, 5, 5, 59, 0, 0);
            g.d(graphics, 0, 64, n4, 0);
            f.a(graphics, dk, 0, 64 + n4, 5, 17, 0, 59);
            g.d(graphics, 0, 64 + n4 + 17, n3, 0);
            f.a(graphics, dk, 0, cR - 5 - 58, 5, 58, 0, 76);
            n2 = cQ - 5;
            f.a(graphics, dk, n2, 5, 5, 59, 5, 0);
            g.d(graphics, n2, 64, n4, 5);
            f.a(graphics, dk, n2, 64 + n4, 5, 17, 5, 59);
            g.d(graphics, n2, 64 + n4 + 17, n4, 5);
            f.a(graphics, dk, n2, cR - 5 - 58, 5, 58, 5, 76);
        }
        n4 = (cQ - 120) / 2;
        n3 = cQ - 120 - n4;
        f.a(graphics, dm, 0, 0, 21, 5, 0, 0);
        g.e(graphics, 21, 0, n4, 0);
        f.a(graphics, dm, 21 + n4, 0, 77, 5, 21, 0);
        g.e(graphics, 98 + n4, 0, n3, 0);
        f.a(graphics, dm, cQ - 21, 0, 21, 5, 98, 0);
        n2 = cR - 5;
        f.a(graphics, dm, 0, n2, 37, 5, 0, 5);
        g.e(graphics, 37, n2, n4, 5);
        f.a(graphics, dm, 37 + n4, n2, 45, 5, 37, 5);
        g.e(graphics, 82 + n4, n2, n3, 5);
        f.a(graphics, dm, cQ - 37, n2, 37, 5, 82, 5);
        f.a(graphics, dn, cW - 46, 0, 46, 15, 0, 0);
        f.a(graphics, dn, cW, 0, 46, 15, 17, 0);
        this.a(graphics, c, cQ / 2, 2, 1, 0xFFFFFF);
    }

    public final void a(Graphics graphics, String string, int n2, int n3, int n4, int n5, boolean bl, boolean bl2) {
        if (bl) {
            f.a(graphics, n2 - 1, n3 - 1, n4 + 2, n5 + 2, 1, 0xFFFFFF);
            f.a(graphics, n2, n3, n4, n5, 0xFFFFFF);
        }
        g.c(graphics, n2, n3, n4, n5);
        if (!bl2) {
            this.a(n2 + n4 / 2, n3 + (n5 - 11) / 2, string, 0x646464);
            return;
        }
        this.a(n2 + n4 / 2, n3 + (n5 - 11) / 2, string, 0xFFFFFF);
    }

    static void c(Graphics graphics, int n2, int n3, int n4, int n5) {
        f.a(graphics, n2, n3, n4, n5, 1, 0x949694);
        f.b(graphics, n2 + 1, n3 + 1, n4 - 2, n5 - 2, 0);
    }

    public final void m(Graphics graphics) {
        cL = 0;
        while (cL < 4) {
            if (bQ[cL]) {
                if (bR[cL] % 2 == 0) {
                    if (ca[cL] == 0) {
                        this.a(de, "face", (int)bZ[cL]);
                        g.c(graphics, 0, bR[cL] / 2 == 0 ? 0 : cR - 12, de[bZ[cL]]);
                        g.de[g.bZ[g.cL]] = null;
                    }
                    this.c(graphics, 0, bR[cL] / 2 == 0 ? 12 : cR - 12 - 15, 60, 15, 1);
                    if (bP[cL].length() == 0 || aR % 2 == 0) {
                        this.a(graphics, 30, bR[cL] / 2 == 0 ? 14 : cR - 12 - 15 + 2, bM[cL], 0xFFFFFF);
                    } else {
                        this.a(graphics, 30, bR[cL] / 2 == 0 ? 14 : cR - 12 - 15 + 2, bP[cL], 0xFFFFFF);
                    }
                } else {
                    if (ca[cL] == 0) {
                        this.a(de, "face", (int)bZ[cL]);
                        g.b(graphics, cQ, bR[cL] / 2 == 0 ? 0 : cR - 12, de[bZ[cL]]);
                        g.de[g.bZ[g.cL]] = null;
                    }
                    this.c(graphics, cQ - 60, bR[cL] / 2 == 0 ? 12 : cR - 12 - 15, 60, 15, 1);
                    if (bP[cL].length() == 0 || aR % 2 == 0) {
                        this.a(graphics, cQ - 30, bR[cL] / 2 == 0 ? 14 : cR - 12 - 15 + 2, bM[cL], 0xFFFFFF);
                    } else {
                        this.a(graphics, cQ - 30, bR[cL] / 2 == 0 ? 14 : cR - 12 - 15 + 2, bP[cL], 0xFFFFFF);
                    }
                }
            }
            ++cL;
        }
        g.X();
    }

    private static void d(Graphics graphics, int n2, int n3, int n4, int n5) {
        int n6 = n4 / 11 + 1;
        int n7 = 0;
        while (n7 < n6) {
            f.a(graphics, dk, n2, n3 + 11 * n7, 5, 11, n5, 8);
            ++n7;
        }
    }

    static void n(Graphics graphics) {
        int n2 = cQ / dl.getWidth() + 1;
        int n3 = cR / dl.getHeight() + 1;
        int n4 = 0;
        while (n4 < n2) {
            int n5 = 0;
            while (n5 < n3) {
                if (n5 % 2 != 0) {
                    f.a(graphics, dl, dl.getWidth() * n4, dl.getHeight() * n5, 0);
                } else {
                    f.a(graphics, dl, dl.getWidth() * n4, dl.getHeight() * n5, 21, 24, 31, 0);
                    f.a(graphics, dl, dl.getWidth() * n4 + 21, dl.getHeight() * n5, 31, 24, 0, 0);
                }
                ++n5;
            }
            ++n4;
        }
    }

    private static void e(Graphics graphics, int n2, int n3, int n4, int n5) {
        int n6 = n4 / 11 + 1;
        int n7 = 0;
        while (n7 < n6) {
            f.a(graphics, dm, n2 + 11 * n7, n3, 11, 5, 10, n5);
            ++n7;
        }
    }

    final void o(Graphics graphics) {
        this.k(graphics);
        cL = 0;
        while (cL < 3) {
            this.c(graphics, cW - 58, cX - 16 + cL * 19, 61, 14, 2);
            this.a(graphics, l.eW[cL], cW - 28, cX - 15 + cL * 19, 1, 0x646464);
            this.c(graphics, cW + 13, cX - 16 + cL * 19, 39, 14, 2);
            ++cL;
        }
    }

    final void Z() {
        this.k(e);
        cL = 0;
        while (cL < 6) {
            this.c(e, cW - 60, cX - 47 + cL * 17, 81, 14, 2);
            this.c(e, cW + 23, cX - 47 + cL * 17, 37, 14, 2);
            this.a(e, l.eX[46 + cL], cW - 19, cX - 45 + cL * 17, 1, 0xFFFFFF);
            switch (cL) {
                case 0: {
                    this.c(cW + 52, cX - 44 + cL * 17, as);
                    break;
                }
                case 1: {
                    this.e(cW + 52, cX - 44 + cL * 17, ax);
                    break;
                }
                case 2: {
                    cu = aA;
                    break;
                }
                case 3: {
                    cu = at;
                    break;
                }
                case 4: {
                    cu = au;
                    break;
                }
                case 5: {
                    cu = aB;
                }
            }
            if (cL > 1) {
                this.d(cW + 52, cX - 44 + cL * 17, cu);
            }
            ++cL;
        }
    }

    final void aa() {
        this.k(e);
        int n2 = 0;
        cL = 0;
        while (cL < 4) {
            this.c(e, cW - 54, cX - 30 + cL * 17, 39, 14, 2);
            this.c(e, cW - 13, cX - 30 + cL * 17, 67, 14, 2);
            this.a(e, l.eX[42 + cL], cW - 35, cX - 28 + cL * 17, 1, 0xFFFFFF);
            switch (cL) {
                case 0: {
                    cu = aC;
                    n2 = aD;
                    break;
                }
                case 1: {
                    cu = aE;
                    n2 = aF;
                    break;
                }
                case 2: {
                    cu = aG;
                    n2 = aH;
                    break;
                }
                case 3: {
                    cu = aI;
                    n2 = aJ;
                }
            }
            this.b(cW + 9, cX - 27 + cL * 17, cu);
            this.a(cW + 52, cX - 27 + cL * 17, n2);
            ++cL;
        }
    }

    final void p(Graphics graphics) {
        this.k(graphics);
        cL = 0;
        while (cL < 5) {
            this.c(graphics, cW - 58, cX - 51 + cL * 16, 91, 14, 2);
            this.c(graphics, cW + 43, cX - 51 + cL * 16, 15, 14, 2);
            ++cL;
        }
        this.a(graphics, cW - 13, cX - 49, "NAME", 0xFFFFFF);
        this.a(graphics, cW + 51, cX - 49, "LV", 0xFFFFFF);
        g.a(graphics, cW - 52, cX + 31, 104, 27, 0);
        g.b(graphics, cW - 52, cX + 30, cW + 51, cX + 30, 0x804000);
        g.b(graphics, cW - 52, cX + 58, cW + 51, cX + 58, 0x804000);
        g.b(graphics, cW - 53, cX + 31, cW - 53, cX + 57, 0x804000);
        g.b(graphics, cW + 52, cX + 31, cW + 52, cX + 57, 0x804000);
    }

    final void ab() {
        cL = 0;
        while (cL < 4) {
            if (dU[dW] == cL) {
                if (da % 4 < 2) {
                    g.c(cW - 65, cX - 32 + cL * 16, di[1]);
                    g.b(cW + 40, cX - 32 + cL * 16, di[1]);
                }
                this.c(e, cW - 58, cX - 35 + cL * 16, 91, 14, 3);
                this.c(e, cW + 43, cX - 35 + cL * 16, 15, 14, 3);
            }
            if (cH[cB[cL] - 3] == 99) {
                this.a(e, cW - 12, cX - 33 + cL * 16, l.eK[cB[cL] - 3], 0x646464);
                if (dU[dW] == cL) {
                    this.b(cW - 50, cX + 32, l.eX[34], 0x646464);
                }
            } else {
                this.a(e, cW - 12, cX - 33 + cL * 16, l.eK[cB[cL] - 3], 0xFFFFFF);
                this.c(cW + 48, cX - 32 + cL * 16, cH[cB[cL] - 3]);
                if (dU[dW] == cL) {
                    this.b(cW - 50, cX + 32, l.eJ[(cB[cL] - 3) * 2], 0xFFFFFF);
                    this.b(cW - 50, cX + 45, l.eJ[(cB[cL] - 3) * 2 + 1], 0xFFFFFF);
                }
            }
            ++cL;
        }
    }

    final void ac() {
        this.k(e);
        cL = 0;
        while (cL < 3) {
            this.c(e, cW - 50, cX - 45 + cL * 34, 100, 14, 2);
            this.c(e, cW - 50, cX - 32 + cL * 34, 100, 14, 2);
            this.a(e, l.eX[52 + cL], cW, cX - 43 + cL * 34, 1, 0xFFFFFF);
            switch (cL) {
                case 0: {
                    cu = ay;
                    break;
                }
                case 1: {
                    cu = ax;
                    break;
                }
                case 2: {
                    cu = az;
                }
            }
            this.d(cW + 24, cX - 29 + cL * 34, cu);
            ++cL;
        }
    }

    final void q(Graphics graphics) {
        this.k(graphics);
        this.c(graphics, cW - 62, cX + 7, 126, 16, 6);
    }

    final void r(Graphics graphics) {
        String string = bG;
        this.a(cW, cX - 44, l.eX[58] + "." + (B + 1), 16400640);
        if (B == 0) {
            this.a(cW, cX - 32, l.eX[23], 0xFFFFFF);
            this.a(cW, cX - 20, l.eX[24], 0xFFFFFF);
        } else {
            this.a(cW, cX - 32, l.eX[15], 0xFFFFFF);
            this.a(cW, cX - 20, l.eX[16], 0xFFFFFF);
        }
        this.a(cW, cX - 8, l.eX[25], 0xFFFFFF);
        this.a(graphics, cW, cX + 9, string, 0x41FF41);
        if (da % 4 < 2) {
            int n2 = n.a(string);
            if (string.length() == 20) {
                n2 -= n.a("A") * 2;
            }
            g.b(graphics, cW + n2 / 2, cX + 20, cW + n2 / 2 + 4, cX + 20, 0xFFFFFF);
        }
        g.b(C, cX + 27);
    }

    public static void a(int n2, int n3) {
        int n4 = cW - 57;
        String[] stringArray = new String[]{"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "OK"};
        i.a(n4, n3, 115, 22, 0);
        i.a(n4 + 99, n3 + 12, 13, 9, 255);
        if (da % 4 < 2) {
            if (n2 == 26) {
                i.a(n4 + 99, n3 + 12, 13, 9, 0xFF0000);
            } else {
                i.a(n4 + 2 + n2 % 14 * 8, n3 + 1 + 11 * (n2 / 14), 7, 9, 0xFF0000);
            }
        }
        i.a(n);
        int n5 = 0;
        while (n5 < stringArray.length) {
            int n6 = n5 == 8 ? 1 : (n5 == 26 ? 1 : 0);
            i.a(stringArray[n5], n4 + 3 + n5 % 14 * 8 + n6, n3 + 11 * (n5 / 14), 0);
            ++n5;
        }
    }

    public static int p(int n2) {
        int n3 = n2;
        if (n2 != -7 && n2 != -5 && n2 != -6) {
            if (n2 == -1) {
                C = (C + 28 - 14) % 28;
            } else if (n2 == -2) {
                C = (C + 28 + 14) % 28;
            } else if (n2 == -3) {
                C = (C + 28 - 1) % 28;
            } else if (n2 == -4 && (C = (C + 28 + 1) % 28) == 27) {
                C = 0;
            }
        }
        if (C == 27) {
            C = 26;
        }
        return n3;
    }

    public static void b(int n2, int n3) {
        int n4 = cW - 60;
        String[] stringArray = new String[]{"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " ", "OK"};
        i.a(n4, n3, 120, 22, 0);
        i.a(n4 + 99, n3 + 13, 5, 7, 0x666666);
        i.a(n4 + 106, n3 + 12, 13, 9, 255);
        if (da % 4 < 2) {
            if (n2 == 27) {
                i.a(n4 + 106, n3 + 12, 13, 9, 0xFF0000);
            } else {
                i.a(n4 + 2 + n2 % 14 * 8, n3 + 1 + 11 * (n2 / 14), 7, 9, 0xFF0000);
            }
        }
        i.a(n);
        int n5 = 0;
        while (n5 < stringArray.length) {
            int n6 = n5 == 8 ? 1 : (n5 == 26 ? 1 : 0);
            i.a(stringArray[n5], n4 + 3 + n5 % 14 * 8 + n6, n3 + 11 * (n5 / 14), 0);
            ++n5;
        }
    }

    public static int q(int n2) {
        int n3 = n2;
        if (n2 != -7 && n2 != -5 && n2 != -6) {
            if (n2 == -1) {
                C = (C + 28 - 14) % 28;
            } else if (n2 == -2) {
                C = (C + 28 + 14) % 28;
            } else if (n2 == -3) {
                C = (C + 28 - 1) % 28;
            } else if (n2 == -4) {
                C = (C + 28 + 1) % 28;
            }
        }
        return n3;
    }

    static String d(String string) {
        int n2 = string.length();
        int n3 = n2 - 1;
        while (n3 >= 0) {
            if (string.charAt(n3) != ' ') break;
            --n3;
        }
        if (n3 == 0) {
            return "";
        }
        return string.substring(0, n3 + 1);
    }

    final void s(Graphics graphics) {
        this.k(graphics);
        this.c(graphics, cW - 62, cX + 7, 126, 16, 6);
        this.a(graphics, cW, cX - 32, l.eU[0], 0xFFFFFF);
        this.a(graphics, cW, cX - 20, l.eU[1], 0xFFFFFF);
        this.a(graphics, cW, cX - 8, l.eU[2], 0xFFFFFF);
    }

    final void t(Graphics graphics) {
        this.a(graphics, cW, cX + 9, bG, 0x41FF41);
        if (da % 4 < 2) {
            int n2 = n.a(bG);
            if (bG.length() == 8) {
                n2 -= n.a("A") * 2;
            }
            g.b(graphics, cW + n2 / 2, cX + 20, cW + n2 / 2 + 4, cX + 20, 0xFFFFFF);
        }
        g.a(C, cX + 27);
    }

    final void u(Graphics graphics) {
        this.c(graphics, cW - 60, cX - 35 - 5, 120, 94, 5);
        this.a(graphics, cW, cX - 32, l.eU[3], 0xFFFFFF);
        this.a(graphics, cW, cX - 20, l.eU[4], 0xFFFFFF);
        this.a(graphics, cW, cX - 8, l.eU[5], 0xFFFFFF);
        this.a(graphics, cW, cX + 8, bG, 0x41FF41);
        cL = 0;
        while (cL < 2) {
            this.c(graphics, cW - 42 + cL * 55, cX + 35, 29, 14, 2);
            this.a(graphics, l.eX[40 + cL], cW - 28 + cL * 55, cX + 38, 1, 0x646464);
            if (dU[dW] == cL) {
                this.a(graphics, l.eX[40 + cL], cW - 28 + cL * 55, cX + 38, 1, 0xFFFFFF);
                this.c(graphics, cW - 42 + cL * 55, cX + 35, 29, 14, 3);
            }
            ++cL;
        }
    }

    final void v(Graphics graphics) {
        this.c(graphics, cW - 53, cX - 34, 106, 68, 5);
        this.a(graphics, cW, cX - 22, l.eX[56], 0xFFFFFF);
        this.a(graphics, cW, cX - 7, l.eX[57], 0xFFFFFF);
        int n2 = 0;
        while (n2 < 2) {
            this.c(graphics, cW - 42 + n2 * 55, cX + 15, 29, 14, y == n2 ? 3 : 2);
            this.a(graphics, l.eX[40 + n2], cW - 27 + n2 * 55, cX + 17, 1, y == n2 ? 0xFFFFFF : 0x646464);
            ++n2;
        }
    }

    final void ad() {
        bu = 0;
        cL = 0;
        while (cL < cw) {
            bu += l.eZ[cL];
            ++cL;
        }
        bJ = 0;
        cL = 0;
        while (cL < l.eZ[cw]) {
            bw = true;
            if (bw) {
                g.ed[g.cL] = l.eY[bu + cL];
            }
            if (bJ < ed[cL].length()) {
                bJ = ed[cL].length();
            }
            ++cL;
        }
        cM = 0;
        this.c(e, cW, cX, bJ * 7, (l.eZ[cw] + 1) * 15 + cM + 4, 0);
        cL = 0;
        while (cL < l.eZ[cw]) {
            this.a(e, cW, cX - l.eZ[cw] * 15 / 2 + cL * 15 - 4 - cM / 3, ed[cL], 0xFFFFFF);
            ++cL;
        }
        this.r(cX + l.eZ[cw] * 15 / 2 - 5);
    }

    final void w(Graphics graphics) {
        this.k(graphics);
        cL = 0;
        while (cL < 2) {
            this.c(graphics, cW - 56, cX - 16 + cL * 20, 111, 14, 2);
            this.a(graphics, l.eX[38 + cL], cS / 2, cX - 15 + cL * 20, 1, 0x646464);
            ++cL;
        }
    }

    final void f(Graphics graphics, int n2) {
        this.k(graphics);
        int n3 = 0;
        while (n3 < 5) {
            this.a(graphics, cW, n2 + 12 * n3, l.eU[(bz == 0 ? 6 : 12) + n3], 0xFFFFFF);
            ++n3;
        }
        this.c(graphics, cW - 40, n2 + 59, 80, 15, 6);
    }

    final void ae() {
        String string = "";
        if (da % 4 == 1) {
            string = ".";
        } else if (da % 4 == 2) {
            string = "..";
        } else if (da % 4 == 3) {
            string = "...";
        }
        int n2 = n.a(l.fa[cv]) + 14;
        this.c(e, cW, cX, n2 + 22, 30, 0);
        this.b(e, cW - n2 / 2, cX - 7 + 2, l.fa[cv] + string, 0xFFFFFF);
    }

    final void af() {
        String string = "";
        if (da % 4 == 1) {
            string = ".";
        } else if (da % 4 == 2) {
            string = "..";
        } else if (da % 4 == 3) {
            string = "...";
        }
        int n2 = n.a(l.eX[7]) + 14;
        this.c(e, cW, cX, n2 + 22, 30, 0);
        this.b(e, cW - n2 / 2, cX - 6, l.eX[7] + string, 0xFFFFFF);
    }

    final void c(int n2, int n3) {
        if (n2 != -1) {
            g.a(e, 0, cT - 11, dt);
            this.a(e, 28, cT - 11, l.eT[n2], 0xFFFFFF);
        }
        if (n3 != -1) {
            g.a(e, cS - 57, cT - 11, dt);
            this.a(e, cS - 28, cT - 11, l.eT[n3], 0xFFFFFF);
        }
    }

    final void r(int n2) {
        this.c(e, cW - 10, n2 + 1, 18, 9, 3);
        this.a(e, cW, n2, l.eT[0], 0xFFFFFF);
    }

    final void s(int n2) {
        g.u(n2);
    }

    final void t(int n2) {
        g.u(n2);
    }

    static void u(int n2) {
        if (b != null) {
            m.v(n2);
        }
    }

    void ag() {
        if (b != null) {
            b.ag();
        }
    }

    static int ah() {
        return am;
    }

    final void ai() {
        am = (am + 6 - 1) % 6;
        this.ag();
        if (am != 0) {
            this.t(3);
        }
    }

    final void aj() {
        am = (am + 1) % 6;
        this.ag();
        if (am != 0) {
            this.t(3);
        }
    }

    static {
        c = "";
        d = 0;
        e = null;
        h = new Random();
        k = 7;
        m = -999;
        n = null;
        o = null;
        p = null;
        q = null;
        u = false;
        w = false;
        x = false;
        D = false;
        H = 0;
        I = -1;
        J = false;
        K = false;
        L = false;
        O = true;
        P = true;
        Y = new String[3];
        Z = new int[3];
        aa = new int[3];
        ac = new int[]{0, 0, 0, 0};
        am = 4;
        an = 1;
        ao = 1;
        bx = true;
        bE = new byte[4];
        bF = new String[4];
        bM = new String[4];
        bN = new String[4];
        bO = new String[4];
        bP = new String[4];
        bQ = new boolean[4];
        bR = new int[4];
        bS = new int[4];
        bT = new int[4];
        bU = new int[4];
        bV = new int[4];
        bW = new int[4];
        bX = new int[4];
        bY = new int[4];
        bZ = new byte[4];
        ca = new int[4];
        cb = new int[4];
        cc = new int[4];
        cd = new int[4];
        ce = new int[4];
        cf = new int[4];
        cg = new int[4];
        ch = new int[4];
        ci = new int[4];
        cj = new int[4];
        ck = new int[4];
        cl = new int[4];
        cm = new int[4];
        cn = new int[4];
        co = new int[4];
        cp = new int[4];
        cq = new int[4];
        cr = new int[4];
        cB = new byte[4];
        cH = new int[11];
        cI = new int[11];
        cJ = new int[12];
        cK = new byte[44];
        dc = 100;
        dd = new Image[6];
        de = new Image[4];
        df = new Image[57];
        dg = new Image[18];
        dh = new Image[8];
        di = new Image[2];
        dj = new Image[22];
        du = new Image[2];
        dv = new a[3];
        dw = new Image[10][2];
        dx = new a[10][3];
        dy = new Image[2][2];
        dz = new a[2][3];
        dA = new Image[2][2];
        dB = new a[2][3];
        dC = new Image[2][2];
        dD = new a[2][3];
        dE = new a[1];
        dF = new Image[2];
        dG = new a[3];
        dH = new Image[2];
        dI = new a[1];
        dJ = new Image[2];
        dK = new a[1];
        dL = new Image[2];
        dM = new a[1];
        dN = new Image[2];
        dO = new a[1];
        dU = new int[10];
        dV = new int[10];
        dW = 0;
        dX = false;
        dY = true;
        dZ = 0;
        ea = false;
        eb = false;
        ec = -1;
        ed = new String[10];
    }
}

