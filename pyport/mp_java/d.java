/*
 * Decompiled with CFR 0.152.
 */
import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;

public final class d {
    DataInputStream a;
    int b;
    byte[] c = new byte[1024];

    public d(InputStream inputStream) {
        this.a = new DataInputStream(inputStream);
        this.b = -1;
    }

    public final void a() {
        try {
            if (this.a != null) {
                this.a.close();
            }
            return;
        }
        catch (Exception exception) {
            return;
        }
    }

    public final synchronized k b() throws IOException {
        byte[] byArray = null;
        this.c[0] = 0;
        this.c[1] = 0;
        this.a.read(this.c, 0, 2);
        this.b = (this.c[0] & 0xFF) << 0 | (this.c[1] & 0xFF) << 8;
        byArray = new byte[this.b - 2];
        this.a.readFully(byArray, 0, byArray.length);
        System.out.print("RECV DATA :  ");
        int n2 = 0;
        while (n2 < byArray.length) {
            System.out.print("[" + n2 + "]" + (byArray[n2] & 0xFF) + "'" + (byArray[n2] <= 47 ? (char)' ' : (char)byArray[n2]) + "' ");
            ++n2;
        }
        System.out.println("");
        k k2 = new k(byArray);
        this.b = -1;
        return k2;
    }
}

