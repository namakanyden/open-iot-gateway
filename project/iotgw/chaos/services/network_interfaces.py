import time

import sh

from __main__ import mqtt
import asyncio
import logging
import json

logger = logging.getLogger("mqtt")


def get_sleep_time(payload):
    try:
        payload_dict = json.loads(payload.decode())
        return payload_dict.get("t", None)
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
        logger.warning(f"Invalid time, skipping request.")
        return

    logger.info(f"Disabling network interface {network_interface}.")

    try:
        sh.ifconfig(network_interface, "down")
    except (sh.ErrorReturnCode_255, sh.ErrorReturnCode_1):
        logger.error(f"Network interface '{network_interface}' does not exist.")
    else:
        await asyncio.sleep(sleep_time)
        sh.ifconfig(network_interface, "up")
        await asyncio.sleep(10)
        logger.info(f"Network interface {network_interface} is enabled again.")


@mqtt.subscribe("gateway/chaos/internet/set")
async def disable_internet(client, topic, payload, qos, properties):
    await asyncio.sleep(5)
    logger.error("Not implemented.")
    await asyncio.sleep(10)
    logger.debug("Hello")


@mqtt.subscribe("gateway/chaos/ethernet/set")
async def disable_eth0(client, topic, payload, qos, properties):
    logger.debug(f"Received message to specific topic: {topic} {payload.decode()} {qos} {properties}")
    await disable_network_interface("eth0", get_sleep_time(payload))


@mqtt.subscribe("gateway/chaos/wireless/set")
async def disable_wn0(client, topic, payload, qos, properties):
    logger.debug(f"Received message to specific topic: {topic} {payload.decode()} {qos} {properties}")
    await disable_network_interface("wn0", get_sleep_time(payload))
