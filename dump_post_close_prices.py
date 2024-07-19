import sqlite3
import datetime
from datetime import *

mktDataDBFile = r"C:\AuroraQuantitative\DB\marketdata.db3"
dsDBFile = r"C:\AuroraQuantitative\DB\dataservice.db3"

deltaDays = timedelta(days=-5)
dateCriteria = date.today()
dateCriteria = dateCriteria + deltaDays

conn = sqlite3.connect(mktDataDBFile)
c = conn.cursor()
strSQL = "Delete From daily_snapshots Where tradingdate < '" + dateCriteria.isoformat() + "'"
print strSQL
c.execute(strSQL)
conn.commit()
strSQL = "select Code, last, TotalVolume from daily_snapshots where code Like 'TX%'"
c.execute(strSQL)
mktData = c.fetchall()
strData = ""
for r in mktData:
    code = r[0]
    last = r[1]
    totalVolume = r[2]
    if last <= 0:
        continue
    #print code, last, totalVolume
    if strData != "":
        strData = strData + ","
    strData += (code + "=" + str(last))

strSQL = "select Code, last, TotalVolume from daily_snapshots where code Like 'MX%'"
c.execute(strSQL)
mktData = c.fetchall()
for r in mktData:
    code = r[0]
    last = r[1]
    totalVolume = r[2]
    if last <= 0:
        continue
    if strData != "":
        strData = strData + ","
    strData += (code + "=" + str(last))
conn.close()

conn = sqlite3.connect(dsDBFile)
c = conn.cursor()
strSQL = ("Replace Into key_value_storage(space,[key],[value],last_change, changed_by) "
        + "Values('PSC','AHPrices','" + strData + "','" + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        + "','PY')")
c.execute(strSQL)
conn.commit()
conn.close()
