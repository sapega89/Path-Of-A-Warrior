import java.io.ByteArrayOutputStream;
import java.io.InputStream;

public final class j {
  public static byte[] a(String paramString) {
    try {
      InputStream inputStream = paramString.getClass().getResourceAsStream(paramString);
      byte[] arrayOfByte1 = new byte[1024];
      ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
      int i;
      while ((i = inputStream.read(arrayOfByte1)) != -1)
        byteArrayOutputStream.write(arrayOfByte1, 0, i); 
      inputStream.close();
      byte[] arrayOfByte2 = byteArrayOutputStream.toByteArray();
      byteArrayOutputStream.close();
      return arrayOfByte2;
    } catch (Exception exception) {
      return null;
    } 
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\j.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */