#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source /app/helpers.bash

function main() {
    log "Setting up MQTT Explorer"

    local template="/app/templates/mqttexplorer/settings.json"
    local target="/mnt/mqttexplorer/settings.json"

    envsubst -i "${template}" -o "${target}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
