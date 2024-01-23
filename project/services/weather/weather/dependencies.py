from functools import lru_cache

import paho.mqtt.client as mqtt

from weather.models import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_mqtt():
    settings = get_settings()
    client = mqtt.Client(client_id="kpi_weather_service", userdata=None)  #, protocol=paho.MQTTv5)
    client.username_pw_set(settings.mqtt_username, settings.mqtt_password)
    client.connect(settings.mqtt_broker, settings.mqtt_port)

    return client
