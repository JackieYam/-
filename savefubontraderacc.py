# -*- coding: cp950 -*-
import zipfile
import sys
import os
import shutil
import codecs
import sqlite3
import datetime
from datetime import *

outputTraderAccFile = "C:\\AuroraQuantitative\\TraderAccount.csv"
sqliteDBFile = "C:\\AuroraQuantitative\\DB\\dataservice.db3"

class AccountData:
    """Account Data"""
    def __init__(self):
        self.alias = ''
        self.exchange = ''
        self.account = ''
        self.userid = ''

traderMap = {}

conn = sqlite3.connect(sqliteDBFile)
cursor = conn.cursor()
for accEntry in cursor.execute("Select user_id, exchange, alias, subaccount from trade_account"):
    tuser = accEntry[0].encode('ascii')
    texch = accEntry[1].encode('ascii')
    talias = accEntry[2].encode('ascii')
    tacc = accEntry[3].encode('ascii')
    strKey = tuser
    if not(strKey in traderMap):
        traderMap[strKey] = []
    accInfo = AccountData()
    accInfo.alias = talias
    accInfo.exchange = texch
    accInfo.account = tacc
    accInfo.userid = tuser
    traderMap[strKey].append(accInfo)
conn.close()


fobj = open(outputTraderAccFile, "wb+")
try:
    outLines = {}
    print 'Get Users'
    users = sys.argv[1].split(',')
    for strUser in users:
        if strUser in traderMap:
            for accData in traderMap[strUser]:
                print accData.account
                strOut = accData.account + ','
                if accData.exchange == 'TAIFEX':
                    strOut += '1'
                elif accData.exchange == 'TWSE':
                    strOut += '3'
                else:
                    strOut += '2'
                strOut += ','
                strOut += accData.userid
                outLines[strOut] = 0
                print strOut
    for vkey,vdata in outLines.items():
        fobj.write(vkey)
        fobj.write('\r\n')
    fobj.close()
except:
    print sys.exc_info()

#raw_input()
