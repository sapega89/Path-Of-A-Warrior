/*
 * Decompiled with CFR 0.152.
 */
public final class k {
    public byte[] a;
    public int b = 0;

    public k(byte[] byArray) {
        this.a = byArray;
    }

    public final byte a() {
        return this.a[this.b++];
    }

    public final short b() {
        byte by = this.a[this.b++];
        byte by2 = this.a[this.b++];
        return (short)((by & 0xFF) << 0 | (by2 & 0xFF) << 8);
    }

    public final int c() {
        byte by = this.a[this.b++];
        byte by2 = this.a[this.b++];
        byte by3 = this.a[this.b++];
        byte by4 = this.a[this.b++];
        return (by & 0xFF) << 0 | (by2 & 0xFF) << 8 | (by3 & 0xFF) << 16 | (by4 & 0xFF) << 24;
    }

    public final String a(int n2) {
        if (this.a[this.b] == 0) {
            this.b += n2;
            return "";
        }
        int n3 = 0;
        while (n3 < n2) {
            if (this.a[this.b + n3] == 0) break;
            ++n3;
        }
        String string = new String(this.a, this.b, n3);
        this.b += n2;
        return string.trim();
    }
}

