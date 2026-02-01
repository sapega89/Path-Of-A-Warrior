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
/*     */ 
/*     */ public class BaseBlock
/*     */   extends Block
/*     */ {
/*     */   private static final long serialVersionUID = -6569135570105011029L;
/*  19 */   private int uniqueKey = 0;
/*     */   
/*  21 */   private String referenceId = "";
/*     */   
/*  23 */   private String unlockKey = "";
/*     */   
/*  25 */   private String appEnv = "";
/*     */   
/*  27 */   private long verifyKey = 0L;
/*     */   
/*  29 */   private long createTime = 0L;
/*     */   
/*  31 */   private long updateTime = 0L;
/*     */ 
/*     */   
/*  34 */   private String licenseServerURL = "";
/*     */   
/*  36 */   private int deviceID = -1;
/*     */   
/*  38 */   private int carrierID = -1;
/*     */   
/*  40 */   private String phoneNo = "";
/*     */   
/*  42 */   private String shortCode = "";
/*     */ 
/*     */   
/*     */   public BaseBlock() {
/*  46 */     setFlag(10000);
/*     */   }
/*     */ 
/*     */   
/*     */   public int getUniqueKey() {
/*  51 */     return this.uniqueKey;
/*     */   }
/*     */ 
/*     */   
/*     */   public void setUniqueKey(int uniqueKey) {
/*  56 */     this.uniqueKey = uniqueKey;
/*     */   }
/*     */ 
/*     */   
/*     */   public String getReferenceId() {
/*  61 */     return this.referenceId;
/*     */   }
/*     */ 
/*     */   
/*     */   public void setReferenceId(String referenceId) {
/*  66 */     this.referenceId = referenceId;
/*     */   }
/*     */ 
/*     */   
/*     */   public String getUnlockKey() {
/*  71 */     return this.unlockKey;
/*     */   }
/*     */ 
/*     */   
/*     */   public void setUnlockKey(String unlockKey) {
/*  76 */     this.unlockKey = unlockKey;
/*     */   }
/*     */ 
/*     */   
/*     */   public String getAppEnv() {
/*  81 */     return this.appEnv;
/*     */   }
/*     */ 
/*     */   
/*     */   public void setAppEnv(String appEnv) {
/*  86 */     this.appEnv = appEnv;
/*     */   }
/*     */ 
/*     */   
/*     */   public long getVerifyKey() {
/*  91 */     return this.verifyKey;
/*     */   }
/*     */ 
/*     */   
/*     */   public void setVerifyKey(long verifyKey) {
/*  96 */     this.verifyKey = verifyKey;
/*     */   }
/*     */ 
/*     */   
/*     */   public long getCreateTime() {
/* 101 */     return this.createTime;
/*     */   }
/*     */ 
/*     */   
/*     */   public void setCreateTime(long createTime) {
/* 106 */     this.createTime = createTime;
/*     */   }
/*     */ 
/*     */   
/*     */   public long getUpdateTime() {
/* 111 */     return this.updateTime;
/*     */   }
/*     */ 
/*     */   
/*     */   public void setUpdateTime(long updateTime) {
/* 116 */     this.updateTime = updateTime;
/*     */   }
/*     */ 
/*     */   
/*     */   public String getLicenseServerURL() {
/* 121 */     return this.licenseServerURL;
/*     */   }
/*     */ 
/*     */   
/*     */   public void setLicenseServerURL(String licenseServerURL) {
/* 126 */     this.licenseServerURL = licenseServerURL;
/*     */   }
/*     */ 
/*     */   
/*     */   public int getDeviceID() {
/* 131 */     return this.deviceID;
/*     */   }
/*     */ 
/*     */   
/*     */   public void setDeviceID(int deviceID) {
/* 136 */     this.deviceID = deviceID;
/*     */   }
/*     */ 
/*     */   
/*     */   public int getCarrierID() {
/* 141 */     return this.carrierID;
/*     */   }
/*     */ 
/*     */   
/*     */   public void setCarrierID(int carrierID) {
/* 146 */     this.carrierID = carrierID;
/*     */   }
/*     */ 
/*     */   
/*     */   public String getPhoneNo() {
/* 151 */     return this.phoneNo;
/*     */   }
/*     */ 
/*     */   
/*     */   public void setPhoneNo(String phoneNo) {
/* 156 */     this.phoneNo = phoneNo;
/*     */   }
/*     */ 
/*     */   
/*     */   public String getShortCode() {
/* 161 */     return this.shortCode;
/*     */   }
/*     */ 
/*     */   
/*     */   public void setShortCode(String shortCode) {
/* 166 */     this.shortCode = shortCode;
/*     */   }
/*     */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\BaseBlock.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */