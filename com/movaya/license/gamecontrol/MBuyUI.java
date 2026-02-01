/*     */ package com.movaya.license.gamecontrol;
/*     */ 
/*     */ import com.movaya.M123456;
/*     */ import com.movaya.license.rms.RmsBiz;
/*     */ import com.movaya.license.structure.Array;
/*     */ import com.movaya.license.structure.CarrierBlock;
/*     */ import com.movaya.license.structure.MLicense;
/*     */ import com.movaya.license.utils.Utils;
/*     */ import javax.microedition.lcdui.Alert;
/*     */ import javax.microedition.lcdui.ChoiceGroup;
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
/*     */ 
/*     */ public class MBuyUI
/*     */   extends Form
/*     */   implements CommandListener
/*     */ {
/*  31 */   public final String ORDER_TYPE_WAP = "waporder";
/*  32 */   public final String ORDER_TYPE_MIDLET = "midorder";
/*     */   
/*  34 */   private M123456 mmidlet = null;
/*     */   
/*  36 */   private Form m_buyForm = null;
/*  37 */   private ChoiceGroup m_carrierGroup = null;
/*  38 */   private ChoiceGroup m_priceGroup = null;
/*  39 */   private TextField m_phoneNumber = null;
/*  40 */   private Command m_exit = null;
/*  41 */   private Command m_ok = null;
/*  42 */   private Command m_back = null;
/*  43 */   RmsBiz rmsBiz = null;
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public MBuyUI(M123456 m) {
/*  49 */     super("");
/*     */     
/*  51 */     this.mmidlet = m;
/*  52 */     this.rmsBiz = this.mmidlet.rmsBiz;
/*     */     
/*  54 */     this.m_exit = Utils.getCmdExit();
/*  55 */     this.m_ok = Utils.getCmdOk("BUY");
/*  56 */     this.m_back = Utils.getCmdBack();
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public MLicense getLic() {
/*  67 */     return this.rmsBiz.getDatLicense();
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
/*  78 */     return MResource.getResource(getLic());
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public void process(boolean isAfterTry) {
/*     */     try {
/*  90 */       if (isAfterTry && !this.rmsBiz.isBuyable(getLic().getDefFeature().getFeatureId())) {
/*     */ 
/*     */         
/*  93 */         this.m_buyForm = new Form((getRes()).buy_trialExpiredTitle);
/*  94 */         this.m_buyForm.append((getRes()).buy_trialExpired);
/*  95 */         this.m_buyForm.addCommand(this.m_exit);
/*     */       
/*     */       }
/*     */       else {
/*     */         
/* 100 */         this.m_buyForm = new Form((getRes()).buy_displayName);
/* 101 */         this.m_buyForm.append((getRes()).buy_pageTitle);
/*     */         
/* 103 */         this.m_phoneNumber = Utils.getPhoneText((getRes()).buy_phoneNoLable, getLic().getBase().getPhoneNo());
/* 104 */         this.m_buyForm.append((Item)this.m_phoneNumber);
/*     */         
/* 106 */         this.m_carrierGroup = new ChoiceGroup((getRes()).buy_carrierLable, 1);
/* 107 */         Array carriers = getLic().getDefReference().getCarriers();
/* 108 */         CarrierBlock carrier = null;
/* 109 */         for (int i = 0; i < carriers.size(); i++) {
/*     */           
/* 111 */           carrier = carriers.elementAt(i);
/* 112 */           this.m_carrierGroup.append(carrier.getCarrierDName(), null);
/*     */         } 
/* 114 */         this.m_buyForm.append((Item)this.m_carrierGroup);
/*     */         
/* 116 */         this.m_priceGroup = new ChoiceGroup((getRes()).buy_priceLable, 1);
/* 117 */         this.m_priceGroup.append(Utils.formatMoney(getLic().getDefFeaSellProduct().getProductPrice()), null);
/* 118 */         this.m_buyForm.append((Item)this.m_priceGroup);
/*     */ 
/*     */         
/* 121 */         if (isAfterTry) {
/*     */           
/* 123 */           this.m_buyForm.setTitle((getRes()).buy_trialExpiredTitle);
/* 124 */           this.m_buyForm.addCommand(this.m_exit);
/*     */         }
/*     */         else {
/*     */           
/* 128 */           this.m_buyForm.addCommand(this.m_back);
/*     */         } 
/* 130 */         this.m_buyForm.addCommand(this.m_ok);
/*     */       } 
/*     */       
/* 133 */       this.m_buyForm.setCommandListener(this);
/* 134 */       this.mmidlet.display.setCurrent((Displayable)this.m_buyForm);
/*     */     }
/* 136 */     catch (Exception e) {
/*     */       
/* 138 */       e.printStackTrace();
/*     */     } 
/*     */   }
/*     */ 
/*     */ 
/*     */   
/*     */   public void commandAction(Command cmd, Displayable dp) {
/*     */     try {
/* 146 */       if (cmd == this.m_exit) {
/*     */ 
/*     */         
/* 149 */         this.mmidlet.notifyDestroyed();
/*     */       }
/* 151 */       else if (cmd == this.m_back) {
/*     */ 
/*     */         
/* 154 */         this.mmidlet.tryNBuy_123456();
/*     */       }
/* 156 */       else if (cmd == this.m_ok) {
/*     */         
/* 158 */         if (this.m_phoneNumber.getString() == null || 10 != this.m_phoneNumber.getString().trim().length()) {
/*     */ 
/*     */           
/* 161 */           this.mmidlet.display.setCurrent(Utils.getAlertError((getRes()).buy_phoneNoErrorTitle, (getRes()).buy_phoneNoError), 
/* 162 */               (Displayable)this.m_buyForm);
/*     */         
/*     */         }
/*     */         else {
/*     */           
/* 167 */           Alert tempAlert = null;
/* 168 */           String carrierDName = "";
/* 169 */           if (getLic().getBase().getCarrierID() <= 0) {
/*     */             
/* 171 */             carrierDName = this.m_carrierGroup.getString(this.m_carrierGroup.getSelectedIndex());
/* 172 */             carrierDName = Utils.htmlParaTransfer(carrierDName);
/*     */           } 
/*     */ 
/*     */           
/* 176 */           int orderStatus = this.rmsBiz.order(getLic().getDefFeature().getFeatureId(), getLic().getDefFeaSell().getBuyFlag(), 
/* 177 */               getLic().getDefFeaSellProduct().getProductId(), carrierDName, this.m_phoneNumber.getString());
/*     */           
/* 179 */           if (orderStatus == -1) {
/*     */ 
/*     */             
/* 182 */             tempAlert = Utils.getAlertCfm((getRes()).buy_connRefusedTitle, (getRes()).buy_connRefused);
/*     */           }
/* 184 */           else if (orderStatus == 3) {
/*     */             
/* 186 */             tempAlert = Utils.getAlertCfm((getRes()).buy_wapOrderTitle, (getRes()).buy_wapOrder);
/*     */           }
/* 188 */           else if (orderStatus == 4) {
/*     */             
/* 190 */             tempAlert = Utils.getAlertCfm((getRes()).buy_wapOrderErrorTitle, (getRes()).buy_wapOrderError);
/*     */           }
/* 192 */           else if (orderStatus == -2) {
/*     */ 
/*     */             
/* 195 */             tempAlert = Utils.getAlertCfm((getRes()).buy_connFailedTitle, (getRes()).buy_connFailed);
/*     */           }
/* 197 */           else if (orderStatus == 1) {
/*     */ 
/*     */             
/* 200 */             tempAlert = Utils.getAlertCfm((getRes()).buy_orderSuccessTitle, (getRes()).buy_orderSuccess);
/*     */           }
/* 202 */           else if (orderStatus == 2) {
/*     */ 
/*     */             
/* 205 */             tempAlert = Utils.getAlertCfm((getRes()).buy_orderExistedTitle, (getRes()).buy_orderExisted);
/*     */           }
/* 207 */           else if (orderStatus == 0) {
/*     */ 
/*     */             
/* 210 */             tempAlert = Utils.getAlertCfm((getRes()).buy_orderFailedTitle, (getRes()).buy_orderFailed);
/*     */           } 
/*     */ 
/*     */           
/* 214 */           tempAlert.setTimeout(-2);
/* 215 */           tempAlert.addCommand(this.m_exit);
/* 216 */           tempAlert.setCommandListener(this);
/* 217 */           this.mmidlet.display.setCurrent((Displayable)tempAlert);
/*     */           
/*     */           return;
/*     */         } 
/*     */       } 
/* 222 */     } catch (Exception ex) {
/*     */       
/* 224 */       ex.printStackTrace();
/*     */     } 
/*     */   }
/*     */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\gamecontrol\MBuyUI.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */