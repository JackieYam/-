# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:20:30 2020

@author: Alvie
"""

import codecs
import requests
import xlrd

def GetHKData(workbook, cmdType, classification):
    retList = []
    worksheet = workbook.sheet_by_index(0)
    for i in range(3,worksheet.nrows):
        cols = worksheet.row(i)
        stkID = cols[0].value.strip()
        if cols[2].value.strip() != classification:
            # print stkID
            continue
        pass
        if len(stkID) >= 5 and stkID[0] == '0':
            stkID = stkID[1:]
        pass
        stkName = cols[1].value.strip()
        roundLots = cols[4].value.strip().replace(',', '')
        #strOut = 'HKEX,' + stkID + '.HKEX,' + stkName + ',HKSTK,HKD,' + roundLots + ',Stock,'
        secID = stkID
        cmdCode = stkID + '.HKEX'
        cmdExchange = 'HKEX'
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
        cmdTickType = 'HKSTK'
        cmdIsCombo = '0'
        cmdLeg1Code = ''
        cmdLeg2Code = ''
        cmdLeg1BBS = '1'
        cmdLeg2BBS = '0'
        cmdLeg1SBS = '0'
        cmdLeg2SBS = '1'
        cmdFactor = '1'
        cmdRoundLot = roundLots   
        cmdSession = 'HKSTK'
        cmdCalendar = 'HK'
        cmdSettlementID = ''
        cmdCurrency = 'HKD'
        cmdTag = ''
        cmdExtra = ''
        cmdRefPri = '0.0'
        cmdUpLimit = '0.0'
        cmdDnLimit = '0.0'
        cmdTradable = '1'
        cmdHasQuote = '1'
        strOut = (cmdCode + ',' + cmdExchange + ',' + cmdExchangeCode + ',' + cmdName + ',' + cmdNameEng + ',' + cmdType + ',' + cmdStrike + ',' + cmdMonth + ','
                  + cmdWeek + ',' + cmdContract + ',' + cmdActivitySeries + ',' + cmdSequenceSeries + ',' + cmdLastTrade + ',' + cmdSettle + ',' + cmdTickType + ','
                  + cmdIsCombo + ',' + cmdLeg1Code + ',' + cmdLeg2Code + ',' + cmdLeg1BBS + ',' + cmdLeg2BBS + ',' + cmdLeg1SBS + ',' + cmdLeg2SBS + ','
                  + cmdFactor + ',' + cmdRoundLot + ',' + cmdSession + ',' + cmdCalendar + ',' + cmdSettlementID + ',' + cmdCurrency + ',' + cmdTag + ',' + cmdExtra + ','
                  + cmdRefPri + ',' + cmdUpLimit + ',' + cmdDnLimit + ',' + cmdTradable + ',' + cmdHasQuote)
        retList.append(strOut)
    pass
    return retList

def WriteCSVFile(retList, strFile):
    if len(retList) > 0:
        fo = codecs.open(strFile, 'wb', 'utf-8')
        fo.write(str(len(retList)))
        fo.write('\r\n')
        for strOut in retList:
            fo.write(strOut)
            fo.write('\r\n')
        pass
        fo.close()
    pass


if __name__ == "__main__":
    retList = []
    url = 'https://www.hkex.com.hk/chi/services/trading/securities/securitieslists/ListOfSecurities_c.xlsx'
    urlGet = requests.get(url)
    # 先取Excel檔案
    workbook = xlrd.open_workbook(file_contents=urlGet.content, encoding_override="U-8")

    # Stock
    strFile = 'C:\\AuroraQuantitative\\DataImportOutput\\hkstks.csv'
    retList = GetHKData(workbook, 'Stock', u"股本")
    WriteCSVFile(retList, strFile)
    
    # ETF
    strFile = 'C:\\AuroraQuantitative\\DataImportOutput\\hketfs.csv'
    retList = GetHKData(workbook, 'ETF', u"交易所買賣產品")
    WriteCSVFile(retList, strFile)
