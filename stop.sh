#!/bin/bash

# Kill all running containers
docker ps | grep security-workshop | grep -v CONTAINER 1>/dev/null && docker ps -a | grep security-workshop | cut -d' ' -f1 | grep -v CONTAINER | xargs docker kill
# Remove any images left over
docker ps -a | grep security-workshop | grep -v CONTAINER 1>/dev/null && docker ps -a | grep security-workshop | cut -d' ' -f1 | grep -v CONTAINER | xargs docker rm
