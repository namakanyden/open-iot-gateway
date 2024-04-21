import http
import json

import httpx
import pendulum
from fastapi import FastAPI, HTTPException
from fastapi_mqtt import MQTTConfig, FastMQTT
from fastapi_restful.tasks import repeat_every
from loguru import logger
from paho.mqtt.publish import single

from weather.dependencies import get_settings
from weather.models import Settings
from weather.mqtt import MQTTClient

URL = 'https://api.openweathermap.org/data/2.5/weather'
TOPIC = 'services/weather/{city}'

settings = get_settings()
app = FastAPI()
mqtt_config = MQTTConfig(
    host=settings.mqtt_broker,
    username=settings.mqtt_username,
    password=settings.mqtt_password
)

mqtt = FastMQTT(config=mqtt_config, client_id='mirek')
mqtt.init_app(app)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    logger.info(f"Connected: {client} {flags} {rc} {properties}")


# @mqtt.on_message()
# async def message(client, topic, payload, qos, properties):
#     print("Received message: ",topic, payload.decode(), qos, properties)
#     return 0


def retrieve_weather_data(settings: Settings) -> dict:
    params = {
        'q': settings.city,
        'units': 'metric',
        'appid': settings.token,
        'lang': 'en'
    }

    response = httpx.get(URL, params=params)
    if response.status_code != http.HTTPStatus.OK:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    data = response.json()
    dt = pendulum.from_timestamp(data['dt'])
    logger.info(f'Weather data retrieved for {data['name']} at {dt.to_iso8601_string()}')

    return data


def publish_weather_data(settings: Settings, data: dict) -> None:
    topic = TOPIC.format(city=settings.city.lower())
    logger.info(f'Publishing weather to topic {topic}')
    mqtt.publish(topic, json.dumps(data), qos=2, retain=True)


    # single(topic=topic, payload=json.dumps(data), qos=2, retain=True,
    #        hostname=settings.mqtt_broker, client_id='mirek',
    #        auth={
    #            'username': settings.mqtt_username,
    #            'password': settings.mqtt_password
    #        }
    #        )
    # with MQTTClient(settings.mqtt_broker,
    #                 username=settings.mqtt_username, password=settings.mqtt_password) as mqtt:
    #     logger.info(f'Publishing weather to topic {topic}')
    #     mqtt.publish(topic, json.dumps(data), qos=2, retain=True)
    #     # logger.info(f'xxxxx')


@app.on_event("startup")
@repeat_every(seconds=get_settings().update_interval)
def cron() -> None:
    try:
        settings = get_settings()
        data = retrieve_weather_data(settings)
        publish_weather_data(settings, data)
    except HTTPException as e:
        logger.error('Weather data were not retrieved.')
        logger.error(f'HTTP Status Code: {e.status_code}')
        logger.error(e.detail)
