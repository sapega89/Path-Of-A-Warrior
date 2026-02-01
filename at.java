public final class at {
  private StringBuffer a;
  
  private int b;
  
  private int c;
  
  private char d;
  
  private int e;
  
  public at(String paramString, int paramInt1, int paramInt2) {
    this.a = new StringBuffer(paramString);
    this.b = paramInt1;
    this.c = 0;
    this.d = ' ';
    this.e = paramString.length();
  }
  
  private void b(int paramInt) {
    if (this.e + paramInt >= 0 && this.e + paramInt <= this.b - 1 && b() == this.e + paramInt)
      this.e += paramInt; 
  }
  
  public final String a() {
    StringBuffer stringBuffer;
    return (stringBuffer = new StringBuffer(this.a.toString())).toString();
  }
  
  public final void a(String paramString) {
    this.a = new StringBuffer(paramString);
  }
  
  public final int b() {
    int i;
    if (this.a.length() == 0) {
      i = 0;
    } else {
      i = this.a.length();
    } 
    return i;
  }
  
  public final int a(int paramInt) {
    int i = this.a.length() - 1;
    if (paramInt == -7 || paramInt == -8) {
      if (i >= 0) {
        this.a.setLength(i);
        this.c = 0;
        b(-1);
      } else {
        return 1;
      } 
    } else if ((paramInt >= 97 && paramInt <= 122) || (paramInt >= 65 && paramInt <= 90)) {
      char c = Character.MIN_VALUE;
      c = (char)paramInt;
      if (this.d != c)
        this.c = 0; 
      this.d = c;
      this.c++;
      if (this.a.length() == this.e) {
        this.a.append(c);
        this.c = 1;
      } else if (this.a.length() < this.b) {
        if (this.a.length() != 0)
          b(1); 
        this.a.append(c);
      } 
    } 
    return 0;
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\at.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */