FROM python:3.6.8

WORKDIR /DATACENTER1

COPY ["requirements.txt", "/root/"]

RUN sed -i "s@/deb.debian.org/@/mirrors.aliyun.com/@g" /etc/apt/sources.list && \
    rm -Rf /var/lib/apt/lists/* && \
    apt-get update && \
    apt-get install -y git net-tools vim tmux htop supervisor nginx && \
    pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple --timeout 6000 && \
    pip install -r /root/requirements.txt -i https://mirrors.aliyun.com/pypi/simple --timeout 6000

ENTRYPOINT ["/bin/bash"]
