import zipfile
import sys
import os

retlist = []
outputCSVFile = "D:\\AuroraQuantitative\\RamenFiles\\Data\\commodityinfo.csv"
outputZipFile = "D:\\AuroraQuantitative\\RamenFiles\\Data\\commodityinfo.zip"
srcfiles = ("D:\\AuroraQuantitative\\TWCmdTransfer\\Indexes.csv",
            "D:\\AuroraQuantitative\\TWCmdTransfer\\commodityinfo.csv")

for strfile in srcfiles:
    rfile = open(strfile, "rb")
    lineData = rfile.readline()
    while lineData != "":
        tokens = lineData.split(',')
        if len(tokens) <= 1:
            lineData = rfile.readline()
            continue
        retlist.append(lineData)
        lineData = rfile.readline()

if len(retlist) != 0:
    ofile = open(outputCSVFile, "wb")
    ofile.write(str(len(retlist)))
    ofile.write("\r\n")
    for strData in retlist:
        ofile.write(strData)
    ofile.close()
    file = zipfile.ZipFile(outputZipFile, "w")
    file.write(outputCSVFile, "commodityinfo.csv", zipfile.ZIP_DEFLATED)
    file.close()
