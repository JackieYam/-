# -*- coding: cp950 -*-
import os
import sys
import math
import urllib2
import json
import codecs

strOutFile = r"C:\AuroraQuantitative\DataImportOutput\huobiCmds.txt"

sys.path.append(r"C:\AuroraQuantitative\Scripts\TradingLibrary")
import commoditydefs
from commoditydefs import *
import cointools
from cointools import *

'''載入加密貨幣清單資料'''
DefaultCoinDataManager.loadFromFile('C:\\AuroraQuantitative\\Scripts\\coins.txt')

def getChineseName(strCurr):
    if strCurr == 'btc' or strCurr == 'BTC':
        return '比特幣'
    if strCurr == 'eth' or strCurr == 'ETH':
        return '以太坊'
    if strCurr == 'usdt' or strCurr == 'USDT':
        return '泰達幣'    
    return strCurr.encode('utf-8').upper()

def getCurrencyID(strCurr):
    if strCurr == 'btc' or strCurr == 'BTC':
        return CurrencyID.CRYPTO_BTC
    if strCurr == 'eth' or strCurr == 'ETH':
        return CurrencyID.CRYPTO_ETH
    if strCurr == 'usdt' or strCurr == 'USDT':
        return CurrencyID.CRYPTO_USTD
    return CurrencyID.NULL  

def getTickIDFromPrecission(iDigit):
    if iDigit == 1: #0.1
        return 'DV1000'
    if iDigit == 2: #0.01
        return 'DV100'
    if iDigit == 3: #0.001
        return 'DV10'
    if iDigit == 4: #0.0001
        return 'DV1'
    if iDigit == 5: #0.00001
        return 'DP05'
    if iDigit == 6: #0.000001
        return 'DP06'
    if iDigit == 7: #0.0000001
        return 'DP07'
    if iDigit == 8: #0.00000001
        return 'DP08'
    if iDigit == 9: #0.00000001
        return 'DP09'
    if iDigit == 10: #0.00000001
        return 'DP10'
    return 'INT'

def getMinimumQuantity(iDigit):
    return math.pow(10.0, (-1*iDigit))


def getStandadCoinID(strID):
    '''
    取得標準化的貨幣代碼
    '''
    if strID == 'BCC':
        return 'BCH'
    if strID == 'VEN':
        return 'VET'
    if strID == 'YOYO':
        return 'YOYOW'
    if strID == 'CVCOIN':
        return 'CVN'
    if strID == 'PROPY':
        return 'PRO'
    if strID == 'IOTA':
        return 'MIOTA'
    return strID


#try:
if True:
    allCommodities = {}
    url = "https://api.huobipro.com/v1/common/symbols"
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    response = opener.open(url)
    data = response.read().decode("utf-8-sig")
    jsonData = json.loads(data)
    if jsonData['status'] == 'ok':
        for cmdObj in jsonData['data']:
            #{"base-currency":"btm","quote-currency":"usdt","price-precision":4,"amount-precision":2,"symbol-partition":"innovation","symbol":"btmusdt"}#
            strSymbol = cmdObj['symbol']
            strBaseCurr = cmdObj['base-currency']
            strQuoteCurr = cmdObj['quote-currency']
            strBaseUpper = getStandadCoinID(strBaseCurr.upper())
            strQuoteUpper = getStandadCoinID(strQuoteCurr.upper())
            baseCoinData = DefaultCoinDataManager.getCoinData(strBaseUpper)
            quoteCoinData = DefaultCoinDataManager.getCoinData(strQuoteUpper)
            if baseCoinData is None or quoteCoinData is None:
                print strSymbol, strBaseUpper, strQuoteUpper, 'Error'
                continue
            pass
            strBaseCurrName = getChineseName(strBaseCurr)
            strBaseCurrName = '[' + strBaseCurrName + ']'                
            strQuoteCurrName = getChineseName(strQuoteCurr)
            strQuoteCurrName = '[' + strQuoteCurrName + ']'
            strPriDigit = cmdObj['price-precision']
            strQtyDigit = cmdObj['amount-precision']
            intQtyDigit = int(strQtyDigit)
            strCode = strBaseCurr.upper() + '/' + strQuoteCurr.upper() + '.HUOBI'
            cmdName = strBaseCurrName + '兌' + strQuoteCurrName + '[火幣]'
            rtsCmd = CommodityInfo()
            rtsCmd.Code = strCode
            rtsCmd.ExchangeCode = strSymbol
            rtsCmd.Name = cmdName
            rtsCmd.NameEnglish = cmdName
            rtsCmd.CmdType = CommodityType.CrossRate
            rtsCmd.ContractID = ''
            rtsCmd.Exchange = 'HUOBI'
            rtsCmd.Strike = 0.0
            rtsCmd.Month = 0
            rtsCmd.WeekSequence = 0
            rtsCmd.SeriesOrderedByActivity = 0
            rtsCmd.SeriesOrderedBySequence = 0
            rtsCmd.LastTrade = '2999-12-31'
            rtsCmd.SettleDate = '2999-12-31'
            rtsCmd.TickType = getTickIDFromPrecission(strPriDigit)            #Tick代碼
            rtsCmd.IsCombo = False
            rtsCmd.Tradable = True
            rtsCmd.HasQuote = True
            rtsCmd.Leg1Code = baseCoinData.rtsCode
            rtsCmd.Leg2Code = quoteCoinData.rtsCode
            rtsCmd.BuyLeg1BS = True
            rtsCmd.BuyLeg2BS = True
            rtsCmd.SellLeg1BS = False
            rtsCmd.SellLeg2BS = False
            rtsCmd.Factor = 1.0
            rtsCmd.RoundLots = 1
            rtsCmd.SettlementID = 'X'
            rtsCmd.SessionID = '24H'
            rtsCmd.RefrencePrice = 0.0
            rtsCmd.UpLimit = 0.0
            rtsCmd.DownLimit = 0.0
            rtsCmd.CalendarID = 'X'
            rtsCmd.Tag = ''
            rtsCmd.ExtraInfo = ''        
            rtsCmd.Currency = getCurrencyID(strBaseCurr)
            rtsCmd.GroupFactor = 1.0
            rtsCmd.OrderVolumeLimit = 0
            rtsCmd.MarketOrderVolumeLimit = 0
            rtsCmd.Divisor = 1 #分數報價的分母
            rtsCmd.MaxDigits = strPriDigit #最大小數位數
            rtsCmd.IsDoubleQuantity = True #數量欄位是否為浮點數
            rtsCmd.MinimumOrderQuantityAsDouble = getMinimumQuantity(intQtyDigit) #最小委託量
            allCommodities[strCode] = rtsCmd
        pass
    if len(allCommodities) > 0:
        fo = codecs.open(strOutFile, 'wb', 'utf-8')
        ##fo.write(str(len(allCommodities)))
        ##fo.write('\r\n')
        for strCode, cmdObj in allCommodities.iteritems():
            strOut = cmdObj.toCSVLineData()
            fo.write(strOut)
            fo.write('\r\n')
        fo.close()
    pass
#except:
#    print sys.exc_info()[0]
#    pass
