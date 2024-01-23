#!/usr/bin/env sh

readonly CONFIG="/app/data/configuration.yaml"

# prepare config file, if it doesn't exist
if [ -f "${CONFIG}" ]; then
    echo "Config file already exists."
    cat "${CONFIG}"
else
    echo "Creating configuration file."
    sed --in-place \
        -e "s/{{ MQTT_PASSWORD }}/$IOTGW_MQTT_PASSWORD/g" \
        -e "s/{{ MQTT_USER }}/$IOTGW_MQTT_USER/g" \
        -e "s/{{ MQTT_BROKER }}/$IOTGW_MQTT_BROKER/g" \
        -e "s|{{ ZIGBEE_ADAPTER }}|$IOTGW_ZIGBEE_ADAPTER|g" \
        "/app/configuration.yaml"
    mv /app/configuration.yaml "${CONFIG}"
fi

exec "${@}"
