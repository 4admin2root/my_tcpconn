#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
my_tcpconn  client
~~~~~~~~~~~~~~~~~~~~~
@time: 2017/5/18 15:49
@contact: piml.lui@gmail.com
usage:
python client.py

links:

:copyright: 4admin2root
:license: BSD 3-Clause License
"""

import requests
import json
from config import SERVER_HOST
from config import SERVER_PORT
from config import INTERVAL
from collections import Counter
import logging
import logging.config
from requests import RequestException
import psutil
import time


__title__ = 'client'
__version__ = '0.0.1'
__author__ = 'adminroot'
__license__ = 'BSD 3-Clause License'

#todo
# daemon and windows service
#

lports = []  # listen ports
ltor = []    # local to remote links
rtol = []    # remote to local links


def postdata(cr):
    """post links to http server"""
    url = 'http://' + SERVER_HOST + ':' + str(SERVER_PORT) + '/tc/api/v1.0/tclist'
    headers = {'content-type': 'application/json'}
    for i in cr:
        payload = {'tcp_conn_key': i, 'tcp_conn_value': cr[i], 'tcp_conn_interval': INTERVAL}
        try:
            requests.post(url, data=json.dumps(payload), headers=headers, timeout=3)  # todo :  bad perf
        except RequestException as re:
            logging.error("Post data failed: {0}".format(re))
            logging.debug('SERVER_HOST:' + SERVER_HOST)
            logging.debug('SERVER_PORT:' + str(SERVER_PORT))
            # exit when post failed
            # exit(1) 


def getlist():
    """ get tcp4 network links """
    tcs = psutil.net_connections('tcp4')
    logging.debug('Get tcp4 connections :' + str(tcs))
    for i in tcs:
        if i.status == 'LISTEN' and i.laddr[0] != '127.0.0.1':
            lports.append(i.laddr[1])  # todo : how to handle same port and diff nic, how to specify nic
    for i in tcs:
        if i.status == 'ESTABLISHED' and i.laddr[0] != '127.0.0.1':
            if i.laddr[1] in lports:
                rtol.append('tc' + '_' + i.raddr[0] + '_' + i.laddr[0] + '_' + str(i.laddr[1]))
            # elif i.raddr[0] != SERVER_HOST and i.raddr[1] != SERVER_PORT:
            else:
                ltor.append('tc' + '_' + i.laddr[0] + '_' + i.raddr[0] + '_' + str(i.raddr[1]))


def run():
    """getlist and post to server"""
    logging.config.fileConfig('logging.conf')
    logging.getLogger('example02')
    getlist()
    ltor_counter = Counter(ltor)
    logging.debug('ltor:' + str(ltor_counter))
    rtol_counter = Counter(rtol)
    logging.debug('rtol:' + str(rtol_counter))
    logging.debug('start to post data to server')
    postdata(ltor_counter)
    postdata(rtol_counter)


if __name__ == '__main__':
    while True:
        run()
        time.sleep(INTERVAL)
