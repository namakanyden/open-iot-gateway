# Additional Services

For adding additional services, which are not part of the *Open IoT Gateway* stack, use additional `docker-compose.yaml` file. For `homepage.group` use label `Services`

if you want to connect to some core services, you can connect with IP address or you can connect your services to the same network `iotgw` by specifying the network in `docker-compose.yaml` file following way:

```yaml
networks:
  iotgw:
    external: true
```




## MQTT Explorer

MQTT Explorer is a comprehensive MQTT client that provides a structured overview of your MQTT topics and makes working with devices/services on your broker dead-simple.

homepage: http://mqtt-explorer.com

```yaml
mqtt-explorer:
  image: smeagolworms4/mqtt-explorer
  restart: allways
  ports:
  - 4000:4000
  labels:
    homepage.group: Applications
    homepage.name: MQTT Explorer
    homepage.href: http://${HOSTIP:-localhost}:4000
    homepage.description: MQTT Web Client
```


## Zigbee2MQTT

konfiguracny subor:

```yaml
# Home Assistant integration (MQTT discovery)
homeassistant: false

# allow new devices to join
permit_join: true

# MQTT settings
mqtt:
  # MQTT server URL
  server: 'mqtt://mosquitto'
  # MQTT server authentication, uncomment if required:
  # user: my_user
  # password: my_password
  # MQTT base topic for zigbee2mqtt MQTT messages
  base_topic: gateway/zigbee

# Serial settings
serial:
  # Location of Zigbee dongle
  port: /dev/ttyACM0

# Will run frontend on port 8080
frontend: true
```

Ziskat id adaptera:

```
ls /dev/serial/by-id/
```


## Running

Konfigurácia sa nachádza v súbore `.env`, ktorý vytvoríte úpravou šablóny `template.env`. Následne spustite kompozíciu príkazom:

```bash
$ docker compose up --detach
```

Poznámka: Overiť si konfiguráciu môžete príkazom:

```bash
$ docker compose config
```


## Environment Variables

* `IOTGW_ZIGBEE_ADAPTER` - location of Zigbee receiver device, default is `/dev/ttyACM0`

