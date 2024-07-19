# -*- coding: utf-8 -*-
#https://www.taifex.com.tw/cht/3/dlFutContractsDateView?queryStartDate=2017/06/19&queryEndDate=2020/06/18&commodityid=TXF
import sys
import urllib
import urllib2
import mysql.connector
import pathsetting
from pathsetting import *
import datetime
from datetime import datetime

def getContractID(strType):
    if strType == u'臺股期貨':
        return 'TXF'
    if strType == u'小型臺指期貨':
        return 'MXF'
    return ''

def getTraderType(strType):
    if strType == u'自營商':
        return 'DEALERS'
    elif strType == u'投信':
        return 'IT'
    elif strType == u'外資及陸資':
        return 'FINI'
    return ''

def executeCommands(listCmds):
    strCommand = ("REPLACE INTO `historicaldb`.`taifex_daily_futures_major_institutional_traders`"
            + "(`DataDate`,`ContractID`,`TraderType`,`LongTradingVolume`,`LongTradingValue`,`ShortTradingVolume`,`ShortTradingValue`,`NetTradingVolume`,"
            + "`NetTradingValue`,`LongOpenIntrests`,`LongOpenIntrestsValue`,`ShortOpenIntrests`,`ShortOpenIntrestsValue`,`NetOpenIntrests`,`NetOpenIntrestsValue`,"
            + "`LastUpdate`,`ChangedBy`) VALUES")
    for strCmd in listQueries:
        strCommand = strCommand + strCmd
    cur.execute(strCommand)
    conn.commit()
    print 'Do Write!!'

try:
    conn = mysql.connector.connect(user=RTS_DBUser, password=RTS_DBPassword,
                               host=RTS_MySQLServer,
                               database=RTS_HistDB)
    cur = conn.cursor()
    listQueries = []
    #firstDate=2017%2F06%2F19+00%3A00&lastDate=2020%2F06%2F19+00%3A00&queryStartDate=2020%2F06%2F19&queryEndDate=2020%2F06%2F19&commodityId=TXF
    url= 'https://www.taifex.com.tw/cht/3/dlFutContractsDateDown'
    queryData = {'firstDate':'2017/06/19 00:00', 'lastDate':'2017/06/19 00:00', 'queryStartDate':'2017/06/19', 'queryEndDate':'2020/06/19', 'commodityId':'MXF'}
    postdata = urllib.urlencode(queryData)
    request =  urllib2.Request(url, postdata)
    response = urllib2.urlopen(request)
    data = response.read().decode('big5')
    lines = data.split('\n')
    for lineData in lines:
        tokens = lineData.split(',')
        if tokens[0] == '日期':
            print(lineData)
        elif len(tokens) < 15:
            continue
        else:
            #print(lineData)
            #日期(0),商品名稱(1),身份別(2),多方交易口數(3),多方交易契約金額(千元)(4),空方交易口數(5),空方交易契約金額(千元)(6),
            #多空交易口數淨額(7),多空交易契約金額淨額(千元)(8),多方未平倉口數(9),多方未平倉契約金額(千元)(10),空方未平倉口數(11),空方未平倉契約金額(千元)(12),多空未平倉口數淨額(13),多空未平倉契約金額淨額(千元)(14)

            strDate = tokens[0].replace('/', '-')
            strContract = getContractID(tokens[1].strip())
            if strContract == '':
                print('未知契約類型!!', tokens[1].strip())
                continue;
            pass
            strTraderType = getTraderType(tokens[2].strip())
            if strTraderType == '':
                print('未知法人類型!!', tokens[2].strip())
                continue
            pass
            strNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            strQuery = ("('" + strDate + "','" +  strContract + "','" + strTraderType + "'," + tokens[3] + "," + tokens[4] + "," + tokens[5] + "," + tokens[6] + "," + tokens[7] + "," + tokens[8]
                        + "," + tokens[9] + "," + tokens[10] + "," + tokens[11] + "," + tokens[12] + "," + tokens[13] + "," + tokens[14] + ",'" +  strNow + "','python')")
            if len(listQueries) > 0:
                strQuery = ',' + strQuery
            listQueries.append(strQuery)
            if len(listQueries) >= 32:
                executeCommands(listQueries)
                listQueries = []
            pass
        pass
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
    
