import java.io.ByteArrayInputStream;
import javax.microedition.media.Manager;
import javax.microedition.media.Player;
import javax.microedition.media.PlayerListener;
import javax.microedition.media.control.VolumeControl;

public final class aq extends q implements PlayerListener {
  private boolean b = false;
  
  public Player[] a;
  
  private boolean c = false;
  
  private boolean d;
  
  private int e;
  
  private int f;
  
  private boolean g;
  
  private boolean[] h;
  
  private String[] i;
  
  private int j;
  
  private int[] k;
  
  private int l = -1;
  
  private boolean m = false;
  
  private int n = -1;
  
  private boolean o = false;
  
  private int p = -1;
  
  public aq(int paramInt1, int paramInt2, boolean paramBoolean1, boolean paramBoolean2) {
    this.e = paramInt1;
    this.a = new Player[this.e];
    this.f = paramInt2;
    this.g = paramBoolean1;
    this.d = paramBoolean2;
    this.h = new boolean[this.e];
    for (byte b1 = 0; b1 < this.e; b1++)
      this.h[b1] = false; 
    this.k = new int[this.e];
    for (byte b2 = 0; b2 < this.e; b2++)
      a(b2, 0); 
    this.j = 100;
    this.i = new String[this.e];
  }
  
  public final void playerUpdate(Player paramPlayer, String paramString, Object paramObject) {
    "-1.:" + this.l;
    if (paramString == "started") {
      this.b = true;
      "-Update START:" + this.n;
      return;
    } 
    if (paramString == "endOfMedia" || paramString == "stopped") {
      "-Update " + paramString + ":" + this.n;
      if (this.o && paramString == "endOfMedia")
        return; 
      if (!this.g)
        a(); 
      this.b = false;
      this.n = -1;
      this.o = false;
    } 
  }
  
  public final void a() {
    for (byte b = 0; b < this.e; b++)
      b(b); 
  }
  
  private void b(int paramInt) {
    if (this.a[paramInt] != null) {
      this.a[paramInt].close();
      this.a[paramInt] = null;
    } 
    this.h[paramInt] = false;
  }
  
  public final void a(int paramInt, boolean paramBoolean) {
    if (paramInt < 0)
      return; 
    if (this.j <= 0)
      return; 
    b(paramInt, paramBoolean);
  }
  
  private synchronized boolean b(int paramInt, boolean paramBoolean) {
    if (paramBoolean) {
      this.p = paramInt;
    } else {
      this.p = -1;
    } 
    this.l = paramInt;
    this.m = paramBoolean;
    if (this.b && this.b)
      return false; 
    d(5);
    "---step 2:" + this.j;
    if (!this.h[paramInt] && !a(this.i[paramInt], paramInt))
      return false; 
    if (this.f == 0)
      f(); 
    if (!a(this.a[paramInt]))
      return false; 
    if (paramBoolean) {
      try {
        this.a[paramInt].setLoopCount(-1);
      } catch (IllegalArgumentException illegalArgumentException) {
        this.a[paramInt].setLoopCount(0);
      } 
    } else {
      this.a[paramInt].setLoopCount(1);
    } 
    if (this.d)
      try {
        this.a[paramInt].setMediaTime(1L);
      } catch (Exception exception) {
        "setMediaTime err:" + exception;
      }  
    if (this.a[paramInt].getState() == 300)
      try {
        this.n = paramInt;
        this.o = paramBoolean;
        this.a[paramInt].start();
        this.l = -1;
        b(this.a[paramInt]);
        return true;
      } catch (Exception exception) {
        "Start err:" + exception;
        return false;
      }  
    return false;
  }
  
  private boolean a(String paramString1, int paramInt, String paramString2) {
    try {
      if (!this.g) {
        g();
        if (this.a[paramInt] != null)
          this.a[paramInt].close(); 
        this.a[paramInt] = null;
        this.h[paramInt] = false;
        this.b = false;
        this.n = -1;
        this.o = false;
        this.l = -1;
        this.m = false;
      } 
      if (!this.h[paramInt]) {
        ByteArrayInputStream byteArrayInputStream;
        Player player;
        (player = Manager.createPlayer(byteArrayInputStream = new ByteArrayInputStream(j.a(paramString1)), paramString2)).addPlayerListener(this);
        player.realize();
        if (this.f == 1 && !a(player))
          return false; 
        this.a[paramInt] = player;
        this.i[paramInt] = paramString1;
        if (this.a[paramInt] != null)
          this.h[paramInt] = true; 
      } 
      return true;
    } catch (Exception exception) {
      "loading err:" + exception;
      return false;
    } 
  }
  
  public final boolean a(String paramString, int paramInt) {
    return a(paramString, paramInt, a(paramString));
  }
  
  private static String a(String paramString) {
    String str = null;
    if (paramString.endsWith("wav")) {
      str = "audio/x-wav";
    } else if (paramString.endsWith("amr")) {
      str = "audio/amr";
    } else if (paramString.endsWith("mid")) {
      str = "audio/midi";
    } else if (paramString.endsWith("mp3")) {
      str = "audio/mpeg";
    } 
    return str;
  }
  
  private static boolean a(Player paramPlayer) {
    if (paramPlayer == null)
      return false; 
    if (paramPlayer.getState() == 200)
      try {
        paramPlayer.prefetch();
        return true;
      } catch (Exception exception) {
        "tryPrefetch err:" + exception;
        return false;
      }  
    return (paramPlayer.getState() == 300);
  }
  
  private void f() {
    for (byte b = 0; b < this.e; b++) {
      if (this.a[b] != null && this.a[b].getState() == 300)
        this.a[b].deallocate(); 
    } 
  }
  
  public final void b() {
    this.l = -1;
    this.m = false;
    this.p = -1;
    g();
  }
  
  private void g() {
    try {
      if (this.n != -1 && this.a[this.n] != null) {
        this.a[this.n].stop();
        if (!this.d)
          this.a[this.n].deallocate(); 
      } 
      return;
    } catch (Exception exception) {
      "playingSoundStop err:" + exception;
      return;
    } 
  }
  
  private void c(int paramInt) {
    if (paramInt >= 0 && paramInt <= 100)
      this.j = paramInt; 
  }
  
  public final void a(int paramInt) {
    c(paramInt);
    int i;
    if ((i = this.n) != -1)
      b(this.a[i]); 
  }
  
  private void b(Player paramPlayer) {
    VolumeControl volumeControl;
    if (paramPlayer != null && (volumeControl = (VolumeControl)paramPlayer.getControl("VolumeControl")) != null)
      volumeControl.setLevel(this.j); 
  }
  
  private void a(int paramInt1, int paramInt2) {
    if (paramInt1 < this.e && paramInt1 >= 0)
      this.k[paramInt1] = paramInt2; 
  }
  
  public final void c() {
    this.c = true;
    "hide:" + this.p;
    this.l = -1;
    this.m = false;
    g();
    this.b = false;
    this.n = -1;
    this.o = false;
  }
  
  public final void d() {
    "show:" + this.p;
    this.c = false;
    if (this.p != -1)
      a(this.p, true); 
  }
  
  public final void e() {
    synchronized (this) {
      if (!this.c)
        if (this.l != -1 && !this.b) {
          if (this.m)
            a(this.l, this.m); 
        } else if (this.b && this.a[this.n] != null && this.a[this.n].getState() != 400 && this.o) {
          this.b = false;
          a(this.n, this.o);
        }  
      return;
    } 
  }
  
  private void d(int paramInt) {
    try {
      Thread.sleep(paramInt);
      Thread.yield();
      return;
    } catch (Exception exception) {
      return;
    } 
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\aq.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */