import logging

from __main__ import usb
from __main__ import mqtt

logger = logging.getLogger("usb")


def device_info(device):
    for attr in list(vars(device.context)):
        logger.debug(attr)


@usb.connect
def print_connect_message(device):
    logger.critical("USB Device connected...")
    logger.debug(device_info(device))
    mqtt.publish("gateway/chaos/device-manager", f"connected {device.device_path}")


@usb.disconnect
def print_disconnect_message(device):
    logger.critical("USB Device disconnected...")
    logger.debug(device_info(device))
    mqtt.publish("gateway/chaos/device-manager", f"disconnected {device.device_path}")
