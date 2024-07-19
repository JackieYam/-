import urllib2
import bs4
import json
import time
import re
from time import *

code = "ZCH14"
tt1 = strptime("2010-01-01", "%Y-%m-%d")
tt2 = strptime("2016-05-07", "%Y-%m-%d")
rangeBegin = mktime(tt1)
rangeEnd = mktime(tt2)
strUrl = ("http://jscharts-e-barchart.aws.barchart.com//charts/dynamic_zoom/" + code + "/?set_chart_data=Request.JSONP.request_map.request_1&cookie_index=0&range[dataMin]="
            + str(int(rangeBegin*1000)) + "&range[dataMax]=" + str(int(rangeEnd*1000))
            + "&range[frequency]=intraday&range[interval]=1&range[record_type]=&zoom=")
print strUrl

content = urllib2.urlopen(strUrl).read()
content = content.replace("Request.JSONP.request_map.request_1(","")
content = content[:-1]
jsonData = json.loads(content)
for skey in jsonData.keys():
    print skey
#
#bs4Data = bs4.BeautifulSoup(jsonData["html"], "html.parser")
#divs = bs4Data.findAll('div')
#mdiv = divs[510]
#
#PriceData
#[1392912780000,454,454.25,453.75,453.75],[1392912840000,453.75,453.75,453.5,453.5],[1392912900000,453.75,454,453.5,453.75]
pattern = "\"data\"\:[\[\]\.\,0-9]*"
m = re.search(pattern, jsonData["html"])
priData = m.group()
priData = priData.replace("\"data\":","")
priData = priData[:-1]
priceEntries = eval(priData)
#VolumeData
#{\"color\":\"#006600\",\"x\":1392912780000,\"y\":112},{\"color\":\"#FF0000\",\"x\":1392912840000,\"y\":128},{\"color\":\"#006600\",\"x\":1392912900000,\"y\":146}
pattern2 = "\"volume\",\"data\":[\\\"#\:{}\[\]\.\,0-9a-zA-Z]*\"name\""
m2 = re.search(pattern2, jsonData["html"])
volData = m2.group()
volData = volData.replace("\"volume\",\"data\":","")
volData = volData.replace("},{\"name\"", "")
volEntries = eval(volData)
#
for i in range(0,5000,1):
    strRes = str(priceEntries[i][0]) + "," + str(priceEntries[i][1]) + "," + str(priceEntries[i][3]) + "," + str(priceEntries[i][4]) + "," + str(volEntries[i]["y"])
    print strRes
#
pass

