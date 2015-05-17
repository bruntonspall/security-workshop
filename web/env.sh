#!/bin/sh
export PORT="-p 8080:8080"
export NAME="--name web"
export CONTAINER="bruntonspall/security-web"
export LINK="--link paymentapi:paymentapi --link userapi:userapi"