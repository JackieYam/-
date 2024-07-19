# -*- coding: UTF-8 -*-
import sys
import os
import datetime
import sqlite3
import pymssql
import time
import shutil
import csv
import pandas as pd
from datetime import date
from FTsettings import *
from balancedefs import *

transdesc = ""
traderMap = {}
strToday = date.today().strftime("%Y-%m-%d")
strTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 中菲庫存存每天都會傳進來，假日就重複傳前一交易日的檔案
'''
使用者代號   BI03030 SALES_NO    營業員號    acc
帳號代碼             SALES_NO                pos.account
策略類型                                     ''
策略代碼                                     ''
交易所                                       TAIFEX
商品代碼    BI03020 STOCK_NO 股票代號        pos.code
交易類型                                     ''
庫存成本 BI03310    TOT_COST                 cost
庫存數量 BI03270    TOT_QTY                  pos.lots 
在途數量 BI03270 -  BI03260                  0
         TOT_QTY - QTY = SEND_QTY 
未實現損益 總庫存市值 - 總庫存成本           pos.unrealize
           TOT_AMT - TOT_COST
           BI03330 - BI03310
已實現損益                                   0
'''
# 連上dbfile
conn = sqlite3.connect(dbFile)
cursor = conn.cursor()
nolots = 0
# 先建立交易員帳號群組
for accEntry in cursor.execute("Select user_id, alias from trade_account where exchange == 'TWSE'"):
    tuser = accEntry[0]
    tacc = accEntry[1]
    if not(tacc in traderMap):
        traderMap[tacc] = []
    traderMap[tacc].append(tuser)
    pass

# 清空中菲庫存
cursor.execute("Delete from balance_info where changed_by == 'Python-DDSC'")
cursor.execute("select max(sequence) from balance_info")

# 檢查sql內index最大值
try:
    for row in cursor:
       i = row[0]
    if i == None:
        i = 0
    pass
except Exception as e:
    print 'CheckDate() Exception=' ,e
    i = 0
    pass
print "i=",i

  
logFo = open(logFile, "a")
# 確認是否當天庫存
if TodayFile :
    # 如果inFile不存在，取消轉庫存
    if not os.path.exists(inFile):
        transdesc ="檔案大小為0或檔案不存在，請檢查庫存檔\n若無誤，可忽略此訊息；若有誤，請修正庫存檔，再執行「中菲庫存轉檔排程」\nClient需要重新update\nRelayServer需要重載庫存檔"
        logFo.write(transdesc)
        logFo.write('\r\n')
    else:
        data = pd.read_csv(inFile, sep=',', encoding = 'latin-1')
        FileTime = str(data.loc[0,'BI03010']).replace('/','')
        # 確認為當天的庫存檔
        if FileTime == strToday:
            for db in data.index:
                strAcc = data.loc[db,'BI03030']
                strAcc = str(strAcc)
                # 如果traderhead非空集合，但是strAcc不在traderhead
                # 跳過此次轉檔
                if traderMap == {} or strAcc not in traderMap.keys():
                    continue
                strCode = data.loc[db,'BI03020']
                strCode = strCode.strip() + ".TWSE"
                strLots = data.loc[db,'BI03270']
                iLots = int(strLots)
                if iLots == 0:
                    continue
                iCost = data.loc[db,'BI03310'] 
                #iCost = float(data.loc[db,'BI03310']) / iLots
                iunrealize = data.loc[db,'BI03330'] - iCost
                irealize = 0
                strAlias = ""
                strKey = strAcc + strCode
                checkPosition(strKey, strCode, strAcc, strAlias, iLots, iunrealize, irealize, iCost)
            pass
            if __name__ == "__main__":
                for pos in balMap.values():
                    i += 1
                    for acc in getTraderID(pos.account, traderMap):
                        writeLogToDB(acc, pos, strToday, cursor, DDSC)
                        i += 1
                    writeLogToDB("RelayServer", pos, strToday, cursor, DDSC)
                    i += 1
                    pass
                pass
            # 將Excel移至備份區並產生log
            transdesc = writeLogFile(inFile, logFo, 'DBBI03P.csv', '中菲', strTime, FileTime, balMap, nolots, transdesc)
        else:
            transdesc ="{0}  中菲 {1}庫存與目前日期不符".format(strTime,FileTime)
            logFo.write(transdesc)
            logFo.write('\r\n')
        pass
    pass
else:# 強制寫庫存檔
    # 如果inFile不存在，取消轉庫存
    if not os.path.exists(inFile):
        transdesc ="檔案大小為0或檔案不存在，請檢查庫存檔\n若無誤，可忽略此訊息；若有誤，請修正庫存檔，再執行「中菲庫存轉檔排程」\nClient需要重新update\nRelayServer需要重載庫存檔"
        logFo.write(transdesc)
        logFo.write('\r\n')
    else:
        data = pd.read_csv(inFile, sep=',', encoding = 'latin-1')
        FileTime = str(data.loc[1,'BI03010']).replace('/','')
        for db in data.index:
            strAcc = data.loc[db,'BI03030']
            strAcc = str(strAcc)
            if traderMap == {} or strAcc not in traderMap.keys():
                continue
            strCode = data.loc[db,'BI03020']
            strCode = strCode.strip() + ".TWSE"
            strLots = data.loc[db,'BI03270']
            iLots = int(strLots)
            if iLots == 0:
                continue
            iCost = data.loc[db,'BI03310']
            #iCost = float(data.loc[db,'BI03310']) / iLots
            iunrealize = data.loc[db,'BI03330'] - iCost
            irealize = 0
            strAlias = ""
            strKey = strAcc + strCode 
            checkPosition(strKey, strCode, strAcc, strAlias, iLots, iunrealize, irealize, iCost)
        pass
        if __name__ == "__main__":
            for pos in balMap.values():
                i += 1
                for acc in getTraderID(pos.account, traderMap):
                    print "acc=",acc
                    writeLogToDB(acc, pos, strToday, cursor, DDSC)
                    i += 1
                writeLogToDB("RelayServer", pos, strToday, cursor, DDSC)
                i += 1
                pass
            pass
        # 將Excel移至備份區並產生log
        transdesc = writeLogFile(inFile, logFo, 'DBBI03P.csv', '中菲', strTime, FileTime, balMap, nolots, transdesc)
    pass
conn.commit()
conn.close()
logFo.close()

if transdesc.find("Success") == -1:
    transstatus = "Error"
else:
    if IsBalanceExpired(FileTime, strToday, 1):
        transstatus = "Warning"
        transdesc += "\n請確認庫存日期是否正確\nD:\\RTS\\ftpStock\\DBBI03P.csv\n若無誤，可忽略此訊息；若有誤，請修正庫存檔，再執行「中菲庫存轉檔排程」\nClient需要重新update\nRelayServer需要重載庫存檔"
    else:
        transstatus = "OK: Count=" + str(len(balMap))
  
writeStatusToDB(dbFile, "DBBI03P", transdesc, transstatus)

if __name__ == "__main__":
    print "Local Mode."
