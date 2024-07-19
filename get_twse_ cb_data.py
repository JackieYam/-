# -*- coding: cp950 -*-
import zipfile
import urllib
import urllib2
import bs4
import shutil
import codecs
import ssl
import dsutilities
import rts_op_settings
import datetime
import requests
from datetime import date


dtNow = datetime.datetime.now()
yearEnd = dtNow.year - 1911
yearBegin = dtNow.year - 10 - 1911
print yearBegin, yearEnd

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-CN;q=0.5',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://mops.twse.com.tw/mops/web/t120sb02_q9',    
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
}
#https://mops.twse.com.tw/server-java/t120sb02_d1?firstin=true&step=12&TYPEK=&bond_kind=5%2C7&nh=h&filename=&mtypek=&bond_id_1=&bond_id_2=&issuer_stock_code_1=&issuer_stock_code_2=&issuer=&issue_date_yy_1=105&issue_date_mm_1=1&issue_date_dd_1=1&issue_date_yy_2=110&issue_date_mm_2=12&issue_date_dd_2=31&mature_date_yy_1=&mature_date_mm_1=&mature_date_dd_1=&mature_date_yy_2=&mature_date_mm_2=&mature_date_dd_2=&underwriter=&bd_currency=&issueFlag=&coupon_kind=&coupon_rate_1=&coupon_rate_2=&spec_issue=&guaranteed_0=&eva_kind=&eva_unit=&evarank=&guaranteed_1=&ontime=Y&listornot=&maturity_hmyear_1=&maturity_hmyear_2=&raiseway=&overtime=0
twCBUrl = 'https://mops.twse.com.tw/server-java/t120sb02_d1?'
formData = ('firstin=true&step=12&TYPEK=&bond_kind=5%2C7&nh=h&filename=&mtypek=&bond_id_1=&bond_id_2=&issuer_stock_code_1=&issuer_stock_code_2=&issuer=&issue_date_yy_1='
           + str(yearBegin) + '&issue_date_mm_1=1&issue_date_dd_1=1&issue_date_yy_2=' + str(yearEnd) + '&issue_date_mm_2=' + str(dtNow.month) + '&issue_date_dd_2=' + str(dtNow.day) + '&mature_date_yy_1=&mature_date_mm_1=&mature_date_dd_1=&'
           + 'mature_date_yy_2=&mature_date_mm_2=&mature_date_dd_2=&underwriter=&bd_currency=&issueFlag=&coupon_kind=&coupon_rate_1=&coupon_rate_2=&spec_issue=&guaranteed_0=&eva_kind=&eva_unit=&evarank=&guaranteed_1=&ontime=Y&listornot=&maturity_hmyear_1=&'
           + 'maturity_hmyear_2=&raiseway=&overtime=0')
twCBUrl = twCBUrl + formData
#print twCBUrl

x = ''
def main():
    global x
    fout = codecs.open(r"C:\AuroraQuantitative\DataImportOutput\twcbinfo.csv", mode="wb+",encoding='utf-8')
    gcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    gcontext.options |= ssl.OP_NO_SSLv2
    gcontext.options |= ssl.OP_NO_SSLv3
    request = urllib2.Request(twCBUrl)
    response = urllib2.urlopen(request, context=gcontext)
    data = response.read()
    ofs = open(r'C:\AuroraQuantitative\DataImportOutput\twcb.html', 'wb')
    data = data.decode('big5', 'ignore')
    x = data
    #,from_encoding='utf-8'
    soup = bs4.BeautifulSoup(data, 'html.parser', from_encoding='windows-1252')
    soup.encoding = 'windows-1252'
    ##soup.prettify('windows-1252')    
    tbls = soup.find_all('table')
    trs = tbls[0].find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        #1:機構代碼	
        #2:機構名稱	
        #3:債券代碼	
        #4:債券簡稱	
        #5:債券種類	
        #8:發行日期
        #9:到期日期
        #11:掛牌地點
        #12:發行總額
        #13:發行幣別
        #14:本月底發行餘額
        #15:本月償還本金金額
        #16:發行面額
        #17:發行張數
        #19:票面利率
        #26:有無債券擔保
        #27:債券擔保情形
        #30:賣回權條款
        #31:(下一次賣回權日期)最近一次還本日期
        #32:(下一次賣回權價格)最近一次還本價格
        #33:信用評等級
        #43:最新認股價格
        #44:最新認股價格生效日期
        #45:行使比率
        #54:轉換匯率/認股匯率
        #57:發行辦法內容
        #64:轉換期間起
        #65:轉換期間迄
        #67:債券買回權條件
        #69:發行地點
        #72:認股標的
        #98:擔保機構
        #126:提前出場條件
        strOut = (tds[1].text + "," + tds[2].text + "," + tds[3].text + "," + tds[4].text + "," + tds[5].text + "," + tds[8].text + ","
                  + tds[9].text + "," + tds[11].text + "," + tds[12].text + "," + tds[13].text + "," + tds[14].text + "," + tds[15].text + ","
                  + tds[16].text + "," + tds[17].text + "," + tds[19].text + "," + tds[26].text + "," + tds[27].text + "," + tds[30].text + ","
                  + tds[31].text + "," + tds[32].text + "," + tds[33].text + "," + tds[43].text + "," + tds[44].text + "," + tds[45].text + ","
                  + tds[54].text + "," + tds[57].text + "," + tds[64].text + "," + tds[65].text + "," + tds[67].text + "," + tds[69].text + ","
                  + tds[72].text + "," + tds[98].text + "," + tds[126].text)
        #print strOut
        strOut = strOut + "\n"
        fout.write(strOut)
    fout.close()
    shutil.copy(r"C:\AuroraQuantitative\DataImportOutput\twcbinfo.csv", r"C:\AuroraQuantitative\RamenFiles\\Data\twcbinfo.csv") 
    pass
pass
if __name__ == '__main__':
    main()
"""
0:申報年月	
1:機構代碼	
2:機構名稱	
3:債券代碼	
4:債券簡稱	
5:債券種類	
6:債券期	
7:債券別
8:發行日期
9:到期日期
10:掛牌日期
11:掛牌地點
12:發行總額
13:發行幣別
14:本月底發行餘額
15:本月償還本金金額
16:發行面額
17:發行張數
18:發行價格
19:票面利率
20:發行期限年
21:發行期限月	
22:上市櫃否
23:計付息方式
24:計息次數
25:付息次數
26:有無債券擔保
27:債券擔保情形
28:還本敘述
29:還本敘述
30:賣回權條款
31:(下一次賣回權日期)最近一次還本日期
32:(下一次賣回權價格)最近一次還本價格
33:信用評等級
34:承銷機構
35:最近發行餘額變動日期
36:最近發行餘額變動原因
37:募集方式
38:受託機構或特殊目的公司
39:簽證機構
40:過戶機構
41:限制條款之內容
42:發行時認股價格
43:最新認股價格
44:最新認股價格生效日期
45:行使比率
46:已認購股份金額
47:認股開始日
48:認股截止日
49:認購股份種類
50:股款繳納方式	
51:息日期-年
52:付息日期-月
53:付息日期-日
54:轉換匯率/認股匯率
55:信託人
56:備註
57:發行辦法內容
58:發行日匯率
59:認購對象
60:申請公開日期
61:證期會核准日期
62:申請發行總額
63:轉換溢價率
64:轉換期間起
65:轉換期間迄
66:賣回權收益率
67:債券買回權條件
68:買回權收益率
69:發行地點
70:形式
71:每單位可認購股數
72:認股標的
73:公司決議私募有價證券股東會或董事會日期
74:申請發行日期
75:金融局核准日期
76:證券種類
77:資產池內容
78:本月公司買回張數(金額)
79:本月行使賣回權張數(金額)
80:本月所認(轉換為)普通股股數(未變更登記)
81:本月受理認股(轉換)之公司債張數
82:本月轉換為債券換股權利證書股數
83:是否依約定按時還本
84:處理情形
85:下櫃日期
86:CFI代碼
87:累計已發行金額
88:票面利率種類	
89:本次重設日期
90:下次重設日期
91:特別發行條件
92:債券評等機構
93:(債券)評等等級
94:(債券)評等日期
95:發行公司評等機構
96:(發行公司)評等等級
97:(發行公司)評等日期
98:擔保機構
99:(擔保機構)評等機構
100:(擔保機構)評等等級
101:(擔保機構)評等日期
102:核准文號
103:核准額度(A)
104:本次核准額度到期日期
105:本次發行前已使用額度元(B)
106:本次發行債券使用額度元(C)
107:本次發行債券後尚有額度元(D)
108:發行面額2
109:發行面額3
110:發行面額4
111:中文名稱
112:英文名稱
113:發行人
114:浮動利率連結標的
115:浮動利率信用加碼(%)
116:永續發展債券
117:還本付息機構金資代號
118:商品種類
119:標的風險類別
120:標的風險類別說明
121:保本率
122:年化收益率
123:投資收益率計算方法
124:投資收益率計算方法說明
125:連結標的說明
126:提前出場條件
127:提前出場條件說明
128:銷售對象
129:備註

"""
