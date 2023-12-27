#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

readonly _PACKAGES="vim btop git tmux"
readonly _USERNAME="maker"
readonly _PASSWORD="rekam"
readonly _TIMEZONE="Europe/Bratislava"
readonly _OS_NAME="Debian GNU/Linux 12 (bookworm)"
readonly _OS_VERSION_ID="12"
readonly _ROOM="${1:?Name of the room is missing as first parameter.}"
readonly _HOSTNAME="${_ROOM}-gw"
readonly _CONNAME="Hotspot"
readonly _SP="    "
readonly _DOCKERNET="iotgw"
readonly _MQTT_REMOTE_BROKER="147.232.205.204"
readonly _MQTT_REMOTE_USERNAME="mother"
readonly _MQTT_REMOTE_PASSWORD="mothermother"

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

function install_software() {
    log "Software installation"

    apt update && sudo apt upgrade --yes
    apt install --yes ${_PACKAGES}

    # install docker
    if [[ ! $(which docker) ]]; then
        log "Installing Docker"
        curl -sSL https://get.docker.io | sh
    fi

    wget https://github.com/Macchina-CLI/macchina/releases/download/v6.1.8/macchina-linux-aarch64 -O /usr/local/bin/macchina
    chmod +x /usr/local/bin/macchina
}

function setup_maker() {
    log "Create and Setup User maker"

    # create user maker
    if ! id "${_USERNAME}" >/dev/null 2>&1; then
        useradd --password "${_PASSWORD}" --user-group "${_USERNAME}"
        chpasswd <<<"${_USERNAME}:${_PASSWORD}"
    fi

    # add maker to group docker
    if [[ ! $(groups "${_USERNAME}") =~ "docker" ]]; then
        usermod -aG docker "${_USERNAME}"
    fi
}

function setup_manager() {
    log "Create and Setup User manager"

    local user=manager

    # create user manager
    if ! id "${user}" >/dev/null 2>&1; then
        useradd --create-home --user-group "${user}"
        mkdir --parents /home/manager/.ssh
        cp assets/manager.pub /home/manager/.ssh/authorized_keys
        chmod 700 /home/manager/.ssh
        chown --recursive manager.manager /home/manager/.ssh
    fi

    # add manager to groups: docker, sudo
    if [[ ! $(groups "${user}") =~ "docker" ]]; then
        usermod -aG docker "${user}"
    fi

    if [[ ! $(groups "${user}") =~ "sudo" ]]; then
        usermod -aG sudo "${user}"
    fi
}

function setup_system() {
    log "System Setup."

    # set the hostname based on the name of the room and update /etc/hosts
    hostnamectl hostname "${_HOSTNAME}"
    sed -i '/127.0.1.1/d' /etc/hosts
    sed -i "\$a127.0.1.1\t${_HOSTNAME}" /etc/hosts

    # disable hwmon kernel module because of too many undervoltage messages
    printf "blacklist raspberrypi_hwmon\n" >/etc/modprobe.d/raspberry_hwmon.conf

    # locales
    timedatectl set-timezone "${_TIMEZONE}"
    localectl set-locale en_US.UTF-8
    localectl set-x11-keymap us
}

function setup_wifi_ap() {
    log "Setup WiFi AP"

    # setup wifi hotspot
    nmcli connection show "${_CONNAME}" >/dev/null || {
        log "${_SP}Creating Hotspot"

        nmcli connection add type wifi ifname wlan0 con-name "${_CONNAME}" autoconnect no ssid "${_ROOM}-things"
        nmcli connection modify "${_CONNAME}" 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
        nmcli connection modify "${_CONNAME}" wifi-sec.key-mgmt wpa-psk
        nmcli connection modify "${_CONNAME}" wifi-sec.psk "welcome.to.the.${_ROOM}"
        nmcli connection modify "${_CONNAME}" ipv4.addresses 10.0.0.1/24
        nmcli connection modify "${_CONNAME}" connection.autoconnect yes
        nmcli connection up "${_CONNAME}"
    } && {
        log "${_SP}Connection ${_CONNAME} already exist."
    }

    # drop trafik comming from the wlan0 interface
    log "${_SP}Configuring Rules for Firewall"

    systemctl stop nftables

    local table="gw-filter"
    nft add table inet "${table}"
    nft add chain inet "${table}" forward '{ type filter hook forward priority 0; }'
    nft add rule inet "${table}" forward iifname "wlan0" drop
    nft add rule inet "${table}" forward oifname "wlan0" drop

    # make the rules apply on system startup
    printf "#!/usr/sbin/nft -f\n\nflush ruleset\n\n" >/etc/nftables.conf
    nft list ruleset >>/etc/nftables.conf

    # enable nftables on boot
    systemctl enable nftables
}

function is_proper_distro() {
    # shellcheck source=/dev/null
    source /etc/os-release

    if [[ "${PRETTY_NAME}" != "${_OS_NAME}" || "${VERSION_ID}" != "${_OS_VERSION_ID}" ]]; then
        return 1
    fi
}

function is_root() {
    if [[ $UID != 0 ]]; then
        return 1
    fi
}

function is_in_proper_folder() {
    if [[ ! -f "docker-compose.yaml" ]]; then
        return 1
    fi
}

function create_env_file() {
    log "Creating .env file for composition"

    local _HOSTIP _DOCKER_GID
    _HOSTIP=$(curl https://ifconfig.me)
    _DOCKER_GID=$(getent group docker | cut -d: -f3)

    # generate .env file
    export _HOSTNAME _ROOM _USERNAME _DOCKER_GID _TIMEZONE _HOSTIP
    envsubst <template.env >.env
}

function create_mosquitto_configuration() {
    log "Creating mosquitto.conf"

    # create configuration file
    export _ROOM _MQTT_REMOTE_BROKER _MQTT_REMOTE_USERNAME _MQTT_REMOTE_PASSWORD
    envsubst <./configs/mosquitto/mosquitto.tpl.conf >./configs/mosquitto/mosquitto.conf

    # generate mqtt password for user maker
    log "${_SP}Creating Mosquitto Password File"
    log "Creating password file for Mosquitto"
    docker image pull eclipse-mosquitto
    docker container run --rm \
        --volume ./configs/mosquitto:/mosquitto/config \
        eclipse-mosquitto \
        mosquitto_passwd -b -c /mosquitto/config/passwd "${_USERNAME}" "${_USERNAME}-${_ROOM}-password"
    # chmod 0700 ./configs/mosquitto/mosquitto.passwd
    chown -R 1883:1883 ./configs/mosquitto
}

function start_containers() {
    log "Starting Docker Containers"

    log "${_SP}Pulling Images"
    docker compose pull

    log "${_SP}Creating Docker Network ${_DOCKERNET}"
    docker network create "${_DOCKERNET}" ||
        log "${_SP}${_SP}Network Already Exist."

    log "${_SP}Starting Composition"
    docker compose up --detach
}

function setup_homepage() {
    log "Updating Configuration of Homepage"

    [[ $(cat configs/homepage/widgets.yaml) =~ "{{ ROOM }}" ]] &&
        sed --in-place "s/{{ ROOM }}/$_ROOM/g" configs/homepage/widgets.yaml
}

function main() {
    is_root ||
        die "ERROR: Need to be root."
    is_proper_distro ||
        die "ERROR: Incorrect OS or version.\nExpected OS is '${_OS_NAME}' with version ${_OS_VERSION_ID}'\nCurrent OS is '${PRETTY_NAME}' with version '${VERSION_ID}'\n"
    is_in_proper_folder ||
        die "ERROR: Script must be executed from folder with docker-compose.yaml file."

    install_software
    setup_system
    setup_wifi_ap
    setup_maker
    setup_manager
    create_env_file
    create_mosquitto_configuration
    setup_homepage
    start_containers

    log "Done"
    log "Reboot in 10 seconds..."
    sleep 10
    log "Rebooting now..."
    reboot
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
