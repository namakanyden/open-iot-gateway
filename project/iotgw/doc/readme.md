# IoT Gateway

IoT Gateway je zariadenie, ktoré slúži ako prostredník pre komunikáciu zariadení v lokálnom prostredí (napr. miestnosť, dom, loď, ...) so zvyšnou architektúrou IoT riešenia. Toto zariadenie pracuje 24/7 a je pripojené k zdroju elektrickej energie.

V našom prípade budeme ako IoT Gateway používať počítač [Raspberry Pi 3](https://www.raspberrypi.com/products/raspberry-pi-3-model-b/).


## Komponenty IoT Gateway

IoT Gateway je postavený pomocou kompozície kontajnerov. Konkrétne sa jedná o tieto kontajnery:

* [Chrony](https://hub.docker.com/r/cturra/ntp) - NTP server
* [Eclipse Mosquitto](https://hub.docker.com/_/eclipse-mosquitto) - MQTT broker
* [Traefik](https://hub.docker.com/_/traefik) - reverzné proxy
* [Node-RED](https://hub.docker.com/r/nodered/node-red) - Low-code programming for event-driven applications
* [homepage](https://gethomepage.dev/v0.8.3/) - aplikačný dashboard
* [Watchtower](https://hub.docker.com/r/containrrr/watchtower) - aktualizuje kontajnery, keď sú k dispozícii aktualizácie ich obrazov
* [Telegraf](https://hub.docker.com/_/telegraf) - agent na zbieranie metrík
* [Theengs](https://hub.docker.com/r/theengs/gateway) - brána z BLE do MQTT


## Inštalácia

[Návod](installation.md) na inštaláciu vás prevedie procesom inštalácie IoT Gateway na minipočítač RPi3.
