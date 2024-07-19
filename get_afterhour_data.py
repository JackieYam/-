# -*- coding: utf-8 -*-
import requests
import pandas
import sqlite3
import datetime
from datetime import *

#---------------------------------------------------------------------------------------------------------------------------
dbFile= "C:\\AuroraQuantitative\\DB\\dataservice.db3"
#http://www.taifex.com.tw/chinese/3/3_1_1.asp?qtype=2&market_code=1&goday=&dateaddcnt=0&DATA_DATE_Y=2018&DATA_DATE_M=3&DATA_DATE_D=23&syear=2018&smonth=3&sday=23&commodity_id=
IndexFutureURL = "http://www.taifex.com.tw/chinese/3/3_1_1.asp?qtype=2&market_code=1&goday=&dateaddcnt=0"
IndexOptionURL = "http://www.taifex.com.tw/chinese/3/3_2_2.asp?qtype=2&market_code=1&goday=&dateaddcnt=0"
IndexF = ["TX", "MTX"]
IndexO = ["TXO"]
FutIDMap = {'TX':'TXF', 'MTX':'MXF'}
#----------------------------------------------------------------------------------------------------------------------------
def getFutYMCode(intMonth):
    mth = intMonth % 100
    year = int(intMonth / 100)
    year = year % 10
    if mth == 1:
        return ("A" + str(year))
    if mth == 2:
        return ("B" + str(year))
    if mth == 3:
        return ("C" + str(year))
    if mth == 4:
        return ("D" + str(year))
    if mth == 5:
        return ("E" + str(year))
    if mth == 6:
        return ("F" + str(year))
    if mth == 7:
        return ("G" + str(year))
    if mth == 8:
        return ("H" + str(year))
    if mth == 9:
        return ("I" + str(year))
    if mth == 10:
        return ("J" + str(year))
    if mth == 11:
        return ("K" + str(year))
    if mth == 12:
        return ("L" + str(year))
    return ("?" + str(year))

def getOptYMCode(bCP, intMonth):
    mth = intMonth % 100
    year = int(intMonth / 100)
    year = year % 10
    if mth == 1:
        if bCP:
            return ("A" + str(year))
        else:
            return ("M" + str(year))
    if mth == 2:
        if bCP:
            return ("B" + str(year))
        else:
            return ("N" + str(year))
    if mth == 3:
        if bCP:
            return ("C" + str(year))
        else:
            return ("O" + str(year))
    if mth == 4:
        if bCP:
            return ("D" + str(year))
        else:
            return ("P" + str(year))
    if mth == 5:
        if bCP:
            return ("E" + str(year))
        else:
            return ("Q" + str(year))
    if mth == 6:
        if bCP:
            return ("F" + str(year))
        else:
            return ("R" + str(year))
    if mth == 7:
        if bCP:
            return ("G" + str(year))
        else:
            return ("S" + str(year))
    if mth == 8:
        if bCP:
            return ("H" + str(year))
        else:
            return ("T" + str(year))
    if mth == 9:
        if bCP:
            return ("I" + str(year))
        else:
            return ("U" + str(year))
    if mth == 10:
        if bCP:
            return ("J" + str(year))
        else:
            return ("V" + str(year))
    if mth == 11:
        if bCP:
            return ("K" + str(year))
        else:
            return ("W" + str(year))
    if mth == 12:
        if bCP:
            return ("L" + str(year))
        else:
            return ("X" + str(year))
    return ("?" + str(year))
    

def toTAIFEXFutCode(cmdID, month):
    idx = month.find('W')
    if idx >= 0:
        #週小台
        week = month[(idx+1):(idx+2)]
        nmonth = month[0:idx]
        return ('MX' + str(week) + getFutYMCode(int(nmonth)) + '.TAIFEX')
    else:
        if cmdID in FutIDMap:
            cmdID = FutIDMap[cmdID]
        return (cmdID + getFutYMCode(int(month)) + '.TAIFEX')

def toTAIFEXOptCode(cmdID, month, strike, cp):
    idx = month.find('W')
    strx = strike.zfill(5)
    bCP = True
    if cp == 'Put':
        bCP = False
    if idx >= 0:
        #週選
        week = month[(idx+1):(idx+2)]
        nmonth = month[0:idx]
        return ('TX' + str(week) + strx + getOptYMCode(bCP, int(nmonth)) + '.TAIFEX')         
    else:
        return (cmdID + strx + getOptYMCode(bCP, int(month)) + '.TAIFEX')  
#----------------------------------------------------------------------------------------------------------------------------
dtToday = date.today()

print dtToday.year, dtToday.month, dtToday.day


strData = ""

for futID in IndexF:
    ##&DATA_DATE_Y=2018&DATA_DATE_M=3&DATA_DATE_D=23&syear=2018&smonth=3&sday=23&commodity_id=
    strURL = IndexFutureURL + "&DATA_DATE_Y=" + str(dtToday.year) + "&DATA_DATE_M=" + str(dtToday.month) + "&DATA_DATE_D=" + str(dtToday.day) + "&syear=" + str(dtToday.year) + "&smonth=" + str(dtToday.month) + "&sday=" + str(dtToday.day) + "&commodity_id=" + futID
    df = pandas.read_html(strURL)[4]
    for row in df.index:
        if row == 0:
            print df[0][row], df[1][row], df[5][row]
            continue
        if type(df[0][row]) == float:
            continue        
        strCmdID = df[0][row].decode().strip()
        strMonth = df[1][row].decode().strip()
        strPrice = df[5][row].decode().strip()
        if strPrice.find('-') >= 0:
            continue
        strCmdCode = toTAIFEXFutCode(strCmdID, strMonth)
        #print strCmdID, strMonth, strPrice, strCmdCode
        if len(strData) > 0:
            strData = strData + ','
        strData = strData + (strCmdCode + "=" + strPrice)

for optID in IndexO:
    strURL = IndexOptionURL + "&DATA_DATE_Y=" + str(dtToday.year) + "&DATA_DATE_M=" + str(dtToday.month) + "&DATA_DATE_D=" + str(dtToday.day) + "&syear=" + str(dtToday.year) + "&smonth=" + str(dtToday.month) + "&sday=" + str(dtToday.day) + "&commodity_id=" + optID
    df = pandas.read_html(strURL)[2]
    for row in df.index:        
        try:
            if row == 0:
                print df[0][row], df[1][row], df[2][row], df[3][row], df[5][row]
                continue
            if type(df[0][row]) == float:
                continue
            strCmdID = df[0][row]
            if strCmdID.find('*') == 0:
                continue
            strPrice = df[5][row]
            if strPrice.find('-') >= 0:
                continue
            strCmdID = strCmdID.decode().strip()
            strPrice = strPrice.decode().strip()
            strMonth = df[1][row].decode().strip()
            strStrike = df[2][row].decode().strip()
            strCP = df[3][row].decode().strip()
            strCmdCode = toTAIFEXOptCode(strCmdID, strMonth, strStrike, strCP)
            #print strCmdID, strMonth, strStrike, strCP, strCmdCode
            if len(strData) > 0:
                strData = strData + ','
            strData = strData + (strCmdCode + "=" + strPrice)
        except:
            pass
            
conn = sqlite3.connect(dbFile)
cursor = conn.cursor()
strSQL = ("Replace Into key_value_storage(space,[key],[value],last_change, changed_by) "
        + "Values('PSC','AHPrices','" + strData + "','" + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        + "','PY')")
cursor.execute(strSQL)
conn.commit()
conn.close()
