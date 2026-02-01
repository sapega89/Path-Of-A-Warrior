/*     */ package com.movaya.license.structure;
/*     */ 
/*     */ import com.movaya.license.utils.Utils;
/*     */ import java.io.ByteArrayInputStream;
/*     */ import java.io.ByteArrayOutputStream;
/*     */ import java.io.DataInputStream;
/*     */ import java.io.DataOutputStream;
/*     */ import java.io.IOException;
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
/*     */ public final class Resolve
/*     */ {
/*     */   public LicenseBlock resolve(byte[] data) {
/*  34 */     ByteArrayInputStream bin = null;
/*  35 */     bin = new ByteArrayInputStream(data);
/*     */     
/*  37 */     return resolve(bin);
/*     */   }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   public LicenseBlock resolve(InputStream in) {
/*  48 */     LicenseBlock licenseBlock = null;
/*  49 */     licenseBlock = new LicenseBlock();
/*     */     
/*  51 */     DataInputStream dis = null;
/*  52 */     dis = new DataInputStream(in);
/*     */     
/*  54 */     int flag = -1;
/*  55 */     int length = -1;
/*  56 */     int dataLen = -1;
/*  57 */     byte[] data = (byte[])null;
/*     */ 
/*     */     
/*     */     try {
/*  61 */       flag = dis.readInt();
/*     */       
/*  63 */       length = dis.readInt();
/*     */       
/*  65 */       dataLen = dis.readInt();
/*     */       
/*  67 */       data = new byte[length];
/*  68 */       dis.read(data);
/*     */       
/*  70 */       Array array = null;
/*  71 */       array = resolveArrays(data);
/*     */       
/*  73 */       for (int i = 0; i < array.size(); i++)
/*     */       {
/*  75 */         licenseBlock.addElement(array.elementAt(i));
/*     */       }
/*     */ 
/*     */       
/*  79 */       return licenseBlock;
/*     */     }
/*  81 */     catch (IOException e) {
/*     */       
/*  83 */       e.printStackTrace();
/*  84 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/*  89 */       Utils.closeIn(dis);
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
/*     */   private Array resolveArrays(byte[] buf) {
/* 101 */     Array array = null;
/* 102 */     array = new Array();
/*     */     
/* 104 */     ByteArrayInputStream bais = null;
/* 105 */     bais = new ByteArrayInputStream(buf);
/*     */     
/* 107 */     DataInputStream dis = null;
/* 108 */     dis = new DataInputStream(bais);
/*     */     
/* 110 */     int flag = -1;
/* 111 */     int length = -1;
/* 112 */     int dataLen = -1;
/* 113 */     byte[] data = (byte[])null;
/* 114 */     byte[] limitData = (byte[])null;
/*     */ 
/*     */     
/*     */     try {
/* 118 */       while (dis.available() != 0) {
/*     */ 
/*     */         
/* 121 */         flag = dis.readInt();
/* 122 */         length = dis.readInt();
/*     */ 
/*     */         
/* 125 */         if (flag == 2) {
/*     */ 
/*     */           
/* 128 */           dataLen = dis.readInt();
/* 129 */           while (dis.available() != 0)
/*     */           {
/* 131 */             array.addElement(dis.readUTF());
/*     */           }
/*     */           continue;
/*     */         } 
/* 135 */         if (flag == 3) {
/*     */ 
/*     */           
/* 138 */           dataLen = dis.readInt();
/*     */           
/* 140 */           limitData = new byte[dataLen];
/*     */           
/* 142 */           while (dis.available() != 0) {
/*     */             
/* 144 */             dis.read(limitData);
/*     */             
/* 146 */             array.addElement(new String(limitData));
/*     */           }  continue;
/*     */         } 
/* 149 */         if (flag == 1) {
/*     */ 
/*     */           
/* 152 */           dataLen = dis.readInt();
/*     */ 
/*     */           
/* 155 */           data = new byte[length];
/* 156 */           dis.read(data);
/*     */           
/* 158 */           array.addElement(resolveArrays(data));
/*     */           
/*     */           continue;
/*     */         } 
/*     */         
/* 163 */         data = new byte[length];
/* 164 */         dis.read(data);
/*     */         
/* 166 */         array.addElement(resolveBlock(getBlockByteArray(data, flag, length)));
/*     */       } 
/*     */ 
/*     */ 
/*     */       
/* 171 */       return array;
/*     */     }
/* 173 */     catch (IOException e) {
/*     */       
/* 175 */       e.printStackTrace();
/* 176 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 181 */       Utils.closeIn(dis);
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
/*     */   private byte[] getBlockByteArray(byte[] buf, int flag, int length) {
/* 195 */     ByteArrayOutputStream baos = null;
/* 196 */     baos = new ByteArrayOutputStream();
/*     */     
/* 198 */     DataOutputStream dos = null;
/* 199 */     dos = new DataOutputStream(baos);
/*     */ 
/*     */     
/*     */     try {
/* 203 */       dos.writeInt(flag);
/* 204 */       dos.writeInt(length);
/* 205 */       dos.write(buf);
/*     */ 
/*     */       
/* 208 */       return baos.toByteArray();
/*     */     }
/* 210 */     catch (IOException e) {
/*     */       
/* 212 */       e.printStackTrace();
/* 213 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 218 */       Utils.closeOut(baos);
/* 219 */       Utils.closeOut(dos);
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
/*     */   private Object resolveBlock(byte[] buf) {
/* 231 */     ByteArrayInputStream bais = null;
/* 232 */     bais = new ByteArrayInputStream(buf);
/*     */     
/* 234 */     DataInputStream dis = null;
/* 235 */     dis = new DataInputStream(bais); try {
/*     */       Array array; BaseBlock baseBlock; FeatureRelationBlock featureRelationBlock; BuyBlock buyBlock; ProductInfoBlock productInfoBlock; FeatureBlock featureBlock; RelationBlock relationBlock; TrialBlock trialBlock;
/*     */       HistoryBlock historyBlock;
/*     */       ReferenceBlock referenceBlock;
/* 239 */       int flag = 0;
/*     */       
/* 241 */       flag = dis.readInt();
/*     */       
/* 243 */       switch (flag) {
/*     */         
/*     */         case 1:
/* 246 */           return resolveArrays(buf);
/*     */         case 10000:
/* 248 */           return resolveBase(buf);
/*     */         case 20000:
/* 250 */           return resolveFeatureRelation(buf);
/*     */         case 21200:
/* 252 */           return resolveBuy(buf);
/*     */         case 21210:
/* 254 */           return resolveProductInfo(buf);
/*     */         case 21000:
/* 256 */           return resolveFeature(buf);
/*     */         case 22000:
/* 258 */           return resolveRelation(buf);
/*     */         case 21100:
/* 260 */           return resolveTrial(buf);
/*     */         case 30000:
/* 262 */           return resolveHistory(buf);
/*     */         
/*     */         case 40000:
/* 265 */           return resolveReference(buf);
/*     */         case 41000:
/* 267 */           return resolveCarrier(buf);
/*     */       } 
/*     */ 
/*     */       
/* 271 */       throw new IOException(" Unkown Type. ");
/*     */     
/*     */     }
/* 274 */     catch (IOException e) {
/*     */       
/* 276 */       e.printStackTrace();
/* 277 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 282 */       Utils.closeIn(bais);
/* 283 */       Utils.closeIn(dis);
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
/*     */   private BaseBlock resolveBase(byte[] buf) {
/* 295 */     BaseBlock baseBlock = null;
/* 296 */     baseBlock = new BaseBlock();
/*     */     
/* 298 */     ByteArrayInputStream bais = null;
/* 299 */     bais = new ByteArrayInputStream(buf);
/*     */     
/* 301 */     DataInputStream dis = null;
/* 302 */     dis = new DataInputStream(bais);
/*     */ 
/*     */     
/*     */     try {
/* 306 */       baseBlock.setFlag(dis.readInt());
/* 307 */       baseBlock.setLength(dis.readInt());
/* 308 */       baseBlock.setId(dis.readInt());
/*     */ 
/*     */       
/* 311 */       baseBlock.setUniqueKey(dis.readInt());
/*     */       
/* 313 */       baseBlock.setUnlockKey(dis.readUTF());
/* 314 */       if (!LicenseBlock.useRmsData) {
/*     */         
/* 316 */         baseBlock.setReferenceId(dis.readUTF());
/* 317 */         baseBlock.setAppEnv(dis.readUTF());
/* 318 */         baseBlock.setVerifyKey(dis.readLong());
/* 319 */         baseBlock.setCreateTime(dis.readLong());
/* 320 */         baseBlock.setUpdateTime(dis.readLong());
/*     */         
/* 322 */         baseBlock.setLicenseServerURL(dis.readUTF());
/* 323 */         baseBlock.setDeviceID(dis.readInt());
/* 324 */         baseBlock.setCarrierID(dis.readInt());
/* 325 */         baseBlock.setPhoneNo(dis.readUTF());
/*     */ 
/*     */         
/* 328 */         baseBlock.setShortCode(dis.readUTF());
/*     */       } 
/*     */ 
/*     */ 
/*     */       
/* 333 */       return baseBlock;
/*     */     }
/* 335 */     catch (IOException e) {
/*     */       
/* 337 */       e.printStackTrace();
/* 338 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 343 */       Utils.closeIn(bais);
/* 344 */       Utils.closeIn(dis);
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
/*     */   private FeatureRelationBlock resolveFeatureRelation(byte[] buf) {
/* 356 */     FeatureRelationBlock featureRelationBlock = null;
/* 357 */     featureRelationBlock = new FeatureRelationBlock();
/*     */     
/* 359 */     ByteArrayInputStream bais = null;
/* 360 */     bais = new ByteArrayInputStream(buf);
/*     */     
/* 362 */     DataInputStream dis = null;
/* 363 */     dis = new DataInputStream(bais);
/*     */     
/* 365 */     byte[] data = (byte[])null;
/*     */     
/*     */     try {
/* 368 */       featureRelationBlock.setFlag(dis.readInt());
/* 369 */       featureRelationBlock.setLength(dis.readInt());
/* 370 */       featureRelationBlock.setId(dis.readInt());
/*     */       
/* 372 */       int flag = -1;
/* 373 */       int length = -1;
/* 374 */       int dataLen = -1;
/*     */       
/* 376 */       flag = dis.readInt();
/* 377 */       length = dis.readInt();
/* 378 */       dataLen = dis.readInt();
/*     */       
/* 380 */       data = new byte[length];
/* 381 */       dis.read(data);
/*     */ 
/*     */       
/* 384 */       featureRelationBlock.setFeature(resolveArrays(data));
/*     */       
/* 386 */       if (!LicenseBlock.useRmsData) {
/*     */         
/* 388 */         flag = dis.readInt();
/* 389 */         length = dis.readInt();
/* 390 */         dataLen = dis.readInt();
/*     */         
/* 392 */         data = new byte[length];
/* 393 */         dis.read(data);
/*     */ 
/*     */         
/* 396 */         featureRelationBlock.setRelation(resolveArrays(data));
/*     */       } 
/*     */ 
/*     */       
/* 400 */       return featureRelationBlock;
/*     */     }
/* 402 */     catch (IOException e) {
/*     */       
/* 404 */       e.printStackTrace();
/* 405 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 410 */       Utils.closeIn(bais);
/* 411 */       Utils.closeIn(dis);
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
/*     */   private FeatureBlock resolveFeature(byte[] buf) {
/* 423 */     FeatureBlock featureBlock = null;
/* 424 */     featureBlock = new FeatureBlock();
/*     */     
/* 426 */     ByteArrayInputStream bais = null;
/* 427 */     bais = new ByteArrayInputStream(buf);
/*     */     
/* 429 */     DataInputStream dis = null;
/* 430 */     dis = new DataInputStream(bais);
/*     */     
/* 432 */     byte[] data = (byte[])null;
/*     */     
/*     */     try {
/* 435 */       featureBlock.setFlag(dis.readInt());
/* 436 */       featureBlock.setLength(dis.readInt());
/* 437 */       featureBlock.setId(dis.readInt());
/* 438 */       featureBlock.setFeatureId(dis.readUTF());
/* 439 */       if (!LicenseBlock.useRmsData)
/*     */       {
/* 441 */         featureBlock.setFeatureName(dis.readUTF());
/*     */       }
/*     */       
/* 444 */       int flag = -1;
/* 445 */       int length = -1;
/* 446 */       int dataLen = -1;
/*     */       
/* 448 */       flag = dis.readInt();
/* 449 */       length = dis.readInt();
/* 450 */       dataLen = dis.readInt();
/*     */       
/* 452 */       data = new byte[length];
/* 453 */       dis.read(data);
/*     */ 
/*     */       
/* 456 */       featureBlock.setTrial(resolveArrays(data));
/*     */       
/* 458 */       flag = dis.readInt();
/* 459 */       length = dis.readInt();
/* 460 */       dataLen = dis.readInt();
/*     */       
/* 462 */       data = new byte[length];
/* 463 */       dis.read(data);
/*     */ 
/*     */       
/* 466 */       featureBlock.setBuy(resolveArrays(data));
/*     */ 
/*     */       
/* 469 */       return featureBlock;
/*     */     }
/* 471 */     catch (IOException e) {
/*     */       
/* 473 */       e.printStackTrace();
/* 474 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 479 */       Utils.closeIn(bais);
/* 480 */       Utils.closeIn(dis);
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
/*     */   private TrialBlock resolveTrial(byte[] buf) {
/* 492 */     TrialBlock trialBlock = null;
/* 493 */     trialBlock = new TrialBlock();
/*     */     
/* 495 */     ByteArrayInputStream bais = null;
/* 496 */     bais = new ByteArrayInputStream(buf);
/*     */     
/* 498 */     DataInputStream dis = null;
/* 499 */     dis = new DataInputStream(bais);
/*     */ 
/*     */     
/*     */     try {
/* 503 */       trialBlock.setFlag(dis.readInt());
/* 504 */       trialBlock.setLength(dis.readInt());
/* 505 */       trialBlock.setId(dis.readInt());
/* 506 */       trialBlock.setTrialFlag(dis.readInt());
/* 507 */       trialBlock.setTrialInfo(dis.readLong());
/* 508 */       trialBlock.setTrialUsed(dis.readLong());
/* 509 */       trialBlock.setTrialRemindKey(dis.readLong());
/*     */ 
/*     */       
/* 512 */       return trialBlock;
/*     */     }
/* 514 */     catch (IOException e) {
/*     */       
/* 516 */       e.printStackTrace();
/* 517 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 522 */       Utils.closeIn(bais);
/* 523 */       Utils.closeIn(dis);
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
/*     */   private BuyBlock resolveBuy(byte[] buf) {
/* 535 */     BuyBlock buyBlock = null;
/* 536 */     buyBlock = new BuyBlock();
/*     */     
/* 538 */     ByteArrayInputStream bais = null;
/* 539 */     bais = new ByteArrayInputStream(buf);
/*     */     
/* 541 */     DataInputStream dis = null;
/* 542 */     dis = new DataInputStream(bais);
/*     */     
/* 544 */     byte[] data = (byte[])null;
/*     */     
/*     */     try {
/* 547 */       buyBlock.setFlag(dis.readInt());
/* 548 */       buyBlock.setLength(dis.readInt());
/* 549 */       buyBlock.setId(dis.readInt());
/* 550 */       buyBlock.setBuyFlag(dis.readInt());
/* 551 */       buyBlock.setBuyInfo(dis.readLong());
/* 552 */       buyBlock.setBuyUsed(dis.readLong());
/* 553 */       buyBlock.setBuyRemindKey(dis.readLong());
/* 554 */       if (!LicenseBlock.useRmsData) {
/*     */         
/* 556 */         buyBlock.setPNumber(dis.readInt());
/*     */         
/* 558 */         int flag = -1;
/* 559 */         int length = -1;
/* 560 */         int dataLen = -1;
/*     */         
/* 562 */         flag = dis.readInt();
/* 563 */         length = dis.readInt();
/* 564 */         dataLen = dis.readInt();
/*     */         
/* 566 */         data = new byte[length];
/* 567 */         dis.read(data);
/*     */ 
/*     */         
/* 570 */         buyBlock.setProductinfo(resolveArrays(data));
/*     */       } 
/*     */ 
/*     */       
/* 574 */       return buyBlock;
/*     */     }
/* 576 */     catch (IOException e) {
/*     */       
/* 578 */       e.printStackTrace();
/* 579 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 584 */       Utils.closeIn(bais);
/* 585 */       Utils.closeIn(dis);
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
/*     */   private ProductInfoBlock resolveProductInfo(byte[] buf) {
/* 597 */     ProductInfoBlock productInfoBlock = null;
/* 598 */     productInfoBlock = new ProductInfoBlock();
/*     */     
/* 600 */     ByteArrayInputStream bais = null;
/* 601 */     bais = new ByteArrayInputStream(buf);
/*     */     
/* 603 */     DataInputStream dis = null;
/* 604 */     dis = new DataInputStream(bais);
/*     */ 
/*     */     
/*     */     try {
/* 608 */       productInfoBlock.setFlag(dis.readInt());
/* 609 */       productInfoBlock.setLength(dis.readInt());
/* 610 */       productInfoBlock.setId(dis.readInt());
/* 611 */       productInfoBlock.setProductId(dis.readUTF());
/* 612 */       productInfoBlock.setProductPrice(dis.readInt());
/* 613 */       productInfoBlock.setProductKey(dis.readLong());
/* 614 */       productInfoBlock.setDisplayName(dis.readUTF());
/*     */ 
/*     */       
/* 617 */       return productInfoBlock;
/*     */     }
/* 619 */     catch (IOException e) {
/*     */       
/* 621 */       e.printStackTrace();
/* 622 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 627 */       Utils.closeIn(bais);
/* 628 */       Utils.closeIn(dis);
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
/*     */   private RelationBlock resolveRelation(byte[] buf) {
/* 640 */     RelationBlock relationBlock = null;
/* 641 */     relationBlock = new RelationBlock();
/*     */     
/* 643 */     ByteArrayInputStream bais = null;
/* 644 */     bais = new ByteArrayInputStream(buf);
/*     */     
/* 646 */     DataInputStream dis = null;
/* 647 */     dis = new DataInputStream(bais);
/*     */     
/* 649 */     byte[] data = (byte[])null;
/*     */     
/*     */     try {
/* 652 */       relationBlock.setFlag(dis.readInt());
/* 653 */       relationBlock.setLength(dis.readInt());
/* 654 */       relationBlock.setId(dis.readInt());
/* 655 */       relationBlock.setRelationName(dis.readUTF());
/* 656 */       relationBlock.setRelationFlag(dis.readInt());
/*     */       
/* 658 */       data = new byte[dis.available()];
/* 659 */       dis.read(data);
/*     */ 
/*     */       
/* 662 */       relationBlock.setFeatureIds(resolveArrays(data));
/*     */ 
/*     */       
/* 665 */       return relationBlock;
/*     */     }
/* 667 */     catch (IOException e) {
/*     */       
/* 669 */       e.printStackTrace();
/* 670 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 675 */       Utils.closeIn(bais);
/* 676 */       Utils.closeIn(dis);
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
/*     */   private HistoryBlock resolveHistory(byte[] buf) {
/* 688 */     HistoryBlock historyBlock = null;
/* 689 */     historyBlock = new HistoryBlock();
/*     */     
/* 691 */     ByteArrayInputStream bais = null;
/* 692 */     bais = new ByteArrayInputStream(buf);
/*     */     
/* 694 */     DataInputStream dis = null;
/* 695 */     dis = new DataInputStream(bais);
/*     */ 
/*     */     
/*     */     try {
/* 699 */       historyBlock.setFlag(dis.readInt());
/* 700 */       historyBlock.setLength(dis.readInt());
/* 701 */       historyBlock.setId(dis.readInt());
/* 702 */       historyBlock.setBuyFlag(dis.readInt());
/* 703 */       historyBlock.setBuyInfo(dis.readLong());
/* 704 */       historyBlock.setBuyTime(dis.readLong());
/* 705 */       historyBlock.setProductPrice(dis.readInt());
/* 706 */       historyBlock.setProductId(dis.readUTF());
/* 707 */       historyBlock.setReferenceId(dis.readUTF());
/*     */ 
/*     */       
/* 710 */       return historyBlock;
/*     */     }
/* 712 */     catch (IOException e) {
/*     */       
/* 714 */       e.printStackTrace();
/* 715 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 720 */       Utils.closeIn(bais);
/* 721 */       Utils.closeIn(dis);
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
/*     */   private ReferenceBlock resolveReference(byte[] buf) {
/* 734 */     ReferenceBlock referenceBlock = null;
/* 735 */     referenceBlock = new ReferenceBlock();
/*     */     
/* 737 */     ByteArrayInputStream bais = null;
/* 738 */     bais = new ByteArrayInputStream(buf);
/*     */     
/* 740 */     DataInputStream dis = null;
/* 741 */     dis = new DataInputStream(bais);
/*     */     
/* 743 */     byte[] data = (byte[])null;
/*     */     
/*     */     try {
/* 746 */       referenceBlock.setFlag(dis.readInt());
/* 747 */       referenceBlock.setLength(dis.readInt());
/* 748 */       referenceBlock.setId(dis.readInt());
/*     */       
/* 750 */       int flag = -1;
/* 751 */       int length = -1;
/* 752 */       int dataLen = -1;
/*     */       
/* 754 */       flag = dis.readInt();
/* 755 */       length = dis.readInt();
/* 756 */       dataLen = dis.readInt();
/*     */       
/* 758 */       data = new byte[length];
/* 759 */       dis.read(data);
/*     */ 
/*     */       
/* 762 */       referenceBlock.setCarriers(resolveArrays(data));
/*     */ 
/*     */       
/* 765 */       return referenceBlock;
/*     */     }
/* 767 */     catch (IOException e) {
/*     */       
/* 769 */       e.printStackTrace();
/* 770 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 775 */       Utils.closeIn(bais);
/* 776 */       Utils.closeIn(dis);
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
/*     */   private CarrierBlock resolveCarrier(byte[] buf) {
/* 788 */     CarrierBlock carrierBlock = null;
/* 789 */     carrierBlock = new CarrierBlock();
/*     */     
/* 791 */     ByteArrayInputStream bais = null;
/* 792 */     bais = new ByteArrayInputStream(buf);
/*     */     
/* 794 */     DataInputStream dis = null;
/* 795 */     dis = new DataInputStream(bais);
/*     */ 
/*     */     
/*     */     try {
/* 799 */       carrierBlock.setFlag(dis.readInt());
/* 800 */       carrierBlock.setLength(dis.readInt());
/* 801 */       carrierBlock.setId(dis.readInt());
/*     */       
/* 803 */       carrierBlock.setCarrierDName(dis.readUTF());
/*     */ 
/*     */       
/* 806 */       return carrierBlock;
/*     */     }
/* 808 */     catch (IOException e) {
/*     */       
/* 810 */       e.printStackTrace();
/* 811 */       return null;
/*     */     
/*     */     }
/*     */     finally {
/*     */       
/* 816 */       Utils.closeIn(bais);
/* 817 */       Utils.closeIn(dis);
/*     */     } 
/*     */   }
/*     */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\license\structure\Resolve.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */