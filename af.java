import javax.microedition.lcdui.Image;

final class af extends ag {
  Image a = d("logo1");
  
  public static int b = 0;
  
  public static long c;
  
  public af() {
    super(ag.bs);
    c = System.currentTimeMillis();
  }
  
  public final void a() {
    if (b == 0) {
      ag.u(16777215);
      if (this.a != null)
        x.a(this.a, ag.bL, ag.bM, 3); 
      if (System.currentTimeMillis() - c > 2500L) {
        this.a = null;
        b = 1;
        ag.cS.e(40);
        return;
      } 
    } else {
      if (b == 1) {
        ag.u(0);
        x.a(ag.bu);
        ag.cS.c();
        return;
      } 
      if (b == 2)
        Main.b.S(); 
    } 
  }
  
  public final void b() {
    if (b == 0)
      return; 
    if (b == 1) {
      int i;
      if ((i = ag.cS.b()) != -1) {
        ag.df = (i == 0);
        if (i == 0) {
          if (ag.dg == 0)
            ag.dg = 75; 
        } else {
          ag.dg = 0;
        } 
        a_(0);
        b = 2;
        E();
      } 
      return;
    } 
    if (b == 2 && b(ag.ch)) {
      ag.ck = 1;
      ag.cv = null;
      ag.cw = null;
      ag.bb.g();
      T();
    } 
  }
  
  private static boolean b(int paramInt) {
    null = false;
    switch (paramInt) {
      case -10:
      case -8:
      case -7:
      case -6:
      case -5:
      case -4:
      case -3:
      case -2:
      case -1:
      case 35:
      case 42:
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
        return true;
    } 
    return false;
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\af.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */