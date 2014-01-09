import cookielib
import urllib2
import urllib
__author__ = 'fanjunwei003'
UserAgent='Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/11B554a (392691824)/Worklight/6.0.0'
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

def post(url,parms):
    data = urllib.urlencode(parms)
    headers={
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': UserAgent
    }
    req=urllib2.Request(url,data,headers)
    response=urllib2.urlopen(req)
    return response.read()

def get(url):
    headers={
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': UserAgent
    }
    req=urllib2.Request(url,None,headers)
    response=urllib2.urlopen(req)
    return response.read()
print post('https://kyfw.12306.cn/otn/confirmPassenger/getQueueCountAsync',{'train_date':' Thu Jan 30 2014 22:36:44 GMT+0800 (CST)',
                                                                            'train_no':'380000D63202',
                                                                            'stationTrainCode':'D632',
                                                                            'seatType':'O',
                                                                            'fromStationTelecode':'ZZF',
                                                                            'toStationTelecode':'AOH',
                                                                            'leftTicket':'O023650869O023653018',
                                                                            })
# print post('http://127.0.0.1:8000/clientLogin/',{'username':'fjw','password':'aco00o68b'})
# print get('http://127.0.0.1:8000/meal/getAllUser/')

