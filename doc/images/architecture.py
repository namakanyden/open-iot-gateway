#!/usr/bin/env python3

from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.logging import Loki
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.database import InfluxDB

with Diagram('IoT', show=True, direction='TB', filename='architecture'):
    with Cluster('IoT Gateway'):
        fluentd = Fluentd()
        telegraf = Custom('metrics', 'telegraf.png')
        theengs = Custom('ble2mqtt', 'theengs.png')
        chrony = Custom('ntp', 'chrony.png')
        mosquitto = Custom('local mqtt broker', 'mosquitto.png')

    with Cluster('Mother'):
        loki = Loki()
        grafana = Grafana('dashboard')
        influxdb = InfluxDB('database')
        mosquitto2 = Custom('mqtt broker', 'mosquitto.png')

    fluentd >> loki
    grafana << [ loki, influxdb ]
    [ theengs, telegraf ] >> mosquitto
    mosquitto >> mosquitto2
