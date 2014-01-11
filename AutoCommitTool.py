# coding=utf8
import json
import datetime
import gzip
import StringIO
import sys
import inspect
import os
import thread
this_file=inspect.getfile(inspect.currentframe())
currentPath=os.path.abspath(os.path.dirname(this_file))
sys.path.append(currentPath)
import CIpQuery

ipQuery=None

def request(context, flow):
    global  ipQuery
    path = flow.request.path
    if flow.request.path.find("loading.gif") != -1:
        flow.request.set_url('http://127.0.0.1/')
    elif flow.request.path.find("otn/leftTicket/query") != -1:
        if ipQuery and ipQuery.enableRes and ipQuery.mQueryURL == flow.request.get_url():
            flow.request.set_url('http://www.baidu.com')
            flow.request.headers['Host']=['www.baidu.com']
            flow.request.headers['Referer']=[]
            flow.request.headers['Cookie']=[]


def response(context, flow):
    global  ipQuery
    #print flow.request.content
    if flow.request.path.find("otn/leftTicket/query") != -1:
        print '************************************'
        url = flow.request.get_url()
        if ipQuery:
            if ipQuery.mQueryURL != url:
                ipQuery.endQuery()
                ipQuery=None
        if not ipQuery :
            #@"二等座" @"一等座"  @"商务座"  @"特等座"  @"高级软卧" @"软卧"   @"硬卧"   @"软座"   @"硬座"
            #@"O"     @"M"      @"9"      @"P"      @"6"       @"4"      @"3"      @"2"     @"1"
            ipQuery=CIpQuery.CIpQuery('D2296','O',queryURL=url)
            ipQuery.startQuery()
        if ipQuery and ipQuery.enableRes :
            print '================ find ================\n'
            flow.response.headers['Content-Encoding']=[]
            flow.response.content = ipQuery.enableRes
    elif flow.request.get_url().find("baidu") != -1:
        print '================new find ================\n'
        flow.response.headers['Content-Encoding']=[]
        flow.response.headers['Content-Type']=['application/json;charset=UTF-8']
        flow.response.content = ipQuery.enableRes


