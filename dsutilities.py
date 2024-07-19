import sys
import os
import shutil
import codecs
import datetime
from datetime import date
from datetime import *
import sqlite3

DS_SqliteDBFile = "C:\\AuroraQuantitative\\DB\\dataservice.db3"
ServerID = ""

def writeStatusToDB(filename, description, message):
    print message
    try:
        conn = sqlite3.connect(DS_SqliteDBFile)
        tt = datetime.now()
        strTT = tt.strftime('%Y-%m-%d %H:%M:%S')        
        c = conn.cursor()
        strSQL = ('Replace Into file_imports Values(\'' + ServerID + filename + '\',\'' + description + '\',\'' + strTT + '\',\'' + message + '\',\'' + strTT + '\',\'Python\')')
        c.execute(strSQL)
        conn.commit()
        conn.close()
    except Exception, e:
        print e


def writeStatusToDBNoAdjustment(filename, description, message):
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
