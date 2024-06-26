#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "/app/lib/helpers.bash"

function main() {
    info "Setting Hostname"

    if [[ -z "${BALENA_SUPERVISOR_ADDRESS:-}" ]]; then
        error "Error: Not a Balena device. Quit."
        return
    fi

    local url="$BALENA_SUPERVISOR_ADDRESS/v1/device/host-config?apikey=$BALENA_SUPERVISOR_API_KEY"
    local payload=$(jo network=$(jo hostname="${IOTGW_ROOM}-gw"))

    curl -X PATCH \
        --header "Content-Type:application/json" \
        --data "${payload}" \
        "${url}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
