# TODO: Load logger

# TODO: Load env values

# TODO: Load config values

# TODO: Check required binaries

# TODO: Check required scripts

# Load core
from core import core

# TODO: on_exit signal

# Load services
from services import *

# Start MQTT client loop
core.mqtt_client.loop_forever()
