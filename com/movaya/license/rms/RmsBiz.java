/*     */ package com.movaya.license.rms;
/*     */ 
/*     */ import com.movaya.M123456;
/*     */ import com.movaya.license.gamecontrol.MResource;
/*     */ import com.movaya.license.structure.Array;
/*     */ import com.movaya.license.structure.BuyBlock;
/*     */ import com.movaya.license.structure.FeatureBlock;
/*     */ import com.movaya.license.structure.LicenseBlock;
/*     */ import com.movaya.license.structure.MLicense;
/*     */ import com.movaya.license.structure.ProductInfoBlock;
/*     */ import com.movaya.license.structure.TrialBlock;
/*     */ import com.movaya.license.utils.HttpConn;
/*     */ import com.movaya.license.utils.Utils;
/*     */ import java.util.Date;
/*     */ import javax.microedition.lcdui.Alert;
/*     */ import javax.microedition.lcdui.Command;
/*     */ import javax.microedition.lcdui.CommandListener;
/*     */ import javax.microedition.lcdui.Display;
/*     */ import javax.microedition.lcdui.Displayable;
/*     */ import javax.microedition.midlet.MIDlet;
/*     */ import javax.microedition.rms.RecordStoreFullException;
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
/*     */ public final class RmsBiz
/*     */ {
/*     */   public static final String ORDER_TYPE_WAP = "waporder";
/*     */   public static final String ORDER_TYPE_MIDLET = "midorder";
/*  40 */   private RmsManager m_manager = null;
/*  41 */   private MLicense datLicense = null;
/*  42 */   private LicenseBlock datLicenseBlock = null;
/*  43 */   private MLicense rmsLicense = null;
/*  44 */   private LicenseBlock rmsLicenseBlock = null;
/*  45 */   private int orderStatus = -1;
/*  46 */   private int resultStatus = -1;
/*  47 */   private M123456 mmidlet = null;
/*     */ 
/*     */   
/*     */   public MLicense getDatLicense() {
/*  51 */     return this.datLicense;
/*     */   }
/*     */ 
/*     */   
/*     */   public LicenseBlock getDatLicenseBlock() {
/*  56 */     return this.datLicenseBlock;
/*     */   }
/*     */ 
/*     */   
/*     */   public RmsBiz(M123456 mmidlet) throws Exception {
/*  61 */     this.mmidlet = mmidlet;
/*     */ 
/*     */ 
/*     */     
/*     */     try {
/*  66 */       LicenseBlock.useRmsData = false;
/*     */ 
/*     */       
/*  69 */       this.datLicense = new MLicense();
/*  70 */       this.datLicenseBlock = this.datLicense.getLicence();
/*     */ 
/*     */       
/*  73 */       this.m_manager = new RmsManager(this.datLicense.getLicenseId());
/*     */ 
/*     */       
/*  76 */       LicenseBlock.useRmsData = true;
/*     */ 
/*     */       
/*  79 */       this.rmsLicenseBlock = this.m_manager.query(this.datLicenseBlock.getLicenseId());
/*  80 */       this.rmsLicense = new MLicense(this.rmsLicenseBlock);
/*     */ 
/*     */     
/*     */     }
/*  84 */     catch (RecordStoreFullException ex) {
/*     */       
/*  86 */       String title = (MResource.getResource(this.datLicense)).exception_rms_fullTitle;
/*  87 */       String msg = (MResource.getResource(this.datLicense)).exception_rms_full;
/*     */       
/*  89 */       Alert alert = null;
/*  90 */       alert = Utils.getAlertError(title, msg);
/*  91 */       Display.getDisplay((MIDlet)this.mmidlet).setCurrent((Displayable)alert);
/*  92 */       alert.addCommand(Utils.getCmdExit());
/*  93 */       alert.setTimeout(-2);
/*  94 */       alert.setCommandListener(new CommandListener(this, mmidlet)
/*     */           {
/*     */             public void commandAction(Command cmd, Displayable d) {
/*  97 */               if (cmd.getCommandType() == 7)
/*     */               {
/*  99 */                 this.val$mmidlet.notifyDestroyed(); } 
/*     */             }
/*     */             final RmsBiz this$0;
/*     */             private final M123456 val$mmidlet;
/*     */           });
/* 104 */       System.out.println("--->3");
/* 105 */       mmidlet.startAble = false;
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
/*     */   
/*     */   public boolean isPlayable(String featureID) {
/*     */     try {
/* 120 */       if (this.rmsLicenseBlock == null) {
/*     */ 
/*     */         
/* 123 */         this.m_manager.update(this.datLicenseBlock);
/*     */ 
/*     */         
/* 126 */         this.rmsLicenseBlock = this.m_manager.query(this.datLicenseBlock.getLicenseId());
/*     */ 
/*     */         
/* 129 */         this.rmsLicense = new MLicense(this.rmsLicenseBlock);
/*     */         
/* 131 */         return false;
/*     */       } 
/*     */ 
/*     */ 
/*     */       
/* 136 */       BuyBlock buyBlock = null;
/* 137 */       buyBlock = getPurchasedBlock(featureID);
/*     */ 
/*     */       
/* 140 */       if (buyBlock == null)
/*     */       {
/* 142 */         return false;
/*     */       }
/*     */ 
/*     */ 
/*     */ 
/*     */       
/* 148 */       if (isPurchaseSuccess(buyBlock)) {
/*     */ 
/*     */         
/* 151 */         if (isUsable(buyBlock))
/*     */         {
/* 153 */           return true;
/*     */         }
/*     */ 
/*     */ 
/*     */         
/* 158 */         return false;
/*     */       } 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */       
/* 165 */       String url = MResource.getResource(this.datLicense).getOrderStatusURL();
/* 166 */       this.resultStatus = HttpConn.visit(url);
/*     */       
/* 168 */       if (this.resultStatus == 1) {
/*     */ 
/*     */         
/* 171 */         buyBlock.setBuyFlag(buyBlock.getBuyFlag() + 4);
/* 172 */         updateLicense();
/*     */ 
/*     */         
/* 175 */         return true;
/*     */       } 
/* 177 */       return false;
/*     */ 
/*     */ 
/*     */     
/*     */     }
/* 182 */     catch (Exception ex) {
/*     */       
/* 184 */       ex.printStackTrace();
/* 185 */       return false;
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
/*     */   
/*     */   public boolean isTriable(String featureID) {
/*     */     try {
/* 200 */       if (this.rmsLicenseBlock == null) {
/*     */ 
/*     */         
/* 203 */         this.m_manager.update(this.datLicenseBlock);
/*     */ 
/*     */         
/* 206 */         this.rmsLicenseBlock = this.m_manager.query(this.datLicenseBlock.getLicenseId());
/*     */         
/* 208 */         return true;
/*     */       } 
/*     */ 
/*     */ 
/*     */       
/* 213 */       Array trialArr = null;
/* 214 */       trialArr = this.rmsLicense.getFeaTrials(featureID);
/*     */       
/* 216 */       TrialBlock trialBlock = null;
/* 217 */       int flag = -1;
/* 218 */       long info = -1L;
/* 219 */       long used = -1L;
/* 220 */       for (int i = 0; i < trialArr.size(); i++) {
/*     */         
/* 222 */         trialBlock = trialArr.elementAt(i);
/*     */         
/* 224 */         flag = trialBlock.getTrialFlag();
/* 225 */         info = trialBlock.getTrialInfo();
/* 226 */         used = trialBlock.getTrialUsed();
/*     */ 
/*     */         
/* 229 */         if ((flag & 0x1) == 1)
/*     */         {
/*     */ 
/*     */           
/* 233 */           if ((flag & 0x10) == 16) {
/*     */             
/* 235 */             if (info > used)
/*     */             {
/*     */               
/* 238 */               return true;
/*     */             }
/*     */           }
/* 241 */           else if ((flag & 0x20) == 32) {
/*     */             
/* 243 */             if (info > (new Date()).getTime())
/*     */             {
/* 245 */               return true;
/*     */             }
/*     */           } 
/*     */         }
/*     */       } 
/* 250 */       return false;
/*     */     
/*     */     }
/* 253 */     catch (Exception ex) {
/*     */       
/* 255 */       ex.printStackTrace();
/* 256 */       return false;
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
/*     */   public boolean isBuyable(String featureID) {
/*     */     try {
/* 270 */       if (this.rmsLicenseBlock == null) {
/*     */ 
/*     */         
/* 273 */         this.m_manager.update(this.datLicenseBlock);
/*     */ 
/*     */         
/* 276 */         this.rmsLicenseBlock = this.m_manager.query(this.datLicenseBlock.getLicenseId());
/*     */         
/* 278 */         return true;
/*     */       } 
/*     */ 
/*     */ 
/*     */       
/* 283 */       BuyBlock buyBlock = null;
/* 284 */       buyBlock = getPurchasedBlock(featureID);
/*     */ 
/*     */ 
/*     */       
/* 288 */       if (buyBlock == null)
/*     */       {
/* 290 */         return true;
/*     */       }
/*     */ 
/*     */ 
/*     */ 
/*     */       
/* 296 */       if (isPurchaseSuccess(buyBlock)) {
/*     */ 
/*     */         
/* 299 */         if (isUsable(buyBlock))
/*     */         {
/* 301 */           return false;
/*     */         }
/*     */ 
/*     */ 
/*     */         
/* 306 */         return true;
/*     */       } 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */       
/* 313 */       if (isOrderFromMidlet(buyBlock))
/*     */       {
/* 315 */         return false;
/*     */       }
/*     */ 
/*     */ 
/*     */       
/* 320 */       return true;
/*     */ 
/*     */ 
/*     */ 
/*     */     
/*     */     }
/* 326 */     catch (Exception ex) {
/*     */       
/* 328 */       ex.printStackTrace();
/* 329 */       return false;
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
/*     */   
/*     */   public boolean isUnlockable(String featureID) {
/*     */     try {
/* 344 */       BuyBlock buyBlock = null;
/* 345 */       buyBlock = getPurchasedBlock(featureID);
/*     */ 
/*     */       
/* 348 */       if (buyBlock == null)
/*     */       {
/* 350 */         return false;
/*     */       }
/*     */ 
/*     */ 
/*     */ 
/*     */       
/* 356 */       if (isOrderFromWap(buyBlock))
/*     */       {
/* 358 */         return true;
/*     */       }
/*     */ 
/*     */       
/* 362 */       return false;
/*     */ 
/*     */     
/*     */     }
/* 366 */     catch (Exception ex) {
/*     */       
/* 368 */       ex.printStackTrace();
/* 369 */       return false;
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
/*     */   
/*     */   public boolean isOrderProcess(String featureID) {
/*     */     try {
/* 384 */       BuyBlock buyBlock = null;
/* 385 */       buyBlock = getPurchasedBlock(featureID);
/*     */ 
/*     */       
/* 388 */       if (buyBlock == null)
/*     */       {
/* 390 */         return false;
/*     */       }
/*     */ 
/*     */ 
/*     */ 
/*     */       
/* 396 */       if (!isOrderFromWap(buyBlock))
/*     */       {
/* 398 */         return true;
/*     */       }
/*     */ 
/*     */       
/* 402 */       return false;
/*     */ 
/*     */     
/*     */     }
/* 406 */     catch (Exception ex) {
/*     */       
/* 408 */       ex.printStackTrace();
/* 409 */       return false;
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
/*     */   
/*     */   private BuyBlock getDatPurchasedBlock(String featureID, int buyFlag) {
/* 423 */     int purchaseFlag = -1;
/*     */ 
/*     */     
/* 426 */     Array purchaseArray = null;
/* 427 */     purchaseArray = this.datLicense.getFeaSells(featureID);
/*     */     
/* 429 */     BuyBlock buyBlock = null;
/* 430 */     for (int i = 0; i < purchaseArray.size(); i++) {
/*     */ 
/*     */       
/* 433 */       buyBlock = purchaseArray.elementAt(i);
/*     */ 
/*     */       
/* 436 */       purchaseFlag = buyBlock.getBuyFlag();
/*     */ 
/*     */       
/* 439 */       if (purchaseFlag == buyFlag)
/*     */       {
/* 441 */         return buyBlock;
/*     */       }
/*     */     } 
/*     */     
/* 445 */     return null;
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
/*     */   private BuyBlock getPurchasedBlock(String featureID) {
/* 457 */     int purchaseFlag = -1;
/*     */ 
/*     */     
/* 460 */     Array purchaseArray = null;
/* 461 */     purchaseArray = this.rmsLicense.getFeaSells(featureID);
/*     */     
/* 463 */     BuyBlock buyBlock = null;
/* 464 */     for (int i = 0; i < purchaseArray.size(); i++) {
/*     */ 
/*     */       
/* 467 */       buyBlock = purchaseArray.elementAt(i);
/*     */ 
/*     */       
/* 470 */       purchaseFlag = buyBlock.getBuyFlag();
/*     */ 
/*     */       
/* 473 */       if ((purchaseFlag & 0x1) == 1)
/*     */       {
/* 475 */         return buyBlock;
/*     */       }
/*     */     } 
/*     */     
/* 479 */     return null;
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
/*     */   private ProductInfoBlock getProductInfoBlock(BuyBlock buyBlock, String productId) {
/*     */     try {
/* 493 */       if (buyBlock == null)
/*     */       {
/* 495 */         throw new NullPointerException("The parameter buyBlock is null.");
/*     */       }
/*     */       
/* 498 */       ProductInfoBlock productInfoBlock = null;
/* 499 */       Array array = buyBlock.getProductinfo();
/* 500 */       for (int i = 0; i < array.size(); i++) {
/*     */         
/* 502 */         productInfoBlock = array.elementAt(i);
/*     */         
/* 504 */         if (productInfoBlock.getProductId().equals(productId))
/*     */         {
/* 506 */           return productInfoBlock;
/*     */         }
/*     */       } 
/*     */       
/* 510 */       return null;
/*     */     }
/* 512 */     catch (Exception ex) {
/*     */       
/* 514 */       ex.printStackTrace();
/* 515 */       return null;
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
/*     */   
/*     */   private boolean isPurchaseSuccess(BuyBlock buyBlock) {
/* 529 */     if (buyBlock == null)
/*     */     {
/* 531 */       return false;
/*     */     }
/*     */ 
/*     */     
/* 535 */     int purchaseFlag = -1;
/*     */ 
/*     */     
/* 538 */     purchaseFlag = buyBlock.getBuyFlag();
/*     */ 
/*     */     
/* 541 */     if ((purchaseFlag & 0x4) == 4)
/*     */     {
/* 543 */       return true;
/*     */     }
/*     */ 
/*     */     
/* 547 */     return false;
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
/*     */   private boolean isUsable(BuyBlock buyBlock) {
/* 559 */     int flag = -1;
/* 560 */     long info = -1L;
/* 561 */     long used = -1L;
/*     */     
/* 563 */     flag = buyBlock.getBuyFlag();
/* 564 */     info = buyBlock.getBuyInfo();
/* 565 */     used = buyBlock.getBuyUsed();
/*     */ 
/*     */     
/* 568 */     if ((flag & 0x40) == 64)
/*     */     {
/* 570 */       return true;
/*     */     }
/*     */ 
/*     */     
/* 574 */     if ((flag & 0x80) == 128) {
/*     */       
/* 576 */       if (info > used)
/*     */       {
/* 578 */         return true;
/*     */ 
/*     */ 
/*     */       
/*     */       }
/*     */ 
/*     */ 
/*     */     
/*     */     }
/* 587 */     else if ((flag & 0x100) == 256) {
/*     */       
/* 589 */       if (info > (new Date()).getTime())
/*     */       {
/* 591 */         return true;
/*     */       }
/*     */     } 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */     
/* 600 */     return false;
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
/*     */   private boolean isOrderFromWap(BuyBlock buyBlock) throws Exception {
/*     */     try {
/* 615 */       int buyFlag = -1;
/* 616 */       buyFlag = buyBlock.getBuyFlag();
/*     */       
/* 618 */       if ((buyFlag & 0x400) == 1024)
/*     */       {
/* 620 */         return true;
/*     */       }
/*     */ 
/*     */       
/* 624 */       return false;
/*     */     
/*     */     }
/* 627 */     catch (Exception ex) {
/*     */       
/* 629 */       throw ex;
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
/*     */ 
/*     */   
/*     */   private boolean isOrderFromMidlet(BuyBlock buyBlock) throws Exception {
/*     */     try {
/* 645 */       int flag = -1;
/* 646 */       flag = buyBlock.getBuyFlag();
/*     */ 
/*     */       
/* 649 */       if ((flag & 0x200) == 512)
/*     */       {
/* 651 */         return true;
/*     */       }
/*     */ 
/*     */       
/* 655 */       return false;
/*     */     
/*     */     }
/* 658 */     catch (Exception ex) {
/*     */       
/* 660 */       throw ex;
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
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public int order(String featureID, int buyFlag, String productId, String carrierName, String phoneNo) throws Exception {
/* 678 */     this.orderStatus = HttpConn.visit(MResource.getResource(this.datLicense).getOrderURL(carrierName, phoneNo, "midorder"));
/*     */     
/* 680 */     if (this.orderStatus == -1 && this.mmidlet.isAdvMIDP()) {
/*     */       
/*     */       try {
/*     */ 
/*     */         
/* 685 */         if (this.mmidlet.wapCheckout(MResource.getResource(this.datLicense).getOrderURL(carrierName, phoneNo, "waporder")))
/*     */         {
/*     */           
/* 688 */           this.orderStatus = 3;
/*     */         
/*     */         }
/*     */         else
/*     */         {
/* 693 */           this.orderStatus = 4;
/*     */         }
/*     */       
/* 696 */       } catch (Exception e) {
/*     */ 
/*     */         
/* 699 */         this.orderStatus = 4;
/*     */       } 
/*     */     }
/*     */ 
/*     */     
/* 704 */     BuyBlock buyBlock = null;
/* 705 */     buyBlock = getDatPurchasedBlock(featureID, buyFlag);
/*     */     
/* 707 */     if (this.orderStatus == 1 || this.orderStatus == 3) {
/*     */ 
/*     */       
/* 710 */       clearBuyModeUsed(featureID);
/*     */ 
/*     */       
/* 713 */       buyBlock.setBuyFlag(buyBlock.getBuyFlag() + 2 + 1);
/* 714 */       if (this.orderStatus == 1) {
/*     */         
/* 716 */         buyBlock.setBuyFlag(buyBlock.getBuyFlag() + 512);
/*     */       }
/*     */       else {
/*     */         
/* 720 */         buyBlock.setBuyFlag(buyBlock.getBuyFlag() + 1024);
/*     */       } 
/*     */ 
/*     */       
/* 724 */       ProductInfoBlock productInfoBlock = null;
/* 725 */       productInfoBlock = getProductInfoBlock(buyBlock, productId);
/*     */ 
/*     */       
/* 728 */       long buyInfo = -1L;
/* 729 */       buyInfo = productInfoBlock.getProductKey();
/* 730 */       buyBlock.setBuyInfo(buyInfo);
/*     */ 
/*     */       
/* 733 */       buyBlock.setBuyUsed(0L);
/*     */ 
/*     */       
/* 736 */       this.rmsLicense.getFeaSells(featureID).addElement(buyBlock);
/*     */ 
/*     */       
/* 739 */       updateLicense();
/*     */     } 
/*     */     
/* 742 */     return this.orderStatus;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   private void clearBuyModeUsed(String featureID) {
/* 752 */     BuyBlock buyBlock = null;
/* 753 */     buyBlock = getPurchasedBlock(featureID);
/*     */     
/* 755 */     if (buyBlock != null)
/*     */     {
/* 757 */       buyBlock.setBuyFlag(buyBlock.getBuyFlag() - 1);
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
/*     */   public void updateTry(String featureID) throws Exception {
/* 769 */     FeatureBlock featureBlock = null;
/* 770 */     featureBlock = this.rmsLicense.getFeatureByID(featureID);
/*     */     
/* 772 */     Array trialArray = null;
/* 773 */     trialArray = featureBlock.getTrial();
/*     */     
/* 775 */     TrialBlock trialBlock = null;
/* 776 */     int trialFlag = -1;
/* 777 */     long trialUsed = -1L;
/* 778 */     for (int i = 0; i < trialArray.size(); i++) {
/*     */       
/* 780 */       trialBlock = trialArray.elementAt(i);
/*     */       
/* 782 */       trialFlag = trialBlock.getTrialFlag();
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */       
/* 788 */       if ((trialFlag & 0x10) == 16) {
/*     */         
/* 790 */         trialUsed = trialBlock.getTrialUsed() + 1L;
/* 791 */         trialBlock.setTrialUsed(trialUsed);
/*     */         
/* 793 */         updateLicense();
/*     */         return;
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
/*     */   public void updateBuy(String featureID) throws Exception {
/* 807 */     FeatureBlock featureBlock = null;
/* 808 */     featureBlock = this.rmsLicense.getFeatureByID(featureID);
/*     */     
/* 810 */     Array buyArray = null;
/* 811 */     buyArray = featureBlock.getBuy();
/*     */     
/* 813 */     BuyBlock buyBlock = null;
/* 814 */     int buyFlag = -1;
/* 815 */     long buyUsed = -1L;
/* 816 */     for (int i = 0; i < buyArray.size(); i++) {
/*     */       
/* 818 */       buyBlock = buyArray.elementAt(i);
/*     */       
/* 820 */       buyFlag = buyBlock.getFlag();
/*     */       
/* 822 */       if ((buyFlag & 0x1) != 1)
/*     */       {
/*     */ 
/*     */ 
/*     */         
/* 827 */         if ((buyFlag & 0x10) == 16) {
/*     */           
/* 829 */           buyUsed = buyBlock.getBuyUsed() + 1L;
/* 830 */           buyBlock.setBuyUsed(++buyUsed);
/*     */           
/* 832 */           updateLicense();
/*     */           return;
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
/*     */   public void unlock(String featureID) throws Exception {
/* 847 */     BuyBlock buyBlock = null;
/* 848 */     buyBlock = getPurchasedBlock(featureID);
/*     */ 
/*     */     
/* 851 */     buyBlock.setBuyFlag(buyBlock.getBuyFlag() + 4);
/* 852 */     updateLicense();
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public void updateLicense() throws Exception {
/* 863 */     this.m_manager.update(this.rmsLicenseBlock);
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public long getTrialTimeLimit() {
/* 873 */     long defTimeLimit = 900000L;
/*     */     
/* 875 */     Array trialArray = null;
/* 876 */     trialArray = this.datLicense.getDefFeature().getTrial();
/*     */     
/* 878 */     TrialBlock trialBlock = null;
/* 879 */     int flag = -1;
/* 880 */     for (int i = 0; i < trialArray.size(); i++) {
/*     */       
/* 882 */       trialBlock = trialArray.elementAt(i);
/*     */       
/* 884 */       flag = trialBlock.getTrialFlag();
/* 885 */       if ((flag & 0x40) == 64) {
/*     */         
/* 887 */         defTimeLimit = trialBlock.getTrialInfo();
/*     */         
/*     */         break;
/*     */       } 
/*     */     } 
/* 892 */     return defTimeLimit;
/*     */   }
/*     */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\rms\RmsBiz.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */