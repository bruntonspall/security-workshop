#!/bin/bash
./stop.sh
# Run each app, one at a time
(cd userapi; ./build.sh && ./run.sh) && sleep 1
(cd paymentapi; ./build.sh && ./run.sh) && sleep 1
(cd web; ./build.sh && ./run.sh) && sleep 1
(cd nginx; ./run.sh) && sleep 1
curl http://localhost:8081/setup
