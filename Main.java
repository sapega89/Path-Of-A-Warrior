import com.movaya.M123456;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.midlet.MIDlet;

public class Main extends M123456 {
  public static Display a = null;
  
  public static ag b = null;
  
  public static boolean c = false;
  
  protected void startApp_123456() {
    if (c)
      return; 
    c = true;
    if (ag.bt == null) {
      ag.bt = new Thread(b);
      ag.bt.start();
    } 
  }
  
  public void pauseApp() {
    b.hideNotify();
  }
  
  public void destroyApp(boolean paramBoolean) {
    if (b != null && ag.bg != null && k.a != null)
      k.a.a(); 
  }
  
  public void constructor_123456() {
    this;
    if (a == null) {
      c = false;
      a = Display.getDisplay((MIDlet)this);
      b = new ag(this);
      a.setCurrent((Displayable)b);
    } 
  }
  
  protected final void startApp() {
    tryNBuy_123456();
  }
}


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\Main.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */