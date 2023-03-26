# Open-IoT-Gateway
Open IoT Gateway for your projects.



## Additional Services

For adding additional services, which are not part of the *Open IoT Gateway* stack, use additional `docker-compose.yaml` file. For `homepage.group` use label `Services`


### Node-RED

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


## Additional Applications

When adding applications, you can create new `docker-compose.yaml` file with all of them. If you want to add them to homepage, use `Applications` as `homepage.group`.

```yaml

```

### MQTT Explorer


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
