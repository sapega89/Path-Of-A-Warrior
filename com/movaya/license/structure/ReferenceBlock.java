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
/*    */ public class ReferenceBlock
/*    */   extends Block
/*    */ {
/* 18 */   private Array carriers = new Array();
/*    */ 
/*    */   
/*    */   public ReferenceBlock() {
/* 22 */     setFlag(40000);
/*    */   }
/*    */ 
/*    */   
/*    */   public Array getCarriers() {
/* 27 */     return this.carriers;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setCarriers(Array carriers) {
/* 32 */     this.carriers = carriers;
/*    */   }
/*    */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\ReferenceBlock.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */