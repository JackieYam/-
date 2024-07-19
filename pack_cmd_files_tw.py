import zipfile
import sys
import os
import shutil
import codecs

retlist = []
outputCSVFile = "C:\\NewPlatform\\RamenFiles\\Data-TW\\commodityinfo.csv"
outputZipFile = "C:\\NewPlatform\\RamenFiles\\Data-TW\\commodityinfo.zip"
srcfiles = ("C:\\NewPlatform\\TWCmdBuilder\\commodityinfo.csv",
            "C:\\AuroraQuantitative\\DataImportOutput\\indexes.csv",)

for strfile in srcfiles:
    if os.path.isfile(strfile) == False:
        continue
    rfile = codecs.open(strfile, "rb", "utf-8")
    lineData = rfile.readline()
    while lineData != "":
        tokens = lineData.split(',')
        if len(tokens) <= 1:
            lineData = rfile.readline()
            continue
        retlist.append(lineData)
        lineData = rfile.readline()

if len(retlist) != 0:
    ofile = codecs.open(outputCSVFile, "wb", "utf-8")
    ofile.write(str(len(retlist)))
    ofile.write("\r\n")
    for strData in retlist:
        ofile.write(strData)
    ofile.close()
    file = zipfile.ZipFile(outputZipFile, "w")
    file.write(outputCSVFile, "commodityinfo.csv", zipfile.ZIP_DEFLATED)
    file.close()
    shutil.copy(outputZipFile, "C:\\AuroraQuantitative\\QuoteServer\\Data\\Commodityinfo.zip")
