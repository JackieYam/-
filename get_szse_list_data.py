# -*- coding: utf-8 -*-
""" Python : Get SSE Classfication Data
"""
import urllib2
import json
import six
import bs4
import codecs
 
#Output File
strfile = 'C:\\AuroraQuantitative\\DataImportOutput\\szsestks.csv'

strURLBase = "http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1110&TABKEY=tab1&PAGENO="

szseStks = []

for pageNo in range(1,200):
    print(pageNo)
    strURL = strURLBase + str(pageNo)
    request = urllib2.Request(strURL)
    useragent = "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
    request.add_header('User-Agent', useragent)
    response = urllib2.urlopen(request)
    data = response.read().decode('utf-8')
    jsonData = json.loads(data)
    iCount = 0
    for obj in jsonData[0]['data']:
        stkData = []
        stkData.append(obj['agdm'])
        strName = obj['agjc']
        ipos1 = strName.find('<u>')
        ipos2 = strName.find('</u>')
        #print strName, ipos1, ipos2
        strStripName = strName[(ipos1+3):ipos2].strip()
        #print strStripName
        stkData.append(strStripName)
        szseStks.append(stkData)
        iCount = iCount + 1
    pass
    if iCount <= 0:
        break
pass



"""
szseStks = ([u"000001",u"平安银行"],
[u"000002",u"万  科Ａ"],
[u"000004",u"国农科技"],
[u"000005",u"世纪星源"],
[u"000792",u"盐湖股份"],
[u"000793",u"华闻传媒"],
[u"000795",u"英洛华"],
[u"000796",u"凯撒旅游"],
[u"000797",u"中国武夷"],
[u"000798",u"中水渔业"],
[u"000799",u"酒鬼酒"],
[u"000800",u"一汽轿车"],
[u"000801",u"四川九洲"],
[u"000802",u"北京文化"],
[u"000803",u"金宇车城"],
[u"300581",u"晨曦航空"],
[u"300582",u"英飞特"],
[u"300585",u"奥联电子"],
)
"""
retList = []

for company in szseStks:
    stkID = company[0]
    stkName = company[1]
    cpFlag = ''
    secID = stkID
    cmdCode = stkID + '.SZSE'
    cmdExchange = 'SZSE'
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
    cmdSession = 'SSEStk'
    cmdCalendar = 'CN'
    cmdSettlementID = ''
    cmdCurrency = 'CNY'
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
"""
url = 'http://www.szse.cn/main/marketdata/jypz/etflb/'
content = urllib2.urlopen('http://www.szse.cn/main/marketdata/jypz/etflb/').read()
#content = bs4.BeautifulSoup(content)
content = bs4.BeautifulSoup(content, "html.parser", from_encoding='GB18030')
#div = content.find('div')
#divs = div.findAll('div')
#div = divs[10]
tbls = content.body.findAll('table')
tbl = tbls[17]
trs = tbl.findAll('tr')
strETFTail = ',ETF,0.0,0,0,,0,0,9999-12-31,9999-12-31,DV10,0,,,,,,,1,100,SSEStk,CN,,CNY,,,0.0,0.0,0.0,1,1'
idx = 0
for tr in trs:
    if idx == 0:
        idx = 1
        continue
    tds = tr.findAll('td')
    if len(tds) <= 2:
        continue
    stkID = tds[1].getText()
    stkName = tds[2].getText()
    cpFlag = ''
    cmdCode = stkID + '.SZSE'
    cmdExchange = 'SZSE'
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
    cmdTickType = 'DV10'
    cmdIsCombo = '0'
    cmdLeg1Code = ''
    cmdLeg2Code = ''
    cmdLeg1BBS = '1'
    cmdLeg2BBS = '0'
    cmdLeg1SBS = '0'
    cmdLeg2SBS = '1'
    cmdFactor = '1'
    cmdRoundLot = '100'   
    cmdSession = 'SSEStk'
    cmdCalendar = 'CN'
    cmdSettlementID = ''
    cmdCurrency = 'CNY'
    cmdTag = ''
    cmdExtra = ''
    cmdRefPri = '0.0'
    cmdUpLimit = '0.0'
    cmdDnLimit = '0.0'
    cmdTradable = '1'
    cmdHasQuote = '1'
    cmdType = 'ETF'
    strOut = (cmdCode + ',' + cmdExchange + ',' + cmdExchangeCode + ',' + cmdName + ',' + cmdNameEng + ',' + cmdType + ',' + cmdStrike + ',' + cmdMonth + ','
              + cmdWeek + ',' + cmdContract + ',' + cmdActivitySeries + ',' + cmdSequenceSeries + ',' + cmdLastTrade + ',' + cmdSettle + ',' + cmdTickType + ','
              + cmdIsCombo + ',' + cmdLeg1Code + ',' + cmdLeg2Code + ',' + cmdLeg1BBS + ',' + cmdLeg2BBS + ',' + cmdLeg1SBS + ',' + cmdLeg2SBS + ','
              + cmdFactor + ',' + cmdRoundLot + ',' + cmdSession + ',' + cmdCalendar + ',' + cmdSettlementID + ',' + cmdCurrency + ',' + cmdTag + ',' + cmdExtra + ','
              + cmdRefPri + ',' + cmdUpLimit + ',' + cmdDnLimit + ',' + cmdTradable + ',' + cmdHasQuote)
    retList.append(strOut)
"""
    
if len(retList) > 0:
    fo = codecs.open(strfile, 'wb', 'utf-8')
    fo.write(str(len(retList)))
    fo.write('\r\n')
    for strOut in retList:
        fo.write(strOut)
        fo.write('\r\n')
    fo.close()
