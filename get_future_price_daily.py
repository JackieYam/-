import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from datetime import date
import time
import random
import mysql.connector
import sys
conn = mysql.connector.connect(user='root', password='1234',
                               host='quantfellow.synology.me',
                               database='historicaldb')

cur = conn.cursor()

'''
    header = {'qtype':'3',
              'commodity_id':'TX',
              'commodity_id2':'',
              'market_code':'0',
              'goday':'',
              'dateaddcnt':'0',
              'DATA_DATE_Y':'2017',
              'DATA_DATE_M':'10',
              'DATA_DATE_D':'14',
              'syear':'2017',
              'smonth':'10',
              'sday':'14',
              'datestart':'2017/10/14',
              'MarketCode':'0',
              'commodity_idt':'TX',
              'commodity_id2t':'',
              'commodity_id2t2':''}
'''
def DateToStop(EndDate):
    if tradedate == EndDate:
        return True

url = "http://www.taifex.com.tw/chinese/3/3_1_1.asp"
def executeCommands(listCmds):
    strCommand = "Replace Into futures_daily_info(tradedate,contract,settlemonth,open,high,low,close,price_change,settleprice) Values"
    for strCmd in listCmds:
        strCommand = strCommand + strCmd
    cur.execute(strCommand)
    conn.commit()
listQueries = []
#strQDate = (datetime.datetime.today() - datetime.timedelta(day)).strftime('%Y/%m/%d')
#datetime.datetime.strptime('01012017', "%d%m%Y").date() + datetime.timedelta(day)

""" --- history data ----


#[td_.get_text().strip() for td_ in MyTable.findAll('tr')[5].findAll('td',{'class':'12bk'})]
for i in range(300):
    tradedate = (datetime.datetime.strptime('01012017', "%d%m%Y").date() + datetime.timedelta(i)).strftime('%Y/%m/%d')
    header = {'qtype':'3',
              'commodity_id':'TX',
              'commodity_id2':'',
              'market_code':'0',
              'goday':'',
              'dateaddcnt':'0',
              'DATA_DATE_Y':tradedate.split('/')[0],
              'DATA_DATE_M':tradedate.split('/')[1],
              'DATA_DATE_D':tradedate.split('/')[2],
              'syear':tradedate.split('/')[0],
              'smonth':tradedate.split('/')[1],
              'sday':tradedate.split('/')[2],
              'datestart':tradedate,
              'MarketCode':'0',
              'commodity_idt':'TX',
              'commodity_id2t':'',
              'commodity_id2t2':''}
    DF = requests.post(url, header)
    DF = BeautifulSoup(DF.text, 'html.parser')
    MyTable = DF.find('table', {'class':'table_f'})
    if DateToStop("2017/10/20"):
        print "End Date: {}".format(tradedate)
        break
    if MyTable == None:
        print "--- No Trade at {0}---".format(tradedate)
        #print "\n"
        continue
    #MyTable
    tradedate = DF.find('h3').get_text()[9:]
    listdata = []
    for tr in MyTable.findAll('tr'):
        tds = tr.findAll('td')
        td = [td_.get_text().strip() for td_ in tds]
        try:
            td[0]
        except:
            continue
        if td[0] == 'TX':
            contract = str(td[0])
            settlemonth = str(td[1])
            #print tr
            open_ = str(td[2])
            high_ = str(td[3])
            low_ = str(td[4])
            close_ = str(td[5])
            price_change = str(('0' if td[6] == '0' else td[6][3:]))
            settleprice = str(('0' if td[11] == '-' else td[11]))
            strQuery = ("('" + tradedate + "','" +  contract + "',"
                        + settlemonth + "," + open_ + "," + high_ + ","
                        + low_ + "," + close_ + ",'"  + price_change + "'," +
                        settleprice +")").encode('utf-8')
            if len(listQueries) > 0:
                strQuery = ',' + strQuery
            listQueries.append(strQuery)
                #break
            if len(listQueries) >= 128:
                executeCommands(listQueries)
                print 'Do Write!!'
                listQueries = []
    time.sleep(random.random())
if len(listQueries) > 0:
    print "Final write!"
    #print listQueries
    executeCommands(listQueries)
    listQueries = []
#print DF.find('h3').get_text()[9:]
#print listdata
    #data = "('" + today + "',"  
#   --- End --- """

tradedate = datetime.datetime.today().strftime('%Y/%m/%d')
header = {'qtype':'3',
          'commodity_id':'TX',
          'commodity_id2':'',
          'market_code':'0',
          'goday':'',
          'dateaddcnt':'0',
          'DATA_DATE_Y':tradedate.split('/')[0],
          'DATA_DATE_M':tradedate.split('/')[1],
          'DATA_DATE_D':tradedate.split('/')[2],
          'syear':tradedate.split('/')[0],
          'smonth':tradedate.split('/')[1],
          'sday':tradedate.split('/')[2],
          'datestart':tradedate,
          'MarketCode':'0',
          'commodity_idt':'TX',
          'commodity_id2t':'',
          'commodity_id2t2':''}
DF = requests.post(url, header)
DF = BeautifulSoup(DF.text, 'html.parser')
MyTable = DF.find('table', {'class':'table_f'})
if MyTable == None:
    print "--- No Trade at {0}---".format(tradedate)
    sys.exit()
#MyTable
tradedate = DF.find('h3').get_text()[9:]
listdata = []
for tr in MyTable.findAll('tr'):
    tds = tr.findAll('td')
    td = [td_.get_text().strip() for td_ in tds]
    try:
        td[0]
    except:
        continue
    if td[0] == 'TX':
        contract = str(td[0])
        settlemonth = str(td[1])
        #print tr
        open_ = str(td[2])
        high_ = str(td[3])
        low_ = str(td[4])
        close_ = str(td[5])
        price_change = str(('0' if td[6] == '0' else td[6][3:]))
        settleprice = str(('0' if td[11] == '-' else td[11]))
        strQuery = ("('" + tradedate + "','" +  contract + "',"
                    + settlemonth + "," + open_ + "," + high_ + ","
                    + low_ + "," + close_ + ",'"  + price_change + "'," +
                    settleprice +")").encode('utf-8')
        print strQuery
        if len(listQueries) > 0:
            strQuery = ',' + strQuery
        listQueries.append(strQuery)
            #break
    
executeCommands(listQueries)
print 'Do Write!!'


