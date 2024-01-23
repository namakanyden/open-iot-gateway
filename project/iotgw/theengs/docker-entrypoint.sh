#!/usr/bin/env sh

export MQTT_HOST="${IOTGW_MQTT_BROKER}"
export MQTT_USERNAME="${IOTGW_MQTT_USER}"
export MQTT_PASSWORD="${IOTGW_MQTT_PASSWORD}"

# export MQTT_PUB_TOPIC="gateway/ble"
  #       #       MQTT_SUB_TOPIC: home/TheengsGateway/commands
# PUBLISH_ALL: true
  #       #       TIME_BETWEEN: 60
  #       #       SCAN_TIME: 60
  #       LOG_LEVEL: INFO
  #       DISCOVERY: false
  #       #      DISCOVERY_TOPIC: gateway/homeassistant/sensor
  #       #       DISCOVERY_DEVICE_NAME: TheengsGateway
  #       #      DISCOVERY_FILTER: "[IBEACON]"  # GAEN,MS-CDP
  #       #       SCANNING_MODE: active
export ADAPTER="hci0" #: ${IOTGW_BLE_ADAPTER:-hci0}

# run
exec "${@}"
