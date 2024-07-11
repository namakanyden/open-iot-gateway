# Mother Server / Cloud


## InfluxDB

po nainstalovani vzniknu tieto bucket-y:

* `metrics` - na zbieranie metrik, obycajne v pravidelnych intervaloch
* `events` - na zbieranie udalosti, v nepravidelnych intervaloch
* `debug` - na testovanie a ladenie

pre pristup k nim je potrebne zistit dva tokeny:

1. na citanie - pre studentov
2. na zapis - pre telegraf (na matke)

zistit tokeny je mozne tymto sposobom:

```bash
token="influxdb-token"
http http://mother:8086/api/v2/authorizations "Authorization:Token ${token}"
```

jednotlive tokeny je vsak mozne dostat takto:

```bash
token="influxdb-token"
token_id="Telegraf: Write to Buckets"
http http://mother:8086/api/v2/authorizations "Authorization:Token ${token}" \
    | jq --raw-output ".. | objects | select(.description == \"${token_id}\") | .token"
```