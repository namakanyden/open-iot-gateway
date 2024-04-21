#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source /app/helpers.bash

function main() {
    log "Setting up Homepage"

    local templates='/app/templates/homepage'
    local target='/mnt/homepage'

    # copy images and files
    cp "${templates}/images/"* "${target}/images/"
    cp "${templates}/config/bookmarks.yaml" "${target}/config/"

    # set templates
    envsubst <"${templates}/config/docker.yaml" >"${target}/config/docker.yaml"
    envsubst <"${templates}/config/services.yaml" >"${target}/config/services.yaml"
    envsubst <"${templates}/config/widgets.yaml" >"${target}/config/widgets.yaml"
    envsubst <"${templates}/config/settings.yaml" >"${target}/config/settings.yaml"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
