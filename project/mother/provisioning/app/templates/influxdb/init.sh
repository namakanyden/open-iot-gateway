#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

readonly __path__=$(dirname "${BASH_SOURCE[0]}")
source "${__path__}/lib/helpers.bash"

function main() {
    info "Post Setup Initialization"

    # create buckets
    info "Creating Buckets"
    influx bucket create --name metrics \
        --description "Metrics from sensors." \
        --retention 0 \
        --org "${INFLUXDB_ADMIN_ORG}" \
        --token "${INFLUXDB_ADMIN_USER_TOKEN}"
    influx bucket create --name events \
        --description "Events from actuators." \
        --retention 0 \
        --org "${INFLUXDB_ADMIN_ORG}" \
        --token "${INFLUXDB_ADMIN_USER_TOKEN}"
    influx bucket create --name debug \
        --description "Accepts all data. For debug purposes only." \
        --retention 1d \
        --org "${INFLUXDB_ADMIN_ORG}" \
        --token "${INFLUXDB_ADMIN_USER_TOKEN}"

    # create token for reading
    local bucket_ids=$(influx bucket ls  --org "${INFLUXDB_ADMIN_ORG}" --token "${INFLUXDB_ADMIN_USER_TOKEN}" --hide-headers | egrep "metrics|events|debug" | cut -f1)
    influx auth create \
        --description "Makers: Read from Buckets" \
        --org "${INFLUXDB_ADMIN_ORG}" \
        --token "${INFLUXDB_ADMIN_USER_TOKEN}" \
        $(for bucket_id in $(echo "${bucket_ids}" | xargs); do echo "--read-bucket ${bucket_id}"; done)
    influx auth create \
        --description "Telegraf: Write to Buckets" \
        --org "${INFLUXDB_ADMIN_ORG}" \
        --token "${INFLUXDB_ADMIN_USER_TOKEN}" \
        $(for bucket_id in $(echo "${bucket_ids}" | xargs); do echo "--read-bucket ${bucket_id}"; done)

    # cleanup
    # delete the default bucket
    influx bucket delete --name primary --org "${INFLUXDB_ADMIN_ORG}"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
