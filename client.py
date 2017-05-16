#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests, json, redis
from config import SERVER_HOST
from config import SERVER_PORT
from config import INTERVAL
from collections import Counter

import psutil
#todo
#rest api post
#ignore 127.0.0.1
#set interval
#daemon
# windows and linux
# just ipv4
# timeout and retry
lports = []
ltor = []
rtol = []

def postdata(cr):
    url = url = 'http://' + SERVER_HOST + ':' + str(SERVER_PORT) + '/tc/api/v1.0/tclist'
    headers = {'content-type': 'application/json'}
    for i in cr:
        payload = {'tcp_conn_key': i, 'tcp_conn_value': cr[i], 'tcp_conn_interval': INTERVAL}
        rp = requests.post(url, data=json.dumps(payload), headers=headers)  # todo :1 .try  2. bad perf


def getlist():
    tcs = psutil.net_connections('tcp4')
    for i in tcs :
        if i.status == 'LISTEN' and i.laddr[0] != '127.0.0.1':
            lports.append(i.laddr[1])  # todo : how to handle same port and diff nic, how to specify nic
    for i in tcs :
        if i.status == 'ESTABLISHED' and i.laddr[0] != '127.0.0.1':
            if i.laddr[1] in lports:
                rtol.append('tc' + '_' + i.raddr[0] + '_' + i.laddr[0] + '_' + str(i.laddr[1]))
            else:
                ltor.append('tc' + '_' + i.laddr[0] + '_' + i.raddr[0] + '_' + str(i.raddr[1]))

if __name__ == '__main__':
    getlist()
    ltor_counter = Counter(ltor)
    rtol_counter = Counter(rtol)
    postdata(ltor_counter)
    postdata(rtol_counter)






