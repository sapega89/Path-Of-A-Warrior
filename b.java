import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;

public final class b {
  DataInputStream a;
  
  int b;
  
  byte[] c = new byte[1024];
  
  public b(InputStream paramInputStream) {
    this.a = new DataInputStream(paramInputStream);
    this.b = -1;
  }
  
  public final void a() {
    try {
      if (this.a != null)
        this.a.close(); 
      return;
    } catch (Exception exception) {
      return;
    } 
  }
  
  public final ab b() throws IOException {
    byte[] arrayOfByte = null;
    this.c[0] = 0;
    this.c[1] = 0;
    this.a.read(this.c, 0, 2);
    this.b = (this.c[0] & 0xFF) << 0 | (this.c[1] & 0xFF) << 8;
    arrayOfByte = new byte[this.b - 2];
    this.a.readFully(arrayOfByte, 0, arrayOfByte.length);
    System.out.print("RECV DATA :  ");
    for (byte b1 = 0; b1 < arrayOfByte.length; b1++)
      System.out.print("[" + b1 + "]" + arrayOfByte[b1] + "'" + ((arrayOfByte[b1] <= 47) ? 32 : (char)arrayOfByte[b1]) + "' "); 
    System.out.println("");
    ab ab = new ab(arrayOfByte);
    this.b = -1;
    return ab;
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\b.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */