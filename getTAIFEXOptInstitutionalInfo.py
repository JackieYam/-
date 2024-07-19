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
    if strType == u'臺指選擇權':
        return 'TXO'
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
    strCommand = ("REPLACE INTO `historicaldb`.`taifex_daily_option_major_institutional_traders`"
            + "(`DataDate`,`ContractID`,`TraderType`,`CallPutType`,`LongTradingVolume`,`LongTradingValue`,`ShortTradingVolume`,`ShortTradingValue`,`NetTradingVolume`,"
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
    #url = 'https://www.taifex.com.tw/cht/3/dlCallsAndPutsDateDown'
    #queryData = {'firstDate':'2017/06/19 00:00', 'lastDate':'2017/06/19 00:00', 'queryStartDate':'2020/06/11', 'queryEndDate':'2020/06/18', 'commodityId':'TXO'}
    #firstDate=2017%2F06%2F19+00%3A00&lastDate=2020%2F06%2F19+00%3A00&queryStartDate=2020%2F06%2F19&queryEndDate=2020%2F06%2F19&commodityId=TXF
    url= 'https://www.taifex.com.tw/cht/3/dlCallsAndPutsDateDown'
    queryData = {'firstDate':'2017/06/19 00:00', 'lastDate':'2017/06/19 00:00', 'queryStartDate':'2017/06/19', 'queryEndDate':'2020/06/19', 'commodityId':'TXO'}
    postdata = urllib.urlencode(queryData)
    request =  urllib2.Request(url, postdata)
    response = urllib2.urlopen(request)
    data = response.read().decode('big5')
    lines = data.split('\n')
    for lineData in lines:
        tokens = lineData.split(',')
        if tokens[0] == '日期':
            print(lineData)
        elif len(tokens) < 16:
            continue
        else:
            #print(lineData)
            #日期(0),商品名稱(1),身份別(2),CallPut(3),多方交易口數(4),多方交易契約金額(千元)(5),空方交易口數(6),空方交易契約金額(千元)(7),
            #多空交易口數淨額(8),多空交易契約金額淨額(千元)(9),多方未平倉口數(10),多方未平倉契約金額(千元)(11),空方未平倉口數(12),空方未平倉契約金額(千元)(13),多空未平倉口數淨額(14),多空未平倉契約金額淨額(千元)(15)
            strDate = tokens[0].replace('/', '-')
            strContract = getContractID(tokens[1].strip())
            if strContract == '':
                print('未知契約類型!!', tokens[1].strip())
                continue;
            pass
            strTraderType = getTraderType(tokens[3].strip())
            if strTraderType == '':
                print('未知法人類型!!', tokens[3].strip())
                continue
            pass
            strNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            strQuery = ("('" + strDate + "','" +  strContract + "','" + strTraderType + "','" + tokens[2] + "'," + tokens[4] + "," + tokens[5] + "," + tokens[6] + "," + tokens[7] + "," + tokens[8]
                        + "," + tokens[9] + "," + tokens[10] + "," + tokens[11] + "," + tokens[12] + "," + tokens[13] + "," + tokens[14] + "," + tokens[15] + ",'" +  strNow + "','python')")
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
    
