/*     */ package com.movaya.license.gamecontrol;
/*     */ 
/*     */ import com.movaya.M123456;
/*     */ import com.movaya.license.rms.RmsBiz;
/*     */ import com.movaya.license.utils.Utils;
/*     */ import javax.microedition.lcdui.Command;
/*     */ import javax.microedition.lcdui.CommandListener;
/*     */ import javax.microedition.lcdui.Displayable;
/*     */ import javax.microedition.lcdui.Form;
/*     */ import javax.microedition.lcdui.Item;
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
/*     */ public class MUnlockUI
/*     */   extends Form
/*     */   implements CommandListener
/*     */ {
/*  25 */   private M123456 mmidlet = null;
/*  26 */   private Form m_ulkForm = null;
/*  27 */   private TextField m_unlockKey = null;
/*  28 */   private Command m_back = null;
/*  29 */   private Command m_unlock = null;
/*  30 */   RmsBiz rmsBiz = null;
/*  31 */   String m_defFID = null;
/*     */ 
/*     */ 
/*     */   
/*     */   public MUnlockUI(M123456 m) {
/*  36 */     super("");
/*     */     
/*  38 */     this.mmidlet = m;
/*  39 */     this.rmsBiz = m.rmsBiz;
/*  40 */     this.m_defFID = this.rmsBiz.getDatLicense().getDefFeature().getFeatureId();
/*     */ 
/*     */     
/*  43 */     this.m_back = Utils.getCmdBack();
/*  44 */     this.m_unlock = Utils.getCmdOk("UNLOCK");
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public MResource getRes() {
/*  55 */     return MResource.getResource(this.rmsBiz.getDatLicense());
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
/*     */   public void unlock() {
/*     */     try {
/*  68 */       this.m_ulkForm = new Form((getRes()).tnb_unlockLable);
/*     */ 
/*     */       
/*  71 */       this.m_unlockKey = Utils.getPwdText((getRes()).tnb_unlockInputLable);
/*  72 */       this.m_ulkForm.append((Item)this.m_unlockKey);
/*     */ 
/*     */       
/*  75 */       this.m_ulkForm.addCommand(this.m_unlock);
/*  76 */       this.m_ulkForm.addCommand(this.m_back);
/*     */ 
/*     */       
/*  79 */       this.m_ulkForm.setCommandListener(this);
/*     */       
/*  81 */       this.mmidlet.display.setCurrent((Displayable)this.m_ulkForm);
/*     */     }
/*  83 */     catch (Exception e) {
/*     */       
/*  85 */       e.printStackTrace();
/*     */     } 
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public void commandAction(Command cmd, Displayable dp) {
/*     */     try {
/*  96 */       if (cmd == this.m_back) {
/*     */         
/*  98 */         (new MTnbUI(this.mmidlet)).process();
/*     */       }
/* 100 */       else if (cmd == this.m_unlock) {
/*     */ 
/*     */         
/* 103 */         if (this.m_unlockKey.getString().equals(this.rmsBiz.getDatLicense().getBase().getUnlockKey()))
/*     */         {
/*     */ 
/*     */           
/* 107 */           this.rmsBiz.unlock(this.m_defFID);
/*     */           
/* 109 */           this.mmidlet.start();
/*     */         
/*     */         }
/*     */         else
/*     */         {
/* 114 */           this.mmidlet.display.setCurrent(Utils.getAlertError((getRes()).tnb_unlockFailedTitle, (getRes()).tnb_unlockFailed), 
/* 115 */               (Displayable)this.m_ulkForm);
/*     */         }
/*     */       
/*     */       } 
/* 119 */     } catch (Exception ex) {
/*     */       
/* 121 */       ex.printStackTrace();
/*     */     } 
/*     */   }
/*     */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\gamecontrol\MUnlockUI.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */