# MQTT Topics

budeme rozlišovať dva typy tém:

-  lokálne na zariadení IoT Gateway - Tieto témy sú dostupné len na zariadení IoT Gateway a slúžia na komunikáciu medzi IoT Gateway a senzormi. Na tieto témy sa nedá odoslať správa z iného zariadenia architektúry, Pokiaľ nie je zariadenie priamo pripojené na IoT Gateway.
-  globálne pre celú infraštruktúru - Tieto témy sú dostupné na celú infraštruktúru a slúžia na komunikáciu medzi zariadeniami architektúry. Najmä na komunikáciu medzi IoT Gateway a Mother.

## Lokálne témy

-  `gateway/alerts`
-  `gateway/ble`
-  `gateway/metrics` - metriky zariadenia IoT Gateway, ako napr. stav diskov, pamäte, CPU, ...

## Globálne témy

#### Témy pre senzory:

> Všetky správy odoslane do týchto tém budú preposlane na Mother do témy, transformácia tém je definovaná v tabuľke.

| Gateway Topic              | Moter Topic                   |
| -------------------------- | ----------------------------- |
| `gateway/temperature/<id>` | `kpi/<room>/temperature/<id>` |
| `gateway/humidity/<id>`    | `kpi/<room>/humidity/<id>`    |
| `gateway/light/<id>`       | `kpi/<room>/light/<id>`       |
| `gateway/door/<id>`        | `kpi/<room>/door/<id>`        |
| `gateway/sound/<id>`       | `kpi/<room>/sound/<id>`       |
| `gateway/pressure/<id>`    | `kpi/<room>/pressure/<id>`    |
| `gateway/things/<id>`      | `kpi/<room>/things/<id>`      |

#### Sepcialne témy:

-  `kpi/services/#`
-  `kpi/alerts`
-  `kpi/<room>/alerts/`

## Ako uložiť namerané údaje do databázy

Všetky správy budú musieť byt odosielane v `json` formáte. Do príslušných gateway tém.
Každá sprava podlieha validacii podľa `jsonConfig, ktorý pripadá danej veličine.
Pokiaľ je správa validna tak sa uloží do databázy.

### Príklad:

Ak je správa odoslaná do témy `gateway/temperature/<id>`, potom sa správa prepošle na mother do témy `kpi/<room>/temperature/<id>`.
Každá správa, ktorá príde do tejto témy, je prečítaná a validovaná podľa `jsonConfig`, ktorý je definovaný pre teplotu. Ak je správa platná, uloží sa do databázy.

Príklad správy teploty:

```json
{
   "ts": 1514764800,
   "temperature": 23.5,
   "battery": 100
}
```

Táto správa je platná a uloží sa do databázy podľa `jsonConfig`, ktorý je definovaný takto:

```json
{
   "type": "object",
   "properties": {
      "ts": {
         "type": "number",
         "description": "The time of the event"
      },
      "temperature": {
         "type": "number",
         "description": "The temperature in degrees Celsius"
      },
      "battery": {
         "type": "number",
         "description": "The battery level",
         "minimum": 0,
         "maximum": 100
      }
   },
   "required": ["ts", "temperature"]
}
```

## Ako čítať namerané údaje z databázy

Čítať údaje z databázy je možné viacerými spôsobmi:

1. https://docs.influxdata.com/influxdb/v2/query-data/execute-queries/
2. https://docs.influxdata.com/influxdb/cloud/api-guide/client-libraries/

InfluxDB pre vytváranie query používa jazyk [Flux](https://docs.influxdata.com/influxdb/v2.0/query-data/flux/).

**Autorizácia:**

-  **Url:** https://47.232.205.204:8086
-  **Token:** \_qCTqTkDdS-jMpgq37NJfloqazaDLl91BHxEviUFeSJ3QPWEiC7tdhTl48U5OM5dEeVzp58nqKmLi8mNi8_RzQ==
-  **Org:** Tuke

**Buckety:**

-  **Measurement:** - Hodnoty namerané pomocou senzorov
-  **Things:** - Testovacie hodnoty
-  **Metrics:** - Metriky zariadenia IoT Gateway

## Zoznam veličín

### Teplota

Priklad spravy teploty:

```json
{
   "ts": 1514764800,
   "temperature": 23.5,
   "battery": 100
}
```

JsonSchema pre teplotu:

````json
{
  "type": "object",
  "properties": {
    "ts": {
      "type": "number",
      "description": "The time of the event"
    },
    "temperature": {
      "type": "number",
      "description": "The temperature in degrees Celsius"
    },
    "battery": {
      "type": "number",
      "description": "The battery level",
      "minimum": 0,
      "maximum": 100
    }
  },
  "required": ["ts", "temperature"]
}
```
### Vlhkosť
Príklad správy vlhkosti:
```json
{
  "ts": 1514764800,
  "humidity": 23.5,
  "battery": 100
}
````

JsonSchema pre vlhkosť:

```json
{
   "type": "object",
   "properties": {
      "ts": {
         "type": "number",
         "description": "The time of the event"
      },
      "humidity": {
         "type": "number",
         "description": "The humidity level"
      },
      "battery": {
         "type": "number",
         "description": "The battery level",
         "minimum": 0,
         "maximum": 100
      }
   },
   "required": ["ts", "humidity"]
}
```

### Svetlo

Príklad správy svetla:

```json
{
   "ts": 1514764800,
   "light": 150,
   "battery": 100
}
```

JsonSchema pre svetlo:

```json
{
   "type": "object",
   "properties": {
      "ts": {
         "type": "number",
         "description": "The time of the event"
      },
      "light": {
         "type": "number",
         "description": "The light level"
      },
      "battery": {
         "type": "number",
         "description": "The battery level",
         "minimum": 0,
         "maximum": 100
      }
   },
   "required": ["ts", "light"]
}
```

### Dvere

```json
{
   "ts": 1514764800,
   "status": 1,
   "battery": 100
}
```

JsonSchema pre dvere:

```json
{
   "type": "object",
   "properties": {
      "ts": {
         "type": "number",
         "description": "The time of the event"
      },
      "status": {
         "type": "number",
         "maximum": 1,
         "minimum": 0,
         "description": "The status of the door"
      },
      "battery": {
         "type": "number",
         "description": "The battery level",
         "minimum": 0,
         "maximum": 100
      }
   },
   "required": ["ts", "status"]
}
```

### Zvuk

```json
{
   "ts": 1514764800,
   "sound": 1,
   "battery": 100
}
```

JsonSchema pre zvuk:

```json
{
   "type": "object",
   "properties": {
      "ts": {
         "type": "number",
         "description": "The time of the event"
      },
      "sound": {
         "type": "number",
         "description": "The sound level in decibels"
      },
      "battery": {
         "type": "number",
         "description": "The battery level",
         "minimum": 0,
         "maximum": 100
      }
   },
   "required": ["ts", "sound"]
}
```

### Tlak

```json
{
   "ts": 1514764800,
   "pressure": 1,
   "battery": 100
}
```

JsonSchema pre tlak:

```json
{
   "type": "object",
   "properties": {
      "ts": {
         "type": "number",
         "description": "The time of the event"
      },
      "pressure": {
         "type": "number",
         "description": "The pressure in hPa"
      },
      "battery": {
         "type": "number",
         "description": "The battery level",
         "minimum": 0,
         "maximum": 100
      }
   },
   "required": ["ts", "pressure"]
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
