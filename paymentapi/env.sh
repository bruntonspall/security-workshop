#!/bin/sh
export PORT="-p 8082:8080"
export NAME="--name security-workshop-paymentapi"
export CONTAINER="bruntonspall/security-paymentapi"
export LINK="--link security-workshop-userapi:userapi"
