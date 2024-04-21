import logging
import json

from __main__ import usb
from __main__ import mqtt

logger = logging.getLogger("usb")


def log_device_info(device):
    for key, value in device.items():
        logging.debug(f"{key}: {value}")


@usb.connect
def print_connect_message(device):
    logger.critical("USB Device connected...")
    log_device_info(device)
    mqtt.publish("gateway/chaos/device-manager", f"{json.dumps(dict(device))}")


@usb.disconnect
def print_disconnect_message(device):
    logger.critical("USB Device disconnected...")
    log_device_info(device)
    mqtt.publish("gateway/chaos/device-manager",  f"{json.dumps(dict(device))}")
