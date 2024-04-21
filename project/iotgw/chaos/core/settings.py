from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

import logging


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='chaos_')

    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_keepalive: int = 60
    mqtt_username: Optional[str] = None
    mqtt_password: Optional[str] = None
    mqtt_ssl: bool = False

    uvicorn_host: str = "localhost"
    uvicorn_port: int = 5000

    log_level: str = "DEBUG"

    logger_formatter: str = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Configure the logger
        logger = logging.getLogger("chaos")
        logger.setLevel(logging.getLevelName(self.log_level))

        # Create a handler and set its formatter
        handler = logging.StreamHandler()
        formatter = logging.Formatter(self.logger_formatter)
        handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(handler)

        for key, value in self.model_dump():
            logger.info(f"{key}: {value}")
            
