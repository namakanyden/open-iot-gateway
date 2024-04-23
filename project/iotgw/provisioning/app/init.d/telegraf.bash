#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source /app/helpers.bash

function main() {
    log "Setting up Telegraf"

    local template='/app/templates/telegraf/telegraf.conf'
    local target='/mnt/telegraf/telegraf.conf'

    # template population
    envsubst <"${template}" >"${target}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
