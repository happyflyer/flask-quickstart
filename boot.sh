#!/bin/sh
# this script is used to boot a Docker container
cd /opt/flask-quickstart || return
cp .env.template .env
while true; do
  flask db upgrade
  if "$?" == "0"; then
    break
  fi
  echo Deploy command failed, retrying in 5 secs...
  sleep 5
done
flask translate compile
cp supervisor.conf /etc/supervisor/conf.d/flask_quickstart.conf
service supervisor start
rm /etc/nginx/sites-enabled/default
cp nginx.conf /etc/nginx/sites-enabled/
service nginx start
