/*     */ package com.movaya.license.structure;
/*     */ 
/*     */ import java.io.InputStream;
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ public class LicenseBlock
/*     */   extends Array
/*     */ {
/*     */   private static final long serialVersionUID = -6530362629533780852L;
/*     */   public static boolean useRmsData = false;
/*     */   
/*     */   public byte[] generate() {
/*  35 */     Generate generate = null;
/*  36 */     generate = new Generate();
/*     */     
/*  38 */     return generate.generateArrays(this, 0, 1);
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public LicenseBlock resolve() {
/*  49 */     InputStream in = null;
/*     */ 
/*     */     
/*     */     try {
/*  53 */       in = getClass().getResourceAsStream("/lic.dat");
/*     */     }
/*  55 */     catch (Exception e) {
/*     */       
/*  57 */       e.printStackTrace();
/*     */     } 
/*  59 */     Resolve r = new Resolve();
/*  60 */     return r.resolve(in);
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public BaseBlock getBaseBlock() {
/*  70 */     BaseBlock baseBlock = null;
/*     */     
/*  72 */     Object obj = null;
/*  73 */     Array tmpArray = null;
/*  74 */     Object tmpObj = null;
/*  75 */     for (int i = 0; i < size(); i++) {
/*     */       
/*  77 */       obj = elementAt(i);
/*     */       
/*  79 */       if (obj instanceof Array) {
/*     */         
/*  81 */         tmpArray = (Array)obj;
/*  82 */         for (int j = 0; j < tmpArray.size(); j++)
/*     */         {
/*  84 */           tmpObj = tmpArray.elementAt(j);
/*     */           
/*  86 */           if (tmpObj instanceof BaseBlock)
/*     */           {
/*  88 */             baseBlock = (BaseBlock)tmpObj;
/*     */           }
/*     */         }
/*     */       
/*  92 */       } else if (obj instanceof BaseBlock) {
/*     */         
/*  94 */         baseBlock = (BaseBlock)obj;
/*     */       } 
/*     */     } 
/*     */     
/*  98 */     return baseBlock;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public Array getFeatrueRelationArray() {
/* 108 */     Array array = null;
/*     */     
/* 110 */     Object obj = null;
/* 111 */     Array tmpArray = null;
/* 112 */     Object tmpObj = null;
/* 113 */     for (int i = 0; i < size(); i++) {
/*     */       
/* 115 */       obj = elementAt(i);
/*     */       
/* 117 */       if (obj instanceof Array) {
/*     */         
/* 119 */         tmpArray = (Array)obj;
/* 120 */         for (int j = 0; j < tmpArray.size(); j++) {
/*     */           
/* 122 */           tmpObj = tmpArray.elementAt(j);
/*     */           
/* 124 */           if (tmpObj instanceof FeatureRelationBlock)
/*     */           {
/* 126 */             array = tmpArray;
/*     */           }
/*     */         } 
/*     */       } 
/*     */     } 
/*     */     
/* 132 */     return array;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public Array getHistoryArray() {
/* 142 */     Array array = null;
/*     */     
/* 144 */     Object obj = null;
/* 145 */     Array tmpArray = null;
/* 146 */     Object tmpObj = null;
/* 147 */     for (int i = 0; i < size(); i++) {
/*     */       
/* 149 */       obj = elementAt(i);
/*     */       
/* 151 */       if (obj instanceof Array) {
/*     */         
/* 153 */         tmpArray = (Array)obj;
/* 154 */         for (int j = 0; j < tmpArray.size(); j++) {
/*     */           
/* 156 */           tmpObj = tmpArray.elementAt(j);
/*     */           
/* 158 */           if (tmpObj instanceof HistoryBlock)
/*     */           {
/* 160 */             array = tmpArray;
/*     */           }
/*     */         } 
/*     */       } 
/*     */     } 
/*     */     
/* 166 */     return array;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public Array getReferenceArray() {
/* 176 */     Array array = null;
/*     */     
/* 178 */     Object obj = null;
/* 179 */     Array tmpArray = null;
/* 180 */     Object tmpObj = null;
/* 181 */     for (int i = 0; i < size(); i++) {
/*     */       
/* 183 */       obj = elementAt(i);
/*     */       
/* 185 */       if (obj instanceof Array) {
/*     */         
/* 187 */         tmpArray = (Array)obj;
/* 188 */         for (int j = 0; j < tmpArray.size(); j++) {
/*     */           
/* 190 */           tmpObj = tmpArray.elementAt(j);
/*     */           
/* 192 */           if (tmpObj instanceof ReferenceBlock)
/*     */           {
/* 194 */             array = tmpArray;
/*     */           }
/*     */         } 
/*     */       } 
/*     */     } 
/*     */     
/* 200 */     return array;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public int getLicenseId() {
/* 208 */     return getBaseBlock().getUniqueKey();
/*     */   }
/*     */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\LicenseBlock.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */