# Additional Services

For adding additional services, which are not part of the *Open IoT Gateway* stack, use additional `docker-compose.yaml` file. For `homepage.group` use label `Services`


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
