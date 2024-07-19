import sys
import pymssql
import sqlite3
from datetime import date

host = '192.168.0.101:3301'
user = 'report'
password = '12345678'
database = 'TestDB'

conn = pymssql.connect(host, user, password, database)

today = date.today()
conn = pymssql.connect(host, user, password, database)        
#conn = pymssql.connect(host='192.168.0.101:3301', user='report', password='12345678', database='TestDB')
cursor = conn.cursor()
try:
    cursor.execute("select dbo.getBeforeReportDate(%s)",today)
    for db in cursor.fetchall():
        strtday = db[0].strftime("%Y%m%d")
except:
  pass

conn.close()

print (strtday)
