#!/bin/sh
. ./env.sh
docker run $PORT $LINK $NAME -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro -d $CONTAINER
