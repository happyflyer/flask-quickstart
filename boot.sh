#!/bin/bash

APP_DIR="/root/flask-quickstart"
cd $APP_DIR

while true; do
  flask db upgrade
  if [[ "$?" == "0" ]]; then
    break
  fi
  echo Deploy command failed, retrying in 5 secs...
  sleep 5
done

flask translate compile

cp config/supervisor.conf /etc/supervisor/conf.d/flask_quickstart.conf
service supervisor start

cp config/nginx.conf /etc/nginx/conf.d/
service nginx start

while true; do
  sleep 1
done
