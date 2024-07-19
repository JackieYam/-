# -*- coding: utf-8 -*-
import urllib2 
import zipfile 
import datetime
import os
import sys
import dsutilities
import requests
import subprocess
#
def download_file():
    #檢查產生目錄
    path = "C:\\AuroraQuantitative"
    if not os.path.isdir(path):
        os.mkdir(path)
    path = "C:\\AuroraQuantitative\\TaifexData"
    if not os.path.isdir(path):
        os.mkdir(path)
    path = "C:\\AuroraQuantitative\\TaifexData\\TickData"
    if not os.path.isdir(path):
        os.mkdir(path)
    dtToGet = datetime.date.today()
    #https://www.taifex.com.tw/file/taifex/Dailydownload/Dailydownload/Daily_2021_11_15.zip
    filename = "Daily_" + dtToGet.strftime("%Y_%m_%d") + ".zip"
    print filename
    url = 'https://www.taifex.com.tw/file/taifex/Dailydownload/Dailydownload/' + filename
    r = requests.get(url)
    if len(r.content) > 512: 
        localFile = path + '\\' + filename
        open(localFile, 'wb').write(r.content)
        strDataPath = 'DATAPATH=' + localFile
        print strDataPath
        subprocess.call(['C:\\AuroraQuantitative\\TaifexData\\Tools\\TAIFEXRptConverter.exe','MODE=CONVERTTICKSFILE',strDataPath,'DBDSN=Server=127.0.0.1;Uid=rtsop;Pwd=1qaz!QAZ;Database=historicaldb;'])
    pass
pass

try:
    download_file()
    dsutilities.writeStatusToDB('維護TAIFEX歷史資料 - 抓當日每筆成交資料', '更新期貨當日每筆成交資料(downloadtickdata.py)','OK')
except:
    x = str(sys.exc_info()[0])
    dsutilities.writeStatusToDB('維護TAIFEX歷史資料 - 抓當日每筆成交資料', '更新期貨當日每筆成交資料(downloadtickdata.py)',("Error:" + x.replace('\'','\'\'')))
#
