from __main__ import mqtt
import asyncio
import logging

logger = logging.getLogger("mqtt")

@mqtt.subscribe("gateway/chaos/disable/set")
async def disable_internet(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    await asyncio.sleep(5)
    logger.info("server")


@mqtt.subscribe("kpi/bed/chaos/disable/set")
async def disable_eth(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    await asyncio.sleep(5)
    print("Done!")


@mqtt.subscribe("my/mqtt/topic/y")
async def disable_wn(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    await asyncio.sleep(5)
    logger.info("server")
