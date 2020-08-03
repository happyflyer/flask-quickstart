#!/bin/sh
# this script is used to boot a Docker container
cp .env.template .env
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
flask translate compile
service supervisor start
service nginx start
