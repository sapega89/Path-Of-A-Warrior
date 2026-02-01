/*     */ package com.movaya.license.structure;
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
/*     */ public class MLicense
/*     */ {
/*  16 */   LicenseBlock licenseBk = null;
/*     */ 
/*     */   
/*     */   public MLicense() {
/*  20 */     this.licenseBk = (new LicenseBlock()).resolve();
/*     */   }
/*     */ 
/*     */   
/*     */   public MLicense(LicenseBlock licenseBlock) {
/*  25 */     this.licenseBk = licenseBlock;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public LicenseBlock getLicence() {
/*  36 */     return this.licenseBk;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public int getLicenseId() {
/*  46 */     return this.licenseBk.getBaseBlock().getUniqueKey();
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public BaseBlock getBase() {
/*  57 */     return this.licenseBk.getBaseBlock();
/*     */   }
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
/*     */   public ReferenceBlock getDefReference() {
/*  80 */     return this.licenseBk.getReferenceArray().elementAt(0);
/*     */   }
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
/*     */   public FeatureRelationBlock getDefFeatureRelation() {
/* 103 */     return this.licenseBk.getFeatrueRelationArray().elementAt(0);
/*     */   }
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
/*     */   public FeatureBlock getDefFeature() {
/* 127 */     return getDefFeatureRelation().getFeature().elementAt(0);
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public FeatureBlock getFeatureByID(String featureID) {
/* 139 */     FeatureBlock feature = null;
/* 140 */     FeatureBlock tempFeature = null;
/* 141 */     Array featureArr = null;
/* 142 */     Array featureRelationArr = null;
/*     */     
/*     */     try {
/* 145 */       featureRelationArr = getLicence().getFeatrueRelationArray();
/*     */       
/* 147 */       for (int i = 0; i < featureRelationArr.size(); i++)
/*     */       {
/* 149 */         featureArr = ((FeatureRelationBlock)featureRelationArr.elementAt(i)).getFeature();
/* 150 */         for (int j = 0; j < featureArr.size(); j++) {
/*     */           
/* 152 */           tempFeature = featureArr.elementAt(j);
/* 153 */           if (tempFeature.getFeatureId().equals(featureID)) {
/*     */             
/* 155 */             feature = tempFeature;
/*     */             
/*     */             break;
/*     */           } 
/*     */         } 
/* 160 */         if (feature != null) {
/*     */           break;
/*     */         }
/*     */       }
/*     */     
/*     */     }
/* 166 */     catch (Exception e) {
/*     */       
/* 168 */       e.printStackTrace();
/*     */     } 
/*     */ 
/*     */     
/* 172 */     return feature;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public Array getFeaTrials(String featureId) {
/* 183 */     return getFeatureByID(featureId).getTrial();
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public Array getFeaSells(String featureId) {
/* 194 */     return getFeatureByID(featureId).getBuy();
/*     */   }
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
/*     */   public BuyBlock getDefFeaSell() {
/* 218 */     return getDefFeature().getBuy().elementAt(0);
/*     */   }
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
/*     */   public ProductInfoBlock getDefFeaSellProduct() {
/* 242 */     return getDefFeaSell().getProductinfo().elementAt(0);
/*     */   }
/*     */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\MLicense.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */