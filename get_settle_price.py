# -*- coding: utf-8 -*-
import requests
import pandas
import sqlite3

#--------------
dbFile= "c:\\AuroraQuantitative\\DB\\dataservice.db3"
dbtable = "settle_prices"

#https://www.taifex.com.tw/cht/5/futIndxFSP
IndexFuture = "https://www.taifex.com.tw/cht/5/FutIndxFSP"
IndexOption = "https://www.taifex.com.tw/cht/5/optIndxFSP"
StockFuture = "https://www.taifex.com.tw/cht/5/sSFFSP"
StockOption = "https://www.taifex.com.tw/cht/5/sSOFSP"
IndexF = ["TXF", "EXF", "FXF", "T5F", "XIF", "GTF", "TJF", "I5F", "UDF", "SPF"]
IndexO = ["TXO", "TEO", "TFO", "XIO", "GTO"]
#--------------

conn = sqlite3.connect(dbFile)
cursor = conn.cursor()

#Check whether table exists
cursor.execute("CREATE TABLE if not exists " + dbtable + "( `exchange` TEXT, `contract` TEXT, `month` Integer,  `settleprice` Real, PRIMARY KEY(`exchange`,`contract`,`month`) )")

def executecmd(listvalues_):
    cmd = "replace into " + dbtable + "(exchange,contract,month,settleprice) Values " + listvalues_
    print cmd
    cursor.execute(cmd)

#指數期貨
df = pandas.read_html(IndexFuture)[3]
listvalues = ""
for col in range(2,12):
    if df[col][1] != '-':
        strContract = IndexF[col-2]
        strMonth = df[1][1]
        if strMonth.find("W1") >= 0:
            strContract = "TX1"
            strMonth = strMonth.replace("W1", "")
        elif strMonth.find("W2") >= 0:
            strContract = "TX2"
            strMonth = strMonth.replace("W2", "")
        elif strMonth.find("W4") >= 0:
            strContract = "TX4"
            strMonth = strMonth.replace("W4", "")            
        elif strMonth.find("W5") >= 0:
            strContract = "TX5"
            strMonth = strMonth.replace("W5", "")            
        strIns = "('TAIFEX', '" + strContract + "', " + strMonth + ", " + df[col][1] + ")"
        print strIns
        if len(listvalues) > 0:
            listvalues += ", " + strIns
        else:
            listvalues += strIns

#指數選擇權
df = pandas.read_html(IndexOption)[3]
for col in range(2,7):
    if df[col][1] != '-':
        #print "('" + df[0][1] + "', '" + df[1][1] + "', '" + IndexF[col-2] + "', '" + df[col][1] + "')"
        #if len(listvalues) > 0:
        #    listvalues += ", " + "('" + df[0][1] + "', '" + df[1][1] + "', '" + IndexO[col-2] + "', '" + df[col][1] + "')"
        #else:
        #    listvalues += "('" + df[0][1] + "', '" + df[1][1] + "', '" + IndexO[col-2] + "', '" + df[col][1] + "')"
        pass
executecmd(listvalues)

#股票期貨
listvalues = ""
try: #it might have error when get info in new month
    df = pandas.read_html(StockFuture)[1]
    for row in df.index:
        if row > 0:
            strContract = df[4][row]
            strMonth = df[1][row]
            strPrice = df[5][row]
            print strContract, strMonth, strPrice
            #print "('" + df[3][row] + "', '" + df[4][row] + "', '" + df[1][row] + "', '" + df[5][row] + "')"
            #if len(listvalues) > 0:
            #    listvalues += ", " + "('" + df[3][row] + "', '" + df[4][row] + "', '" + df[1][row] + "', '" + df[5][row] + "')"
            #else:
            #    listvalues += "('" + df[3][row] + "', '" + df[4][row] + "', '" + df[1][row] + "', '" + df[5][row] + "')"
    #executecmd(listvalues)
#print listvalues
except:
    pass
#股票選擇權
listvalues = ""
try:
    df = pandas.read_html(StockOption)[1]
    for row in df.index:
        if row > 0:
            #print "('" + df[3][row] + "', '" + df[4][row] + "', '" + df[1][row] + "', '" + df[5][row] + "')"
            if len(listvalues) > 0:
                listvalues += ", " + "('" + df[3][row] + "', '" + df[4][row] + "', '" + df[1][row] + "', '" + df[5][row] + "')"
            else:
                listvalues += "('" + df[3][row] + "', '" + df[4][row] + "', '" + df[1][row] + "', '" + df[5][row] + "')"
    #executecmd(listvalues)
#print listvalues
except:
    pass
conn.commit()
conn.close()
