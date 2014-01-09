# coding=utf8
import json
import datetime
import gzip
import StringIO
import  time

def response(context, flow):
    #print flow.request.content
    if flow.request.path.find("hdinfo") != -1:
        print '************'
        txt = flow.response.content.replace('hdinfo(','').replace(')','')
        print txt
        obj = json.loads(txt)
        obj['pmstart']=True
        obj['stime']=obj['stime']+1000
        print time.ctime(obj['stime'])
        flow.response.content = 'hdinfo('+json.dumps(obj)+')'
    elif flow.request.path.find("hdcontrol") != -1:
        print '************'
        txt = flow.response.content.replace('hdcontrol(','').replace(')','')
        print txt
        obj = json.loads(txt)
        obj['pmstart']=True
        flow.response.content = 'hdcontrol('+json.dumps(obj)+')'


