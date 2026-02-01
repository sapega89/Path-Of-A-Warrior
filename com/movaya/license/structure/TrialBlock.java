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
/*    */ public class TrialBlock
/*    */   extends Block
/*    */ {
/*    */   private static final long serialVersionUID = 3202500337024383845L;
/* 18 */   private int trialFlag = 0;
/*    */   
/* 20 */   private long trialInfo = 0L;
/*    */   
/* 22 */   private long trialUsed = 0L;
/*    */ 
/*    */   
/* 25 */   private long trialRemindKey = 0L;
/*    */   
/*    */   public TrialBlock() {
/* 28 */     setFlag(21100);
/*    */   }
/*    */ 
/*    */   
/*    */   public int getTrialFlag() {
/* 33 */     return this.trialFlag;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setTrialFlag(int trialFlag) {
/* 38 */     this.trialFlag = trialFlag;
/*    */   }
/*    */ 
/*    */   
/*    */   public long getTrialInfo() {
/* 43 */     return this.trialInfo;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setTrialInfo(long trialInfo) {
/* 48 */     this.trialInfo = trialInfo;
/*    */   }
/*    */ 
/*    */   
/*    */   public long getTrialUsed() {
/* 53 */     return this.trialUsed;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setTrialUsed(long trialUsed) {
/* 58 */     this.trialUsed = trialUsed;
/*    */   }
/*    */ 
/*    */   
/*    */   public long getTrialRemindKey() {
/* 63 */     return this.trialRemindKey;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setTrialRemindKey(long trialRemindKey) {
/* 68 */     this.trialRemindKey = trialRemindKey;
/*    */   }
/*    */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\TrialBlock.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */