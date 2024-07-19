# -*- coding: utf-8 -*-

""" Python: Get Cathay ETF Fund Assets
"""
import urllib2
import json
import six
import bs4
import codecs
import sys
import datetime
from datetime import date
import shutil
import sinopacutils
from sinopacutils import *
import pathsetting
from pathsetting import *
import dsutilities

urlPCF = "http://sitc.sinopac.com/SitcAPI/api.ashx?kind=PCF&etfcode="
urlPCD = "http://sitc.sinopac.com/SitcAPI/api.ashx?kind=PCD&etfcode="
urlRealTimeNAV = "http://sitc.sinopac.com/SitcAPI/api.ashx?kind=RtNAV&etfcode="

urlPCFTest = "http://211.76.157.52/SitcAPI/api.ashx?kind=PCF&etfcode="
urlPCDTest = "http://211.76.157.52/SitcAPI/api.ashx?kind=PCD&etfcode="

####################################################################################
#PCF: (虛擬)
#{
#  "FundCode": "006204",
#  "bonds": [
#      {
#      "baldate": "2021-03-26",
#      "bonds_id": "US01609WAU62",
#      "bonds_name": "BABA 4 12/06/37",
#      "face_value": "3397000.0000",
#      "amt": "105478984.0000",
#      "shareholding": "1.2719",
#      "Cur": "USD",
#      "ex_rate": "28.6080000000",
#      "per_amt": "0"
#    }],
#  "stock": [
#    {
#      "baldate": "2021-03-26",
#      "stock_id": "1101",
#      "stock_name": "台泥",
#      "quantity": "12830.0000",
#      "amt": "592105.0000",
#      "shareholding": "0.3600",
#      "Cur": "NTD",
#      "ex_rate": "",
#      "per_amt": "0"
#    },
#    .....
#  ],
#  "futures": [
#    {
#      "baldate": "2021-03-26",
#      "futures_id": "TX",
#      "futures_name": "台指期貨",
#      "contruct_date": "202104",
#      "quantity": "6",
#      "amt": "19542000.000000",
#      "shareholding": "11.9700",
#      "Cur": "NTD",
#      "ex_rate": "",
#      "per_amt": "0",
#      "price": "16285.000000"
#    }
#  ],
#  "cashdata": [
#    {
#      "baldate": "2021-03-26",
#      "item_name": "保證金(NTD)",
#      "amt": "2659766",
#      "ex_rate": "1.0000000000"
#    },
#    {
#      "baldate": "2021-03-26",
#      "item_name": "現金(NTD)",
#      "amt": "14847271",
#      "ex_rate": "1.0000000000"
#    },
#    {
#      "baldate": "2021-03-26",
#      "item_name": "現金(USD)",
#      "amt": "156440477",
#      "ex_rate": "28.6080000000"
#    },
#  ],
#  "navdata": [
#    {
#      "nav_date": "2021-03-26",
#      "nav": "81.630000",
#      "issued_units": "2000000.000000",
#      "fund_size": "163252208.000000"
#    }
#  ]
#}
#    
#PCD:
#{
#  "FundCode": "006204",
#  "pcfdata": [
#    {
#      "AnnouncesData": "20210329",
#      "SumNav": "163252208.000000",
#      "ReleaseNumberUnits": "2000000.000000",
#      "DifferenceNumber": "0",
#      "UnitWorth": "81.630000",
#      "FundamentalUnit": "500000",
#      "MarketValue": "40813052",
#      "BasketValue": "44944000",
#      "BasketValue_P": "40858865",
#      "Diff_BasketValue": "-3398135",
#      "EstimatedReleaseUnit": "0.00"
#    }
#  ]
#}
#################################################################

# 因為沒有債券商品，先不抓債券相關的
fundEntries = [('006204',u'永豐臺灣加權ETF基金', u'TWSE.TWSE', u'1'),
               ('00858',u'永豐美國大型500股票ETF基金', u'', u'1'),
               ('00886',u'永豐美國科技ETF基金', u'', u'1'),
               ('00887',u'永豐中國科技50大ETF基金', u'', u'1'),               
               ('00888',u'永豐台灣ESG永續優質ETF基金', u'', u'1'),
               #('00836B',u'永豐10年期以上美元A級公司債券ETF基金', u'', u'1'),
               #('00838B',u'永豐7至10年期中國政策性金融債券ETF基金', u'', u'1'),
               #('00856B',u'永豐1至3年期美國公債ETF基金', u'', u'1'),
               #('00857B',u'永豐20年期以上美國公債ETF基金', u'', u'1'),
    ]


todayStr = date.today().strftime("%Y%m%d")
basketEntries = []
unknownCodes = []

if True:
    for fundEntry in fundEntries:
        #fundEntry = fundEntries[7]
            
        currDict = {}
        #PCF
        
        url = urlPCF + fundEntry[0]
        #url = urlPCF + fundEntry[0]
        etfUnderlying = fundEntry[2]
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        data = response.read().decode('utf-8')
        jsonData = json.loads(data)
        fundStkCode = jsonData[u'FundCode']
        if u'pcfdata' in jsonData:        
            assets = jsonData[u'pcfdata']
            #{"FundCode":"006204","pcfdata":[{"AnnouncesData":"20210329","SumNav":"163252208.000000","ReleaseNumberUnits":"2000000.000000",
            #"DifferenceNumber":"0","UnitWorth":"81.630000","FundamentalUnit":"500000","MarketValue":"40813052","BasketValue":"44944000",
            #"BasketValue_P":"40858865","Diff_BasketValue":"-3398135","EstimatedReleaseUnit":"0.00"}]}
            #print assets[0]
            print len(assets)
            if len(assets) == 0:
                continue
            fundStkName = fundEntry[1]
            fundmv = float(assets[0][u'SumNav'])
            fundTotalUnit = float(assets[0][u'ReleaseNumberUnits'])
            fundNAV = float(assets[0][u'UnitWorth'])
            converTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #Output Data
            strTagBegin = (u'\t<ETFDetail ID="' + fundEntry[0].decode('utf-8') + u'-' + fundEntry[1] + u'" DataTime="' + converTime +  u'" Description="' + fundEntry[1] + u'(' + todayStr.decode('utf-8') + u')" BasketLastMarketValue="'
                       + str(fundmv).decode('utf-8') +  u'" BaseCurrency="TWD" BasketLastNAV="' + str(fundNAV).decode('utf-8') + '" Units="'
                           + str(int(fundTotalUnit)).decode('utf-8') + u'" Multiplier="' + fundEntry[3].decode('utf-8') + u'" Code="' + fundEntry[0].decode('utf-8') + u'.TWSE" BaseCommodity="' + etfUnderlying + u'">\r\n')
            basketEntries.append(strTagBegin)
        pass
        
        #PCD
        url = urlPCD + fundEntry[0]
        #url = urlPCD + fundEntry[0]
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        data = response.read().decode('utf-8')
        jsonData = json.loads(data)
        
        #PCD-bonds
        # 20210331 志明希望把這家投信的bond忽略
        '''
        if u"bonds" in jsonData:
            bonds = jsonData[u"bonds"]
            for bond in bonds:
                #bond = bonds[0]
                code = bond[u"bonds_id"]
                name = bond[u"bonds_name"]
                amt = float(bond[u'amt'])
                ratio = float(bond[u'shareholding']) / 100.0
                strCode = getStockCode(code)
                if strCode == '':
                    unknownCodes.append((code + '-' + name))
                strEntry = u'\t\t<BasketEntry Code="' + strCode + '" AseetValue="' + str(amt).decode('utf-8') + '" Weight="' + str(ratio).decode('utf-8') + '" Comment=""/>\r\n'
                basketEntries.append(strEntry)
            pass
        pass
        '''
        
        #PCD-sotck
        if u"stock" in jsonData:
            stocks = jsonData[u"stock"]
            for stock in stocks:
                #stock = stocks[0]
                code = stock[u"stock_id"]
                name = stock[u"stock_name"]
                quantity = float(stock[u'quantity'])
                ratio = float(stock[u'shareholding']) / 100.0
                amount = float(stock[u'amt'])
                price = amount / quantity
                strCode = getStockCode(code)
                if(stock[u"ex_rate"] != ""):
                    currID = stock[u"Cur"]
                    currEx = float(stock[u"ex_rate"])
                    currDict[currID] = currRate
                pass
                if strCode == '':
                    unknownCodes.append((code + '-' + name))
                iquantity = int(quantity)
                strEntry = u'\t\t<BasketEntry Code="' + strCode + '" Shares="' + str(iquantity).decode('utf-8') + '" RefPrice="' + str(price) + '" Weight="' + str(ratio).decode('utf-8') + '" Comment=""/>\r\n'
                basketEntries.append(strEntry)
            pass
        pass
        
        #PCD-futures
        if u"futures" in jsonData:
            futures = jsonData[u"futures"]
            for future in futures:
                #future = futures[0]
                code = future[u"futures_id"]
                name = future[u"futures_name"]
                quantity = float(future[u'quantity'])
                ratio = float(future[u'shareholding']) / 100.0
                amount = float(future[u'amt'])
                futYM = future[u'contruct_date']
                price = float(future[u'price'])
                if(stock[u"ex_rate"] != ""):
                    currID = stock[u"Cur"]
                    currEx = float(stock[u"ex_rate"])
                    currDict[currID] = currRate
                pass
                strCode = getFuturesCode(code, futYM)
                iquantity = int(quantity)
                strEntry = u'\t\t<BasketEntry Code="' + strCode + '" Shares="' + str(iquantity).decode('utf-8') + '" RefPrice="' + str(price) + '" Weight="' + str(ratio).decode('utf-8') + '" Comment=""/>\r\n'
                basketEntries.append(strEntry)
            pass
        pass
        
        #PCD-cashdata (永豐的匯率是對新台幣的)
        if u"cashdata" in jsonData:
            cashdatas = jsonData[u"cashdata"]
            for cashdata in cashdatas:
                currID = cashdata[u"item_name"]
                if(currID.find(u"現金") < 0):
                    continue
                currID = currID.replace(u"現金(", u"")
                currID = currID.replace(u")", u"")
                currRate = float(cashdata[u"ex_rate"])
                currDict[currID] = currRate
            pass
        pass
            
        if(u"USD" in currDict.keys()):
            for key in currDict:
                if key == u"NTD":
                    strEntry = u'\t\t<ExchangeRate CurrencyID="TWD" Rate="' + str(currDict[u'USD']) + u'"/>\r\n'
                elif key == u"USD":
                    strEntry = u'\t\t<ExchangeRate CurrencyID="USD" Rate="1"/>\r\n'
                else:
                    strEntry = u'\t\t<ExchangeRate CurrencyID="' + key + u'" Rate="' + str(currDict[key]/currDict[u'USD']) + u'"/>\r\n'
                pass
                basketEntries.append(strEntry)
            pass
        pass
    
    
        if u"cashdata" in jsonData:
            cashdatas = jsonData[u"cashdata"]
            for cashdata in cashdatas:
                currID = cashdata[u"item_name"]
                if(currID.find(u"現金") < 0):
                    continue
                currID = currID.replace(u"現金(", u"")
                currID = currID.replace(u")", u"")
                currAmt = float(cashdata[u"amt"])
                if(currID not in currDict.keys()):
                    continue
                print currDict[currID]
                if currID == u"NTD":
                    strEntry = u'\t\t<CurrencyWeight CurrencyID="' + "TWD" + u'" AseetValue="' + str(currAmt).decode('utf-8') + u'" Weight="' + 'Null' + u'"/>\r\n'
                else:
                    try:
                        strEntry = u'\t\t<CurrencyWeight CurrencyID="' + currID + u'" AseetValue="' + str(currAmt).decode('utf-8') + u'" Weight="' + 'Null' + u'"/>\r\n'
                    except:#沒有TWD
                        pass
                    basketEntries.append(strEntry)
            
        strTagEnd = u'\t</ETFDetail>\r\n'
        basketEntries.append(strTagEnd)
        #bonds = assets[u'repo_bonds_array']

    fo = codecs.open(sinopac_etf_details, 'wb', 'utf-8')
    for strOut in basketEntries:
        fo.write(strOut)
    fo.close()
    #dsutilities.writeStatusToDB("抓永豐ETF資料","產生永豐ETF檔(get_sinopac_etfs_details.py)", "OK")
    ####except:
    x = str(sys.exc_info()[0])
    #dsutilities.writeStatusToDB("抓永豐ETF資料","產生永豐ETF檔(get_sinopac_etfs_details.py)",("Error:" + x.replace('\'','\'\'')))    
sys.exit(0)



