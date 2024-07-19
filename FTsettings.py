# -*- coding: UTF-8 -*-
import sys
import datetime
import sqlite3
from datetime import date
import time
import requests
from bs4 import BeautifulSoup
sys.path.append('D:\AuroraQuantitative\Scripts\TradingLibrary')
#Settings
#------------------
#庫存檔日期設定：True為當日, False為非當日
TodayFile = False
#------------------
#轉出的資料筆數低於這個數值時，log上會出error訊息!!
warningThreshold = 1
transdesc = ""
#庫存檔TestLan is EXCEL file, Production is csv file
inFile = 'D:\\RTS\\ftpStock\\DBBI03P.csv'
JFncoInFile  = 'D:\\RTS\\ftpJihsun\\FUHNCO.txt'
JFcomInFile  = 'D:\\RTS\\ftpJihsun\\FUMCOM.txt'
FFHMATFile = 'D:\\RTS\\ftpFuOp\\FUTMAT'
DDSCbackupFile = 'D:\\AuroraQuantitative\\DB\\old\\{0}\\DBBI03P.csv'.format(date.today().strftime("%Y%m%d"))
#商品檔zip
CommodityInfoFile = 'D:\AuroraQuantitative\RamenFiles\Data\CommodityInfo.zip'
#檢查庫存日期時，超過N天會出Warning
daysToBeCheck = 0
#交易資料庫的位置
dbFile = "D:\\AuroraQuantitative\\DB\\dataservice.db3"
jfFile = "D:\\AuroraQuantitative\\DB\\FUHNCO.txt"
conFile = "D:\\AuroraQuantitative\\DB\\FUMCOM.txt"
#輸出log檔的位置
logFile = "D:\\AuroraQuantitative\\DB\\FTtransfer.log"
#庫存來源
DDSC = "DDSC"
JF = "JF"
SYSCOM = "SYCOM"
#交易員代碼範圍設定 沒有指定則給''
begin = 710 #代碼起始值
end = 719 #代碼結束值

traderhead = list('{:03d}'.format(i) for i in range(begin,end+1))

#SQL server setting
host = '192.168.0.101'
user = 'FTSIuser'
password = '1234'
database = 'TestDB'
port = '1433'
table = 'dbo.DCENK'

#新增codemap處理股票期貨的代碼

CodeMap = {"FITX":"TXF",
"FIMTX":"MXF",
"FIMTX1":"MX1",
"FIMTX2":"MX2",
"FIMTX4":"MX4",
"FIMTX5":"MX5",
"FITE":"EXF",
"FITF":"FXF",
"FIXI":"XIF",
"FIGT":"GTF",
"FIT5":"T5F",
"FII5":"IFF",
"FTGD":"GDF",
"FIBR":"BRF",
"FICP":"CPF",
"FIGB":"GBF",
"FIRH":"RHF",
"FIRT":"RTF",
"FISP":"SPF",
"FITG":"TGF",
"FITJ":"TJF",
"FIUD":"UDF",
"FIUN":"UNF",
"FIXA":"XAF",
"FIXB":"XBF",
"FIXE":"XEF",
"FIXJ":"XJF",
"FIG2":"G2F",
"FIE4":"E4F",
"FIBT":"BTF",}
url = "http://www.yuantafutures.com.tw/TradeInfo/marginlistSTKF.aspx"
url_get = requests.get(url)
url_get.encoding = 'utf-8'
#print(url_get.text)
soup = BeautifulSoup(url_get.text, 'html.parser')
#print(soup)
soup_table = soup.find(id='dg0')
for td in soup_table.find_all('td'):
    if td.get_text()[:2] == "FI":
        #print(td.get_text())
        codekey = td.get_text().strip().encode('utf-8')
        if codekey in CodeMap:
            pass
        else:
            CodeMap[codekey] = codekey[2:]

