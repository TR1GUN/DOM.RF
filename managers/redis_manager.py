from schemas.schemas_cadastre import RecordCadastre, CadastreNumber, CoordinateObject, PositionInQueue, QueueCadastre
from controllers import RedisController
from config import Settings


# Задачи Менеджера:

# Добавить новую запись в очередь +
# Получение записи +
# Редактирование записи +
# Удалить запись в очереди +

# Получение информации об очереди +
# Получение информации о записи в очереди +

# Получение первой записи в очереди +
# Переместить запись в очереди +


class RedisManager:
    """
    Redis Manager
    """
    _controller: RedisController
    _topic: str

    def __init__(self, topic='cadastre'):
        self._controller = RedisController(
            host=Settings.redis.host,
            port=Settings.redis.port,
            db=Settings.redis.db
        )
        self._topic = topic

    def add_record(self, record: RecordCadastre) -> PositionInQueue:
        """
        Добавление новой записи на расчет
        :param record:
        :return: Номерок, что выдают и Место в очереди
        """
        key = self._formation_of_new_primary_key()
        self._controller.add_json_record(pk=key, record=record)
        position_in_queue = self._controller.add_element_in_queue_topic(topic=self._topic, value=key)
        return PositionInQueue(position=position_in_queue, key=key, len_queue=position_in_queue)

    def get_record(self, key: str) -> RecordCadastre:
        """
        Получение записи по его значению.
        :param key:
        :return:
        """
        return RecordCadastre.model_validate(self._controller.get_json_record(pk=key))

    def edit_record(self, key: str, record: RecordCadastre) -> None:
        """
        Изменение записи кадастра которая должна будет отправлена на расчет
        :param key:
        :param record:
        :return:
        """
        self._controller.edit_json_record(pk=key, record=record)
        # или так -
        # self._controller.delete_json_record(pk=key)
        # self._controller.add_json_record(pk=key, record=record)

    def delete_record(self, key: str):
        """
        Удаление записи
        :param key:
        :return:
        """
        self._controller.delete_json_record(pk=key)

    def get_queue(self) -> QueueCadastre:
        """
        Получение всей очереди
        :return:
        """
        return QueueCadastre.model_validate(self._controller.get_elements_in_in_queue_topic(topic=self._topic))

    def get_position_in_queue(self, key: str):
        """
        Получение информации о своем положении в очереди
        :return:
        """
        # Вся очередь
        len_queue = len(self._controller.get_elements_in_in_queue_topic(topic=self._topic))
        # твое место в очереди
        position_in_queue = self._controller.find_index_element_in_queue_topic(topic=self._topic, key=key)
        return PositionInQueue(position=position_in_queue, key=key, len_queue=len_queue)

    def move_record_in_queue(self, new_position: int, key: str):
        """
        Изменить твое место в очереди
        :param new_position:
        :return:
        """
        # Изменение номера записи в очереди
        self._controller.move_element(topic=self._topic, new_index=new_position, value=key)

    def get_first_record_in_queue(self) -> RecordCadastre|None:
        """
        Получение первой записи в очереди
        :return:
        """
        # получение первой записи в очереди
        # Получение записи по ключу
        # удаление записи из очереди ?
        value = self._controller.first_record_in_queue(topic=self._topic)
        return value

    # сбросить очередь
    def reset_queue_count(self):
        """
        Сброс отсчета очереди
        :return:
        """
        self._controller.reset_index_queue(topic=self._topic)

    def _formation_of_new_primary_key(self) -> str:
        """
        Формирование уникального первичного ключа для новой записи
        :return:
        """
        # Получение максимального индекса из списка
        # index = self._controller.get_new_new_index_by_topic(topic=self._topic)
        len_topic = self._controller.get_len_queue_topic(topic=self._topic)
        # data = int(datetime.datetime.now().timestamp())
        # Добавление
        return f'{self._topic}-{len_topic + 1}'


# ---------------------------------------


redis_client = RedisManager()

# record = RecordCadastre(
#     cadastre_number=CadastreNumber(АА='АА', ВВ='ВВ', CCCCСCC='CCCCСCC', КК='КК'),
#     coordinates=CoordinateObject(coordinate_x=2.0, coordinate_y=4.3)
# )
#
# position = redis_client.add_record(record=record)
#
# record = redis_client.get_record(key=position.key)
# print(record)

redis_client.move_record_in_queue(new_position=1, key='cadastre-5')
