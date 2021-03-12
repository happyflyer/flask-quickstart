#!/bin/bash

docker run -itd \
  --name=flask_quickstart_debug \
  --network=host \
  --restart=always \
  -v /etc/localtime:/etc/localtime \
  -v /etc/timezone:/etc/timezone \
  -v ${PWD}:/exec \
  flask_quickstart:latest bash
