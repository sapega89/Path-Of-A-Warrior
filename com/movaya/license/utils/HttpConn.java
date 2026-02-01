/*    */ package com.movaya.license.utils;
/*    */ 
/*    */ import java.io.IOException;
/*    */ import javax.microedition.io.Connection;
/*    */ import javax.microedition.io.Connector;
/*    */ import javax.microedition.io.HttpConnection;
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
/*    */ public final class HttpConn
/*    */ {
/*    */   public static final int CONNECTION_REFUSED = -1;
/*    */   public static final int CONNECTION_FAILED = -2;
/*    */   public static final int MIDLET_ORDER_FAILED = 0;
/*    */   public static final int MIDLET_ORDER_SUCCESS = 1;
/*    */   public static final int MIDLET_ORDER_EXIST = 2;
/*    */   public static final int WAP_ORDER_SUCCESS = 3;
/*    */   public static final int WAP_ORDER_FAILED = 4;
/*    */   
/*    */   public static final int visit(String url) {
/* 32 */     String status = null;
/* 33 */     HttpConnection conn = null;
/*    */ 
/*    */ 
/*    */ 
/*    */     
/*    */     try {
/*    */       try {
/* 40 */         conn = (HttpConnection)Connector.open(url);
/*    */       }
/* 42 */       catch (Exception ex) {
/*    */         
/* 44 */         ex.printStackTrace();
/* 45 */         return -1;
/*    */       } 
/*    */ 
/*    */ 
/*    */       
/*    */       try {
/* 51 */         if (conn.getResponseCode() == 200) {
/*    */ 
/*    */           
/*    */           try {
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
/* 65 */             status = conn.getHeaderField("STATUS");
/* 66 */             if (status != null) {
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
/* 79 */               Utils.closeConnection((Connection)conn);
/*    */ 
/*    */               
/* 82 */               if (status.toUpperCase().equals("T"))
/*    */               {
/* 84 */                 return 1;
/*    */               }
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */               
/* 92 */               return 0;
/*    */             } 
/*    */           } catch (IOException ex) {
/*    */             ex.printStackTrace();
/*    */           } 
/*    */           return 0;
/*    */         } 
/*    */       } catch (IOException iOException) {
/*    */         iOException.printStackTrace();
/*    */       } 
/*    */       return -2;
/*    */     } finally {
/*    */       Utils.closeConnection((Connection)conn);
/*    */     } 
/*    */   }
/*    */ }


/* Location:              C:\User\\user\OneDrive\Рабочий стол\Path-Of-A-Warrior-240x320.jar!\com\movaya\licens\\utils\HttpConn.class
 * Java compiler version: 1 (45.3)
 * JD-Core Version:       1.1.3
 */