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
/*    */ public class BuyBlock
/*    */   extends Block
/*    */ {
/*    */   private static final long serialVersionUID = 8639225189957760040L;
/* 19 */   private int buyFlag = 0;
/*    */   
/* 21 */   private long buyInfo = 0L;
/*    */   
/* 23 */   private long buyUsed = 0L;
/*    */ 
/*    */   
/* 26 */   private long buyRemindKey = 0L;
/*    */   
/* 28 */   private int pNumber = 0;
/*    */   
/* 30 */   private Array productinfo = new Array();
/*    */ 
/*    */   
/*    */   public BuyBlock() {
/* 34 */     setFlag(21200);
/*    */   }
/*    */ 
/*    */   
/*    */   public int getBuyFlag() {
/* 39 */     return this.buyFlag;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setBuyFlag(int buyFlag) {
/* 44 */     this.buyFlag = buyFlag;
/*    */   }
/*    */ 
/*    */   
/*    */   public long getBuyInfo() {
/* 49 */     return this.buyInfo;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setBuyInfo(long buyInfo) {
/* 54 */     this.buyInfo = buyInfo;
/*    */   }
/*    */ 
/*    */   
/*    */   public long getBuyUsed() {
/* 59 */     return this.buyUsed;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setBuyUsed(long buyUsed) {
/* 64 */     this.buyUsed = buyUsed;
/*    */   }
/*    */ 
/*    */   
/*    */   public long getBuyRemindKey() {
/* 69 */     return this.buyRemindKey;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setBuyRemindKey(long buyRemindKey) {
/* 74 */     this.buyRemindKey = buyRemindKey;
/*    */   }
/*    */ 
/*    */   
/*    */   public int getPNumber() {
/* 79 */     return this.pNumber;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setPNumber(int number) {
/* 84 */     this.pNumber = number;
/*    */   }
/*    */ 
/*    */   
/*    */   public Array getProductinfo() {
/* 89 */     return this.productinfo;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setProductinfo(Array productinfo) {
/* 94 */     this.productinfo = productinfo;
/*    */   }
/*    */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\BuyBlock.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */