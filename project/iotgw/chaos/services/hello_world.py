from main import mqtt
import asyncio


@mqtt.subscribe("my/mqtt/topic/#")
async def hello_world(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    await asyncio.sleep(5)
    print("Done!")
