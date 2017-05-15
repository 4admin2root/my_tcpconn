#!/usr/bin/env python
#-*- coding:utf-8 -*-
from flask import Flask, jsonify, abort, make_response
from tcp_conn import TcpConn
from flask_restful import Api, Resource, reqparse, fields, marshal

import redis
from config import REDIS_HOST
from config import REDIS_PORT
from config import INTERVAL

app = Flask(__name__)
api = Api(app)

# names = ['127.0.0.1_127.0.0.1_6379',]
# values = [127,]
tcp_conn = {
    'tcp_conn_key': fields.String,
    # 'tcp_conn_value': fields.Integer
}


class TcpConnListAPI(Resource):


    def __init__(self):
        self.pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
        self.r = redis.Redis(connection_pool=self.pool)
        self.ex = INTERVAL  # expire time s
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('tcp_conn_key', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('tcp_conn_value', type=int, default=0,
                                   location='json')
        super(TcpConnListAPI, self).__init__()

    def get(self):
        tclist = self.r.keys('tc*')
        return {'tcp_conn_list': tclist }

    def post(self):
        args = self.reqparse.parse_args()
        self.r.set(args['tcp_conn_key'],args['tcp_conn_value'])
        return {'ok': True}, 201


@app.route('/')
def hello_world():
    return 'xxx'

@app.route('/test')
def netjson():
    return render_template('topo.html', name=name)

api.add_resource(TcpConnListAPI, '/tc/api/v1.0/tclist', endpoint='tclist')

if __name__ == '__main__':
    app.run(debug=True)
