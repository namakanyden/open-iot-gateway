#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source /app/helpers.bash

function main() {
    log "Setting up Zigbee2MQTT"

    local template='/app/templates/zigbee2mqtt/configuration.yaml'
    local target='/mnt/zigbee2mqtt/configuration.yaml'

    # create default config file
    if [[ ! -f $target ]]; then
        cp "${template}" "${target}"
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

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
