/*     */ package com.movaya.license.gamecontrol;
/*     */ 
/*     */ import com.movaya.license.structure.MLicense;
/*     */ import com.movaya.license.utils.Utils;
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
/*     */ public class MResource
/*     */ {
/*  18 */   private static MLicense license = null;
/*     */ 
/*     */   
/*     */   public static MResource getResource(MLicense mlic) {
/*  22 */     MResource mRes = null;
/*     */     
/*     */     try {
/*  25 */       license = mlic;
/*  26 */       mRes = (mRes == null) ? new MResource() : mRes;
/*     */     }
/*  28 */     catch (Exception e) {
/*     */       
/*  30 */       e.printStackTrace();
/*     */     } 
/*     */ 
/*     */     
/*  34 */     return mRes;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*  40 */   public String tnb_displayName = "Movaya TryNBuy";
/*  41 */   public String tnb_tryNBuyGroupLable = "";
/*  42 */   public String tnb_tryLable = "Try it now";
/*  43 */   public String tnb_buyLable = "Buy it now";
/*  44 */   public String tnb_orderProcessLable = "We're processing your order, restart game after you receive our confirmation message.";
/*  45 */   public String tnb_unlockLable = "Activate with passcode";
/*  46 */   public String tnb_unlockInputLable = "Passcode";
/*  47 */   public String tnb_unlockFailedTitle = "Unlock Failed";
/*  48 */   public String tnb_unlockFailed = "Your passcode is invaild, please use an valid passcode";
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*  54 */   public String buy_displayName = "Buy It Now";
/*  55 */   public String buy_trialExpiredTitle = "Trial Expired";
/*  56 */   public String buy_trialExpired = "Your trial this time has expired.";
/*  57 */   public String buy_pageTitle = "Please provide the following info:";
/*  58 */   public String buy_phoneNoLable = "Phone Number:";
/*  59 */   public String buy_carrierGroupLable = "";
/*  60 */   public String buy_carrierLable = "Carrier:";
/*  61 */   public String buy_priceLable = "Price:";
/*  62 */   public String buy_orderSuccessTitle = "Order Successful";
/*  63 */   public String buy_orderSuccess = "Thank you. We're processing your order. You'll receive a confirmation message from " + 
/*  64 */     license.getBase().getShortCode() + ". Please following instructions if your carrier is AT&T.";
/*  65 */   public String buy_orderFailedTitle = "Order Failed";
/*  66 */   public String buy_orderFailed = "Your order failed, please contact customer support: support@movaya.com";
/*  67 */   public String buy_orderExistedTitle = "Order Result";
/*  68 */   public String buy_orderExisted = "Thank you. We're processing your order.";
/*  69 */   public String buy_connRefusedTitle = "Connection Refused";
/*  70 */   public String buy_connRefused = "To buy the game requires a network connection. Network connection is not available on your phone. Please call your service provider to enable it.";
/*  71 */   public String buy_connFailedTitle = "Connection Failed";
/*  72 */   public String buy_connFailed = "Our service is not able to process your order now, please try it later.";
/*  73 */   public String buy_phoneNoErrorTitle = "Invalid Phone Number";
/*  74 */   public String buy_phoneNoError = "Phone number is invalid, please provide a valid phone number";
/*  75 */   public String buy_wapOrderTitle = "Order Result";
/*  76 */   public String buy_wapOrder = "Thank you. If you see the success info on wap page, you order is sucessful, or you'd better exit and buy again.";
/*  77 */   public String buy_wapOrderErrorTitle = "Order Failed";
/*  78 */   public String buy_wapOrderError = "Your order failed. WAP platform request in the game is not available on your phone. Please call your service provider to enable it.";
/*     */   
/*  80 */   public String exception_rms_fullTitle = "RMS Full";
/*  81 */   public String exception_rms_full = "Your Record Management System is full, please remove some game first.";
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
/*     */   public String getOrderURL(String cName, String phoneNo, String type) {
/*  94 */     String path = "o=".concat("checkout").concat("&om=").concat(type).concat("&lid=").concat(String.valueOf(license.getBase().getUniqueKey()))
/*  95 */       .concat("&cid=").concat(String.valueOf(license.getBase().getCarrierID())).concat("&cdn=").concat(cName).concat("&did=").concat(
/*  96 */         String.valueOf(license.getBase().getDeviceID())).concat("&pn=").concat(phoneNo);
/*     */     
/*  98 */     return license.getBase().getLicenseServerURL().concat("mm=").concat(Utils.encrypt(path));
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public String getOrderStatusURL() {
/* 109 */     String path = "o=".concat("getResult").concat("&lid=").concat(String.valueOf(license.getBase().getUniqueKey()));
/*     */     
/* 111 */     return license.getBase().getLicenseServerURL().concat("mm=").concat(Utils.encrypt(path));
/*     */   }
/*     */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\gamecontrol\MResource.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */