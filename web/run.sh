#!/bin/sh
. ./env.sh
docker run $PORT $LINK $NAME -d $CONTAINER
