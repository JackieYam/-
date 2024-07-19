# -*- coding: utf-8 -*-
import urllib2
import bs4
import shutil
import codecs
import ssl
import dsutilities
import rts_op_settings
import sys
import datetime

strLogFile = r'C:\AuroraQuantitative\Temp\get_twse_wrt.log'

def append_log(file_name, text_to_append):
    try:
        stMsgToAppend = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\t" + text_to_append
        with open(file_name, "a+") as file_object:
            file_object.seek(0, 2)
            if file_object.tell() > 0:
                file_object.write("\n");
            file_object.write(stMsgToAppend)
    except:
        pass
    pass
pass
"""
    tds[0] ==> <th>權證代號</th>
    tds[1] ==> <th>權證簡稱</th>
    tds[2] ==> <th>美式/歐式</th>
    tds[3] ==> <th>認購/認售</th>
    tds[4] ==> <th>發行人</th>
    tds[5] ==> <th>流動量提供者報價方式</th>
    tds[6] ==> <th>105/02/26<br>權證收盤價格</th>
    tds[7] ==> <th>上市日期</th>
    tds[8] ==> <th>最後交易日</th>
    tds[9] ==> <th>到期日</th>
    tds[10] ==> <th>結算方式(備註一)</th>
    tds[11] ==> <th>權證發行數量(仟單位)</th>
    tds[12] ==> <th>標的證券(指數)代號</th>
    tds[13] ==> <th>標的證券(指數)</th>
    tds[14] ==> <th>105/02/26<br>標的證券(指數)收盤價格(指數)</th>
    tds[15] ==> <th>最新標的履約配發數量(每仟單位權證)</th>
    tds[16] ==> <th>最新履約價格(元)/履約指數</th>
    tds[17] ==> <th>最新上限價格(元)/上限指數(備註二、三)</th>
    tds[18] ==> <th>最新下限價格(元)/下限指數(備註二、三)</th>
    tds[19] ==> <th>價內外程度</th>
    tds[20] ==> <th>發行時財務費用年率</th>

    output fields:
    tds[0] ==> <th>權證代號</th>                                   [ 0-15], Len = 16                   
    tds[1] ==> <th>權證簡稱</th>                                   [16-47], Len = 32
    tds[2] ==> <th>美式/歐式</th>                                  [48-55], Len = 8
    tds[3] ==> <th>認購/認售</th>                                  [56-63], Len = 8
    tds[4] ==> <th>發行人</th>                                     [64-79], Len = 16
    tds[5] ==> <th>流動量提供者報價方式</th>                       [80-91], Len = 12     
    tds[7] ==> <th>上市日期</th>                                   [92-107], Len = 16    
    tds[8] ==> <th>最後交易日</th>                                 [108-123], Len = 16
    tds[9] ==> <th>到期日</th>                                     [124-139], Len = 16
    tds[10] ==> <th>結算方式(備註一)</th>                          [140-143], Len = 4
    tds[11] ==> <th>權證發行數量(仟單位)</th>                      [144-151], Len = 8
    tds[12] ==> <th>標的證券(指數)代號</th>                        [152-183], Len = 32
    tds[13] ==> <th>標的證券(指數)</th>                            [184-247], Len = 64
    tds[15] ==> <th>最新標的履約配發數量(每仟單位權證)</th>        [248-259], Len = 12
    tds[16] ==> <th>最新履約價格(元)/履約指數</th>                 [260-271], Len = 12
    tds[17] ==> <th>最新上限價格(元)/上限指數(備註二、三)</th>     [272-283], Len = 12
    tds[18] ==> <th>最新下限價格(元)/下限指數(備註二、三)</th>     [284-295], Len = 12
    tds[20] ==> <th>發行時財務費用年率</th>                        [296-311], Len = 16
"""

listDataOut = []

const_codec = 'utf-8'

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

def handleWarrantData(trs):
    for tr in trs:
        headerAttr = tr['class']
        if headerAttr != [u'tblHead']:
            tds = tr.findAll('td')
            tmp = tds[0].getText().strip() + u'.TWSE' #tds[0] ==> <th>權證代號</th>                                     [ 0-15], Len = 16
            strOut = tmp.encode(const_codec).ljust(16)
            tmp = tds[1].getText().strip()              #tds[1] ==> <th>權證簡稱</th>                                   [16-47], Len = 32
            strOut = strOut + tmp.encode(const_codec).ljust(32)[:32]
            tmp = tds[2].getText().strip()              #tds[2] ==> <th>美式/歐式</th>                                  [48-55], Len = 8
            strOut = strOut + tmp.encode(const_codec).ljust(8)[:8]
            tmp = tds[3].getText().strip()              #tds[3] ==> <th>認購/認售</th>                                  [56-63], Len = 8
            strOut = strOut + tmp.encode(const_codec).ljust(8)[:8]
            tmp = tds[4].getText().strip()              #tds[4] ==> <th>發行人</th>                                     [64-79], Len = 16
            strOut = strOut + tmp.encode(const_codec).ljust(16)[:16]
            tmp = tds[5].getText().strip()              #tds[5] ==> <th>流動量提供者報價方式</th>                       [80-91], Len = 12            
            strOut = strOut + tmp.encode(const_codec).ljust(12)[:12]
            tmp = tds[7].getText().strip()              #tds[7] ==> <th>上市日期</th>                                   [92-107], Len = 16
            tmp = replaceDate(tmp)
            strOut = strOut + tmp.encode(const_codec).ljust(16)[:16]
            tmp = tds[8].getText().strip()              #tds[8] ==> <th>最後交易日</th>                                 [108-123], Len = 16
            tmp = replaceDate(tmp)
            strOut = strOut + tmp.encode(const_codec).ljust(16)[:16]
            tmp = tds[9].getText().strip()              #tds[9] ==> <th>到期日</th>                                     [124-139], Len = 16
            tmp = replaceDate(tmp)
            strOut = strOut + tmp.encode(const_codec).ljust(16)[:16]
            tmp = tds[10].getText().strip()              #tds[10] ==> <th>結算方式(備註一)</th>                         [140-143], Len = 4
            strOut = strOut + tmp.encode(const_codec).ljust(4)[:4]
            tmp = tds[11].getText().strip()              #tds[11] ==> <th>權證發行數量(仟單位)</th>                     [144-151], Len = 8
            strOut = strOut + tmp.encode(const_codec).ljust(8)[:8]
            tmp = tds[12].getText().strip()              #tds[12] ==> <th>標的證券(指數)代號</th>                       [152-183], Len = 32
            tmp = getUnderlyingCode(tmp)
            underlyings[tmp] = 1            
            strOut = strOut + tmp.encode(const_codec).ljust(32)[:32]
            tmp = tds[13].getText().strip()              #tds[13] ==> <th>標的證券(指數)</th>                           [184-247], Len = 64
            strOut = strOut + tmp.encode(const_codec).ljust(64)[:64]
            tmp = tds[15].getText().strip()              #tds[15] ==> <th>最新標的履約配發數量(每仟單位權證)</th>       [248-259], Len = 12
            strOut = strOut + tmp.encode(const_codec).ljust(12)[:12]
            tmp = tds[16].getText().strip()              #tds[16] ==> <th>最新履約價格(元)/履約指數</th>                [260-271], Len = 12
            strOut = strOut + tmp.encode(const_codec).ljust(12)[:12]
            tmp = tds[17].getText().strip()              #tds[17] ==> <th>最新上限價格(元)/上限指數(備註二、三)</th>    [272-283], Len = 12
            strOut = strOut + tmp.encode(const_codec).ljust(12)[:12]
            tmp = tds[18].getText().strip()              #tds[18] ==> <th>最新下限價格(元)/下限指數(備註二、三)</th>    [284-295], Len = 12
            strOut = strOut + tmp.encode(const_codec).ljust(12)[:12]
            tmp = tds[20].getText().strip()              #tds[20] ==> <th>發行時財務費用年率</th>                       [296-311], Len = 16
            strOut = strOut + tmp.encode(const_codec).ljust(16)[:16]
            if len(strOut) != 312:
                print (len(strOut), strOut  )
                continue
            listDataOut.append(strOut)
        pass
    pass
            
def main():
    try:
        gcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        gcontext.options |= ssl.OP_NO_SSLv2
        gcontext.options |= ssl.OP_NO_SSLv3
        #Market=1 ==> 上市
        print (u"上市權證資料")
        append_log(strLogFile, "上市權證資料")
        keep_parse = True
        page_no = 1
        while keep_parse:
            twWrtUrl = 'https://mops.twse.com.tw/mops/web/ajax_t90sbfa01?encodeURIComponent=1&step=1&ver=1.9&TYPEK=&market=1&wrn_class=all&stock_no=&wrn_no=&co_id=all&wrn_type=all&left_month=all&return_rate=all&price_down=&price_up=&price_inout=all&newprice_down=&newprice_up=&fin_down=&fin_up=&sort=1&pageno=' + str(page_no)
            content = urllib2.urlopen(twWrtUrl, context=gcontext).read()
            content = bs4.BeautifulSoup(content, "html.parser")
            tables = content.findAll('table')
            # 20220721 tables[1] 改為 tables[2]
            try:
                print (page_no)
                append_log(strLogFile, str(page_no))
                trs = tables[2].findAll('tr')
                handleWarrantData(trs)
                page_no += 1
            except:
                #e = sys.exc_info()
                #print (e)
                keep_parse = False
                print ("FAIL: " + str(page_no))
                append_log(strLogFile, ("FAIL: " + str(page_no)))
                pass
        #Market=2 ==> 上櫃
        print (u"上櫃權證資料")
        append_log(strLogFile, "上櫃權證資料")
        keep_parse = True
        page_no = 1
        while keep_parse:
            twWrtUrl = 'https://mops.twse.com.tw/mops/web/ajax_t90sbfa01?encodeURIComponent=1&step=1&ver=1.9&TYPEK=&market=2&wrn_class=all&stock_no=&wrn_no=&co_id=all&wrn_type=all&left_month=all&return_rate=all&price_down=&price_up=&price_inout=all&newprice_down=&newprice_up=&fin_down=&fin_up=&sort=1&pageno=' + str(page_no)
            content = urllib2.urlopen(twWrtUrl, context=gcontext).read()
            content = bs4.BeautifulSoup(content, "html.parser")
            tables = content.findAll('table')
            # 20220721 tables[1] 改為 tables[2]
            try:
                print (page_no)
                append_log(strLogFile, str(page_no))
                trs = tables[2].findAll('tr')
                handleWarrantData(trs)
                page_no += 1
            except:
                keep_parse = False
                print ("FAIL: " + str(page_no))
                append_log(strLogFile, ("FAIL: " + str(page_no)))
                pass
        for skey, val in underlyings.iteritems():
            print (skey)
        pass
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
            dsutilities.writeStatusToDB("抓取臺灣權證資料","抓取臺灣權證資料(get_twse_wrt_data.py)", "Error:No Data")
    except:
            dsutilities.writeStatusToDB("抓取臺灣權證資料","抓取臺灣權證資料(get_twse_wrt_data.py)", "Error:No Data")
            append_log(strLogFile, sys.exc_info()[0])
    pass

if __name__ == '__main__':
    main()
