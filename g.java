import javax.microedition.lcdui.Image;

public final class g {
  private Image a;
  
  private int b;
  
  private int c;
  
  private int d;
  
  private static int e = 0;
  
  public g(String paramString, int paramInt1, int paramInt2, int paramInt3, int paramInt4) {
    this.b = paramInt1;
    this.c = paramInt2;
    this.d = paramInt3;
    try {
      byte[] arrayOfByte = j.a(paramString);
      byte b1 = (byte)(paramInt4 >> 16 & 0xFF);
      byte b2 = (byte)(paramInt4 >> 8 & 0xFF);
      byte b3 = (byte)(paramInt4 & 0xFF);
      for (byte b = 0; b < 100; b++) {
        if (arrayOfByte[b] == 80 && arrayOfByte[b + 1] == 76 && arrayOfByte[b + 2] == 84 && arrayOfByte[b + 3] == 69) {
          e = b;
          break;
        } 
      } 
      if (arrayOfByte[e + 4] != b1 || arrayOfByte[e + 5] != b2 || arrayOfByte[e + 6] != b3) {
        arrayOfByte[e + 4] = b1;
        arrayOfByte[e + 5] = b2;
        arrayOfByte[e + 6] = b3;
        long l = x.a(arrayOfByte, e, 10);
        arrayOfByte[e + 10] = (byte)(int)(l >> 24L & 0xFFL);
        arrayOfByte[e + 11] = (byte)(int)(l >> 16L & 0xFFL);
        arrayOfByte[e + 12] = (byte)(int)(l >> 8L & 0xFFL);
        arrayOfByte[e + 13] = (byte)(int)(l & 0xFFL);
      } 
      this.a = Image.createImage(arrayOfByte, 0, arrayOfByte.length);
      return;
    } catch (Exception exception) {
      return;
    } 
  }
  
  public final int a() {
    return this.c;
  }
  
  public static int b() {
    return 9;
  }
  
  public static int c() {
    return 1;
  }
  
  final void a(char paramChar, int paramInt1, int paramInt2) {
    if (paramChar == ' ')
      return; 
    x.a(this.a, paramInt1, paramInt2, this.b, this.c, b(paramChar) * this.b, 0);
  }
  
  private static int b(char paramChar) {
    int i = 0;
    if (paramChar >= 'A' && paramChar <= 'Z') {
      i = 32 + paramChar - 65;
    } else if (paramChar >= 'a' && paramChar <= 'z') {
      i = 64 + paramChar - 97;
    } else if (paramChar >= '0' && paramChar <= '9') {
      i = 15 + paramChar - 48;
    } else if (paramChar == '!') {
      i = 0;
    } else if (paramChar == '"') {
      i = 1;
    } else if (paramChar == '#') {
      i = 2;
    } else if (paramChar == '$') {
      i = 3;
    } else if (paramChar == '%') {
      i = 4;
    } else if (paramChar == '&') {
      i = 5;
    } else if (paramChar == '\'') {
      i = 6;
    } else if (paramChar == '(') {
      i = 7;
    } else if (paramChar == ')') {
      i = 8;
    } else if (paramChar == '*') {
      i = 9;
    } else if (paramChar == '+') {
      i = 10;
    } else if (paramChar == ',') {
      i = 11;
    } else if (paramChar == '-') {
      i = 12;
    } else if (paramChar == '.') {
      i = 13;
    } else if (paramChar == '/') {
      i = 14;
    } else if (paramChar == ':') {
      i = 25;
    } else if (paramChar == ';') {
      i = 26;
    } else if (paramChar == '<') {
      i = 27;
    } else if (paramChar == '=') {
      i = 28;
    } else if (paramChar == '>') {
      i = 29;
    } else if (paramChar == '?') {
      i = 30;
    } else if (paramChar == '@') {
      i = 31;
    } else if (paramChar == '[') {
      i = 58;
    } else if (paramChar == ']') {
      i = 60;
    } else if (paramChar == '^') {
      i = 61;
    } else if (paramChar == '_') {
      i = 62;
    } else if (paramChar == '`') {
      i = 63;
    } else if (paramChar == '{') {
      i = 90;
    } else if (paramChar == '|') {
      i = 91;
    } else if (paramChar == '}') {
      i = 92;
    } else if (paramChar == '~') {
      i = 93;
    } else if (paramChar == ' ') {
      i = 99;
    } 
    return i;
  }
  
  public final int a(char paramChar) {
    return (paramChar == ' ') ? this.d : (this.b + 1 - 0);
  }
  
  public final int a(char[] paramArrayOfchar, int paramInt1, int paramInt2) {
    int i = 0;
    int j = paramInt1 + paramInt2;
    for (int k = paramInt1; k < j; k++)
      i += a(paramArrayOfchar[k]); 
    return i;
  }
  
  public final int a(String paramString) {
    char[] arrayOfChar = paramString.toCharArray();
    return a(arrayOfChar, 0, arrayOfChar.length);
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\g.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */