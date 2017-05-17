#!/usr/bin/env python
#-*- coding:utf-8 -*-
import requests, json
from config import SERVER_HOST
from config import SERVER_PORT
from config import INTERVAL
from collections import Counter
import logging
import logging.config
from requests import RequestException



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
        try:
            requests.post(url, data=json.dumps(payload), headers=headers, timeout=3)  # todo :  bad perf
        except RequestException as re:
            print "Post data failed: {0}".format(re)
            exit(1)


def getlist():
    tcs = psutil.net_connections('tcp4')
    for i in tcs:
        if i.status == 'LISTEN' and i.laddr[0] != '127.0.0.1':
            lports.append(i.laddr[1])  # todo : how to handle same port and diff nic, how to specify nic
    for i in tcs:
        if i.status == 'ESTABLISHED' and i.laddr[0] != '127.0.0.1':
            if i.laddr[1] in lports and i.raddr[0] != SERVER_HOST and i.raddr[1] != 22:
                rtol.append('tc' + '_' + i.raddr[0] + '_' + i.laddr[0] + '_' + str(i.laddr[1]))
            elif i.raddr[0] != SERVER_HOST and i.raddr[1] != SERVER_PORT:
                ltor.append('tc' + '_' + i.laddr[0] + '_' + i.raddr[0] + '_' + str(i.raddr[1]))


if __name__ == '__main__':
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('example02')
    getlist()
    ltor_counter = Counter(ltor)
    rtol_counter = Counter(rtol)
    logging.debug('start to post data to server')
    postdata(ltor_counter)
    postdata(rtol_counter)
    logging.info('finished')





