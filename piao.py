# coding=utf8
import json
import datetime
import gzip
import StringIO

GMT_FORMAT = '%H:%M:%S'
def request(context, flow):
    print '本机:' + datetime.datetime.utcnow().strftime(GMT_FORMAT)
    flow.request.headers['Accept-Encoding']=[]

def response(context, flow):
    #print '*********'+flow.request.path
    # if flow.response.headers['Content-Encoding'] && flow.response.headers['Content-Encoding'][0]=='gzip':
    #     data = StringIO.StringIO(flow.response.content)
    #     gz = gzip.GzipFile(fileobj=data)
    #     flow.response.content = gz.read()
    #     #print flow.response.content
    #     gz.close()
    #     flow.response.headers['Content-Encoding']=[]
    #     flow.response.headers['My']=['aa','bb']
    # print '*********001'
    print '服务:' + flow.response.headers['Date'][0][17:17 + 8]
    print '本机:' + datetime.datetime.utcnow().strftime(GMT_FORMAT)
    #print flow.request.content
    if flow.request.path.find("queryLeftTicket") != -1:
    #        flow.response.content=/*-secure-   */
        print '************'
        txt = flow.response.content.replace('/*-secure-', '').replace('*/', '')
        obj = json.loads(txt)
        tickets = obj['ticketResult']
        for t in tickets:
            print '%s\t%s\t%s\t%s\n' % (t['station_train_code'], t['yp_info'], t['yp_ex'], t['message'])
            t['message'] = ''
            t['flag'] = ''
            t['yp_info'] = yupiao(t['yp_info'])
            #print t['yp_info']
        flow.response.content = json.dumps(obj)
    # elif flow.request.content.find('procedure=confirmPassengerInfoSingle') != -1 :
    #     obj = json.loads(flow.response.content)
    #     #obj['succ_flag']='1'
    #     print obj['error_msg']
        #flow.response.content = json.dumps(obj)

def yupiao(yu):
    res = ''
    for i in range(0, len(yu) / 10):
        one = yu[i * 10:i * 10 + 7] + '222'
        res = res + one
    return res


