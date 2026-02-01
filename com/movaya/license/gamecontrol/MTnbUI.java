/*     */ package com.movaya.license.gamecontrol;
/*     */ 
/*     */ import com.movaya.M123456;
/*     */ import com.movaya.license.rms.RmsBiz;
/*     */ import com.movaya.license.utils.Utils;
/*     */ import java.util.Vector;
/*     */ import javax.microedition.lcdui.Canvas;
/*     */ import javax.microedition.lcdui.Command;
/*     */ import javax.microedition.lcdui.CommandListener;
/*     */ import javax.microedition.lcdui.Displayable;
/*     */ import javax.microedition.lcdui.Font;
/*     */ import javax.microedition.lcdui.Graphics;
/*     */ import javax.microedition.lcdui.Image;
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
/*     */ public class MTnbUI
/*     */   extends Canvas
/*     */   implements CommandListener
/*     */ {
/*  29 */   private M123456 mmidlet = null;
/*     */   
/*     */   private static final int ROWSPACING = 5;
/*     */   
/*  33 */   private int focusInd = -1;
/*  34 */   private int firstInd = 0;
/*  35 */   private int lastInd = 0;
/*     */   private Font titleFont;
/*     */   private Font defFont;
/*     */   private Font focusFont;
/*     */   private int bgColor;
/*  40 */   private Vector m_cmdList = null; private int titleColor; private int defColor; private int focusColor; private int titleBgColor; private int focusBgColor;
/*  41 */   private Vector m_strList = null;
/*     */   
/*  43 */   private Command m_exit = null;
/*  44 */   private Command m_tnbok = null;
/*     */   
/*  46 */   private RmsBiz rmsBiz = null;
/*  47 */   private String m_defFID = null;
/*  48 */   private long timeLimit = -1L;
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public MTnbUI(M123456 m) {
/*  54 */     this.mmidlet = m;
/*  55 */     this.rmsBiz = this.mmidlet.rmsBiz;
/*  56 */     this.m_defFID = this.rmsBiz.getDatLicense().getDefFeature().getFeatureId();
/*  57 */     this.timeLimit = this.rmsBiz.getTrialTimeLimit();
/*     */ 
/*     */     
/*  60 */     this.m_cmdList = new Vector();
/*  61 */     this.m_strList = new Vector();
/*  62 */     this.titleFont = Font.getFont(Font.getDefaultFont().getFace(), 1, Font.getDefaultFont().getSize());
/*  63 */     this.defFont = Font.getFont(Font.getDefaultFont().getFace(), 1, Font.getDefaultFont().getSize());
/*  64 */     this.focusFont = Font.getFont(Font.getDefaultFont().getFace(), 1, Font.getDefaultFont().getSize());
/*  65 */     this.titleColor = 0;
/*  66 */     this.defColor = 0;
/*  67 */     this.focusColor = 10158080;
/*  68 */     this.titleBgColor = 11184810;
/*  69 */     this.focusBgColor = 14606046;
/*  70 */     this.bgColor = 16777215;
/*     */ 
/*     */     
/*  73 */     this.m_exit = Utils.getCmdExit();
/*  74 */     this.m_tnbok = Utils.getCmdOk();
/*     */     
/*  76 */     addCommand(this.m_exit);
/*  77 */     setCommandListener(this);
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   private MResource getRes() {
/*  88 */     return MResource.getResource(this.rmsBiz.getDatLicense());
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
/*     */   public void process() {
/*     */     try {
/* 101 */       if (!this.rmsBiz.isPlayable(this.m_defFID))
/*     */       {
/*     */ 
/*     */ 
/*     */         
/* 106 */         this.mmidlet.start();
/*     */       
/*     */       }
/*     */       else
/*     */       {
/*     */         
/* 112 */         if (this.rmsBiz.isTriable(this.m_defFID))
/*     */         {
/*     */           
/* 115 */           addList((getRes()).tnb_tryLable);
/*     */         }
/*     */         
/* 118 */         if (this.rmsBiz.isBuyable(this.m_defFID)) {
/*     */ 
/*     */           
/* 121 */           addList((getRes()).tnb_buyLable);
/*     */         }
/* 123 */         else if (this.rmsBiz.isOrderProcess(this.m_defFID)) {
/*     */ 
/*     */           
/* 126 */           addStr((getRes()).tnb_orderProcessLable);
/*     */         } 
/*     */         
/* 129 */         if (this.rmsBiz.isUnlockable(this.m_defFID))
/*     */         {
/*     */           
/* 132 */           addList((getRes()).tnb_unlockLable);
/*     */         }
/*     */         
/* 135 */         if (this.m_cmdList.size() > 0)
/*     */         {
/* 137 */           addCommand(this.m_tnbok);
/*     */         }
/*     */ 
/*     */         
/* 141 */         this.mmidlet.display.setCurrent((Displayable)this);
/*     */       }
/*     */     
/* 144 */     } catch (Exception e) {
/*     */       
/* 146 */       e.printStackTrace();
/*     */     } 
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public void commandAction(Command cmd, Displayable dp) {
/* 155 */     if (cmd == this.m_exit) {
/*     */       
/* 157 */       this.mmidlet.notifyDestroyed();
/*     */     }
/* 159 */     else if (cmd == this.m_tnbok) {
/*     */ 
/*     */       
/* 162 */       proCmd();
/*     */     } 
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   protected void proCmd() {
/* 173 */     String focus = this.m_cmdList.elementAt(this.focusInd).toString();
/*     */     
/*     */     try {
/* 176 */       if (focus.equals((getRes()).tnb_tryLable))
/*     */       {
/*     */         
/* 179 */         this.rmsBiz.updateTry(this.m_defFID);
/*     */ 
/*     */         
/* 182 */         this.mmidlet.start();
/*     */ 
/*     */         
/* 185 */         (new Controller(this, this.mmidlet, this.timeLimit)).start();
/*     */       }
/* 187 */       else if (focus.equals((getRes()).tnb_buyLable))
/*     */       {
/*     */         
/* 190 */         this.mmidlet.purchase_123456(false);
/*     */       }
/* 192 */       else if (focus.equals((getRes()).tnb_unlockLable))
/*     */       {
/*     */         
/* 195 */         (new MUnlockUI(this.mmidlet)).unlock();
/*     */       }
/* 197 */       else if (focus.equals((getRes()).tnb_orderProcessLable))
/*     */       {
/*     */         
/* 200 */         this.mmidlet.notifyDestroyed();
/*     */       }
/*     */     
/* 203 */     } catch (Exception e) {
/*     */ 
/*     */       
/* 206 */       e.printStackTrace();
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
/*     */   protected void addList(Object item) {
/* 218 */     this.m_cmdList.addElement(item);
/*     */   }
/*     */ 
/*     */   
/*     */   protected void addStr(Object str) {
/* 223 */     this.m_strList.addElement(str);
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   protected void paint(Graphics g) {
/* 232 */     int y = 0;
/* 233 */     int x = 0;
/*     */ 
/*     */     
/* 236 */     g.setColor(this.bgColor);
/* 237 */     g.fillRect(0, 0, getWidth(), getHeight());
/*     */ 
/*     */     
/* 240 */     g.setColor(this.titleBgColor);
/* 241 */     g.fillRect(0, y, getWidth(), this.titleFont.getHeight());
/* 242 */     g.setFont(this.titleFont);
/* 243 */     g.setColor(this.titleColor);
/* 244 */     x = (getWidth() - this.titleFont.stringWidth((getRes()).tnb_displayName)) / 2;
/* 245 */     g.drawString((getRes()).tnb_displayName, x, 0, 0);
/* 246 */     y += this.titleFont.getHeight();
/*     */ 
/*     */     
/* 249 */     Object obj = null;
/* 250 */     String str = null;
/* 251 */     Image image = null;
/* 252 */     Vector v = null;
/*     */     
/* 254 */     for (int i = 0; i < this.m_cmdList.size(); i++) {
/*     */       
/* 256 */       obj = this.m_cmdList.elementAt(i);
/* 257 */       y += 5;
/*     */       
/* 259 */       if (obj instanceof Image) {
/*     */ 
/*     */         
/* 262 */         image = (Image)obj;
/*     */         
/* 264 */         x = (getWidth() - image.getWidth()) / 2;
/* 265 */         g.drawImage(image, x, y, 0);
/* 266 */         y += image.getHeight();
/*     */       }
/* 268 */       else if (obj instanceof String) {
/*     */ 
/*     */         
/* 271 */         str = (String)obj;
/*     */         
/* 273 */         v = Utils.split(str, this.focusFont, getWidth());
/*     */         
/* 275 */         if (-1 == this.focusInd) {
/*     */           
/* 277 */           this.firstInd = i;
/* 278 */           this.focusInd = i;
/*     */         } 
/* 280 */         this.lastInd = i;
/*     */         
/* 282 */         if (i == this.focusInd) {
/*     */ 
/*     */           
/* 285 */           g.setColor(this.focusBgColor);
/* 286 */           g.fillRect(0, y, getWidth(), this.focusFont.getHeight() * v.size());
/*     */ 
/*     */ 
/*     */ 
/*     */           
/* 291 */           g.setColor(this.focusColor);
/* 292 */           g.setFont(this.focusFont);
/* 293 */           for (int j = 0; j < v.size(); j++)
/*     */           {
/* 295 */             x = (1 == v.size()) ? ((getWidth() - this.focusFont.stringWidth(v.elementAt(j).toString())) / 2) : 2;
/* 296 */             g.drawString(v.elementAt(j).toString(), x, y, 0);
/* 297 */             y += this.focusFont.getHeight();
/*     */           }
/*     */         
/*     */         } else {
/*     */           
/* 302 */           g.setColor(this.defColor);
/* 303 */           g.setFont(this.defFont);
/* 304 */           x = (getWidth() - this.defFont.stringWidth(str)) / 2;
/* 305 */           for (int j = 0; j < v.size(); j++) {
/*     */             
/* 307 */             x = (1 == v.size()) ? ((getWidth() - this.focusFont.stringWidth(v.elementAt(j).toString())) / 2) : 2;
/* 308 */             g.drawString(v.elementAt(j).toString(), x, y, 0);
/* 309 */             y += this.defFont.getHeight();
/*     */           } 
/*     */         } 
/*     */       } 
/*     */     } 
/*     */ 
/*     */     
/* 316 */     for (int h = 0; h < this.m_strList.size(); h++) {
/*     */       
/* 318 */       y += 5;
/*     */ 
/*     */       
/* 321 */       str = this.m_strList.elementAt(h);
/*     */       
/* 323 */       v = Utils.split(str, this.focusFont, getWidth());
/*     */       
/* 325 */       g.setColor(this.defColor);
/* 326 */       g.setFont(this.defFont);
/* 327 */       for (int m = 0; m < v.size(); m++) {
/*     */         
/* 329 */         x = (1 == v.size()) ? ((getWidth() - this.focusFont.stringWidth(v.elementAt(m).toString())) / 2) : 2;
/* 330 */         g.drawString(v.elementAt(m).toString(), x, y, 0);
/* 331 */         y += this.defFont.getHeight();
/*     */       } 
/*     */     } 
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   protected void keyPressed(int keyCode) {
/* 341 */     int key = getGameAction(keyCode);
/*     */     
/* 343 */     if (key == 1 || keyCode == 50) {
/*     */       
/* 345 */       if (this.focusInd == this.firstInd) {
/*     */         
/* 347 */         this.focusInd = this.lastInd;
/*     */       }
/*     */       else {
/*     */         
/* 351 */         this.focusInd--;
/*     */       } 
/* 353 */       repaint();
/*     */     }
/* 355 */     else if (key == 6 || keyCode == 56) {
/*     */       
/* 357 */       if (this.focusInd == this.lastInd) {
/*     */         
/* 359 */         this.focusInd = this.firstInd;
/*     */       }
/*     */       else {
/*     */         
/* 363 */         this.focusInd++;
/*     */       } 
/* 365 */       repaint();
/*     */     }
/* 367 */     else if (key == 8 || keyCode == 53) {
/*     */ 
/*     */       
/* 370 */       proCmd();
/*     */     } 
/*     */   }
/*     */   
/*     */   class Controller
/*     */     extends Thread
/*     */   {
/*     */     private long timeLimit;
/*     */     M123456 m_midlet;
/*     */     final MTnbUI this$0;
/*     */     
/*     */     public Controller(MTnbUI this$0, M123456 mm, long timeLimit) {
/* 382 */       this.this$0 = this$0; this.timeLimit = -1L;
/*     */       this.m_midlet = null;
/* 384 */       this.timeLimit = timeLimit;
/* 385 */       this.m_midlet = mm;
/*     */     }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */     
/*     */     public synchronized void run() {
/*     */       try {
/*     */         return;
/* 396 */       } catch (Exception e) {
/*     */         
/* 398 */         e.printStackTrace();
/*     */       } 
/*     */       while (true)
/*     */         return; 
/*     */     }
/*     */   }
/*     */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\gamecontrol\MTnbUI.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */