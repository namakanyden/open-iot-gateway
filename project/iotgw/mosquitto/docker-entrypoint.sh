#!/usr/bin/env sh

readonly MOSQUITTO_CONFIG="/mosquitto/config/mosquitto.conf"

# prepare config file
sed --in-place \
    -e "s/{{ ROOM }}/$IOTGW_ROOM/g" \
    -e "s/{{ MQTT_REMOTE_PASSWORD }}/$IOTGW_MQTT_REMOTE_PASSWORD/g" \
    -e "s/{{ MQTT_REMOTE_USERNAME }}/$IOTGW_MQTT_REMOTE_USER/g" \
    -e "s/{{ MQTT_REMOTE_BROKER }}/$IOTGW_MQTT_REMOTE_BROKER/g" \
    "${MOSQUITTO_CONFIG}"

# prepare password file
mosquitto_passwd -b -c /mosquitto/config/passwd "${IOTGW_MQTT_USER}" "${IOTGW_MQTT_PASSWORD}"

# update ownership
chown -R 1883:1883 /mosquitto/config/

# original entrypoint goes here ;)
user="$(id -u)"
if [ "$user" = '0' ]; then
    [ -d "/mosquitto" ] && chown -R mosquitto:mosquitto /mosquitto || true
fi

exec "${@}"
