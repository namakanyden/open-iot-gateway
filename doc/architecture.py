#!/usr/bin/env python3

from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.logging import Loki
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.database import InfluxDB

with Diagram('IoT', show=True, direction='TB'):
    with Cluster('IoT Gateway'):
        fluentd = Fluentd()
        telegraf = Custom('metrics', 'icons/telegraf.png')
        theengs = Custom('ble2mqtt', 'icons/theengs.png')
        chrony = Custom('ntp', 'icons/chrony.png')
        mosquitto = Custom('local mqtt broker', 'icons/mosquitto.png')

    with Cluster('Mother'):
        loki = Loki()
        grafana = Grafana('dashboard')
        influxdb = InfluxDB('database')
        mosquitto2 = Custom('mqtt broker', 'icons/mosquitto.png')

    fluentd >> loki
    grafana << [ loki, influxdb ]
    [ theengs, telegraf ] >> mosquitto
    mosquitto >> mosquitto2
