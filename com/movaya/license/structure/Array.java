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
/*    */ 
/*    */ public class Array
/*    */   extends Vector
/*    */ {
/*    */   private static final long serialVersionUID = -4594004506159070086L;
/* 22 */   private int length = 0;
/*    */ 
/*    */ 
/*    */   
/* 26 */   private int dataLen = 0;
/*    */ 
/*    */   
/*    */   public Array() {
/* 30 */     this.dataLen = 0;
/*    */   }
/*    */ 
/*    */   
/*    */   public Array(int dataLen) {
/* 35 */     this.dataLen = dataLen;
/*    */   }
/*    */ 
/*    */   
/*    */   public int getLength() {
/* 40 */     return this.length;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setLength(int length) {
/* 45 */     this.length = length;
/*    */   }
/*    */ 
/*    */   
/*    */   public int getDataLen() {
/* 50 */     return this.dataLen;
/*    */   }
/*    */ 
/*    */   
/*    */   public void setDataLen(int dataLen) {
/* 55 */     this.dataLen = dataLen;
/*    */   }
/*    */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\Array.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */