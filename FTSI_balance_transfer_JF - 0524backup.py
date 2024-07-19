# -*- coding: UTF-8 -*-
import sys
import os
from datetime import datetime
import sqlite3
from datetime import date, timedelta
import pandas as pd
import pymssql
#import FTsettings
from FTsettings import *
import time
import shutil
import csv
jftransdesc = ""
if os.path.exists(JFncoInFile) : # os.stat(JFncoInFile).st_size != 0
    shutil.move(JFncoInFile, jfFile)
    
if os.path.exists(JFcomInFile) and os.stat(JFcomInFile).st_size != 0:
    shutil.copyfile(JFcomInFile, conFile)

CodeMap = {"FITX":"TXF",
           "FIMTX":"MXF",
           "FIMTX1":"MX1",
           "FIMTX2":"MX2",
           "FIMTX4":"MX4",
           "FIMTX5":"MX5",
           "FITE":"EXF",
           "FITF":"FXF",
           "FIXI":"XIF",
           "FIGT":"GTF",
           "FIT5":"T5F",
           "FICP":"CPF",
           "FIGB":"GBF",
           "FIGD":"GDF",
           "FIMS":"MSF",
           "FITG":"TGF"}
#轉換商品代碼的格式讓系統看得懂
def getTAIFEXCode(strContract, strYM, cp = "", strike = ""):
    if cp == "":
        intYM = int(strYM)
        mth = intYM % 100
        year = ((intYM / 100) % 10)
        ymCode = unichr((ord('A') + mth - 1)) + str(year).decode('utf-8') + u'.TAIFEX'
        return (strContract + ymCode)
    if cp == "C":
        intYM = int(strYM)
        mth = intYM % 100
        year = ((intYM / 100) % 10)
        ymCode = unichr((ord('A') + mth - 1)) + str(year).decode('utf-8') + u'.TAIFEX'
        return (strContract + str(int(strike)) + ymCode)
    elif cp == "P":
        intYM = int(strYM)
        mth = intYM % 100
        year = ((intYM / 100) % 10)
        ymCode = unichr((ord('M') + mth - 1)) + str(year).decode('utf-8') + u'.TAIFEX'
        return (strContract + str(int(strike)) + ymCode)

ContractDetails = {}
with open(conFile) as a: 
    for line in a:
        ContractDetails[line[7:14]] = int(line[113:120])/100.

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
    

#確認是期貨還是選擇權
def CheckFutorOpt(code):
    _code = code.strip().split(" ")
    if _code[0] in CodeMap:
        return CodeMap[_code[0]], ""
    if _code[-1] == "C" or _code[-1] == "P":
        return _code[0], _code[-1]
    if len(code) > 2:
        code = code[2:]
    return code, ""
'''
追蹤證券庫存檔的日期
因為證券庫存在第一金方面會每天轉
期權方面只有交易日才會轉
所以改成如果期權的庫存日期與證券一致
才執行轉庫存
'''

def CheckFileDateandSize():
    #期權檔案可能是空白或者沒有檔案
    #先確認有檔案並且檔案非空白
    if os.path.exists(jfFile) and os.stat(jfFile).st_size != 0:
        return True
    return False

def CheckDate():
    IsHoliday = True
    try:
        with open('D:\\RTS\\ftpStock\\holiday.csv','rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['TradeDate']==date.today().strftime("%Y/%m/%d"):
                    if row["Flag"] == "N":
                        IsHoliday = False
                    break
    except Exception as e:
        print 'CheckDate() Exception=' ,e
    return IsHoliday

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

i = 0
strToday = date.today().strftime("%Y-%m-%d")
strTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

conn = sqlite3.connect(dbFile)
cursor = conn.cursor()
if CheckDate(): 
    cursor.execute("Delete from balance_info where exchange == 'TAIFEX'")
    cursor.execute("select max(sequence) from balance_info")
else:
    sys.exit(0) 
try:
    row = cursor.fetchone()
    if(row is not None):
        i = cursor.fetchall()[0][0]
    else :
        i = 0
except:
    i = 0
nolots = 0

#日盛
jfMap = {}
#讀庫存建檔
if TodayFile:
    if CheckDate():
        with open(jfFile) as jf:
            for line in jf:
                FileTime = line[0:8]
                strAcc = str(line[18:25])
                strCode,strCp = CheckFutorOpt(line[25:32].strip())
                strYM = line[32:38]
                strStike = str(int(line[38:44]))
                strCode = getTAIFEXCode(strCode, strYM, cp=strCp, strike=strStike)
                if line[55:56] == "B":
                    strLots = int(line[76:80])
                else:
                    strLots = int(line[76:80]) * -1
                iLots = strLots
                #strOtherCost = int(line[89:101].strip())/100 + int(line[101:113].strip())/100 + int(line[113:125].strip())/100 + int(line[125:137].strip())/100
                iCost = int(line[80:89])/1000 * ContractDetails[line[25:32]] * int(iLots)# + strOtherCost
                iunrealize = int(line[137:147].strip())
                strKey = strAcc + strCode
                #if strKey == u'0000243TXFL7.TAIFEX':
                #    print iLots, iCost, iunrealize, ContractDetails[line[25:32]], int(line[80:89])
                if strKey in jfMap:
                    jfMap[strKey].lots += iLots
                    jfMap[strKey].unrealize += iunrealize
                    jfMap[strKey].cost += iCost
                else:
                    pos = PosInfo()
                    pos.code = strCode
                    pos.account = strAcc
                    pos.lots = iLots
                    pos.unrealize = iunrealize
                    pos.cost = iCost
                    jfMap[strKey] = pos
        #create sub-account dict
        logFo = open(logFile, "a")
        if datetime.strptime(FileTime, '%Y%m%d').strftime('%Y-%m-%d') == strToday:
            cursor.execute("select * from trade_account where exchange == 'TAIFEX'")
            rows = cursor.fetchall()
            sub_account = {}
            for row in rows:
                if not sub_account.has_key(row[8]):
                    sub_account[row[8]] = {row[0]:row[1]}
                else:
                    sub_account[row[8]].update({row[0]:row[1]})
            for pos in jfMap.values():
                if pos.lots == 0:
                    nolots += 1
                    continue
                if pos.account in sub_account:
                    for _account in sub_account[pos.account]:
                        i += 1
                        strSQL = "Insert into balance_info(user_id,account_alias,strategy_type,strategy_id,exchange,code,trade_tag,cost,volume,onway_volume,unrealized_pl,realized_pl,last_change,changed_by) Values('"  + _account + "','"
                        strSQL = strSQL + sub_account[pos.account][_account] + "','','','TAIFEX','" + pos.code + "',''," + str(pos.cost) + "," + str(pos.lots) + ",0," + str(pos.unrealize) + ",0,'" + strToday + "','Python')"
                        cursor.execute(strSQL)
                       
                        i += 1
                        strSQL = "Insert into balance_info(user_id,account_alias,strategy_type,strategy_id,exchange,code,trade_tag,cost,volume,onway_volume,unrealized_pl,realized_pl,last_change,changed_by) Values('RelayServer','"
                        strSQL = strSQL + sub_account[pos.account][_account] + "','','','TAIFEX','" + pos.code + "',''," + str(pos.cost) + "," + str(pos.lots) + ",0," + str(pos.unrealize) + ",0,'" + strToday + "','Python')"
                        cursor.execute(strSQL)
            if not os.path.exists('D:\\AuroraQuantitative\\DB\\old\\{0}'.format(date.today().strftime("%Y%m%d"))):
                os.makedirs('D:\\AuroraQuantitative\\DB\\old\\{0}'.format(date.today().strftime("%Y%m%d")))
            shutil.move(jfFile, 'D:\\AuroraQuantitative\\DB\\old\\{0}\\FUHNCO.txt'.format(date.today().strftime("%Y%m%d")))
            jftransdesc = "{0}  期貨Success 已完成轉入{1}庫存，共{2}筆".format(strTime,FileTime,len(jfMap)-nolots)
            logFo.write(jftransdesc)
            if len(jfMap) <= warningThreshold:
                logFo.write("  Exception: Too fewer records!!")
            logFo.write('\r\n')
        else:
            jftransdesc = "{0}  期貨 {1}庫存與目前日期不符".format(strTime,FileTime)
            logFo.write(jftransdesc)
            logFo.write('\r\n')
        logFo.close()
    else:
        logFo = open(logFile,'a')
        jftransdesc = "{0}  Jihsun File is not correct:file not exits or file size is 0!! Cancel data converting.".format(strTime)
        logFo.write(jftransdesc)
        logFo.write('\r\n')
        logFo.close()
else:  
    if CheckFileDateandSize():
        with open(jfFile) as jf:
            for line in jf:
                FileTime = line[0:8]
                strAcc = str(line[18:25])
                strCode,strCp = CheckFutorOpt(line[25:32].strip())
                strYM = line[32:38]
                strStike = str(int(line[38:44]))
                strCode = getTAIFEXCode(strCode, strYM, cp=strCp, strike=strStike)
                if line[55:56] == "B":
                    strLots = int(line[76:80])
                else:
                    strLots = int(line[76:80]) * -1
                iLots = strLots
                #strOtherCost = int(line[89:101].strip())/100 + int(line[101:113].strip())/100 + int(line[113:125].strip())/100 + int(line[125:137].strip())/100
                iCost = int(line[80:89])/1000 * ContractDetails[line[25:32]] * int(iLots)# + strOtherCost
                iunrealize = int(line[137:147].strip())
                strKey = strAcc + strCode
                #if strKey == u'0000243TXFL7.TAIFEX':
                #    print iLots, iCost, iunrealize, ContractDetails[line[25:32]], int(line[80:89])
                if strKey in jfMap:
                    jfMap[strKey].lots += iLots
                    jfMap[strKey].unrealize += iunrealize
                    jfMap[strKey].cost += iCost
                else:
                    pos = PosInfo()
                    pos.code = strCode
                    pos.account = strAcc
                    pos.lots = iLots
                    pos.unrealize = iunrealize
                    pos.cost = iCost
                    jfMap[strKey] = pos
        #create sub-account dict
        cursor.execute("select * from trade_account where exchange == 'TAIFEX'")
        rows = cursor.fetchall()
        sub_account = {}
        for row in rows:
            if not sub_account.has_key(row[8]):
                sub_account[row[8]] = {row[0]:row[1]}
            else:
                sub_account[row[8]].update({row[0]:row[1]})
        for pos in jfMap.values():
            if pos.lots == 0:
                nolots += 1
                continue
            if pos.account in sub_account:
                for _account in sub_account[pos.account]:
                    print i
                    #if i == None:
                    #    i = 0
                    i += 1
                    strSQL = "Insert into balance_info(user_id,account_alias,strategy_type,strategy_id,exchange,code,trade_tag,cost,volume,onway_volume,unrealized_pl,realized_pl,last_change,changed_by)  Values('"  + _account + "','"
                    strSQL = strSQL + sub_account[pos.account][_account] + "','','','TAIFEX','" + pos.code + "',''," + str(pos.cost) + "," + str(pos.lots) + ",0," + str(pos.unrealize) + ",0,'" + strToday + "','Python')"
                    cursor.execute(strSQL)
                    
                    i += 1
                    strSQL = "Insert into balance_info(user_id,account_alias,strategy_type,strategy_id,exchange,code,trade_tag,cost,volume,onway_volume,unrealized_pl,realized_pl,last_change,changed_by)  Values('RelayServer','"
                    strSQL = strSQL + sub_account[pos.account][_account] + "','','','TAIFEX','" + pos.code + "',''," + str(pos.cost) + "," + str(pos.lots) + ",0," + str(pos.unrealize) + ",0,'" + strToday + "','Python')"
                    cursor.execute(strSQL)
            #log
        logFo = open(logFile, "a")
        if not os.path.exists('D:\\AuroraQuantitative\\DB\\old\\{0}'.format(date.today().strftime("%Y%m%d"))):
            os.makedirs('D:\\AuroraQuantitative\\DB\\old\\{0}'.format(date.today().strftime("%Y%m%d")))
        shutil.move(jfFile, 'D:\\AuroraQuantitative\\DB\\old\\{0}\\FUHNCO.txt'.format(date.today().strftime("%Y%m%d")))
        jftransdesc = "{0}  期貨Success 已完成轉入{1}庫存，共{2}筆".format(strTime,FileTime,len(jfMap)-nolots)
        logFo.write(jftransdesc)
        
        if len(jfMap) <= warningThreshold:
            jftransdesc = "  Exception: Too fewer records!!"
            logFo.write(jftransdesc)
        logFo.write('\r\n')
        logFo.close()
    else:
        logFo = open(logFile,'a')
        jftransdesc = "{0}  File is not correct:file not exits or file size is 0!! Cancel data converting.".format(strTime)
        logFo.write(jftransdesc)
        logFo.write('\r\n')
        logFo.close()
conn.commit()
conn.close()

if jftransdesc.find("Success") == -1:
    jftransstatus = "Error"
else:
    jftransstatus = "OK:Count=" +str(len(jfMap)-nolots)
  
writeStatusToDB("FUHNCO",jftransdesc,jftransstatus)
