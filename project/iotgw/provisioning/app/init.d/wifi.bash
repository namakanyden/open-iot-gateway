#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "/app/lib/helpers.bash"

function main() {
    info "Setting up WiFi"

    local ssid="${IOTGW_ROOM}-things"
    local password="welcome.to.the.${IOTGW_ROOM}"

    # delete existing WiFi network, if exist
    # if nmcli connection show | grep -q "^${ssid} "; then
    #     log "Deleting existing network '${ssid}'"
    #     nmcli connection delete "${ssid}"
    # fi

    # create WiFi hotspot/AP

}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
