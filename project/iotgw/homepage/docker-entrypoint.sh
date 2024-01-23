#!/usr/bin/env sh

# set room name
sed --in-place "s|{{ ROOM }}|$IOTGW_DEPARTMENT/$IOTGW_ROOM|g" config/widgets.yaml

# set host ip
# hostip=$(wget -q -O - ifconfig.me)
sed --in-place "s/{{ HOSTIP }}/$IOTGW_HOSTIP/g" config/services.yaml

# set docker socket
sed --in-place "s|{{ SOCKET }}|${DOCKER_HOST#unix://}|g" config/docker.yaml

exec "${@}"
