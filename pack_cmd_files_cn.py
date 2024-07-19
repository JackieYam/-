import zipfile
import sys
import os
import shutil
import codecs

retlist = []
outputCSVFile = "C:\\AuroraQuantitative\\RamenFiles\\Data-CN\\commodityinfo.csv"
outputZipFile = "C:\\AuroraQuantitative\\RamenFiles\\Data-CN\commodityinfo.zip"
srcfiles = ("C:\\AuroraQuantitative\\DataImportOutput\\cmdinfo_from_ctp.csv",
            "C:\\AuroraQuantitative\\DataImportOutput\\ssestks.csv",
            "C:\\AuroraQuantitative\\DataImportOutput\\szsestks.csv",         
            "C:\\AuroraQuantitative\\DataImportOutput\\etfopts.csv",
            "C:\\AuroraQuantitative\\XSpeedCmdBuilder\\commodityinfo.csv")

for strfile in srcfiles:
    if os.path.isfile(strfile) == False:
        continue
    rfile = codecs.open(strfile, 'rb', 'utf-8')
    lineData = rfile.readline()
    while lineData != '':
        #lineData = lineData.decode('utf-8-sig')
        tokens = lineData.split(',')
        if len(tokens) <= 1:
            lineData = rfile.readline()
            continue
        retlist.append(lineData)
        lineData = rfile.readline()

if len(retlist) != 0:
    ofile = codecs.open(outputCSVFile, "wb", 'utf-8')
    ofile.write(str(len(retlist)))
    ofile.write("\r\n")
    for strData in retlist:
        ofile.write(strData)
    ofile.close()
    file = zipfile.ZipFile(outputZipFile, "w")
    file.write(outputCSVFile, "commodityinfo.csv", zipfile.ZIP_DEFLATED)
    file.close()
    shutil.copy(outputZipFile, "C:\\AuroraQuantitative\\MusubiQuoteServer-CTP-Test\\Data\\Commodityinfo.zip")

