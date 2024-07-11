#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "/app/lib/helpers.bash"

function main() {
    info "Setting up InfluxDB"

    local templates='/app/templates/influxdb'
    local target='/mnt/influxdb'

    # copy content
    cp -r "${templates}/"* "${target}"

    # teardown
    chmod +x "${target}/init.sh"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
