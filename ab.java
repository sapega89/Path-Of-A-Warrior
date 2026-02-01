public final class ab {
  public byte[] a;
  
  public int b = 0;
  
  public ab(byte[] paramArrayOfbyte) {
    this.a = paramArrayOfbyte;
  }
  
  public final byte a() {
    return this.a[this.b++];
  }
  
  public final short b() {
    byte b1 = this.a[this.b++];
    byte b2 = this.a[this.b++];
    return (short)((b1 & 0xFF) << 0 | (b2 & 0xFF) << 8);
  }
  
  public final int c() {
    byte b1 = this.a[this.b++];
    byte b2 = this.a[this.b++];
    byte b3 = this.a[this.b++];
    byte b4 = this.a[this.b++];
    return (b1 & 0xFF) << 0 | (b2 & 0xFF) << 8 | (b3 & 0xFF) << 16 | (b4 & 0xFF) << 24;
  }
  
  public final String a(int paramInt) {
    if (this.a[this.b] == 0) {
      this.b += paramInt;
      return "";
    } 
    byte b;
    for (b = 0; b < paramInt && this.a[this.b + b] != 0; b++);
    String str = new String(this.a, this.b, b);
    this.b += paramInt;
    return str;
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\ab.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */