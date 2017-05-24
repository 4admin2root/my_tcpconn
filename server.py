#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
my_tcpconn  test
~~~~~~~~~~~~~~~~~~~~~
@time: 2017/5/18 15:49
@contact: piml.lui@gmail.com
usage:
python server.py

links:

:copyright: 
:license: BSD 3-Clause License
"""

from flask import Flask, render_template, redirect
from flask_restful import Api, Resource, reqparse, fields
import json
from numpy import matrix
from numpy import zeros
import redis
from config import REDIS_HOST
from config import REDIS_PORT
from config import INTERVAL

__title__ = 'server'
__version__ = '0.0.1'
__author__ = 'adminroot'
__license__ = 'BSD 3-Clause License'


app = Flask(__name__)
api = Api(app)


tcp_conn = {
    'tcp_conn_key': fields.String,
    # 'tcp_conn_value': fields.Integer,
    # 'interval': fields.Interger,default value
}


class TcpConnListAPI(Resource):
    """restful api"""
    def __init__(self):
        """init redis connection and reqparse"""
        self.pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
        self.r = redis.Redis(connection_pool=self.pool)
        self.ex = INTERVAL  # expire time s
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('tcp_conn_key', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('tcp_conn_value', type=int, required=True,
                                   location='json')
        self.reqparse.add_argument('tcp_conn_interval', type=int, default=60,
                                   location='json')
        super(TcpConnListAPI, self).__init__()

    def get(self):
        """ get method"""
        tclist = self.r.keys('tc*')
        return {'tcp_conn_list': tclist}

    def post(self):
        """ post method """
        args = self.reqparse.parse_args()
        self.r.set(args['tcp_conn_key'], args['tcp_conn_value'], args['tcp_conn_interval'])  # todo try exception
        return {'ok': True}, 201

@app.route('/')
def hello_world():
    return 'xxx'


@app.route('/topo.html')
def netjson():
    return render_template('topo.html')

@app.route('/chord.html')
def getchord():
    return render_template('chord.html')

@app.route('/favicon.ico')
def getfavicon():
    return redirect('static/favicon.ico')

@app.route('/getjson')
def getjson():
    tcl = TcpConnListAPI().get()['tcp_conn_list']
    d_netjson = {'type': 'test', 'label': 'test', 'protocol': 'tcp', 'version': '0.0.1', 'metric': 'test', 'nodes': [], 'links': [] }
    nodes = []  # netjsongraph node list
    links = []  # netjsongraph link list
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


@app.route('/getmatrix')
def getmatrix():
    tcl = TcpConnListAPI().get()['tcp_conn_list']
    nodes = []
    for i in tcl:
        link = i.split('_')
        l1 = link[1]
        l2 = link[2]
        if l1 not in nodes:
            nodes.append(l1)
        if l2 not in nodes:
            nodes.append(l2)
    tcl_conn_matrix = zeros((len(nodes), len(nodes)))
    for t in tcl:
        l = t.split('_')
        x = nodes.index(l[1])
        y = nodes.index(l[2])
        n = l[3]
        tcl_conn_matrix[x, y] = n
    d_matrix = {'nodes': nodes, 'tcl_conn_matrix': tcl_conn_matrix.tolist() }
    return json.dumps(d_matrix)


api.add_resource(TcpConnListAPI, '/tc/api/v1.0/tclist', endpoint='tclist')

if __name__ == '__main__':
    """run server"""
    app.run(host='0.0.0.0')

