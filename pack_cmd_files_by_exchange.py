# -*- coding: utf-8 -*-
import zipfile
import sys
import os
import shutil
import codecs
import sqlite3
import datetime
from datetime import *
import dsutilities

outputZipFolder = "C:\\AuroraQuantitative\\RamenFiles\\Data\\CmdFiles\\"
jqOutputZipFolder = "C:\\JQ\\CmdFiles\\"
srcfiles = ("C:\\AuroraQuantitative\\RamenFiles\\Data\\commodityinfo.csv",)
cmdsByExchange = {}

try:
    for strfile in srcfiles:
        if os.path.isfile(strfile) == False:
            continue
        rfile = open(strfile, "rb")
        lineData = rfile.readline()
        while lineData != "":
            lineData = lineData.decode('utf-8-sig')
            if lineData.isdigit():
                print lineData
                lineData = rfile.readline()
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
        pass
        rfile.close()
    pass
    ###############################################
    # For JQ, KSE Only
    ###############################################
    rfile = open("C:\\AuroraQuantitative\\DataImportOutput\\jq_kgicmds.csv", "rb")
    lineData = rfile.readline()
    while lineData != "":
        lineData = lineData.decode('utf-8-sig')
        if lineData.isdigit():
            lineData = rfile.readline()
            continue
        tokens = lineData.split(',')
        if len(tokens) <= 1:
            lineData = rfile.readline()
            continue
        strExchange = tokens[1]
        if strExchange != u"KSE":
            lineData = rfile.readline()
            continue
        pass
        if strExchange not in cmdsByExchange:
            cmdsByExchange[strExchange] = []
        pass
        cmdsByExchange[strExchange].append(lineData)
        lineData = rfile.readline()
    pass
    rfile.close()
    rfile = codecs.open("C:\\AuroraQuantitative\\DataService\\Uploads\\EsunnyCmds.csv", "rb", 'utf-8')
    lineData = rfile.readline()
    while lineData != "":
        if lineData.isdigit():
            lineData = rfile.readline()
            continue
        tokens = lineData.split(',')
        if len(tokens) <= 1:
            lineData = rfile.readline()
            continue
        pass    
        strExchange = tokens[1]
        if strExchange != u"DCE" and strExchange != u"HNX" and strExchange != u'TFEX' and strExchange != u'INE':
            lineData = rfile.readline()
            continue
        pass
        #直接Print會有問題，會有unicode error
        #用IDLE執行不會有Error，是用python.exe直接執行才會有
        print lineData.encode('utf-8')
        if strExchange not in cmdsByExchange:
            cmdsByExchange[strExchange] = []
        pass
        cmdsByExchange[strExchange].append(lineData)
        lineData = rfile.readline()
    pass
    rfile.close()
    ###############################################
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
            jqZipFile = jqOutputZipFolder + key + ".zip"
            file = zipfile.ZipFile(outputZipFile, "w")
            file.write(outputCSVFile, "commodityinfo.csv", zipfile.ZIP_DEFLATED)
            file.close()
            shutil.copy(outputZipFile, jqZipFile)
        try:
            shutil.copy("C:\\AuroraQuantitative\\RamenFiles\\Data\\CmdFiles\\TWSE.CSV", "C:\\AuroraQuantitative\\XQDataImporter\\TWSE.CSV")
        except:
            pass                
        dsutilities.writeStatusToDB('切分各交易所','將商品檔切分成各交易所(提供DS下載用)',('OK:Count=' + str(len(cmdsByExchange))))
    else:
        dsutilities.writeStatusToDB('切分各交易所','將商品檔切分成各交易所(提供DS下載用)','Error:No Data!!')
except:
    x = str(sys.exc_info()[0])
    print x
    dsutilities.writeStatusToDB('切分各交易所','將商品檔切分成各交易所(提供DS下載用)',('Error:' + x))
