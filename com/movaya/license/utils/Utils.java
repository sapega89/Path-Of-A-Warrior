/*     */ package com.movaya.license.utils;
/*     */ 
/*     */ import java.io.ByteArrayInputStream;
/*     */ import java.io.ByteArrayOutputStream;
/*     */ import java.io.DataInputStream;
/*     */ import java.io.DataOutputStream;
/*     */ import java.io.IOException;
/*     */ import java.io.InputStream;
/*     */ import java.io.OutputStream;
/*     */ import java.util.Vector;
/*     */ import javax.microedition.io.Connection;
/*     */ import javax.microedition.lcdui.Alert;
/*     */ import javax.microedition.lcdui.AlertType;
/*     */ import javax.microedition.lcdui.Command;
/*     */ import javax.microedition.lcdui.Font;
/*     */ import javax.microedition.lcdui.TextField;
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ public final class Utils
/*     */ {
/*     */   private static final int X = 31;
/*     */   
/*     */   private static final int simpleCrypt(int p_int) {
/*  37 */     return p_int ^ 0x1F;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public static boolean s_showException = false;
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public static final void closeIn(InputStream p_inputStream) {
/*  52 */     if (p_inputStream != null) {
/*     */       
/*     */       try {
/*     */         
/*  56 */         p_inputStream.close();
/*     */       }
/*  58 */       catch (IOException ex) {
/*     */         
/*  60 */         if (s_showException)
/*     */         {
/*  62 */           ex.printStackTrace();
/*     */         }
/*     */       } 
/*     */     }
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public static final void closeOut(OutputStream p_outputStream) {
/*  75 */     if (p_outputStream != null) {
/*     */       
/*     */       try {
/*     */         
/*  79 */         p_outputStream.close();
/*     */       }
/*  81 */       catch (IOException ex) {
/*     */         
/*  83 */         if (s_showException)
/*     */         {
/*  85 */           ex.printStackTrace();
/*     */         }
/*     */       } 
/*     */     }
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public static final void closeConnection(Connection conn) {
/*     */     try {
/* 101 */       if (conn != null)
/*     */       {
/* 103 */         conn.close();
/*     */       }
/*     */     }
/* 106 */     catch (IOException ex) {
/*     */       
/* 108 */       if (s_showException)
/*     */       {
/* 110 */         ex.printStackTrace();
/*     */       }
/*     */     } 
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public static String encrypt(String para) {
/* 124 */     if (para == null)
/*     */     {
/* 126 */       return null;
/*     */     }
/*     */     
/* 129 */     String result = "";
/*     */     
/* 131 */     byte[] bytes = (byte[])null;
/* 132 */     bytes = para.getBytes();
/*     */     
/* 134 */     ByteArrayInputStream bin = null;
/* 135 */     ByteArrayOutputStream bout = null;
/* 136 */     DataInputStream din = null;
/* 137 */     DataOutputStream dout = null;
/*     */ 
/*     */     
/*     */     try {
/* 141 */       bin = new ByteArrayInputStream(bytes);
/* 142 */       bout = new ByteArrayOutputStream();
/* 143 */       din = new DataInputStream(bin);
/* 144 */       dout = new DataOutputStream(bout);
/*     */       
/* 146 */       byte data = -1;
/* 147 */       String str = "";
/* 148 */       while (din.available() != 0) {
/*     */         
/* 150 */         data = din.readByte();
/* 151 */         str = Integer.toHexString(simpleCrypt(data));
/* 152 */         dout.write(str.getBytes());
/*     */       } 
/*     */       
/* 155 */       result = bout.toString();
/*     */     }
/* 157 */     catch (IOException ex) {
/*     */       
/* 159 */       ex.printStackTrace();
/*     */     }
/*     */     finally {
/*     */       
/* 163 */       closeIn(bin);
/* 164 */       closeOut(bout);
/*     */     } 
/*     */     
/* 167 */     return result;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public static String decrypt(String para) {
/* 179 */     if (para == null)
/*     */     {
/* 181 */       return null;
/*     */     }
/*     */     
/* 184 */     String result = "";
/*     */     
/* 186 */     byte[] bytes = (byte[])null;
/* 187 */     bytes = para.getBytes();
/*     */     
/* 189 */     ByteArrayInputStream bin = null;
/* 190 */     ByteArrayOutputStream bout = null;
/* 191 */     DataInputStream din = null;
/* 192 */     DataOutputStream dout = null;
/*     */ 
/*     */     
/*     */     try {
/* 196 */       bin = new ByteArrayInputStream(bytes);
/* 197 */       bout = new ByteArrayOutputStream();
/* 198 */       din = new DataInputStream(bin);
/* 199 */       dout = new DataOutputStream(bout);
/*     */       
/* 201 */       byte[] data = new byte[2];
/* 202 */       while (din.available() != 0) {
/*     */         
/* 204 */         din.read(data);
/* 205 */         dout.writeByte(simpleCrypt(Integer.parseInt(new String(data), 16)));
/*     */       } 
/*     */       
/* 208 */       result = bout.toString();
/*     */     }
/* 210 */     catch (IOException ex) {
/*     */       
/* 212 */       ex.printStackTrace();
/*     */     }
/*     */     finally {
/*     */       
/* 216 */       closeIn(bin);
/* 217 */       closeOut(bout);
/*     */     } 
/*     */     
/* 220 */     return result;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public static String htmlParaTransfer(String para) {
/* 232 */     if (para == null)
/*     */     {
/* 234 */       return null;
/*     */     }
/*     */     
/* 237 */     String tmpStr = para;
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */     
/* 243 */     tmpStr = replace(tmpStr, "&", "%26");
/*     */     
/* 245 */     return tmpStr;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public static String replace(String srcStr, String from, String to) {
/* 259 */     if (srcStr == null)
/*     */     {
/* 261 */       return null;
/*     */     }
/*     */ 
/*     */     
/* 265 */     StringBuffer resultStr = new StringBuffer();
/*     */     
/* 267 */     String tmpStr = "";
/*     */     
/* 269 */     int index = -1;
/* 270 */     int length = -1;
/*     */ 
/*     */     
/* 273 */     tmpStr = srcStr;
/* 274 */     index = -1 * from.length();
/*     */     
/* 276 */     while ((index = tmpStr.indexOf(from)) != -1) {
/*     */       
/* 278 */       length = tmpStr.length();
/* 279 */       resultStr.append(tmpStr.substring(0, index)).append(to);
/* 280 */       tmpStr = tmpStr.substring(index + from.length(), length);
/*     */     } 
/*     */     
/* 283 */     resultStr.append(tmpStr);
/*     */     
/* 285 */     return resultStr.toString();
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public static String formatMoney(int money) {
/* 297 */     String s = "0";
/* 298 */     if (money > 0)
/*     */     {
/* 300 */       s = String.valueOf(money / 100).concat(".").concat(String.valueOf(money % 100));
/*     */     }
/* 302 */     return "$ " + s;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public static Command getCmdExit() {
/* 310 */     return new Command("EXIT", 7, 0);
/*     */   }
/*     */ 
/*     */   
/*     */   public static Command getCmdBack() {
/* 315 */     return new Command("BACK", 2, 0);
/*     */   }
/*     */ 
/*     */   
/*     */   public static Command getCmdOk() {
/* 320 */     return new Command("OK", 4, 0);
/*     */   }
/*     */ 
/*     */   
/*     */   public static Command getCmdOk(String displayName) {
/* 325 */     return new Command(displayName, 4, 0);
/*     */   }
/*     */ 
/*     */   
/*     */   public static Alert getAlertCfm(String title, String content) {
/* 330 */     return new Alert(title, content, null, AlertType.CONFIRMATION);
/*     */   }
/*     */ 
/*     */   
/*     */   public static Alert getAlertError(String title, String content) {
/* 335 */     return new Alert(title, content, null, AlertType.ERROR);
/*     */   }
/*     */ 
/*     */   
/*     */   public static TextField getPhoneText(String lable, String def) {
/* 340 */     return new TextField(lable, def, 10, 3);
/*     */   }
/*     */ 
/*     */   
/*     */   public static TextField getPwdText(String lable) {
/* 345 */     return new TextField(lable, "", 16, 65536);
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */   
/* 351 */   public static final char[] specail = new char[] { ' ', ',', '.', '!', '?', ';' };
/*     */ 
/*     */ 
/*     */   
/*     */   public static final Vector split(String str, Font font, int maxLength) {
/*     */     try {
/* 357 */       Vector result = new Vector();
/* 358 */       int lastIndex = -1;
/*     */       
/* 360 */       if (str == null || str.length() == 0)
/*     */       {
/* 362 */         throw new NullPointerException("The para str is null.");
/*     */       }
/*     */       
/* 365 */       Vector words = splitByPunctuation(str);
/* 366 */       String word = "";
/* 367 */       String sentence = "";
/* 368 */       for (int idx = 0; idx < words.size(); idx++) {
/*     */         
/* 370 */         word = String.valueOf(words.elementAt(idx));
/* 371 */         lastIndex = result.size() - 1;
/*     */         
/* 373 */         if (lastIndex == -1) {
/*     */           
/* 375 */           result.addElement(word);
/*     */         }
/*     */         else {
/*     */           
/* 379 */           sentence = String.valueOf(result.elementAt(lastIndex));
/* 380 */           if (font.stringWidth(sentence.concat(word)) >= maxLength) {
/*     */             
/* 382 */             result.addElement(word);
/*     */           }
/*     */           else {
/*     */             
/* 386 */             result.setElementAt(sentence.concat(word), lastIndex);
/*     */           } 
/*     */         } 
/*     */       } 
/*     */       
/* 391 */       return result;
/*     */     }
/* 393 */     catch (Exception ex) {
/*     */       
/* 395 */       ex.printStackTrace();
/* 396 */       return null;
/*     */     } 
/*     */   }
/*     */ 
/*     */   
/*     */   private static final boolean isPunctuation(char c) {
/* 402 */     for (int i = 0; i < specail.length; i++) {
/*     */       
/* 404 */       if (c == specail[i])
/*     */       {
/* 406 */         return true;
/*     */       }
/*     */     } 
/*     */     
/* 410 */     return false;
/*     */   }
/*     */ 
/*     */ 
/*     */   
/*     */   private static final Vector splitByPunctuation(String str) {
/*     */     try {
/* 417 */       Vector result = new Vector();
/*     */       
/* 419 */       char[] chars = str.toCharArray();
/*     */       
/* 421 */       String s = "";
/* 422 */       char c = Character.MIN_VALUE;
/* 423 */       for (int i = 0; i < chars.length; i++) {
/*     */         
/* 425 */         c = chars[i];
/* 426 */         s = s.concat(String.valueOf(c));
/* 427 */         if (isPunctuation(c)) {
/*     */           
/* 429 */           result.addElement(s);
/* 430 */           s = "";
/*     */         } 
/*     */       } 
/*     */       
/* 434 */       if (!s.equals(""))
/*     */       {
/* 436 */         result.addElement(s);
/*     */       }
/*     */       
/* 439 */       return result;
/*     */     }
/* 441 */     catch (Exception ex) {
/*     */       
/* 443 */       ex.printStackTrace();
/* 444 */       return null;
/*     */     } 
/*     */   }
/*     */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\licens\\utils\Utils.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */