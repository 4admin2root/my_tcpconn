#!/usr/bin/env python
#-*- coding:utf-8 -*-
import  random
import sys
sys.path.append("../")
from config import REDIS_HOST
from config import REDIS_PORT
from config import INTERVAL
import redis


i = 0
conn = redis.Redis(host=REDIS_HOST,port=REDIS_PORT)
pipe = conn.pipeline()

if __name__ == '__main__':

    while i < 1000:
        ip = 'tc' + str(random.randint(192,255)) + '.' + \
              str(random.randint(168,255)) + '.' + \
              str(random.randint(0,255)) + '.' + \
              str(random.randint(0,255)) + '_' + \
              str(random.randint(1024,65535))
        num = random.randint(1024,65535)
        pipe.set(ip,num,INTERVAL)
        i +=1
    pipe.execute()
