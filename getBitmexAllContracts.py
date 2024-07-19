# -*- coding: cp950 -*-
import urllib2
import json
import datetime
import dateutil.parser
import time
import mysql.connector

mydb = mysql.connector.connect( host="quantfellow.synology.me", user="root", passwd="1234")
myCursor = mydb.cursor()


class XBTContract:
    """Bitmex合約"""
    def __init__(self):
        self.symbol = ''
        self.contractID = ''
        self.settleMonth = ''
        self.instrumentType = ''        
        self.list = ''
        self.expiry = ''
        self.settle = ''
        self.quoteCurrency = ''
        self.state = ''
        self.settledPrice = ''
        self.factor = ''
        self.tickSize = ''
        pass

def getTimeStamp(dt):
    t = time.mktime((dt.year,dt.month,dt.day, 0, 0, 0, 0, 0, 0))
    return t

#https://www.bitmex.com/api/v1/instrument?count=400&reverse=false

ValidCmds = { "XBT":None, "ADA":None, "BCH":None, "EOS":None, "ETH":None, "LTC":None, "TRX":None, "XRP":None }

DataList = []
strURL = 'https://www.bitmex.com/api/v1/instrument?count=400&reverse=false'
opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
response = opener.open(strURL)
data = response.read().decode("utf-8-sig")
jsonData = json.loads(data)
for ct in jsonData:
    strType = ct['typ']
    strSymbol = ct['symbol'].strip()
    strLast = strSymbol[-2:]
    strBegin = strSymbol[0:3]
    if strLast.isnumeric() and strSymbol.find('_') < 0 and strBegin in ValidCmds:
        #print strSymbol, strType, ct['isQuanto'], ct['listing'], ct['expiry']
        ctObj = XBTContract()
        ctObj.symbol = strSymbol
        ctObj.contractID = strBegin
        ctObj.settleMonth = ct['expiry'][0:7].replace("-", "")
        ctObj.instrumentType = "Futures"
        ctObj.list = dateutil.parser.parse(ct['listing']).strftime("%Y-%m-%d %H:%M:%S")
        ctObj.expiry = dateutil.parser.parse(ct['expiry']).strftime("%Y-%m-%d %H:%M:%S")
        ctObj.settle = dateutil.parser.parse(ct['settle']).strftime("%Y-%m-%d %H:%M:%S")
        ctObj.quoteCurrency = ct['quoteCurrency']
        ctObj.state = ct['state']
        sobj = ct['settledPrice']
        if sobj == None or sobj == '':
            ctObj.settledPrice = '0'
        else:
            ctObj.settledPrice = sobj
        ctObj.factor = '1'
        ctObj.tickSize = ct['tickSize']
        DataList.append(ctObj)
        pass
    pass
DataList.sort(key=lambda x: x.list)
for ctObj in DataList:
    #print ctObj.symbol, ctObj.list, ctObj.expiry
    strSQL = "Replace into crypto_price_db.bitmex_instruments(symbol,contractid,settlemonth,instrumenttype,listing,expiry,settle,quoteCurrency,sate,settledPrice,factor,tickSize,lastupdate) Value('"
    dtNow = datetime.datetime.now()
    strNow = dtNow.strftime("%Y-%m-%d %H:%M:%S")
    strSQL = (strSQL + ctObj.symbol + "','" + ctObj.contractID + "'," + ctObj.settleMonth + ",'" + ctObj.instrumentType + "','" + ctObj.list + "','" + ctObj.expiry + "','"
              + ctObj.settle + "','" + ctObj.quoteCurrency + "','" + ctObj.state + "'," + str(ctObj.settledPrice) + ","
              + str(ctObj.factor) + "," + str(ctObj.tickSize) + ",'" + strNow + "')")   
    myCursor.execute(strSQL)
    #print strSQL
pass
mydb.commit()
mydb.close()
