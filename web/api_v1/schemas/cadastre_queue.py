import uuid
from pydantic import BaseModel, Field

from schemas.cadastre_info import ObjectsCadastres, RecordStageStatus, PositionInQueue


class RecordRequestQueueCreate(BaseModel):
    """Входные данные для POST /records."""
    objects_cadastres: ObjectsCadastres = Field(description="Кадастровые данные объекта")
    user_name: str = Field(description="Имя пользователя (идентификатор запроса)")


class RecordInfo(BaseModel):
    """Ответ на POST /records."""
    request_uuid: uuid.UUID = Field(description="Уникальный идентификатор запроса")
    user_name: str = Field(description="Имя пользователя (идентификатор запроса)")
    status: RecordStageStatus = Field(description="Статус запроса (created)")
    position_in_queue: PositionInQueue = Field(description="Позиция в очереди")

class RecordRenameRequest(BaseModel):
    """Входные данные для PATCH /records/{user_name}."""
    user_name: str = Field(description="Новое имя пользователя")


class RecordRenamedResponse(BaseModel):
    """Ответ на PATCH /records/{user_name}."""
    request_uuid: uuid.UUID = Field(description="Уникальный идентификатор запроса")
    old_user_name: str = Field(description="Старое имя пользователя")
    new_user_name: str = Field(description="Новое имя пользователя")
    position_in_queue: PositionInQueue = Field(description="Позиция в очереди")

class QueueItem(BaseModel):
    """Элемент очереди."""
    position_in_queue: PositionInQueue = Field(description="Позиция в очереди")
    user_name: str = Field(description="Имя пользователя")


class QueueInfo(BaseModel):
    """Ответ на GET /records/queue."""
    queue_length: int = Field(description="Общее количество элементов в очереди")
    data_in_queue: list[QueueItem] = Field(exclude=True, description="Массив элементов очереди, отсортированный по позиции")

    def queue(self)->list[QueueItem]:
        """Возвращает отсортированный массив элементов очереди."""
        return [
            QueueItem(**item) for item in sorted(self.data_in_queue, key=lambda item: item.position_in_queue)

        ]
