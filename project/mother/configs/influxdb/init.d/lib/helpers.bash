source "/docker-entrypoint-initdb.d/lib/colors.bash"

function log() {
    local level="${1}"
    shift
    local message="${*}"
    local now
    local color

    now=$(date +%H:%M:%S)

    # pick color for level
    case "${level}" in
        "ERROR" | "error" )
            color="${RED}"
            ;;
        "WARNING" | "WARN" | "warning" | "warn" )
            color="${YELLOW}"
            ;;
        "SUCCESS" | "success" )
            color="${GREEN}"
            ;;
        "DEBUG" | "debug" )
            color="${BLUE}"
            ;;
        "CRITICAL" | "critical" )
            color="${BG_RED}"
            ;;
        *)
            color="${WHITE}"
            ;;
    esac

    printf "${GREEN}%s${RESET} ${color}%-7s %s${RESET}\n" \
        "${now}" "${level}" "${message}"
}


function debug() {
    log DEBUG "${*}"
}


function info() {
    log INFO "${*}"
}


function warning() {
    log WARNING "${*}"
}


function error() {
    log ERROR "${*}"
}


function critical() {
    log CRITICAL "${*}"
}


function success() {
    log SUCCESS "${*}"
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
