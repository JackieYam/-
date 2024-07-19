# -*- coding: utf-8 -*-
import sys
import os
import datetime
import time
import dsutilities

csvFile = r"C:\AuroraQuantitative\ForeignDataConverter\commodityinfo.csv"

tt = os.path.getmtime(csvFile)
dtFile = datetime.datetime.fromtimestamp(tt)
dtNow = datetime.datetime.now()
dtCheck = dtNow#datetime.datetime(dtNow.year, dtNow.month, dtNow.day, 8, 22, 0)
diff = dtCheck - dtFile
if diff.seconds > 420:
    dsutilities.writeStatusToDB("臺灣證期權商品","抓凱基證期權商品",("Error-商品檔時間有誤:" + dtFile.strftime("%Y-%m-%d %H:%M:%S")))
else:
    dsutilities.writeStatusToDB("臺灣證期權商品","抓凱基證期權商品","OK")
##dsutilities.writeStatusToDB("DeleteLog","Clear Logs!!","OK")
