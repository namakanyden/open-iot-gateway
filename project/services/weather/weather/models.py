from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    token: str | None = None
    city: str
    mqtt_broker: str
    mqtt_port: int = 1883
    mqtt_username: str | None = None
    mqtt_password: str | None = None
    update_interval: int = 20 * 60

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_prefix='weather_'
    )
