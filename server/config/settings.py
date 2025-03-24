"""
Settings module for Server application.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# TODO: generare .env di esempio completo con tutti i parametri

class AppConfiguration(BaseSettings):
    drawer_button: str = Field('primary', alias='APP_DRAWER_BTN')
    eraser_button: str = Field('secondary', alias='APP_ERASER_BTN')
    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=True,
        extra='ignore'
    )

class LoggingConfiguration(BaseSettings):
    level: str = Field('INFO', alias='LOG_LEVEL')
    pattern: str = Field('%(asctime)s - %(name)s - %(levelname)s - %(message)s', alias='LOG_PATTERN')
    date_format: str = Field('%Y-%m-%d %H:%M:%S', alias='LOG_DATE_FORMAT')
    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=True,
        extra='ignore'
    )

class RedisConfiguration(BaseSettings) :
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(6379, alias="REDIS_PORT")
    expiration_time: int = Field(3600000, alias="REDIS_EXPIRATION_TIME") # in millis
    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=True,
        extra='ignore'
    )

class WebServerConfiguration(BaseSettings) :
    port: int = Field(5000, alias='WEBS_PORT')
    cors_allowed_origins: str = Field('*', alias='WEBS_CORS_ALLOWED_ORIGINS')
    templates_path: str = Field('../resources/templates', alias="WEBS_TEMPLATES_PATH")
    statics_path: str = Field('../resources/static', alias="WEBS_STATICS_PATH")
    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=True,
        extra='ignore'
    )

class ServerConfiguration(BaseSettings):
    app: AppConfiguration = Field(default_factory=AppConfiguration)
    logging: LoggingConfiguration = Field(default_factory=LoggingConfiguration)
    redis: RedisConfiguration = Field(default_factory=RedisConfiguration)
    webserver: WebServerConfiguration = Field(default_factory=WebServerConfiguration)
    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=True,
        extra='ignore'
    )
server_config = ServerConfiguration()

__all__ = [
    'server_config'
]
    