import sys
import socket
import select
import os

timeout_in_seconds = 5

def restarthttpd():
    os.startfile(r'C:\Apache\Apache24\bin\httpd.exe')
    pass

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('www.quantfellow.com', 80))
    s.send('GET Index.html\r\n')
    s.setblocking(0)

    ready = select.select([s], [], [], timeout_in_seconds)
    if ready[0]:
        data = s.recv(1024)
        print data
    else:
        print 'timeout'
        os.system("taskkill /f /im httpd.exe")
        os.system("taskkill /f /im httpd.exe")
        restarthttpd()
    s.close()
except socket.error, exc:
    if exc.errno == 10061:
        restarthttpd()
        pass
    
