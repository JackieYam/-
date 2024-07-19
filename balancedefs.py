# -*- coding: UTF-8 -*-
# 有關庫存轉檔相關function在此新增及修改
import os
import sqlite3
import datetime
import csv
import shutil
from datetime import date
from FTsettings import *
balMap = {}
traderMap = {}
class PosInfo:
    def __init__(self):
        self.lots = 0
        self.code = ''
        self.account = ''
        self.alias = ''
        self.onwaylots = 0
        self.realize = 0
        self.unrealize = 0
        self.cost = 0

# 將轉檔狀態寫入db3
def writeStatusToDB(dbFile, filename, description, message):
    try:
        conn = sqlite3.connect(dbFile)
        strTT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")      
        c = conn.cursor()
        strSQL = ('Replace Into file_imports Values(\'' + filename + '\',\'' 
            + description + '\',\'' + strTT + '\',\'' + message + '\',\'' 
            + strTT + '\',\'Python\')')
        c.execute(strSQL)
        conn.commit()
        conn.close()
    except Exception as e:
        print 'Exception=', e
        
# 轉換商品代碼的格式讓系統看得懂
def getTAIFEXCode(strContract, strYM, cp = "", strike = ""):
    if cp == "":
        intYM = int(strYM)
        mth = intYM % 100
        year = ((intYM / 100) % 10)
        ymCode = unichr((ord('A') + mth - 1)) \
            + str(year).decode('utf-8') + u'.TAIFEX'
        return (strContract + ymCode)
    if cp == "C":
        intYM = int(strYM)
        mth = intYM % 100
        year = ((intYM / 100) % 10)
        ymCode = unichr((ord('A') + mth - 1)) + str(year).decode('utf-8') \
            + u'.TAIFEX'
        return (strContract + str(int(strike)) + ymCode)
    elif cp == "P":
        intYM = int(strYM)
        mth = intYM % 100
        year = ((intYM / 100) % 10)
        ymCode = unichr((ord('M') + mth - 1)) + str(year).decode('utf-8') \
            + u'.TAIFEX'
        return (strContract + str(int(strike)) + ymCode)
        
# 期權檔案可能是空白或者沒有檔案，先確認有檔案並且檔案非空白
def checkFileDateandSize(file):
    if os.path.exists(file) and os.stat(file).st_size != 0:
        return True
    return False


# 取得交易原帳號
def getTraderID(accID, traderMap):
    if accID in traderMap:
        return traderMap[accID]
    return (accID,)

# 建立庫存dict
def checkPosition(strKey, strCode, strAcc, strAlias, iLots, iOnwayLots, iunrealize, irealize, iCost):
    if strKey in balMap:
        balMap[strKey].lots += iLots
        balMap[strKey].unrealize += iunrealize
        balMap[strKey].onwaylots += iOnwayLots
        balMap[strKey].realize += irealize
        balMap[strKey].cost += iCost
        pass
    else:
        pos = PosInfo()
        pos.code = strCode
        pos.account = strAcc
        pos.alias = strAlias
        pos.lots = iLots
        pos.onwaylots = iOnwayLots
        pos.unrealize = iunrealize
        pos.realize = irealize
        pos.cost = iCost
        balMap[strKey] = pos
        pass

# 確認是否為假日
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


# 確認是期貨還是選擇權
def CheckFutorOpt(code, CodeMap):
    _code = code.strip().split(" ")
    if _code[0] in CodeMap:
        return CodeMap[_code[0]], ""
    if _code[-1] == "C" or _code[-1] == "P":
        return _code[0], _code[-1]
    if len(code) > 2:
        code = code[2:]
    return code, ""

# 寫log到DB
def writeLogToDB(userID, pos, strToday, cursor, balsource):
    strSQL = "Insert into balance_info(user_id,account_alias,strategy_type,strategy_id,exchange,code,trade_tag,cost,volume,onway_volume,unrealized_pl,realized_pl,last_change,changed_by) Values('"  + userID + "','"
    if balsource == DDSC:
        strSQL = strSQL + pos.account + "','','','TWSE','" + pos.code + "',''," + str(float(pos.cost)/pos.lots) + "," + str(pos.lots) + "," + str(pos.onwaylots) + ",'" + str(pos.unrealize) + "','"+ str(pos.realize) + "','"+ strToday + "','Python-" + balsource + "')"
        #print pos.code, str(pos.cost)
    elif balsource == JF:
        strSQL = strSQL + pos.alias + "','','','TAIFEX','" + pos.code + "',''," + str(float(pos.cost)/pos.lots) + "," + str(pos.lots) + "," + str(pos.onwaylots) + ",'" + str(pos.unrealize) + "','"+ str(pos.realize) + "','"+ strToday + "','Python-" + balsource + "')"
    cursor.execute(strSQL)

# 寫log檔案
def writeLogFile(FileDir, logFo, filename, balancesource, strTime, FileTime, balMap, nolots, transdesc):
    if not os.path.exists('D:\\AuroraQuantitative\\DB\\old\\{0}'.format(date.today().strftime("%Y%m%d"))):
        os.makedirs('D:\\AuroraQuantitative\\DB\\old\\{0}'.format(date.today().strftime("%Y%m%d")))
    pass
    if not os.path.exists(FileDir):
        transdesc = "{0} 庫存檔不存在，取消轉檔。".format(strTime)
        return transdesc
    else:
        shutil.copy2(FileDir, 'D:\\AuroraQuantitative\\DB\\{0}'.format(filename))
    shutil.copy2(FileDir, 'D:\\AuroraQuantitative\\DB\\old\\{0}\\{1}'.format(date.today().strftime("%Y%m%d"), filename))
    transdesc = "{0}已轉入{1}庫存，共{2}筆，Success ".format(balancesource, FileTime, len(balMap)-nolots)
    logFo.write(transdesc)
    if len(balMap) < warningThreshold:
        transdesc = "  Exception: Too fewer records!!"
        logFo.write(transdesc)
    pass
    logFo.write('\r\n')
    return transdesc
    # 20191007 建宏希望將庫存檔複製(copy)至DB下而不是移動(move)，Alvie。

# 檢查庫存日期，超過一定天數會跳警示
def IsBalanceExpired(FileTime,strToday, daysToBeCheck):
    strToday = strToday.replace("-","")
    FileTime = FileTime.replace("-","")
    strToday = date(int(strToday[0:4]),int(strToday[4:6]), int(strToday[6:]))
    FileTime = date(int(FileTime[0:4]),int(FileTime[4:6]), int(FileTime[6:]))
    delta = strToday - FileTime
    if delta.days > daysToBeCheck:
        return True
    return False
