import sys
import os
import datetime
import shutil
from datetime import date
import dsutilities

#Begin Settings
daysLimit = 5
dirsToBeChcecked = [("C:\\AuroraQuantitative\\ExecutionServer\\ChannelData\\", daysLimit), \
                ("C:\\AuroraQuantitative\\ExecutionServer\\Logs\\", daysLimit), \
                ("C:\\AuroraQuantitative\\ExecutionServer\\ServerLogs\\", daysLimit), \
                ("C:\\AuroraQuantitative\\ExecutionServer\\ClientLogs\\", daysLimit), \
                ("C:\\AuroraQuantitative\\QuoteServer\\Logs\\", daysLimit), \
                ("C:\\AuroraQuantitative\\QuoteServer\\ServerLogs\\", daysLimit), \
                ("C:\\AuroraQuantitative\\QuoteServer\\ClientLogs\\", daysLimit), \
                ("C:\\AuroraQuantitative\\QuoteServer2\\Logs\\", daysLimit), \
                ("C:\\AuroraQuantitative\\QuoteServer2\\ServerLogs\\", daysLimit), \
                ("C:\\AuroraQuantitative\\QuoteServer2\\ClientLogs\\", daysLimit), \
                ("C:\\AuroraQuantitative\\QuoteServer64\\Logs\\", daysLimit), \
                ("C:\\AuroraQuantitative\\QuoteServer64\\ServerLogs\\", daysLimit), \
                ("C:\\AuroraQuantitative\\QuoteServer64\\ClientLogs\\", daysLimit), \
                ("C:\\AuroraQuantitative\\XMessageServer\\ChannelData\\", daysLimit), \
                ("C:\\AuroraQuantitative\\XMessageServer\\ClientLogs\\", daysLimit), \
                ("C:\\AuroraQuantitative\\XMessageServer\\ServerLogs\\", daysLimit),
                ("C:\\AuroraQuantitative\\XUpdateServer\\ClientLogs\\", daysLimit), \
                ("C:\\AuroraQuantitative\\XUpdateServer\\ServerLogs\\", daysLimit),\
                ("C:\\AuroraQuantitative\\RiskManager\\Logs\\", daysLimit),
                ("C:\\AuroraQuantitative\\DataService\\Logs\\", daysLimit),
		("C:\\DDSCSystem\\Concord\\API\\Log\\", 3)]
filesToBeChecked = []
#End Settings

mToday = date.today()

for dirEntry, thisDaysLimit in dirsToBeChcecked:
    dirs = os.listdir(dirEntry)
    for dirItem in dirs:
        if not os.path.isdir((dirEntry + dirItem)):
            continue
        try:            
            ival = int(dirItem)
            mDay = (ival % 100)
            mMonth = (int((ival - mDay) / 100) % 100)
            mYear = int((ival / 10000))
            dtDir = date(mYear, mMonth, mDay)
            delta = mToday - dtDir
            if delta.days >= thisDaysLimit and delta.days <= 365:
                shutil.rmtree((dirEntry + dirItem))
                print ("Removed:" + (dirEntry + dirItem))
        except Exception, e:
            print 'Error!!', e
            continue


for f in filesToBeChecked:
    try:
        os.remove(f)
        print ("Removed:" + f)
    except Exception, e:
        print 'Error', e

dsutilities.writeStatusToDB("DeleteLog","Clear Logs!!", "OK")
