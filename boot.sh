#!/bin/bash
# this script is used to boot a Docker container
sleep 5
cd /opt/flask-quickstart || return
# 生成配置文件
cp .env.template .env
# 数据库升级
# 执行前提：创建好数据库和配置 .env 文件
# 执行效果：生成数据库表结构
while true; do
  flask db upgrade
  if [[ "$?" == "0" ]]; then
    break
  fi
  echo Deploy command failed, retrying in 5 secs...
  sleep 5
done
# 编译 web 后端界面的本地化文件
# 执行效果：后端界面变成全中文
flask translate compile
# 启动 supervisor 服务
cp supervisor.conf /etc/supervisor/conf.d/flask_quickstart.conf
service supervisor start
# 启动 nginx 服务
rm /etc/nginx/sites-enabled/default
cp nginx.conf /etc/nginx/sites-enabled/
service nginx start
while true; do
  sleep 1
done
