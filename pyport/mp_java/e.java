/*
 * Decompiled with CFR 0.152.
 */
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.OutputStream;

public final class e {
    DataOutputStream a;
    ByteArrayOutputStream b = new ByteArrayOutputStream();
    int c = 0;
    byte[] d;
    byte[] e = new byte[4];

    public e(OutputStream outputStream) {
        this.a = new DataOutputStream(outputStream);
        this.e[0] = 0;
        this.e[1] = 1;
        this.e[2] = 117;
        this.e[3] = 126;
    }

    public final void a() {
        try {
            if (this.b != null) {
                this.b.close();
            }
            if (this.a != null) {
                this.a.close();
            }
            return;
        }
        catch (Exception exception) {
            return;
        }
    }

    public final void a(int n2) {
        this.b.write((byte)(n2 >>> 0 & 0xFF));
        this.b.write((byte)(n2 >>> 8 & 0xFF));
    }

    public final void a(byte by) {
        this.b.write(by);
    }

    public final void b(int n2) {
        this.b.write((byte)(n2 >>> 0 & 0xFF));
        this.b.write((byte)(n2 >>> 8 & 0xFF));
        this.b.write((byte)(n2 >>> 16 & 0xFF));
        this.b.write((byte)(n2 >>> 24 & 0xFF));
    }

    public final void a(String string, int n2) {
        byte[] byArray = string.getBytes();
        int n3 = 0;
        while (n3 < n2) {
            if (n3 < byArray.length) {
                this.b.write(byArray[n3]);
            } else {
                this.b.write(0);
            }
            ++n3;
        }
    }

    public final synchronized void b() {
        try {
            int n2 = 0;
            byte[] byArray = this.b.toByteArray();
            this.b.reset();
            this.c = byArray.length;
            int n3 = this.c + 2;
            this.d = new byte[n3];
            this.d[0] = (byte)(n3 >>> 0 & 0xFF);
            this.d[1] = (byte)(n3 >>> 8 & 0xFF);
            System.arraycopy(byArray, 0, this.d, 2, this.c);
            n2 = 2 + this.c;
            this.a.write(this.d, 0, n2);
            this.a.flush();
            System.out.print("SEND DATA :  ");
            int n4 = 0;
            while (n4 < n2) {
                System.out.print("[" + n4 + "]" + (this.d[n4] & 0xFF) + "'" + (this.d[n4] == 0 ? (char)' ' : (char)this.d[n4]) + "' ");
                ++n4;
            }
            System.out.println("");
            this.c = 0;
            this.d = null;
            return;
        }
        catch (Exception exception) {
            return;
        }
    }
}

