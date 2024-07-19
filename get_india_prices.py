# -*- coding: utf8 -*-
import urllib2
import json
import sys
import zipfile
import datetime
from datetime import date
import mysql.connector

conn = mysql.connector.connect(user='root', password='1234', host='quantfellow.synology.me', database='historicaldb')
cur = conn.cursor()

def executeCommands(listCmds):
    strCommand = "Replace Into daily_snapshots(code,open,high,low,close,volume,nextreference,datadate) Values"
    for strCmd in listQueries:
        strCommand = strCommand + strCmd
    cur.execute(strCommand)
    conn.commit()

strTmpZipFile = 'C:\\AuroraQuantitative\\DataImportOutput\\india.zip'

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


todayObj = date.today()

strQDate = 'qdate=105%2F10%2F07'
#strQDate = 'qdate=' + str(todayObj.year - 1911) + '%2F' + ("%02d" % todayObj.month) + '%2F' + ("%02d" % todayObj.day)
strDataDate = str(todayObj.year) + '-' + ("%02d" % todayObj.month) + '-' + ("%02d" % todayObj.day)

def GetMonthStr(intMth):
    if intMth == 1:
        return "JAN"
    if intMth == 2:
        return "FEB"
    if intMth == 3:
        return "MAR"
    if intMth == 4:
        return "APR"
    if intMth == 5:
        return "MAY"
    if intMth == 6:
        return "JUN"
    if intMth == 7:
        return "JUL"
    if intMth == 8:
        return "AUG"
    if intMth == 9:
        return "SEP"
    if intMth == 10:
        return "OCT"
    if intMth == 11:
        return "NOV"
    if intMth == 12:
        return "DEC"
    return ""


#https://www.nseindia.com/content/historical/EQUITIES/2017/APR/cm03APR2017bhav.csv.zip

mthStr = GetMonthStr(todayObj.month)
url = 'https://www.nseindia.com/content/historical/EQUITIES/' + str(todayObj.year) + '/' + mthStr + '/cm' + ("%02d" % (todayObj.day - 1)) + mthStr + str(todayObj.year) + 'bhav.csv.zip'
print url
req = urllib2.Request(url, headers=hdr)
content = urllib2.urlopen(req)
fzip = open(strTmpZipFile, 'wb')
fzip.write(content.read())
fzip.close()

#01 SYMBOL,
#02 SERIES,
#03 OPEN,
#04 HIGH,
#05 LOW,
#06 CLOSE,
#07 LAST,
#08 PREVCLOSE,
#09 TOTTRDQTY,
#10 TOTTRDVAL,
#11 TIMESTAMP,
#12 TOTALTRADES,
#13 ISIN,
#20MICRONS,EQ,35.2,38,34.75,37.65,37.95,35,153831,5695928.1,03-APR-2017,748,INE144J01027,
#3IINFOTECH,EQ,5.05,5.15,5,5.05,5.05,5.05,1438199,7283382,03-APR-2017,429,INE748C01020,
#3MINDIA,EQ,11760,11989.5,11602.2,11930.95,11945,11567.55,2067,24376135.15,03-APR-2017,669,INE470A0101

iCounter = 0
listQueries = []

zf = zipfile.ZipFile(strTmpZipFile, 'r')
for strFile in zf.namelist():
    ff = zf.read(strFile)
    lines = ff.split('\n')
    for strline in lines:
        iCounter = iCounter + 1
        if iCounter < 2:
            continue
        tokens = strline.split(',')
        if len(tokens) <= 12:
            continue
        strCode = tokens[0].strip()
        strVolume = tokens[9].strip()
        strOpen = tokens[3].strip()
        strHigh = tokens[4].strip()
        strLow = tokens[5].strip()
        strClose = tokens[6].strip()           
        strQuery = ("('" + strCode + ".NSE'," +  strOpen + "," + strHigh + "," + strLow + "," + strClose + ","
                + strVolume + "," + strClose + ",'" + strDataDate + "')")
        if len(listQueries) > 0:
            strQuery = ',' + strQuery
        listQueries.append(strQuery)
        if len(listQueries) >= 64:
            executeCommands(listQueries)
            listQueries = []
            print 'data updated .......'
if len(listQueries) > 0:
    executeCommands(listQueries)
    listQueries = []
        
conn.close()
