#!/usr/bin/env bash

set -o errexit  # stop when error occurs
set -o pipefail # if not, expressions like `error here | true` will always succeed
set -o nounset  # detects uninitialised variables

readonly _PACKAGES="vim btop dnsmasq hostapd podman git tmux"
readonly _USERNAME="maker"
readonly _PASSWORD="rekam"
readonly _ROOM="caprica"
readonly _OPEN_IOT_GW_URL="https://github.com/namakanyden/open-iot-gateway"

readonly _HOSTAPD_CONF="
country_code=SK
interface=wlan0
ssid=${_ROOM}-things
wpa_passphrase=welcome.to.the.${_ROOM}
driver=nl80211
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
"

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

    # stop service with no proper configuration
    systemctl stop dnsmasq
    systemctl stop hostapd

    # set DHCP server static IP address
    cat >"/etc/dhcpd.conf" <<-'EOF'
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
EOF
    # systemctl restart dhcpcd

    # setup DHCP server
    cat <<-'EOF' >"/etc/dnsmasq.conf"
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
EOF
    systemctl restart dnsmasq

    # setup hostapd
    printf "
#country_code=SK
interface=wlan0
ssid=%s-things
wpa_passphrase=welcome.to.the.%s
#driver=nl80211
hw_mode=g
channel=6
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
" "${_ROOM}" "${_ROOM}" >/etc/hostapd/hostapd.conf

    sed -e '/DAEMON_CONF/d' -e '$aDAEMON_CONF="/etc/hostapd/hostapd.conf"' -i /etc/default/hostapd

    # run
    systemctl unmask hostapd
    systemctl enable hostapd
    systemctl start hostapd
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

    log "Done"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
