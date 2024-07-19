# -*- coding: utf-8 -*-
import sys
import os
import sqlite3
import pymssql
import time
import shutil
import csv
import pandas as pd
from datetime import date
from FTsettings import *
from balancedefs import *
import pymssql
from datetime import datetime
from FTSI_balance_transfer import *
from commoditydefs import *

DefaultCommodityManager = CommodityManager()
today = datetime.datetime.today().strftime("%Y%m%d")
strToday = date.today().strftime("%Y-%m-%d")

# 連上SQL Server
'''
conn = pymssql.connect(
    host = "km01\km01",
    user = "DFAPUser1",
    password = "apuser168",
    database = "AS400DS"
    )
'''
conn = pymssql.connect(
    host = "localhost",
    user = "sa",
    password = "test@1234",
    database = "AS400DS"
    )
cursor = conn.cursor(as_dict=True)
cursor.execute("SELECT * FROM DBFILE_DBTXIO")
# 連上dbfile
connLite = sqlite3.connect(dbFile)
cursorLite = connLite.cursor()

#%%
# --- 部位移轉的資料 ---
"""
TXIO01  [numeric](7, 0) NOT NULL,  DEFAULT ((0))  移轉日期
TXIO02  [numeric](3, 0) NOT NULL,  DEFAULT ((0))  序號
TXIO03  [char](6) NOT NULL,        DEFAULT (' ')  證券代號
TXIO04  [char](2) NOT NULL,        DEFAULT (' ')  移出部門
TXIO05  [char](2) NOT NULL,        DEFAULT (' ')  移出下單員
TXIO06  [char](2) NOT NULL,        DEFAULT (' ')  移入部門
TXIO07  [char](2) NOT NULL,        DEFAULT (' ')  移入下單員
TXIO08  [numeric](10, 0) NOT NULL, DEFAULT ((0))  移轉股數
TXIO09  [numeric](12, 0) NOT NULL, DEFAULT ((0))  移轉金額
TXIO10  [numeric](12, 0) NOT NULL, DEFAULT ((0))  移轉成本
TXIO11  [numeric](10, 0) NOT NULL, DEFAULT ((0))  移轉待撥股數
TXIO20  [char](30) NOT NULL,       DEFAULT (' ')  備註
TXIO98  [numeric](8, 0) NOT NULL,  DEFAULT ((0))  系統日期
TXIO99  [numeric](6, 0) NOT NULL,  DEFAULT ((0))  系統時間
TXIO21  [char](1) NOT NULL,        DEFAULT (' ')  交易種類
TXIO22  [numeric](8, 0) NOT NULL,  DEFAULT ((0))  交易稅
TXIO23  [numeric](10, 0) NOT NULL, DEFAULT ((0))  履約金額
TXIO24  [numeric](10, 0) NOT NULL, DEFAULT ((0))  ETF申贖手續費
TXIO25  [numeric](10, 0) NOT NULL  DEFAULT ((0))  ETF交易費

"""

for row in cursor:
    if str(row["TXIO01"] + 19110000) == today: # today
        if row["TXIO04"].strip() + row["TXIO05"].strip() != u"":
            newAccount = row["TXIO04"].strip() + row["TXIO05"].strip()
            newVolume = "-" + str(row["TXIO08"])
            newCost = "-" + str(row["TXIO10"])
            # 會不會Alias都是空的，要怎麼避免
            newCode = row["TXIO03"].strip() + ".TWSE"
            newTime = str(row["TXIO99"])
            newAlias = ""
            newRealize = int(row["TXIO09"]) - int(newCost)
            newUnrealize = 0
            print "交易員: {0} \t證券代碼: {1} \t移轉股數: {2} \t移轉成本：{3}\t已實現損益: {4}\t時間: {5}".format(newAccount, newCode, newVolume, newCost, newRealize, newTime)
            # 把移轉庫存的加進balMap
            if traderMap == {} or newAccount not in traderMap.keys():
                pass
            else:
                newVolume = int(newVolume)
                print "New Balance - Alias : " + newAccount + "\tCode : " + newCode
                strKey = newAccount + newCode 
                checkPosition(strKey, newCode, newAccount, newAlias, int(newVolume), newUnrealize, newRealize, int(newCost))
        if row["TXIO06"].strip() + row["TXIO07"].strip() != u"":
            newAccount = row["TXIO06"].strip() + row["TXIO07"].strip()
            newVolume = str(row["TXIO08"])
            newCost = str(row["TXIO10"])
            # 會不會Alias都是空的，要怎麼避免
            newCode = row["TXIO03"].strip() + ".TWSE"
            newTime = str(row["TXIO99"])
            newAlias = ""
            newRealize = int(row["TXIO09"]) - int(newCost)
            newUnrealize = 0
            print "交易員: {0} \t證券代碼: {1} \t移轉股數: {2} \t移轉成本：{3}\t已實現損益: {4}\t時間: {5}".format(newAccount, newCode, newVolume, newCost, newRealize, newTime)
            # 把移轉庫存的加進balMap
            if traderMap == {} or newAccount not in traderMap.keys():
                pass
            else:
                newVolume = int(newVolume)
                print "New Balance - Alias : " + newAccount + "\tCode : " + newCode
                strKey = newAccount + newCode
                checkPosition(strKey, newCode, newAccount, newAlias, int(newVolume), newUnrealize, newRealize, int(newCost))
        
'''
交易員: 889 	證券代碼: 041740 	移轉股數: -1990000 	移轉成本: 238800 	時間: 83035
交易員: 505 	證券代碼: 32894 	移轉股數: -289000 	移轉成本: 29506614 	時間: 83158
交易員: 041 	證券代碼: 00732 	移轉股數: -1500000 	移轉成本: 57971435 	時間: 140335
交易員: 505 	證券代碼: 17333 	移轉股數: 5000  移轉成本: 500000 	時間: 132508
交易員: 812 	證券代碼: 704881 	移轉股數: -1000000 	移轉成本: 457961 	時間: 131919
'''

#%%先不計算
# --- 借券庫存 --- 
#     Seq.    名稱                  位置        類型長度    說明                    範例          備註
#     1       標的代號            001-006         X(6)    左靠右補空白              2303
#     2       標的名稱            007-022         X(16)   左靠右補空白              台積電
#     3       借券庫存            023-032         9(10)   單位：股數，右靠左補0                 借入尚未還券之股數
#     4       可賣庫存            033-042         9(10)   單位：股數， 右靠左補0                剩餘可賣股數
#     5       當日賣出            043-052         9(10)   單位：股數，右靠左補0
#     6       市價損益(正負號)     053-053         X(1)   +或空白為正數， -為負數
#     7       市價損益            054-065         9(12)   單位：元，右靠左補0                  0A1 與 0A2 之當日市價損益合計(借券回補子帳關聯檔)
#     8       日損益差(正負號)     066-066         X(1)   +或空白為正數， -為負數
#     9       日損益差            067-078         9(12)   單位：元，右靠左補0                  本日市價損益-前日市價損益
#     10      現股庫存            079-088         9(10)   單位：股數，右靠左補0                 0A2 庫存股數
#     11      還券不足(正負號)     089-089         X(1)   +或空白為正數， -為負數
#     12      還券不足股數        090-099         9(10)   單位：股數，右靠左補0                可借券賣出股數+現股庫存-借券股數
#     13      帳號                100-102         X(3)    交易員代號，左靠右補空白   0A1       下單員號


with open(SecuriyLendingFile) as fobj:
    if len(fobj.readlines()) > 0 :
        #如果有資料，才讀商品檔，減少耗費的時間
        DefaultCommodityManager.LoadFromZipFile(CommodityInfoFile)
    for line in fobj:
        strSubAccount = line[99:102]
        strCode = line[0:6].strip() + ".TWSE"
        intTotalLots = int(line[22:32].strip()) #借券庫存
        intAvailableLots = int(line[32:42].strip()) #可賣庫存
        intAlreadySellLots = intTotalLots - intAvailableLots #已經賣的庫存數
        intUnrealize = float(line[53:65]) #是RTS要用的嗎
        if line[52:53] == "-":
            intUnrealize *= -1
        floatCost = intUnrealize #要先確認成本怎麼算
        print strSubAccount, strCode, intLots, intUnrealize
        strKey = strSubAccount + strCode
        #checkPosition(strKey, strCode, strSubAccount, strSubAccount, int(intLots), intUnrealize, 0, int(floatCost))




#%%
# --- 轉檔結束，寫入資料庫 ---

for pos in balMap.values():
    print pos
    if pos.lots <= 0:
        print "數量 <= 0 -- 帳號: {0}\t證券代碼: {1}".format(pos.account,pos.code)
        continue
    for acc in getTraderID(pos.account, traderMap):
        # print "acc=",acc
        writeLogToDB(acc, pos, strToday, cursorLite, DDSC)
    writeLogToDB("RelayServer", pos, strToday, cursorLite, DDSC)
            
                
connLite.commit()
connLite.close()
conn.close()
#print row




