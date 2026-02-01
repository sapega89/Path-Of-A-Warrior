/*     */ package com.movaya.license.rms;
/*     */ 
/*     */ import com.movaya.license.structure.LicenseBlock;
/*     */ import com.movaya.license.structure.Resolve;
/*     */ import javax.microedition.rms.RecordStore;
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
/*     */ public final class RmsManager
/*     */ {
/*     */   private static final String RECORD_STORM_NAME_PREFIX = "movaya.license";
/*  21 */   private RecordStore m_recordStore = null;
/*  22 */   private int recordIndex = 1;
/*  23 */   private String recordStoreName = "";
/*     */ 
/*     */   
/*  26 */   private Resolve resolve = new Resolve();
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
/*     */   public RmsManager(int licenseId) throws Exception {
/*  38 */     this.recordStoreName = "movaya.license".concat(String.valueOf(licenseId));
/*     */     
/*  40 */     this.m_recordStore = RecordStore.openRecordStore(this.recordStoreName, true);
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
/*     */   private void insert(LicenseBlock lic) throws Exception {
/*  53 */     if (lic == null)
/*     */     {
/*  55 */       throw new NullPointerException("The parameter licenseBlock is null.");
/*     */     }
/*     */ 
/*     */     
/*  59 */     byte[] data = lic.generate();
/*     */ 
/*     */     
/*  62 */     this.m_recordStore.addRecord(data, 0, data.length);
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
/*     */   public LicenseBlock query(int licenseId) throws Exception {
/*     */     try {
/* 110 */       if (getRecordSize() > 0) {
/*     */ 
/*     */         
/* 113 */         LicenseBlock rmslic = null;
/*     */ 
/*     */         
/* 116 */         rmslic = this.resolve.resolve(this.m_recordStore.getRecord(this.recordIndex));
/*     */ 
/*     */         
/* 119 */         if (rmslic.getLicenseId() == licenseId)
/*     */         {
/*     */           
/* 122 */           return rmslic;
/*     */         }
/*     */ 
/*     */         
/* 126 */         return null;
/*     */       } 
/*     */ 
/*     */ 
/*     */       
/* 131 */       throw new Exception("RecordStore ".concat(this.recordStoreName).concat(" is empty."));
/*     */     
/*     */     }
/* 134 */     catch (Exception ex) {
/*     */ 
/*     */       
/* 137 */       return null;
/*     */     } 
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
/*     */   public void update(LicenseBlock lic) throws Exception {
/* 151 */     if (getRecordSize() > 0) {
/*     */ 
/*     */       
/* 154 */       LicenseBlock rmslic = null;
/*     */ 
/*     */       
/* 157 */       rmslic = this.resolve.resolve(this.m_recordStore.getRecord(this.recordIndex));
/*     */ 
/*     */       
/* 160 */       if (rmslic.getLicenseId() == lic.getLicenseId())
/*     */       {
/* 162 */         byte[] data = lic.generate();
/*     */         
/* 164 */         this.m_recordStore.setRecord(this.recordIndex, data, 0, data.length);
/*     */       }
/*     */     
/*     */     }
/*     */     else {
/*     */       
/* 170 */       insert(lic);
/*     */     } 
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
/*     */   private int getRecordSize() {
/*     */     try {
/* 184 */       return this.m_recordStore.getNumRecords();
/*     */     }
/* 186 */     catch (Exception e) {
/*     */ 
/*     */       
/* 189 */       return 0;
/*     */     } 
/*     */   }
/*     */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\rms\RmsManager.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */