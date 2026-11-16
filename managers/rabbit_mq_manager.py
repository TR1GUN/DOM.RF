from controllers.rabbit_mq_controller import RabbitMQControllerConsumer, RabbitMQControllerPublisher
from controllers.template import BaseController
from settings.settings import settings_app


class _RabbitMQManager:
    _controller: BaseController
    _topic: str


class PublisherManager(_RabbitMQManager):
    topic = "cadastre"
    _controller: RabbitMQControllerPublisher

    def __init__(self, topic="cadastre"):
        self._controller = RabbitMQControllerPublisher(
            host=settings_app.rabbit_mq.broker_host,
            port=settings_app.rabbit_mq.broker_port,
            login=settings_app.rabbit_mq.broker_login,
            password=settings_app.rabbit_mq.broker_password,
        )
        self._topic = topic

    def send_message(self, message: str, priority: int = 10):
        self._controller.send_message(topic=self._topic, message=message, priority=priority)


class ConsumerManager(_RabbitMQManager):
    topic = "cadastre"
    _controller: RabbitMQControllerConsumer

    def __init__(self, topic="cadastre"):
        self._controller = RabbitMQControllerConsumer(
            host=settings_app.rabbit_mq.broker_host,
            port=settings_app.rabbit_mq.broker_port,
            login=settings_app.rabbit_mq.broker_login,
            password=settings_app.rabbit_mq.broker_password,
        )
        self._topic = topic

    def read_message(self, message: dict):
        self._controller.accept_message(topic=self._topic, message=message)
