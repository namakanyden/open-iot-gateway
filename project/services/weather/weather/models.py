from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: str | None = None
    city: str
    mqtt_broker: str
    mqtt_port: int = 1883
    mqtt_username: str | None = None
    mqtt_password: str | None = None
