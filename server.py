#!/usr/bin/env python
#-*- coding:utf-8 -*-
from flask import Flask
from tcp_conn import TcpConn

app = Flask(__name__)

names = ['127.0.0.1_127.0.0.1_6379',]
values = [127,]

@app.route('/')
def hello_world():
    return value

if __name__ == '__main__':
    tc = TcpConn()
    value = tc.get(names[0])
    print value
    
    app.run()

