import javax.microedition.lcdui.Image;

public final class l extends ag {
  public short a;
  
  public short b;
  
  public short b_;
  
  public short d;
  
  public short e;
  
  public short f;
  
  public short g;
  
  public short h;
  
  public short i;
  
  public short j;
  
  public short k;
  
  String[] l = new String[10];
  
  public String m;
  
  public String n;
  
  public String o;
  
  public String p;
  
  public boolean q;
  
  public static Image r = null;
  
  boolean s;
  
  public l() {
    super(ag.bs);
  }
  
  public final void a() {
    this.b = 0;
    this.b_ = 0;
    this.d = 0;
    this.e = 0;
    this.f = 0;
    this.g = 0;
    this.h = 0;
    this.i = 0;
    this.j = 0;
    this.k = 0;
    this.q = false;
    for (byte b = 0; b < this.l.length; b++)
      this.l[b] = ""; 
  }
  
  public final int b() {
    if (ag.ch != 0) {
      this.j = 1;
      if (this.e != 0) {
        if ((ag.ch == -5 || ag.ch == 53) && this.f > 2)
          this.f = 2; 
      } else {
        switch (this.b) {
          case 1:
            if (ag.ch == -5 || ag.ch == 53) {
              if (this.a == 1) {
                if (this.d > 2 && this.b_ != 20)
                  this.d = 2; 
                return -1;
              } 
              if (ag.bV != 1) {
                if (this.d > 2 && this.b_ != 20)
                  this.d = 2; 
                break;
              } 
              if (this.b_ == 37)
                as(); 
            } 
            break;
          case 2:
            switch (ag.ch) {
              case -4:
              case -3:
              case 52:
              case 54:
                this.k = (short)(this.k + 1 & 0x1);
                break;
              case -5:
              case 53:
                this.d = 1;
                if (this.k == 0) {
                  if (this.a == 1) {
                    this.b = 0;
                    this.q = true;
                    return -1;
                  } 
                  if (this.b_ == 28) {
                    as();
                    return -1;
                  } 
                  if (ag.bV == 2) {
                    switch (ag.cM[0]) {
                      case 3:
                        ag.cM[0] = 4;
                        ag.dG = 0;
                        ag.dH = (short)(ag.dH + 1);
                        am();
                        break;
                      case 5:
                        if (this.b_ == 28) {
                          as();
                          return -1;
                        } 
                        if (this.b_ == 41) {
                          try {
                            ag.bs.platformRequest(ag.bm);
                          } catch (Exception exception) {}
                          ag.bs.destroyApp(true);
                          ag.bs.notifyDestroyed();
                          return -1;
                        } 
                        if (this.b_ == 42) {
                          try {
                            ag.bs.platformRequest(ag.bn);
                          } catch (Exception exception) {}
                          ag.bs.destroyApp(true);
                          ag.bs.notifyDestroyed();
                          return -1;
                        } 
                        if (ag.cM[1] == 1)
                          au(); 
                        break;
                      case 8:
                        ag.ax();
                        ay();
                        ag.eo = ag.B();
                        if (ag.be != null)
                          as.d = true; 
                        if (ar() != 0) {
                          ag.bb.c();
                          ag.dE = ag.fU;
                          ag.cM[0] = 0;
                          ag.cN = ae.v[ag.cM[0]];
                          ag.cM[2] = 0;
                          ag.cM[1] = 0;
                          aA();
                          l(100, 0);
                          break;
                        } 
                        ag.aw();
                        e(1);
                        break;
                      case 10:
                        ag.aj();
                        ag.cM[0] = 5;
                        ag.cN = 10;
                        ag.cM[2] = 0;
                        ag.cM[1] = 0;
                        break;
                      case 29:
                        ag.bb.c();
                        ag.cM[0] = 6;
                        break;
                    } 
                    break;
                  } 
                  if (ag.cR.a == 1) {
                    if (ag.cM[1] == 5) {
                      al();
                      w(2);
                      ag.cM[0] = 5;
                      ag.cN = 10;
                      ag.bV = 2;
                      ag.cL = 0;
                      ag.cK = 0;
                    } 
                    break;
                  } 
                  if (ag.bV == 0)
                    return 0; 
                  break;
                } 
                if (this.a == 1) {
                  this.b = 0;
                  return -1;
                } 
                if (ag.cM[0] == 8)
                  ag.aw(); 
                return 1;
              case -7:
                if (ag.cM[0] == 8) {
                  this.d = 1;
                  ag.aw();
                  return 1;
                } 
                break;
            } 
            break;
          case 3:
            if (this.d > 5)
              switch (ag.ch) {
                case -1:
                case 50:
                  this.k = (short)(this.k - 1);
                  this.k = (short)(this.k & 0x3);
                  break;
                case -2:
                case 56:
                  this.k = (short)(this.k + 1);
                  this.k = (short)(this.k & 0x3);
                  break;
                case -5:
                case 53:
                  this.d = 4;
                  break;
              }  
            break;
          case 10:
            if (ag.ch == -5 || ag.ch == 53) {
              this.d = 2;
              ag.cS.b = 0;
              this.q = true;
              ag.ck = 1;
            } 
            break;
        } 
      } 
    } 
    if (this.e != 0) {
      this.f = (short)(this.f - 1);
      if (this.f < 1) {
        this.e = 0;
        ag.ck = 1;
      } 
    } else {
      if (this.d < 200)
        this.d = (short)(this.d - 1); 
      if (this.d == 0) {
        byte b;
        this.b = 0;
        ag.ck = 1;
        switch (this.b_) {
          case 9:
            if ((ag.eO[ag.eP]).o != 0) {
              ag.bd.g();
              break;
            } 
            ag.co = 1;
            ag.cn = 5;
            break;
          case 10:
            e(11);
            c.h();
            break;
          case 11:
            if (ag.dX < (ag.dz[ag.dm]).i) {
              e(12);
              ag.ea = 0;
              break;
            } 
            ag.bd.d(1);
            break;
          case 12:
            ag.bd.d(1);
            break;
          case 14:
            ag.fD++;
            ag.fI = this.k;
            e.a(0, (ag.fF << 2) + 2 + this.k);
            ag.fw[ag.fD & 0x1] = ag.gf[3];
            break;
          case 15:
            ag.cM[0] = 0;
            for (b = 0; b < 5; b++)
              ag.gf[b] = ""; 
            ag.ap();
            ag.dE = ag.fU;
            break;
          case 16:
            ag.cz.S = 0;
            ag.bb.o();
            if (ag.fu != 0) {
              ag.fu = (short)e.b(ag.fn[2][ag.fv], 5);
            } else {
              ag.fu = (short)e.b(ag.fn[0][ag.fH], 5);
            } 
            ar();
            e(15);
            break;
          case 1:
          case 18:
            as();
            break;
          case 22:
            if ((ag.dz[ag.dm]).g > 200) {
              ag.bd.d(0);
              break;
            } 
            w(2);
            F();
            ag.cM[0] = 0;
            ag.cN = ae.v[ag.cM[0]];
            ag.dE = ag.fU;
            ag.bV = 2;
            ag.ck = 1;
            ag.cL = 0;
            ag.cK = 0;
            break;
          case 39:
            ag.cM[0] = 12;
            ag.cN = ae.v[ag.cM[0]];
            ag.cM[1] = 3;
            break;
        } 
      } 
    } 
    return -1;
  }
  
  final void c() {
    int j;
    int i = -(this.h >> 1);
    if (this.b == 4)
      i += 20; 
    if (ag.bV == 3 || ag.bW == 3)
      i -= 30; 
    b(this.h);
    x.a(ag.bu);
    byte b;
    for (b = 0; b < this.i; b++) {
      b(this.l[b], ag.de + i, 0);
      i += 20;
    } 
    switch (this.b) {
      case 10:
        c(ag.de + this.h / 2 - 18);
        break;
      case 2:
        O(ag.de + i + 5);
        break;
      case 3:
        i += 5;
        for (b = 0; b < 4; b++) {
          if (this.k == b) {
            x.a(ag.bw);
          } else {
            x.a(ag.bu);
          } 
          b(this.l[b + 2], ag.de + i, 0);
          i += 16;
        } 
        break;
      case 4:
        if (ag.bV == 3)
          ag.de -= 30; 
        b(ag.dl, ag.de - 75, ag.dl.length() + 1);
        switch (this.b_) {
          case 10:
            j = (ag.dz[ag.dm]).h * 150 * (1 + (ag.ep ^ 0x1));
            b("Gold Acquired!", ag.de + 10, "Gold Acquired!".length() + 1);
            d(j, ag.dd + (ag.D(j) * 9 >> 1) - ag.db, ag.de + 30, 0);
            break;
          case 11:
            b("Total Exp", ag.de, "Total Exp".length() + 1);
            break;
          case 12:
            b("Time Exp", ag.de - 7, "Time Exp".length() + 1);
            "Time Limit:".length();
            ag.d("Time Limit:", ag.dd - 78 - ag.db, ag.de - 7 + 20);
            j(ag.dd + 34 - ag.db, ag.de - 7 + 21, (ag.dz[ag.dm]).i);
            "Ested Time:".length();
            ag.d("Ested Time:", ag.dd - 78 - ag.db, ag.de - 7 + 40);
            j(ag.dd + 34 - ag.db, ag.de - 7 + 41, ag.dX);
            break;
        } 
        if (ag.bV == 3)
          ag.de += 30; 
        break;
    } 
    if (this.e != 0) {
      b(this.g);
      if (ag.bV == 3)
        ag.de -= 30; 
      b(this.l[5], ag.de - (this.g >> 1) - 3, 0);
      if (ag.bV == 3)
        ag.de += 30; 
    } 
    if (this.s)
      c(ag.de + i - 10); 
    this.j = 0;
  }
  
  final void b(int paramInt) {
    int i = ag.de - (paramInt >> 1) - 10;
    if (r == null)
      r = d(ag.bA.a(33)); 
    if ((ag.bV == 3 || ag.bW == 3) && !ag.bS)
      i -= 30; 
    byte b;
    for (b = 0; b < 26; b++)
      b(r, ag.dd - 103 + b * 8 - ag.db, i, 8, 3, 10, 0); 
    a(ag.dd - 102 - ag.db, i + 3, 210, paramInt + 14);
    b(r, ag.dd - 105 - ag.db, i, 3, 10, 0, 0);
    b(r, ag.dd + 104 - ag.db, i, 3, 10, 2, 0);
    i += 10;
    int[][] arrayOfInt = { { ag.dd - 105 - ag.db, 162, 162, 162, ag.dd + 106 - ag.db }, { ag.dd - 104 - ag.db, 67, 67, 67, ag.dd + 105 - ag.db }, { ag.dd - 103 - ag.db, 33, 33, 33, ag.dd + 104 - ag.db } };
    for (b = 0; b < 3; b++) {
      x.c(arrayOfInt[b][0] + ag.db, i + ag.dc, arrayOfInt[b][0] + ag.db, i + paramInt - 1 + ag.dc, ag.k(arrayOfInt[b][1], arrayOfInt[b][2], arrayOfInt[b][3]));
      x.c(arrayOfInt[b][4] + ag.db, i + ag.dc, arrayOfInt[b][4] + ag.db, i + paramInt - 1 + ag.dc, ag.k(arrayOfInt[b][1], arrayOfInt[b][2], arrayOfInt[b][3]));
    } 
    i += paramInt;
    b(r, ag.dd - 105 - ag.db, i, 3, 10, 5, 0);
    b(r, ag.dd + 104 - ag.db, i, 3, 10, 7, 0);
    i += 7;
    for (b = 0; b < 26; b++)
      b(r, ag.dd - 103 + b * 8 - ag.db, i, 8, 3, 10, 3); 
  }
  
  private void a(int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    if (ag.ct[10] == null)
      ag.ct[10] = d(ag.bA.a(59)); 
    for (byte b = 0; b * 24 < paramInt4; b++) {
      int i;
      if (paramInt4 >= (b + 1) * 24) {
        i = 24;
      } else {
        i = paramInt4 - b * 24;
      } 
      for (byte b1 = 0; b1 * 52 < paramInt3; b1++) {
        int j;
        if (paramInt3 >= (b1 + 1) * 52) {
          j = 52;
        } else {
          j = paramInt3 - b1 * 52;
        } 
        if (ag.ct[10] != null)
          b(ag.ct[10], paramInt1 + b1 * 52, paramInt2 + b * 24, j, i, 0, 0); 
      } 
    } 
  }
  
  private void O(int paramInt) {
    boolean bool = false;
    for (byte b = 0; b < 2; b++) {
      if (this.k == b) {
        x.a(ag.bu);
        bool = true;
      } else {
        x.a(ag.bx);
        bool = false;
      } 
      a(ag.dd - 60 + b * 80, paramInt + ag.dc, 40, 17, bool);
      ag.c(ae.aZ[b], ag.dd - 40 + b * 80, paramInt + 1);
    } 
  }
  
  final void c(int paramInt) {
    x.a(ag.bu);
    a(ag.dd - 60 + 40 + ag.db, paramInt + ag.dc, 40, 17, true);
    ag.c(ae.aZ[2], ag.dd, paramInt);
  }
  
  final void a(String paramString) {
    this.s = false;
    int i = 1;
    if (paramString != "") {
      this.b = (short)(paramString.charAt(0) - 48);
      if (this.b == 3) {
        this.b = 10;
        this.d = 200;
      } 
      short s = 0;
      for (byte b = 0; b < paramString.length(); b++) {
        if (paramString.charAt(b) == '|') {
          s = (short)(s + 1);
          this.l[s] = paramString.substring(i, b);
          i = b + 1;
        } 
      } 
      s = (short)(s + 1);
      this.l[s] = paramString.substring(i, paramString.length());
      this.i = s;
      this.h = (short)(20 * s + (s - 1) * 2);
      if (this.b == 2 || this.b == 10)
        this.h = (short)(this.h + 20); 
      if (this.d == 0)
        this.d = 10; 
      this.j = 1;
    } 
  }
  
  static String d() {
    return " You bought|1 " + e.c(ag.fK[19]) + '.';
  }
  
  static String e() {
    return " You sold|" + e.c(ag.fK[19]) + '.';
  }
  
  final void d(int paramInt) {
    String str2;
    this.a = 1;
    this.s = false;
    if (ag.bV == 3) {
      ag.ck = 1;
    } else {
      ag.cS.j = 1;
    } 
    this.k = 0;
    this.b_ = (short)paramInt;
    String str1;
    char c;
    if ((c = (str1 = ag.M(paramInt + 15)).charAt(0)) >= '0' && c <= '9') {
      this.b = (short)(c - 48);
      if (this.b != 2)
        this.b = 10; 
      str2 = str1.substring(1, str1.length());
    } else {
      this.b = 10;
      str2 = str1;
    } 
    this.d = 200;
    int i = str2.length();
    byte b2 = 0;
    int j = 0;
    for (byte b1 = 0; b1 <= i; b1++) {
      if (b1 == i || str2.charAt(b1) == '\\') {
        if (j == b1) {
          this.l[b2] = " ";
        } else {
          this.l[b2] = str2.substring(j, b1);
        } 
        b2++;
        j = b1 + 1;
      } 
    } 
    this.i = (short)b2;
    switch (paramInt) {
      case 53:
        this.i = 4;
        this.l[0] = this.m;
        this.l[1] = this.n;
        this.l[2] = this.o;
        this.l[3] = this.p;
        break;
      case 34:
        this.l[0] = e.c(ag.fK[19]);
        this.l[1] = this.l[1] + this.m;
        break;
      case 35:
        this.l[1] = this.l[1] + " " + e.c(ag.fK[19]);
        break;
      case 39:
        this.l[3] = this.m + "?";
        break;
      case 40:
        this.l[0] = this.m;
        break;
      case 41:
        this.l[0] = this.m + " " + this.l[0];
        this.l[1] = this.n + " " + this.l[1];
        this.l[4] = this.o + " Level up";
        break;
      case 49:
        this.l[1] = this.n;
        this.l[2] = this.m;
        this.i = 3;
        break;
      case 54:
        this.l[0] = "You can't use the ID.";
        this.i = 1;
        break;
    } 
    this.h = (short)(20 * this.i + (this.i - 1 << 1));
    switch (this.b) {
      case 2:
        this.h = (short)(this.h + 25);
        break;
      case 3:
        this.h = 140;
        break;
      case 4:
        this.h = 150;
        break;
      case 10:
        this.h = (short)(this.h + 30);
        break;
    } 
    ag.ck = 1;
    if (ag.be != null)
      as.aJ(); 
  }
  
  final void e(int paramInt) {
    int i;
    this.a = 0;
    this.s = false;
    byte[] arrayOfByte1 = { 
        2, 2, 2, 4, 3, 3, 5, 3, 3, 3, 
        2, 2, 2, 2, 2, 5, 3, 2, 2, 3, 
        2, 4, 3, 2, 2, 2, 2, 0, 2, 3, 
        1, 1, 1, 1, 4, 4, 4, 1, 5, 5, 
        2, 5, 6 };
    byte[] arrayOfByte2 = { 
        1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 
        4, 4, 4, 1, 3, 1, 1, 1, 1, 2, 
        1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 
        1, 1, 1, 1, 2, 10, 2, 1, 1, 1, 
        2, 2, 2 };
    short[] arrayOfShort = { 
        20, 20, 20, 200, 200, 200, 200, 20, 20, 20, 
        20, 200, 200, 20, 200, 200, 20, 20, 200, 200, 
        200, 20, 20, 20, 20, 20, 20, 20, 200, 200, 
        20, 20, 20, 200, 200, 200, 200, 20, 200, 200, 
        200, 200, 200 };
    if (paramInt == 39)
      this.s = true; 
    this.b = (short)arrayOfByte2[paramInt];
    if (ag.bV == 3) {
      ag.ck = 1;
    } else {
      this.j = 1;
    } 
    this.d = arrayOfShort[paramInt];
    this.i = (short)arrayOfByte1[paramInt];
    this.k = 0;
    this.b_ = (short)paramInt;
    switch (paramInt) {
      case 0:
        this.l[0] = "Saving";
        this.l[1] = "Success!";
        break;
      case 1:
        this.l[0] = "Not enough";
        this.l[1] = "FreeSpace.";
        break;
      case 2:
        this.l[0] = "Not athorized";
        this.l[1] = "Letter.";
        break;
      case 3:
        this.l[0] = "Starting a new game";
        this.l[1] = "will cause your saved";
        this.l[2] = "game to be deleted.";
        this.l[3] = "Continue?";
        break;
      case 4:
        this.l[0] = "Character settings";
        this.l[1] = "are complete.";
        this.l[2] = "Continue?";
        break;
      case 5:
        this.k = 1;
        this.l[0] = "Exit Game";
        this.l[1] = "and go to";
        this.l[2] = "main menu?";
        break;
      case 6:
        B((ag.dz[ag.dm]).e);
        ag.cT[0] = ag.dC.a;
        ag.cT[1] = "Lv" + (ag.cz.l + (ag.dz[ag.dm]).j) + " / Gold: " + ((ag.dz[ag.dm]).h * 150 * (1 + (ag.ep ^ 0x1)));
        this.l[0] = ag.cT[0];
        this.l[1] = ag.cT[1];
        this.l[2] = "Do you want to";
        this.l[3] = "accept this";
        this.l[4] = "mission?";
        break;
      case 7:
        this.l[0] = "Can't Save!";
        this.l[1] = "it Needs all";
        this.l[2] = "enemy dead.";
        break;
      case 8:
      case 9:
        ag.cT[0] = "Stage " + ag.do;
        if (paramInt == 9) {
          ag.cT[0] = ag.cT[0] + " Complete.";
          a_(5);
        } 
        this.l[0] = ag.dl;
        this.l[1] = ag.dn;
        this.l[2] = ag.cT[0];
        break;
      case 10:
        this.l[0] = ag.dn;
        this.l[1] = "Mission Success";
        break;
      case 13:
        ag.cT[0] = ag.cX.a;
        this.l[0] = ag.cT[0];
        this.l[1] = "Acquired!!";
        break;
      case 14:
        this.l[0] = "What do you want";
        this.l[1] = "to talk about?";
        for (i = 0; i < 4; i++)
          this.l[i + 2] = ae.ba[i]; 
        break;
      case 15:
        ag.cT[1] = ag.dC.a;
        this.l[0] = "You visited";
        this.l[1] = ag.cT[1] + '.';
        if (ag.fu != 0) {
          this.l[2] = "Friendship:100%";
        } else {
          this.l[2] = "Friendship ";
          this.l[3] = "increased by 5.";
        } 
        if (ag.fJ < 8) {
          this.l[5] = ag.cT[0];
          this.i = (short)(this.i + 1);
        } else {
          this.l[4] = "";
          this.l[5] = "Press OK";
          this.i = (short)(this.i + 1);
        } 
        a_(10);
        break;
      case 16:
        this.l[0] = "You discussed";
        ag.cT[0] = ae.ba[ag.fI] + " with";
        this.l[1] = ag.cT[0];
        ag.cT[1] = ag.dC.a + '.';
        this.l[2] = ag.cT[1];
        break;
      case 17:
        this.l[0] = "You can't take";
        this.l[1] = "this equipment.";
        break;
      case 18:
        this.l[0] = "Data is crashed";
        this.l[1] = "Shutting down..";
        break;
      case 22:
        this.l[0] = ag.dl;
        this.l[1] = ag.dn;
        this.l[2] = "Mission fail!";
        if (ag.cz.l > 9 && C(100) < ag.cz.l >> 2) {
          i = C(9);
          if ((ag.cz.X[i]).a != 0) {
            ag.bb.e((ag.cz.X[i]).a);
            if ((ag.cz.X[i]).a < 300) {
              ag.cT[0] = ag.cX.a;
            } else if ((ag.cz.X[i]).a < 500) {
              ag.cT[0] = ag.cY.a;
            } else {
              ag.cT[0] = ag.cZ.a;
            } 
            ag.cz.X[i] = null;
            this.l[3] = "Lost!!";
            this.l[4] = ag.cT[0];
            this.i = (short)(this.i + 2);
          } 
        } 
        a_(6);
        break;
      case 23:
        this.l[0] = " / Hp 5 Increased".substring(3);
        this.l[1] = "";
        break;
      case 24:
        this.l[0] = " / MP 3 Increased".substring(3);
        this.l[1] = "";
        break;
      case 25:
        this.l[0] = " / DEF 1 Increased".substring(3);
        this.l[1] = "";
        break;
      case 26:
        this.l[0] = " / ATK 1 Increased".substring(3);
        this.l[1] = "";
        break;
      case 27:
        if (ag.ef != 0) {
          if (ag.ef == 502) {
            ag.cT[0] = " / Catherine's scarf".substring(3);
          } else {
            ag.bb.e(ag.ef);
            ag.cT[0] = ag.cX.a;
          } 
          this.l[0] = ag.cT[0];
          this.i = (short)(this.i + 1);
          this.l[1] = "received!";
          this.i = (short)(this.i + 1);
        } 
        if (ag.eg != 0) {
          if (ag.ef != 0) {
            this.i = (short)(this.i + 1);
            this.l[this.i] = "";
          } 
          byte[] arrayOfByte = null;
          arrayOfByte = ag.v(48);
          int j = 38 * ag.eg + 10;
          byte b = 0;
          for (b = 0; b < 30 && arrayOfByte[j + b] != 0; b++);
          ag.dt[0] = ag.a(arrayOfByte, j, j + b);
          this.i = (short)(this.i + 1);
          this.l[this.i] = "Hidden Mission!";
          ag.cT[1] = ag.dt[0];
          this.i = (short)(this.i + 1);
          this.l[this.i] = ag.cT[1];
        } 
        break;
      case 28:
        this.k = 1;
        this.l[0] = "Exit Game?";
        this.l[1] = "";
        break;
      case 30:
        this.l[0] = "Wait..";
        break;
      case 31:
        this.l[0] = "Wait...";
        break;
      case 32:
        this.l[0] = "Wait....";
        break;
      case 35:
        this.l[0] = "Generals can not be";
        this.l[1] = "visited at this time.";
        this.l[2] = "Try again after";
        this.l[3] = "completing a mission.";
        break;
      case 36:
        this.l[0] = "Difficulty will";
        this.l[1] = "not change";
        this.l[2] = "after starting.";
        this.l[3] = "Continue?";
        break;
      case 38:
        this.l[0] = "Not enough";
        this.l[1] = "FreeSpace.";
        this.l[2] = "Please delete";
        this.l[3] = "some files";
        this.l[4] = "before starting.";
        break;
      case 39:
        this.l[0] = "You must have";
        this.l[1] = "at least 3 items";
        this.l[2] = "in order to have";
        this.l[3] = "them combined.";
        this.l[4] = "";
        break;
      case 40:
        this.l[0] = "Would you like";
        this.l[1] = "sound enabled?";
        break;
      case 41:
        this.l[0] = "Accessing 'More Games'";
        this.l[1] = "will exit the game";
        this.l[2] = "and open the browser.";
        this.l[3] = "Would you like";
        this.l[4] = "to continue?";
        break;
      case 42:
        this.l[0] = "Selecting YES will";
        this.l[1] = "exit the game and open";
        this.l[2] = "the browser to allow";
        this.l[3] = "downloading of the";
        this.l[4] = "Multiplayer version.";
        this.l[5] = "Continue?";
        break;
    } 
    boolean bool = false;
    this.h = (short)(20 * this.i + (this.i - 1 << 1));
    switch (this.b) {
      case 2:
        this.h = (short)(this.h + 25);
        break;
      case 3:
        this.h = 140;
        break;
      case 4:
        this.h = 150;
        break;
      case 10:
        this.h = (short)(this.h + 25);
        break;
    } 
    ag.ck = 1;
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\l.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */