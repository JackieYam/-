#!C:\python\python -u
import sys
import socket
import time
import thread
import os

host = '127.0.0.1'
dest = '127.0.0.1'
orderPort = 6021
recoverPort = 6024
orderReportPort = 6022
matchReportPort = 6023

def orderService(c):
    while True:
        try:
            data = c.recv(1024)
            time.sleep(15)
        except:
            c.close()        

def orderListenJob(iVal):
    ordService = socket.socket()
    ordService.bind((host, orderPort))
    ordService.listen(5)
    while True:
        print 'Wait new order connection...\n'
        c, addr = ordService.accept()
    print 'We have a order connection from:', addr
    thread.start_new(orderService,(c,))


def recoverService(c):
    while True:
        try:
            data = c.recv(1024)
            time.sleep(15)
        except:
            c.close()   

def recoverListenJob(iVal):
    recService = socket.socket()
    recService.bind((host, recoverPort))
    recService.listen(5)
    while True:
        print 'Wait new recover connection...\n'
        c, addr = recService.accept()
    print 'We have a recover connection from:', addr
    thread.start_new(recoverService,(c,))

ordRptConn = None
matRptConn = None

def doOrdRptService(iVal):
    print "Connect To Dest...From OrderConn"
    ordRptConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ordRptConn.connect((dest, orderReportPort))
    while True:
        try:
            data = "1234567"
            ordRptConn.send(data)
            time.sleep(15)
        except:
            ordRptConn = None
            break

def doMatRptService(iVal):
    print "Connect To Dest...From MatchConn"
    matRptConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    matRptConn.connect((dest, matchReportPort))
    while True:
        try:
            data = "1234567"
            matRptConn.send(data)            
            time.sleep(15)
        except:
            matRptConn = None
            break

while True:
    thread.start_new(orderListenJob, (0,))
    thread.start_new(recoverListenJob, (0,))
    while True:
        try:
            print "Check Connection"
            if ordRptConn is None:
                thread.start_new(doOrdRptService,(1,))
            if matRptConn is None:
                thread.start_new(doMatRptService,(1,))        
            time.sleep(15)
        except:
            pass
    

pass
