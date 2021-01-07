#!/bin/bash

docker pull mysql:5.7

docker run -itd \
  --name flask_quickstart_mysql \
  --restart=always \
  -p 33060:3306 \
  -v ./sql:/docker-entrypoint-initdb.d \
  -e MYSQL_ROOT_PASSWORD=MySQL@root123456 \
  mysql:5.7
