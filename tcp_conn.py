#!/usr/bin/env python
#-*- coding:utf-8 -*-
import redis
from config import REDIS_HOST
from config import REDIS_PORT
from config import INTERVAL

class TcpConn(object):
    def __init__(self):
        self.pool = redis.ConnectionPool(host=REDIS_HOST,port=REDIS_PORT)
        self.r = redis.Redis(connection_pool = self.pool)
        self.ex = INTERVAL # expire time s
    def get(self,tname):
        return self.r.get(tname)
