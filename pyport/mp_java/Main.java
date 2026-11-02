/*
 * Decompiled with CFR 0.152.
 * 
 * Could not load the following classes:
 *  javax.microedition.lcdui.Display
 *  javax.microedition.lcdui.Displayable
 *  javax.microedition.midlet.MIDlet
 */
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Displayable;
import javax.microedition.midlet.MIDlet;

public class Main
extends MIDlet {
    public static Display a;
    public static g b;
    public static boolean c;

    public Main() {
        c = false;
        a = Display.getDisplay((MIDlet)this);
        b = new g(this);
        a.setCurrent((Displayable)b);
    }

    protected void startApp() {
        if (c) {
            return;
        }
        c = true;
        g.dT = new Thread(b);
        g.dT.setPriority(1);
        g.dT.start();
    }

    public void pauseApp() {
        if (b != null) {
            b.hideNotify();
        }
    }

    public void destroyApp(boolean bl) {
    }

    static {
        c = false;
    }
}

