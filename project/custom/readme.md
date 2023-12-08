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


## Running

```bash
$ docker compose --env-file ../global.env --env-file custom.env up --detach
```


## Environment Variables

* `IOTGW_ZIGBEE_ADAPTER` - location of Zigbee receiver device, default is `/dev/ttyACM0`
