#!/bin/bash

container_name="sensordata-api"
db_name="sensordata-db"

docker stop $container_name
docker rm -f $container_name
docker build -t $container_name .
docker run -d -p 4000:4000 --name $container_name --link $db_name:$db_name --env-file ../sensordata-api.env $container_name

