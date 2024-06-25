FROM alpine:3.20

LABEL author "mirek"

# Environment variables substitution for Go:  https://github.com/a8m/envsubst
RUN set -o errexit \
    && apk add \
        jo \
        yq \
        jq \
        bash \
        mosquitto \
        networkmanager-cli \
        curl \
    && machine=$(uname --machine | sed 's/aarch64/arm64/') \
    && curl -L https://github.com/a8m/envsubst/releases/download/v1.2.0/envsubst-$(uname --kernel-name)-"${machine}" --output /usr/local/bin/envsubst \
    && chmod +x /usr/local/bin/envsubst

COPY app/ /app/

WORKDIR /app

ENV DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

CMD [ "/bin/bash", "init.bash" ]
