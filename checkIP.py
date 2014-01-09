# coding=utf8
import urllib2
import urllib
import cookielib
import  datetime
import time
import json
import  threading
import thread
import sys
import base64
import socket
import httplib
threadcount=0
writeLock=threading.RLock()
countLock=threading.RLock()
UserAgent='Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a (392691824)/Worklight/6.0.0'

def addThreadCount():
    global writeLock,threadcount
    writeLock.acquire()
    threadcount=threadcount+1
    writeLock.release()

def subThreadCount():
    global writeLock,threadcount
    writeLock.acquire()
    threadcount=threadcount-1
    writeLock.release()

def outip(ip):
    global writeLock
    writeLock.acquire()
    try:
        txt = ip+'\n'
        output = open('enableIp.txt', 'a')
        output.write(txt)
        output.close()
    finally:
        writeLock.release()

def propxy(url,ip):
    try:
        array=url.split('/')
        host=array[2]
        array[2]=ip
        url='/'.join(array)

        req = urllib2.Request(url)
        req.add_header('User-Agent', UserAgent)
        req.add_header('Host', host)
        return urllib2.urlopen(req,timeout=5).read()
    except:
        print 'err'
        return None

def checkOneIP(ip):
    try:
        addThreadCount()
        url='https://kyfw.12306.cn/otn/login/init'
        res= propxy(url,ip)
        if res :
            print ip
            outip(ip)
            # resobj=json.loads(res)
            # if(resobj['status']):
            #     print ip
            #     outip(ip)
    finally:
        subThreadCount()

httpres= urllib.urlopen('http://www.fishlee.net/apps/cn12306/ipservice/getlist').read()

print httpres
obj = json.loads(httpres)
for i in obj:
    if i['host']=='kyfw.12306.cn':
        ip= i['ip']
        thread.start_new_thread(checkOneIP,(ip,))
    while threadcount>10:
        print 'wait'
        time.sleep(1)


while threadcount>0:
    print 'wait=='
    time.sleep(1)
print '==============================complate==============================='


