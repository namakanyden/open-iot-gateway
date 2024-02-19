import json
from device_monitor import DeviceMonitor
from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
import uvicorn


# TODO: Load logger
# FAST API LOGGER

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print("Error: Config not found")
    except json.JSONDecodeError as e:
        print("Error: Decoding")
    except Exception as e:
        print("Error: Config")


# TODO: Check required binaries

# TODO: Check required scripts

config = load_config("./config.json")

if __name__ == "__main__":
    uvicorn.run("main:rest", host=config["uvicorn_host"], port=config["uvicorn_port"], log_level="info")

mqtt_config = MQTTConfig(
    host=config["mqtt_host"],
    port=config["mqtt_port"],
    keepalive=config["mqtt_keep_alive"],
    username=config["mqtt_username"],
    password=config["mqtt_password"],
)

rest = FastAPI()
mqtt = FastMQTT(config=mqtt_config)
usb = DeviceMonitor("usb")

mqtt.init_app(rest)

# Load services
from services import *

# TODO: on_exit signal
