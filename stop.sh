#!/bin/bash

# Kill all running containers
docker ps | grep -v CONTAINER 1>/dev/null && docker ps -a | cut -d' ' -f1 | grep -v CONTAINER | xargs docker kill
# Remove any images left over
docker ps -a | grep -v CONTAINER 1>/dev/null && docker ps -a | cut -d' ' -f1 | grep -v CONTAINER | xargs docker rm
