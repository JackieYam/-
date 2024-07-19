# -*- coding: cp950 -*-
import sys
import urllib
import urllib2
import mysql.connector
import pathsetting
from pathsetting import *
import datetime
from datetime import datetime


def getContractID(strType):
    if strType == 'TX':
        return 'TXF'
    if strType == 'TE':
        return 'EXF'
    if strType == 'TF':
        return 'FXF'
    if len(strType) == 2:
        return (strType + 'F')
    return strType

def convertPrice(strPri):
    if strPri == '-':
        return '0'
    return strPri


def executeCommands(listCmds):
    strCommand = ("INSERT INTO `historicaldb`.`taifex_daily_futures_large_open_interests`(`DataDate`,`ContractID`,`ContractMonth`,`OIType`,"
                  + "`Top5BuyOI`,`Top5SellOI`,`Top10BuyOI`,`Top10SellOI`,`TotalOI`) VALUES ")
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
    url= 'https://www.taifex.com.tw/cht/3/largeTraderFutDown'
    queryData = {'queryStartDate': '2020/06/02', 'queryEndDate': '2020/06/21'}
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
        elif len(tokens) < 10:
            continue
        else:
            #日期,商品(契約),商品名稱(契約名稱),到期月份(週別),交易人類別,前五大交易人買方,前五大交易人賣方,前十大交易人買方,前十大交易人賣方,全市場未沖銷部位數
            strContract = tokens[1].strip()
            strMonth = tokens[3].strip()
            if strMonth.find('W') >= 0:
                continue
            strContract = getContractID(strContract)
            #日期(0),商品(契約)(1),商品名稱(契約名稱)(2),到期月份(週別)(3),交易人類別(4),前五大交易人買方(5),前五大交易人賣方(6),前十大交易人買方(7),前十大交易人賣方(8),全市場未沖銷部位數(9)
            strTraderType = tokens[4].strip()
            strTop5BuyOI = tokens[5].strip()
            strTop5SellOI = tokens[6].strip()
            strTop10BuyOI = tokens[7].strip()
            strTop10SellOI = tokens[8].strip()
            strMarketOI = tokens[9].strip()
            #(`DataDate`,`ContractID`,`ContractMonth`,`OIType`,`Top5BuyOI`,`Top5SellOI`,`Top10BuyOI`,`Top10SellOI`,`TotalOI`) 
            strQuery = ("('" + strDate + "','" +  strContract + "'," + strMonth + "," + strTraderType + "," + strTop5BuyOI + "," + strTop5SellOI + "," +  strTop10BuyOI + "," + strTop10SellOI + "," + strMarketOI + ")")
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
