# Additional Applications

When adding applications, you can create new `docker-compose.yaml` file with all of them. If you want to add them to homepage, use `Applications` as `homepage.group`.

```yaml

```

if you want to connect to some core services, you can connect with IP address or you can connect your application to the same network `iotgw` by specifying the network in `docker-compose.yaml` file following way:

```yaml
networks:
  iotgw:
    external: true
```


## MQTT Explorer


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
$ docker compose --env-file ../global.env up --detach
```

