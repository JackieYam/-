# -*- coding: utf-8 -*-
""" Python : Get SSE Classfication Data
"""
import urllib2
import json
import six
import bs4
import codecs
#Output File
strfile = 'C:\\AuroraQuantitative\\DataImportOutput\\ssestks.csv'

retList = []

url = 'http://query.sse.com.cn/commonQuery.do?jsonCallBack=jsonpCallback50621&isPagination=true&sqlId=COMMON_SSE_ZQPZ_GPLB_MCJS_SSAG_L&pageHelp.pageSize=1500'
refererurl = 'http://www.sse.com.cn/assortment/stock/list/name/'
request = urllib2.Request(url)
request.add_header('Referer', refererurl)
response = urllib2.urlopen(request)
data = response.read().decode('utf-8')
data = data.replace("jsonpCallback50621(","")
data = data[:-1]
jsonData = json.loads(data)
#print type(jsonData['pageHelp']['data'])
companies = jsonData['pageHelp']['data']
for company in companies:
    #company['FULLNAME'],
    stkID = company['PRODUCTID']
    stkName = company['PRODUCTNAME']
    cpFlag = ''
    secID = stkID
    cmdCode = stkID + '.SSE'
    cmdExchange = 'SSE'
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

#url = 'http://www.sse.com.cn/assortment/fund/list/'
#content = urllib2.urlopen('http://www.sse.com.cn/assortment/fund/list/').read()
#content = bs4.BeautifulSoup(content, from_encoding='GB18030')
#table = content.find('table')
#table = table.find('table')
#trs = table.findAll('tr')
#table = trs[1].find('table')
#tables = table.findAll('table')
#trs = tables[0].findAll('tr')
#strETFTail = ',ETF,0.0,0,0,,0,0,9999-12-31,9999-12-31,DV10,0,,,,,,,1,100,SSEStk,CN,,CNY,,,0.0,0.0,0.0,1,1'
#for tr in trs:
#    tds = tr.findAll('td')
#    if len(tds) <= 1:
#        continue
# new page (SSE ETF) is too dificult to parse, give up, for temporary, maintain it mannually.

sseETFList = ([
            (u'510010',u'治理ETF'),
            (u'510020',u'超大ETF'),
            (u'510030',u'价值ETF'),
            (u'510050',u'50ETF'),
            (u'510060',u'央企ETF'),
            (u'510070',u'民企ETF'),
            (u'510090',u'责任ETF'),
            (u'510110',u'周期ETF'),
            (u'510120',u'非周ETF'),
            (u'510130',u'中盘ETF'),
            (u'510150',u'消费ETF'),
            (u'510160',u'小康ETF'),
            (u'510170',u'商品ETF'),
            (u'510180',u'180ETF'),
            (u'510190',u'龙头ETF'),
            (u'510210',u'综指ETF'),
            (u'510220',u'中小ETF'),
            (u'510230',u'金融ETF'),
            (u'510260',u'新兴ETF'),
            (u'510270',u'国企ETF'),
            (u'510280',u'成长ETF'),
            (u'510290',u'380ETF'),
            (u'510300',u'300ETF'),
            (u'510310',u'HS300ETF'),
            (u'510330',u'华夏300'),
            (u'510360',u'广发300'),
            (u'510410',u'资源ETF'),
            (u'510420',u'180EWETF'),
            (u'510430',u'50等权'),
            (u'510440',u'500沪市'),
            (u'510450',u'180高ETF'),
            (u'510500',u'500ETF'),
            (u'510510',u'广发500'),
            (u'510520',u'诺安500'),
            (u'510560',u'国寿500'),
            (u'510580',u'ZZ500ETF'),
            (u'510610',u'能源行业'),
            (u'510620',u'材料行业'),
            (u'510630',u'消费行业'),
            (u'510650',u'金融行业'),
            (u'510660',u'医药行业'),
            (u'510680',u'万家50'),
            (u'510700',u'百强ETF'),
            (u'510710',u'上50ETF'),
            (u'510880',u'红利ETF'),
            (u'510900',u'H股ETF'),
            (u'511010',u'国债ETF'),
            (u'511210',u'企债ETF'),
            (u'511220',u'城投ETF'),
            (u'511800',u'易货币'),
            (u'511810',u'理财金H'),
            (u'511820',u'鹏华添利'),
            (u'511830',u'华泰货币'),
            (u'511860',u'博时货币'),
            (u'511880',u'银华日利'),
            (u'511890',u'景顺货币'),
            (u'511900',u'富国货币'),
            (u'511920',u'广发货币'),
            (u'511930',u'中融日盈'),
            (u'511960',u'嘉实快线'),
            (u'511980',u'现金添富'),
            (u'511990',u'华宝添益'),
            (u'512010',u'医药ETF'),
            (u'512070',u'非银ETF'),
            (u'512110',u'中证地产'),
            (u'512120',u'中证医药'),
            (u'512210',u'景顺食品'),
            (u'512220',u'景顺TMT'),
            (u'512230',u'景顺医药'),
            (u'512300',u'500医药'),
            (u'512310',u'500工业'),
            (u'512330',u'500信息'),
            (u'512340',u'500原料'),
            (u'512500',u'中证500'),
            (u'512510',u'ETF500'),
            (u'512600',u'主要消费'),
            (u'512610',u'医药卫生'),
            (u'512640',u'金融地产'),
            (u'512990',u'MSCIA股'),
            (u'513030',u'德国30'),
            (u'513100',u'纳指ETF'),
            (u'513500',u'标普500'),
            (u'513600',u'恒指ETF'),
            (u'513660',u'恒生通'),
            (u'518800',u'黄金基金'),
            (u'518880',u'黄金ETF')
            ])

for etfEntry in sseETFList:
    stkID = etfEntry[0]
    stkName = etfEntry[1]
    cpFlag = ''
    secID = stkID
    cmdCode = stkID + '.SSE'
    cmdExchange = 'SSE'
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

if len(retList) > 0:
    fo = codecs.open(strfile, 'wb', 'utf-8')
    fo.write(str(len(retList)))
    fo.write('\r\n')
    for strOut in retList:
        fo.write(strOut)
        fo.write('\r\n')
    fo.close()
