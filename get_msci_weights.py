import urllib2
import bs4
import codecs
import sys

#Output File
strfile = 'C:\\AuroraQuantitative\\DataImportOutput\\hketfs.csv'

retList = []
#https://app2.msci.com/eqb/custom_indexes/tw_performance.html

url = 'https://app2.msci.com/eqb/custom_indexes/tw_performance.html'

content = urllib2.urlopen(url).read()
content = bs4.BeautifulSoup(content, "html.parser")
tables = content.findAll('table')
tbody = tables[2].find('tbody')
trs = tbody.findAll('tr')
for tr in trs:
    tds = tr.findAll('td')
    stkName = tds[1].getText().strip()
    price = tds[2].getText().strip()
    curency = tds[3].getText().strip()
    shares = tds[4].getText().strip()
    weight = tds[5].getText().strip()
    adjFactor = tds[6].getText().strip()
    adjDescription = tds[7].getText().strip()
    fxRate = tds[8].getText().strip()
    country = tds[9].getText().strip()
    code = tds[10].getText().strip()
    print code, stkName, price, shares
"""
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
"""
