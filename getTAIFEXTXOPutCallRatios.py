# -*- coding: cp950 -*-
import sys
import urllib
import urllib2
import mysql.connector
import pathsetting
from pathsetting import *
import datetime
from datetime import datetime



def executeCommands(listCmds):
    strCommand = "INSERT INTO `historicaldb`.`taifex_txo_put_call_ratios` (`DataDate`, `CallVolume`, `PutVolume`, `PutCallRatioVolume`, `CallOI`, `PutOI`, `PutCallRatioOI`) VALUES "
    for strCmd in listQueries:
        strCommand = strCommand + strCmd
    cur.execute(strCommand)
    conn.commit()
    print 'Do Write!!'

if True:
    conn = mysql.connector.connect(user=RTS_DBUser, password=RTS_DBPassword,
                               host=RTS_MySQLServer,
                               database=RTS_HistDB)
    cur = conn.cursor()
    listQueries = []
    url= 'https://www.taifex.com.tw/cht/3/pcRatioDown'
    queryData = {'down_type':'', 'queryStartDate': '2020/06/02', 'queryEndDate': '2020/06/21'}
    postdata = urllib.urlencode(queryData)
    request =  urllib2.Request(url, postdata)
    response = urllib2.urlopen(request)
    data = response.read()
    lines = data.split('\n')
    for lineData in lines:
        tokens = lineData.split(',')
        strDate = tokens[0].strip().replace('/', '-')
        if strDate.find('日期') >= 0:
            print('表頭略過')
            continue
        elif len(tokens) < 7:
            continue
        else:
            #日期(0),賣權成交量(1),買權成交量(2),買賣權成交量比率%(3),賣權未平倉量(4),買權未平倉量(5),買賣權未平倉量比率%(6)
            strDate = tokens[0].strip().replace('/', '-')
            strPutVolume = tokens[1].strip()
            strCallVolume = tokens[2].strip()
            strPutCallVolume = tokens[3].strip()
            strPutOI = tokens[4].strip()
            strCallOI = tokens[5].strip()
            strPutCallOI = tokens[6].strip()
            #(`DataDate`, `CallVolume`, `PutVolume`, `PutCallRatioVolume`, `CallOI`, `PutOI`, `PutCallRatioOI`)
            strQuery = ("('" + strDate + "'," +  strCallVolume + "," + strPutVolume + "," + strPutCallVolume + "," + strCallOI + "," + strPutOI + "," + strPutCallOI + ")")
            if len(listQueries) > 0:
                strQuery = ',' + strQuery
            listQueries.append(strQuery)
            if len(listQueries) >= 64:
                executeCommands(listQueries)
                listQueries = []
            pass
        pass
    pass
    if len(listQueries) > 0:
        executeCommands(listQueries)
        listQueries = []       
    pass
    conn.close()
"""
except mysql.connector.errors.ProgrammingError as e:
    bError = True
    print str(e)
except:
    bError = True
    x = str(sys.exc_info()[0])
    print x
pass
"""
