# -*- coding: UTF-8 -*-
import sys
import os
import time
import shutil
import csv
import pymssql
import sqlite3
import pandas as pd
from datetime import datetime
from datetime import date, timedelta
from FTsettings import *
from balancedefs import *

jftransdesc = ""
ContractDetails = {}
nolots = 0
i = 0
traderMap = {}
strToday = date.today().strftime("%Y-%m-%d")
strTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
conn = sqlite3.connect(dbFile)
cursor = conn.cursor()
# 先建立交易員帳號群組
for accEntry in cursor.execute("Select user_id, account from trade_account \
    where ordermanager_id='RS'"):
    tuser = accEntry[0]
    tacc = accEntry[1]
    if not(tacc in traderMap):
        traderMap[tacc] = []
    traderMap[tacc].append(tuser)


'''追蹤證券庫存檔的日期

因為證券庫存在第一金方面會每天轉
期權方面只有交易日才會轉
所以改成如果期權的庫存日期與證券一致
才執行轉庫存
'''

if os.path.exists(JFncoInFile) : # os.stat(JFncoInFile).st_size != 0
    shutil.move(JFncoInFile, jfFile)

if os.path.exists(JFcomInFile) and os.stat(JFcomInFile).st_size != 0:
    shutil.copyfile(JFcomInFile, conFile)

# 如果當天是交易日就刪除TAIFEX庫存
# 反之，取消執行轉檔
if CheckDate(): 
    cursor.execute("Delete from balance_info where changed_by == 'Python-JF'")
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

with open(conFile) as a: 
    for line in a:
        ContractDetails[line[7:14]] = int(line[113:120])/100.

logFo = open(logFile, "a")
# 讀庫存建檔
if TodayFile:
    if CheckDate():
        with open(jfFile) as jf:
            for line in jf:
                FileTime = line[0:8]
                strAcc = str(line[18:25])
                strCode,strCp = CheckFutorOpt(line[25:32].strip(), CodeMap)
                strYM = line[32:38]
                strStike = str(int(line[38:44]))
                strCode = getTAIFEXCode(strCode, strYM, cp=strCp, strike=strStike)
                if line[55:56] == "B":
                    strLots = int(line[76:80])
                else:
                    strLots = int(line[76:80]) * -1
                iLots = strLots
                #iCost = int(line[80:89])/1000 * ContractDetails[line[25:32]] * int(iLots)
                iCost = int(line[80:89])/1000 * int(iLots)
                iunrealize = int(line[137:147].strip())
                strKey = strAcc + strCode
                checkPosotion(strKey, strCode, strAcc, iLots, iunrealize, iCost)
            pass
        pass
        # create sub-account dict
        if datetime.strptime(FileTime, '%Y%m%d').strftime('%Y-%m-%d') == strToday:
            cursor.execute("select * from trade_account where exchange == 'TAIFEX'")
            rows = cursor.fetchall()
            sub_account = {}
            for row in rows:
                if not sub_account.has_key(row[8]):
                    sub_account[row[8]] = {row[0]:row[1]}
                else:
                    sub_account[row[8]].update({row[0]:row[1]})
                pass
            pass
            for pos in balMap.values():
                if pos.lots == 0:
                    nolots += 1
                    continue
                pass
                if pos.account in sub_account:
                    for _account in sub_account[pos.account]:
                        pos.alias = sub_account[pos.account][_account]
                        i += 1
                        writeLogToDB(_account, pos, strToday, cursor, JF)
                    i += 1
                    writeLogToDB("RelayServer", pos, strToday, cursor, JF)
                    pass
            transdesc = writeLogFile(JFncoInFile, logFo, 'FUHNCO.txt', '期貨', strTime, FileTime, balMap, nolots)
        else:
            transdesc = "{0}  期貨 {1}庫存與目前日期不符".format(strTime,FileTime)
            logFo.write(transdesc)
            logFo.write('\r\n')
        pass
    else:
        transdesc = "{0}  Jihsun File is not correct:file not exits or file size is 0!! Cancel data converting.".format(strTime)
        logFo.write(transdesc)
        logFo.write('\r\n')
    pass
else:  
    if checkFileDateandSize(jfFile):
        with open(jfFile) as jf:
            for line in jf:
                FileTime = line[0:8]
                strAcc = str(line[18:25])
                strCode,strCp = CheckFutorOpt(line[25:32].strip(), CodeMap)
                strYM = line[32:38]
                strStike = str(int(line[38:44]))
                strCode = getTAIFEXCode(strCode, strYM, cp=strCp, strike=strStike)
                if line[55:56] == "B":
                    strLots = int(line[76:80])
                else:
                    strLots = int(line[76:80]) * -1
                iLots = strLots
                #iCost = int(line[80:89])/1000 * ContractDetails[line[25:32]] * int(iLots)# + strOtherCost
                iCost = int(line[80:89])/1000 * int(iLots)# + strOtherCost
                iunrealize = int(line[137:147].strip())
                strKey = strAcc + strCode
                checkPosotion(strKey, strCode, strAcc, iLots, iunrealize, iCost)
            pass
        #create sub-account dict
        cursor.execute("select * from trade_account where exchange == 'TAIFEX'")
        rows = cursor.fetchall()
        sub_account = {}
        for row in rows:
            if not sub_account.has_key(row[8]):
                sub_account[row[8]] = {row[0]:row[1]}
            else:
                sub_account[row[8]].update({row[0]:row[1]})
        for pos in balMap.values():
            print pos.account
            if pos.lots == 0:
                nolots += 1
                continue
            if pos.account in sub_account:
                for _account in sub_account[pos.account]:
                    pos.alias = sub_account[pos.account][_account]
                    print i
                    i += 1
                    writeLogToDB(_account, pos, strToday, cursor, JF)
                i += 1
                writeLogToDB("RelayServer", pos, strToday, cursor, JF)
                pass
        #log
        transdesc = writeLogFile(JFncoInFile, logFo, 'FUHNCO.txt', '期貨', strTime, FileTime, balMap, nolots, jftransdesc)
    else:
        transdesc = "{0}  File is not correct:file not exits or file size is 0!! Cancel data converting.".format(strTime)
        logFo.write(transdesc)
        logFo.write('\r\n')
    pass
conn.commit()
conn.close()
logFo.close()

if transdesc.find("Success") == -1:
    transstatus = "Error"
else:
    transstatus = "OK:Count=" + str(len(traderMap)-nolots)
  
writeStatusToDB(dbFile, "FUHNCO", transdesc, transstatus)
