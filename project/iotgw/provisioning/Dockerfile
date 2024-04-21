FROM alpine

LABEL author "mirek"

RUN apk add jo yq jq bash envsubst mosquitto networkmanager-cli

COPY app/ /app/

WORKDIR /app

ENV DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

CMD [ "/bin/bash", "init.bash" ]
