#!/bin/sh
export PORT="-p 8082:8080"
export NAME="--name paymentapi"
export CONTAINER="bruntonspall/security-paymentapi"
export LINK="--link userapi:userapi"