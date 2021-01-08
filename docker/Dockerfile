# 使用方法：docker build --squash -t <NAME>:<TAG> .

FROM ubuntu:18.04

# 工作路径
WORKDIR /root

# 默认启动bash
CMD ["/bin/bash"]

RUN set -x && \
    # rm /etc/apt/sources.list.d/* && \
    # 设置apt源
    # mirrors.163.com
    # mirrors.aliyun.com
    # 192.168.9.1   (实验室搭建的，暂时只用于构建docker)
    export APT_MIRROR=mirrors.aliyun.com && \
    # 设置ubuntu系统代号
    # 16.04=xenial 18.04=bionic 20.04=focal
    export MARK=bionic && \
    rm /etc/apt/sources.list && \
    echo "deb http://$APT_MIRROR/ubuntu/ $MARK main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://$APT_MIRROR/ubuntu/ $MARK-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://$APT_MIRROR/ubuntu/ $MARK-security main restricted universe multiverse" >> /etc/apt/sources.list && \
    apt-get clean && \
    apt-get update && \
    apt-get install -y --no-install-recommends language-pack-zh-hans

# shell切换中文支持
ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN:zh:en_US:en
ENV LC_ALL zh_CN.UTF-8

# 复制本目录所有文件
COPY . .

# 执行安装脚本
RUN bash install.sh && \
    # 刷新C++库清单
    ldconfig && \
    # 清除无用文件
    cd /root && rm -rf resources && \
    rm -rf /var/lib/apt/lists/*
