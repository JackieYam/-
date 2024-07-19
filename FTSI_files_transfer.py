# -*- coding: UTF-8 -*-
import os
from balancedefs import *

fileTransferMsg = ""

Tag_SIZE = "ERRSIZE"
Tag_Date = "ERRDATE"
Tag_DataMissing = "ERRMISSING"
Tag_Length = "ERRLENGTH"
Tag_Pass = "PASS"

List_ErrStockID = []
transStatus = ""
BetaFile = u"D:\\RTS\\RiskControlParams\\CMoney_日常用技術指標表.txt"
FN07File = u"D:\\RTS\\ftpFuOp\\FN07"
PN07File = u"D:\\RTS\\ftpFuOp\\PN07"

FileDict = {"Beta":BetaFile, 
            "FN07":FN07File, 
            "PN07":PN07File}
#time.strftime('%Y%m%d',time.localtime(os.path.getmtime(BetaFile)))

#可能要客製化各個檔案的檢查方式
def DoSomeCheck(fileName):
    #先做檔案大小還有日期的檢查
    if not checkFileDateandSize(fileName):
        return Tag_SIZE
    fileData = time.strftime('%Y%m%d',time.localtime(os.path.getmtime(fileName)))
    if fileData != date.today().strftime("%Y%m%d"):
        return Tag_Date
    if fileName == BetaFile:
        #可能資料有缺
        #紀錄有缺的代號
        f = open(fileName)
        lines = f.readlines()
        for line in lines:
            tokens = line.split(',')
            if tokens[1] == "\n":
                List_ErrStockID.append(tokens[0])
        if List_ErrStockID != []:
            return Tag_DataMissing
        return Tag_Pass
    elif fileName == FN07File or fileName == PN07File:
        #每一筆資料為46個char
        f = open(fileName)
        length = len(f.readline())
        if (length % 46) != 0:
            return Tag_Length
    else:
        return Tag_Pass
    return Tag_Pass

        

def AddMsg(tag, fileName):
    tag = tag.upper()
    if tag == Tag_SIZE:
        return u"檔案大小有誤，請檢查或重新轉檔。\r\n檔案路徑為{}".format(fileName), "Warning"
    elif tag == Tag_Date:
        return u"檔案日期有誤，請檢查或重新轉檔。\r\n檔案路徑為{}".format(fileName), "Warning"
    elif tag == Tag_DataMissing:
        IDs = ""
        for i in List_ErrStockID:
            IDs += "{},".format(i)
        return u"檔案資料有漏，請檢查後重新轉檔。\r\n檔案路徑為{}\r\n證券代碼為: {}".format(fileName, IDs), "Warning"
    elif tag == Tag_Length:
        return u"檔案資料長度不正確，可能會造成讀檔錯誤。\r\n檔案路徑為{}".format(fileName), "Warning"
    elif tag == Tag_Pass:
        return u"轉檔完成", "OK"
    return u"轉檔完成", "OK"

if __name__ == "__main__":
    for key in FileDict.keys():
        #print _file
        fileName = FileDict[key]
        tag = DoSomeCheck(fileName)
        fileTransferMsg, transStatus = AddMsg(tag,fileName)
        writeStatusToDB(dbFile, key, fileTransferMsg, transStatus)
