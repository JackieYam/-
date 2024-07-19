# -*- coding: cp950 -*-
import zipfile
import sys
import os
import shutil
import codecs
import sqlite3
import datetime
from datetime import *
import time
mToday = date.today()
outputZipFolder = "D:\\AuroraQuantitative\\RamenFiles\\CmdFiles\\"
srcfiles = ("D:\\AuroraQuantitative\\RamenFiles\\Data\\commodityinfo.csv",)

sqliteDBFile = "D:\\AuroraQuantitative\\DB\\dataservice.db3"

#check file date
bl_fileerror = False
filesToBeChecked = "D:\\AuroraQuantitative\\TWCmdTransfer\\"
files = ["T30.TSE","T30.OTC","FP08","PP08","FP09"]
for dirItem in files:
    print filesToBeChecked+dirItem
    if not os.path.isfile((filesToBeChecked + dirItem)):
        bl_fileerror= True
        break
    try:
        ival = int(time.strftime("%Y%m%d",time.localtime(os.path.getmtime(filesToBeChecked + dirItem))))
        mDay = (ival % 100)
        mMonth = (int((ival - mDay) / 100) % 100)
        mYear = int((ival / 10000))
        dtDir = date(mYear, mMonth, mDay)
        delta = mToday - dtDir
        if delta.days != 0:
            bl_fileerror= True
            break
    except Exception, e:
        print 'Error!!', e
        bl_fileerror= True
        break
    
if bl_fileerror == True:
    print filesToBeChecked + ' file was old!'
    pass #sys.exit(0)
print 'File date is today.'

def writeStatusToDB(filename, description, message):
    try:
        conn = sqlite3.connect(sqliteDBFile)
        tt = datetime.now()
        strTT = tt.strftime('%Y-%m-%d %H:%M:%S')        
        c = conn.cursor()
        strSQL = ('Replace Into file_imports Values(\'' + filename + '\',\'' + description + '\',\'' + strTT + '\',\'' + message + '\',\'' + strTT + '\',\'Python\')')
        c.execute(strSQL)
        conn.commit()
        conn.close()
    except:
        print 'Exception'
    
cmdsByExchange = {}
for strfile in srcfiles:
    if os.path.isfile(strfile) == False:
        continue
    rfile = open(strfile, "rb")
    lineData = rfile.readline()
    while lineData != "":
        lineData = lineData.decode('utf-8-sig')
        if lineData.isdigit():
            print lineData
            continue
        tokens = lineData.split(',')
        if len(tokens) <= 1:
            lineData = rfile.readline()
            continue
        strExchange = tokens[1]
        if strExchange not in cmdsByExchange:
            cmdsByExchange[strExchange] = []
        cmdsByExchange[strExchange].append(lineData)
        lineData = rfile.readline()

if len(cmdsByExchange) != 0:
    for key, value in cmdsByExchange.iteritems():
        outputCSVFile = outputZipFolder + key + ".csv"
        ofile = codecs.open(outputCSVFile, "wb", "utf-8")
        ofile.write(str(len(value)))
        ofile.write('\r')
        ofile.write('\n')
        for strData in value:
            ofile.write(strData)
        ofile.close()
        outputZipFile = outputZipFolder + key + ".zip"
        file = zipfile.ZipFile(outputZipFile, "w")
        file.write(outputCSVFile, "commodityinfo.csv", zipfile.ZIP_DEFLATED)
        file.close()    
    writeStatusToDB('CmdZips By Exchange','Zipped Commodity files by exchanges.',('OK:Count=' + str(len(cmdsByExchange))))
else:
    writeStatusToDB('CmdZips By Exchange','Zipped Commodity files by exchanges.','Error:No Data!!')
