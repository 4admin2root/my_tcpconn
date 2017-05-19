[![Build Status](https://travis-ci.org/4admin2root/my_tcpconn.svg?branch=master)](https://travis-ci.org/4admin2root/my_tcpconn)
# my_tcpconn
## a tool for show tcp connection topology
### todo
* init
* daemon
* dockerfile
* travis
* ansible deploy

##server config
* install and start redis first
* test for nginx
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

 * test for gunicorn
 ```
 pip install gunicorn
gunicorn -D -w 4 -b 10.9.5.11:5000 --access-logfile /tmp/access.log \
  --error-logfile /tmp/error.log server:app

 ```
 ##client install
 /ansible/README.md
 
 ##view topo.html
 
browser http://{{SERVER_HOST}}:5000/topo.html
the graph is using [netjsongraph](https://github.com/netjson/netjsongraph.js)

![](https://github.com/4admin2root/my_tcpconn/blob/master/test/demo.png)


