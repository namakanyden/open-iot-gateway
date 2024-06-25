# Core Services

The core services contains:

* Mosquitto Broker
* Theengs Gateway
* Telegraf
* Chrony
* Traefik
* Homepage
* Watchtower


## Theengs Gateway

Provides bridge between BLE and MQTT.


## Running

```bash
$ docker compose --env-file ../global.env --env-file core.env up --detach
```

## Environment Variables

* `IOTGW_ROOM` - name of room, where the gateway is located, default is `home`
* `IOTGW_DEPARTMENT` - name of the department, default is `none`
* `IOTGW_BLE_ADAPTER` - name of the local BLE adapter, default is `hci0`
* `IOTGW_NTP_SERVERS` - list (pool) of NTP servers, default is `time.cloudflare.com`

