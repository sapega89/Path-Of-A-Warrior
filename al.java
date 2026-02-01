import java.io.ByteArrayInputStream;
import java.io.DataInputStream;

public final class al {
  private byte[] a;
  
  public al(String paramString) {
    this.a = j.a(paramString);
  }
  
  public final String a(int paramInt) {
    int i = 2 + paramInt * 2;
    int j = this.a[i] & 0xFF | (this.a[i + 1] & 0xFF) << 8;
    int k = this.a[i + 2] & 0xFF | (this.a[i + 3] & 0xFF) << 8;
    String str = null;
    try {
      int m;
      byte[] arrayOfByte;
      (arrayOfByte = new byte[(m = k - j) + 2])[0] = (byte)(m >> 8 & 0xFF);
      arrayOfByte[1] = (byte)(m & 0xFF);
      System.arraycopy(this.a, j, arrayOfByte, 2, m);
      ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(arrayOfByte, 0, arrayOfByte.length);
      DataInputStream dataInputStream;
      str = (dataInputStream = new DataInputStream(byteArrayInputStream)).readUTF();
      byteArrayInputStream.close();
      dataInputStream.close();
    } catch (Exception exception) {}
    return str;
  }
  
  public final void a() {
    this.a = null;
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\al.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */