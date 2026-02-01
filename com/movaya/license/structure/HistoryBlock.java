/*    */ package com.movaya.license.structure;
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ public class HistoryBlock
/*    */   extends Block
/*    */ {
/*    */   private static final long serialVersionUID = -1873562775536019816L;
/* 19 */   private int buyFlag = 0;
/*    */   
/* 21 */   private long buyInfo = 0L;
/*    */   
/* 23 */   private long buyTime = 0L;
/*    */   
/* 25 */   private int productPrice = 0;
/*    */   
/* 27 */   private String productId = "";
/*    */   
/* 29 */   private String referenceId = "";
/*    */ 
/*    */   
/*    */   public HistoryBlock() {
/* 33 */     setFlag(30000);
/*    */   }
/*    */ 
/*    */   
/*    */   public int getBuyFlag() {
/* 38 */     return this.buyFlag;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setBuyFlag(int buyFlag) {
/* 43 */     this.buyFlag = buyFlag;
/*    */   }
/*    */ 
/*    */   
/*    */   public long getBuyInfo() {
/* 48 */     return this.buyInfo;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setBuyInfo(long buyInfo) {
/* 53 */     this.buyInfo = buyInfo;
/*    */   }
/*    */ 
/*    */   
/*    */   public long getBuyTime() {
/* 58 */     return this.buyTime;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setBuyTime(long buyTime) {
/* 63 */     this.buyTime = buyTime;
/*    */   }
/*    */ 
/*    */   
/*    */   public int getProductPrice() {
/* 68 */     return this.productPrice;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setProductPrice(int productPrice) {
/* 73 */     this.productPrice = productPrice;
/*    */   }
/*    */ 
/*    */   
/*    */   public String getProductId() {
/* 78 */     return this.productId;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setProductId(String productId) {
/* 83 */     this.productId = productId;
/*    */   }
/*    */ 
/*    */   
/*    */   public String getReferenceId() {
/* 88 */     return this.referenceId;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setReferenceId(String referenceId) {
/* 93 */     this.referenceId = referenceId;
/*    */   }
/*    */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\HistoryBlock.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */