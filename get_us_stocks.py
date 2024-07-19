# -*- coding: utf8 -*-
import urllib2
import json
import codecs
import sys
import datetime
from datetime import date

#Output File
strfile = 'C:\\AuroraQuantitative\\DataImportOutput\\usstks.csv'


#"Symbol"(0),
#"Name"(1),
#"LastSale"(2),
#"MarketCap"(3),
#"IPOyear"(4),
#"Sector"(5),
#"industry"(6),
#"Summary Quote"(7),
#"PIH",
#"1347 Property Insurance Holdings, Inc.",
#"7.85",
#"$46.76M",
#"2014",
#"Finance",
#"Property-Casualty Insurers",
#"http://www.nasdaq.com/symbol/pih",

class StkEntry:
    def __init__(self):
        self.name = ''
        self.symbol = ''
        self.lastSale = ''

stkMap = {}


def makeStkMap(strExch):
    url = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=' + strExch + '&render=download'
    content = urllib2.urlopen(url).read().decode('utf-8')
    stks = content.split('\n')
    for stk in stks:        
        tokens = stk.split(',')
        if len(tokens) <= 2:
            continue
        stkObj = StkEntry()
        stkObj.symbol = tokens[0].strip().replace('"', '')
        stkObj.name = tokens[1].strip().replace('"', '')
        stkMap[stkObj.symbol] = stkObj
    pass

makeStkMap('nasdaq')
makeStkMap('nyse')
makeStkMap('amex')

retList = []
for idval, stk in stkMap.iteritems():
    strCode = stk.symbol
    strName = stk.name
    stkID = strCode
    stkName = strName
    cpFlag = ''
    secID = stkID
    cmdCode = stkID + '.US'
    cmdExchange = 'US'
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
    cmdSession = 'USStk'
    cmdCalendar = 'US'
    cmdSettlementID = ''
    cmdCurrency = 'USD'
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
