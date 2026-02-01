import java.io.IOException;
import java.io.InterruptedIOException;
import javax.microedition.io.Connector;
import javax.microedition.io.StreamConnection;

public final class v extends Thread {
  public static StreamConnection a;
  
  public static u b;
  
  public static b c;
  
  public static s d;
  
  public ab e;
  
  public static boolean f = true;
  
  public static int g;
  
  public static boolean h = false;
  
  public static boolean i = true;
  
  public static boolean j = false;
  
  public String k;
  
  public int l;
  
  public static boolean m;
  
  public final void a(String paramString, int paramInt) {
    this.k = paramString;
    this.l = paramInt;
    j = true;
  }
  
  public final void a() {
    try {
      h = false;
      if (c != null)
        c.a(); 
      if (b != null)
        b.a(); 
      if (a != null) {
        a.close();
        a = null;
      } 
      System.gc();
      return;
    } catch (Exception exception) {
      return;
    } 
  }
  
  private void c() {
    try {
      a = (StreamConnection)Connector.open("socket://" + this.k + ":" + this.l);
      c = new b(a.openInputStream());
      b = new u(a.openOutputStream());
      h = true;
      d.f();
      m = true;
      return;
    } catch (Exception exception) {
      d.e();
      return;
    } 
  }
  
  public static void a(s params) {
    d = params;
  }
  
  public final void run() {
    while (i) {
      if (h) {
        try {
          this.e = c.b();
          d.a(this.e);
          Thread.yield();
        } catch (InterruptedIOException interruptedIOException) {
          d.e();
        } catch (IOException iOException) {
          d.e();
        } catch (Exception exception) {
          d.e();
        } 
      } else {
        if (j) {
          j = false;
          c();
        } else if (h && ++g > Integer.MAX_VALUE) {
          g = 300;
        } 
        Thread.yield();
        c(100);
      } 
      c(100);
    } 
  }
  
  private static void c(int paramInt) {
    try {
      Thread.sleep(paramInt);
      return;
    } catch (Exception exception) {
      return;
    } 
  }
  
  public final synchronized void a(int paramInt) {
    if (h) {
      while (!f)
        c(50); 
      f = false;
      b.a(paramInt);
    } 
  }
  
  public static void a(short paramShort) {
    if (h)
      b.a(paramShort); 
  }
  
  public static void a(byte paramByte) {
    if (h)
      b.a(paramByte); 
  }
  
  public static void b(int paramInt) {
    if (h)
      b.b(paramInt); 
  }
  
  public static void a(boolean paramBoolean) {
    if (h)
      b.a(paramBoolean); 
  }
  
  public static void b(String paramString, int paramInt) {
    if (h)
      b.a(paramString, paramInt); 
  }
  
  public final void b() {
    b.b();
    f = true;
  }
  
  public v() {
    f = true;
    h = false;
    i = true;
    j = false;
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\v.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */