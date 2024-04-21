from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from core import Settings

import logging
import uvicorn

from core.device_monitor import DeviceMonitor


def config_logger(logger_name, config):
    # Configure the logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Create a handler and set its formatter
    handler = logging.StreamHandler()
    formatter = logging.Formatter(config.logger_formatter)
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)


def create_usb(config: Settings) -> DeviceMonitor:
    config_logger("usb", config)
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

    config_logger("mqtt", config)
    return FastMQTT(config=mqtt_config, mqtt_logger=logging.getLogger("mqtt"))
