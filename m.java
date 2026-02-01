import javax.microedition.rms.RecordStore;

final class m extends as implements s {
  public final void a() {
    if (as.hq) {
      ag.bb.e();
      if (as.hn != null) {
        x.a(ag.bu);
        ag.b(ag.bJ / 2, 2, as.hn);
      } 
      as.hq = false;
    } 
    switch (as.ho) {
      case 1:
        bj();
        break;
      case 2:
        bk();
        break;
      case 3:
        bu();
        break;
      case 4:
        bv();
        break;
      case 5:
        bq();
        break;
      case 6:
        br();
        break;
      case 7:
        bs();
        break;
      case 8:
        bt();
        break;
      case 9:
        bl();
        break;
      case 10:
        bm();
        break;
      case 11:
        bn();
        break;
      case 12:
        bo();
        break;
      case 13:
        bp();
        break;
    } 
    if (ag.cS.b != 0)
      ag.cS.c(); 
  }
  
  private void bj() {
    aD();
    ag.h(-1, 2);
  }
  
  private void bk() {
    c("Local", 85);
    i(108);
    ag.a(85, 138, 70, 21, ag.ct[7], 45, 138);
    if (as.ht[15] == 0) {
      ag.a(85, 138, 30, 21, as.r, 0, 0);
      ag.a(126, 139, 28, 19, as.r, 30, 18);
    } else {
      ag.a(86, 139, 28, 19, as.r, 30, 0);
      ag.a(125, 138, 30, 21, as.r, 0, 20);
    } 
    c("Server", 167);
    c(as.gy, 190);
    ag.h(-1, 2);
  }
  
  private void bl() {
    String[] arrayOfString = { "Enter your selling", "price. " + as.ht[4] + "% of total", "will go to taxes." };
    String str1 = "EnchantLv";
    byte b1 = 101;
    x.a(ag.bu);
    for (byte b2 = 0; b2 < 3; b2++) {
      as.a(arrayOfString[b2], 0, b1, 240);
      b1 += 13;
    } 
    as.a(as.hi, 39, 180, false);
    c(71, 183, 130, 17);
    x.a(ag.bu);
    e.c(as.hi);
    String str2 = null;
    as.a(str2 = str1 + as.gR, 141, 180, 0);
    a(45, 210, 150, 22);
    x.a(ag.bv);
    as.a(ag.n(as.hv[14]), 0, 212, 240);
    ag.a(ag.cz.Y[ag.fK[18]], true, -1);
    ag.dF.b.b = 155 - ag.dc;
    ag.bb.k();
    ag.h(7, 2);
  }
  
  private void bm() {
    ag.h(-1, 2);
    i(83);
    int i = 42;
    for (byte b = 0; b < 5; b++) {
      as.a((as.gz[b]).a, i, 115, (b == as.hk));
      i += 32;
    } 
    i = b(160, 200, 48);
    if ((as.gz[as.hk]).a > 0) {
      x.a(ag.bu);
      String str;
      as.a(str = e.c((as.gz[as.hk]).a), i, 164, 200);
      as.a(str = "Price " + ag.n(as.gB[as.hk]), i, 178, 200);
      ag.a(as.gz[as.hk], false, -1);
    } 
  }
  
  private void bn() {
    String[] arrayOfString1 = { "Listed Items", "has been sold." };
    String[] arrayOfString2 = { "Listed Items", "has been recieved." };
    String str = (as.gD == 0) ? arrayOfString1[0] : arrayOfString2[0];
    x.a(ag.bu);
    as.a(str, 0, 100, 240);
    as.a(str = (as.gD == 0) ? arrayOfString1[1] : arrayOfString2[1], 0, 113, 240);
    int i = 42;
    for (byte b = 0; b < 5; b++) {
      as.a((as.gz[b]).a, i, 130, (b == as.hk));
      i += 32;
    } 
    i = b(166, 150, 45) + 25;
    if ((as.gz[as.hk]).a > 0) {
      x.a(ag.bu);
      if (as.gD == 0) {
        as.a(e.c((as.gz[as.hk]).a), i, 170, 100);
        as.a("Price " + ag.n(as.gB[as.hk]), i, 183, 100);
        as.a("EnchantLv " + (as.gz[as.hk]).f, i, 196, 100);
        return;
      } 
      as.a(as.gC[as.hk], i, 170, 100);
      as.a(e.c((as.gz[as.hk]).a), i, 183, 100);
      ag.a(as.gz[as.hk], false, -1);
      ag.bb.k();
    } 
  }
  
  private static void bo() {
    if (ag.cS.b == 0 && !as.gu && as.j++ > 10) {
      as.gt = 3;
      ag.cS.d(29);
      as.j = 0;
    } 
  }
  
  private void bp() {
    byte b1;
    int j;
    boolean bool;
    byte b2;
    int i = ag.bK / 2 - 45;
    switch (as.k) {
      case 0:
        x.a(ag.bu);
        x.a("Please enter", ag.bJ / 2, i, 1);
        x.a("your password.", ag.bJ / 2, i + 15, 1);
        x.a("(4-12 numbers)", ag.bJ / 2, i + 30, 1);
        x.b(ag.bJ / 2 - 65, i + 65, 130, 20, 13421772);
        x.a(ag.bv);
        x.a(as.l, ag.bJ / 2, i + 67, 1);
        if (as.gE && as.i++ > 2) {
          as.k = 1;
          ag.cS.d(29);
          as.i = 0;
          as.gE = false;
        } 
        a(ag.ct[7], 0, ag.bK - 20, ag.bJ, 20, 0, ag.bK - 20);
        b1 = 2;
        if (as.l.length() > 0)
          b1 = 10; 
        if (as.l.length() >= 4) {
          ag.h(8, b1);
          return;
        } 
        ag.h(-1, b1);
        return;
      case 1:
        if (ag.cS.b == 0) {
          as.gE = false;
          x.a(ag.bu);
          x.a("In order to access", ag.bJ / 2, i - 30, 1);
          x.a("Gamevil Live", ag.bJ / 2, i - 10, 1);
          x.a("you must register first.", ag.bJ / 2, i + 10, 1);
          x.a("Please enter a UserID.", ag.bJ / 2, i + 30, 1);
          x.a("(4-12 characters)", ag.bJ / 2, i + 50, 1);
          x.b(ag.bJ / 2 - 60, i + 70, 120, 20, 13421772);
          x.a(ag.bv);
          x.a(ag.bz.a(), ag.bJ / 2, i + 72, 1);
          ag.f(ag.bP, i + 90);
        } 
        a(ag.ct[7], 0, ag.bK - 20, ag.bJ, 20, 0, ag.bK - 20);
        bool = ((j = ag.bz.b()) >= 4 && j <= 12) ? true : true;
        b2 = (j == 0) ? 2 : 10;
        ag.h(bool, b2);
        break;
    } 
  }
  
  private void bq() {
    i(as.hv[15]);
    bj();
  }
  
  private void br() {
    int i = 20 + (255 - 64 + ag.fK[6] >> 1);
    i(i);
    i += 32;
    c(as.hw[as.gP], i);
    i += 32;
    ag.bb.a(i, (z[])null, as.gF[as.gP]);
    ag.h(-1, 2);
  }
  
  private void bs() {
    int j = 0;
    i(47);
    int i = b(89, 200, 32);
    x.a(ag.bu);
    as.a(as.hw[as.gP], i, 99, 167);
    as.a(as.gF[as.gP][as.gQ], i + 167, 91, false);
    j = 131;
    byte b1 = 0;
    byte b2 = 0;
    while (b1 < 2) {
      i = 32;
      byte b = 0;
      while (b < 5) {
        as.a(0, i, j, (b2 == as.gR));
        x.a(as.s, i + 1, j + 8, 0);
        h(b2, i + 27, j + 6);
        as.a(0, i, j + 28 + 1, (b2 == as.gR));
        h(as.hu[15 - b2] / 10, i + 13, j + 28 + 8);
        h(as.hu[15 - b2] % 10, i + 22, j + 28 + 8);
        i += 37;
        b++;
        b2++;
      } 
      j += 60;
      b1++;
    } 
    ag.h(-1, 2);
  }
  
  private void bt() {
    int j = 20 + (255 - 84 + ag.fK[6] + 10 + 32 >> 1);
    i(j);
    j += 42;
    int i = b(j, 200, 32);
    x.a(ag.bu);
    as.a(as.hw[as.gP], i, j + 10, 157);
    i += 157;
    as.a(as.hi, i - 15, j + 9 - 7, false);
    if (as.gP != 2) {
      x.a(as.s, i + 28 - 14, j + 11, 0);
      h(as.gR, i + 28 + 14, j + 9);
    } 
    j += 42;
    ag.bb.a(j, as.gz, (int[])null);
    ag.fK[14] = 1;
    ag.a(as.gz[ag.fK[18]], true, as.gB[ag.fK[18]]);
    ag.bb.k();
    ag.h(-1, 2);
  }
  
  static boolean b() {
    try {
      RecordStore recordStore;
      return !((recordStore = RecordStore.openRecordStore("gamevil_pow_regist", true)).getNumRecords() == 0);
    } catch (Exception exception) {
      return false;
    } 
  }
  
  static void c() {
    byte[] arrayOfByte1 = new byte[28];
    byte[] arrayOfByte2 = as.l.getBytes();
    byte b;
    for (b = 0; b < arrayOfByte2.length; b++)
      arrayOfByte1[b] = arrayOfByte2[b]; 
    arrayOfByte2 = as.m.getBytes();
    for (b = 0; b < arrayOfByte2.length; b++)
      arrayOfByte1[12 + b] = arrayOfByte2[b]; 
    try {
      RecordStore recordStore;
      if ((recordStore = RecordStore.openRecordStore("gamevil_pow_regist", true)).getNumRecords() == 0)
        recordStore.addRecord(arrayOfByte1, 0, arrayOfByte1.length); 
      recordStore.setRecord(1, arrayOfByte1, 0, arrayOfByte1.length);
      return;
    } catch (Exception exception) {
      return;
    } 
  }
  
  final void d() {
    byte[] arrayOfByte = new byte[26];
    try {
      RecordStore recordStore;
      if ((recordStore = RecordStore.openRecordStore("gamevil_pow_regist", false)) == null || recordStore.getNumRecords() < 1) {
        as.l = "";
        as.m = "";
        return;
      } 
      arrayOfByte = recordStore.getRecord(1);
    } catch (Exception exception) {}
    as.l = ag.f(ag.a(arrayOfByte, 0, 12));
    as.m = ag.f(ag.a(arrayOfByte, 12, 26));
  }
  
  private void bu() {
    if (ag.ct[22] == null)
      ag.ct[22] = d(ag.bA.a(18)); 
    if (ag.ct[24] == null)
      ag.ct[24] = d(ag.bA.a(20)); 
    if (as.ht[15] == 0) {
      x.a(ag.ct[22], 107, 111);
    } else {
      x.a(ag.ct[24], 107, 111);
    } 
    x.a(ag.bu);
    x.a("Local", ag.bJ / 2 - 44, 111, 1);
    x.a("Server", ag.bJ / 2 + 50, 111, 1);
    x.a("How much do", ag.bJ / 2, 131, 1);
    x.a("you want to move?", ag.bJ / 2, 143, 1);
    a(70, 163, 100, 20);
    x.a(ag.bv);
    x.a(ag.n(as.hv[14]), ag.bJ / 2, 165, 1);
    ag.h(-1, 2);
    ag.cS.c(200);
  }
  
  private void a(int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    ag.bo.c = paramInt3 + 1;
    ag.bo.a = paramInt1 - 1;
    ag.bo.d = paramInt4 + 1;
    ag.bo.b = paramInt2 - 1;
    ag.b(ag.bo, 0);
    ag.bo.a++;
    ag.bo.b++;
    ag.b(ag.bo, 16777215);
    ag.bo.c--;
    ag.bo.d--;
    ag.a(ag.bo, ag.k(192, 192, 192));
  }
  
  private void bv() {
    String str;
    z[] arrayOfZ;
    if (as.ht[7] == 0) {
      str = "Backpack";
      arrayOfZ = ag.cz.Y;
    } else {
      str = "Warehouse";
      arrayOfZ = as.gw;
    } 
    int i = 20 + (255 - 38 + ag.fK[6] + 16 + 22 >> 1);
    c(str, i);
    i += 38;
    ag.bb.a(i, arrayOfZ, (int[])null);
    ag.fK[14] = 0;
    ag.a(arrayOfZ[ag.fK[18]], true, -1);
    ag.bb.k();
    if (as.ht[7] == 0) {
      ag.h(4, 2);
      return;
    } 
    ag.h(3, 2);
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\m.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */