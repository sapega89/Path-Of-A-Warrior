/*    */ package com.movaya.license.structure;
/*    */ 
/*    */ import java.util.Vector;
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
/*    */ public abstract class Block
/*    */   extends Vector
/*    */ {
/* 20 */   private static int uid = 1;
/*    */ 
/*    */ 
/*    */   
/*    */   static synchronized int getUniquenId() {
/* 25 */     return uid++;
/*    */   }
/*    */   
/* 28 */   private int flag = 0;
/* 29 */   private int length = 0;
/* 30 */   private int id = 0;
/*    */ 
/*    */   
/*    */   public Block() {
/* 34 */     setId(getUniquenId());
/*    */   }
/*    */ 
/*    */   
/*    */   public int getFlag() {
/* 39 */     return this.flag;
/*    */   }
/*    */ 
/*    */   
/*    */   void setFlag(int flag) {
/* 44 */     this.flag = flag;
/*    */   }
/*    */ 
/*    */   
/*    */   public int getLength() {
/* 49 */     return this.length;
/*    */   }
/*    */ 
/*    */   
/*    */   void setLength(int length) {
/* 54 */     this.length = length;
/*    */   }
/*    */ 
/*    */   
/*    */   public int getId() {
/* 59 */     return this.id;
/*    */   }
/*    */ 
/*    */   
/*    */   void setId(int id) {
/* 64 */     this.id = id;
/*    */   }
/*    */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\Block.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */