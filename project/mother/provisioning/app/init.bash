#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

function main() {
    for file in init.d/*.bash; do
        bash "${file}"
    done

    if [[ "${DEBUG_PROVISIONING:-0}" == 1 ]]; then
        printf "Debug mode active...\n"
        while true; do
            sleep 60
        done
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
