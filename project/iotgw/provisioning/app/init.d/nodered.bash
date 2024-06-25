#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source /app/helpers.bash

function main() {
    log "Setting up Node-RED"

    local templates='/app/templates/nodered'
    local target='/mnt/nodered/'

    if [[ "${DEBUG_PROVISIONING:-0}" == 1 ]]; then
        # copy all files
        cp "${templates}/"* "${target}"

        # set credentials
        envsubst < "${templates}/flows_cred.json" > "${target}/flows_cred.json"

        chown 1000:1000 "${target}/"*
    fi

    if [[ $(ls -A "${target}") == 'flows.json' ]]; then
        cp "${templates}/"* "${target}"
        chown 1000:1000 "${target}/"*
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
