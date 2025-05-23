import contextlib
import typing

import redis

from controllers.template import TemplateController
from schemas.schemas_cadastre import RecordCadastre, QueueCadastre


class RedisController(TemplateController):
    """
    Redis Controller
    """
    host: str
    port: int
    db:int

    _redis_client: redis.Redis | None = None

    def __init__(self, host: str = '127.0.0.1', port: int = 6379, db: int = 0):
        self.host = host
        self.port = port
        self.db = db
        # self.__redis = redis_broker.Redis(host=host, port=port)

    @contextlib.contextmanager
    def _session_redis(self):
        session = redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True)
        yield session
        session.save()
        session.close()

    # def get_all_keys(self):
    #     with redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True) as redis_client:
    #         keys = redis_client.keys()
    #     return keys

    # добавление записи
    def add_json_record(self, pk: str, record: RecordCadastre) -> None:
        with self._session_redis() as self._redis_client:
            self._add_json_record(pk=pk, record=record)

    def get_json_record(self, pk: str) -> dict[str:typing.Any]:
        with self._session_redis() as self._redis_client:
            record = self._redis_client.json().get(name=pk)
        return record

    def get_queue_topic(self, topic: str, start: int = 0, end: int = -1) -> list[str]:
        with self._session_redis() as self._redis_client:
            queue = self._get_queue(topic=topic, start=start, end=end)
        return queue

    def add_queue_topic(self, topic: str, pk: str) -> int:
        with self._session_redis() as self._redis_client:
            return self._add_element_queue(topic=topic, value=pk)

    def get_len_queue_topic(self, topic: str) -> int:
        return len(self._get_queue(topic=topic))

    def move_element(self, topic: str, new_index: int, name_key: str, direction:str='before', ):
        """
        Перемещаем элемент
        :param key:
        :param topic:
        :param new_index:
        :param direction:
        :return:
        """
        with self._session_redis() as self._redis_client:
            # Находим какой элемент нам нужен
            old_index =
            # Вставляем наш элемент
            self._insert_element(topic=topic, index=new_index, value=name_key, direction=direction)
            # Удаляем старую копию


    def _insert_element(self, topic: str, index: int, value: str, direction:str='before'):
            self._redis_client.linsert(name=topic,where=direction, refvalue=index,value=value )

    def _remove_element(self,topic:str, key, count ):
        self._redis_client.lrem(key=topic, count=, value=value)



    def _pop_element(self, topic: str, index: int)-> str:
            self._redis_client.lpop(name=topic, count=1)


        # переместить значение:
        # способ 1 - Удаляем вставляем нужный элемент в нужную позицию

    def move_up_element(self, topic: str, new_index: int, old_index: int):
        queue_element = self.get_queue(topic=topic, start=new_index, end=old_index)
        # переместить значение:
        # способ 2 - перемещаем нужное значение в начало списка, после перезапись всего отрезка
        queue_element = [queue_element[-1]] + queue_element[:-1]
        for i, element in enumerate(queue_element, new_index):
            self._set_value_to_element(topic=topic, index=i, updated_value=element)



    # -----

    def _get_queue(self, topic: str, start: int = 0, end: int = -1) -> list[str]:
        return self._redis_client.lrange(topic, start, end)

    def _add_json_record(self, pk: str, record: RecordCadastre):
        # with redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True) as redis_client:
        #     redis_client.json().set(pk, ".", record.model_dump())
        self._redis_client.json().set(pk, ".", record.model_dump())

    def _add_element_queue(self, topic: str, value: str) -> int:
        self._redis_client.rpush(topic, value)
        return self.get_len_queue_topic(topic=topic)
    #

    #
    #     def get_queue_topic(self, topic: str, start: int = 0, end: int = -1) -> list[str]:
    #         # with redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True) as redis_client:
    #         #     return redis_client.lrange(topic, start, end)
    #         return self._redis_client.lrange(topic, start, end)
    #

#
#
#
#
# # ---------------->
#     def add_first_element_queue(self, topic: str, value: str):
#         with redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True) as redis_client:
#             redis_client.rpush(topic, value)
#
#             # redis_client.rpush(topic, 'dobavili')
#             # redis_client.lset(topic, 1, 'updated_value2')
#             # print(redis_client.lrange(topic, 0, -1))  # Вывод: [b'value1', b'updated_value2', b'value3']
#
#     def get_first_element_queue(self, topic: str) -> str:
#         with redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True) as redis_client:
#             return redis_client.lpop(topic)
#
#     # Добавить открытый метод для получения всей очереди


#
#     def get_len_queue(self, topic: str) -> int:
#         return len(self.get_queue(topic=topic))
#
#     def _set_value_to_element(self, topic: str, index: int, updated_value: str):
#         with redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True) as redis_client:
#             redis_client.lset(topic, 1, updated_value)
#
#
#     def _insert_element(self, topic: str, index: int, value: str, direction:str='before'):
#         with redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True) as redis_client:
#             redis_client.linsert(name=topic,where=direction, pivot=index,value=value )
#
#     def _pop_element(self, topic: str, index: int,)-> str:
#         with redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True) as redis_client:
#             redis_client.lpop(name=topic, count=1)
#
#     def move_element(self, topic: str, new_index: int, old_index: int, direction:str='before'):
#         # переместить значение:
#         # способ 1 - Удаляем вставляем нужный элемент в нужную позицию
#
#     def move_up_element(self, topic: str, new_index: int, old_index: int):
#         queue_element = self.get_queue(topic=topic, start=new_index, end=old_index)
#         # переместить значение:
#         # способ 2 - перемещаем нужное значение в начало списка, после перезапись всего отрезка
#         queue_element = [queue_element[-1]] + queue_element[:-1]
#         for i, element in enumerate(queue_element, new_index):
#             self._set_value_to_element(topic=topic, index=i, updated_value=element)
#
#     def get_new_new_index_by_topic(self, topic:str)->int:
#         # Формирование уникального индекса:
#         # Храним максимально возможный индекс
#         # При получении нового индекса - плюсуем его.
#
#         with self._session_redis() as self._redis_client:
#             self._redis_client.se


# def get_last_element(self, ):
#     with redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True) as redis_client:
#         redis_client.lmove(name=topic)

# Получение последней записи

# def get_record(self) -> RecordCadastre:
#     pass
#     # Изменить номер в очереди
#
# def change_queue_number(self, number, record):
#     pass

# -----------------------------------
