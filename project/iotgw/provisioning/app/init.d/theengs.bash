#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source /app/helpers.bash

function main() {
    log "Setting up Theengs"

    local template='/app/templates/theengs/theengsgw.conf'
    local target='/mnt/theengs/theengsgw.conf'

    # template population
    envsubst <"${template}" >"${target}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
