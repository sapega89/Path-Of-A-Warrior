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
/*    */ public class ProductInfoBlock
/*    */   extends Block
/*    */ {
/*    */   private static final long serialVersionUID = 1174677898189959408L;
/* 19 */   private String productId = "";
/*    */   
/* 21 */   private int productPrice = 0;
/*    */   
/* 23 */   private long productKey = -1L;
/*    */   
/* 25 */   private String displayName = "";
/*    */ 
/*    */   
/*    */   public ProductInfoBlock() {
/* 29 */     setFlag(21210);
/*    */   }
/*    */ 
/*    */   
/*    */   public String getProductId() {
/* 34 */     return this.productId;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setProductId(String productId) {
/* 39 */     this.productId = productId;
/*    */   }
/*    */ 
/*    */   
/*    */   public int getProductPrice() {
/* 44 */     return this.productPrice;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setProductPrice(int productPrice) {
/* 49 */     this.productPrice = productPrice;
/*    */   }
/*    */ 
/*    */   
/*    */   public long getProductKey() {
/* 54 */     return this.productKey;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setProductKey(long productKey) {
/* 59 */     this.productKey = productKey;
/*    */   }
/*    */ 
/*    */   
/*    */   public String getDisplayName() {
/* 64 */     return this.displayName;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setDisplayName(String displayName) {
/* 69 */     this.displayName = displayName;
/*    */   }
/*    */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\ProductInfoBlock.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */