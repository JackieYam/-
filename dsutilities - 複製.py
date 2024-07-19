import sys
import os
import shutil
import codecs
import datetime
from datetime import date
from datetime import *
import sqlite3
import socket

""""
DS_SqliteDBFile = "C:\\AuroraQuantitative\\DB\\dataservice.db3"
"""
def writeStatusToDB(filename, description, message):
    print message
"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('118.163.27.181', 9999))
    strToSend = 'SS' + 'PUMO:' + filename + '\b' + description + '\b' + message + '\0'
    s.send(strToSend)
    s.close()
"""
    
"""
    print message
    try:
        conn = sqlite3.connect(DS_SqliteDBFile)
        tt = datetime.now()
        strTT = tt.strftime('%Y-%m-%d %H:%M:%S')        
        c = conn.cursor()
        strSQL = ('Replace Into file_imports Values(\'' + filename + '\',\'' + description + '\',\'' + strTT + '\',\'' + message + '\',\'' + strTT + '\',\'Python\')')
        c.execute(strSQL)
        conn.commit()
        conn.close()
    except Exception, e:
        print e
"""
