#!/bin/sh
. ./env.sh
docker run $PORT $NAME $LINK -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf --rm $CONTAINER
