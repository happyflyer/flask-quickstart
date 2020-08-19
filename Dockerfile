FROM python:3.6.8

WORKDIR /opt/flask-quickstart

COPY . ./

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 6000 && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 6000 && \
    sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list && \
    rm -Rf /var/lib/apt/lists/* && \
    apt-get update && \
    apt-get install -y git net-tools vim supervisor nginx && \
    cp supervisor.conf /etc/supervisor/conf.d/flaskqs.conf && \
    rm /etc/nginx/sites-enabled/default && \
    cp nginx.conf /etc/nginx/sites-enabled/

EXPOSE 8080

# ENTRYPOINT ["./boot.sh"]
