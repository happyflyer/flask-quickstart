FROM python:3.6.8

WORKDIR /opt/docker_build

COPY ["requirements.txt", "supervisor.conf", "nginx.conf", "/opt/docker_build/"]

VOLUME [ "/opt/flask-quickstart" ]

RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple --timeout 6000 && \
    pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple --timeout 6000 && \
    sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list && \
    rm -Rf /var/lib/apt/lists/* && \
    apt-get update && \
    apt-get install -y git net-tools vim supervisor nginx && \
    cp supervisor.conf /etc/supervisor/conf.d/flask_quickstart.conf && \
    rm /etc/nginx/sites-enabled/default && \
    cp nginx.conf /etc/nginx/sites-enabled/

EXPOSE 8080

# ENTRYPOINT ["./boot.sh"]
