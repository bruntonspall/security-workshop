#!/bin/sh
. ./env.sh
docker run $PORT $NAME $LINK -v $(pwd):/app --rm $CONTAINER
