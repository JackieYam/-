# -*- coding: utf-8 -*-
import requests
import sys
sys.path.append(r"C:\AuroraQuantitative\Scripts")
import dsutilities

#注意:使用元富的檔案時要注意不含換行字元(轉檔時要用T30LINEMODE參數)

try:
    #元富的URL url = 'http://210.59.202.15/download/T30V.TSE'
    url = 'https://clear.twse.com.tw/index/datafile/T30'
    r = requests.post(url, allow_redirects=True)
    dataContent = r.content
    # 作格式檢查，T30每筆應該要有100byte
    rCount = len(dataContent) / 100
    if rCount <= 1000:
        dsutilities.writeStatusToDB("抓證交所T30","下載證交所T30(T30.TSE)(get_t30files.py)",("Error: 資料筆數過少,僅有{0}筆".format(rCount)))        
    else:
        dsutilities.writeStatusToDB("抓證交所T30","下載證交所T30(T30.TSE)(get_t30files.py)", "OK")
        open(r'C:\AuroraQuantitative\ForeignDataConverter\T30.TSE', 'wb').write(r.content)
        open(r'C:\AuroraQuantitative\TWCmdTrasfer\T30.TSE', 'wb').write(r.content)
    pass
except:
    x = str(sys.exc_info()[1])
    dsutilities.writeStatusToDB("抓證交所T30","下載證交所T30(T30.TSE)(get_t30files.py)",("Error: " + x))
pass


try:
    #元富的URL url = 'http://210.59.202.15/download/T32.TSE'
    url = 'https://clear.twse.com.tw/index/datafile/T32'
    r = requests.post(url, allow_redirects=True)
    dataContent = r.content
    tmp = dataContent
    # 作格式檢查，T32每筆應該要有50byte
    i = 0
    if(i > 0):
        dsutilities.writeStatusToDB("抓證交所T32","下載證交所T32(T32.TSE)(get_t30files.py)",("Error: 有{0}筆不符合電文長度".format(i)))
    else:
        dsutilities.writeStatusToDB("抓證交所T32","下載證交所T32(T32.TSE)(get_t30files.py)", "OK")
        open(r'C:\AuroraQuantitative\ForeignDataConverter\T32.TSE', 'wb').write(r.content)
        open(r'C:\AuroraQuantitative\TWCmdTrasfer\T32.TSE', 'wb').write(r.content)
    pass
except:
    x = str(sys.exc_info()[1])
    dsutilities.writeStatusToDB("抓證交所T32","下載證交所T32(T32.TSE)(get_t30files.py)",("Error: " + x))
pass

try:
    #元富的URL url = 'http://210.59.202.15/download/T30V.OTC' #'https://dsp.tpex.org.tw/storage/mops/home/java/t30.dat'
    url = 'https://dsp.tpex.org.tw/storage/mops/home/java/t30.dat'
    r = requests.get(url, allow_redirects=True)
    dataContent = r.content
    # 作格式檢查，T30每筆應該要有100byte
    i = 0
    rCount = len(dataContent) / 100
    if rCount <= 1000:
        dsutilities.writeStatusToDB("抓櫃買中心T30","下載櫃買中心T30(T30.OTC)(get_t30files.py)",("Error: 資料筆數過少,僅有{0}筆".format(rCount)))        
    else:
        dsutilities.writeStatusToDB("抓櫃買中心T30","下載櫃買中心T30(T30.OTC)(get_t30files.py)", "OK")
        open(r'C:\AuroraQuantitative\ForeignDataConverter\T30.OTC', 'wb').write(r.content)
        open(r'C:\AuroraQuantitative\TWCmdTrasfer\T30.OTC', 'wb').write(r.content)
    pass
except:
    x = str(sys.exc_info()[1])
    dsutilities.writeStatusToDB("抓櫃買中心T30","下載櫃買中心T30(T30.OTC)(get_t30files.py)",("Error: " + x))
pass
