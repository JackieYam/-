# -*- coding: utf8 -*-
import urllib2
import bs4
import json
import codecs
import sys
import datetime
from datetime import date

class StockEntry:
    def __init__(self):
        self.stockID = ''
        self.stockName = ''
        self.market = ''
        self.lastPrice = 0.0
    pass
pass


#Output File
strfile = 'C:\\AuroraQuantitative\\DataImportOutput\\jpstks.csv'

urlBase = 'http://www.morningstar.co.jp/StockInfo/sec/list?code=1000&code_detail=&sort=0&order=0&page='

Stocks = []

for idx in range(0,1000):
    print(('Page=' + str(idx)))
    url = urlBase + str(idx)
    content = urllib2.urlopen(url).read().decode('cp932')
    soup = bs4.BeautifulSoup(content, "html.parser")
    tables = soup.find_all('table')
    tbl = tables[0]
    trs = tbl.find_all('tr')
    intCount = 0
    for rowIdx in range(1, len(trs)):
        intCount = intCount + 1
        """
        <tr>
        <td class="tac"><a href="/StockInfo/info/snap/1385">1385</a></td>
        <td class="tac"><a href="/StockInfo/info/snap/1385">ユーロ圏５０</a></td>
        <td class="tac">東証２部</td>
        <td class="right w70">03/13　14:11</td>
        <td class="right w70">3,490</td>
        <td class="right w70">-305</td>
        <td class="right w70">-8.04%</td>
        <td class="right">37</td>
        <td class="right">128,700</td>
        </tr>
        """
        tr = trs[rowIdx]
        tds = tr.find_all('td')
        stkEntry = StockEntry()
        stkEntry.stockID = tds[0].text.strip()
        stkEntry.stockName = tds[1].text.strip()
        stkEntry.market = tds[2].text.strip()
        stkEntry.lastPrice = float(tds[4].text.strip().replace(',', ''))
        Stocks.append(stkEntry)
    pass
    if intCount <= 0:
        break
    pass


iCounter = 0
listQueries = []

retList = []
for stk in Stocks:
    strCode = stk.stockID
    strName = stk.stockName
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
    cmdExtra = stk.market
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
pass
