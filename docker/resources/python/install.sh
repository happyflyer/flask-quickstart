#!/bin/bash
set -x

SCRIPT_DIR="/root/resources/python"
cd $SCRIPT_DIR

# ********** ice
apt-get install -y --no-install-recommends python3-zeroc-ice
# pip install --no-cache-dir zeroc-ice

# ********** mysql
pip install --no-cache-dir mysql-connector-python

# ********** web后端
pip install --no-cache-dir \
    python-dotenv \
    flask \
    flask_sqlalchemy \
    flask_migrate \
    flask_login \
    flask_mail \
    flask_bootstrap \
    flask_babel \
    flask_wtf \
    flask_cors \
    flask_docs \
    flask_httpauth \
    flask_apscheduler

# ********** 测试
pip install --no-cache-dir pytest coverage httpie

# ********** 部署
pip install --no-cache-dir gunicorn

# ********** 代码风格
pip install --no-cache-dir autopep8
