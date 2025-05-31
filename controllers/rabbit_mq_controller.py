import time
import typing
import contextlib

from amqp.spec import Basic
from pika import ConnectionParameters, BlockingConnection, PlainCredentials, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
import pika

# from .errors import RabbitException
import time
from contextlib import contextmanager

from config import Settings

from controllers.template import BaseController


class RabbitMQControllerBase(BaseController):
    """
    Base class Rabbit MQ
    """
    _login: str = Settings.rabbit_mq.login
    _password: str = Settings.rabbit_mq.password

    _connection_params: ConnectionParameters

    _connection: BlockingConnection | None
    _channel: BlockingChannel | None

    _rabbit_client = None

    def __init__(self,
                 host: str = 'localhost',
                 port: int = 5672,
                 login: str | None = None,
                 password: str | None = None
                 ):
        self._host = host
        self._port = port
        if login and password:
            self._login = login
            self._password = password

    @contextlib.contextmanager
    def _session_rabbit(self):
        connection = BlockingConnection(parameters=self._connection_parameters())
        yield connection
        if connection.is_open:
            connection.close()

    @contextlib.contextmanager
    def _session_channel(self):
        with self._session_rabbit() as session:
            channel = session.channel()
            yield channel
            if channel.is_open:
                channel.close()

    def _connection_parameters(self) -> None:
        credentials: PlainCredentials = PlainCredentials(username=self._login, password=self._password)
        self._connection_params = ConnectionParameters(
            host=self._host,
            port=self._port,
            credentials=credentials
        )
        self._connection = None
        self._channel = None

    def get_connection(self) -> BlockingConnection:
        return BlockingConnection(self._connection_params)
    @property
    def channel_(self) -> BlockingChannel:
        if self._channel is None:
            raise Exception("Chanel is not exist!")
        return self._channel
    #
    # @contextmanager
    # def _session_rabbit(self):
    #     self._connection = self.get_connection()
    #     with self._connect_channel as ch:
    #         self._channel = ch
    #         yield self
    #
    #     if self._connection.is_open:
    #         self._connection.close()




    # # классический вариант
    # def __enter__(self):
    #     self._connection = BlockingConnection(self._connection_params)
    #     self._channel = self._connection.channel()
    #     return self
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     if self._channel.is_open:
    #         self._channel.close()
    #     if self._connection.is_open:
    #         self._connection.close()

    # вариант через метод
    # @contextmanager
    # def connect(self):
    #     self._connection = self.get_connection()
    #     with self._connect_channel as ch:
    #         self._channel = ch
    #         yield self
    #
    #     if self._connection.is_open:
    #         self._connection.close()

    # @contextmanager
    # def _connect_channel(self):
    #     _channel = self._connection.channel()
    #     yield _channel
    #
    #     if _channel.is_open:
    #         _channel.close()


class RabbitMQControllerPublisher(RabbitMQControllerBase):
    _exchange: str = ''
    # @create_queue
    def send_message(self, message: str, topic: str,priority:int=10) -> None:
        # log.info("Publish message %s", message_body)
        with self._session_channel() as self.channel:
            queue = self.channel.queue_declare(queue=topic)
            self.channel.basic_publish(
                exchange=self._exchange,
                routing_key=topic,
                body=message,
                properties=pika.BasicProperties(priority=priority)
        )

            # queue = self.channel.queue_declare(queue=topic)
            # self.channel.basic_publish(
            #     exchange=MQ_EXCHANGE,
            #     routing_key=topic,
            #     body=message,
            #     properties=pika.BasicProperties(priority=priority))

        print(f"Отпраивли сообщение {message} в топик {topic}")


def process_new_message(
        ch: "BlockingChannel",
        method: "Basic.Deliver",
        properties: "BasicProperties",
        body: bytes,
):
    """
    Обработчик сообщения
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    # print("наш канал", ch)
    # print("метод обработки", method)
    # print("properties: %s", properties)
    print("Тело сообшщения", body.decode())
    # Подтверждение обработки
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print('Обработали')
    key = body.decode()
    # Берем из редиса запись
    # record = Redis
    # Отправляем данные на расчет
    #
    # Фиксируем данные


class RabbitMQControllerConsumer(RabbitMQControllerBase):
    _exchange: str = ''

    # _callback = produce_message

    def accept_message(self, topic: str, process_new_message) -> None:
        with self._session_channel() as self.channel:
            self.channel.basic_consume(
                queue=topic,
                on_message_callback=process_new_message,
                # auto_ack=True,
            )
            self.channel.start_consuming()


# client = RabbitMQControllerPublisher(
#     host=Settings.rabbit_mq.host,
#     port=Settings.rabbit_mq.port,
#     login=Settings.rabbit_mq.login,
#     password=Settings.rabbit_mq.password
# )
#
# client2 = RabbitMQControllerConsumer(
#     host=Settings.rabbit_mq.host,
#     port=Settings.rabbit_mq.port,
#     login=Settings.rabbit_mq.login,
#     password=Settings.rabbit_mq.password
# )
# message = 'message cadastre - наше сообщение'
# topic = 'cadastre'
# client.send_message(topic=topic, message=message + '1')
# client.send_message(topic=topic, message=message + '2')
# client.send_message(topic=topic, message=message + '3', priority=2)
# time.sleep(2)
#
#
# client2.accept_message(topic=topic, process_new_message=process_new_message)
