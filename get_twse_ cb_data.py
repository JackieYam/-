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
        #1:���c�N�X	
        #2:���c�W��	
        #3:�Ũ�N�X	
        #4:�Ũ�²��	
        #5:�Ũ����	
        #8:�o����
        #9:������
        #11:���P�a�I
        #12:�o���`�B
        #13:�o����O
        #14:���멳�o��l�B
        #15:�����v�٥������B
        #16:�o�歱�B
        #17:�o��i��
        #19:�����Q�v
        #26:���L�Ũ��O
        #27:�Ũ��O����
        #30:��^�v����
        #31:(�U�@����^�v���)�̪�@���٥����
        #32:(�U�@����^�v����)�̪�@���٥�����
        #33:�H�ε�����
        #43:�̷s�{�ѻ���
        #44:�̷s�{�ѻ���ͮĤ��
        #45:��Ϥ�v
        #54:�ഫ�ײv/�{�Ѷײv
        #57:�o���k���e
        #64:�ഫ�����_
        #65:�ഫ������
        #67:�Ũ�R�^�v����
        #69:�o��a�I
        #72:�{�ѼЪ�
        #98:��O���c
        #126:���e�X������
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
0:�ӳ��~��	
1:���c�N�X	
2:���c�W��	
3:�Ũ�N�X	
4:�Ũ�²��	
5:�Ũ����	
6:�Ũ��	
7:�Ũ�O
8:�o����
9:������
10:���P���
11:���P�a�I
12:�o���`�B
13:�o����O
14:���멳�o��l�B
15:�����v�٥������B
16:�o�歱�B
17:�o��i��
18:�o�����
19:�����Q�v
20:�o������~
21:�o�������	
22:�W���d�_
23:�p�I���覡
24:�p������
25:�I������
26:���L�Ũ��O
27:�Ũ��O����
28:�٥��ԭz
29:�٥��ԭz
30:��^�v����
31:(�U�@����^�v���)�̪�@���٥����
32:(�U�@����^�v����)�̪�@���٥�����
33:�H�ε�����
34:�ӾP���c
35:�̪�o��l�B�ܰʤ��
36:�̪�o��l�B�ܰʭ�]
37:�Ҷ��覡
38:���U���c�ίS��ت����q
39:ñ�Ҿ��c
40:�L����c
41:������ڤ����e
42:�o��ɻ{�ѻ���
43:�̷s�{�ѻ���
44:�̷s�{�ѻ���ͮĤ��
45:��Ϥ�v
46:�w�{�ʪѥ����B
47:�{�Ѷ}�l��
48:�{�ѺI���
49:�{�ʪѥ�����
50:�Ѵ�ú�Ǥ覡	
51:�����-�~
52:�I�����-��
53:�I�����-��
54:�ഫ�ײv/�{�Ѷײv
55:�H�U�H
56:�Ƶ�
57:�o���k���e
58:�o���ײv
59:�{�ʹ�H
60:�ӽФ��}���
61:�Ҵ��|�֭���
62:�ӽеo���`�B
63:�ഫ�����v
64:�ഫ�����_
65:�ഫ������
66:��^�v���q�v
67:�Ũ�R�^�v����
68:�R�^�v���q�v
69:�o��a�I
70:�Φ�
71:�C���i�{�ʪѼ�
72:�{�ѼЪ�
73:���q�Mĳ�p�Ҧ����Ҩ�ѪF�|�θ��Ʒ|���
74:�ӽеo����
75:���ħ��֭���
76:�Ҩ����
77:�겣�����e
78:���뤽�q�R�^�i��(���B)
79:�����Ͻ�^�v�i��(���B)
80:����һ{(�ഫ��)���q�ѪѼ�(���ܧ�n�O)
81:������z�{��(�ഫ)�����q�űi��
82:�����ഫ���Ũ鴫���v�Q�ҮѪѼ�
83:�O�_�̬��w�����٥�
84:�B�z����
85:�U�d���
86:CFI�N�X
87:�֭p�w�o����B
88:�����Q�v����	
89:�������]���
90:�U�����]���
91:�S�O�o�����
92:�Ũ�������c
93:(�Ũ�)��������
94:(�Ũ�)�������
95:�o�椽�q�������c
96:(�o�椽�q)��������
97:(�o�椽�q)�������
98:��O���c
99:(��O���c)�������c
100:(��O���c)��������
101:(��O���c)�������
102:�֭�帹
103:�֭��B��(A)
104:�����֭��B�ר�����
105:�����o��e�w�ϥ��B�פ�(B)
106:�����o��Ũ�ϥ��B�פ�(C)
107:�����o��Ũ��|���B�פ�(D)
108:�o�歱�B2
109:�o�歱�B3
110:�o�歱�B4
111:����W��
112:�^��W��
113:�o��H
114:�B�ʧQ�v�s���Ъ�
115:�B�ʧQ�v�H�Υ[�X(%)
116:����o�i�Ũ�
117:�٥��I�����c����N��
118:�ӫ~����
119:�Ъ����I���O
120:�Ъ����I���O����
121:�O���v
122:�~�Ʀ��q�v
123:��ꦬ�q�v�p���k
124:��ꦬ�q�v�p���k����
125:�s���Ъ�����
126:���e�X������
127:���e�X�����󻡩�
128:�P���H
129:�Ƶ�

"""
