import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.OutputStream;

public final class u {
  DataOutputStream a;
  
  ByteArrayOutputStream b = new ByteArrayOutputStream();
  
  int c = 0;
  
  byte[] d;
  
  byte[] e = new byte[4];
  
  public u(OutputStream paramOutputStream) {
    this.a = new DataOutputStream(paramOutputStream);
    this.e[0] = 0;
    this.e[1] = 1;
    this.e[2] = 117;
    this.e[3] = 126;
  }
  
  public final void a() {
    try {
      if (this.b != null)
        this.b.close(); 
      if (this.a != null)
        this.a.close(); 
      return;
    } catch (Exception exception) {
      return;
    } 
  }
  
  public final void a(int paramInt) {
    this.b.write((byte)(paramInt >>> 0 & 0xFF));
    this.b.write((byte)(paramInt >>> 8 & 0xFF));
  }
  
  public final void a(boolean paramBoolean) {
    this.b.write(paramBoolean ? 1 : 0);
  }
  
  public final void a(byte paramByte) {
    this.b.write(paramByte);
  }
  
  public final void a(short paramShort) {
    this.b.write((byte)(paramShort >>> 0 & 0xFF));
    this.b.write((byte)(paramShort >>> 8 & 0xFF));
  }
  
  public final void b(int paramInt) {
    this.b.write((byte)(paramInt >>> 0 & 0xFF));
    this.b.write((byte)(paramInt >>> 8 & 0xFF));
    this.b.write((byte)(paramInt >>> 16 & 0xFF));
    this.b.write((byte)(paramInt >>> 24 & 0xFF));
  }
  
  public final void a(String paramString, int paramInt) {
    byte[] arrayOfByte = paramString.getBytes();
    for (byte b = 0; b < paramInt; b++) {
      if (b < arrayOfByte.length) {
        this.b.write(arrayOfByte[b]);
      } else {
        this.b.write(0);
      } 
    } 
  }
  
  public final synchronized void b() {
    try {
      int i = 0;
      byte[] arrayOfByte = this.b.toByteArray();
      this.b.reset();
      this.c = arrayOfByte.length;
      int j = this.c + 2;
      this.d = new byte[j];
      this.d[0] = (byte)(j >>> 0 & 0xFF);
      this.d[1] = (byte)(j >>> 8 & 0xFF);
      System.arraycopy(arrayOfByte, 0, this.d, 2, this.c);
      i = 2 + this.c;
      this.a.write(this.d, 0, i);
      this.a.flush();
      System.out.print("SEND DATA :  ");
      for (byte b = 0; b < i; b++)
        System.out.print("[" + b + "]" + this.d[b] + "'" + ((this.d[b] == 0) ? 32 : (char)this.d[b]) + "' "); 
      System.out.println("");
      this.c = 0;
      this.d = null;
      return;
    } catch (Exception exception) {
      return;
    } 
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar\\u.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */