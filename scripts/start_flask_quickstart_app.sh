#!/bin/bash

chmod +x boot.sh

docker run -itd \
  --name=flask_quickstart_app \
  --network=host \
  --restart=always \
  -v $PWD:/exec/flask-quickstart \
  -v /etc/localtime:/etc/localtime \
  -v /etc/timezone:/etc/timezone \
  flask_quickstart:latest bash /exec/flask-quickstart/boot.sh
