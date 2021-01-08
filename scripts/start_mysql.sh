#!/bin/bash

# docker pull mysql:5.7

docker run -itd \
  --name flask_quickstart_mysql \
  --restart=always \
  -p 33060:3306 \
  -e MYSQL_ROOT_PASSWORD=MySQL@root123456 \
  -v $PWD/scripts/sql:/docker-entrypoint-initdb.d \
  -v /etc/localtime:/etc/localtime \
  -v /etc/timezone:/etc/timezone \
  mysql:5.7
