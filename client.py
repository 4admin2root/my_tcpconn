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
import config
from collections import Counter
import logging
import logging.config
from requests import RequestException
import psutil
import time
import json

__title__ = 'client'
__version__ = '0.0.1'
__author__ = 'adminroot'
__license__ = 'BSD 3-Clause License'

# todo
# daemon and windows service
#

lports = []  # listen ports
ltor = []  # local to remote links
rtol = []  # remote to local links
logging_config = json.load(open('logging.json', 'r'))
logging.config.dictConfig(logging_config)
logger = logging.getLogger('mylogger')


def postdata(cr):
    """post links to http server"""
    url = 'http://' + config.SERVER_HOST + ':' + str(config.SERVER_PORT) + '/tc/api/v1.0/tclist'
    headers = {'content-type': 'application/json'}
    for i in cr:
        payload = {'tcp_conn_key': i, 'tcp_conn_value': cr[i], 'tcp_conn_interval': config.INTERVAL}
        try:
            requests.post(url, data=json.dumps(payload), headers=headers, timeout=3)  # todo :  bad perf
        except RequestException as re:
            logger.error("Post data failed: {0}".format(re))
            logger.debug('SERVER_HOST:' + config.SERVER_HOST)
            logger.debug('SERVER_PORT:' + str(config.SERVER_PORT))
            # exit when post failed
            # exit(1) 


def getlist():
    """ get tcp network links """
    tcs = psutil.net_connections('tcp')
    logger.debug('Get tcp connections :' + str(tcs))
    for i in tcs:
        if i.status == 'LISTEN' and i.laddr.ip != '127.0.0.1':
            lports.append(i.laddr.port)  # todo : how to handle same port and diff nic, how to specify nic
    for i in tcs:
        if i.status == 'ESTABLISHED' and i.laddr.ip != '127.0.0.1':
            if i.laddr.port in lports:
                rtol.append('tc' + '_' + i.raddr.ip.lstrip('::ffff:') + '_' + i.laddr.ip.lstrip('::ffff:') + '_' + str(
                    i.laddr.port))
            # elif i.raddr[0] != SERVER_HOST and i.raddr[1] != SERVER_PORT:
            else:
                ltor.append('tc' + '_' + i.laddr.ip.lstrip('::ffff:') + '_' + i.raddr.ip.lstrip('::ffff:') + '_' + str(
                    i.raddr.port))


def clearlist():
    """ clean tcp data """
    lports.clear()
    ltor.clear()
    rtol.clear()


def run():
    """getlist and post to server"""
    getlist()
    ltor_counter = Counter(ltor)
    logger.debug('ltor:' + str(ltor_counter))
    rtol_counter = Counter(rtol)
    logger.debug('rtol:' + str(rtol_counter))
    logger.debug('start to post data to server')
    postdata(ltor_counter)
    postdata(rtol_counter)
    if not config.KEEP_DATA:
        clearlist()


if __name__ == '__main__':
    while True:
        run()
        time.sleep(config.INTERVAL)
