#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

# functions
function log(){
    local message="${*}"
    local now

    now=$(date +%H:%M:%S)
    printf "\e[0;35m%s\e[m: \e[0;33m%s\e[m\n" "${now}" "${message}"
}

function setup_zigbee2mqtt() {
    log "Setting up Zigbee2MQTT"

    local template='/templates/zigbee2mqtt/configuration.yaml'
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

function setup_mosquitto() {
    log "Setting up Mosquitto"

    local template='/templates/mosquitto/mosquitto.conf'
    local target='/mnt/mosquitto/mosquitto.conf'

    # create config
    envsubst <"${template}" >"${target}"

    # create user and password
    mosquitto_passwd -b -c /mnt/mosquitto/passwd "${IOTGW_MQTT_USER}" "${IOTGW_MQTT_PASSWORD}"

    # teardown
    chown -R 1883:1883 /mnt/mosquitto/
}

function setup_homepage() {
    log "Setting up Homepage"

    local templates='/templates/homepage'
    local target='/mnt/homepage'

    # copy images and files
    cp "${templates}/images/"* "${target}/images/"
    cp "${templates}/config/bookmarks.yaml" "${target}/config/"

    # set templates
    envsubst <"${templates}/config/docker.yaml" >"${target}/config/docker.yaml"
    envsubst <"${templates}/config/services.yaml" >"${target}/config/services.yaml"
    envsubst <"${templates}/config/widgets.yaml" >"${target}/config/widgets.yaml"
    envsubst <"${templates}/config/settings.yaml" >"${target}/config/settings.yaml"
}

function main() {
    setup_zigbee2mqtt
    setup_mosquitto
    setup_homepage
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
