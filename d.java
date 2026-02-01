import java.io.InputStream;

public final class d {
  private byte[] a;
  
  private byte[] b;
  
  private byte[] c;
  
  private int d;
  
  public d(String paramString) {
    try {
      InputStream inputStream;
      int i = (inputStream = getClass().getResourceAsStream(paramString)).read();
      this.a = new byte[i];
      this.b = new byte[i];
      inputStream.read(this.a);
      int j = inputStream.available();
      this.c = new byte[j];
      inputStream.read(this.c);
      inputStream.close();
      int k = 0;
      for (byte b = 0; b < i; b++) {
        this.b[b] = (byte)k;
        k += this.a[b] & 0xFF;
      } 
      this.d = k;
      return;
    } catch (Exception exception) {
      return;
    } 
  }
  
  public final int a(int paramInt1, int paramInt2) {
    int i = 0;
    try {
      int j = this.a[paramInt2] & 0xFF;
      int k = paramInt1 * this.d + (this.b[paramInt2] & 0xFF);
      for (byte b = 0; b < j; b++)
        i |= (this.c[k + b] & 0xFF) << b * 8; 
    } catch (Exception exception) {}
    return i;
  }
  
  public final String b(int paramInt1, int paramInt2) {
    return (new String(this.c, paramInt1 * this.d + (this.b[paramInt2] & 0xFF), this.a[paramInt2] & 0xFF)).trim();
  }
  
  public final void a() {
    this.a = null;
    this.b = null;
    this.c = null;
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\d.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */