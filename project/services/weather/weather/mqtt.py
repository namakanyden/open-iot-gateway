from loguru import logger
import paho.mqtt.client as mqtt


class MQTTClient(object):
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.debug("Connected to MQTT Broker!")
        else:
            logger.error(f"Failed to connect, return code {rc}")

    def __init__(self, broker, port=1883, username=None, password=None):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.client = mqtt.Client(client_id="kpiweatherservice", protocol=mqtt.MQTTv311, clean_session=True)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self.on_connect

    def __enter__(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.loop_stop()
        # self.client.loop()
