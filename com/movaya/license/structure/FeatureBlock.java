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
/*    */ public class FeatureBlock
/*    */   extends Block
/*    */ {
/*    */   private static final long serialVersionUID = -4330673063290158632L;
/* 20 */   private String featureId = "";
/*    */ 
/*    */   
/* 23 */   private String featureName = "";
/*    */ 
/*    */   
/* 26 */   private Array trial = new Array();
/*    */ 
/*    */   
/* 29 */   private Array buy = new Array();
/*    */ 
/*    */   
/*    */   public FeatureBlock() {
/* 33 */     setFlag(21000);
/*    */   }
/*    */ 
/*    */   
/*    */   public String getFeatureId() {
/* 38 */     return this.featureId;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setFeatureId(String featureId) {
/* 43 */     this.featureId = featureId;
/*    */   }
/*    */ 
/*    */   
/*    */   public String getFeatureName() {
/* 48 */     return this.featureName;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setFeatureName(String featureName) {
/* 53 */     this.featureName = featureName;
/*    */   }
/*    */ 
/*    */   
/*    */   public Array getTrial() {
/* 58 */     return this.trial;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setTrial(Array trial) {
/* 63 */     this.trial = trial;
/*    */   }
/*    */ 
/*    */   
/*    */   public Array getBuy() {
/* 68 */     return this.buy;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setBuy(Array buy) {
/* 73 */     this.buy = buy;
/*    */   }
/*    */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\FeatureBlock.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */