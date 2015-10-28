#!/bin/sh
export PORT="-p 80:80"
export NAME="--name security-workshop-nginx"
export CONTAINER="nginx"
export LINK="--link security-workshop-web:web"
