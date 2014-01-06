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
import  re
UserAgent='Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a (392691824)/Worklight/6.0.0'
writeLock=threading.RLock()
countLock=threading.RLock()
threadcount=0

def propxy(url,proxyUrl):
    starts = time.time()
    proxy_support = urllib2.ProxyHandler({"http":"http://"+proxyUrl})
    opener = urllib2.build_opener(proxy_support)
    req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
    res=''
    try:
        f=opener.open(req,timeout=3)
        res= f.read()
    except urllib2.URLError ,e:
        res=None

    return (res,time.time()-starts)


#print propxy('http://ip.chinaz.com/','217.169.209.2:6666')

def outPropxy(proxyAddr,delay):
    global writeLock
    writeLock.acquire()
    try:
        txt = proxyAddr+'\t'+str(delay)+'\n'

        output = open('/Users/fanjunwei003/Desktop/enableProxy.txt', 'a')
        output.write(txt)
        output.close()
    finally:
        writeLock.release()


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



def checkPropxy(proxyAddr):
    addThreadCount()
    try:
        (res,t)= propxy('http://www.7manba.com/getheader.aspx',proxyAddr)
        print proxyAddr
        print res

        if(res and t<2 and res.find('114.91.120.191')==-1 and res.find('check_propxy')!=-1):
            #print '%s\t%d'%(res,t)
            print proxyAddr
            print t
            outPropxy(proxyAddr,t)
    except:
        print 'errpr'
    finally:
        subThreadCount()

def checkAllPropxy():
    file = open('/Users/fanjunwei003/Desktop/proxy.txt')
    for line in file.readlines():
        #print line
        thread.start_new_thread(checkPropxy,(line.strip(),))
        while threadcount>10:
            print 'wait'
            time.sleep(1)
    file.close()
    print '============================= comple ================================================================================='

#checkAllPropxy()
#sys.stdin.readline()
#print propxy('http://www.7mnaba.com/getheader.aspx','117.25.129.238:8888')
#<table id="ip_list">
def getProxy(url):
    try:
        addThreadCount()
        print url
        output = open('/Users/fanjunwei003/Desktop/proxy.txt', 'a')
        httpres= urllib.urlopen(url).read()
        #print httpres
        tablere = re.compile('<table id="ip_list">(.*)</table>',re.DOTALL)
        #print tablere
        table= tablere.search(httpres).groups()[0]
        rowre=re.compile('<tr class.*?</tr>',re.DOTALL)
        tdre=re.compile('<td>(.*?)</td>',re.DOTALL)
        for row in  rowre.findall(httpres) :
            args= tdre.findall(row)
            txt = args[1]+":"+args[2]+'\n'
            output.write(txt)
        output.close()
    finally:
        subThreadCount()

def getAllProxy():
    for i in range(1,100):
        thread.start_new_thread(getProxy,('http://www.xici.net.co/nn/'+str(i),))
        #getProxy('http://www.xici.net.co/nn/'+str(i))
        while threadcount>10:
            print 'wait'
            time.sleep(1)
    print '============================= comple ================================================================================='

#getAllProxy()
checkAllPropxy()
while threadcount==0:
    print '****'
    time.sleep(1)