FROM python:3.6.8

WORKDIR /opt/docker_build

COPY ["requirements.txt", "/opt/docker_build/"]

RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple --timeout 6000 && \
    pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple --timeout 6000 && \
    sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list && \
    rm -Rf /var/lib/apt/lists/* && \
    apt-get update && \
    apt-get install -y git net-tools vim tmux htop supervisor nginx

EXPOSE 8080

# ENTRYPOINT ["./boot.sh"]
