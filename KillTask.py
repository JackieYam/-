import wmi
import os
import time
import sys
c = wmi.WMI()

testTask = 'C:\\WINDOWS\\system32\\notepad.exe'
testTask2 = 'C:\\Program Files\Microsoft Office\\Root\\Office16\\WINWORD.EXE'
quoteServer = 'C:\\AuroraQuantitative\\QuoteServer\\RTSQuoteServer.exe'
quoteServer2 = 'C:\\AuroraQuantitative\\QuoteServer64\\RTSQuoteServer.exe'
f = open('C:\AuroraQuantitative\Scripts\KillTask_Log.txt','a')

for process in c.win32_Process():
    #print process.ProcessId, process.Name, process.ExecutablePath
    if (process.ExecutablePath is not None and process.ExecutablePath.lower() == quoteServer.lower()):
        print 'Kill ',process.ProcessId, process.Name, process.ExecutablePath
        os.system("taskkill /pid "+str(process.ProcessId))
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' KillTask '+ process.ExecutablePath + '\n')
        #process.Terminate()
    if (process.ExecutablePath is not None and process.ExecutablePath.lower() == quoteServer2.lower()):
        print 'Kill ',process.ProcessId, process.Name, process.ExecutablePath
        os.system("taskkill /pid "+str(process.ProcessId))
        f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' KillTask '+ process.ExecutablePath + '\n')

f.close()
