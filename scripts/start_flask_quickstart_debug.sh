#!/bin/bash

docker run -itd \
  --name=flask_quickstart_debug \
  --network=host \
  --restart=always \
  -v $PWD:/exec/flask-quickstart \
  -v /etc/localtime:/etc/localtime \
  -v /etc/timezone:/etc/timezone \
  flask_quickstart:latest bash
