import javax.microedition.lcdui.Image;

public final class e extends ag {
  public static byte[] a;
  
  public e() {
    super(ag.bs);
  }
  
  final void a(int paramInt) {
    if (paramInt == 1) {
      if (ag.cM[0] != 5) {
        x.a(ag.bu);
        if (ag.bW == 3) {
          x.b(7, 19, 225, 242, 0);
        } else {
          e();
        } 
        if (ag.cM[0] != 28) {
          if (ag.bW == 3) {
            x.a(ag.bu);
            b(ag.fT[ag.cM[0]], 15, 0);
          } else {
            b(ag.fT[ag.cM[0]], 2 - ag.dc, 0);
          } 
        } else {
          String str = ag.b(ag.ga[0], ag.ej);
          if (ag.bW == 3) {
            x.a(ag.bu);
            b(str, 15, 0);
          } else {
            b(str, 2 - ag.dc, 0);
          } 
        } 
        if (ae.u[ag.cM[0]] != -1 || (ae.u[ag.cM[0]] == -1 && ag.cM[0] == 15))
          if (ag.cM[0] == 3) {
            ag.h(11, 2);
          } else {
            ag.h(-1, 2);
          }  
      } 
      switch (ag.cM[0]) {
        case 0:
          ag.cL = 0;
          ag.cK = 0;
          bf();
          break;
        case 1:
        case 2:
        case 10:
        case 11:
        case 12:
        case 13:
        case 25:
        case 27:
          f();
          break;
        case 3:
          aH();
          break;
        case 4:
          aI();
          break;
        case 5:
          S();
          aJ();
          break;
        case 6:
          aK();
          break;
        case 7:
          aL();
          aM();
          break;
        case 8:
        case 14:
          O(1);
          break;
        case 9:
          j();
          break;
        case 15:
          P(0);
          k();
          break;
        case 16:
          n(ag.cM[2], 0);
          k();
          ag.h(5, -1);
          break;
        case 17:
          Q(0);
          k();
          ag.h(5, -1);
          break;
        case 18:
          d(0);
          k();
          break;
        case 19:
          aN();
          break;
        case 20:
          b(ag.fE);
          if (ag.fA[0] > 0)
            a(ag.fD + 1 & 0x1, 0, 1); 
          if (ag.fA[1] > 0)
            a(ag.fD & 0x1, 0, 1); 
          break;
        case 21:
        case 22:
        case 23:
        case 24:
          c(true);
          k();
          break;
        case 28:
          l();
          break;
        case 29:
          aU();
          break;
      } 
      if (ag.cS.b != 0) {
        ag.cS.c();
        return;
      } 
    } else {
      if (paramInt == 2) {
        switch (ag.cM[0]) {
          case 0:
            bf();
            return;
          case 4:
            x.a(ag.bu);
            e();
            aI();
            ag.ch = -5;
            ag.dS = 0;
            i();
            ag.ck--;
            break;
        } 
        return;
      } 
      if (ag.cS.b != 0) {
        if (ag.cS.j != 0) {
          ag.cS.c();
          return;
        } 
      } else {
        switch (ag.cM[0]) {
          case 0:
            bf();
            return;
          case 4:
            i();
            return;
          case 5:
            S();
            aJ();
            return;
          case 7:
            aM();
            ag.f(ag.bP, ag.de + 32 + ag.dc);
            return;
          case 8:
          case 14:
            if (ag.da != 0) {
              O(0);
              return;
            } 
            break;
          case 15:
            if (ag.da != 0)
              P(ag.da); 
            k();
            return;
          case 16:
            k();
            return;
          case 17:
            if (ag.da != 0)
              Q(1); 
            k();
            return;
          case 18:
            if (ag.da != 0)
              d(1); 
            k();
            return;
          case 20:
            aO();
            return;
          case 21:
          case 22:
          case 23:
          case 24:
            c(false);
            k();
            break;
        } 
      } 
    } 
  }
  
  final void a() {
    int i;
    if (ag.bj)
      ag.ed = -1; 
    switch (ag.cM[0]) {
      case 4:
        return;
      case 7:
        if ((i = ag.r(ag.ch)) == -7) {
          if (ag.bz.a().length() == 0) {
            ag.cM[0] = 6;
            ag.ck = 1;
            return;
          } 
          ag.bz.a(-8);
          return;
        } 
        if (i == -5 || i == 53)
          if (ag.bP == 26) {
            if (ag.bz.a().length() != 0) {
              ag.cz.k = ag.bz.a();
              ag.bz.a(ag.cz.k);
              ag.cM[0] = 8;
              ag.O();
              ag.cN = 4;
              ag.aw();
              return;
            } 
          } else {
            byte b;
            if (ag.bz.a().length() == 0) {
              b = 65;
            } else {
              b = 97;
            } 
            ag.bz.a(b + ag.bP);
            return;
          }  
        return;
      case 20:
        if (ag.ch != -5) {
          ag.ch = -999;
          return;
        } 
        return;
      case 21:
      case 22:
      case 23:
      case 24:
        aW();
        return;
    } 
    switch (ag.ch) {
      case -1:
      case 50:
        aB();
        return;
      case -2:
      case 56:
        aC();
        return;
      case -3:
      case 52:
        aD();
        return;
      case -4:
      case 54:
        aE();
        return;
      case 42:
        if (ag.cM[0] == 18) {
          ag.ck = ar.c(0);
          return;
        } 
        break;
      case 35:
        if (ag.cM[0] == 18) {
          ag.ck = ar.c(1);
          return;
        } 
        break;
      case -5:
      case 53:
        b();
        return;
      case -6:
        if (ag.cM[0] == 16 || ag.cM[0] == 17 || ag.cM[0] == 3) {
          b();
          return;
        } 
        break;
      case -7:
        aF();
        break;
    } 
  }
  
  private static int m(int paramInt1, int paramInt2) {
    byte b;
    return b = ae.aW[paramInt1][paramInt2];
  }
  
  private void aB() {
    switch (ag.cM[0]) {
      case 0:
        if (ag.cL == 0) {
          ag.ck = 2;
          ag.cL = -1;
        } 
        return;
      case 3:
      case 5:
      case 6:
      case 18:
      case 20:
      case 28:
        return;
      case 8:
      case 14:
        T(0);
        ag.cM[1] = ag.cM[1] - 1;
        if (ag.cM[1] - 1 < 0)
          ag.cM[1] = ag.cN - 1; 
        T(1);
        return;
      case 9:
        ag.cM[1] = ag.cM[1] - 1;
        if (ag.cM[1] - 1 < 1)
          ag.cM[1] = ag.cN - 1; 
        if (!ag.df && ag.cM[1] == 1)
          ag.cM[1] = 0; 
        ag.I();
        ag.ck = 1;
        return;
      case 15:
        if (ag.cM[3] == 2) {
          if (ag.cM[1] < 4) {
            ag.cM[2] = ag.cM[2] - 3;
            if (ag.cM[2] < 0)
              ag.cM[2] = ag.cM[2] + 18; 
            ag.da = 3;
          } 
          ag.da = 3;
          return;
        } 
        return;
      case 16:
        ag.cM[2] = ag.cM[2] + 1;
        if (ag.cM[2] + 1 >= ag.cN)
          ag.cM[2] = 0; 
        ag.ck = 1;
        return;
      case 17:
        ag.cM[2] = ag.cM[2] - 5;
        if (ag.cM[2] < 0)
          ag.cM[2] = ag.cM[2] + 25; 
        ag.da = 1;
        return;
      case 19:
        if (ag.cM[1] > 0) {
          ag.cM[1] = ag.cM[1] - 1;
          ag.ck = 1;
          return;
        } 
        return;
      case 29:
        ag.cM[1] = 1 - ag.cM[1];
        ag.ck = 1;
        return;
      case 25:
        if (ag.cM[1] == 20) {
          ag.cM[1] = 23;
        } else {
          ag.cM[1] = ag.cM[1] - 1;
        } 
        if (ag.cM[1] < ag.cM[2])
          ag.cM[1] = ag.cM[2] + 4; 
        ag.ck = 1;
        return;
    } 
    ag.cM[1] = ag.cM[1] - 1;
    if (ag.cM[1] - 1 < 0)
      ag.cM[1] = ag.cN - 1; 
    ag.I();
    ag.ck = 1;
  }
  
  private void aC() {
    switch (ag.cM[0]) {
      case 0:
        if (ag.cL == 0) {
          ag.cL = 1;
          ag.ck = 2;
        } 
        return;
      case 3:
      case 5:
      case 6:
      case 18:
      case 20:
      case 28:
        return;
      case 8:
      case 14:
        T(0);
        ag.cM[1] = ag.cM[1] + 1;
        if (ag.cM[1] + 1 >= ag.cN)
          ag.cM[1] = 0; 
        T(1);
        return;
      case 9:
        ag.cM[1] = ag.cM[1] + 1;
        if (ag.cM[1] + 1 >= ag.cN) {
          ag.cM[2] = 0;
          ag.cM[1] = 0;
        } 
        if (!ag.df && ag.cM[1] == 1)
          ag.cM[1] = 2; 
        ag.I();
        ag.ck = 1;
        return;
      case 15:
        if (ag.cM[3] == 2) {
          if (ag.cM[1] < 4) {
            ag.cM[2] = ag.cM[2] + 3;
            if (ag.cM[2] > 17)
              ag.cM[2] = ag.cM[2] - 18; 
          } 
          ag.da = 3;
          return;
        } 
        return;
      case 16:
        ag.cM[2] = ag.cM[2] - 1;
        if (ag.cM[2] - 1 < 0)
          ag.cM[2] = ag.cN - 1; 
        ag.ck = 1;
        return;
      case 17:
        ag.cM[2] = ag.cM[2] + 5;
        if (ag.cM[2] > 24)
          ag.cM[2] = ag.cM[2] - 25; 
        ag.da = 1;
        return;
      case 19:
        if (ag.cM[1] < ag.cN - 1) {
          ag.cM[1] = ag.cM[1] + 1;
          ag.ck = 1;
          return;
        } 
        return;
      case 29:
        ag.cM[1] = 1 - ag.cM[1];
        ag.ck = 1;
        return;
      case 25:
        if (ag.cM[1] == 23) {
          ag.cM[1] = 20;
        } else {
          ag.cM[1] = ag.cM[1] + 1;
        } 
        if (ag.cM[1] > ag.cM[2] + 4)
          ag.cM[1] = ag.cM[2]; 
        ag.ck = 1;
        return;
    } 
    ag.cM[1] = ag.cM[1] + 1;
    if (ag.cM[1] + 1 >= ag.cN) {
      ag.cM[2] = 0;
      ag.cM[1] = 0;
    } 
    ag.I();
    ag.ck = 1;
  }
  
  private void aD() {
    switch (ag.cM[0]) {
      case 1:
        if (ag.bj && ag.cq > 0) {
          ag.cq = (byte)(ag.cq - 1);
          C();
        } else {
          break;
        } 
        ag.ck = 1;
        break;
      case 3:
        if (ag.cM[2] > 0) {
          ag.cM[2] = ag.cM[2] - 1;
        } else {
          ag.cM[2] = ag.dq[0] / 6;
        } 
        ag.ck = 1;
        return;
      case 28:
        if (ag.cM[1] <= 0 && ag.ej == 8) {
          ag.cM[1] = 1;
          ag.ck = 1;
          return;
        } 
        ag.ck = 1;
        ag.cM[1] = ag.cM[1] - 1;
        if (ag.cM[1] - 1 < 0) {
          ag.cM[1] = ae.z[ag.ej + 1] - ae.z[ag.ej] - 1;
          return;
        } 
        break;
      case 5:
        ag.ck = 1;
        ag.cM[1] = ag.cM[1] - 1;
        if (ag.cM[1] - 1 < 0) {
          ag.cM[1] = 8;
          return;
        } 
        break;
      case 18:
        ag.da = 1;
        ag.cM[1] = ag.cM[1] - 1;
        if (ag.cM[1] - 1 < 0) {
          ag.cM[1] = ag.cN - 1;
          return;
        } 
        break;
      case 6:
        ag.cz.aB = ag.cz.aB - 1 & 0x3;
        ag.ck = 1;
        break;
      case 9:
        y(0);
        ag.ck = 1;
        break;
      case 15:
        ag.cM[ag.cM[3]] = ag.cM[ag.cM[3]] - 1;
        if (ag.cM[3] == 1) {
          if (ag.cM[ag.cM[3]] < 0)
            ag.cM[ag.cM[3]] = 4; 
          ag.da = 2;
          return;
        } 
        if (ag.cM[1] < 4) {
          if (ag.cM[ag.cM[3]] < 0)
            ag.cM[ag.cM[3]] = 17; 
        } else if (ag.cM[ag.cM[3]] < 18) {
          ag.cM[ag.cM[3]] = 20;
        } 
        ag.da = 3;
        return;
      case 16:
        ag.ck = 1;
        ag.cM[2] = ag.cM[2] + 1;
        if (ag.cM[2] + 1 >= ag.cN) {
          ag.cM[2] = 0;
          return;
        } 
        break;
      case 17:
        ag.cM[2] = ag.cM[2] - 1;
        if (ag.cM[2] - 1 < 0)
          ag.cM[2] = ag.cN - 1; 
        ag.da = 1;
        return;
      case 19:
        ag.cM[1] = ag.cM[1] - 4;
        if (ag.cM[1] < 0)
          ag.cM[1] = 0; 
        ag.ck = 1;
        return;
      case 25:
        ag.cM[2] = ag.cM[2] - 5;
        ag.cM[1] = ag.cM[1] - 5;
        if (ag.cM[2] < 0) {
          ag.cM[2] = 20;
          ag.cM[1] = 20 + (ag.cM[1] + 20) % 5;
        } 
        ag.ck = 1;
        break;
    } 
  }
  
  private void aE() {
    switch (ag.cM[0]) {
      case 1:
        if (ag.bj && ag.cq < 44) {
          ag.cq = (byte)(ag.cq + 1);
          C();
        } else {
          break;
        } 
        ag.ck = 1;
        break;
      case 3:
        if ((ag.cM[2] + 1) * 6 - 1 < ag.dq[0]) {
          ag.cM[2] = ag.cM[2] + 1;
        } else {
          ag.cM[2] = 0;
        } 
        ag.ck = 1;
        return;
      case 28:
        if (ag.cM[1] >= 1 && ag.ej == 8) {
          ag.ck = 1;
          ag.cM[1] = 0;
          return;
        } 
        ag.ck = 1;
        ag.cM[1] = ag.cM[1] + 1;
        if (ag.cM[1] + 1 >= ae.z[ag.ej + 1] - ae.z[ag.ej]) {
          ag.cM[1] = 0;
          return;
        } 
        break;
      case 5:
        ag.ck = 1;
        ag.cM[1] = ag.cM[1] + 1;
        if (ag.cM[1] + 1 >= 9) {
          ag.cM[1] = 0;
          return;
        } 
        break;
      case 18:
        ag.cM[1] = ag.cM[1] + 1;
        if (ag.cM[1] + 1 >= ag.cN)
          ag.cM[1] = 0; 
        ag.da = 1;
        return;
      case 6:
        ag.cz.aB = ag.cz.aB + 1 & 0x3;
        ag.ck = 1;
        break;
      case 9:
        y(1);
        ag.ck = 1;
        break;
      case 15:
        ag.cM[ag.cM[3]] = ag.cM[ag.cM[3]] + 1;
        if (ag.cM[3] == 1) {
          if (ag.cM[ag.cM[3]] > 4)
            ag.cM[ag.cM[3]] = 0; 
          ag.da = 2;
          return;
        } 
        if (ag.cM[1] < 4) {
          if (ag.cM[ag.cM[3]] > 17)
            ag.cM[ag.cM[3]] = 0; 
        } else if (ag.cM[ag.cM[3]] > 20) {
          ag.cM[ag.cM[3]] = 18;
        } 
        ag.da = 3;
        return;
      case 16:
        ag.ck = 1;
        ag.cM[2] = ag.cM[2] - 1;
        if (ag.cM[2] - 1 < 0) {
          ag.cM[2] = ag.cN - 1;
          return;
        } 
        break;
      case 17:
        ag.cM[2] = ag.cM[2] + 1;
        if (ag.cM[2] + 1 >= ag.cN)
          ag.cM[2] = 0; 
        ag.da = 1;
        return;
      case 19:
        ag.cM[1] = ag.cM[1] + 4;
        if (ag.cM[1] >= ag.cN)
          ag.cM[1] = ag.cN - 1; 
        ag.ck = 1;
        return;
      case 25:
        ag.cM[2] = ag.cM[2] + 5;
        ag.cM[1] = ag.cM[1] + 5;
        if (ag.cM[2] > 20) {
          ag.cM[2] = 0;
          ag.cM[1] = ag.cM[1] % 5;
        } 
        ag.ck = 1;
        break;
    } 
  }
  
  final void b() {
    if (ag.cM[0] == 9) {
      y(1);
      ag.ck = 1;
      return;
    } 
    if (ag.cM[0] == 5) {
      switch (ag.cM[1]) {
        case 4:
          ag.ej = 0;
          break;
        case 5:
          ag.ck = 1;
          ag.cO = ag.cM[0];
          ag.cM[0] = 28;
          ag.cM[1] = 0;
          ag.cM[2] = 0;
          ag.dE = ag.ga;
          ag.ei = (short)ag.cO;
          ag.ej = 8;
          return;
        case 6:
          ag.cS.e(41);
          return;
        case 7:
          ag.cS.e(42);
          return;
        case 8:
          ag.cS.e(28);
          ag.ck = 1;
          return;
      } 
      int[] arrayOfInt = { 0, 1, 3, 4, 5 };
      ag.cM[1] = arrayOfInt[ag.cM[1]];
    } 
    if (m(ag.cM[0], ag.cM[1] % 7) > -1) {
      c();
      ag.cN = ae.v[ag.cM[0]];
      switch (ag.cM[0]) {
        case 1:
          aG();
          C();
          break;
        case 3:
          ag.dm = (short)ag.cM[1];
          D();
          break;
        case 7:
          ag.cz.k = "";
          break;
        case 9:
          ag.ai();
          break;
        case 10:
          ag.dE = ag.fW;
          break;
        case 12:
          ag.dE = ag.fX;
          break;
        case 13:
          ag.dE = ag.fY;
          break;
        case 14:
          ag.O();
          break;
        case 15:
          ag.cM[3] = 1;
          ag.ct[37] = d(ag.bA.a(44));
          ag.ct[38] = d(ag.bA.a(45));
          break;
        case 17:
          if (ag.cO == 16 && (ag.cz.X[ag.cM[2]]).a != 0)
            for (byte b = 0; b < 25; b++) {
              if (0 == (ag.cz.Y[b]).a)
                a(ag.cz.X[ag.cM[2]], ag.cz.Y[b]); 
            }  
          ag();
          break;
        case 20:
          bg();
          break;
        case 21:
        case 22:
        case 23:
        case 24:
          aY();
          break;
        case 27:
          ag.dE = ag.ga;
          ag.ei = (short)ag.cO;
          break;
        case 28:
          ag.ej = (short)ag.cM[1];
          ag.cN = ae.z[ag.ej + 1] - ae.z[ag.ej];
          break;
      } 
      ag.cM[2] = 0;
      ag.cM[1] = 0;
      return;
    } 
    switch (ag.cM[0]) {
      case 0:
        if (ag.cM[1] == 3) {
          if (ag.fo == 0) {
            ag.cS.e(35);
            return;
          } 
          if (ag.cz.S != 0 && ag.fo != 0) {
            c();
            ag.cM[0] = 19;
            ag.fu = (short)ag.L(504);
            if (ag.fu != 0) {
              ag.cN = 44;
            } else {
              ag.cN = ag.fo;
            } 
            bh();
            ag.cM[2] = 0;
            ag.cM[1] = 0;
            return;
          } 
          ag.cS.e(35);
          ag.ck = 0;
          ag.cL = 0;
          ag.cK = 0;
          return;
        } 
        if (ag.cM[1] == 2) {
          ag.be.g();
          ag.ck = 0;
          ag.cL = 0;
          ag.cK = 0;
          return;
        } 
        break;
      case 1:
        if ((ag.dw & 1L << ag.ds[ag.cM[1]] - 1) != 0L) {
          c();
          ag.cM[0] = 2;
          ag.cN = ae.v[ag.cM[0]];
          ag.dk = (short)(byte)ag.cM[1];
          bi();
          ag.cM[2] = 0;
          ag.cM[1] = 0;
          return;
        } 
        break;
      case 3:
        ag.cS.e(6);
        return;
      case 5:
        ag.ck = 1;
        if (ag.cM[1] == 0) {
          if (ag.aq()) {
            U();
            if (ag.fS != 0)
              return; 
            ag.ai();
            F();
            c();
            ag.cK = 0;
            ag.cL = 0;
            ag.cM[0] = 0;
            ag.cN = ae.v[ag.cM[0]];
            ag.dE = ag.fU;
            ag.cM[2] = 0;
            ag.cM[1] = 0;
            aA();
            if (ag.dj != 0) {
              C();
              bi();
              D();
              y();
              U();
              ag.dW[1] = ag.B();
              ag.dW[0] = ag.B();
              ag.dV = ag.dW[0] - ag.dV;
              a_(-1);
              return;
            } 
          } 
          break;
        } 
        if (ag.cM[1] == 1) {
          ag.bz = null;
          ag.bz = new at("", 8, 10);
          if (ag.aq()) {
            ag.cS.e(3);
            return;
          } 
          au();
          return;
        } 
        break;
      case 8:
      case 14:
        if (ag.cz.J > 0) {
          ag.da = 1;
          ag.cz.J--;
          switch (ag.cM[1]) {
            case 0:
              ag.cz.o += 5;
              break;
            case 1:
              ag.cz.q += 3;
              break;
            case 2:
              ag.cz.m++;
              break;
            case 3:
              ag.cz.n++;
              break;
          } 
          if (ag.cM[0] == 8 && ag.cz.J == 0) {
            ag.cS.e(4);
            ag.ck = 1;
            return;
          } 
        } 
        break;
      case 10:
        if (ag.cM[1] == 2) {
          ag.cS.e(5);
          return;
        } 
        break;
      case 11:
        switch (ag.cM[1]) {
          case 0:
            if (ar() != 0)
              ag.cS.e(0); 
            break;
        } 
        return;
      case 15:
        if (ag.cM[3] == 1) {
          if (ag.cz.V[ag.cM[1]] != 0) {
            ag.cM[2] = ae.aD[ag.cz.V[ag.cM[1]] - 12];
            ag.cz.V[ag.cM[1]] = 0;
          } else if (ag.cM[1] < 4) {
            ag.cM[2] = 0;
          } else {
            ag.cM[2] = 18;
          } 
          ag.cM[3] = 2;
          if (ag.cM[2] < 18) {
            ag.da = 6;
            return;
          } 
          ag.ck = 1;
          return;
        } 
        if (ae.aC[ag.cM[2]] != 0) {
          if (ag.cz.W[ae.aC[ag.cM[2]] - 12] != 0) {
            ag.cz.V[ag.cM[1]] = ae.aC[ag.cM[2]];
            ag.cM[3] = 1;
          } 
          ag.da = 6;
          return;
        } 
        break;
      case 17:
        if ((ag.cz.Y[ag.cM[2]]).a != 0) {
          byte b = ag.g((ag.cz.Y[ag.cM[2]]).a);
          if (ag.m((ag.cz.Y[ag.cM[2]]).a) <= ag.cz.l) {
            switch ((ag.cz.Y[ag.cM[2]]).a) {
              case 434:
                (ag.cz.Y[ag.cM[2]]).a = 0;
                ag.cz.o += 5;
                ag.cS.e(23);
                break;
              case 435:
                (ag.cz.Y[ag.cM[2]]).a = 0;
                ag.cz.q += 3;
                ag.cS.e(24);
                break;
              case 436:
                (ag.cz.Y[ag.cM[2]]).a = 0;
                ag.cz.n++;
                ag.cS.e(25);
                break;
              case 437:
                (ag.cz.Y[ag.cM[2]]).a = 0;
                ag.cz.m++;
                ag.cS.e(26);
                break;
              case 502:
              case 504:
                ag.cS.e(17);
                break;
              default:
                a(ag.cz.Y[ag.cM[2]], ag.cz.X[ae.aE[b]]);
                break;
            } 
          } else {
            ag.cS.e(17);
          } 
        } 
        ag.da = 1;
        return;
      case 25:
        if ((ag.ed & 1 << ag.cM[1]) != 0) {
          c();
          l(ag.cM[1], 0);
          return;
        } 
        ag.cS.a("3You must first complete|the missions needed|to view this ending.");
        return;
      case 29:
        ag.cS.e(36);
        break;
    } 
  }
  
  private void aF() {
    boolean bool = false;
    if (ae.u[ag.cM[0]] > -1) {
      switch (ag.cM[0]) {
        case 14:
        case 15:
        case 16:
        case 17:
        case 18:
          ar();
          break;
      } 
      if (ae.u[ag.cM[0]] > 99) {
        ag.ej = 0;
        if (ag.cM[0] == 28 && ag.cO == 5) {
          ag.ej = 7;
          bool = true;
        } 
        ag.cM[0] = ag.cO;
        if (ag.cM[0] == 0) {
          ag.cK = 0;
          ag.cL = 0;
        } 
        ag.ap();
        ag.ak();
        if (bool) {
          ag.cM[1] = 5;
          return;
        } 
      } else {
        if (ag.cM[0] == 1)
          F(); 
        ag.cM[0] = ae.u[ag.cM[0]];
        if (ag.cM[0] == 0) {
          ag.cK = 0;
          ag.cL = 0;
        } 
        ag.ap();
        ag.ak();
        if (ag.cO == 5)
          switch (ag.cM[1]) {
            case 3:
              ag.cM[1] = 2;
              break;
            case 4:
              ag.cM[1] = 3;
              if (ag.bW == 3) {
                ag.bV = ag.bW;
                ag.bW = -1;
                ag.cM[0] = 10;
                ag.cM[1] = 4;
                ag.cN = 7;
                ag.dE = ag.fZ;
                return;
              } 
              break;
            case 5:
              ag.cM[1] = 4;
              break;
          }  
        if (ag.cO == 25)
          ag.cM[1] = 4; 
        if (ag.cO == 27) {
          ag.cM[1] = 3;
          if (ag.bW == 3) {
            ag.bV = ag.bW;
            ag.bW = -1;
            ag.cM[0] = 10;
            ag.cM[1] = 4;
            ag.cN = 7;
            ag.dE = ag.fZ;
            return;
          } 
        } 
      } 
    } else {
      switch (ag.cM[0]) {
        case 0:
          ag.aj();
          aG();
          ae();
          ag.cM[0] = 5;
          ag.cN = 10;
          ag.cM[2] = 0;
          ag.cM[1] = 0;
          ag.cS.b = 0;
          ag.ck = 1;
          return;
        case 15:
          if (ag.cM[3] == 1) {
            ag.cM[0] = 13;
            ag.ap();
            ag.ct[37] = null;
            ag.ct[38] = null;
            ar();
            return;
          } 
          ag.cM[3] = 1;
          ag.da = 6;
          return;
        case 27:
          ag.cM[0] = ag.ei;
          ag.ap();
          ag.ak();
          break;
      } 
    } 
  }
  
  private static void aG() {
    ag.cy = 0;
    while (ag.cy < 4) {
      ag.ct[26 + ag.cy] = null;
      ag.cy++;
    } 
    ag.gl = null;
  }
  
  final void c() {
    ag.cO = ag.cM[0];
    ag.cP[ag.cM[0]] = (short)ag.cM[1];
    ag.cQ[ag.cM[0]] = (short)ag.cM[2];
    ag.cM[0] = m(ag.cM[0], ag.cM[1] % 7);
    ag.ck = 1;
    ag.da = 0;
  }
  
  final void d() {
    ag.ct[17] = null;
    ag.ct[10] = null;
    ag.cU = null;
    ag.cW = null;
    ag.cV = null;
    for (byte b = 1; b < 4; b++)
      ag.ct[0 + b] = null; 
    ag.fN = null;
    aG();
  }
  
  final void e() {
    a(ag.ct[7], 0, 0, ag.bZ.a, ag.bZ.b, 0, 0);
  }
  
  final void f() {
    int i = ag.dd - 90;
    byte[] arrayOfByte = { 
        13, 34, 20, 0, 0, 0, 0, 0, 0, 0, 
        12, 18, 12, 13, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 13, 0, 0 };
    byte b2 = (ag.cN > 5) ? 5 : ag.cN;
    if (ag.cM[0] == 25 && ag.cM[2] >= 20) {
      b2 = 4;
      if (ag.cM[1] >= 24)
        ag.cM[1] = 23; 
    } 
    int j = ag.de - (b2 * 30 - 10) / 2;
    if (ag.bV == 3 || ag.bW == 3)
      j -= 30; 
    int k = j;
    byte b = arrayOfByte[ag.cM[0]];
    for (byte b1 = 0; b1 < b2; b1++) {
      boolean bool;
      if (ag.cM[1] - ag.cM[2] == b1) {
        bool = true;
        x.a(ag.bw);
      } else {
        bool = false;
        x.a(ag.bu);
      } 
      int m = i;
      a(m, j + ag.dc, 180, 20, bool);
      if (ag.bV == 2) {
        switch (ag.cM[0]) {
          case 0:
            if (ag.cM[2] + b1 == 3 && (0 == ag.cz.S || ag.fo == 0))
              x.a(ag.bx); 
            break;
          case 1:
            if (ag.bj)
              ag.dw = -1L; 
            if (0L == (ag.dw & 1L << ag.ds[ag.cM[2] + b1] - 1))
              x.a(ag.bx); 
            break;
          case 25:
            if (0 == (ag.ed & 1 << ag.cM[2] + b1))
              x.a(ag.bx); 
            break;
        } 
      } else {
        switch (ag.cR.a) {
          case 1:
            if (ag.cM[2] + b1 == 2 && (ag.ez > 0 || ag.cr != 0 || ag.eD[0] != 0))
              x.a(ag.bx); 
            break;
        } 
      } 
      if (ag.cM[0] == 25) {
        if (ag.cM[2] + b1 < 24) {
          byte[] arrayOfByte1;
          String str = ag.a(arrayOfByte1 = d(54, 38 + ag.cM[2] + b1), 0, arrayOfByte1.length);
          b(str, j - 1, 18);
        } 
      } else if (ag.cM[0] == 0 || ag.cM[0] == 10 || ag.cM[0] == 12 || ag.cM[0] == 13 || ag.cM[0] == 27) {
        b(ag.b(ag.dE[0], b1 + ag.cM[2]), j - 1, 0);
      } else {
        b(ag.dE[b1 + ag.cM[2]], j - 1, b);
      } 
      j += 30;
    } 
    if (ag.cM[0] == 25) {
      a(ag.cM[2] / 5 + 1, 5, ag.bZ.b - 35, true);
    } else if (ag.cM[2] != 0 || ag.cM[2] + 5 < ag.cN - 1) {
      f(2, ag.dd - 8 - ag.db, k - 10 - 5);
      f(3, ag.dd - 8 - ag.db, j - 5);
    } 
    if (ag.cM[0] == 10) {
      x.a(ag.bU, 120, ag.dc + 15, 17);
      x.a(ag.bu);
      b("PAUSE", 13, 0);
    } 
    if (ag.bj && ag.cM[0] == 1) {
      x.a(ag.bu);
      x.b(ag.bJ / 2 - 16, ag.bK - 17, 32, 17, 0);
      x.a("" + (ag.cq + 1), ag.bJ / 2, ag.bK - 16, 1);
    } 
  }
  
  private void aH() {
    a(ag.dd - 100 + ag.db, ag.de - 80, 200, 40, false);
    b(ag.dl, ag.de - 80, 30);
    b(ag.dn, ag.de - 60, 30);
    a(ag.dd - 110, ag.de - 30, 220, 119, false);
    for (byte b = 0; b < 6; b++) {
      if (ag.dq[0] >= ag.cM[2] * 6 + b)
        ag.a(ag.dd - 100 + ag.db, ag.de - 28 + b * 20 + ag.dc, ag.dp[0][ag.cM[2] * 6 + b]); 
    } 
    a(ag.cM[2] + 1, ag.dq[0] / 6 + 1, ag.de + 110, true);
  }
  
  final void g() {
    E();
    ag.ct[18] = d(ag.bA.a(77));
  }
  
  private void aI() {
    b(ag.dB[ag.dm]);
    q(1);
    R(3);
  }
  
  final void h() {
    int i;
    if ((ag.dK & 0x1) != 0) {
      i = 0 + ag.dC.e;
    } else {
      i = 38 + ag.cz.aB;
    } 
    int j = ag.bY.b - 46 - 4;
    a(2 + ag.db, j + ag.dc, 48, 48, true);
    a(ag.bB.a(i), 3 + ag.db, ++j + ag.dc, 46, 46, 0, 0);
    aT();
    q(1);
  }
  
  final void i() {
    byte[] arrayOfByte1 = { 2, 3, 5 };
    byte[] arrayOfByte2 = { 2, 1, 1 };
    if (ag.bV == 5 && ag.ch != -6)
      ag.ch = -999; 
    x.a(ag.bu);
    if (ag.ch == -6) {
      ag.dS = 1;
      ag.dQ = (short)ag.dq[ag.dR];
      ag.dK = (short)arrayOfByte1[ag.dG];
    } 
    if (ag.dS > 0) {
      ag.dS = (short)(ag.dS - 1);
      if (ag.ch != -999)
        ag.dS = 0; 
      if (ag.dS < 1) {
        if (ag.dQ >= ag.dq[ag.dR]) {
          if (ag.dK >= arrayOfByte1[ag.dG]) {
            ag.ck = 1;
            if (ag.dG != 0) {
              if (ag.dG == 1) {
                ag.bV = 3;
                return;
              } 
              if (ag.cr != 0) {
                w(2);
                F();
                ag.cM[0] = 0;
                ag.cN = ae.v[ag.cM[0]];
                ag.dE = ag.fU;
                ag.bV = 2;
                ag.cL = 0;
                ag.cK = 0;
                ag.ck = 1;
                L();
                return;
              } 
              ag.co = 1;
              ag.cn = 5;
              ag.bV = 3;
              return;
            } 
            y();
            return;
          } 
          ag.dP = 0;
          ag.dQ = 0;
          if (0 == ag.dG)
            ag.dR = (short)(ag.dR + 1 & 0x1); 
          ag.ao();
          z(ag.dI + ag.dK - 1);
          if (ag.dG != 0) {
            h();
            return;
          } 
          aS();
          return;
        } 
        ag.dP = (short)(ag.dP + 1);
        ag.dQ = (short)(ag.dQ + 1);
        ag.dO = 0;
        ag.dN = ag.dL[ag.dR];
        if (ag.dP > arrayOfByte2[ag.dG]) {
          ag.dP = (short)arrayOfByte2[ag.dG];
          for (byte b = 0; b < 20; b++) {
            if (b < ag.dq[ag.dR])
              ag.dp[ag.dR][b] = ag.dp[ag.dR][b + 1]; 
          } 
          if (ag.dG != 0) {
            aT();
            return;
          } 
          aS();
          return;
        } 
      } 
    } else {
      if (ag.ch == -5) {
        ag.dQ = (short)(ag.dQ + arrayOfByte2[ag.dG] - ag.dP);
        ag.dP = (short)arrayOfByte2[ag.dG];
        ag.dO = 29;
        if (ag.dG != 0) {
          aT();
        } else {
          aS();
        } 
        ag.dS = 3;
        return;
      } 
      String str;
      if ((str = ag.dp[ag.dR][ag.dP].substring(ag.dO)).length() != 0 && str.charAt(0) > '\000') {
        ag.dO = (short)(ag.dO + 1);
        x.a(str.substring(0, 1), ag.dN + ag.db, ag.dM[ag.dR] + 16 * ag.dP + ag.dc, 0);
        ag.dN = (short)(ag.dN + 9);
        return;
      } 
      if (ag.dQ >= ag.dq[ag.dR]) {
        ag.dS = 15;
        return;
      } 
      ag.dS = 1;
    } 
  }
  
  private void aJ() {
    int i = ag.cM[1];
    int j = ag.dd - 52 + ag.db;
    if (0 == i && !ag.aq())
      i = 9; 
    ag.a(j, ag.bZ.b - 65, 116, 21, ag.ct[18], 0, i * 21);
    ag.a(j - 24 - ag.dr % 3 * 2, ag.bZ.b - 65 + 2, 10, 16, ag.ct[17], 0, 0);
    ag.a(j + 116 + 16 + ag.dr % 3 * 2, ag.bZ.b - 65 + 2, 10, 16, ag.ct[17], 10, 0);
    if (ag.dr > 100) {
      ag.dr = 32;
      return;
    } 
    ag.dr++;
  }
  
  private void aK() {
    Image image = null;
    int i = ag.cz.aB - 1 & 0x3;
    x.a(ag.bu);
    byte b;
    for (b = 0; b < 3; b++) {
      String str = ag.M(65 + b);
      b(str, ag.de - 90 - b * 20 + 10, 0);
    } 
    for (b = 0; b < 3; b++) {
      image = d(ag.bB.a(38 + i));
      b(ag.dd - 94 + 69 * b + ag.db, ag.de + 9 + ag.dc, 50, 50, 148, 109, 82);
      a(ag.dd - 93 + 69 * b + ag.db, ag.de + 10 + ag.dc, 48, 48, 33, 0, 0);
      b(image, ag.dd - 92 + 69 * b, ag.de + 11, 46, 46, 0, 0);
      i = i + 1 & 0x3;
    } 
    c(ag.dd - 27 + ag.db + 1, ag.de + 8 + ag.dc, 52, 52, 255, 182, 82);
    f(0, ag.dd - 40, ag.de + 23);
    f(1, ag.dd + 30, ag.de + 23);
  }
  
  private void aL() {
    x.a(ag.bu);
    ag.cy = 0;
    while (ag.cy < 2) {
      b(ag.M(69 + ag.cy), ag.de - 47 + ag.cy * 20, 0);
      ag.cy++;
    } 
  }
  
  private void aM() {
    int i = ag.dd - 80 + ag.db;
    int j = ag.de + 8 + ag.dc;
    x.b(i, j, 160, 20, 0);
    x.a(i, j, 160, 20, ag.k(173, 170, 173));
    x.a(ag.bu);
    x.a(ag.bz.a(), ag.bL, j + 2, 1);
    if (ag.bz.b() == 0) {
      ag.h(-1, 2);
      return;
    } 
    ag.h(-1, 10);
  }
  
  private void O(int paramInt) {
    int[] arrayOfInt1 = { ag.cz.o, ag.cz.q, ag.cz.m, ag.cz.n };
    Image image = null;
    if (paramInt != 0) {
      int[] arrayOfInt = null;
      arrayOfInt = p();
      ag.dZ[0] = (short)(ag.cz.G * 100 / arrayOfInt[0]);
      int i = (image = d(ag.bA.a(26))).getWidth();
      int j = image.getHeight();
      ag.eN = ag.de - j / 2;
      b(image, ag.eM = ag.dd - i / 2, ag.eN, i, j, 0, 0);
      ag.c(ag.cz.k, ag.eM + 110, ag.eN + 6);
      d(ag.cz.l, ag.eM + 152, ag.eN + 34, 0);
      d(ag.cz.F, ag.eM + 152, ag.eN + 61, 0);
    } else {
      int[] arrayOfInt;
      x.b((arrayOfInt = new int[] { ag.eM + 88, ag.eN + 83, 68, 20 }, )[0], arrayOfInt[1], arrayOfInt[2], arrayOfInt[3], 0);
      arrayOfInt[0] = ag.eM + 39;
      arrayOfInt[1] = ag.eN + 108;
      arrayOfInt[2] = 104;
      arrayOfInt[3] = 18;
      for (byte b1 = 0; b1 < 4; b1++) {
        x.b(arrayOfInt[0], arrayOfInt[1], arrayOfInt[2], arrayOfInt[3], 0);
        arrayOfInt[1] = arrayOfInt[1] + 20;
      } 
    } 
    int[] arrayOfInt2 = { ag.cz.u, ag.cz.v, ag.cz.s, ag.cz.t };
    d(ag.cz.J, ag.eM + 152, ag.eN + 86, 0);
    for (byte b = 0; b < 4; b++) {
      int i = d(arrayOfInt1[b], ag.eM + 44, ag.eN + 110 + b * 20, 1);
      if (arrayOfInt2[b] > 0) {
        b(ag.ct[19], i + 1, ag.eN + 110 + b * 20, 10, 14, 105, 0);
        d(arrayOfInt2[b], i + 9, ag.eN + 110 + b * 20, 1);
      } 
    } 
    image = d(ag.bB.a(38 + ag.cz.aB));
    b(image, ag.eM + 2, ag.eN + 3, 46, 46, 0, 0);
    if (ag.cz.J > 0)
      a(ag.eM + 144, ag.eN + 97 + 20 * ag.cM[1] + ag.dc + 11, 14, 18, 255, 255, 255); 
    ag.da = 0;
  }
  
  final void j() {
    int i = 0;
    i = ag.de - 50;
    if (ag.cM[1] == 0)
      ag.cM[1] = 1; 
    for (byte b = 1; b < 3; b++) {
      boolean bool;
      String str;
      byte b1;
      if (ag.cM[1] == b) {
        bool = true;
        x.a(ag.bw);
      } else if (b == 3) {
        bool = false;
        x.a(ag.bx);
      } else {
        bool = false;
        x.a(ag.bu);
      } 
      a(ag.dd - 100, i + ag.dc, 80, 20, bool);
      a(ag.dd - 10, i + ag.dc, 110, 20, bool);
      ag.c(ag.gb[b], ag.dd - 100 + 40 - ag.db, i + 1);
      if (bool == true) {
        f(0, ag.dd - 10 - ag.db, i + 2);
        f(1, ag.dd - 10 + 110 - 10 - 1 - ag.db, i + 2);
      } 
      switch (b) {
        case 0:
          str = ag.gc[ag.df ? 1 : 0];
          break;
        case 1:
          str = "";
          for (b1 = 0; b1 < ag.dg / 25; b1++)
            str = str + 'I'; 
          if (str.equals(""))
            str = "OFF"; 
          break;
        case 2:
          str = ag.ge[ag.dh];
          break;
        case 3:
          str = ae.aX[ag.ep];
          break;
        default:
          return;
      } 
      ag.c(str, ag.dd + 156 - 111 - ag.db, i + 1);
      i += 10;
      i += 20;
    } 
  }
  
  private void P(int paramInt) {
    byte[] arrayOfByte = { 1, 3, 7, 9, 0 };
    if (0 == paramInt)
      for (byte b = 0; b < 5; b++) {
        i(40 + b * 30 + 4 * b, 60);
        d(arrayOfByte[b], 40 + b * 30 + 18 + 4 * b, 70, 0);
      }  
    if (paramInt % 2 == 0) {
      for (byte b = 0; b < 5; b++) {
        i(40 + b * 30 + 4 * b, 90);
        if (ag.cz.V[b] != 0)
          b(ag.ct[37], 40 + b * 30 + 4 * b + 1, 91, 28, 28, (ag.cz.V[b] - 12) * 28, 0); 
      } 
      b(40 + ag.cM[1] * 30 + 4 * ag.cM[1], 90, 30, 30, 255, 255, 255);
    } 
    ac[] arrayOfAc;
    (arrayOfAc = new ac[2])[0] = new ac(40, 140, 60, 20);
    arrayOfAc[1] = new ac(40, 165, 60, 20);
    if (paramInt % 3 == 0) {
      byte b2;
      int i = ag.cM[2] / 6 << 1;
      if (ag.cM[2] < 18) {
        b2 = 2;
      } else {
        b2 = 1;
      } 
      for (byte b1 = 0; b1 < b2; b1++) {
        int j = ag.cM[2] / 6 * 6 + b1 * 3;
        ac ac1;
        (ac1 = arrayOfAc[b1]).b = ac1.b + b1 * 10 + 5;
        b(ac1.a - 1, ac1.b - 1, ac1.c + 2, ac1.d + 2, 152, 152, 152);
        ag.a(ac1, 0);
        x.a(ag.bu);
        ag.dD = ag.c(ag.gd[i + b1]);
        ag.d(ag.gd[i + b1], ac1.a + (ac1.c - ag.dD) / 2, ac1.b + 1);
        for (byte b = 0; b < 3; b++) {
          i(40 + (b + 2) * 34, 140 + 35 * b1);
          if (ae.aC[j + b] != 0) {
            Image image;
            if (ag.cz.W[ae.aC[j + b] - 12] != 0) {
              image = ag.ct[37];
            } else {
              image = ag.ct[38];
            } 
            b(image, 40 + (b + 2) * 34 + 1, 140 + 35 * b1 + 1, 28, 28, (ae.aC[j + b] - 12) * 28, 0);
          } 
        } 
      } 
      if (ag.cM[3] == 2)
        b(40 + (ag.cM[2] % 3 + 2) * 34, 140 + 35 * ag.cM[2] % 6 / 3, 30, 30, 255, 255, 255); 
      ac ac = new ac(210, 0, 3, 20);
      a(210, 150, 3, 50, false);
      if (i == 6) {
        ac.a = 210;
        ac.b = 152;
        ac.c = 3;
        ac.d = 46;
        ag.a(ac, ag.k(231, 227, 198));
      } else {
        ac.b = 151 + (i >> 1) * 14 + ag.dc;
        ag.a(ac, ag.k(231, 227, 198));
      } 
    } 
    System.out.println("GameCanvas.DrawSkillSet(2)");
    if (ag.cM[3] == 1) {
      b(ag.cz.V[ag.cM[1]] + 2000, ag.dd - 100, ag.bZ.b - 70, 200, 22);
    } else {
      b(ae.aC[ag.cM[2]] + 2000, ag.dd - 100, ag.bZ.b - 70, 200, 22);
    } 
    ag.da = 0;
  }
  
  final void k() {
    a(ag.dF.b.a + ag.db, ag.dF.b.b + ag.dc, ag.dF.b.c, ag.dF.b.d, false);
    x.a(ag.bu);
    if (ag.dF.a != 0) {
      ag.dD = ag.c(ag.dF.c);
      ag.dF.d = (short)(ag.dF.d - 5);
      if (ag.dF.b.a - ag.dF.d > ag.dD + 3)
        ag.dF.d = (short)(ag.dF.b.a + ag.dF.b.c); 
    } 
    ag.d(ag.dF.c, ag.dF.d, ag.dF.b.b + (ag.dF.b.d - 11 >> 1) - 2);
    int i = (ag.bJ - ag.dF.b.c) / 2;
    int j = ag.dF.b.b + ag.dc;
    short s1 = 0;
    short s2 = 0;
    if (ag.bV == 3) {
      s1 = ag.db;
      s2 = ag.dc;
      x.b(0, j, i, ag.dF.b.d, 0);
      x.b(ag.bJ - i, j, i, ag.dF.b.d, 0);
    } 
    a(ag.ct[7], 0, j, i, ag.dF.b.d, -s1, j - s2);
    x.c(i - 1, j, i - 1, j + ag.dF.b.d - 1, ag.k(80, 80, 80));
    a(ag.ct[7], ag.bJ - i, j, i - s1, ag.dF.b.d, ag.bJ - i - s1, j - s2);
    x.c(ag.bJ - i, j, ag.bJ - i, j + ag.dF.b.d - 1, ag.k(80, 80, 80));
    if (ag.bV == 3) {
      x.a(0, j, ag.bJ, ag.dF.b.d);
      ag.bd.b();
      x.a();
      x.a(0, j, i - 1, ag.dF.b.d);
      ag.cS.b(170);
      x.a();
      x.a(ag.bJ - i + 1, j, i - 1, ag.dF.b.d);
      ag.cS.b(170);
      x.a();
    } 
  }
  
  private void n(int paramInt1, int paramInt2) {
    byte[] arrayOfByte1 = { -77, -77, -77, -33, 3, 47, 47, 47, -15 };
    byte[] arrayOfByte2 = { 21, -15, -51, -79, -79, -51, -15, 21, 49 };
    ag.ct[39] = d(ag.bA.a(50));
    b(ag.ct[39], ag.dd - ag.ct[39].getWidth() / 2, ag.de - ag.ct[39].getHeight() / 2, ag.ct[39].getWidth(), ag.ct[39].getHeight(), 0, 0);
    ag.ct[39] = null;
    for (byte b = 0; b < 9; b++) {
      if ((ag.cz.X[b]).a != 0) {
        e((ag.cz.X[b]).a);
        g((ag.cz.X[b]).a, ag.dd + arrayOfByte1[b], ag.de + arrayOfByte2[b], 0);
      } 
    } 
    b(ag.dd + arrayOfByte1[paramInt1] - 1, ag.de + arrayOfByte2[paramInt1] - 1, 30, 30, 255, 255, 255);
    ag.fK[24] = ag.dd + arrayOfByte1[paramInt1] + ag.db + 7;
    ag.fK[25] = ag.de + arrayOfByte2[paramInt1] + ag.dc + 7;
    b(ag.cz.aH, ag.dd - (ag.cz.aE[1]).e, ag.de + 7 - (ag.cz.aE[1]).f + 17, (ag.cz.aE[1]).c, (ag.cz.aE[1]).d, (ag.cz.aE[1]).a, (ag.cz.aE[1]).b);
    b(ag.cz.aG, ag.dd - (ag.cz.aC[1]).e, ag.de + 7 - (ag.cz.aC[1]).f + 17, (ag.cz.aC[1]).c, (ag.cz.aC[1]).d, (ag.cz.aC[1]).a, (ag.cz.aC[1]).b);
    if (paramInt2 != 0) {
      ag.a(o(-1), true, -1);
      return;
    } 
    b(paramInt1 + 1000, ag.dd - 79, ag.de + 81 + 5, 158, 20);
  }
  
  private void Q(int paramInt) {
    byte b2;
    byte b3;
    int[] arrayOfInt1 = { ag.dd - 75, ag.dd - 45, ag.dd - 15, ag.dd + 15, ag.dd + 45 };
    int[] arrayOfInt2 = { ag.de - 45, ag.de - 15, ag.de + 15 };
    ac ac = new ac(ag.dd + 80, ag.de - 40, 5, 80);
    if (ag.cM[2] < 15) {
      b2 = 3;
      b3 = 0;
    } else {
      b2 = 2;
      b3 = 15;
    } 
    if (paramInt != 0)
      b(ag.ct[7], ag.dd - 75, ag.de - 45, 150, 100, ag.dd - 75, ag.de - 45); 
    for (byte b1 = 0; b1 < b2; b1++) {
      for (byte b = 0; b < 5; b++) {
        i(arrayOfInt1[b] + ag.db, arrayOfInt2[b1] + ag.dc);
        e((ag.cz.Y[b3 + b1 * 5 + b]).a);
        g((ag.cz.Y[b3 + b1 * 5 + b]).a, arrayOfInt1[b] + 1, arrayOfInt2[b1] + 1, 0);
      } 
    } 
    ag.a(ac, ag.k(148, 148, 148));
    ac.a++;
    ac.b++;
    ac.c -= 2;
    ac.d -= 2;
    ag.a(ac, ag.k(33, 0, 0));
    ac.b = ag.de - 39 + ((b3 != 0) ? 39 : 0) + ag.dc;
    ac.d = 39;
    ag.a(ac, ag.k(231, 227, 198));
    b(ag.cM[2] + 1100, ag.dd - 75, ag.de + 50, 150, 22);
    b(arrayOfInt1[ag.cM[2] % 5], arrayOfInt2[(ag.cM[2] - b3) / 5] + ag.dc, 30, 30, 255, 255, 255);
    if (0 == paramInt)
      J(); 
    ag.da = 0;
  }
  
  private void aN() {
    String[] arrayOfString = { "Name", "Points" };
    int i;
    int j = (i = (ag.bZ.a - 208) / 2 + 2) + 134 + 10;
    int k = ag.bY.b - 20 - 20 + 10;
    int m = 20 + (k - 177) / 2 + 2;
    int n = m;
    int i1 = ag.cM[1] % 4;
    int i2 = ag.cM[1] / 4;
    ag.fp[1] = (short)(i2 + 1);
    i2 *= 4;
    a(i, n, 130, 22, false);
    a(j, n, 60, 22, false);
    x.a(ag.bu);
    ag.b(i + 65, n + 1, arrayOfString[0]);
    ag.b(j + 30, n + 1, arrayOfString[1]);
    n += 31;
    for (byte b = 0; b < 4; b++) {
      boolean bool;
      if (b == i1) {
        bool = true;
        x.a(ag.bw);
      } else {
        bool = false;
        x.a(ag.bu);
      } 
      a(i, n, 130, 22, bool);
      a(j, n, 60, 22, bool);
      if (i2 < ag.cN) {
        String str;
        if (ag.fu != 0) {
          str = ag.fr.b(ag.fn[2][i2] - 1, 0);
        } else {
          str = ag.fr.b(ag.fn[0][i2] - 1, 0);
        } 
        ag.b(i + 65, n + 1, str);
        if (ag.fu != 0) {
          byte b1;
          for (b1 = 0; b1 < ag.fo && ag.fn[2][i2] != ag.fn[0][b1]; b1++);
          if (b1 < ag.fo) {
            str = "" + ag.fn[1][b1];
          } else {
            str = "0";
          } 
        } else {
          str = "" + ag.fn[1][i2];
        } 
        ag.b(j + 30, n + 1, str);
      } 
      i2++;
      n += 31;
    } 
    n += 6;
    a(ag.fp[1], ag.fp[0], n, true);
  }
  
  private void aO() {
    if (ag.dS > 0) {
      ag.dS = (short)(ag.dS - 1);
      if (ag.ch != 0 && ag.dS > 3)
        ag.dS = 3; 
      if (0 == ag.dS) {
        ag.fD++;
        if (ag.fD <= 3) {
          ag.fw[ag.fD & 0x1] = ag.gf[ag.fD - 1];
          ag.fA[ag.fD & 0x1] = 0;
          return;
        } 
        if (ag.fD == 4) {
          ag.cS.e(14);
          ag.fA[1] = 0;
          return;
        } 
        if (ag.fD < 7) {
          ag.fw[ag.fD & 0x1] = ag.gf[ag.fD - 2];
          ag.fA[ag.fD & 0x1] = 0;
          return;
        } 
        ag.fs.a();
        ag.fs = null;
        ag.fr.a();
        ag.fr = null;
        ag.cS.e(16);
        return;
      } 
    } else {
      int i;
      int j;
      if (ag.fD >= 10) {
        ag.fD -= 10;
        i = ag.fD & 0x1;
        ag.fA[i] = ag.fw[i].length();
        j = 0;
      } else {
        i = ag.fD & 0x1;
        j = ag.fA[i];
      } 
      if (ag.fD != 4) {
        a(i, j, 0);
        if (ag.fw[i].length() <= ag.fA[i] + 1) {
          if (ag.ch != 0) {
            ag.dS = 5;
            return;
          } 
          ag.dS = 15;
        } 
      } 
    } 
  }
  
  final void a(int paramInt, z[] paramArrayOfz, int[] paramArrayOfint) {
    int i = ag.fK[8] * 5;
    if (ag.fK[11] == 1) {
      ac ac1 = new ac(0, 0, 0, 0);
      ac ac2 = new ac(0, 0, 0, 0);
      ac1.c = 4;
      ac1.a = ag.fK[12];
      ac1.d = ag.fK[6];
      ac1.b = paramInt;
      ag.a(ac1, 16777215, 0);
      ac1.c -= 2;
      ac1.a++;
      ac1.d -= 2;
      ac1.b++;
      int j = ag.fK[8] * 32;
      int k = ac2.d;
      j = j * k / ag.fK[7];
      ac2.d = ag.fK[13];
      ac2.b += j;
      ag.a(ac2, 16777215);
      ag.b(ac1, 10000536);
    } 
    paramInt++;
    byte b1 = 0;
    byte b2 = 0;
    while (b1 < ag.fK[3]) {
      int j = ag.fK[5];
      for (byte b = 0; b < 5; b++) {
        boolean bool;
        if (i == ag.fK[18]) {
          bool = true;
          ag.fK[24] = j + 13 + 1;
          ag.fK[25] = paramInt + 13 + 1;
        } else {
          bool = false;
        } 
        for (byte b3 = 0; b3 < ag.fO[3]; b3++) {
          if (ag.fO[b3] == i) {
            bool = true;
            (ag.fP[b2]).a = (short)(j + 13 + 1);
            (ag.fP[b2]).b = (short)(paramInt + 13 + 1);
            b2++;
            break;
          } 
        } 
        a(j, paramInt, bool);
        if (paramArrayOfint != null) {
          a(paramArrayOfint[i], j, paramInt, 0);
        } else {
          a(i, j, paramInt, paramArrayOfz);
        } 
        j += 32;
        i++;
      } 
      paramInt += 32;
      b1++;
    } 
  }
  
  private void a(int paramInt1, int paramInt2, int paramInt3, z[] paramArrayOfz) {
    z z1;
    boolean bool;
    if (paramArrayOfz != null) {
      z1 = paramArrayOfz[paramInt1];
    } else {
      z1 = o(paramInt1);
    } 
    if (ag.fK[0] == 1 && z1.a > 0 && z1.a < 100) {
      bool = z1.b;
    } else {
      bool = false;
    } 
    a(z1.a, paramInt2, paramInt3, bool);
  }
  
  final void a(int paramInt1, int paramInt2, boolean paramBoolean) {
    ag.a(paramInt1 + 1, paramInt2 + 1, 26, 26, 0, 0, paramBoolean ? 16777215 : 5263440, true);
  }
  
  final void a(int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    Image image;
    int i;
    if (paramInt1 > 500) {
      image = ag.ct[3];
      i = paramInt1 - 501;
    } else if (paramInt1 > 300) {
      image = ag.ct[2];
      i = ag.bH[1].a(paramInt1 - 301, 7);
    } else if (paramInt1 > 100) {
      image = ag.ct[1];
      i = ag.bH[0].a(paramInt1 - 101, 7);
    } else {
      image = ag.ct[0];
      i = paramInt1 - 1;
    } 
    ag.a(paramInt2, paramInt3, 28, 28, image, i * 28, 0);
    if (paramInt4 > 0)
      ag.a(paramInt2, paramInt3, 9, 12, ag.ct[20], paramInt4 * 9, 0); 
  }
  
  private void aP() {
    int i = ag.fK[1] + 1;
    i(i);
    i += 29;
    a(i, (z[])null, (int[])null);
    ag.a(o(-1), true, -1);
  }
  
  private void c(boolean paramBoolean) {
    // Byte code:
    //   0: iload_1
    //   1: ifeq -> 115
    //   4: getstatic ag.fK : [I
    //   7: bipush #27
    //   9: iaload
    //   10: ifne -> 20
    //   13: aload_0
    //   14: invokespecial aP : ()V
    //   17: goto -> 31
    //   20: aload_0
    //   21: getstatic ag.fK : [I
    //   24: bipush #18
    //   26: iaload
    //   27: iconst_1
    //   28: invokespecial n : (II)V
    //   31: getstatic ag.fK : [I
    //   34: bipush #23
    //   36: iaload
    //   37: iconst_m1
    //   38: if_icmpne -> 115
    //   41: getstatic ag.cS : Ll;
    //   44: getfield b : S
    //   47: ifne -> 115
    //   50: getstatic ag.fK : [I
    //   53: bipush #23
    //   55: iconst_0
    //   56: iastore
    //   57: getstatic ag.ch : I
    //   60: bipush #-5
    //   62: if_icmpne -> 112
    //   65: getstatic ag.cS : Ll;
    //   68: getfield k : S
    //   71: ifne -> 112
    //   74: getstatic ag.fK : [I
    //   77: bipush #21
    //   79: iaload
    //   80: getstatic ag.cz : Ln;
    //   83: getfield E : I
    //   86: if_icmple -> 102
    //   89: getstatic ag.fK : [I
    //   92: bipush #20
    //   94: iconst_4
    //   95: iastore
    //   96: invokestatic aV : ()V
    //   99: goto -> 112
    //   102: getstatic ag.fK : [I
    //   105: bipush #26
    //   107: iconst_0
    //   108: iastore
    //   109: goto -> 115
    //   112: invokestatic bb : ()V
    //   115: getstatic ag.fK : [I
    //   118: bipush #26
    //   120: iaload
    //   121: iconst_m1
    //   122: if_icmpeq -> 421
    //   125: getstatic ag.fK : [I
    //   128: bipush #26
    //   130: iaload
    //   131: iconst_5
    //   132: if_icmpge -> 150
    //   135: aload_0
    //   136: invokespecial aR : ()V
    //   139: getstatic ag.fK : [I
    //   142: bipush #26
    //   144: dup2
    //   145: iaload
    //   146: iconst_1
    //   147: iadd
    //   148: iastore
    //   149: return
    //   150: getstatic ag.fK : [I
    //   153: bipush #26
    //   155: iconst_m1
    //   156: iastore
    //   157: iconst_1
    //   158: putstatic ag.ck : I
    //   161: getstatic ag.fK : [I
    //   164: iconst_0
    //   165: iaload
    //   166: iconst_2
    //   167: if_icmpne -> 177
    //   170: aload_0
    //   171: invokespecial aQ : ()V
    //   174: goto -> 413
    //   177: getstatic ag.fK : [I
    //   180: iconst_0
    //   181: iaload
    //   182: iconst_3
    //   183: if_icmpne -> 413
    //   186: getstatic ag.fK : [I
    //   189: bipush #22
    //   191: iaload
    //   192: ifne -> 352
    //   195: iconst_0
    //   196: istore_2
    //   197: goto -> 218
    //   200: getstatic ag.cz : Ln;
    //   203: getfield Y : [Lz;
    //   206: getstatic ag.fO : [I
    //   209: iload_2
    //   210: iaload
    //   211: aaload
    //   212: invokevirtual a : ()V
    //   215: iinc #2, 1
    //   218: iload_2
    //   219: iconst_3
    //   220: if_icmplt -> 200
    //   223: getstatic ag.cz : Ln;
    //   226: getfield Y : [Lz;
    //   229: getstatic ag.fO : [I
    //   232: iconst_2
    //   233: iaload
    //   234: aaload
    //   235: getstatic ag.fQ : Lz;
    //   238: getfield a : S
    //   241: putfield a : S
    //   244: getstatic ag.cz : Ln;
    //   247: getfield Y : [Lz;
    //   250: getstatic ag.fO : [I
    //   253: iconst_2
    //   254: iaload
    //   255: aaload
    //   256: getstatic ag.fQ : Lz;
    //   259: getfield b : S
    //   262: putfield b : S
    //   265: getstatic ag.cz : Ln;
    //   268: getfield Y : [Lz;
    //   271: getstatic ag.fO : [I
    //   274: iconst_2
    //   275: iaload
    //   276: aaload
    //   277: getstatic ag.fQ : Lz;
    //   280: getfield c : S
    //   283: putfield c : S
    //   286: getstatic ag.cz : Ln;
    //   289: getfield Y : [Lz;
    //   292: getstatic ag.fO : [I
    //   295: iconst_2
    //   296: iaload
    //   297: aaload
    //   298: getstatic ag.fQ : Lz;
    //   301: getfield d : S
    //   304: putfield d : S
    //   307: getstatic ag.cz : Ln;
    //   310: getfield Y : [Lz;
    //   313: getstatic ag.fO : [I
    //   316: iconst_2
    //   317: iaload
    //   318: aaload
    //   319: getstatic ag.fQ : Lz;
    //   322: getfield e : S
    //   325: putfield e : S
    //   328: getstatic ag.cz : Ln;
    //   331: getfield Y : [Lz;
    //   334: getstatic ag.fO : [I
    //   337: iconst_2
    //   338: iaload
    //   339: aaload
    //   340: getstatic ag.fQ : Lz;
    //   343: getfield f : B
    //   346: putfield f : B
    //   349: goto -> 385
    //   352: getstatic ag.fK : [I
    //   355: bipush #31
    //   357: iaload
    //   358: iconst_m1
    //   359: if_icmpeq -> 385
    //   362: getstatic ag.cz : Ln;
    //   365: getfield Y : [Lz;
    //   368: getstatic ag.fK : [I
    //   371: bipush #31
    //   373: iaload
    //   374: aaload
    //   375: invokevirtual a : ()V
    //   378: getstatic ag.fK : [I
    //   381: bipush #31
    //   383: iconst_m1
    //   384: iastore
    //   385: invokestatic bb : ()V
    //   388: getstatic ag.fK : [I
    //   391: bipush #20
    //   393: bipush #9
    //   395: iastore
    //   396: getstatic ag.cz : Ln;
    //   399: dup
    //   400: getfield E : I
    //   403: getstatic ag.fK : [I
    //   406: bipush #21
    //   408: iaload
    //   409: isub
    //   410: putfield E : I
    //   413: aload_0
    //   414: invokevirtual ar : ()I
    //   417: pop
    //   418: invokestatic aV : ()V
    //   421: return
  }
  
  private void aQ() {
    byte[] arrayOfByte1 = { 100, 90, 80, 70, 60, 45, 30, 10, 1 };
    byte[] arrayOfByte2 = { 0, 10, 20, 40, 50, 60, 70, 80, 90 };
    z z = o(-1);
    ag.fK[20] = 2;
    ag.cz.E -= ag.fK[21];
    if (ag.fK[22] == -1) {
      ag.fK[23] = 2;
    } else {
      int i;
      if ((i = C(100) + 1) > arrayOfByte1[z.f]) {
        i = C(100);
        ag.fK[23] = (i <= arrayOfByte2[z.f]) ? 2 : 1;
      } else {
        a(z, 1);
        ag.fK[23] = 0;
      } 
    } 
    if (ag.fK[23] == 2) {
      z.a();
      ag.fK[23] = 1;
    } 
  }
  
  private void o(int paramInt1, int paramInt2) {
    byte[] arrayOfByte1 = { 0, 15, 30, 0, 20 };
    byte[] arrayOfByte2 = { 0, 0, 0, 16, 16 };
    byte[] arrayOfByte3 = { 16, 16, 16, 20, 24 };
    paramInt1 -= arrayOfByte3[ag.fK[26]] >> 1;
    paramInt2 -= arrayOfByte3[ag.fK[26]] >> 1;
    ag.a(paramInt1, paramInt2, arrayOfByte3[ag.fK[26]], arrayOfByte3[ag.fK[26]], ag.fN, arrayOfByte1[ag.fK[26]], arrayOfByte2[ag.fK[26]]);
  }
  
  private void aR() {
    if (ag.fK[0] == 2) {
      o(ag.fK[24], ag.fK[25]);
      return;
    } 
    if (ag.fK[0] == 3)
      for (byte b = 0; b < 3; b++) {
        if ((ag.fP[b]).a > 0 && (ag.fP[b]).b > 0)
          o((ag.fP[b]).a, (ag.fP[b]).b); 
      }  
  }
  
  final void b(int paramInt) {
    a(19 + ag.db + 2, ag.de - 72 + 9 + ag.dc, 46, 46, true);
    if (paramInt > -1)
      a(ag.bB.a(0 + paramInt), 19 + ag.db + 2, ag.de - 73 + 10 + ag.dc, 46, 46, 0, 0); 
    a(ag.bZ.a / 2 + 60 - ag.db, ag.de - 72 + 109 + ag.dc, 46, 46, true);
    a(ag.bB.a(38 + ag.cz.aB), ag.bZ.a / 2 + 60 - ag.db, ag.de - 73 + 110 + ag.dc, 46, 46, 0, 0);
    R(3);
  }
  
  private void R(int paramInt) {
    if ((paramInt & 0x1) != 0)
      a(ag.dd - 60 + 15 + ag.db, ag.de - 73 + 7 + ag.dc, 150, 53, false); 
    if ((paramInt & 0x2) != 0)
      a(ag.dd - 60 + -40 + ag.db, ag.de - 73 + 107 + ag.dc, 150, 53, false); 
  }
  
  private void aS() {
    x.a(ag.bu);
    R((ag.dR != 0) ? 2 : 1);
    if (ag.dR != 0) {
      for (byte b = 0; b < 3; b++)
        ag.c(ag.dL[0] + ag.db, ag.dM[0] + 16 * b + ag.dc, ag.dp[0][b]); 
    } else {
      for (byte b = 0; b < ag.dP; b++) {
        if (ag.dp[0][b] != null)
          ag.c(ag.dL[0] + ag.db, ag.dM[0] + 16 * b + ag.dc, ag.dp[0][b]); 
      } 
      if (ag.dp[0][ag.dP] != null) {
        String str = ag.dp[0][ag.dP].substring(0, Math.min(ag.dO, ag.dp[0][ag.dP].length()));
        ag.c(ag.dL[0] + ag.db, ag.dM[0] + 16 * ag.dP + ag.dc, str);
      } 
    } 
    if (ag.dK > 1)
      if (ag.dR != 0) {
        for (byte b = 0; b < ag.dP; b++) {
          if (ag.dp[1][b] != null)
            ag.c(ag.dL[1] + ag.db, ag.dM[1] + 16 * b + ag.dc, ag.dp[1][b]); 
        } 
        if (ag.dp[1][ag.dP] != null) {
          String str = ag.dp[1][ag.dP].substring(0, Math.min(ag.dO, ag.dp[1][ag.dP].length()));
          ag.c(ag.dL[1] + ag.db, ag.dM[1] + 16 * ag.dP + ag.dc, str);
          return;
        } 
      } else {
        for (byte b = 0; b < 3; b++)
          ag.c(ag.dL[1] + ag.db, ag.dM[1] + 16 * b + ag.dc, ag.dp[1][b]); 
      }  
  }
  
  private void aT() {
    a(54 + ag.db, ag.bY.b - 40 + ag.dc, ag.bY.a - 56, 38, true);
    x.a(ag.bu);
    for (byte b = 0; b < ag.dP; b++)
      ag.c(ag.dL[0] + ag.db, ag.dM[0] + 16 * b + ag.dc, ag.dp[0][b]); 
    String str = ag.dp[0][ag.dP].substring(0, ag.dO);
    ag.c(ag.dL[0] + ag.db, ag.dM[0] + 16 * ag.dP + ag.dc, str);
  }
  
  static boolean a(int paramInt1, int paramInt2, int paramInt3) {
    int i;
    int j;
    int k;
    int m;
    int i1;
    int i2;
    int i3;
    int i4;
    if (paramInt1 == 0) {
      i3 = ag.dd - 60 + 15 + 2 + ag.db;
      i4 = ag.de - 73 + 7 + 2 + ag.dc;
    } else if (paramInt1 == 1) {
      i3 = ag.dd - 60 + -40 + 2 + ag.db;
      i4 = ag.de - 73 + 107 + 2 + ag.dc;
    } else {
      return false;
    } 
    if ((ag.ch == -6 || ag.ch == -5) && 0 == paramInt3) {
      i1 = 1000;
    } else {
      i1 = ag.fA[paramInt1];
    } 
    int n;
    if (!(n = (paramInt2 != i1) ? 0 : paramInt2)) {
      i = i3;
      j = i4;
      i2 = 0;
      m = 0;
      k = 0;
    } else {
      i = ag.fx[paramInt1];
      j = ag.fy[paramInt1];
      i2 = ag.fB[paramInt1];
      m = ag.fC[paramInt1];
      k = ag.fz[paramInt1];
    } 
    x.a(ag.bu);
    while (n <= i1 && n < ag.fw[paramInt1].length()) {
      int i5 = g.b() + g.c();
      if (i == i3 || (((n <= 0) ? 1 : n) - 1 < ag.fw[paramInt1].length() && ag.fw[paramInt1].charAt(((n <= 0) ? 1 : n) - 1) == ' ') || (n - 1 < ag.fw[paramInt1].length() && ag.fw[paramInt1].charAt(n - 1) == ']')) {
        byte b = 0;
        int i6 = 0;
        while (n + b + 1 < ag.fw[paramInt1].length() && ag.fw[paramInt1].charAt(n + b) != ' ' && ag.fw[paramInt1].charAt(n + b) != ']' && ag.fw[paramInt1].charAt(n + b) != ',') {
          i6 += g.b() + g.c();
          b++;
          if (i6 > 146)
            i6 -= g.b() + g.c(); 
        } 
        if (ag.fw[paramInt1].charAt(n + b) == ']')
          k += g.b(); 
        if (i6 + k > 146)
          k += i6; 
      } 
      if ((k += i5) > 146) {
        if (ag.ch != -999 && m == 2)
          break; 
        i = i3;
        k = i5;
        if (m == 0) {
          i2 = n;
        } else if (m != 1 && m == 2) {
          String str = ag.fw[paramInt1].substring(i2, ag.fw[paramInt1].length());
          ag.fw[paramInt1] = str;
          i1 -= i2;
          m = n = 0;
          j = i4;
          k = 0;
          continue;
        } 
        m++;
        j += 16;
      } 
      if (n == 0)
        ag.bb.R(paramInt1 + 1); 
      if (i == i3 && ag.fw[paramInt1].charAt(n) == ' ')
        n++; 
      if (ag.fw[paramInt1].length() >= n + 1) {
        String str;
        x.a(str = ag.fw[paramInt1].substring(n, n + 1), i, j, 0);
      } 
      i += i5;
      n++;
    } 
    if (0 == paramInt3) {
      ag.fA[paramInt1] = n;
      ag.fx[paramInt1] = i;
      ag.fy[paramInt1] = j;
      ag.fz[paramInt1] = k;
      ag.fB[paramInt1] = i2;
      ag.fC[paramInt1] = m;
    } 
    return true;
  }
  
  final void l() {
    if (ag.bV == 3 || ag.bW == 3)
      ag.de -= 30; 
    int i = ag.cM[1] + ae.z[ag.ej];
    byte[] arrayOfByte = d(61, i);
    if (ag.bV == 2) {
      b(arrayOfByte, 190, 0);
      e(ag.dd - 100 + ag.db, ag.de - 90 + ag.dc, 200, 175);
    } else {
      b(arrayOfByte, 190, 0);
      e(ag.dd - 100, ag.de - 70 + ag.dc, 200, 120);
    } 
    x.a(ag.bu);
    for (byte b = 0; b <= ag.dq[0]; b++) {
      if (ag.bV == 2) {
        if (ag.cM[0] == 28 && ag.ej == 8) {
          b(ag.dp[0][b], ag.de - 80 + b * 20 + 3, 30);
          if (ag.cM[1] == 1)
            b("v" + ag.bh, ag.de - 80 + 20 + 3, 30); 
        } else {
          ag.d(ag.dp[0][b], ag.dd - 95 - 1, ag.de - 80 + b * 20 + 3);
        } 
      } else {
        ag.d(ag.dp[0][b], ag.dd - 90 - 1 - ag.db, ag.de - 62 + b * 15);
      } 
    } 
    if (ag.bV == 2) {
      if (ag.bW == 3) {
        a(ag.cM[1] + 1, ae.z[ag.ej + 1] - ae.z[ag.ej], ag.bZ.b - 100, true);
      } else {
        a(ag.cM[1] + 1, ae.z[ag.ej + 1] - ae.z[ag.ej], ag.bZ.b - 35, true);
      } 
    } else {
      a(ag.cM[1] + 1, ae.z[ag.ej + 1] - ae.z[ag.ej], ag.de + 65, true);
    } 
    if (ag.bV == 3 || ag.bW == 3)
      ag.de += 30; 
  }
  
  private void a(int paramInt1, int paramInt2, int paramInt3, boolean paramBoolean) {
    if (paramInt2 == 1)
      return; 
    int i = ag.dd - 25 - 10;
    if (paramInt2 > 1) {
      if (paramInt1 != 1 || paramBoolean == true)
        f(0, i, paramInt3); 
      i += 60;
      if (paramInt1 != paramInt2 || paramBoolean == true)
        f(1, i, paramInt3); 
    } 
    paramInt3 += 2;
    i = (i = ag.dd - (8 + 9 * (((paramInt2 > 9) ? 2 : 1) + ((paramInt1 > 9) ? 2 : 1)) + 2) / 2) + ((paramInt1 > 9) ? 18 : 9);
    e(paramInt1, i, paramInt3 + ag.dc);
    i++;
    if (ag.bW == 3) {
      ag.a(i - ag.db, paramInt3 + 16, 8, 12, ag.ct[20], 90, 0);
    } else {
      ag.a(i - ag.db, paramInt3, 8, 12, ag.ct[20], 90, 0);
    } 
    i += 9 + ((paramInt2 > 9) ? 18 : 9);
    e(paramInt2, i, paramInt3 + ag.dc);
  }
  
  private void aU() {
    int[] arrayOfInt = { ag.dd - 80 + ag.db, ag.de - 60 + ag.dc };
    ag.ep = (short)ag.cM[1];
    byte b;
    for (b = 0; b < 2; b++) {
      boolean bool;
      if (ag.cM[1] == b) {
        x.a(ag.bw);
        bool = true;
      } else {
        x.a(ag.bu);
        bool = false;
      } 
      a(arrayOfInt[0], arrayOfInt[1] + b * 25, 160, 20, bool);
      b(ae.aX[b], arrayOfInt[1] + 1 + b * 25 - 1, 15);
    } 
    x.a(ag.bu);
    a(arrayOfInt[0], ag.de + ag.dc, 160, 80, false);
    for (b = 0; b < 3; b++)
      b(ae.aY[ag.cM[1]][b], ag.de + 10 + b * 20, 17); 
  }
  
  private static void aV() {
    String[] arrayOfString = { "Success", "Fail" };
    String str = "";
    ag.cS.a();
    ag.ck = 1;
    switch (ag.fK[20]) {
      case 0:
        if (ag.fK[19] < 1)
          return; 
        str = l.d();
        break;
      case 11:
        str = l.e();
        break;
      case 1:
        if (ag.fK[22] == 0) {
          str = "1Not possible |to enchant.";
          break;
        } 
        str = "2Price is " + ag.fK[21] + ".If |enchanting fails,|Items can be lost.|Continue?";
        ag.cS.d = 200;
        break;
      case 2:
        if (ag.fK[23] != 0)
          ag.fK[23] = 1; 
        str = "1Enchant|" + arrayOfString[ag.fK[23]];
        break;
      case 3:
        str = "1Fully enchanted.|Not possible|to enchant.";
        break;
      case 4:
        str = "1Not enough Gold";
        break;
      case 5:
        str = "1You cannot|buy anymore.";
        break;
      case 6:
        str = "3Your backpack|is full. Please|empty some items|and try again.";
        break;
      case 7:
        str = "3Please select|3 items to|combine into one.";
        break;
      case 8:
        if (ag.fK[22] == 2) {
          str = "1Not possible.";
          break;
        } 
        str = "2Compounding fee|is " + ag.fK[21] + ".|Selected items|could be lost|when it fails.|Continue?";
        ag.cS.d = 200;
        break;
      case 9:
        str = "1Compounding| " + arrayOfString[ag.fK[22]];
        break;
    } 
    ag.cS.a(str);
  }
  
  private void aW() {
    boolean bool = true;
    if (ag.fK[26] != -1)
      return; 
    switch (ag.ch) {
      case -1:
      case 50:
        if (ag.fK[27] == 0) {
          ag.fK[10] = ag.fK[10] - 1;
        } else {
          ag.fK[18] = ag.fK[18] + 1;
          if (ag.fK[18] + 1 > 8)
            ag.fK[18] = 0; 
        } 
        ag.dF.c = "";
        break;
      case -2:
      case 56:
        if (ag.fK[27] == 0) {
          ag.fK[10] = ag.fK[10] + 1;
        } else {
          ag.fK[18] = ag.fK[18] - 1;
          if (ag.fK[18] - 1 < 0)
            ag.fK[18] = 8; 
        } 
        ag.dF.c = "";
        break;
      case -3:
      case 52:
        if (ag.fK[27] == 0) {
          ag.fK[9] = ag.fK[9] - 1;
          if (ag.fK[9] - 1 < 0) {
            ag.fK[9] = 4;
            ag.fK[10] = ag.fK[10] - 1;
          } 
        } else {
          ag.fK[18] = ag.fK[18] + 1;
          if (ag.fK[18] + 1 > 8)
            ag.fK[18] = 0; 
        } 
        ag.dF.c = "";
        break;
      case -4:
      case 54:
        if (ag.fK[27] == 0) {
          ag.fK[9] = ag.fK[9] + 1;
          if (ag.fK[9] + 1 >= 5) {
            ag.fK[9] = 0;
            ag.fK[10] = ag.fK[10] + 1;
          } 
        } else {
          ag.fK[18] = ag.fK[18] - 1;
          if (ag.fK[18] - 1 < 0)
            ag.fK[18] = 8; 
        } 
        ag.dF.c = "";
        break;
      case -7:
        ag.cM[0] = ae.u[ag.cM[0]];
        ag.cN = ae.v[ag.cM[0]];
        ag.cM[1] = ag.cP[ag.cM[0]];
        ag.cM[2] = ag.cQ[ag.cM[0]];
        ag.ck = 1;
        bool = false;
        ag.ct[39] = null;
        ag.dF.c = "";
        bb();
        break;
      case -5:
      case 53:
        if (ag.fK[0] == 0) {
          bc();
          bool = false;
          aV();
          break;
        } 
        if (ag.fK[0] == 1) {
          if (ag.fK[19] != 0) {
            bd();
            aV();
            break;
          } 
        } else if (ag.fK[0] == 2) {
          be();
          aV();
        } else {
          if (ag.fK[0] == 3 && (o(-1)).a > 100) {
            byte b = 3;
            if (ag.fO[3] > 0)
              for (b = 0; b < ag.fO[3] && ag.fO[b] != ag.fK[18]; b++); 
            if (b < ag.fO[3]) {
              while (b < 2) {
                ag.fO[b] = ag.fO[b + 1];
                b++;
              } 
              ag.fO[3] = ag.fO[3] - 1;
            } else {
              ag.fO[ag.fO[3]] = ag.fK[18];
              ag.fO[3] = ag.fO[3] + 1;
            } 
            if (ag.fO[3] == 3)
              aX(); 
          } 
          break;
        } 
      default:
        bool = false;
        break;
    } 
    if (bool) {
      ba();
      ag.bb.c(true);
    } 
  }
  
  private void aX() {
    int[] arrayOfInt = { 0, 0, 0 };
    int i = 0;
    byte b;
    for (b = 0; b < 3; b++) {
      z z = o(ag.fO[b]);
      byte b1;
      for (b1 = 0; b1 < b && arrayOfInt[b1] <= z.a; b1++);
      for (byte b2 = b; b2 > b1; b2--)
        arrayOfInt[b2] = arrayOfInt[b2 - 1]; 
      arrayOfInt[b1] = z.a;
      i += z.f;
    } 
    a = j.a("/" + ag.bE.a(68));
    if (a != null) {
      int[] arrayOfInt1;
      (arrayOfInt1 = new int[3])[0] = 0;
      arrayOfInt1[1] = 149;
      arrayOfInt1[2] = 298;
      int j = 0;
      int k = 149;
      for (b = 0; b < 3; b++) {
        int[] arrayOfInt2;
        j = (arrayOfInt2 = b(arrayOfInt1[b], arrayOfInt[b], j, k))[0];
        k = arrayOfInt2[1];
        if (0 == arrayOfInt2[2])
          break; 
      } 
      if (b < 3) {
        ag.fK[22] = 2;
        bb();
      } else {
        j += C(k);
        arrayOfInt[0] = S(447 + j);
        ag.fQ = J(arrayOfInt[0]);
        ag.fK[21] = b(ag.fQ) / 4;
        if (arrayOfInt[0] < 500) {
          arrayOfInt[1] = ag.bH[1].a(arrayOfInt[0] - 301, 8);
          arrayOfInt[2] = 15;
        } else {
          arrayOfInt[1] = ag.bH[2].a(arrayOfInt[0] - 501, 7);
          arrayOfInt[2] = 12;
        } 
        arrayOfInt[1] = (200 - arrayOfInt[1]) / 12;
        if (arrayOfInt[1] >= C(101)) {
          ag.fK[22] = 0;
          ag.fQ = a(ag.fQ, i / 3);
        } else {
          ag.fK[22] = 1;
          arrayOfInt[1] = (100 - arrayOfInt[1]) * 10 / arrayOfInt[2];
          ag.fK[31] = (arrayOfInt[1] >= C(101)) ? ag.fO[C(3)] : -1;
        } 
        ag.fK[23] = -1;
      } 
      ag.fK[20] = 8;
      aV();
    } 
    a = null;
  }
  
  private z a(z paramz, int paramInt) {
    byte[] arrayOfByte = { 30, 25, 20, 15, 9, 1 };
    for (byte b = 0; b < paramInt; b++) {
      int i = 0;
      int j = C(101);
      byte b1;
      for (b1 = 0; b1 < 5; b1++) {
        i += arrayOfByte[b1];
        if (j < i)
          break; 
      } 
      j = (b1 + 5) * 10;
      short s = 0;
      for (b1 = 0; b1 < 4; b1++) {
        if (b1 == 0) {
          s = paramz.b;
        } else if (b1 == 1) {
          s = paramz.c;
        } else if (b1 == 2) {
          s = paramz.d;
        } else if (b1 == 3) {
          s = paramz.e;
        } 
        if ((i = s) > 0) {
          if ((i = (i * j / 10 + 50) / 100) == 0)
            i = 1; 
          if (b1 == 0) {
            paramz.b = (short)(paramz.b + i);
          } else if (b1 == 1) {
            paramz.c = (short)(paramz.c + i);
          } else if (b1 == 2) {
            paramz.d = (short)(paramz.d + i);
          } else if (b1 == 3) {
            paramz.e = (short)(paramz.e + i);
          } 
        } 
      } 
      paramz.f = (byte)(paramz.f + 1);
    } 
    return paramz;
  }
  
  private static int S(int paramInt) {
    return a[paramInt * 2] & 0xFF | (a[paramInt * 2 + 1] & 0xFF) << 8;
  }
  
  private int[] b(int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    int[] arrayOfInt;
    (arrayOfInt = new int[3])[0] = paramInt3;
    arrayOfInt[1] = paramInt4;
    byte b;
    int i;
    for (b = 0; b < arrayOfInt[1] && (i = S(paramInt1 + arrayOfInt[0])) != paramInt2; b++)
      arrayOfInt[0] = arrayOfInt[0] + 1; 
    if (b < arrayOfInt[1]) {
      arrayOfInt[1] = arrayOfInt[1] - b;
      b = 0;
      for (i = S(paramInt1 + arrayOfInt[0]); b < arrayOfInt[1] && i == paramInt2; i = S(paramInt1 + arrayOfInt[0] + ++b));
      arrayOfInt[1] = b;
      arrayOfInt[2] = 1;
      return arrayOfInt;
    } 
    arrayOfInt[2] = 0;
    return arrayOfInt;
  }
  
  private boolean aY() {
    if (ag.cM[0] == 24) {
      m();
      if (ag.fK[16] < 3) {
        ag.cS.e(39);
        ag.ck = 1;
        ag.cM[1] = 3;
        return true;
      } 
    } 
    ag.az();
    aZ();
    return true;
  }
  
  private void aZ() {
    ag.fK[0] = ag.cM[0] - 21;
    if (ag.fK[0] == 0 || ag.fK[0] == 1) {
      ag.fK[14] = ag.fK[0] + 1;
    } else {
      ag.fK[14] = 0;
    } 
    if (ag.fK[0] == 3) {
      bb();
      ag.fK[20] = 7;
      aV();
    } 
    m();
    int i = 0;
    char c = '­';
    ag.fK[4] = 5;
    if (ag.fK[0] == 1)
      ag.fK[4] = ag.fK[4] + 1; 
    ag.fK[3] = 5;
    if (ag.fK[3] > 3)
      ag.fK[3] = 3; 
    if (ag.fK[3] < ag.fK[4]) {
      ag.fK[11] = 1;
    } else {
      ag.fK[3] = ag.fK[4];
      ag.fK[11] = 0;
    } 
    ag.fK[6] = ag.fK[3] * 32 - 2;
    i = 72 + ag.fK[6];
    ag.fK[1] = 26 + (243 - i) / 2 + 1;
    i = 158;
    if (ag.fK[11] == 1) {
      c = ' ';
      i = 164;
      ag.fK[7] = 32 * ag.fK[4] - 2;
      ag.fK[13] = ag.fK[6] * (ag.fK[6] - 2) / ag.fK[7] + 1;
    } 
    ag.fK[5] = (240 - i) / 2 + 1;
    ag.fK[12] = ag.fK[5] + c;
    ag.fK[27] = 0;
    ag.fK[8] = 0;
    ag.fK[10] = 0;
    ag.fK[9] = 0;
    ba();
    ag.fK[26] = -1;
  }
  
  private void ba() {
    if (ag.fK[27] == 0) {
      if (ag.fK[10] < 0) {
        ag.fK[10] = ag.fK[4] - 1;
      } else if (ag.fK[10] >= ag.fK[4]) {
        ag.fK[10] = 0;
      } 
      if (ag.fK[10] < ag.fK[8]) {
        ag.fK[8] = ag.fK[10];
      } else if (ag.fK[10] >= ag.fK[8] + ag.fK[3]) {
        ag.fK[8] = ag.fK[10] - ag.fK[3] + 1;
      } 
      ag.fK[18] = ag.fK[10] * 5 + ag.fK[9];
    } 
    z z = o(-1);
    ag.fK[19] = (z != null) ? z.a : 0;
  }
  
  static String c(int paramInt) {
    String str;
    if (paramInt < 100) {
      str = ae.aN[paramInt - 1];
    } else if (paramInt < 300) {
      str = ag.bH[0].b(paramInt - 101, 0);
    } else if (paramInt < 500) {
      str = ag.bH[1].b(paramInt - 301, 0);
    } else {
      str = ag.bH[2].b(paramInt - 501, 0);
    } 
    return str;
  }
  
  private static void bb() {
    byte b;
    for (b = 0; b < ag.fO.length; b++)
      ag.fO[b] = 0; 
    for (b = 0; b < ag.fP.length; b++) {
      if (ag.fP[b] == null)
        ag.fP[b] = new h(); 
      (ag.fP[b]).a = 0;
      (ag.fP[b]).b = 0;
    } 
    if (ag.fQ == null)
      ag.fQ = new z(); 
    ag.fQ.a();
  }
  
  static void m() {
    ag.fK[16] = 0;
    byte b;
    for (b = 0; b < 25; b++) {
      if ((ag.cz.Y[b]).a > 0)
        ag.fK[16] = ag.fK[16] + 1; 
    } 
    ag.fK[17] = 0;
    for (b = 0; b < 5; b++) {
      if ((ag.cz.Z[b]).a > 0)
        ag.fK[17] = ag.fK[17] + 1; 
    } 
  }
  
  private static int b(z paramz) {
    int i;
    if (paramz.a < 100) {
      i = ae.y[paramz.a - 1];
    } else if (paramz.a < 300) {
      i = (i = (i = (i = (i = ag.bH[0].a(paramz.a - 101, 6)) + paramz.b * 100) + paramz.c * 100) + paramz.d / 5 * 100) + paramz.e / 3 * 100;
    } else if (paramz.a < 500) {
      int j = ((j = ag.bH[1].a(paramz.a - 301, 6)) == 0) ? 800 : 400;
      i = (i = (i = (i = paramz.b * j) + paramz.c * j) + paramz.d / 5 * j) + paramz.e / 3 * j;
    } else {
      i = ag.bH[2].a(paramz.a - 501, 6);
    } 
    return i;
  }
  
  private void bc() {
    z z;
    if ((z = ag.fL[ag.fK[18]]).a == 0) {
      ag.fK[20] = -1;
      return;
    } 
    int i = b(z);
    if (ag.cz.E >= i) {
      if (z.a < 100) {
        byte b;
        for (b = 0; b < 5 && (ag.cz.Z[b]).a != z.a; b++);
        if (b < 5) {
          if ((ag.cz.Z[b]).b < 5) {
            (ag.cz.Z[b]).b = (short)((ag.cz.Z[b]).b + 1);
            ag.fK[20] = 0;
          } else {
            ag.fK[20] = 5;
          } 
        } else {
          for (b = 0; b < 5 && (ag.cz.Z[b]).a != 0; b++);
          if (b < 5) {
            (ag.cz.Z[b]).a = z.a;
            (ag.cz.Z[b]).b = 1;
            ag.fK[17] = ag.fK[17] + 1;
            ag.fK[20] = 0;
          } else {
            ag.fK[20] = 6;
          } 
        } 
      } else if (ag.fK[16] < 25) {
        byte b;
        for (b = 0; b < 25 && (ag.cz.Y[b]).a != 0; b++);
        (ag.cz.Y[b]).a = z.a;
        (ag.cz.Y[b]).b = z.b;
        (ag.cz.Y[b]).c = z.c;
        (ag.cz.Y[b]).d = z.d;
        (ag.cz.Y[b]).e = z.e;
        (ag.cz.Y[b]).f = z.f;
        z.a();
        ag.fK[16] = ag.fK[16] + 1;
        ag.fK[20] = 0;
      } else {
        ag.fK[20] = 6;
      } 
    } else {
      ag.fK[20] = 4;
    } 
    if (ag.fK[20] == 0) {
      ag.cz.E -= i;
      ar();
    } 
  }
  
  private void bd() {
    z z;
    if ((z = o(-1)) == null || z.a == 0)
      return; 
    int i = b(z);
    if (z.a < 100) {
      if ((ag.cz.Z[ag.fK[18]]).b > 1) {
        (ag.cz.Z[ag.fK[18]]).b = (short)((ag.cz.Z[ag.fK[18]]).b - 1);
      } else {
        (ag.cz.Z[ag.fK[18]]).a = 0;
        (ag.cz.Z[ag.fK[18]]).b = 0;
        ag.fK[17] = ag.fK[17] - 1;
      } 
    } else {
      z.a();
      ag.fK[16] = ag.fK[16] - 1;
    } 
    ag.fK[20] = 11;
    ag.cz.E += i / 2;
    ar();
  }
  
  private void be() {
    z z;
    if ((z = o(-1)).a == 0) {
      ag.fK[20] = -1;
      return;
    } 
    ag.fK[22] = 0;
    ag.fK[21] = 0;
    if (z.a > 100 && z.a < 500) {
      if (z.a < 300) {
        ag.fK[22] = ag.bH[0].a(z.a - 101, 5);
      } else {
        ag.fK[22] = ag.bH[1].a(z.a - 301, 6);
      } 
      if (ag.fK[22] > 0) {
        ag.fK[21] = z.b * 100;
        ag.fK[21] = ag.fK[21] + z.c * 100;
        ag.fK[21] = ag.fK[21] + z.d * 100 / 5;
        ag.fK[21] = ag.fK[21] + z.e * 100 / 3;
        if (z.f >= ag.fK[22]) {
          ag.fK[22] = 0;
          ag.fK[20] = 3;
          return;
        } 
      } 
    } 
    ag.fK[20] = 1;
    if (ag.fK[22] != 0)
      ag.fK[23] = -1; 
  }
  
  final void n() {
    int i = 0;
    switch (ag.cS.b_) {
      case 11:
        i = p(ag.ea, 0);
        if (0 == i && 0 == ag.cS.e)
          ag.ea = (short)(ag.ea + 1); 
        break;
      case 12:
        i = p(ag.ea, 1);
        if (0 == i && 0 == ag.cS.e)
          ag.ea = (short)(ag.ea + 1); 
        break;
    } 
    if (i != 0 && 0 == ag.cS.e) {
      if (i == 1) {
        ag.dZ[0] = 0;
        ag.dZ[1] = (short)(ag.dZ[1] - 100);
        if (ag.dZ[1] < 0)
          ag.dZ[1] = 0; 
        ag.dZ[2] = (short)(ag.dZ[2] - 100);
        ag.ea = 0;
        ag.cS.e = 1;
        ag.cS.f = 20;
        ag.cS.g = 12;
        ag.cz.l++;
        ag.cz.J += 3;
        ag.cT[0] = "Level Up : Lv " + ag.cz.l;
        ag.cS.l[5] = ag.cT[0];
        ag.cS.j = 1;
        return;
      } 
      if (ag.cS.d > 100)
        ag.cS.d = 16; 
    } 
  }
  
  private int p(int paramInt1, int paramInt2) {
    byte b2;
    int i;
    int[][] arrayOfInt = { { ag.k(115, 142, 140), ag.k(181, 178, 181), 16777215 }, { ag.k(99, 0, 0), ag.k(181, 0, 0), ag.k(247, 73, 0) }, { ag.k(0, 65, 255), ag.k(0, 146, 255), ag.k(0, 255, 173) }, { ag.k(247, 73, 0), ag.k(255, 162, 0), ag.k(255, 223, 0) } };
    ac[] arrayOfAc = new ac[4];
    if (ag.bV == 3)
      ag.dc = (short)(ag.dc - 30); 
    arrayOfAc[0] = new ac(ag.dd - 51, ag.de + 37 + ag.dc + 20, 102, 7);
    arrayOfAc[1] = new ac(ag.dd - 50, ag.de + 37 + ag.dc + 20, ag.dZ[0], 7);
    arrayOfAc[2] = new ac(ag.dd - 50 + ag.dZ[0], ag.de + 37 + ag.dc + 20, ag.dZ[1] - ag.dZ[0], 7);
    arrayOfAc[3] = new ac(ag.dd - 50 + ag.dZ[1], ag.de + 37 + ag.dc + 20, 0, 7);
    if (ag.bV == 3)
      ag.dc = (short)(ag.dc + 30); 
    byte b3 = 0;
    if (paramInt2 != 0) {
      boolean bool = false;
      b2 = 4;
    } else {
      boolean bool = false;
      b2 = 3;
    } 
    if (ag.dZ[paramInt2] + paramInt1 * 4 > ag.dZ[paramInt2 + 1]) {
      i = ag.dZ[paramInt2 + 1] - ag.dZ[paramInt2];
      b3 = 2;
    } else {
      i = paramInt1 * 4;
    } 
    if (ag.dZ[paramInt2] + i > 100) {
      (arrayOfAc[paramInt2 + 2]).c = 100 - ag.dZ[paramInt2];
      b3 = 1;
    } else {
      (arrayOfAc[paramInt2 + 2]).c = i;
    } 
    ag.a(arrayOfAc[0], 0);
    (arrayOfAc[0]).a++;
    (arrayOfAc[0]).c = 100;
    for (byte b1 = 0; b1 < b2; b1++) {
      if ((arrayOfAc[b1]).c > 0)
        for (byte b = 0; b < 3; b++) {
          (arrayOfAc[b1]).b++;
          (arrayOfAc[b1]).d -= 2;
          ag.a(arrayOfAc[b1], arrayOfInt[b1][b]);
        }  
    } 
    return b3;
  }
  
  final void d(int paramInt) {
    if (ag.bV == 3)
      ag.de -= 30; 
    if (0 == paramInt) {
      J();
      x.a(ag.bu);
      for (byte b1 = 0; b1 < 5; b1++) {
        a(ag.dd - 80 + 32 * b1, ag.de - 40 + ag.dc, 30, 22, false);
        if (ag.cz.aa[0] == b1) {
          ag.d(" * ", ag.dd - 80 + 32 * b1 - ag.db, ag.de - 38);
        } else if (ag.cz.aa[1] == b1) {
          ag.d(" # ", ag.dd - 80 + 32 * b1 - ag.db, ag.de - 38);
        } 
      } 
    } 
    for (byte b = 0; b < 5; b++) {
      if (ag.bV == 3) {
        a(ag.dd - 79 + 32 * b, ag.de + 6, 28, 28, false);
        g((ag.cz.Z[b]).a, ag.dd - 79 + 32 * b - ag.db, ag.de + 6 - ag.dc, b);
      } else {
        a(ag.dd - 79 + 32 * b, ag.de - 10, 28, 28, false);
        g((ag.cz.Z[b]).a, ag.dd - 79 + 32 * b - ag.db, ag.de - 10 - ag.dc, b);
      } 
    } 
    if (ag.bV == 3) {
      b(ag.dd - 80 + 32 * ag.cM[1], ag.de + 6, 30, 29, 255, 255, 255);
    } else {
      b(ag.dd - 80 + 32 * ag.cM[1], ag.de - 10, 30, 29, 255, 255, 255);
    } 
    ag.da = 0;
    b(ag.cM[1] + 1200, ag.dd - 80 - ag.db, ag.de + 30, 160, 22);
    a(ag.dd - 80, ag.de + 60 + ag.dc, 160, 22, false);
    x.a(ag.bu);
    b("*,# key Assign", ag.de + 60, 15);
    if (ag.bV == 3)
      ag.de += 30; 
  }
  
  private void g(int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    int i = -1;
    byte b = 0;
    if (paramInt1 > 500) {
      i = paramInt1 - 501;
      b = 3;
    } else if (paramInt1 > 300) {
      i = ag.cY.g;
      b = 2;
    } else if (paramInt1 > 100) {
      i = ag.cX.f;
      b = 1;
    } else if (paramInt1 > 0) {
      i = paramInt1 - 1;
      b = 0;
    } 
    if (i > -1) {
      b(ag.ct[0 + b], paramInt2, paramInt3, 28, 28, i * 28, 0);
      if (paramInt1 < 100)
        i(paramInt2, paramInt3 + 2, (ag.cz.Z[paramInt4]).b); 
    } 
  }
  
  final void a(z paramz, int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, boolean paramBoolean) {
    String str1 = "/ Price: ";
    String str2 = "Price: ";
    if (paramz.a == 0) {
      ag.dF.a();
      ag.dF.b.a = (ag.bJ - 202) / 2 - ag.db;
      ag.dF.b.b = 200;
      ag.dF.b.c = paramInt3 + 2;
      ag.dF.b.d = paramInt4;
      return;
    } 
    if (ag.fK[14] > 0 && paramInt5 == -1)
      paramInt5 = b(paramz); 
    if (paramz.a < 100) {
      String str;
      int i = paramz.a - 1;
      ag.dF.c = ae.aN[i];
      if (ag.fK[14] == 2) {
        if (ag.dF.c.length() > 0)
          ag.dF.c += " / "; 
        ag.dF.c += str2;
        str = ag.n(paramInt5 >> 1);
        ag.dF.c += str;
      } 
      ag.dF.c += " / ";
      if (i < 9) {
        str = "Recover " + ae.aP[i % 3] + "% of total " + ae.aO[i / 3];
      } else {
        str = "Ranged Atk";
      } 
      ag.dF.c += str;
      if (ag.fK[14] == 1) {
        ag.dF.c += str1;
        str = ag.n(paramInt5);
        ag.dF.c += str;
      } 
    } else {
      String str;
      int i;
      if (paramz.a < 300) {
        str = ag.bH[0].b(paramz.a - 101, 0);
        i = ae.w[(paramz.a - 101) % 5];
      } else if (paramz.a < 500) {
        str = ag.bH[1].b(paramz.a - 301, 0);
        i = ag.bH[1].a(paramz.a - 301, 8);
      } else {
        str = ag.bH[2].b(paramz.a - 501, 0);
        i = ag.bH[2].a(paramz.a - 501, 7);
      } 
      if (paramBoolean)
        ag.dF.c += str; 
      if (ag.fK[14] == 2) {
        if (ag.dF.c.length() > 0)
          ag.dF.c += " / "; 
        ag.dF.c += str2;
        str = ag.n(paramInt5 >> 1);
        ag.dF.c += str;
      } 
      if (ag.dF.c.length() > 0)
        ag.dF.c += " / "; 
      if (paramz.a == 434) {
        ag.dF.c += " / Hp 5 Increased".substring(3, " / Hp 5 Increased".length());
      } else if (paramz.a == 435) {
        ag.dF.c += " / MP 3 Increased".substring(3, " / MP 3 Increased".length());
      } else if (paramz.a == 436) {
        ag.dF.c += " / DEF 1 Increased".substring(3, " / DEF 1 Increased".length());
      } else if (paramz.a == 437) {
        ag.dF.c += " / ATK 1 Increased".substring(3, " / ATK 1 Increased".length());
      } else if (paramz.a == 502) {
        ag.dF.c += " / Catherine's scarf".substring(3, " / Catherine's scarf".length());
      } else if (paramz.a == 504) {
        ag.dF.c += " / all General Visiting".substring(3, " / all General Visiting".length());
        if (paramz.f > 0) {
          str = " / Enchanted Lv" + paramz.f;
          ag.dF.c += str;
        } 
      } else {
        if (paramz.b > 0) {
          str = "Atk+" + paramz.b + " ";
          ag.dF.c += str;
        } 
        if (paramz.c > 0) {
          str = "Def+" + paramz.c + " ";
          ag.dF.c += str;
        } 
        if (paramz.d > 0) {
          str = "HP+" + paramz.d + " ";
          ag.dF.c += str;
        } 
        if (paramz.e > 0) {
          str = "MP+" + paramz.e + " ";
          ag.dF.c += str;
        } 
        if (paramz.f > 0) {
          str = "/ Enchanted Lv" + paramz.f + " ";
          ag.dF.c += str;
        } 
        if (i > 0) {
          str = "/ Available at Lv" + i + " ";
          ag.dF.c += str;
        } 
      } 
      if (ag.fK[14] == 1) {
        ag.dF.c += str1;
        str = ag.n(paramInt5);
        ag.dF.c += str;
      } 
    } 
    ag.dF.b.a = (ag.bJ - 202) / 2 - ag.db;
    ag.dF.b.b = 200;
    ag.dF.b.c = paramInt3 + 2;
    ag.dF.b.d = paramInt4;
    ag.dD = ag.c(ag.dF.c);
    if (ag.dD > paramInt3 - 2) {
      ag.dF.a = 1;
      if (ag.ch != -999) {
        ag.dF.d = (short)(ag.dF.b.a + ag.dF.b.c);
        return;
      } 
    } else {
      ag.dF.a = 0;
      ag.dF.d = (short)(paramInt1 + 1);
    } 
  }
  
  final void o() {
    short[][][] arrayOfShort = { { { 500, 800, 900, 960, 990, 995, 998 }, { 60, 61, 91, 92, 392, 892, 992 }, { 100, 600, 900, 930, 990, 995, 996 }, { 1, 2, 5, 305, 310, 410, 910 } }, { { 1, 101, 106, 606, 609, 610, 910 }, { 30, 31, 91, 92, 592, 892, 992 }, { 300, 360, 860, 960, 961, 991, 996 }, { 1, 2, 5, 10, 40, 100, 200 } } };
    if (C(100) < ag.fn[1][ag.fH]) {
      int i = C(1000);
      ag.fJ = 0;
      while (ag.fJ < 7 && i >= arrayOfShort[ag.dC.f][ag.fI][ag.fJ])
        ag.fJ = (short)(ag.fJ + 1); 
      ag.cS.l[4] = "";
      switch (ag.fJ) {
        case 0:
          i = p(0);
          if (ag.cz.W[i - 1] < 10) {
            String str = ag.e(54, i - 1);
            ag.cz.W[i - 1] = ag.cz.W[i - 1] + 1;
            if (ag.cz.W[i - 1] == 1) {
              ag.cS.l[4] = "Skill :";
              ag.cT[0] = str;
              return;
            } 
            ag.cS.l[4] = "Skill up :";
            ag.cT[0] = str;
            return;
          } 
          break;
        case 1:
          if (ag.cz.m < 10000) {
            ag.cz.m++;
            ag.cT[0] = ae.aR[0];
            return;
          } 
          break;
        case 2:
          if (ag.cz.n < 10000) {
            ag.cz.n++;
            ag.cT[0] = ae.aR[1];
            return;
          } 
          break;
        case 3:
          if (ag.cz.o < 25000) {
            ag.cz.o += 5;
            ag.cT[0] = ae.aR[2];
            return;
          } 
          break;
        case 4:
          if (ag.cz.q < 20000) {
            ag.cz.q += 3;
            ag.cT[0] = ae.aR[3];
            return;
          } 
          break;
        case 5:
          ag.cz.F += 10;
          ag.cT[0] = ae.aR[4];
          return;
        case 6:
          if (k(ag.bc.P(4), 1) != 0) {
            ag.cT[0] = ag.cX.a;
            ag.cS.l[4] = "Item Acquired!";
            return;
          } 
          break;
        default:
          if (k((i = C(11)) + 1, 1) != 0) {
            ag.cT[0] = ae.aN[i];
            ag.cS.l[4] = "Item Acquired!";
            return;
          } 
          break;
      } 
    } 
    ag.fJ = 8;
  }
  
  private void bf() {
    short s = ag.cK;
    if (ag.ct[27] == null)
      F(); 
    int[] arrayOfInt1 = { ag.dd - 44 + 0, ag.dd - 44 + 0, ag.dd - 44 + 0, ag.dd - 44 + 0 };
    int[] arrayOfInt2 = { 164, 180, 188, 166 };
    int[] arrayOfInt3 = { ag.dd - 44 + 0, ag.dd - 44 + 0, ag.dd - 44 + 0, ag.dd - 44 + 0 };
    int[] arrayOfInt4 = { 244, 230, 220, 244 };
    int[] arrayOfInt5 = { ag.dd - 63 - 5 + 0, ag.dd - 63 - 5 + 0, ag.dd - 63 - 5 + 0, ag.dd - 63 - 5 + 0 };
    int[] arrayOfInt6 = { 200, 232, 185, 204 };
    int i = ag.dd - 60;
    if (ag.ck == 2)
      if (ag.cL == 1) {
        int j = arrayOfInt1[1];
        arrayOfInt1[1] = arrayOfInt1[2];
        arrayOfInt1[2] = j;
        j = arrayOfInt2[1];
        arrayOfInt2[1] = arrayOfInt2[2];
        arrayOfInt2[2] = j;
        j = arrayOfInt3[1];
        arrayOfInt3[1] = arrayOfInt3[2];
        arrayOfInt3[2] = j;
        j = arrayOfInt4[1];
        arrayOfInt4[1] = arrayOfInt4[2];
        arrayOfInt4[2] = j;
        j = arrayOfInt5[1];
        arrayOfInt5[1] = arrayOfInt5[2];
        arrayOfInt5[2] = j;
        j = arrayOfInt6[1];
        arrayOfInt6[1] = arrayOfInt6[2];
        arrayOfInt6[2] = j;
        ag.cK = (short)(ag.cK + 1);
        if (ag.cK == 3) {
          ag.cM[1] = ag.cM[1] + 1;
          if (ag.cM[1] + 1 >= ag.cN - 1) {
            ag.cM[2] = 0;
            ag.cM[1] = 0;
          } 
          ag.I();
        } else if (ag.cK > 3) {
          ag.ck = 0;
          ag.cL = 0;
          ag.cK = 0;
        } 
      } else if (ag.cL == -1) {
        ag.cK = (short)(ag.cK + 1);
        if (ag.cK == 3) {
          ag.cM[1] = ag.cM[1] - 1;
          if (ag.cM[1] - 1 < 0)
            ag.cM[1] = ag.cN - 1 - 1; 
          ag.I();
        } else if (ag.cK > 3) {
          ag.ck = 0;
          ag.cL = 0;
          ag.cK = 0;
        } 
      }  
    a(ag.ct[7], 0, 0, ag.bZ.a, ag.bZ.b, 0, 0);
    b(ag.fT[ag.cM[0]], 2 - ag.dc, 0);
    if (ag.gl == null || ag.gm != ag.cM[1]) {
      ag.gl = d(ag.bA.a(66 + ag.cM[1]));
      ag.gm = ag.cM[1];
    } 
    if (ag.gl != null)
      ag.a(i, 60, 117, 90, ag.gl, 0, 0); 
    ag.a(arrayOfInt1[s], arrayOfInt2[s], 89, 20, ag.ct[27], 0, 0);
    ag.a(arrayOfInt1[s] + 22, arrayOfInt2[s] + 5, 62, 11, ag.ct[29], 0, 11 * ((ag.cM[1] == 0) ? 4 : (ag.cM[1] - 1)));
    ag.a(arrayOfInt3[s], arrayOfInt4[s], 89, 20, ag.ct[27], 0, 0);
    ag.a(arrayOfInt3[s] + 22, arrayOfInt4[s] + 5, 62, 11, ag.ct[29], 0, 11 * ((ag.cM[1] == 4) ? 0 : (ag.cM[1] + 1)));
    ag.a(arrayOfInt5[s], arrayOfInt6[s], 127, 29, ag.ct[26], 0, 0);
    ag.a(arrayOfInt5[s] + 22 + 2, arrayOfInt6[s] + 5 + 1, 94, 18, ag.ct[28], 0, 18 * ag.cM[1]);
    if (ag.ck != 2 && ag.cK == 0) {
      ag.a(ag.dd - 5 + ag.db, arrayOfInt6[s] - 6 - 5 - ag.dr % 3 * 2, 16, 10, ag.ct[17], 20, 0);
      ag.a(ag.dd - 5 + ag.db, arrayOfInt6[s] + 29 + ag.dr % 3 * 2, 16, 10, ag.ct[17], 20, 10);
    } 
    if (ag.dr > 100) {
      ag.dr = 32;
    } else {
      ag.dr++;
    } 
    ag.h(-1, 2);
  }
  
  private boolean bg() {
    if (ag.fu != 0) {
      j = 2;
      byte b;
      for (b = 0; b < ag.fo && ag.fn[0][b] != ag.fn[2][ag.cM[1]]; b++);
      ag.fH = (short)b;
      ag.fv = (short)ag.cM[1];
    } else {
      j = 0;
      ag.fH = (short)ag.cM[1];
    } 
    int i = ag.fn[j][ag.cM[1]] - 1;
    B(ag.fn[j][ag.cM[1]]);
    ag.ft = ag.fr.b(i, 0);
    int j = ag.fr.a(i, 9);
    int k = ag.fr.a(i, 8);
    i = ag.fn[1][ag.fH];
    ag.fE = k;
    ag.fF = j;
    if (a(i, j)) {
      ag.fw[0] = "";
      ag.fw[1] = ag.gf[0];
      ag.fA[1] = 0;
      ag.fA[0] = 0;
      ag.fD = 1;
      return true;
    } 
    return false;
  }
  
  static boolean a(int paramInt1, int paramInt2) {
    if (ag.fs != null) {
      ag.fs.a();
      ag.fs = null;
    } 
    ag.fs = new al("/" + ag.bE.a(62));
    if (paramInt1 >= 0 && paramInt1 <= 100 && ag.fs != null) {
      byte b1;
      byte b2;
      if (paramInt2 < 2) {
        if (paramInt1 > 99)
          paramInt1 = 99; 
        paramInt1 = paramInt1 / 10 * 3;
        if (paramInt2 == 1)
          paramInt1 += 30; 
        b1 = 3;
        b2 = 0;
      } else {
        paramInt1 = 60 + (paramInt2 - 2 << 1);
        b1 = 2;
        b2 = 3;
      } 
      for (byte b3 = 0; b3 < b1; b3++) {
        if (ag.fs.a(paramInt1).length() > 0) {
          String str = ((b3 & 0x1) != 0) ? ag.ft : ag.cz.k;
          ag.gf[b3 + b2] = "[" + str + "] " + ag.fs.a(paramInt1) + " ";
          paramInt1++;
        } else {
          return false;
        } 
      } 
      return true;
    } 
    return false;
  }
  
  static int b(int paramInt1, int paramInt2) {
    byte b;
    for (b = 0; b < ag.fo && ag.fn[0][b] != paramInt1; b++);
    if (b == ag.fo) {
      if (paramInt2 > 0) {
        d d = new d("/" + ag.bE.a(52));
        for (byte b1 = 0; b1 < 44; b1++) {
          int i;
          if ((i = d.a(b1, 0)) == paramInt1) {
            ag.fn[0][b] = (short)paramInt1;
            ag.fo = (short)(ag.fo + 1);
            ag.fn[1][b] = (short)(ag.fn[1][b] + paramInt2);
            break;
          } 
        } 
      } 
    } else {
      ag.fn[1][b] = (short)(ag.fn[1][b] + paramInt2);
      if (ag.fn[1][b] > 200 || 0 == ag.fn[1][b]) {
        while (b < ag.fo) {
          ag.fn[0][b] = ag.fn[0][b + 1];
          ag.fn[1][b] = ag.fn[1][b + 1];
          b++;
        } 
        ag.fo = (short)(ag.fo - 1);
      } else if (ag.fn[1][b] >= 100) {
        ag.fn[1][b] = 100;
        return 1;
      } 
    } 
    return 0;
  }
  
  final void e(int paramInt) {
    byte[] arrayOfByte = new byte[16];
    if (paramInt < 100)
      return; 
    if (paramInt < 300) {
      if (ag.cU == null)
        ag.cU = ag.v(47); 
      int i = 9 + (paramInt - 101) * 23;
      byte b;
      for (b = 0; b < 15; b++) {
        arrayOfByte[b] = ag.cU[i + b];
        if (arrayOfByte[b] == 0)
          break; 
      } 
      ag.cX.a = ag.a(arrayOfByte, 0, b);
      ag.cX.b = (short)ag.cU[i + 15];
      ag.cX.c = (short)ag.cU[i + 15 + 1];
      ag.cX.d = (short)ag.cU[i + 15 + 2];
      ag.cX.e = (short)ag.cU[i + 15 + 3];
      ag.cX.f = (short)ag.cU[i + 22];
      if (ag.bV != 2) {
        ag.cU = null;
        return;
      } 
    } else if (paramInt < 500) {
      if (ag.cV == null)
        ag.cV = ag.v(51); 
      int i = 10 + (paramInt - 301) * 24;
      byte b;
      for (b = 0; b < 15; b++) {
        arrayOfByte[b] = ag.cV[i + b];
        if (arrayOfByte[b] == 0)
          break; 
      } 
      ag.cY.a = ag.a(arrayOfByte, 0, b);
      ag.cY.b = ag.cV[i + 15];
      ag.cY.c = ag.a(ag.cV[i + 16], ag.cV[i + 17]);
      ag.cY.d = ag.cV[i + 18];
      ag.cY.e = (short)(ag.cV[i + 19] & 0xFF);
      ag.cY.f = ag.cV[i + 20];
      ag.cY.g = ag.cV[i + 22];
      ag.cY.h = (short)(ag.cV[i + 23] & 0xFF);
      if (ag.bV != 2) {
        ag.cV = null;
        return;
      } 
    } else {
      if (ag.cW == null)
        ag.cW = ag.v(49); 
      int i = 9 + (paramInt - 501) * 27;
      byte b;
      for (b = 0; b < 15; b++) {
        arrayOfByte[b] = ag.cW[i + b];
        if (arrayOfByte[b] == 0)
          break; 
      } 
      ag.cZ.a = ag.a(arrayOfByte, 0, b);
      ag.cZ.b = ag.cW[i + 15];
      ag.cZ.c = ag.a(ag.cW[i + 16], ag.cW[i + 17]);
      ag.cZ.d = ag.cW[i + 18];
      ag.cZ.e = ag.a(ag.cW[i + 19], ag.cW[i + 20]);
      ag.cZ.f = ag.cW[i + 21];
      ag.cZ.g = (short)(ag.cW[i + 26] & 0xFF);
      if (ag.bV != 2)
        ag.cW = null; 
    } 
  }
  
  private void T(int paramInt) {
    if (ag.cz.J > 0) {
      boolean bool1;
      boolean bool2;
      boolean bool3;
      if (paramInt != 0) {
        bool1 = bool2 = bool3 = true;
      } else {
        bool1 = bool2 = bool3 = false;
      } 
      a(ag.eM + 144, ag.eN + 97 + 20 * ag.cM[1] + 11, 14, 18, bool1, bool2, bool3);
    } 
  }
  
  final int[] p() {
    byte[] arrayOfByte = null;
    int i = 0;
    int j = 40;
    arrayOfByte = ag.v(45);
    if (ag.cz.l > 190)
      j = 200 - ag.cz.l << 2; 
    int k;
    int[] arrayOfInt = new int[k = j / 4];
    i = 4 * (ag.cz.l - 1) + 2;
    for (byte b = 0; b < k; b++)
      arrayOfInt[b] = (arrayOfByte[i + b * 4 + 3] & 0xFF) << 24 | (arrayOfByte[i + b * 4 + 2] & 0xFF) << 16 | (arrayOfByte[i + b * 4 + 1] & 0xFF) << 8 | arrayOfByte[i + b * 4] & 0xFF; 
    return arrayOfInt;
  }
  
  private static boolean bh() {
    ag.fp[0] = (short)((ag.cN - 1) / 4 + 1);
    if (ag.fr == null)
      ag.fr = new d("/" + ag.bE.a(46)); 
    return false;
  }
  
  private void bi() {
    int i = 0;
    ag.cg = ag.ds[ag.dk];
    ag.dl = ag.dt[ag.dk];
    byte[] arrayOfByte1 = ag.v(50);
    ag.cN = ag.dv[ag.dk];
    i = 11 * ag.du[ag.dk] + 11;
    byte[] arrayOfByte2 = ag.v(55);
    for (byte b = 0; b < ag.cN; b++) {
      if (ag.dz[b] == null)
        ag.dz[b] = new an(); 
      (ag.dz[b]).a = ag.b(arrayOfByte1[i]);
      (ag.dz[b]).b = ag.b(arrayOfByte1[i + 1]);
      (ag.dz[b]).c = ag.b(arrayOfByte1[i + 2]);
      (ag.dz[b]).d = ag.b(arrayOfByte1[i + 3]);
      (ag.dz[b]).e = ag.b(arrayOfByte1[i + 4]);
      (ag.dz[b]).f = ag.b(arrayOfByte1[i + 5]);
      (ag.dz[b]).g = ag.b(arrayOfByte1[i + 6]);
      (ag.dz[b]).h = ag.b(arrayOfByte1[i + 7]);
      (ag.dz[b]).i = (short)(arrayOfByte1[i + 8] & 0xFF | arrayOfByte1[i + 9] & 0xFF00);
      (ag.dz[b]).j = ag.b(arrayOfByte1[i + 10]);
      i += 11;
      int j = 3 + ((ag.dz[b]).a - 1) * 15;
      byte b1 = 14;
      for (byte b2 = 0; b2 < 14; b2++) {
        if (arrayOfByte2[j + b2] == 0) {
          b1 = b2;
          break;
        } 
      } 
      ag.dA[b] = ag.a(arrayOfByte2, j, j + b1);
      ag.dB[b] = (short)arrayOfByte2[17 + ((ag.dz[b]).a - 1) * 15];
    } 
    ag.dE = ag.dA;
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\e.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */