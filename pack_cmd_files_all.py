# -*- coding: utf-8 -*-
import zipfile
import sys
import os
import shutil
import codecs
import datetime
from datetime import date
from datetime import *
import dsutilities

retlist = {}
outputCSVFile = "C:\\AuroraQuantitative\\RamenFiles\\Data\\commodityinfo.csv"
outputZipFile = "C:\\AuroraQuantitative\\RamenFiles\\Data\\commodityinfo.zip"
backupDir = "C:\\AuroraQuantitative\\RamenFiles\\Data\\"
srcfiles = (["C:\\AuroraQuantitative\\DataImportOutput\\cmdinfo_from_ctp.csv", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\ssestks.csv", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\szsestks.csv", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\etfopts.csv", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\indexes.csv", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\kgicmds.csv", {"CheckExcludedExchange":True, "ExcludedExchanges":{u"TAIFEX",u"TWSE"}}],
            ["C:\\AuroraQuantitative\\TWCmdTrasfer\\commodityinfo.csv", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DSDataReceiver\\Data\\TAIFEX\\commodityinfo.csv", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\jq_kgicmds.csv", {"ValidExchangeOnly":True, "ValidExchanges":{u"KSE"}, "CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataService\\Uploads\\EsunnyCmds.csv", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\hkstks.csv", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\q.csv", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\jpstks.csv", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\indiastks.csv", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\usstks_finhub.csv", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\hketfs.csv", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\bitmexCmds.txt", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\binanceCmds.txt", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\huobiCmds.txt", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],
            ["C:\\AuroraQuantitative\\DataImportOutput\\AddJRCmd.txt", {"CheckExcludedExchange":False, "ExcludedExchanges":{}}],)

warningLevel = 30000

try:
    for strfileEntry in srcfiles:
        strfile = strfileEntry[0]
        if os.path.isfile(strfile) == False:
            continue
        pass
        isExcludeExchanges = strfileEntry[1]["CheckExcludedExchange"]
        excludedExchanges = strfileEntry[1]["ExcludedExchanges"]
        if "ValidExchangeOnly" in strfileEntry[1]:
            isValidExchangesOnly = strfileEntry[1]["ValidExchangeOnly"]
            validExchanges = strfileEntry[1]["ValidExchanges"]
        else:
            isValidExchangesOnly = False
            validExchanges = None
        pass
        #解開每一個檔案
        print strfile, isExcludeExchanges, excludedExchanges
        rfile = open(strfile, "rb")
        lineData = rfile.readline()        
        while lineData != "":
            lineData = lineData.decode('utf-8-sig')
            tokens = lineData.split(',')
            if len(tokens) <= 5:
                lineData = rfile.readline()
                continue
            pass            
            strExch = tokens[1].strip()
            if isExcludeExchanges and strExch in excludedExchanges:
                lineData = rfile.readline()
                continue
            pass
            if isValidExchangesOnly and not strExch in validExchanges:
                lineData = rfile.readline()
                continue
            pass
            #將商品存到dictionary中，如果存在多個，會保留最後一筆
            retlist[tokens[0].strip()] = lineData
            lineData = rfile.readline()
        pass
    pass
    if len(retlist) != 0:
        #For Cooperative Bank
        ofile = codecs.open(outputCSVFile, "wb", "utf-8")
        ofile.write(str(len(retlist)))
        ofile.write("\r\n")
        for code in sorted(retlist):
            strData = retlist[code]
            if strData.find(u",SI,") != -1 and strData.find(u".COMEX,COMEX") != -1:
                strData2 = strData.replace(u"COMEX", u"NYMEX").replace(u",5000,",u",50,").replace(u"DV50",u"DV5000")
                print strData2
                ofile.write(strData2)
            else:
                ofile.write(strData)
        pass
        ofile.close()
        file = zipfile.ZipFile(outputZipFile, "w")
        file.write(outputCSVFile, "commodityinfo.csv", zipfile.ZIP_DEFLATED)
        file.close()
        shutil.copy(outputZipFile, "C:\\AuroraQuantitative\\RamenFiles\\UDONBIN\\Data\\Commodityinfo.zip")
        shutil.copy(outputZipFile, "C:\\AuroraQuantitative\\RamenFiles\\UDONBIN-NEW\\Data\\Commodityinfo.zip")
        ofile = codecs.open(outputCSVFile, "wb", "utf-8")
        ofile.write(str(len(retlist)))
        ofile.write("\r\n")
        for code in sorted(retlist):
            strData = retlist[code]
            if strData.isdigit():
                print strData
                continue
            pass
            ofile.write(strData)
        pass
        ofile.close()
        file = zipfile.ZipFile(outputZipFile, "w")
        file.write(outputCSVFile, "commodityinfo.csv", zipfile.ZIP_DEFLATED)
        file.close()
        shutil.copy(outputZipFile, "C:\\AuroraQuantitative\\ExecutionServer\\Data\\Commodityinfo.zip")
        shutil.copy(outputZipFile, "C:\\AuroraQuantitative\\QuoteServer\\Data\\Commodityinfo.zip")
        shutil.copy(outputZipFile, "C:\\AuroraQuantitative\\QuoteServer2\\Data\\Commodityinfo.zip")
        shutil.copy(outputZipFile, "C:\\AuroraQuantitative\\QuoteServer64\\Data\\Commodityinfo.zip")
        shutil.copy(outputZipFile, "C:\\AuroraQuantitative\\RelayOrderServer\\Data\\Commodityinfo.zip")
        shutil.copy(outputZipFile, "C:\\AuroraQuantitative\\RiskManager\\Data\\Commodityinfo.zip")
        shutil.copy(outputZipFile, "C:\\Apache24\htdocs\\Public\\Commodityinfo.zip")
        tt = date.today()
        backupDir = backupDir + str(tt)
        try:
            os.mkdir(backupDir)
        except:
            pass
        if len(retlist) < warningLevel:
            dsutilities.writeStatusToDB('打包商品檔', '將各零散的商品檔組成完整一包CommodityInfo.zip',('Warning:Count=' + str(len(retlist))))
        else:
            dsutilities.writeStatusToDB('打包商品檔', '將各零散的商品檔組成完整一包CommodityInfo.zip',('OK:Count=' + str(len(retlist))))
    else:
        dsutilities.writeStatusToDB('打包商品檔','將各零散的商品檔組成完整一包CommodityInfo.zip','Error:No Data!!')
except:
    x = str(sys.exc_info()[0])
    dsutilities.writeStatusToDB('打包商品檔','將各零散的商品檔組成完整一包CommodityInfo.zip', ('Error:' + x))
