from schemas.cadastre_info import (
    PositionInQueue,
    QueueCadastre,
    RecordCadastre,
    RecordCadastreInRedis,
)
from controllers import RedisController
from settings.settings import settings_app


class RedisManager:
    """Менеджер Redis-очереди (API v3)."""

    _controller: RedisController
    _topic: str

    def __init__(self, topic: str = "cadastre"):
        self._controller = RedisController(
            host=settings_app.redis.redis_host,
            port=settings_app.redis.redis_port,
            db=settings_app.redis.redis_db,
        )
        self._topic = topic

    def add_record(self, record: RecordCadastreInRedis) -> PositionInQueue:
        """
        Добавить запись в конец очереди.

        Ключом записи служит ``request_uuid``.
        """
        key = str(record.request_uuid)
        self._controller.add_json_record(
            pk=key,
            record=record.model_dump(mode="json"),
        )
        position_in_queue = self._controller.add_element_in_queue_topic(
            topic=self._topic,
            value=key,
        )
        queue_length = self._controller.get_len_queue_topic(topic=self._topic)

        return PositionInQueue(
            position_in_queue=position_in_queue,
            queue_length=queue_length,
        )

    def get_record(self, key: str) -> RecordCadastreInRedis | None:
        """Получить запись по ключу."""
        record = self._controller.get_json_record(pk=key)
        if record is None:
            return None
        return RecordCadastreInRedis.model_validate(record)

    def edit_record(self, key: str, record: RecordCadastre) -> None:
        """Изменить данные кадастра в записи."""
        self._controller.edit_json_record(pk=key, record=record)

    def delete_record(self, key: str) -> None:
        """Удалить запись."""
        self._controller.delete_json_record(pk=key)

    def get_queue(self) -> QueueCadastre:
        """Получить всю очередь."""
        return QueueCadastre(
            queue=self._controller.get_elements_in_in_queue_topic(
                topic=self._topic,
            )
        )

    def get_queue_length(self) -> int:
        """Получить количество элементов в очереди."""
        return self._controller.get_len_queue_topic(topic=self._topic)

    def add_element_in_queue(self, key: str) -> int:
        """Добавить запись в конец очереди. Возвращает её индекс."""
        return self._controller.add_element_in_queue_topic(
            topic=self._topic,
            value=key,
        )

    def get_position_in_queue(self, key: str) -> PositionInQueue:
        """Получить позицию записи и длину очереди."""
        queue_length = self._controller.get_len_queue_topic(topic=self._topic)
        position_in_queue = self._controller.find_index_element_in_queue_topic(
            topic=self._topic,
            key=key,
        )

        return PositionInQueue(
            position_in_queue=(
                position_in_queue if position_in_queue is not None else -1
            ),
            queue_length=queue_length,
        )

    def move_record_in_queue(self, new_position: int, key: str) -> int | None:
        """Переместить запись на новую позицию. Возвращает новый индекс."""
        return self._controller.move_element(
            topic=self._topic,
            new_index=new_position,
            value=key,
        )

    def get_first_record_in_queue(self) -> RecordCadastreInRedis | None:
        """Получить и удалить первую запись из очереди."""
        record = self._controller.first_record_in_queue(topic=self._topic)
        if record is None:
            return None
        return RecordCadastreInRedis.model_validate(record)

    def reset_queue_count(self) -> None:
        """Очистить очередь."""
        self._controller.reset_index_queue(topic=self._topic)
