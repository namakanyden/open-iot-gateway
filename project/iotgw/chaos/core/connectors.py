from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from core import Settings

import logging
import uvicorn
import os

from core.device_monitor import DeviceMonitor


def create_usb(config: Settings) -> DeviceMonitor:
    config.config_logger("usb")
    return DeviceMonitor("usb")


def create_http(config: Settings) -> FastAPI:
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = config.logger_formatter
    log_config["formatters"]["default"]["fmt"] = config.logger_formatter

    return FastAPI()


def create_mqtt(config: Settings) -> FastMQTT:
    mqtt_config = MQTTConfig(
        host=config.mqtt_host,
        port=config.mqtt_port,
        ssl=config.mqtt_ssl,
        keepalive=config.mqtt_keepalive,
        username=config.mqtt_username,
        password=config.mqtt_password
    )

    config.config_logger("mqtt")
    logger = logging.getLogger("mqtt")

    try:
        mqtt = FastMQTT(config=mqtt_config, mqtt_logger=logging.getLogger("mqtt"))
    except Exception:
        logger.critical("Unable to connect to broker.")
        os._exit(1)

    return mqtt
