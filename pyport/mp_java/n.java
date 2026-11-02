/*
 * Decompiled with CFR 0.152.
 */
import java.io.ByteArrayOutputStream;
import java.io.InputStream;

public final class n {
    public static byte[] a(String string) {
        try {
            int n2;
            InputStream inputStream = string.getClass().getResourceAsStream(string);
            byte[] byArray = new byte[1024];
            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
            while ((n2 = inputStream.read(byArray)) != -1) {
                byteArrayOutputStream.write(byArray, 0, n2);
            }
            inputStream.close();
            byte[] byArray2 = byteArrayOutputStream.toByteArray();
            byteArrayOutputStream.close();
            return byArray2;
        }
        catch (Exception exception) {
            System.out.println("fail to read " + string + " e:" + exception);
            return null;
        }
    }
}

