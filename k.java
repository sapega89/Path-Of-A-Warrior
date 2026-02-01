final class k extends ag {
  public static aq a = null;
  
  public static int b = -1;
  
  public static int a_ = -1;
  
  public static int d = -1;
  
  public static long e;
  
  public static int[] f = new int[17];
  
  public k(Main paramMain) {
    super(paramMain);
    for (byte b = 0; b < 17; b++)
      f[b] = 0; 
    f[9] = 500;
    a = new aq(17, 1, true, true);
  }
  
  public final void a_(int paramInt) {
    if (a == null || !ag.df)
      return; 
    long l = System.currentTimeMillis() - e;
    if (d != -1 && f[d] != 0 && l < f[d])
      return; 
    if (paramInt > 2 && paramInt != 15 && paramInt != 16 && paramInt != 3 && paramInt != 4)
      b(); 
    b = paramInt;
    d = paramInt;
    e = System.currentTimeMillis();
  }
  
  public final void a() {
    if (a == null || !ag.df)
      return; 
    a.e();
    boolean bool1 = false;
    boolean bool2 = true;
    int i = b;
    b = -1;
    if (ag.df && i != -1) {
      if (i <= 2) {
        if (a_ == i) {
          bool2 = false;
        } else {
          b();
        } 
        a_ = i;
        bool1 = true;
      } else {
        a_ = -1;
        bool1 = false;
      } 
      if (bool2)
        a(i, bool1); 
    } 
  }
  
  private void a(int paramInt, boolean paramBoolean) {
    a.a(ag.dg);
    if (ag.dg == 0) {
      b();
      return;
    } 
    if (paramInt <= 2) {
      a.a("/snd" + paramInt + ".mid", paramInt);
    } else {
      a.a("/snd" + paramInt + ".wav", paramInt);
    } 
    a.a(paramInt, paramBoolean);
  }
  
  public static void b() {
    b = -1;
    a_ = -1;
    a.b();
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\k.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */