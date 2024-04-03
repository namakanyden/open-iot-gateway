from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from core import Settings

import logging
import uvicorn

from core.device_monitor import DeviceMonitor


def create_usb() -> DeviceMonitor:
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

    # Configure the logger
    mqtt_logger = logging.getLogger("mqtt")
    mqtt_logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG

    # Create a handler and set its formatter
    handler = logging.StreamHandler()
    formatter = logging.Formatter(config.logger_formatter)
    handler.setFormatter(formatter)

    # Add the handler to the logger
    mqtt_logger.addHandler(handler)

    return FastMQTT(config=mqtt_config, mqtt_logger=mqtt_logger)
