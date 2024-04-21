import logging

from __main__ import usb
from __main__ import mqtt

logger = logging.getLogger("usb")


@usb.connect
def print_connect_message(device):
    logger.critical("USB Device connected...")
    mqtt.publish("gateway/chaos/device-manager", "connected")
    logger.debug(device)


@usb.disconnect
def print_disconnect_message(device):
    logger.critical("USB Device disconnected...")
    mqtt.publish("gateway/chaos/device-manager", "disconnected")
    logger.debug(device)
