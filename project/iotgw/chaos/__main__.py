from core.connectors import *

import uvicorn

config = Settings()

http = create_http(config)
mqtt = create_mqtt(config)
usb = create_usb(config)

mqtt.init_app(http)

# Load services
from services import *

uvicorn.run("__main__:http", host=config.uvicorn_host, port=config.uvicorn_port)
