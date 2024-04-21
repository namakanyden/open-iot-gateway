#!/usr/bin/env bash

trap stop SIGINT SIGTERM

function stop() {
    kill "${CHILD_PID}"
    wait "${CHILD_PID}"
}

# install packages first
(
    cd /data
    npm install --unsafe-perm --no-update-notifier --no-fund --omit=dev
)

# run nodered
/usr/local/bin/node $NODE_OPTIONS node_modules/node-red/red.js --userDir /data $FLOWS "${@}" &

CHILD_PID="$!"

wait "${CHILD_PID}"
