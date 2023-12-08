# MQTT Topics

budeme rozlišovať dva typy tém:

* lokálne na zariadení IoT Gateway
* globálne pre celú infraštruktúru


## Lokálne témy

* `gateway/alerts`
* `gateway/ble`
* `gateway/metrics` - metriky zariadenia IoT Gateway, ako napr. stav diskov, pamäte, CPU, ...

## Globálne témy

* `kpi/services/`
* `kpi/<room>/alerts/`
* `kpi/<room>/temperature/<id>`
* `kpi/<room>/humidity/<id>`
* `kpi/<room>/light/<id>`
