# -*- coding: utf8 -*-
import urllib2
import json
import bs4
import codecs
import sys
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

todayObj = date.today()

#strQDate = 'qdate=105%2F10%2F07'
strQDate = 'qdate=' + str(todayObj.year - 1911) + '%2F' + ("%02d" % todayObj.month) + '%2F' + ("%02d" % todayObj.day)
strDataDate = unicode(datetime.datetime.now()) #str(todayObj.year) + '-' + ("%02d" % todayObj.month) + '-' + ("%02d" % todayObj.day)
print strQDate, strDataDate

url = 'https://hesonogoma.com/stocks/data/japan-all-stock-prices.json?'

content = urllib2.urlopen(url).read().decode('utf-8')
jsonData = json.loads(content)

iCounter = 0
listQueries = []
#0  ["0001",                 SC
#1  "日経225（日経平均株価）",  名称
#2  "東証",                   市場
#3  "株価指数",                業種
#4  "4/4 15:15",              日時
#5  "18810.25",                株価
#6  "-172.98",                前日比
#7  "-0.91",                  前日比(%)
#8  "18983.23",               前日終値
#9  "18933.82",               始値
#10 "18947.33",               高値
#11 "18703.63",               安値
#12 "-","-","-","-","-"],  
#00 ["1301",
#01 "極洋",
#02 "東証一部",
#03 "水産・農林",
#04 "4/4 15:00",
#05 "3010",    株価
#06 "0",
#07 "0.00",    
#08 "3010",    前日終値
#09 "3005",    始値
#10 "3020",    高値
#11 "2983",    安値
#12 "77200",   出来高
#13 "231801",  売買代金
#14 "32894",   時価総額
#15 "2310",    値幅下限
#16 "3710"],   値幅上限

for tr in jsonData["japan-all-stock-prices"]:
    strCode = tr[0].strip() + ".JPX"
    strVolume = tr[12].strip()
    strOpen = tr[9].strip()
    strHigh = tr[10].strip()
    strLow = tr[11].strip()
    strClose = tr[5].strip()
    if strVolume == '-':
        strVolume = "0"
    if strVolume == '0' or strOpen == '--':
        print "No Trade Today:", strCode, tr[1]
        continue    
    strQuery = ("('" + strCode + "'," +  strOpen + "," + strHigh + "," + strLow + "," + strClose + ","
                + strVolume + "," + strClose + ",'" + strDataDate + "')")
    #print "Data:", tds[0].getText().strip(), tds[1].getText().strip()
    #print strQuery
    if len(listQueries) > 0:
        strQuery = ',' + strQuery
    listQueries.append(strQuery)
    if len(listQueries) >= 128:
        executeCommands(listQueries)
        print 'Do Write!!'
        listQueries = []
        
if len(listQueries) > 0:
    executeCommands(listQueries)
    listQueries = []

conn.close()
