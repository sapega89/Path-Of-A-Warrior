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
/*    */ public class RelationBlock
/*    */   extends Block
/*    */ {
/*    */   private static final long serialVersionUID = -5172033732555953086L;
/* 19 */   private String relationName = "";
/*    */   
/* 21 */   private int relationFlag = 0;
/*    */ 
/*    */   
/* 24 */   private Array featureIds = new Array();
/*    */   
/*    */   public RelationBlock() {
/* 27 */     setFlag(22000);
/*    */   }
/*    */ 
/*    */   
/*    */   public String getRelationName() {
/* 32 */     return this.relationName;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setRelationName(String relationName) {
/* 37 */     this.relationName = relationName;
/*    */   }
/*    */ 
/*    */   
/*    */   public int getRelationFlag() {
/* 42 */     return this.relationFlag;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setRelationFlag(int relationFlag) {
/* 47 */     this.relationFlag = relationFlag;
/*    */   }
/*    */ 
/*    */   
/*    */   public Array getFeatureIds() {
/* 52 */     return this.featureIds;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setFeatureIds(Array featureIds) {
/* 57 */     this.featureIds = featureIds;
/*    */   }
/*    */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\RelationBlock.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */