# -*- coding: utf-8 -*-
import urllib2
import json
import codecs
import sys
import time
import datetime
from datetime import date
import mysql.connector
import pathsetting
from pathsetting import *
import dsutilities

def toGregorianDate(strDate):
    tokens = strDate.split('/')
    iYear = int(tokens[0])
    iYear = iYear + 1911
    return (str(iYear) + '-' + tokens[1] + '-' + tokens[2])

def executeCommands(listCmds):
    strCommand = "Replace Into tw_stk_ori_daily_prices(Code,BarDate,Open,High,Low,Close,Volume) Values"
    for strCmd in listQueries:
        strCommand = strCommand + strCmd
    cur.execute(strCommand)
    conn.commit()
    print 'Do Write!!'
pass

try:
    conn = mysql.connector.connect(user=RTS_DBUser, password=RTS_DBPassword,
                               host=RTS_MySQLServer,
                               database=RTS_HistDB)
    cur = conn.cursor()
    currYear = 1999
    currMonth = 1
    endMonth = 202006
    #
    iCounter = 0
    listQueries = []
    #
    while ((currYear*100) + currMonth) <= endMonth:
        strDay = str(((currYear*100) + currMonth)) + "01"
        #https://www.twse.com.tw/indicesReport/MI_5MINS_HIST?response=json&date=19990101
        url = 'https://www.twse.com.tw/indicesReport/MI_5MINS_HIST?response=json&date=' + strDay
        #
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        data = response.read().decode('utf-8')
        jsonData = json.loads(data)
        if jsonData['stat'] == 'OK':
            print(strDay, '處理資料中', len(jsonData['data']))
            for record in jsonData['data']:
                strDate = record[0]
                strOpen = record[1].replace(',', '');
                strHigh = record[2].replace(',', '');
                strLow = record[3].replace(',', '');
                strClose = record[4].replace(',', '');
                print(toGregorianDate(strDate), strOpen, strHigh, strLow, strClose)
                strQuery = ("('TWSE.TWSE','" + toGregorianDate(strDate) + "'," +  strOpen + ","
                    + strHigh + "," + strLow + "," + strClose + ",0)")
                if len(listQueries) > 0:
                    strQuery = ',' + strQuery
                listQueries.append(strQuery)
                if len(listQueries) >= 128:
                    executeCommands(listQueries)
                    listQueries = []
                pass
            pass
        else:
            print(strDay, jsonData['stat'])                
        pass
        #
        currMonth = currMonth + 1
        if currMonth == 13:
            currMonth = 1
            currYear = currYear + 1
        pass
        time.sleep(3)
    pass
    if len(listQueries) > 0:
        executeCommands(listQueries)
        listQueries = []       
    conn.close()
except mysql.connector.errors.ProgrammingError as e:
    bError = True
    print str(e)
except:
    bError = True
    x = str(sys.exc_info()[0])
    print x
pass
    
