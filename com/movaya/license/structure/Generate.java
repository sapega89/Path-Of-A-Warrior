/*     */ package com.movaya.license.structure;
/*     */ 
/*     */ import com.movaya.license.utils.Utils;
/*     */ import java.io.ByteArrayOutputStream;
/*     */ import java.io.DataOutputStream;
/*     */ import java.io.IOException;
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
/*     */ public final class Generate
/*     */ {
/*     */   byte[] generateArrays(Array array, int dataLen, int flag) {
/*  33 */     ByteArrayOutputStream baos = null;
/*  34 */     baos = new ByteArrayOutputStream();
/*     */     
/*  36 */     DataOutputStream dos = null;
/*  37 */     dos = new DataOutputStream(baos);
/*     */     
/*  39 */     Object obj = null;
/*     */ 
/*     */     
/*     */     try {
/*  43 */       for (int i = 0; i < array.size(); i++) {
/*     */         
/*  45 */         obj = array.elementAt(i);
/*     */ 
/*     */         
/*  48 */         if (obj instanceof Array) {
/*     */           
/*  50 */           dos.write(generateArrays((Array)obj, 0, 1));
/*     */         
/*     */         }
/*  53 */         else if (obj instanceof Block) {
/*     */           
/*  55 */           dos.write(generateBlocks((Block)obj));
/*     */         
/*     */         }
/*  58 */         else if (obj instanceof String) {
/*     */           
/*  60 */           dos.writeUTF((String)obj);
/*     */         
/*     */         }
/*     */         else {
/*     */           
/*  65 */           dos.write(((String)obj).getBytes());
/*     */         } 
/*     */       } 
/*     */ 
/*     */       
/*  70 */       return getArrayResult(baos.toByteArray(), dataLen, flag);
/*     */     }
/*  72 */     catch (IOException e) {
/*     */       
/*  74 */       e.printStackTrace();
/*  75 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/*  80 */       Utils.closeOut(baos);
/*  81 */       Utils.closeOut(dos);
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
/*     */   
/*     */   private byte[] getArrayResult(byte[] data, int dataLen, int flag) {
/*  96 */     ByteArrayOutputStream baos = null;
/*  97 */     baos = new ByteArrayOutputStream();
/*     */     
/*  99 */     DataOutputStream dos = null;
/* 100 */     dos = new DataOutputStream(baos);
/*     */ 
/*     */ 
/*     */     
/*     */     try {
/* 105 */       dos.writeInt(flag);
/*     */ 
/*     */       
/* 108 */       dos.writeInt(data.length);
/*     */ 
/*     */       
/* 111 */       dos.writeInt(dataLen);
/*     */ 
/*     */       
/* 114 */       dos.write(data);
/*     */ 
/*     */       
/* 117 */       return baos.toByteArray();
/*     */     }
/* 119 */     catch (IOException e) {
/*     */       
/* 121 */       e.printStackTrace();
/* 122 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 127 */       Utils.closeOut(baos);
/* 128 */       Utils.closeOut(dos);
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
/*     */   private byte[] getBlockResult(byte[] data, int flag) {
/* 141 */     ByteArrayOutputStream baos = null;
/* 142 */     baos = new ByteArrayOutputStream();
/*     */     
/* 144 */     DataOutputStream dos = null;
/* 145 */     dos = new DataOutputStream(baos);
/*     */ 
/*     */ 
/*     */     
/*     */     try {
/* 150 */       dos.writeInt(flag);
/*     */ 
/*     */       
/* 153 */       dos.writeInt(data.length);
/*     */ 
/*     */       
/* 156 */       dos.write(data);
/*     */ 
/*     */       
/* 159 */       return baos.toByteArray();
/*     */     }
/* 161 */     catch (IOException e) {
/*     */       
/* 163 */       e.printStackTrace();
/* 164 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 169 */       Utils.closeOut(baos);
/* 170 */       Utils.closeOut(dos);
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
/*     */   private byte[] generateBlocks(Block block) {
/* 182 */     byte[] buf = (byte[])null;
/*     */     
/* 184 */     if (block instanceof BaseBlock) {
/*     */       
/* 186 */       buf = generateBase(block);
/*     */     }
/* 188 */     else if (block instanceof FeatureRelationBlock) {
/*     */       
/* 190 */       buf = generateFeatureRelation(block);
/*     */     }
/* 192 */     else if (block instanceof FeatureBlock) {
/*     */       
/* 194 */       buf = generateFeature(block);
/*     */     }
/* 196 */     else if (block instanceof TrialBlock) {
/*     */       
/* 198 */       buf = generateTrial(block);
/*     */     }
/* 200 */     else if (block instanceof BuyBlock) {
/*     */       
/* 202 */       buf = generateBuy(block);
/*     */     }
/* 204 */     else if (block instanceof ProductInfoBlock) {
/*     */       
/* 206 */       buf = generateProductInfo(block);
/*     */     }
/* 208 */     else if (block instanceof RelationBlock) {
/*     */       
/* 210 */       buf = generateRelation(block);
/*     */     }
/* 212 */     else if (block instanceof HistoryBlock) {
/*     */       
/* 214 */       buf = generateHistory(block);
/*     */     
/*     */     }
/* 217 */     else if (block instanceof ReferenceBlock) {
/*     */       
/* 219 */       buf = generateReference(block);
/*     */     }
/* 221 */     else if (block instanceof CarrierBlock) {
/*     */       
/* 223 */       buf = generateCarrier(block);
/*     */     } 
/*     */ 
/*     */     
/* 227 */     return buf;
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   private byte[] generateBase(Block block) {
/* 238 */     BaseBlock baseBlock = null;
/* 239 */     baseBlock = (BaseBlock)block;
/*     */     
/* 241 */     ByteArrayOutputStream baos = null;
/* 242 */     baos = new ByteArrayOutputStream();
/*     */     
/* 244 */     DataOutputStream dos = null;
/* 245 */     dos = new DataOutputStream(baos);
/*     */ 
/*     */     
/*     */     try {
/* 249 */       dos.writeInt(baseBlock.getId());
/*     */       
/* 251 */       dos.writeInt(baseBlock.getUniqueKey());
/*     */       
/* 253 */       dos.writeUTF(baseBlock.getUnlockKey());
/* 254 */       if (!LicenseBlock.useRmsData) {
/*     */         
/* 256 */         dos.writeUTF(baseBlock.getReferenceId());
/* 257 */         dos.writeUTF(baseBlock.getAppEnv());
/* 258 */         dos.writeLong(baseBlock.getVerifyKey());
/* 259 */         dos.writeLong(baseBlock.getCreateTime());
/* 260 */         dos.writeLong(baseBlock.getUpdateTime());
/*     */         
/* 262 */         dos.writeUTF(baseBlock.getLicenseServerURL());
/* 263 */         dos.writeInt(baseBlock.getDeviceID());
/* 264 */         dos.writeInt(baseBlock.getCarrierID());
/* 265 */         dos.writeUTF(baseBlock.getPhoneNo());
/*     */ 
/*     */         
/* 268 */         dos.writeUTF(baseBlock.getShortCode());
/*     */       } 
/*     */ 
/*     */ 
/*     */       
/* 273 */       return getBlockResult(baos.toByteArray(), 10000);
/*     */     }
/* 275 */     catch (IOException e) {
/*     */       
/* 277 */       e.printStackTrace();
/* 278 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 283 */       Utils.closeOut(baos);
/* 284 */       Utils.closeOut(dos);
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
/*     */   private byte[] generateFeatureRelation(Block block) {
/* 297 */     FeatureRelationBlock featureRelationBlock = null;
/* 298 */     featureRelationBlock = (FeatureRelationBlock)block;
/*     */     
/* 300 */     ByteArrayOutputStream baos = null;
/* 301 */     baos = new ByteArrayOutputStream();
/*     */     
/* 303 */     DataOutputStream dos = null;
/* 304 */     dos = new DataOutputStream(baos);
/*     */ 
/*     */     
/*     */     try {
/* 308 */       dos.writeInt(featureRelationBlock.getId());
/*     */       
/* 310 */       dos.write(generateArrays(featureRelationBlock.getFeature(), 0, 1));
/* 311 */       if (!LicenseBlock.useRmsData)
/*     */       {
/* 313 */         dos.write(generateArrays(featureRelationBlock.getRelation(), 0, 1));
/*     */       }
/*     */ 
/*     */       
/* 317 */       return getBlockResult(baos.toByteArray(), 20000);
/*     */     }
/* 319 */     catch (IOException e) {
/*     */       
/* 321 */       e.printStackTrace();
/* 322 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 327 */       Utils.closeOut(baos);
/* 328 */       Utils.closeOut(dos);
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
/*     */   private byte[] generateFeature(Block block) {
/* 340 */     FeatureBlock featureBlock = null;
/* 341 */     featureBlock = (FeatureBlock)block;
/*     */     
/* 343 */     ByteArrayOutputStream baos = null;
/* 344 */     baos = new ByteArrayOutputStream();
/*     */     
/* 346 */     DataOutputStream dos = null;
/* 347 */     dos = new DataOutputStream(baos);
/*     */ 
/*     */     
/*     */     try {
/* 351 */       dos.writeInt(featureBlock.getId());
/* 352 */       dos.writeUTF(featureBlock.getFeatureId());
/* 353 */       if (!LicenseBlock.useRmsData)
/*     */       {
/* 355 */         dos.writeUTF(featureBlock.getFeatureName());
/*     */       }
/* 357 */       dos.write(generateArrays(featureBlock.getTrial(), 0, 1));
/* 358 */       dos.write(generateArrays(featureBlock.getBuy(), 0, 1));
/*     */ 
/*     */       
/* 361 */       return getBlockResult(baos.toByteArray(), 21000);
/*     */     }
/* 363 */     catch (IOException e) {
/*     */       
/* 365 */       e.printStackTrace();
/* 366 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 371 */       Utils.closeOut(baos);
/* 372 */       Utils.closeOut(dos);
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
/*     */   private byte[] generateTrial(Block block) {
/* 384 */     TrialBlock trialBlock = null;
/* 385 */     trialBlock = (TrialBlock)block;
/*     */     
/* 387 */     ByteArrayOutputStream baos = null;
/* 388 */     baos = new ByteArrayOutputStream();
/*     */     
/* 390 */     DataOutputStream dos = null;
/* 391 */     dos = new DataOutputStream(baos);
/*     */ 
/*     */     
/*     */     try {
/* 395 */       dos.writeInt(trialBlock.getId());
/* 396 */       dos.writeInt(trialBlock.getTrialFlag());
/* 397 */       dos.writeLong(trialBlock.getTrialInfo());
/* 398 */       dos.writeLong(trialBlock.getTrialUsed());
/* 399 */       dos.writeLong(trialBlock.getTrialRemindKey());
/*     */ 
/*     */       
/* 402 */       return getBlockResult(baos.toByteArray(), 21100);
/*     */     }
/* 404 */     catch (IOException e) {
/*     */       
/* 406 */       e.printStackTrace();
/* 407 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 412 */       Utils.closeOut(baos);
/* 413 */       Utils.closeOut(dos);
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
/*     */   private byte[] generateBuy(Block block) {
/* 425 */     BuyBlock buyBlock = null;
/* 426 */     buyBlock = (BuyBlock)block;
/*     */     
/* 428 */     ByteArrayOutputStream baos = null;
/* 429 */     baos = new ByteArrayOutputStream();
/*     */     
/* 431 */     DataOutputStream dos = null;
/* 432 */     dos = new DataOutputStream(baos);
/*     */ 
/*     */     
/*     */     try {
/* 436 */       dos.writeInt(buyBlock.getId());
/* 437 */       dos.writeInt(buyBlock.getBuyFlag());
/* 438 */       dos.writeLong(buyBlock.getBuyInfo());
/* 439 */       dos.writeLong(buyBlock.getBuyUsed());
/* 440 */       dos.writeLong(buyBlock.getBuyRemindKey());
/* 441 */       if (!LicenseBlock.useRmsData) {
/*     */         
/* 443 */         dos.writeInt(buyBlock.getPNumber());
/* 444 */         dos.write(generateArrays(buyBlock.getProductinfo(), 0, 1));
/*     */       } 
/*     */ 
/*     */       
/* 448 */       return getBlockResult(baos.toByteArray(), 21200);
/*     */     }
/* 450 */     catch (IOException e) {
/*     */       
/* 452 */       e.printStackTrace();
/* 453 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 458 */       Utils.closeOut(baos);
/* 459 */       Utils.closeOut(dos);
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
/*     */   private byte[] generateProductInfo(Block block) {
/* 471 */     ProductInfoBlock productInfoBlock = null;
/* 472 */     productInfoBlock = (ProductInfoBlock)block;
/*     */     
/* 474 */     ByteArrayOutputStream baos = null;
/* 475 */     baos = new ByteArrayOutputStream();
/*     */     
/* 477 */     DataOutputStream dos = null;
/* 478 */     dos = new DataOutputStream(baos);
/*     */ 
/*     */     
/*     */     try {
/* 482 */       dos.writeInt(productInfoBlock.getId());
/* 483 */       dos.writeUTF(productInfoBlock.getProductId());
/* 484 */       dos.writeInt(productInfoBlock.getProductPrice());
/* 485 */       dos.writeLong(productInfoBlock.getProductKey());
/* 486 */       dos.writeUTF(productInfoBlock.getDisplayName());
/*     */ 
/*     */       
/* 489 */       return getBlockResult(baos.toByteArray(), 21210);
/*     */     }
/* 491 */     catch (IOException e) {
/*     */       
/* 493 */       e.printStackTrace();
/* 494 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 499 */       Utils.closeOut(baos);
/* 500 */       Utils.closeOut(dos);
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
/*     */   private byte[] generateRelation(Block block) {
/* 512 */     RelationBlock relationBlock = null;
/* 513 */     relationBlock = (RelationBlock)block;
/*     */     
/* 515 */     ByteArrayOutputStream baos = null;
/* 516 */     baos = new ByteArrayOutputStream();
/*     */     
/* 518 */     DataOutputStream dos = null;
/* 519 */     dos = new DataOutputStream(baos);
/*     */ 
/*     */     
/*     */     try {
/* 523 */       dos.writeInt(relationBlock.getId());
/* 524 */       dos.writeUTF(relationBlock.getRelationName());
/* 525 */       dos.writeInt(relationBlock.getRelationFlag());
/* 526 */       dos.write(generateArrays(relationBlock.getFeatureIds(), 0, 2));
/*     */ 
/*     */       
/* 529 */       return getBlockResult(baos.toByteArray(), 22000);
/*     */     }
/* 531 */     catch (IOException e) {
/*     */       
/* 533 */       e.printStackTrace();
/* 534 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 539 */       Utils.closeOut(baos);
/* 540 */       Utils.closeOut(dos);
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
/*     */   private byte[] generateHistory(Block block) {
/* 552 */     HistoryBlock historyBlock = null;
/* 553 */     historyBlock = (HistoryBlock)block;
/*     */     
/* 555 */     ByteArrayOutputStream baos = null;
/* 556 */     baos = new ByteArrayOutputStream();
/*     */     
/* 558 */     DataOutputStream dos = null;
/* 559 */     dos = new DataOutputStream(baos);
/*     */ 
/*     */     
/*     */     try {
/* 563 */       dos.writeInt(historyBlock.getId());
/* 564 */       dos.writeInt(historyBlock.getBuyFlag());
/* 565 */       dos.writeLong(historyBlock.getBuyInfo());
/* 566 */       dos.writeLong(historyBlock.getBuyTime());
/* 567 */       dos.writeInt(historyBlock.getProductPrice());
/* 568 */       dos.writeUTF(historyBlock.getProductId());
/* 569 */       dos.writeUTF(historyBlock.getReferenceId());
/*     */ 
/*     */       
/* 572 */       return getBlockResult(baos.toByteArray(), 30000);
/*     */     }
/* 574 */     catch (IOException e) {
/*     */       
/* 576 */       e.printStackTrace();
/* 577 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 582 */       Utils.closeOut(baos);
/* 583 */       Utils.closeOut(dos);
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
/*     */   private byte[] generateReference(Block block) {
/* 596 */     ReferenceBlock referenceBlock = null;
/* 597 */     referenceBlock = (ReferenceBlock)block;
/*     */     
/* 599 */     ByteArrayOutputStream baos = null;
/* 600 */     baos = new ByteArrayOutputStream();
/*     */     
/* 602 */     DataOutputStream dos = null;
/* 603 */     dos = new DataOutputStream(baos);
/*     */ 
/*     */     
/*     */     try {
/* 607 */       dos.writeInt(referenceBlock.getId());
/* 608 */       dos.write(generateArrays(referenceBlock.getCarriers(), 0, 1));
/*     */ 
/*     */       
/* 611 */       return getBlockResult(baos.toByteArray(), 40000);
/*     */     }
/* 613 */     catch (IOException e) {
/*     */       
/* 615 */       e.printStackTrace();
/* 616 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 621 */       Utils.closeOut(baos);
/* 622 */       Utils.closeOut(dos);
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
/*     */   private byte[] generateCarrier(Block block) {
/* 634 */     CarrierBlock carrierBlock = null;
/* 635 */     carrierBlock = (CarrierBlock)block;
/*     */     
/* 637 */     ByteArrayOutputStream baos = null;
/* 638 */     baos = new ByteArrayOutputStream();
/*     */     
/* 640 */     DataOutputStream dos = null;
/* 641 */     dos = new DataOutputStream(baos);
/*     */ 
/*     */     
/*     */     try {
/* 645 */       dos.writeInt(carrierBlock.getId());
/*     */       
/* 647 */       dos.writeUTF(carrierBlock.getCarrierDName());
/*     */ 
/*     */       
/* 650 */       return getBlockResult(baos.toByteArray(), 41000);
/*     */     }
/* 652 */     catch (IOException e) {
/*     */       
/* 654 */       e.printStackTrace();
/* 655 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 660 */       Utils.closeOut(baos);
/* 661 */       Utils.closeOut(dos);
/*     */     } 
/*     */   }
/*     */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\Generate.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */