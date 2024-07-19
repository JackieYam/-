# -*- coding: utf-8 -*-
""" Python : Get SSE Classfication Data
"""
import codecs
import datetime
import time
from time import *

#Last Trading/Settle Dates
settleDates = ([strptime("2016-03-10", "%Y-%m-%d"), strptime("2016-06-09", "%Y-%m-%d"),
                strptime("2016-09-08", "%Y-%m-%d"), strptime("2016-12-08", "%Y-%m-%d"),
                strptime("2017-03-09", "%Y-%m-%d"), strptime("2017-06-08", "%Y-%m-%d"),
                strptime("2017-09-07", "%Y-%m-%d"), strptime("2017-12-07", "%Y-%m-%d")])
#Output File
strfile = 'C:\\AuroraQuantitative\\DataImportOutput\\Topix.csv'

#January        F
#February	G
#March	        H
#April	        J
#May	        K
#June	        M
#July	        N
#August	        Q
#September	U
#October	V
#November	X
#December	Z
def getYearMonthCode(intYear, intMth):
    iY =(intYear % 10)
    if intMth == 1:
        return ("F" + str(iY))
    if intMth == 2:
        return ("G" + str(iY))
    if intMth == 3:
        return ("H" + str(iY))
    if intMth == 4:
        return ("J" + str(iY))
    if intMth == 5:
        return ("K" + str(iY))
    if intMth == 6:
        return ("M" + str(iY))
    if intMth == 7:
        return ("N" + str(iY))
    if intMth == 8:
        return ("Q" + str(iY))
    if intMth == 9:
        return ("U" + str(iY))
    if intMth == 10:
        return ("V" + str(iY))
    if intMth == 11:
        return ("X" + str(iY))
    if intMth == 12:
        return ("Z" + str(iY))
    return ("?" + str(iY))

def main():
    #Codes
    ttoday = time()
    outputlist = []
    for ts in settleDates:
        settleDt = mktime((ts.tm_year, ts.tm_mon, ts.tm_mday,0,0,0,0,0,0))
        if settleDt < ttoday:
            continue
        stkID = "TOPIX" + getYearMonthCode(ts.tm_year, ts.tm_mon)
        stkName = (u"東證指期" + strftime("%Y%m", ts))
        cpFlag = 'F'
        secID = stkID
        cmdType = 'Futures'
        cmdCode = stkID + '.OSM'
        cmdExchange = "OSM"
        cmdExchangeCode = secID
        cmdName = stkName
        cmdNameEng = stkName
        #cmdType
        cmdStrike = "0"
        cmdMonth = strftime("%Y%m", ts)
        cmdWeek = "0"
        cmdContract = "TOPIX"
        cmdActivitySeries = "0"
        cmdSequenceSeries = "0"
        cmdLastTrade = strftime("%Y-%m-%d", ts)
        cmdSettle = cmdLastTrade
        cmdTickType = 'DV5000'
        cmdIsCombo = '0'
        cmdLeg1Code = ''
        cmdLeg2Code = ''
        cmdLeg1BBS = '1'
        cmdLeg2BBS = '0'
        cmdLeg1SBS = '0'
        cmdLeg2SBS = '1'
        cmdFactor = '1'
        cmdRoundLot = '1' 
        cmdSession = 'JPX'
        cmdCalendar = 'JP'
        cmdSettlementID = 'JPX_TPX'
        cmdCurrency = 'JPY'
        cmdTag = ''
        cmdExtra = ''
        cmdRefPri = '0'
        cmdUpLimit = '0'
        cmdDnLimit = '0'
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

if __name__ == "__main__":
    main()
