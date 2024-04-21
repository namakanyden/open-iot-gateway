function log() {
    local message="${*}"
    local now

    now=$(date +%H:%M:%S)
    printf "\e[0;35m%s\e[m: \e[0;33m%s\e[m\n" "${now}" "${message}"
}


function is_folder_empty() {
    local folder="${1:?Folder name is missing.}"

    if [[ -z $(ls -A "${folder}") ]]; then
        return 0
    else
        return 1
    fi
}


function die() {
    local message="${1}"

    printf "%s\n" "${message}" >&2
    exit 1
}
