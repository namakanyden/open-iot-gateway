# Additional Services

For adding additional services, which are not part of the *Open IoT Gateway* stack, use additional `docker-compose.yaml` file. For `homepage.group` use label `Services`

if you want to connect to some core services, you can connect with IP address or you can connect your services to the same network `iotgw` by specifying the network in `docker-compose.yaml` file following way:

```yaml
networks:
  iotgw:
    external: true
```


## Node-RED

```yaml
nodered:
  image: nodered/node-red
  restart: always
  ports:
  - 1880:1880
  volumes:
  - nodered_data:/data
  labels:
   homepage.group: Services
   homepage.name: Node-RED
   homepage.icon: nodered.png
   homepage.href: http://${HOSTIP:-localhost}:1880
   homepage.description: Node-RED
```
