from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class RabbitMQSettings(BaseSettings):
    """Rabbit MQ settings."""

    broker_host: str = Field(description="RabbitMQ broker host")
    broker_port: int = Field(description="RabbitMQ broker port")
    broker_login: str = Field(description="RabbitMQ broker login")
    broker_password: str = Field(description="RabbitMQ broker password")
    broker_cadaster_queue: str = Field(description="RabbitMQ cadastre queue name")
    broker_url: str = Field(description="RabbitMQ broker URL", alias="rabbitmq_broker_url")


class APIs(BaseSettings):
    """APIs settings."""

    billing_cadastre_url: str = Field(description="Billing API cadastre URL")


class DataBase(BaseSettings):
    """Database settings."""

    db_user: str = Field(description="Database user")
    db_password: str = Field(description="Database password")
    db_host: str = Field(description="Database host")
    db_port: int = Field(description="Database port")
    db_database: str = Field(description="Database name")


class RedisSettings(BaseSettings):
    """Redis settings."""

    redis_host: str = Field(description="Redis host")
    redis_port: int = Field(description="Redis port")
    redis_db: int = Field(description="Redis database number")
    redis_password: str = Field(description="Redis password")


class CelerySettings(BaseSettings):
    """Celery settings."""

    broker_url: str = Field(description="Celery broker URL", alias="celery_broker_url")
    result_backend: str = Field(description="Celery result backend", alias="celery_result_backend")


class Settings(BaseSettings):
    """Base Settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", populate_by_name=True)

    rabbit_mq: RabbitMQSettings = Field(default_factory=RabbitMQSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    api: APIs = Field(default_factory=APIs)
    database: DataBase = Field(default_factory=DataBase)
    celery: CelerySettings = Field(default_factory=CelerySettings)


settings_app = Settings()
