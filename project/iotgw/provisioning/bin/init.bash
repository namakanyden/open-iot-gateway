#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

function setup_zigbee2mqtt() {
    local config='/configs/zigbee2mqtt/configuration.yaml'
    local target='/mnt/zigbee2mqtt/configuration.yaml'

    # create default config file
    if [[ ! -f $target ]]; then
        cp "${config}" "${target}"
    fi

    # set mqtt connection settings
    yq --inplace ".mqtt.server=\"mqtt://${IOTGW_MQTT_BROKER}\"" "${target}"
    yq --inplace ".mqtt.user=\"${IOTGW_MQTT_USER}\"" "${target}"
    yq --inplace ".mqtt.password=\"${IOTGW_MQTT_PASSWORD}\"" "${target}"

    # zigbee adapter
    yq --inplace ".serial.adapter=\"${IOTGW_ZIGBEE_ADAPTER}\"" "${target}"
    yq --inplace ".serial.port=\"${IOTGW_ZIGBEE_ADAPTER_PORT}\"" "${target}"

    # advanced settings
    yq --inplace ".advanced.pan_id=${IOTGW_ZIGBEE_PAN_ID}" "${target}"
    yq --inplace ".advanced.channel=${IOTGW_ZIGBEE_CHANNEL}" "${target}"
}

function setup_mosquitto() {
    local config='/configs/mosquitto/mosquitto.conf'
    local target='/mnt/mosquitto/mosquitto.conf'

    # create config
    envsubst <"${config}" > "${target}"

    # create user and password
    mosquitto_passwd -b -c /mnt/mosquitto/passwd "${IOTGW_MQTT_USER}" "${IOTGW_MQTT_PASSWORD}"

    # teardown
    chown -R 1883:1883 /mnt/mosquitto/
}

function main() {
    setup_zigbee2mqtt
    setup_mosquitto
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
