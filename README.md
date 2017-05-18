# my_tcpconn
## a tool for show tcp connection topology
### todo
* init
* daemon
* dockerfile
* travis
* ansible deploy

##server config
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
