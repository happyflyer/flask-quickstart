#!/bin/bash

chmod +x boot.sh

docker run -itd \
  --name=flask_quickstart_app \
  -p 8080:8080 \
  --restart=always \
  -v ../:/root/flask-quickstart \
  flask_quickstart:latest bash /root/flask-quickstart/boot.sh
