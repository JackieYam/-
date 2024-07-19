# -*- coding: utf8 -*-
import urllib2
import json
import codecs
import sys
import datetime
from datetime import date

#Output File
strfile = 'C:\\AuroraQuantitative\\DataImportOutput\\indiastks.csv'

#00 Symbol,
#01 Series,
#02 cc,
#03 Security Name,
#04 Band,Remarks
#01 BLUECHIP,
#02 BE,
#03 BLUECHIPBE,
#04 Blue Chip India Limited,2,GSM - Stage I

retList = []

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

url = 'https://www.nseindia.com/content/equities/sec_list.csv'
req = urllib2.Request(url, headers=hdr)
content = urllib2.urlopen(req).read().decode('utf-8')
stks = content.split('\n')
for stk in stks:        
    tokens = stk.split(',')
    if len(tokens) <= 2:
            continue
    strCode = tokens[0].strip()
    strName = tokens[3].strip()
    stkID = strCode
    stkName = strName
    cpFlag = ''
    secID = stkID
    cmdCode = stkID + '.NSE'
    cmdExchange = 'NSE'
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
    cmdSession = 'INStk'
    cmdCalendar = 'IN'
    cmdSettlementID = ''
    cmdCurrency = 'INR'
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
