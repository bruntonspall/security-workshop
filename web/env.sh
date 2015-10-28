#!/bin/sh
export PORT="-p 8080:8080"
export NAME="--name security-workshop-web"
export CONTAINER="bruntonspall/security-web"
export LINK="--link security-workshop-paymentapi:paymentapi --link security-workshop-userapi:userapi"
