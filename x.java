import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;

public final class x {
  private static Graphics b;
  
  private static int c;
  
  private static int d;
  
  private static int e;
  
  private static int f;
  
  private static int g;
  
  private static int h;
  
  private static int i;
  
  private static int j;
  
  private static g k;
  
  static int[] a;
  
  public static synchronized void a(Graphics paramGraphics) {
    b = paramGraphics;
    g = b.getClipX();
    h = b.getClipY();
    i = b.getClipWidth();
    j = b.getClipHeight();
  }
  
  public static void a(int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    c = g;
    d = h;
    e = i;
    f = j;
    g = paramInt1;
    h = paramInt2;
    i = paramInt3;
    j = paramInt4;
    b.clipRect(paramInt1, paramInt2, paramInt3, paramInt4);
  }
  
  public static void a() {
    g = c;
    h = d;
    i = e;
    j = f;
    b.setClip(c, d, e, f);
  }
  
  public static void a(Image paramImage, int paramInt1, int paramInt2) {
    b.drawImage(paramImage, paramInt1, paramInt2, 20);
  }
  
  public static void a(Image paramImage, int paramInt1, int paramInt2, int paramInt3) {
    b.drawImage(paramImage, paramInt1, paramInt2, paramInt3);
  }
  
  public static void a(Image paramImage, int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5, int paramInt6) {
    b.clipRect(paramInt1, paramInt2, paramInt3, paramInt4);
    b.drawImage(paramImage, paramInt1 - paramInt5, paramInt2 - paramInt6, 20);
    b.setClip(g, h, i, j);
  }
  
  public static void a(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5) {
    b.setColor(paramInt5);
    b.drawRect(paramInt1, paramInt2, paramInt3 - 1, paramInt4 - 1);
  }
  
  public static void b(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5) {
    b.setColor(paramInt5);
    b.fillRect(paramInt1, paramInt2, paramInt3, paramInt4);
  }
  
  public static void c(int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5) {
    b.setColor(paramInt5);
    b.drawLine(paramInt1, paramInt2, paramInt3, paramInt4);
  }
  
  public static void a(g paramg) {
    k = paramg;
  }
  
  private static void a(char[] paramArrayOfchar, int paramInt1, int paramInt2, int paramInt3, int paramInt4, int paramInt5) {
    if ((paramInt5 & 0x1) != 0) {
      paramInt3 -= k.a(paramArrayOfchar, paramInt1, paramInt2) / 2;
    } else if ((paramInt5 & 0x8) != 0) {
      paramInt3 -= k.a(paramArrayOfchar, paramInt1, paramInt2);
    } 
    int i = paramInt1 + paramInt2;
    int j = paramInt3;
    for (int k = paramInt1; k < i; k++) {
      char c = paramArrayOfchar[k];
      int m = k.a(c);
      k.a(c, j, paramInt4);
      j += m;
    } 
  }
  
  public static void a(String paramString, int paramInt1, int paramInt2, int paramInt3) {
    a(paramString.toCharArray(), 0, paramString.length(), paramInt1, paramInt2, paramInt3);
  }
  
  private static void b() {
    a = new int[256];
    for (byte b = 0; b < 'Ā'; b++) {
      int i = b;
      byte b1 = 8;
      while (--b1 >= 0) {
        if ((i & 0x1) != 0) {
          i = 0xEDB88320 ^ i >>> 1;
          continue;
        } 
        i >>>= 1;
      } 
      a[b] = i;
    } 
  }
  
  static long a(byte[] paramArrayOfbyte, int paramInt1, int paramInt2) {
    if (a == null)
      b(); 
    for (int i = -1; --paramInt2 >= 0; i = a[(i ^ paramArrayOfbyte[paramInt1++]) & 0xFF] ^ i >>> 8);
    return (i ^ 0xFFFFFFFF) & 0xFFFFFFFFL;
  }
  
  static {
    (new byte[29])[0] = -119;
    (new byte[29])[1] = 80;
    (new byte[29])[2] = 78;
    (new byte[29])[3] = 71;
    (new byte[29])[4] = 13;
    (new byte[29])[5] = 10;
    (new byte[29])[6] = 26;
    (new byte[29])[7] = 10;
    (new byte[29])[8] = 0;
    (new byte[29])[9] = 0;
    (new byte[29])[10] = 0;
    (new byte[29])[11] = 13;
    (new byte[29])[12] = 73;
    (new byte[29])[13] = 72;
    (new byte[29])[14] = 68;
    (new byte[29])[15] = 82;
    (new byte[29])[16] = 0;
    (new byte[29])[17] = 0;
    (new byte[29])[18] = 0;
    (new byte[29])[19] = 0;
    (new byte[29])[20] = 0;
    (new byte[29])[21] = 0;
    (new byte[29])[22] = 0;
    (new byte[29])[23] = 0;
    (new byte[29])[24] = 8;
    (new byte[29])[25] = 3;
    (new byte[29])[26] = 0;
    (new byte[29])[27] = 0;
    (new byte[29])[28] = 0;
    (new byte[12])[0] = 0;
    (new byte[12])[1] = 0;
    (new byte[12])[2] = 0;
    (new byte[12])[3] = 0;
    (new byte[12])[4] = 73;
    (new byte[12])[5] = 69;
    (new byte[12])[6] = 78;
    (new byte[12])[7] = 68;
    (new byte[12])[8] = -82;
    (new byte[12])[9] = 66;
    (new byte[12])[10] = 96;
    (new byte[12])[11] = -126;
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\x.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */