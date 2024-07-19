# -*- coding: UTF-8 -*-
import sys
import os
from datetime import datetime
import sqlite3
from datetime import date, timedelta
import pandas as pd
#import FTsettings
from FTsettings import *
import time
import shutil
import csv
from FTsettings import *
from balancedefs import *
from commoditydefs import *
DefaultCommodityManager = CommodityManager()
DefaultCommodityManager.LoadFromZipFile(CommodityInfoFile)

#變數:轉檔狀態說明，用來在最後輸出轉檔狀態說明使用，最後會寫入ImportStatus
transdesc = "" 
#變數:檢查是不是直接傳交易所代碼的狀態結果，最後會寫入ImportStatus
exchangecodedesc = ""
#變數:檢查不在CodeMap的代碼的狀態結果，最後會寫入ImportStatus
codemapdesc = ""
#變數:檢查轉出的庫存代碼有沒有在商品檔案中的狀態結果，最後會寫入ImportStatus
commoditydesc = ""
importFile = "FUTMAT"
nolots = 0
strTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
traderMap = {}

def getTraderInfo(accID):
    if accID in traderMap:
        return traderMap[accID]
    return None

def getTAIFEXContractID(cpFlag, ctID):
    if cpFlag == 'C' or cpFlag == 'P':
        return ctID
    if ctID in CodeMap:
        return CodeMap[ctID]
    if len(ctID) > 2 and ctID[0:2] == "FI":
        return ctID[2:]
    if len(ctID) == 4 and ctID[0:2] == "FI":
        return ctID[2:] + "F"
    return ctID

#轉換商品代碼的格式讓系統看得懂
def getTAIFEXCode(strContract, strYM, cp = "", dblStrike = 0.0):
    if cp == "":
        intYM = int(strYM)
        mth = intYM % 100
        year = ((intYM / 100) % 10)
        ymCode = unichr((ord('A') + mth - 1)) + str(year).decode('utf-8') + u'.TAIFEX'
        return (strContract + ymCode)
    if dblStrike < 2000.0:
        dblStrike = dblStrike * 10;
    strStrike = str(int(dblStrike)).zfill(5)
    if cp == "C":
        intYM = int(strYM)
        mth = intYM % 100
        year = ((intYM / 100) % 10)
        ymCode = unichr((ord('A') + mth - 1)) + str(year).decode('utf-8') + u'.TAIFEX'
        return (strContract + strStrike + ymCode)
    elif cp == "P":
        intYM = int(strYM)
        mth = intYM % 100
        year = ((intYM / 100) % 10)
        ymCode = unichr((ord('M') + mth - 1)) + str(year).decode('utf-8') + u'.TAIFEX'
        return (strContract + strStrike + ymCode)
    return '--'
'''
def writeStatusToDB(filename, description, message):   
    try:
        conn = sqlite3.connect(dbFile)
        strTT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")      
        c = conn.cursor()
        strSQL = ('Replace Into file_imports Values(\'' + filename + '\',\'' + description + '\',\'' + strTT + '\',\'' + message + '\',\'' + strTT + '\',\'Python\')')
        c.execute(strSQL)
        conn.commit()
        conn.close()
    except Exception as e:
        print 'Exception=' ,e
    
'''
#確認是期貨還是選擇權
def CheckFutorOpt(code):
    _code = code.strip().split(" ")
    if _code[0] in CodeMap:
        return CodeMap[_code[0]], ""
    if _code[-1] == "C" or _code[-1] == "P":
        return _code[0], _code[-1]
    return code
'''
追蹤證券庫存檔的日期
因為證券庫存在第一金方面會每天轉
期權方面只有交易日才會轉
所以改成如果期權的庫存日期與證券一致
才執行轉庫存
'''

class TraderInfo:
    def __init__(self):
        self.userID = ''
        self.alias = ''
        self.account = ''
        self.subaccount= ''

class PosInfo:
    def __init__(self):
        self.lots = 0
        self.code = ''
        self.account = ''
        self.unrealize = 0
        self.cost = 0

def getTraderID(accID):
    if accID in traderMap:
        return traderMap[accID]
    return (accID,)
traderMap = {}


conn = sqlite3.connect(dbFile)
cursor = conn.cursor()

#先建立交易員帳號群組
for accEntry in cursor.execute("Select user_id, alias, account, subaccount from trade_account where ordermanager_id='RS' And Exchange='TAIFEX'"):
    tuser = accEntry[0]
    talias = accEntry[1]
    tacc = accEntry[2]
    tsubacc = accEntry[3]
    trInfo = TraderInfo()
    trInfo.userID = tuser
    trInfo.alias = talias
    trInfo.account = tacc
    trInfo.subaccount = tsubacc
    if not(tsubacc in traderMap):
        traderMap[tsubacc] = []
    traderMap[tsubacc].append(trInfo)
logFo = open(logFile, "a")
nolots = 0
cursor.execute("delete from balance_info where changed_by = 'Python-SYSCOM'")
cursor.execute("select max(sequence) from balance_info")
#第一金
FFHMap = {}
#讀庫存建檔
if checkFileDateandSize(FFHMATFile):
    with open(FFHMATFile) as fobj:
        for line in fobj:
            header = line[0:3]
            if header == 'BOF' or header == 'EOF':
                FileTime = line[13:21]
                continue
            offset = 0
            #LMAT-BROKER-ID	X(07)	期貨商代號
            brokerID = line[offset:(offset+7)]
            offset += 7
            #FILLER	X(1)  	 "|"
            offset += 1
            #LMAT-MATCH-DATE	9(08)	成交日期
            matchDate = line[offset:(offset+8)]
            offset += 8
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-INVESTOR-ACNO	X(07)	投資人帳號
            investorAcNo = line[offset:(offset + 7)]
            offset += 7
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-COMMODITY-ID	X(07)	商品代號
            ctID = line[offset:(offset+7)]
            offset += 7
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-SETTLEMENT-MONTH	9(06)	商品年月
            settleMonth = line[offset:(offset + 6)]
            offset += 6
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-STRIKE-PRICE	9(06).9(03)	履約價
            strikePrice = line[offset:(offset + 10)]
            offset += 10
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-BUY-SELL-KIND	X(01)	買/賣別
            buySellKind = line[offset:(offset + 1)]
            offset += 1
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-SEQNO	9(04)	流水號
            offset += 4
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-MATCH-PRICE	9(06).9(03)	成交價/交割價
            matPrice = line[offset:(offset + 10)]
            offset += 10
            #FILLER	X(1)  	 "|"        
            offset += 1
            #LMAT-MATCH-QTY	9(04)	成交口數
            matQty = line[offset:(offset + 4)]
            offset += 4
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-NON-COVER-QTY	9(04)	未完全平倉口數
            nonCoverQty = line[offset:(offset + 4)]
            offset += 4
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-CANCEL-FLAG	X(01)	註銷記號
            offset += 1
            #FILLER	X(1)  	 "|"        
            offset += 1
            #LMAT-CONTRACT-SIZE	9(05).9(04)	個股期購入時股數
            offset += 10
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-CURRENCY	X(03)	交易幣別
            currency = line[offset:(offset + 3)]
            offset += 3
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-DAY-TRADE-ID	X(01)	當日沖銷碼
            offset += 1
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-DOS-IN-KIND	X(01)	委託下單方式
            offset += 1
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-EXCH-TAX	-9(09).9(2)	交易稅/交割費用二
            offset += 13
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-FEE	-9(09).9(2)	手續費/交割費用一
            offset += 13
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-FEE-CURRENCY	X(03)	手續費幣別
            offset += 3
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-LAST-SOLD-DATE	9(08)	最後銷帳日
            offset += 8
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-LOCK-OFFSET-FLAG	X(01)	鎖定盤中不沖銷註記
            offset += 1
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-OPEN-OFFSET-KIND	X(01)	新增/沖銷別
            offset += 1
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-ORDER-NO-4	X(05)	委託書編號
            offset += 5
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-OTHER-AMT	-9(09).9(2)	其它費用2
            offset += 13
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-SOURCE-FLAG	X(01)	資料來源
            offset += 1
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-SPREAD-ODR-FLAG	X(01)	複式委託註記
            offset += 1
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-SPREAD-QTY	9(04).9(02)	組合(價差)口數
            offset += 7
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-STOCK-FUT	X(03)	個股期購入時商品代號
            stkFut = line[offset:(offset + 3)]
            offset += 3
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            #LMAT-VALUE-ADDED-TAX	-9(09).9(02)	其他費用1/交割費用三
            offset += 13
            #FILLER	X(1)  	 "|"                                           
            offset += 1
            cpFlag = ctID[-1].strip()
            contractID = ctID[0:(len(ctID) - 1)].strip()
            contractID = getTAIFEXContractID(cpFlag, contractID)        
            strCode = getTAIFEXCode(contractID, settleMonth, cpFlag, float(strikePrice))
            buySellKind = buySellKind.strip()
            iLots = int(nonCoverQty)
            if buySellKind == 'S':
                iLots *= -1
            fCost = float(matPrice)*iLots
            #fCost = float(matPrice)
            iunrealize = 0
            strKey = investorAcNo + strCode
            if strKey in FFHMap:
                pos = FFHMap[strKey]
                pos.lots += iLots
                pos.unrealize += iunrealize
                pos.cost += fCost
            else:
                pos = PosInfo()
                pos.code = strCode
                pos.account = investorAcNo
                pos.lots = iLots
                pos.unrealize = iunrealize
                pos.cost = fCost
                FFHMap[strKey] = pos
            pass
        pass
    strToday = date.today().strftime("%Y-%m-%d")
    strTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for k, v in FFHMap.iteritems():
        costPrice = 0.0
        if v.lots != 0:
            costPrice = float(v.cost / v.lots)
        print v.account, v.code, costPrice , v.lots
        trInfos =  getTraderInfo(v.account)
        if not (trInfos is None):
            print trInfos
            for trInfo in trInfos:
                print trInfo.userID, v.code
                strSQL = "Insert into balance_info(user_id,account_alias,strategy_type,strategy_id,exchange,code,trade_tag,cost,volume,onway_volume,unrealized_pl,realized_pl,last_change,changed_by) "
                strSQL = strSQL + "Values('"  + trInfo.userID + "','"
                strSQL = strSQL + trInfo.alias + "','','','TAIFEX','" + v.code + "',''," + str(costPrice) + "," + str(v.lots) + ",0," + str(pos.unrealize) + ",0,'" + strToday + "','Python-SYSCOM')"
                cursor.execute(strSQL)

                strSQL = "Insert into balance_info(user_id,account_alias,strategy_type,strategy_id,exchange,code,trade_tag,cost,volume,onway_volume,unrealized_pl,realized_pl,last_change,changed_by) Values('RelayServer','"
                strSQL = strSQL + trInfo.alias + "','','','TAIFEX','" + v.code + "',''," + str(costPrice) + "," + str(v.lots) + ",0," + str(pos.unrealize) + ",0,'" + strToday + "','Python-SYSCOM')"
                print strSQL
                cursor.execute(strSQL)
        conn.commit()
    transdesc = writeLogFile(FFHMATFile, logFo, 'FUTMAT', '凌群', strTime, FileTime, FFHMap, nolots, transdesc)
    pass
else:
    transdesc = "檔案大小為0或檔案不存在，請檢查庫存檔\n若無誤，可忽略此訊息；若有誤，請修正庫存檔，再執行「凌群庫存轉檔排程」\nClient需要重新update\nRelayServer需要重載庫存檔"
    transdesc = writeLogFile(FFHMATFile, logFo, 'FUTMAT', '凌群', strTime, "", FFHMap, nolots, transdesc)

conn.close()

if transdesc.find("Success") == -1:
    transstatus = "Error"
else:
    if IsBalanceExpired(FileTime, strToday, 0):
        transstatus = "Warning"
        transdesc += "\n請確認庫存日期是否正確\nD:\\RTS\\ftpFuOp\\FUTMAT\n若無誤，可忽略此訊息；若有誤，請修正庫存檔，再執行「凌群庫存轉檔排程」\nClient需要重新update\nRelayServer需要重載庫存檔"
    else:
        transstatus = "OK:Count=" +str(len(FFHMap)-nolots)
writeStatusToDB(dbFile, importFile, transdesc, transstatus)

#檢查是不是直接傳交易所代碼
if exchangecodedesc == "":
    exchangecodestatus = "OK"
    exchangecodedesc = ""
else:
    exchangecodestatus = "Error:Count=" + str(exchangecodedesc.count(","))
writeStatusToDB(dbFile,"FUTMAT-三位數代碼", exchangecodedesc.encode('utf-8'), exchangecodestatus)

#檢查不在CodeMap的代碼
if codemapdesc == "":
    codemapdescstatus = "OK"
    codemapdesc = ""
else:
    codemapdescstatus = "Error:Count=" + str(codemapdesc.count(","))
writeStatusToDB(dbFile,"FUTMAT-CodeMap無法辨識的代碼", codemapdesc.encode('utf-8'),codemapdescstatus)

#檢查轉出的庫存代碼有沒有在商品檔案中
for pos in FFHMap.values():
    if not DefaultCommodityManager.GetCommodity(pos.code):
        commoditydesc += pos.code + ", "

if commoditydesc == "":
    commoditystatus = "OK"
    commoditydesc = ""
else:
    commoditystatus = "Error:Count=" + str(commoditydesc.count(","))
writeStatusToDB(dbFile,"FUTMAT-商品檔無法辨識的代碼".format(importFile), commoditydesc.encode('utf-8'), commoditystatus)
