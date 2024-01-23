#!/usr/bin/env bash

# to run
# curl -sSL http://xxx/script.bash | bash -s -- hostname
# curl -sSL http://mirek.s.cnl.sk/download/provisioning.balena.bash | bash -s -- dune

set -o errexit
set -o pipefail
set -o nounset

# globals
readonly _CONFIG_FILE="/mnt/boot/config.json"
readonly _CONNAME="balena-hotspot"
readonly _HOTSPOT_CONFIG="/mnt/boot/system-connections/balena-hotspot"
readonly _SP="    "

readonly _HOTSPOT_TEMPLATE='
[connection]
id=balena-hotspot
type=wifi
autoconnect=true
interface-name=wlan0

[wifi]
band=bg
mac-address-randomization=0
mode=ap
ssid=%s

[wifi-security]
key-mgmt=wpa-psk
proto=rsn
psk=%s

[ipv4]
method=shared
addresses=10.0.0.1/24
'

# functions
function log() {
    local message="${*}"
    local now
    now=$(date +%H:%M:%S)

    printf "\e[0;35m%s\e[m: \e[0;33m%s\e[m\n" "${now}" "${message}"
}

function die() {
    local message="${1}"

    printf "%s\n" "${message}" >&2
    exit 1
}

function set_hostname() {
    log "Setup Hostname"

    local hostname="${1:?Hostname is missing}"
    local tempfile

    tempfile=$(mktemp)
    jq ". += {\"hostname\" : \"${hostname}\" }" "${_CONFIG_FILE}" >"${tempfile}"
    mv "${tempfile}" "${_CONFIG_FILE}"
}

function set_hotspot() {
    log "Setup WiFi Hotspot"

    local hostname="${1:?Hostname is missing}"

    ( nmcli connection show "${_CONNAME}" || [ -f  "${_HOTSPOT_CONFIG}" ] ) >/dev/null 2>&1 && {
        log "${_SP}Connection ${_CONNAME} already exist."
    } || {
        log "${_SP}Creating Hotspot"

        local ssid="${hostname}-things"
        local password="welcome.to.the.${hostname}"

        printf "${_HOTSPOT_TEMPLATE}" "${ssid}" "${password}" >"${_HOTSPOT_CONFIG}"
    }
}

function main() {
    local hostname="${1:?Error: Hostname is missing.}"

    set_hostname "${hostname}"
    set_hotspot "${hostname}"

    printf "Rebooting in 10s...\n"
    sleep 10
    reboot
}

# if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "${@}"
# fi
