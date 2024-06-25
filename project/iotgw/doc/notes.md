# Notes

## Balena

* zrejme sa nedaju nastavit zdroje
   * zrejme problem s docker compose v2


## Node-RED



## Mosquitto

* pomocou nastroja `mosquitto_ctrl` sa da nastavit healthcheck, len treba preskumat moznosti. [dokumentacia](https://mosquitto.org/man/mosquitto_ctrl-1.html). trapny priklad:

   ```docker-compose
   healthcheck:
      test: ["CMD", "mosquitto_ctrl", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
   ```


## Homepage

* healthcheck:

   ```docker-compose
   healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:3000 || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
   ```


## Telegraf

* telegraf musi byt v balene spusteny so skupinou pouzivatela `991`, pretoze zvonku ma socket id skupinu `991`
* na lokalnom systeme musi byt spusteny s pravami, ktore ma skupina `docker` na lokalnom pocitaci
   * treba vymysliet nejake pekne riesenie miesto toho, aby sa GID musel zadavat rucne
