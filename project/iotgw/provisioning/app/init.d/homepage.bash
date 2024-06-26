#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "/app/lib/helpers.bash"

function main() {
    info "Setting up Homepage"

    local templates='/app/templates/homepage'
    local target='/mnt/homepage'

    # copy images and files
    cp "${templates}/images/"* "${target}/images/"
    cp "${templates}/config/bookmarks.yaml" "${target}/config/"

    # set templates
    envsubst -i "${templates}/config/docker.yaml" -o "${target}/config/docker.yaml"
    sed -i 's|unix://||' "${target}/config/docker.yaml"

    envsubst -i "${templates}/config/services.yaml" -o "${target}/config/services.yaml"
    envsubst -i "${templates}/config/widgets.yaml" -o "${target}/config/widgets.yaml"
    envsubst -i "${templates}/config/settings.yaml" -o "${target}/config/settings.yaml"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
