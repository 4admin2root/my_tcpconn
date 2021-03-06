#https://hub.docker.com/r/4admin2root/my_tcpconn/
FROM centos:7
MAINTAINER Jason Lui
ADD . /opt/my_tcpconn
WORKDIR /opt/my_tcpconn
RUN yum install python3-pip -y
RUN pip3 install -r requirements_server.txt -i https://mirrors.aliyun.com/pypi/simple/
EXPOSE 5000
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--access-logfile", "logs/access.log", "--error-logfile", "logs/error.log", "server:app"]
