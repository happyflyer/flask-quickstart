#!/bin/bash

# 测试
docker run -itd --name=flask_quickstart_container -p 8080:8080 --restart=always \
  -v /DATACENTER4/fei.li/flask-quickstart:/opt/flask-quickstart \
  flask_quickstart_image /opt/flask-quickstart/boot.sh
