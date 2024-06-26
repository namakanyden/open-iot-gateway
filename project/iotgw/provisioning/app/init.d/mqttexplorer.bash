#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "/app/lib/helpers.bash"

function main() {
    info "Setting up MQTT Explorer"

    local template="/app/templates/mqttexplorer/settings.json"
    local target="/mnt/mqttexplorer/settings.json"

    envsubst -i "${template}" -o "${target}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
