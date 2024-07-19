# -*- coding: cp950 -*-
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
    if len(strType) == 2:
        return (strType + 'O')
    return strType

def convertPrice(strPri):
    if strPri == '-':
        return '0'
    return strPri

def getCP(strCP):
    if strCP == '�R�v':
        return 'Call'
    elif strCP == '���v':
        return 'Put'
    return strCP

def executeCommands(listCmds):
    strCommand = ("REPLACE INTO `historicaldb`.`taifex_daily_option_large_open_interests`(`DataDate`,`ContractID`,`ContractMonth`,`CallPut`,`OIType`,"
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
    url= 'https://www.taifex.com.tw/cht/3/dlLargeTraderOptDown'
    queryData = {'queryStartDate': '2020/06/02', 'queryEndDate': '2020/06/21'}
    postdata = urllib.urlencode(queryData)
    request =  urllib2.Request(url, postdata)
    response = urllib2.urlopen(request)
    data = response.read()
    lines = data.split('\n')
    for lineData in lines:
        tokens = lineData.split(',')
        strDate = tokens[0].strip().replace('/', '-')
        if strDate.find('���') >= 0:
            print('���Y���L')
            continue
        elif len(tokens) < 10:
            continue
        else:
            #���,�ӫ~(����),�ӫ~�W��(�����W��),�R���v,������(�g�O),����H���O,�e���j����H�R��,�e���j����H���,�e�Q�j����H�R��,�e�Q�j����H���,���������R�P�����
            strContract = tokens[1].strip()
            strMonth = tokens[4].strip()
            strContract = getContractID(strContract, strMonth)
            strMonth = strMonth.replace('W4', '').replace('W5','').replace('W2','').replace('W1','')
            #���(0),�ӫ~(����)(1),�ӫ~�W��(�����W��)(2),�R���v(3),������(�g�O)(4),����H���O(5),�e���j����H�R��(6),�e���j����H���(7),
            #�e�Q�j����H�R��(8),�e�Q�j����H���(9),���������R�P�����(10)
            strTraderType = tokens[5].strip()
            strTop5BuyOI = tokens[6].strip()
            strTop5SellOI = tokens[7].strip()
            strTop10BuyOI = tokens[8].strip()
            strTop10SellOI = tokens[9].strip()
            strMarketOI = tokens[10].strip()
            strCP = getCP(tokens[3].strip())
            print(strCP)
            #(`DataDate`,`ContractID`,`ContractMonth`,`CallPut`,`OIType`,`Top5BuyOI`,`Top5SellOI`,`Top10BuyOI`,`Top10SellOI`,`TotalOI`)
            strQuery = ("('" + strDate + "','" +  strContract + "'," + strMonth + ",'" + strCP + "'," + strTraderType + "," + strTop5BuyOI + "," + strTop5SellOI + "," +  strTop10BuyOI + "," + strTop10SellOI + "," + strMarketOI + ")")
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
