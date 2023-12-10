# MQTT Topics

budeme rozlišovať dva typy tém:

* lokálne na zariadení IoT Gateway
* globálne pre celú infraštruktúru


## Lokálne témy

* `gateway/alerts`
* `gateway/ble`
* `gateway/metrics` - metriky zariadenia IoT Gateway, ako napr. stav diskov, pamäte, CPU, ...

## Globálne témy

* `kpi/services/#`
* `kpi/alerts`
* `kpi/<room>/alerts/`
* `kpi/<room>/temperature/<id>`
* `kpi/<room>/humidity/<id>`
* `kpi/<room>/light/<id>`
* `kpi/<room>/door/<id>`


* `kpi/<room>/temperature/<id>/set`


## Meranie teploty

Odpoveď príde v požiadavke na tému `kpi/<room>/temperature/<id>`

```json
{
   "ts": 1702142100,                # UTC timestamp
   "name": "human readable name",
   "id": "unique id",
   "battery": 100,                  # 0 - 100, if available
   "temp": 12.34,                   # value
   "unit": "metric",                # value unit
   "interval": 60                   # repeat interval in seconds
}
```

## Nastavenie vlastností merania

Nastaviť vlastnosti merania je možné odoslaním vlastnej správy do zariadenia v téme `kpi/<room>/temperature/<id>/set`:

```json
{
   "interval": 30,      # new update interval
   "unit": "imperial"   # change unit of value
}
```
