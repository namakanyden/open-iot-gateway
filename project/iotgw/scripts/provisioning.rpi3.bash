#!/usr/bin/env bash

set -o errexit  # stop when error occurs
set -o pipefail # if not, expressions like `error here | true` will always succeed
set -o nounset  # detects uninitialised variables

readonly _PACKAGES="vim btop podman git tmux"  # dnsmasq hostapd
readonly _USERNAME="maker"
readonly _PASSWORD="rekam"
readonly _ROOM="caprica"
readonly _OPEN_IOT_GW_URL="https://github.com/namakanyden/open-iot-gateway"


# functions
function log() {
    local message="${*}"
    local now
    now=$(date +%H:%M:%S)

    printf "\e[0;35m%s\e[m: \e[0;33m%s\e[m\n" "${now}" "${message}"
}

function install_software() {
    log "Software installation"

    apt update && sudo apt upgrade --yes
    apt install --yes ${_PACKAGES}

    # install docker
    #   log "Installing Docker"
    #   curl -sSL https://get.docker.io | sh

    wget https://github.com/Macchina-CLI/macchina/releases/download/v6.1.8/macchina-linux-aarch64 -O /usr/local/bin/macchina
    chmod +x /usr/local/bin/macchina
}

function setup_maker() {
    log "Create and setup maker user"

    if [[ ! $(id $_USERNAME >/dev/null 2>&1) ]]; then
        log "User maker already exists."
        return 0
    fi

    useradd --password "${_PASSWORD}" --user-group "${_USERNAME}"
    chpasswd <<<"${_USERNAME}:${_PASSWORD}"
}

function setup_system() {
    log "System Setup."

    # set the hostname based on the name of the room
    hostnamectl hostname "${_ROOM}-gw"

    # disable hwmon kernel module because of too many undervoltage messages
    printf "blacklist raspberrypi_hwmon\n" >/etc/modprobe.d/raspberry_hwmon.conf
}

# sources:
# https://raspberrypi-guide.github.io/networking/create-wireless-access-point
function setup_wifi_ap() {
    log "Setup WiFi AP"

    nmcli connection add type wifi ifname wlan0 con-name Hotspot autoconnect yes ssid "${_ROOM}-things"
    nmcli connection modify Hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
    nmcli connection modify Hotspot wifi-sec.key-mgmt wpa-psk
    nmcli connection modify Hotspot wifi-sec.psk "welcome.to.the.${_ROOM}"
    nmcli connection up Hotspot
}

function main() {
    if [[ $UID != 0 ]]; then
        printf "ERROR: Need to be root.\n" >&2
        exit 1
    fi

    install_software
    setup_system
    setup_wifi_ap
    setup_maker

    log "Reboot in 10 seconds..."
    sleep 10
    log "Rebooting now..."
    reboot
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
