from controllers.rabbit_mq_controller import RabbitMQControllerConsumer, RabbitMQControllerPublisher
from controllers.template import BaseController
from config import Settings


class _RabbitMQManager:
    _controller: BaseController
    _topic:str


class PublisherManager(_RabbitMQManager):
    topic = 'cadastre'
    _controller: RabbitMQControllerPublisher

    def __init__(self, topic='cadastre'):
        self._controller = RabbitMQControllerPublisher(
            host=Settings.rabbit_mq.url,
            port=Settings.rabbit_mq.port,
            login=Settings.rabbit_mq.login,
            password=Settings.rabbit_mq.password
        )
        self._topic = topic

    def send_message(self, message: str, priority:int):
        self._controller.send_message(topic=self.topic, message=message, priority=priority)


class ConsumerManager(_RabbitMQManager):
    topic = 'cadastre'
    _controller: RabbitMQControllerConsumer

    def __init__(self, topic='cadastre'):
        self._controller = RabbitMQControllerConsumer(
            host=Settings.rabbit_mq.url,
            port=Settings.rabbit_mq.port,
            login=Settings.rabbit_mq.login,
            password=Settings.rabbit_mq.password
        )
        self._topic = topic

    def read_message(self, message: dict):
        self._controller.accept_message(topic=self.topic, message=message)
