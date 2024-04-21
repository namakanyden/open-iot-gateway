import time

import sh

from __main__ import mqtt
import asyncio
import logging

logger = logging.getLogger("mqtt")


def get_sleep_time(payload):
    try:
        return int(payload.decode()["t"])
    except KeyError:
        logger.error("Parameter t in payload missing.")
    except ValueError:
        logger.error("Parameter t expects integer value.")
    except Exception as err:
        logger.error(f"Exception: {err}")


async def disable_network_interface(network_interface, sleep_time):
    logger.info(f"Disabling network interface {network_interface}.")

    try:
        sh.ifconfig(network_interface, "down")
    except sh.ErrorReturnCode_255:
        logger.error(f"Error: Network interface '{network_interface}' does not exist.")
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
