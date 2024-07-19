# -*- coding: cp950 -*-
import os
import sys
import math
import urllib2
import json
import codecs

strOutFile = r"C:\AuroraQuantitative\DataImportOutput\binanceCmds.txt"
#strOutFile = r"C:\Temp\bianceCmds.txt"

sys.path.append(r"C:\AuroraQuantitative\Scripts\TradingLibrary")
#sys.path.append(r"C:\Projects\capitalpipe\Python\PyLiteTrading")

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

def getTickIDFromTickValue(fTickValue):
    if fTickValue == 0.1:
        return 'DV1000'
    if fTickValue == 0.01:
        return 'DV100'
    if fTickValue == 0.001:
        return 'DV10'
    if fTickValue == 0.0001:
        return 'DV1'
    if fTickValue == 0.00001:
        return 'DP05'
    if fTickValue == 0.000001:
        return 'DP06'
    if fTickValue == 0.0000001:
        return 'DP07'
    if fTickValue == 0.00000001:
        return 'DP08'
    if fTickValue == 0.000000001:
        return 'DP09'
    if fTickValue == 0.0000000001:
        return 'DP10'
    print 'Unknown Tick', fTickValue
    return 'INT'

def getMinimumQuantity(iDigit):
    return math.pow(10.0, (-1*iDigit))


def getTickIDFromTickValue(fTickValue):
    if fTickValue == 0.1:
        return 'DV1000'
    if fTickValue == 0.01:
        return 'DV100'
    if fTickValue == 0.001:
        return 'DV10'
    if fTickValue == 0.0001:
        return 'DV1'
    if fTickValue == 0.00001:
        return 'DP05'
    if fTickValue == 0.000001:
        return 'DP06'
    if fTickValue == 0.0000001:
        return 'DP07'
    if fTickValue == 0.00000001:
        return 'DP08'
    if fTickValue == 0.000000001:
        return 'DP09'
    if fTickValue == 0.0000000001:
        return 'DP10'
    print 'Unknown Tick', fTickValue
    return 'INT'

def getStandadCoinID(strID):
    '''
    取得標準化的貨幣代碼
    '''
    if strID == 'BCC':
        return 'BCH'
    if strID == 'YOYO':
        return 'YOYOW'
    if strID == 'BQX':
        return 'ETHOS'
    if strID == 'IOTA':
        return 'MIOTA'
    return strID

"""
    {
        "symbol":"ETHBTC",
        "status":"TRADING",
        "baseAsset":"ETH",
        "baseAssetPrecision":8,
        "quoteAsset":"BTC",
        "quotePrecision":8,
        "orderTypes":["LIMIT","LIMIT_MAKER","MARKET","STOP_LOSS_LIMIT","TAKE_PROFIT_LIMIT"],
        "icebergAllowed":true,
        "filters":[
            {"filterType":"PRICE_FILTER","minPrice":"0.00000000","maxPrice":"0.00000000","tickSize":"0.00000100"},
            {"filterType":"PERCENT_PRICE","multiplierUp":"10","multiplierDown":"0.1","avgPriceMins":5},
            {"filterType":"LOT_SIZE","minQty":"0.00100000","maxQty":"100000.00000000","stepSize":"0.00100000"},
            {"filterType":"MIN_NOTIONAL","minNotional":"0.00100000","applyToMarket":true,"avgPriceMins":5},
            {"filterType":"ICEBERG_PARTS","limit":10},{"filterType":"MAX_NUM_ALGO_ORDERS","maxNumAlgoOrders":5}]
    },
    {
        "symbol":"LTCBTC",
        "status":"TRADING",
        "baseAsset":"LTC",
        "baseAssetPrecision":8,
        "quoteAsset":"BTC",
        "quotePrecision":8,
        "orderTypes":["LIMIT","LIMIT_MAKER","MARKET","STOP_LOSS_LIMIT","TAKE_PROFIT_LIMIT"],"icebergAllowed":true,
        "filters":[
            {"filterType":"PRICE_FILTER","minPrice":"0.00000000","maxPrice":"0.00000000","tickSize":"0.00000100"},
            {"filterType":"PERCENT_PRICE","multiplierUp":"10","multiplierDown":"0.1","avgPriceMins":5},
            {"filterType":"LOT_SIZE","minQty":"0.01000000","maxQty":"100000.00000000","stepSize":"0.01000000"},
            {"filterType":"MIN_NOTIONAL","minNotional":"0.00100000","applyToMarket":true,"avgPriceMins":5},
            {"filterType":"ICEBERG_PARTS","limit":10},{"filterType":"MAX_NUM_ALGO_ORDERS","maxNumAlgoOrders":5}]
    }
"""


#try:
if True:
    allCommodities = {}
    url = "https://api.binance.com/api/v1/exchangeInfo"
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    response = opener.open(url)
    data = response.read().decode("utf-8-sig")
    #data = urllib2.urlopen(url).read()
    jsonData = json.loads(data)
    print "parse ok!!"
    symbols = jsonData["symbols"]
    #幣安的symbol先暫定為BIANCE
    for cmdObj in symbols:
        strSymbol = cmdObj['symbol']
        strBaseCurr = getStandadCoinID(cmdObj['baseAsset'])
        strQuoteCurr = getStandadCoinID(cmdObj['quoteAsset'])
        strBaseCurrName = getChineseName(strBaseCurr)
        strBaseCurrName = '[' + strBaseCurrName + ']'                
        strQuoteCurrName = getChineseName(strQuoteCurr)
        strQuoteCurrName = '[' + strQuoteCurrName + ']'
        baseCoinData = DefaultCoinDataManager.getCoinData(strBaseCurr)
        quoteCoinData = DefaultCoinDataManager.getCoinData(strQuoteCurr)
        if baseCoinData is None or quoteCoinData is None:
            if cmdObj['status'] != 'BREAK':
                print strSymbol, strBaseCurr, strQuoteCurr, cmdObj['status'], 'Error'
            pass
            continue
        pass
        strPriDigit = cmdObj['quotePrecision']
        filters = cmdObj['filters']
        minQty = 0.001
        tickSize = 0.001
        for filterObj in filters:
            if filterObj['filterType'] == 'LOT_SIZE':
                minQty = float(filterObj['minQty'])
            if filterObj['filterType'] == 'PRICE_FILTER':
                tickSize = float(filterObj['tickSize'])
            pass
        pass
        strCode = strBaseCurr.upper() + '/' + strQuoteCurr.upper() + '.BINANCE'
        cmdName = strBaseCurrName + '兌' + strQuoteCurrName  + '[幣安]'
        rtsCmd = CommodityInfo()
        rtsCmd.Code = strCode
        rtsCmd.ExchangeCode = strSymbol
        rtsCmd.Name = cmdName
        rtsCmd.NameEnglish = cmdName
        rtsCmd.CmdType = CommodityType.CrossRate
        rtsCmd.ContractID = ''
        rtsCmd.Exchange = 'BINANCE'
        rtsCmd.Strike = 0.0
        rtsCmd.Month = 0
        rtsCmd.WeekSequence = 0
        rtsCmd.SeriesOrderedByActivity = 0
        rtsCmd.SeriesOrderedBySequence = 0
        rtsCmd.LastTrade = '2999-12-31'
        rtsCmd.SettleDate = '2999-12-31'
        rtsCmd.TickType = getTickIDFromTickValue(tickSize)            #Tick代碼
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
        rtsCmd.MinimumOrderQuantityAsDouble = minQty #最小委託量
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
