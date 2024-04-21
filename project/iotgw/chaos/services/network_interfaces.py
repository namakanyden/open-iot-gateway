import time

import sh

from __main__ import mqtt
import asyncio
import logging

logger = logging.getLogger("mqtt")


def get_sleep_time(payload):
    try:
        return int(dict(payload.decode())["t"])
    except KeyError:
        logger.warning("Parameter t in payload missing.")
        return 0
    except ValueError:
        logger.warning("Parameter t expects integer value.")
        return 0
    except Exception as err:
        logger.warning(f"Exception: {err}")
        return 0


async def disable_network_interface(network_interface, sleep_time):
    if sleep_time <= 0:
        logger.info(f"Invalid time, skipping request.")
        return

    logger.info(f"Disabling network interface {network_interface}.")

    try:
        sh.ifconfig(network_interface, "down")
    except sh.ErrorReturnCode_255:
        logger.error(f"Network interface '{network_interface}' does not exist.")
    else:
        await asyncio.sleep(sleep_time)
        sh.ifconfig(network_interface, "up")
        logger.info(f"Network interface {network_interface} is enabled again.")


@mqtt.subscribe("gateway/chaos/internet/set")
async def disable_internet(client, topic, payload, qos, properties):
    logger.info(f"Received message to specific topic: {topic} {payload.decode()} {qos} {properties}")
    await asyncio.sleep(5)
    logger.info("server")


@mqtt.subscribe("gateway/chaos/ethernet/set")
async def disable_eth(client, topic, payload, qos, properties):
    logger.debug(f"Received message to specific topic: {topic} {payload.decode()} {qos} {properties}")
    await disable_network_interface("eth0", get_sleep_time(payload))


@mqtt.subscribe("gateway/chaos/wireless/set")
async def disable_wn(client, topic, payload, qos, properties):
    logger.debug(f"Received message to specific topic: {topic} {payload.decode()} {qos} {properties}")
    await disable_network_interface("wn0", get_sleep_time(payload))
