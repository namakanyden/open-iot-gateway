#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source /app/helpers.bash

function main() {
    log "Setting up Node-RED"

    local templates='/app/templates/nodered'
    local target='/mnt/nodered/'

    if [[ $(ls -A "${target}") == 'flows.json' ]]; then
        cp "${templates}/"* "${target}"
        chown 1000:1000 "${target}/"*
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
