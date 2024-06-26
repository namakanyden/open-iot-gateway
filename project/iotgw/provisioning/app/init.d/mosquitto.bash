#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "/app/lib/helpers.bash"

function main() {
    info "Setting up Mosquitto"

    local template='/app/templates/mosquitto/mosquitto.conf'
    local target='/mnt/mosquitto/mosquitto.conf'

    # create config
    envsubst -i "${template}" -o "${target}"

    # create user and password
    mosquitto_passwd -b -c /mnt/mosquitto/passwd "${IOTGW_MQTT_USER}" "${IOTGW_MQTT_PASSWORD}"

    # teardown
    chown -R 1883:1883 "/mnt/mosquitto"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
