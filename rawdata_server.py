#!C:\python\python -u
import sys
import socket
import time
import thread
import os

rawFile = 'C:\\Temp\\Raw-2016-3-31.bin'
host = '127.0.0.1'
port = 10005

def push_data(c):
    mcounter = 1
    print 'Push Data To Client...\n'
    fo = open(rawFile, 'rb')
    bRunning = True
    while bRunning:
        a = fo.read(4096)
        if not a:
            bRunning = False
        else:
            try:
                c.send(a)
            except:
                print 'Socket Closed Abnormally!'
                bRunning = False
        mcounter = mcounter + 1
        if mcounter >= 20:
            mcounter = 0
            time.sleep(0.0001)
    print 'Close Socket!!'
    c.close()

s = socket.socket()
s.bind((host, port))
s.listen(5)

while True:
    print 'Wait new connection...\n'
    c, addr = s.accept()
    print 'We have a connection from:', addr
    thread.start_new(push_data,(c,))

pass
