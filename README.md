[![Build Status](https://travis-ci.org/4admin2root/my_tcpconn.svg?branch=master)](https://travis-ci.org/4admin2root/my_tcpconn)
[![Docs Build Status](https://readthedocs.org/projects/my-tcpconn/badge/?version=latest)](http://my-tcpconn.readthedocs.io/)
[![Code Climate][codeclimate-badge]][codeclimate-url]
[![Quality Gate](https://sonarcloud.io/api/badges/gate?key=my_tcpconn)](https://sonarcloud.io/dashboard/index/my_tcpconn)
# my_tcpconn
## a tool for show tcp connection topology
todo:
docs
bootstrap
swagger
codeclimate

### server config
* install and start redis first

* for nginx
```
pip install uwsgi
uwsgi -s /run/uwsgi.sock -w server:app
#   #nginx config file block
#     server {
#        listen       5000 default_server;
#        server_name  localhost;
#
#        location / { try_files $uri @yourapplication; }
#        location @yourapplication {
#                include      uwsgi_params;
#                uwsgi_pass   unix:/run/uwsgi.sock;
#       }
#   }
 ```

 * for gunicorn
 ```
 pip install gunicorn
gunicorn -D -w 4 -b 10.9.5.11:5000 --access-logfile /tmp/access.log \
  --error-logfile /tmp/error.log server:app

 ```
 * for docker 
```text
docker-compose up --build
```
 ### client install
 
 linux : /ansible/README.md
 
 you can also run it in windows but without ansible playbook
 
 ### view topo.html ant chord.html
 
browser
 
http://{{SERVER_HOST}}:5000/topo.html

http://{{SERVER_HOST}}:5000/chord.html

http://{{SERVER_HOST}}:5000/bar.html

the graph is using 
[netjsongraph](https://github.com/netjson/netjsongraph.js)
[d3.js](https://d3js.org/)
[echarts](http://echarts.baidu.com/)

![](https://github.com/4admin2root/my_tcpconn/raw/master/test/demo.png)
![](https://github.com/4admin2root/my_tcpconn/raw/master/test/demo2.png)
![](https://github.com/4admin2root/my_tcpconn/raw/master/test/bar.png)


[codeclimate-badge]: https://codeclimate.com/github/4admin2root/my_tcpconn/badges/gpa.svg
[codeclimate-url]: https://codeclimate.com/github/4admin2root/my_tcpconn
