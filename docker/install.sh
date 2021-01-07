#!/bin/bash
set -x

RESOURCES_FLODER="/root/resources"

# apt安装过程非交互
export DEBIAN_FRONTEND=noninteractive

#  -------------------------- 基本的工具包 --------------------------
apt-get install -y --no-install-recommends \
htop tmux vim git net-tools supervisor nginx

#  -------------------------- python 3.6 --------------------------
# bionic仓库下载的是3.6版本的python，跑模型用的python建议都用3.6版本
apt-get install -y --no-install-recommends \
python3 python3-dev python3-distutils python3-pip python3-numpy
rm /usr/bin/python
ln -s /usr/bin/python3 /usr/bin/python
ln -s /usr/bin/pip3 /usr/bin/pip

mkdir ~/.pip/
echo '[global]' >> ~/.pip/pip.conf
echo 'index-url = https://mirror.baidu.com/pypi/simple' >> ~/.pip/pip.conf

python -m pip install --upgrade pip
# 工具包
pip install --no-cache-dir setuptools wheel cython numpy

# -------------------------- python的运行库 --------------------------
bash $RESOURCES_FLODER/python/install.sh
