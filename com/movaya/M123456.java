/*     */ package com.movaya;
/*     */ 
/*     */ import com.movaya.license.gamecontrol.MBuyUI;
/*     */ import com.movaya.license.rms.RmsBiz;
/*     */ import javax.microedition.lcdui.Display;
/*     */ import javax.microedition.lcdui.Displayable;
/*     */ import javax.microedition.midlet.MIDlet;
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
/*     */ public abstract class M123456
/*     */   extends MIDlet
/*     */ {
/*  23 */   public static Displayable movaya = null;
/*  24 */   public Display display = Display.getDisplay(this);
/*     */ 
/*     */   
/*  27 */   public RmsBiz rmsBiz = null;
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public boolean startAble = true;
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public M123456() {
/*     */     try {
/*  40 */       this.rmsBiz = new RmsBiz(this);
/*     */     }
/*  42 */     catch (Exception ex) {
/*     */       
/*  44 */       ex.printStackTrace();
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
/*     */   public void tryNBuy_123456() {
/*  56 */     (new MTnbCall(this)).process();
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public void purchase_123456(boolean b) {
/*  67 */     (new MBuyUI(this)).process(b);
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
/*     */   public boolean wapCheckout(String url) {
/*  79 */     return false;
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
/*     */   public boolean isAdvMIDP() {
/*  91 */     return false;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public void start() {
/* 101 */     constructor_123456();
/* 102 */     startApp_123456();
/*     */   }
/*     */   
/*     */   protected abstract void constructor_123456();
/*     */   
/*     */   protected abstract void startApp_123456();
/*     */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\M123456.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */