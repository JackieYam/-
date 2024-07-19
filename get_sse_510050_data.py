# -*- coding: utf-8 -*-
""" Python : Get SSE Classfication Data
"""
import urllib2
import json
import six
import bs4
import codecs
#Output File
strfile = 'C:\\AuroraQuantitative\\DataImportOutput\\etfopts.csv'

#Codes
url = 'http://query.sse.com.cn/commonQuery.do?jsonCallBack=jsonpCallback99714&isPagination=true&expireDate=&securityId=&sqlId=SSE_ZQPZ_YSP_GGQQZSXT_XXPL_DRHY_SEARCH_L&pageHelp.pageSize=10000&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1482310667695'
refererurl = 'http://www.sse.com.cn/assortment/options/disclo/preinfo/'
request = urllib2.Request(url)
useragent = "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
request.add_header('Referer', refererurl)
request.add_header('User-Agent', useragent)
response = urllib2.urlopen(request)
data = response.read().decode('utf-8')
data = data.replace("jsonpCallback99714(","")
data = data[:-1]
jsonData = json.loads(data)
wrts = jsonData['result']
outputlist = []
for wrt in wrts:
    stkID = wrt['CONTRACT_ID']
    stkName = wrt['CONTRACT_SYMBOL']
    cpFlag = wrt['CALL_OR_PUT'].strip()
    secID = wrt['SECURITY_ID'].strip()
    if cpFlag == u'认购':
        cmdType = 'Call'
    elif cpFlag == u'认沽':
        cmdType = 'Put'
    else:
        cmdType = 'Unknown'
        print cpFlag
    cmdCode = stkID + '.SSE'
    cmdExchange = "SSE"
    cmdExchangeCode = secID
    #print stkID, stkID[11], stkID[12]
    cmdName = stkName
    cmdNameEng = stkName
    #cmdType
    cmdStrike = wrt['EXERCISE_PRICE'].strip()
    cmdMonth = wrt['END_DATE'][:-2]
    cmdWeek = "0"
    cmdContract = wrt['SECURITYNAMEBYID'][-7:-1]
    if stkID[11] != 'M':
        cmdContract = cmdContract + stkID[11]
    cmdActivitySeries = "0"
    cmdSequenceSeries = "0"
    tmpDate = wrt['EXPIRE_DATE']
    cmdLastTrade = tmpDate[:4] + '-' + tmpDate[4:6] + '-' + tmpDate[6:8]
    cmdSettle = cmdLastTrade
    cmdTickType = 'SSE_OPT'
    cmdIsCombo = '0'
    cmdLeg1Code = ''
    cmdLeg2Code = ''
    cmdLeg1BBS = '1'
    cmdLeg2BBS = '0'
    cmdLeg1SBS = '0'
    cmdLeg2SBS = '1'
    cmdFactor = wrt['CONTRACT_UNIT']
    cmdRoundLot = wrt['ROUND_LOT']    
    cmdSession = 'SSEStk'
    cmdCalendar = 'CN'
    cmdSettlementID = 'SSE_ETF'
    cmdCurrency = 'CNY'
    cmdTag = ''
    cmdExtra = ''
    cmdRefPri = wrt['SETTL_PRICE']
    cmdUpLimit = wrt['DAILY_PRICE_UPLIMIT']
    cmdDnLimit = wrt['DAILY_PRICE_DOWNLIMIT']
    cmdTradable = '1'
    cmdHasQuote = '1'
    strOut = (cmdCode + ',' + cmdExchange + ',' + cmdExchangeCode + ',' + cmdName + ',' + cmdNameEng + ',' + cmdType + ',' + cmdStrike + ',' + cmdMonth + ','
              + cmdWeek + ',' + cmdContract + ',' + cmdActivitySeries + ',' + cmdSequenceSeries + ',' + cmdLastTrade + ',' + cmdSettle + ',' + cmdTickType + ','
              + cmdIsCombo + ',' + cmdLeg1Code + ',' + cmdLeg2Code + ',' + cmdLeg1BBS + ',' + cmdLeg2BBS + ',' + cmdLeg1SBS + ',' + cmdLeg2SBS + ','
              + cmdFactor + ',' + cmdRoundLot + ',' + cmdSession + ',' + cmdCalendar + ',' + cmdSettlementID + ',' + cmdCurrency + ',' + cmdTag + ',' + cmdExtra + ','
              + cmdRefPri + ',' + cmdUpLimit + ',' + cmdDnLimit + ',' + cmdTradable + ',' + cmdHasQuote)
    outputlist.append(strOut)

if len(outputlist) > 0:
    fo = codecs.open(strfile, 'wb', 'utf-8')
    fo.write(str(len(outputlist)))
    fo.write('\r\n')
    for strOut in outputlist:
        fo.write(strOut)
        fo.write('\r\n')
    fo.close()

