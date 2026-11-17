from uuid import UUID

from pydantic import BaseModel, Field

from enums import Priority
from schemas.cadastre_info import RecordCadastre, RecordStageStatus


class RecordRequestQueueCreate(RecordCadastre):
    """Входные данные для POST /v2/records."""

    priority: Priority = Field(
        default=Priority.STANDARD,
        description="Приоритет обработки (1 — обычная подписка, 2 — премиум)",
    )


class RecordInfo(BaseModel):
    """Информация о запросе с приоритетом."""

    request_uuid: UUID = Field(description="Уникальный идентификатор запроса")
    status: RecordStageStatus = Field(description="Статус запроса")
    priority: Priority = Field(description="Приоритет обработки")


class RecordPriorityChangeRequest(BaseModel):
    """Входные данные для PATCH /v2/records/{request_uuid}."""

    priority: Priority = Field(description="Новый приоритет обработки")


class RecordPriorityChangedResponse(BaseModel):
    """Ответ на PATCH /v2/records/{request_uuid}."""

    request_uuid: UUID = Field(description="Уникальный идентификатор запроса")
    old_priority: Priority | None = Field(description="Старый приоритет обработки")
    new_priority: Priority = Field(description="Новый приоритет обработки")
    status: RecordStageStatus = Field(description="Статус запроса")


class QueueItem(BaseModel):
    """Элемент очереди с приоритетом."""

    request_uuid: UUID = Field(description="Уникальный идентификатор запроса")
    priority: Priority = Field(description="Приоритет обработки")


class QueueInfo(BaseModel):
    """Ответ на GET /v2/records/queue."""

    queue_length: int = Field(description="Общее количество элементов в очереди")
    queue: list[QueueItem] = Field(
        description="Очередь, отсортированная по приоритету обработки"
    )
