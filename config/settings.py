from pydantic import BaseModel, Field


class RabbitMQSettings(BaseModel):
    """
    Rabbit MQ settings
    """
    url: str = 'localhost'
    port: int = 5672
    login: str = 'guest'
    password:str = 'guest'
    cadaster_queue:str = 'cadastre'


class APIs(BaseModel):
    """
    APIs settings
    """
    billing_cadastre_url:str = 'cadastrebilling.ru'


class DataBase(BaseModel):
    """
    Database settings
    """
    user:str = ''
    password:str = ''


class RedisSettings(BaseModel):
    """
    Redis settings
    """
    # host:str ='localhost'
    host:str = '127.0.0.1'
    port:int = 6379
    db:int = 0


class Settings(BaseModel):
    """
    Base Settings
    """
    rabbit_mq: RabbitMQSettings = RabbitMQSettings()
    redis: RedisSettings = RedisSettings()
    api: APIs = APIs()
    database: DataBase = DataBase()


settings_app = Settings()
