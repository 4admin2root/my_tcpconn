#!/usr/bin/env python
#-*- coding:utf-8 -*-
from flask import Flask, jsonify, abort, make_response,render_template
from flask_restful import Api, Resource, reqparse, fields, marshal_with
import json

import redis
from config import REDIS_HOST
from config import REDIS_PORT
from config import INTERVAL

app = Flask(__name__)
api = Api(app)


tcp_conn = {
    'tcp_conn_key': fields.String,
    # 'tcp_conn_value': fields.Integer,
    # 'interval': fields.Interger,default value
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
        self.reqparse.add_argument('tcp_conn_interval', type=int, default=60,
                                   location='json')
        super(TcpConnListAPI, self).__init__()

    def get(self):
        tclist = self.r.keys('tc*')
        return {'tcp_conn_list': tclist}

    def post(self):
        args = self.reqparse.parse_args()
        self.r.set(args['tcp_conn_key'], args['tcp_conn_value'], args['tcp_conn_interval'])  # todo try exception
        return {'ok': True}, 201

@app.route('/')
def hello_world():
    return 'xxx'


@app.route('/topo.html')
def netjson():
    return render_template('topo.html')


@app.route('/getjson')
def getjson():
    # pass  # todo : return formatted json data
    tcl = TcpConnListAPI().get()['tcp_conn_list']
    d_netjson = {'type': 'test', 'label': 'test', 'protocol': 'tcp', 'version': '0.0.1', 'metric': 'test', 'nodes': [], 'links': [] }
    nodes = []
    links = []
    for i in tcl:
        link = i.split('_')
        l1 = {'id': link[1]}
        l2 = {'id': link[2]}
        if l1 not in nodes:
            nodes.append(l1)
        if l2 not in nodes:
            nodes.append(l2)
        d_link = {'source': link[1], 'target': link[2], 'cost': 1}
        if d_link not in links:
            links.append(d_link)
    d_netjson['nodes'] = nodes
    d_netjson['links'] = links
    return json.dumps(d_netjson)


api.add_resource(TcpConnListAPI, '/tc/api/v1.0/tclist', endpoint='tclist')

if __name__ == '__main__':
    app.run(debug=True)
