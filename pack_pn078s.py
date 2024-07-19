# -*- coding: utf-8 -*-
import sys
import os
import zlib
import gzip
import base64
import dsutilities
import datetime
import sqlite3
import StringIO
import struct


futPN07BFile = 'C:\\AuroraQuantitative\\Scripts\\TTPN07BF'
optPN07BFile = 'C:\\AuroraQuantitative\\Scripts\\TTPN07B'


dataEntries = {'FUTPN07B':futPN07BFile, 'OPTPN07B':optPN07BFile}



sqliteDBFile = "C:\\AuroraQuantitative\\DB\\dataservice.db3"


conn = sqlite3.connect(sqliteDBFile)
cursor = conn.cursor()

#try:
for keyVal,fileName in dataEntries.iteritems():
    fo  = open(fileName, 'rb+')
    data = fo.read()
    fo.close()
    lData = len(data)
    data2 = unicode(data)
    buf = StringIO.StringIO()
    compressed = gzip.GzipFile(fileobj=buf, mode="wb")
    compressed.write(data2)
    compressed.close()
    zdata = buf.getvalue()
    zdata = struct.pack("@I", lData) + zdata
    print zdata[0], zdata[1], zdata[2], zdata[3]
    base64Data = base64.b64encode(zdata)
    strDt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print strDt, len(base64Data)
    strSQL = "Replace Into key_value_storage(space,key,value,last_change,changed_by) Values(\'PSC\',\'" + keyVal + "\',\'" + base64Data + "\',\'" + strDt + "\',\'PY\')"
    cursor.execute(strSQL)
conn.commit()
conn.close()
    
#except:
#    x = str(sys.exc_info()[0])
#    print x
#    pass
