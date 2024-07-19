import urllib2
import bs4
import codecs
import sys

#Output File
strfile = 'C:\\AuroraQuantitative\\DataImportOutput\\hketfs.csv'

retList = []
#https://www.hkex.com.hk/chi/market/sec_tradinfo/stockcode/eisdreit_c.htm

def getHKData(url, cmdType):
    content = urllib2.urlopen(url).read()
    content = bs4.BeautifulSoup(content, "html.parser", from_encoding='GB18030')
    table = content.find('table')
    table = table.find('table')
    tables = table.findAll('table')
    trs = tables[1].findAll('tr')
    iRow = 1
    for tr in trs:
        tds = tr.findAll('td')
        stkID = tds[0].getText().strip()
        if len(stkID) >= 5 and stkID[0] == '0':
            stkID = stkID[1:]
        if iRow == 1:
            iRow = 2
            continue
        stkName = tds[1].getText().strip()
        roundLots = tds[2].getText().strip().replace(',', '')
        #strOut = 'HKEX,' + stkID + '.HKEX,' + stkName + ',HKSTK,HKD,' + roundLots + ',Stock,'
        cpFlag = ''
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
    return None

#"https://www.hkex.com.hk/chi/market/sec_tradinfo/stockcode/eisdreit_c.htm"
#"https://www.hkex.com.hk/chi/market/sec_tradinfo/stockcode/eisdetf_pf_c.htm"

if __name__ == "__main__":
    retList = []
    getHKData("https://www.hkex.com.hk/chi/market/sec_tradinfo/stockcode/eisdreit_c.htm","DepositReceipt")
    iLen = len(retList)
    if iLen <= 0:
        sys.exit(1)
    getHKData("https://www.hkex.com.hk/chi/market/sec_tradinfo/stockcode/eisdetf_pf_c.htm","ETF")
    iLen2 = len(retList)
    if iLen2 <= iLen:
        sys.exit(1) 
    if len(retList) > 0:
        fo = codecs.open(strfile, 'wb', 'utf-8')
        fo.write(str(len(retList)))
        fo.write('\r\n')
        for strOut in retList:
            fo.write(strOut)
            fo.write('\r\n')
        fo.close()
        sys.exit(0)
