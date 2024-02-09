import paho.mqtt.client as mqtt


# TODO: Get config
class DecoratedMQTTClient:
    def __init__(self):
        self.callbacks = []
        self.mqtt_client = mqtt.Client()

        self.mqtt_client.on_connect = self.__on_connect
        self.mqtt_client.on_message = self.__on_message

        self.mqtt_client.username_pw_set("", "")
        self.mqtt_client.connect("127.0.0.1", 1883, 60)

        print("Client connected!")

    def message(self, func):
        # register function
        self.callbacks.append(func)
        print(f"{func.__name__}() is registred!")

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(f"On message in function {func.__name__}")
            return result

        return wrapper

    def __on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code: {rc}")
        client.subscribe("topic/+")

    def __on_message(self, client, userdata, msg):
        print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

        for func in self.callbacks:
            func()


