# -*- coding: utf8 -*-
import urllib2
import json
import codecs
import sys
import datetime
from datetime import date

#Output File
strfile = 'C:\\AuroraQuantitative\\DataImportOutput\\jpstks.csv'

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
retList = []
for tr in jsonData["japan-all-stock-prices"]:
    strCode = tr[0].strip()
    strName = tr[1].strip()
    strVolume = tr[12].strip()
    strOpen = tr[9].strip()
    strHigh = tr[10].strip()
    strLow = tr[11].strip()
    strClose = tr[5].strip()
    if strVolume == '-':
        strVolume = "0" 
    stkID = strCode
    stkName = strName
    cpFlag = ''
    secID = stkID
    cmdCode = stkID + '.JPX'
    cmdExchange = 'JPX'
    cmdExchangeCode = secID
    cmdName = stkName
    cmdNameEng = stkName
    cmdStrike = '0.0'
    cmdMonth = '0'
    cmdWeek = '0'
    cmdContract = ''
    cmdActivitySeries = "0"
    cmdSequenceSeries = "0"
    cmdLastTrade = '9999-12-31'
    cmdSettle = cmdLastTrade
    cmdTickType = 'DV100'
    cmdIsCombo = '0'
    cmdLeg1Code = ''
    cmdLeg2Code = ''
    cmdLeg1BBS = '1'
    cmdLeg2BBS = '0'
    cmdLeg1SBS = '0'
    cmdLeg2SBS = '1'
    cmdFactor = '1'
    cmdRoundLot = '100'   
    cmdSession = 'JPStk'
    cmdCalendar = 'JP'
    cmdSettlementID = ''
    cmdCurrency = 'JPY'
    cmdTag = ''
    cmdExtra = ''
    cmdRefPri = '0.0'
    cmdUpLimit = '0.0'
    cmdDnLimit = '0.0'
    cmdTradable = '1'
    cmdHasQuote = '1'
    cmdType = 'Stock'
    strOut = (cmdCode + ',' + cmdExchange + ',' + cmdExchangeCode + ',' + cmdName + ',' + cmdNameEng + ',' + cmdType + ',' + cmdStrike + ',' + cmdMonth + ','
              + cmdWeek + ',' + cmdContract + ',' + cmdActivitySeries + ',' + cmdSequenceSeries + ',' + cmdLastTrade + ',' + cmdSettle + ',' + cmdTickType + ','
              + cmdIsCombo + ',' + cmdLeg1Code + ',' + cmdLeg2Code + ',' + cmdLeg1BBS + ',' + cmdLeg2BBS + ',' + cmdLeg1SBS + ',' + cmdLeg2SBS + ','
              + cmdFactor + ',' + cmdRoundLot + ',' + cmdSession + ',' + cmdCalendar + ',' + cmdSettlementID + ',' + cmdCurrency + ',' + cmdTag + ',' + cmdExtra + ','
              + cmdRefPri + ',' + cmdUpLimit + ',' + cmdDnLimit + ',' + cmdTradable + ',' + cmdHasQuote)
    retList.append(strOut)
        
if len(retList) > 0:
    fo = codecs.open(strfile, 'wb', 'utf-8')
    fo.write(str(len(retList)))
    fo.write('\r\n')
    for strOut in retList:
        fo.write(strOut)
        fo.write('\r\n')
    fo.close()
