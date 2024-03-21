from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
import uvicorn
import logging
from settings import Settings
from device_monitor import DeviceMonitor

if __name__ == "__main__":
    config = Settings()

    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = config.logger_formatter
    log_config["formatters"]["default"]["fmt"] = config.logger_formatter

    uvicorn.run("main:rest", host=config.uvicorn_host, port=config.uvicorn_port, log_config=log_config)
    exit()


config = Settings()
print(config.model_dump())

# Configure the logger
mqtt_logger = logging.getLogger("mqtt")
mqtt_logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG

# Create a handler and set its formatter
handler = logging.StreamHandler()
formatter = logging.Formatter(config.logger_formatter)
handler.setFormatter(formatter)
# Add the handler to the logger
mqtt_logger.addHandler(handler)

rest = FastAPI()
config = Settings()
print(config.mqtt_host)

mqtt_config = MQTTConfig(
    host=config.mqtt_host,
    port=config.mqtt_port,
    ssl=config.mqtt_ssl,
    keepalive=config.mqtt_keepalive,
    username=config.mqtt_username,
    password=config.mqtt_password
)

mqtt = FastMQTT(config=mqtt_config, mqtt_logger=mqtt_logger)
usb = DeviceMonitor("usb")

mqtt.init_app(rest)

# Load services
from services import *
