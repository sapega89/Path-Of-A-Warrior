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
/*    */ 
/*    */ public class FeatureRelationBlock
/*    */   extends Block
/*    */ {
/*    */   private static final long serialVersionUID = -8881342914993895271L;
/* 20 */   private Array feature = new Array();
/*    */ 
/*    */   
/* 23 */   private Array relation = new Array();
/*    */ 
/*    */   
/*    */   public FeatureRelationBlock() {
/* 27 */     setFlag(20000);
/*    */   }
/*    */ 
/*    */   
/*    */   public Array getFeature() {
/* 32 */     return this.feature;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setFeature(Array feature) {
/* 37 */     this.feature = feature;
/*    */   }
/*    */ 
/*    */   
/*    */   public Array getRelation() {
/* 42 */     return this.relation;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setRelation(Array relation) {
/* 47 */     this.relation = relation;
/*    */   }
/*    */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\FeatureRelationBlock.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */