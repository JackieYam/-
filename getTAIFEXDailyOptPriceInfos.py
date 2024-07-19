# -*- coding: utf-8 -*-
import sys
import urllib
import urllib2
import mysql.connector
import pathsetting
from pathsetting import *
import datetime
from datetime import datetime


def getContractID(strType, strMonth):
    if strType == 'TXO':
        if strMonth.endswith('W1'):
            return 'TX1'
        elif strMonth.endswith('W2'):
            return 'TX2'
        elif strMonth.endswith('W4'):
            return 'TX4'
        elif strMonth.endswith('W5'):
            return 'TX5'
        return 'TXO'
    return strType

def convertPrice(strPri):
    if strPri == '-':
        return '0'
    return strPri

def getCallPutFlag(strCP):
    if strCP == u'買權':
        return 'Call'
    if strCP == u'賣權':
        return 'Put'
    return strCP

def executeCommands(listCmds):
    strCommand = ("INSERT INTO `historicaldb`.`taifex_daily_option_price_info`(`DataDate`,`ContractID`,`ContractMonth`,"
                  + "`Strike`,`CallPut`,`Open`,`High`,`Low`,`Close`,`TotalVolume`,`SettlePrice`,`OpenInterests`,`LastBid`,`LastAsk`) VALUES ")
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
    #down_type: 1
    #commodity_id: TXO
    #commodity_id2: 
    #queryStartDate: 2020/06/03
    #queryEndDate: 2020/06/17
    url= 'https://www.taifex.com.tw/cht/3/dlOptDataDown'
    queryData = {'down_type':'1', 'commodity_id':'TXO', 'commodity_id2':'', 'queryStartDate':'2020/06/01', 'queryEndDate':'2020/06/30'}
    postdata = urllib.urlencode(queryData)
    request =  urllib2.Request(url, postdata)
    response = urllib2.urlopen(request)
    print 'request'
    data = response.read().decode('big5')
    lines = data.split('\n')
    for lineData in lines:
        tokens = lineData.split(',')
        if tokens[0] == u'交易日期':
            print('表頭略過')
        elif len(tokens) < 18:
            continue
        else:
            #print(lineData)
            #交易日期,契約,到期月份(週別),履約價,買賣權,開盤價,最高價,最低價,收盤價,成交量,結算價,未沖銷契約數,最後最佳買價,最後最佳賣價,歷史最高價,歷史最低價,是否因訊息面暫停交易,交易時段
            strDate = tokens[0].replace('/', '-')
            strContract = tokens[1]
            strMonth = tokens[2].strip()
            if strMonth.find('/') >= 0:
                continue
            strContract = getContractID(strContract, strMonth)
            strMonth = strMonth.replace('W1', '').replace('W2','').replace('W4','').replace('W5','')
            #交易日期(0),契約(1),到期月份(週別)(2),履約價(3),買賣權(4),開盤價(5),最高價(6),最低價(7),收盤價(8),成交量(9),結算價(10),
            #未沖銷契約數(11),最後最佳買價(12),最後最佳賣價(13),歷史最高價(14),歷史最低價(15),是否因訊息面暫停交易(16),交易時段(17)
            strSession = tokens[17].strip()
            if strSession != u'一般':
                continue
            strStrike = tokens[3].strip()
            strCP = getCallPutFlag(tokens[4].strip())
            strOpen = convertPrice(tokens[5].strip())
            strHigh = convertPrice(tokens[6].strip())
            strLow = convertPrice(tokens[7].strip())
            strClose = convertPrice(tokens[8].strip())
            strVolume = convertPrice(tokens[9].strip())
            strSettle = convertPrice(tokens[10].strip())
            strOI = tokens[11].strip()
            strLastBid = convertPrice(tokens[12].strip())
            strLastAsk = convertPrice(tokens[13].strip())
            strNow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #(`DataDate`,`ContractID`,`ContractMonth`,`Strike`,`CallPut`,`Open`,`High`,`Low`,`Close`,`TotalVolume`,`SettlePrice`,`OpenInterests`,`LastBid`,`LastAsk`) 
            strQuery = ("('" + strDate + "','" +  strContract + "'," + strMonth + ",'" + strStrike + "','" + strCP + "'," + strOpen + "," +  strHigh + "," + strLow + "," + strClose + "," + strVolume + "," + strSettle
                        + "," + strOI + "," + strLastBid + "," + strLastAsk + ")")
            if len(listQueries) > 0:
                strQuery = ',' + strQuery
            listQueries.append(strQuery)
            if len(listQueries) >= 64:
                executeCommands(listQueries)
                listQueries = []
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
    
