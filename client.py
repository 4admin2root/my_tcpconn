#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests, json, redis
from config import SERVER_HOST
from config import SERVER_PORT
from config import INTERVAL
import  platform

import psutil
#rest api post
#ignore 127.0.0.1
#set interval
#daemon
# windows and linux
# just ipv4
# timeout and retry

def postdata():
    url = url = 'http://'+ SERVER_HOST + ':' +  str(SERVER_PORT) + '/tc/api/v1.0/tclist'
    payload = {'tcp_conn_key': 'tc192.168.111.222_192.168.222.111_1025', 'tcp_conn_value':5000, 'tcp_conn_interval':INTERVAL}
    headers = {'content-type': 'application/json'}
    rp = requests.post(url, data=json.dumps(payload), headers=headers)
    return rp


def getlist():
    tcp_conn = []
    for  i in psutil.net_connections('tcp4'):
        if i.status == 'ESTABLISHED':
            print i.laddr
            print i.raddr
            print i
if __name__ == '__main__':
    getlist()






