# -*- coding: utf-8 -*-
import sys
import pathsetting
from pathsetting import *
sys.path.append(CommondityPath)
import commoditydefs
from commoditydefs import *

DefaultCommodityManager = CommodityManager()
#DefaultCommodityManager.LoadFromZipFile(r'C:\Temp\CommodityInfo.zip')
DefaultCommodityManager.LoadFromZipFile(CommodityInfoFile)


ForeignFuturesMap = {'SCN':'CN', 'SSI':'NK', 'YM':'YM', 'UB':'UB', "ES":"ES", "MES":"MES"}
ForeignFuturesExchangeMap = {'SCN':'SGX', 'SSI':'SGX', 'YM':'CBOT','UB':'CBOT', "ES":"CME", "MES":"CME"} 
def getRTSCurrencyID(currID):
    if currID == u'NTD':
        return u'TWD'
    return currID

def isTAIFEXFutures(strContract):
    if strContract in ForeignFuturesMap:
        return False
    return True

def getStockCode(strCode):
    idx = strCode.find(' CH')
    if idx != -1:
        strCode = strCode.replace('.CH','')
        tCode = strCode + '.SSE'
        cmd = DefaultCommodityManager.GetCommodity(tCode)
        if cmd == None:
            tCode = strCode + '.SZSE'
            cmd = DefaultCommodityManager.GetCommodity(tCode)
            if cmd == None:
                return ''
            return tCode
        return tCode
    idx = strCode.find(' JP')
    if idx != -1:
        strCode = strCode.replace(' JP', '.JPX')
        return strCode
    idx = strCode.find(' US')
    if idx != -1:
        strCode = strCode.replace(' US', '.US')
        return strCode
    cmd = DefaultCommodityManager.GetCommodity((strCode + '.TWSE'))
    if cmd != None:
        return (strCode + '.TWSE')
    tCode = strCode.replace('.OQ', '').replace('.N', '')
    tCode = tCode + '.US'
    cmd = DefaultCommodityManager.GetCommodity(tCode)
    if cmd != None:
        return tCode
    print strCode
    return strCode
    
def getFuturesCode(strContract, strYM):
    if isTAIFEXFutures(strContract):
        return getTAIFEXCode(strContract, strYM)
    else:
        newContract = ForeignFuturesMap[strContract]
        strExch = ForeignFuturesExchangeMap[strContract]
        return getForeignFuturesCode(newContract, strYM, strExch)

def getTAIFEXCode(strContract, strYM):
    intYM = int(strYM)
    mth = intYM % 100
    year = ((intYM / 100) % 10)
    ymCode = unichr((ord('A') + mth - 1)) + str(year).decode('utf-8') + u'.TAIFEX'
    if strContract == 'TX':
        return (u'TXF' + ymCode)
    if strContract == 'TE':
        return (u'EXF' + ymCode)
    if strContract == 'TF':
        return (u'FXF' + ymCode)
    return (strContract + ymCode)

def getForeignFuturesCode(strContract, strYM, strExch):
    intYM = int(strYM)
    mth = intYM % 100
    year = ((intYM / 100) % 100)
    mthCode = u''
    if mth == 1:
        mthCode = u'F'
    elif mth == 2:
        mthCode = u'G'
    elif mth == 3:
        mthCode = u'H'
    elif mth == 4:
        mthCode = u'J'
    elif mth == 5:
        mthCode = u'K'
    elif mth == 6:
        mthCode = u'M'
    elif mth == 7:
        mthCode = u'N'
    elif mth == 8:
        mthCode = u'Q'
    elif mth == 9:
        mthCode = u'U'
    elif mth == 10:
        mthCode = u'V'
    elif mth == 11:
        mthCode = u'X'
    elif mth == 12:
        mthCode = u'Z'    
    ymCode = mthCode + str(year).decode('utf-8') + u'.' + strExch.decode('utf-8')
    return (strContract + ymCode)




