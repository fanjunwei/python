# coding=utf8
import urllib2
import urllib
import time
import json
import threading
import thread
import sys
import base64

class CIpQuery(object):
    
    def __init__(self,trainCode,seat,date=None,stationFrom=None,stationTo=None,queryURL=None):
    #@"二等座" @"一等座"  @"商务座"  @"特等座"  @"高级软卧" @"软卧"   @"硬卧"   @"软座"   @"硬座"
    #@"O"     @"M"      @"9"      @"P"      @"6"       @"4"      @"3"      @"2"     @"1"
        self.mSeatMap={"O":"二等座","M":"一等座","9":"商务座","P":"特等座","6":"高级软卧","4":"软卧","3":"硬卧","2":"软座","1":"硬座"}
        proxy_support = urllib2.ProxyHandler({"http":"http://127.0.0.1:8888"})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        self.mIpFilePath='enableIp.txt'
        self.mDate=date
        self.mStationFrom=stationFrom
        self.mStationTo=stationTo
        self.mTrainCode=trainCode
        self.mSeat=seat
        self.hasStart=False
        if queryURL:
            self.mQueryURL=queryURL
        else:
            self.mQueryURL='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT'%(self.mDate,self.mStationFrom,self.mStationTo)
        self.mUserAgent='Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a (392691824)/Worklight/6.0.0'
        self.mCountLock=threading.RLock()
        self.mMustCount=2
        self.mIndex=0
        self.mIps =[]
        self.mFinished=False
        self.readProxyFromFile()
    def printLog(self,log):
        if not self.mFinished:
            print log

    def propxy(self,url,ip):
        try:
            array=url.split('/')
            host=array[2]
            array[2]=ip
            url='/'.join(array)
            req = urllib2.Request(url)
            req.add_header('User-Agent', self.mUserAgent)
            req.add_header('Host', host)
            return urllib2.urlopen(req,timeout=60).read()
        except:
            self.printLog('err')


    def readProxyFromFile(self):
        file = open(self.mIpFilePath,'r')
        for line in file.readlines():
            self.mIps.append(line.strip())

    def getYupiaoCount(self,yupiaoStr,seat):
        out=0
        for i in range(0,len(yupiaoStr)/10):
            s=yupiaoStr[i*10:i*10+10]
            c_mSeat=s[0:1]
            if(c_mSeat==seat):
                count=int(s[6:6+4])
                if(count<3000):
                    out=out+count
                else:
                    out=out+count-3000

        return out

    def getNewIndex(self):
        try:
            self.mCountLock.acquire()
            self.mIndex=self.mIndex+1
            if(self.mIndex>=len(self.mIps)):
                self.mIndex=0
            return self.mIndex
        finally:
            self.mCountLock.release()


    def query(self,ip):
        if self.mFinished :
            return
        print '预订%s,%s\n'%(self.mTrainCode,self.mSeatMap[self.mSeat])
        res = self.propxy(self.mQueryURL,ip)
        if self.mFinished :
            return
        obj = json.loads(res)
        data=obj['data']
        #queryLeftNewDTO=data['queryLeftNewDTO']

        for tr in data:
            secretStr = tr['secretStr']
            unquoteSecretStr=urllib.unquote(secretStr)
            decodeSecretStr=base64.b64decode(unquoteSecretStr)
            args = decodeSecretStr.split('#')
            code=args[2]
            #printLog(code)
            yupiaoStr=args[13]
            count=self.getYupiaoCount(yupiaoStr,self.mSeat)
            timeTick=float(args[15])/1000.0
            #
            if(code==self.mTrainCode):
                if not self.mFinished:
                    print yupiaoStr
                # print decodeSecretStr
                # print code
                # print yupiaoStr
                # print decodeSecretStr
                #printLog(time.ctime(timeTick))

                if(not self.mFinished and count>self.mMustCount):
                    obj['data']=[tr];
                    res=json.dumps(obj)
                    self.mFinished=True
                    self.enableRes=res
                    print '================================ ok ====================================='
                    return

    def queryThread(self):
        while not self.mFinished:
            i=self.getNewIndex()
            try:
                self.query(self.mIps[i])
            except Exception ,e:
                #printLog(e.message)
                time.sleep(1)
    def startQuery(self):
        if not self.hasStart:
            self.hasStart=True
            for i in range(0,10):
                thread.start_new_thread(self.queryThread,())
    def endQuery(self):
        self.mFinished=True

if __name__=='__main__':
    date=sys.argv[1]
    stationFrom=sys.argv[2]
    stationTo=sys.argv[3]
    trainCode=sys.argv[4]
    seat=sys.argv[5]
    cipq=CIpQuery(date,stationFrom,stationTo,trainCode,seat)
    cipq.startQuery()

