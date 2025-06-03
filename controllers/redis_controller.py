import contextlib
import typing

import redis

from controllers.template import BaseController
from schemas.schemas_cadastre import RecordCadastre, QueueCadastre, RecordCadastreInRedis


class RedisController(BaseController):
    """
    Redis Controller
    """
    # _host: str
    # _port: int
    _db: int

    _redis_client: redis.Redis | None = None

    def __init__(self, host: str = '127.0.0.1', port: int = 6379, db: int = 0):
        self._host = host
        self._port = port
        self._db = db

    @contextlib.contextmanager
    def _session_redis(self):
        session = redis.Redis(host=self._host, port=self._port, db=self._db, decode_responses=True)
        yield session
        session.save()
        session.close()

    def add_json_record(self, pk: str, record: dict[str, typing.Any]) -> None:
        """
        Added json(dict) record in Storage
        :param pk:
        :param record:
        :return:
        """
        with self._session_redis() as self._redis_client:
            self._redis_client.json().set(pk, ".", record)

    def get_json_record(self, pk: str) -> dict[str:typing.Any]:
        """
        Получаем JSON запись из хранилища
        :param pk:
        :return:
        """
        with self._session_redis() as self._redis_client:
            record = self._redis_client.json().get(name=pk)
        return record

    def edit_json_record(self, pk: str, record: RecordCadastre):
        """
        Изменяем JSON запись из хранилища
        :param pk:
        :param record:
        :return:
        """
        with self._session_redis() as self._redis_client:
            record = self._redis_client.json().set(pk, ".", record.model_dump())
        return record

    def delete_json_record(self, pk: str):
        """
        Удаляем запись
        :param pk:
        :return:
        """
        with self._session_redis() as self._redis_client:
            record = self._redis_client.json().delete(key=pk)
        return record

    def add_key_topic_in_set(self, topic: str, value: str):
        """
        Добавление уникального ключа в очереди
        :param topic:
        :param value:
        :return:
        """
        with self._session_redis() as self._redis_client:
            # для сетов
            self._redis_client.sadd(name=topic, *value)

    def get_keys_topic_in_set(self, topic: str) -> int:
        """
        знаем длину через измерение общей длины
        :param topic:
        :return:
        """
        with self._session_redis() as self._redis_client:
            # Узнаем длину через измерение общей длины
            return self._redis_client.scard(name=topic)
            # len_queue = len(queue)
            # return len_queue

    def add_element_in_queue_topic(self, topic: str, value: str) -> int:
        """
        Добавляем в очередь первичный ключ
        :param topic:
        :param value:
        :return:
        """
        with self._session_redis() as self._redis_client:
            self._redis_client.rpush(name=topic, *value)
            return self._redis_client.llen(name=topic)

    def get_elements_in_in_queue_topic(self, topic: str, start: int = 1, end: int = -1) -> list[str]:
        """
        Получаем срез очереди
        :param topic:
        :param start:
        :param end:
        :return:
        """
        with self._session_redis() as self._redis_client:
            queue = self._get_queue(topic=topic, start=start - 1, end=end)
        return queue

    def find_index_element_in_queue_topic(self, topic: str, key: str) -> int:
        """
        Поиск индекса элемента
        :param topic:
        :param key:
        :return:
        """
        with self._session_redis() as self._redis_client:
            index = self._redis_client.lpos(name=topic, value=key)
        return index

    def move_element(self, topic: str, new_index: int, value: str,
                     direction: typing.Literal["BEFORE", "AFTER", "before", "after"] = 'before', ):
        """
        Перемещаем элемент
        :param value:
        :param topic:
        :param new_index:
        :param direction:
        :return:
        """
        with self._session_redis() as self._redis_client:
            # Теперь - у нас несколько путей:
            # Путь первый - Удалить элемент из очереди и вставить в нужное место
            # Путь второй - Изменить по элементарно каждый элемент
            # Путь третий - Взять массив, переместить элемент в нужное значение и перезаписать последовательность.

            # Путь первый
            # Находим какой элемент нам нужен
            old_index = self._redis_client.lpos(name=topic, value=value)
            # Удаляем
            self._redis_client.lrem(name=topic, count=old_index, value=value)
            # Получаем значение элемента
            element = self._redis_client.lindex(name=topic, index=new_index)
            # Вставляем в нужный элемент
            self._redis_client.linsert(name=topic, where=direction, refvalue=element, value=value)

            # # Путь второй
            # # Берем последовательность элементов которую надо изменить
            # # Начальный элемент
            # old_index = self._redis_client.lpos(name=topic, value=value)
            # queue_elements = self._get_queue(topic=topic, start=new_index - 1, end=old_index)
            #
            # new_queue = [queue_elements[-1]] + queue_elements[:-1]
            # for i, element in enumerate(new_queue, new_index - 1):
            #     self._redis_client.lset(topic, i, element)
            #
            # # Путь третий
            # # берем срез очереди - От начала до нашего элемента
            # old_index = self._redis_client.lpos(name=topic, value=value)
            # queue_elements = self._get_queue(topic=topic, start=0, end=old_index)
            # # формируем новую очередь
            # new_queue = queue_elements[:new_index] + [queue_elements[-1]] + queue_elements[new_index:-1]
            # # Обрезаем очередь
            # self._redis_client.ltrim(name=topic, start=0, end=old_index)
            # # Вставляем нужные значения
            # self._redis_client.lpush(name=topic, *new_queue)

    def first_record_in_queue(self, topic:str) -> RecordCadastreInRedis:
        """
        Получаем первую очередь в очереди
        :return:
        """
        with self._session_redis() as self._redis_client:
            key = self._redis_client.lpop(name=topic)
            record = self._redis_client.json().get(name=key)
        return record

    def reset_index_queue(self, topic:str):
        """
        Сброс значений в очереди
        :param topic:
        :return:
        """
        with self._session_redis() as self._redis_client:
            len_set_keys = self._redis_client.smembers(name=topic)
            self._redis_client.srem(name=topic,*len_set_keys )

    def get_len_queue_topic(self, topic:str) -> int:
        with self._session_redis() as self._redis_client:
            return self._redis_client.smembers(name=topic)


    def _get_queue(self, topic: str, start: int = 0, end: int = -1) -> list[str]:
        return self._redis_client.lrange(topic, start, end)

            # queue_element = [queue_element[-1]] + element[:-1]
            #
            # for i, element in enumerate(queue_element, new_index):
            #     self._redis_client.lset(topic, 1, updated_value)

            # Путь третий

            # self._redis_client.lpop(name=topic, count=old_index, value=name_key)
            # Находим какой элемент нам нужен
            # old_index = self._redis_client.lpos(name=topic,value=name_key)
            # # Удаляем
            # self._redis_client.srem(name=topic, count=old_index, value=name_key)
            #
            # # Вставляем наш элемент
            # self._redis_client.sadd(name=topic,)1

            # self._redis_client.sadd(name=topic,where=direction, refvalue=index,value=value)

    # ------------------------
    # Путь первый - изменить по элементарно каждый элемент
    # def _change_elements(self):
    #     """
    #     Изменить по элементарно каждый элемент в очереди
    #     :return:
    #     """
    #     # Взять отрезок который необходимо изменить
    #
    #     # Перезапись значений в этом отрезке


    #
    # def get_len_queue_topic(self, topic: str) -> int:
    #     return len(self._get_queue(topic=topic))
    #
    # def _insert_element(self, topic: str, index: int, value: str, direction: str = 'before'):
    #     self._redis_client.linsert(name=topic, where=direction, refvalue=index, value=value)
    #
    # def _remove_element(self, topic: str, index: int):
    #     """
    #     Удалить элемет
    #     :param topic:
    #     :param index:
    #     :return:
    #     """
    #     self._redis_client.ltrim(name=topic, start=index, end=0)
    #
    # # def get_all_keys(self):
    # #     with redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True) as redis_client:
    # #         keys = redis_client.keys()
    # #     return keys
    #
    # def _pop_element(self, topic: str, index: int) -> str:
    #     self._redis_client.lpop(name=topic, count=1)
    #
    # # переместить значение:
    # # способ 1 - Удаляем вставляем нужный элемент в нужную позицию
    #
    # def move_up_element(self, topic: str, new_index: int, old_index: int):
    #     queue_element = self.get_queue(topic=topic, start=new_index, end=old_index)
    #     # переместить значение:
    #     # способ 2 - перемещаем нужное значение в начало списка, после перезапись всего отрезка
    #     queue_element = [queue_element[-1]] + queue_element[:-1]
    #     for i, element in enumerate(queue_element, new_index):
    #         self._set_value_to_element(topic=topic, index=i, updated_value=element)
    #
    # # -----
    #
    # def _get_queue(self, topic: str, start: int = 0, end: int = -1) -> list[str]:
    #     return self._redis_client.lrange(topic, start, end)
    #
    # # def _add_json_record(self, pk: str, record: RecordCadastre):
    # #     # with redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True) as redis_client:
    # #     #     redis_client.json().set(pk, ".", record.model_dump())
    # #     self._redis_client.json().set(pk, ".", record.model_dump())
    #
    # def _add_element_queue(self, topic: str, value: str) -> int:
    #     self._redis_client.rpush(topic, value)
    #     return self.get_len_queue_topic(topic=topic)
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
# import redis
#
# key = KEYS[0]
# item = ARGV[0]
# by = int(ARGV[1])
#
# if by is None or by == 0:
#     return
#
# r = redis.Redis()
#
# # Получаем наш весь список
# items = r.lrange(key, 0, -1)
# pos = None
#
# # Проходимся по списку
# for k, v in enumerate(items):
#     if v == item:
#         pos = k + by
#         pos = max(pos, 0)
#         pos = min(pos, len(items) - 1)
#         items.pop(k)
#         items.insert(pos, v)
#         break
#
# if pos is None:
#     return
#
# r.delete(key)
# for v in items:
#     r.rpush(key, v)
#
# return pos
