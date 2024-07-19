# -*- coding: utf-8 -*-

import requests
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os, time, sys
from os import listdir
from os.path import isfile, join, getctime
import rts_op_settings
import shutil
import dsutilities

# ---- Members
output_folder = os.getcwd() + "\\WrtFiles"
now = time.time()
expired_days = 7
listDataOut = []
underlyings = {}

const_codec = 'utf-8'


try:
    os.mkdir(output_folder)
except:
    pass

# ----

# ---- Functions
def getUnderlyingCode(undCode):
    #" IX0001 加權指數; IX0027 電子類指; IX0039 金融保險; IX0118 富櫃200指數"
    if undCode == u'IX0001':
        return 'TWSE.TWSE'
    elif undCode == u'IX0027':
        return 'TWSEELEC.TWSE'
    elif undCode == u'IX0039':
        return 'TWSEBKI.TWSE'
    elif undCode.startswith(u'TXF'):
        return (undCode + '.TAIFEX')
    elif undCode.startswith(u'HSI'):
        #恒生指數
        return ('^HSI.Index')
    return (undCode + '.TWSE')

def replaceDate(strDt):
    strDt = strDt.replace(u'103',u'2014')
    strDt = strDt.replace(u'104',u'2015')
    strDt = strDt.replace(u'105',u'2016')
    strDt = strDt.replace(u'106',u'2017')
    strDt = strDt.replace(u'107',u'2018')
    strDt = strDt.replace(u'108',u'2019')
    strDt = strDt.replace(u'109',u'2020')
    strDt = strDt.replace(u'110',u'2021')
    strDt = strDt.replace(u'111',u'2022')
    strDt = strDt.replace(u'112',u'2023')
    strDt = strDt.replace(u'113',u'2024')
    strDt = strDt.replace(u'114',u'2025')
    strDt = strDt.replace(u'115',u'2026')
    strDt = strDt.replace(u'116',u'2027')
    strDt = strDt.replace(u'117',u'2028')
    strDt = strDt.replace(u'118',u'2029')
    strDt = strDt.replace(u'119',u'2030')
    strDt = strDt.replace(u'120',u'2031')
    strDt = strDt.replace(u'121',u'2032')
    strDt = strDt.replace(u'/',u'-')
    return strDt

underlyings = {}

def handleWarrantData(filename):
    with open(filename) as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.decode("cp950")
            line = line.replace('=', '')
            line = line.replace('\n', '')
            line = line.replace('","', '\a')
            line = line.replace('"', '')
            
            tokens = line.split('\a')
            #line = line.replace('"', '')
            tmp = tokens[0].strip() + u'.TWSE' #tds[0] ==> <th>權證代號</th>                                     [ 0-15], Len = 16
            strOut = tmp.encode(const_codec).ljust(16)
            tmp = tokens[1].strip()              #tds[1] ==> <th>權證簡稱</th>                                   [16-47], Len = 32
            strOut = strOut + tmp.encode(const_codec).ljust(32)
            tmp = tokens[2].strip()              #tds[2] ==> <th>美式/歐式</th>                                  [48-55], Len = 8
            strOut = strOut + tmp.encode(const_codec).ljust(8)
            tmp = tokens[3].strip()              #tds[3] ==> <th>認購/認售</th>                                  [56-63], Len = 8
            strOut = strOut + tmp.encode(const_codec).ljust(8)
            tmp = tokens[4].strip()              #tds[4] ==> <th>發行人</th>                                     [64-79], Len = 16
            strOut = strOut + tmp.encode(const_codec).ljust(16)
            tmp = tokens[5].strip()              #tds[5] ==> <th>流動量提供者報價方式</th>                       [80-91], Len = 12            
            strOut = strOut + tmp.encode(const_codec).ljust(12)
            tmp = tokens[7].strip()              #tds[7] ==> <th>上市日期</th>                                   [92-107], Len = 16
            tmp = replaceDate(tmp)
            strOut = strOut + tmp.encode(const_codec).ljust(16)
            tmp = tokens[8].strip()              #tds[8] ==> <th>最後交易日</th>                                 [108-123], Len = 16
            tmp = replaceDate(tmp)
            strOut = strOut + tmp.encode(const_codec).ljust(16)
            tmp = tokens[9].strip()              #tds[9] ==> <th>到期日</th>                                     [124-139], Len = 16
            tmp = replaceDate(tmp)
            strOut = strOut + tmp.encode(const_codec).ljust(16)
            tmp = tokens[10].strip()              #tds[10] ==> <th>結算方式(備註一)</th>                         [140-143], Len = 4
            strOut = strOut + tmp.encode(const_codec).ljust(4)
            tmp = tokens[11].strip()              #tds[11] ==> <th>權證發行數量(仟單位)</th>                     [144-151], Len = 8
            strOut = strOut + tmp.encode(const_codec).ljust(8)
            tmp = tokens[12].strip()              #tds[12] ==> <th>標的證券(指數)代號</th>                       [152-183], Len = 32
            tmp = getUnderlyingCode(tmp)
            underlyings[tmp] = 1            
            strOut = strOut + tmp.encode(const_codec).ljust(32)
            tmp = tokens[13].strip()              #tds[13] ==> <th>標的證券(指數)</th>                           [184-247], Len = 64
            strOut = strOut + tmp.encode(const_codec).ljust(64)
            tmp = tokens[15].strip()              #tds[15] ==> <th>最新標的履約配發數量(每仟單位權證)</th>       [248-259], Len = 12
            strOut = strOut + tmp.encode(const_codec).ljust(12)
            tmp = tokens[16].strip()              #tds[16] ==> <th>最新履約價格(元)/履約指數</th>                [260-271], Len = 12
            strOut = strOut + tmp.encode(const_codec).ljust(12)
            tmp = tokens[17].strip()              #tds[17] ==> <th>最新上限價格(元)/上限指數(備註二、三)</th>    [272-283], Len = 12
            strOut = strOut + tmp.encode(const_codec).ljust(12)
            tmp = tokens[18].strip()              #tds[18] ==> <th>最新下限價格(元)/下限指數(備註二、三)</th>    [284-295], Len = 12
            strOut = strOut + tmp.encode(const_codec).ljust(12)
            tmp = tokens[20].strip()              #tds[20] ==> <th>發行時財務費用年率</th>                       [296-311], Len = 16
            strOut = strOut + tmp.encode(const_codec).ljust(16)
            if len(strOut) != 312:
                invalid_tokens = tokens
                print (len(strOut), strOut )
                continue
            listDataOut.append(strOut)
        pass
    pass
# ----


# 總存放檔案資料
output_files = [f for f in listdir(output_folder) if isfile(join(output_folder, f))]

# 把舊的檔案移除
for f in output_files:
    f = join(output_folder, f)
    #print (f)
    if os.stat(f).st_mtime < now - expired_days * 86400:
        if isfile(f):
            os.remove(f)
            print ("remove: " + f)

def main():
    # 上市
    twWrtUrl = 'https://mops.twse.com.tw/mops/web/ajax_t90sbfa01?encodeURIComponent=1&step=1&ver=1.9&TYPEK=&market=1&wrn_class=all&stock_no=&wrn_no=&co_id=all&wrn_type=all&left_month=all&return_rate=all&price_down=&price_up=&price_inout=all&newprice_down=&newprice_up=&fin_down=&fin_up=&sort=1'
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : output_folder}
    options.add_experimental_option("prefs",prefs)
    chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    chrome.get(twWrtUrl)
    button = chrome.find_element_by_tag_name("button")
    button.click()
    time.sleep(10)
    chrome.close()
    # 找剛剛下載的檔案 by創建日期最大值
    download_filename = max([output_folder + "\\" + f for f in listdir(output_folder)],key=getctime)
    handleWarrantData(download_filename)
    chrome.quit()
    # 上櫃
    twWrtUrl = 'https://mops.twse.com.tw/mops/web/ajax_t90sbfa01?encodeURIComponent=1&step=1&ver=1.9&TYPEK=&market=2&wrn_class=all&stock_no=&wrn_no=&co_id=all&wrn_type=all&left_month=all&return_rate=all&price_down=&price_up=&price_inout=all&newprice_down=&newprice_up=&fin_down=&fin_up=&sort=1'
    chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
    chrome.get(twWrtUrl)
    button = chrome.find_element_by_tag_name("button")
    button.click()
    time.sleep(10)
    chrome.close()
    # 找剛剛下載的檔案 by創建日期最大值
    download_filename = max([output_folder + "\\" + f for f in listdir(output_folder)],key=getctime)
    handleWarrantData(download_filename)
    chrome.quit()
    for skey, val in underlyings.iteritems():
        print (skey)
    if len(listDataOut) >= 1000:
        fo = open(rts_op_settings.TW_WRT_FILE_OUT, 'wb+')
        for strdata in listDataOut:
            fo.write(strdata)
        fo.close()
        for outpath in rts_op_settings.TW_WRT_FILE_COPY_TO:            
            shutil.copy(rts_op_settings.TW_WRT_FILE_OUT, outpath)
        print ('Convert Warrant Data Done!!')
        dsutilities.writeStatusToDB("抓取臺灣權證資料","抓取臺灣權證資料(get_twse_wrt_data.py)", ("OK,Count=" + str(len(listDataOut))))
    else:
        dsutilities.writeStatusToDB("抓取臺灣權證資料","抓取臺灣權證資料(get_twse_wrt_data.py)", "Error:Data too few, Count=" + str(len(listDataOut)))

if __name__ == '__main__':
    main()
