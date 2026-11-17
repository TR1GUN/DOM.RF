from uuid import UUID

from pydantic import BaseModel, Field

from schemas.cadastre_info import RecordCadastre, RecordStageStatus


class RecordRequestQueueCreate(RecordCadastre):
    """Входные данные для POST /v3/records."""


class RecordInfo(BaseModel):
    """Информация о запросе в очереди."""

    request_uuid: UUID = Field(description="Уникальный идентификатор запроса")
    status: RecordStageStatus = Field(description="Статус запроса")
    position_in_queue: int | None = Field(
        default=None,
        description="Место в очереди (0 — первая позиция); None, если запрос не в очереди",
    )
    elements_before: int | None = Field(
        default=None,
        description="Количество элементов в очереди перед запросом",
    )


class RecordMoveRequest(BaseModel):
    """Входные данные для PATCH /v3/records/{request_uuid}."""

    new_position: int = Field(
        ge=0,
        description="Новое место в очереди (0 — первая позиция)",
    )


class RecordMovedResponse(BaseModel):
    """Ответ на PATCH /v3/records/{request_uuid}."""

    request_uuid: UUID = Field(description="Уникальный идентификатор запроса")
    old_position_in_queue: int = Field(description="Старое место в очереди")
    new_position_in_queue: int = Field(description="Новое место в очереди")
    elements_before: int = Field(
        description="Количество элементов в очереди перед запросом после перемещения"
    )


class QueueItem(BaseModel):
    """Элемент очереди."""

    request_uuid: UUID = Field(description="Уникальный идентификатор запроса")
    position_in_queue: int = Field(description="Место в очереди")


class QueueInfo(BaseModel):
    """Ответ на GET /v3/records/queue."""

    queue_length: int = Field(description="Общее количество элементов в очереди")
    queue: list[QueueItem] = Field(
        description="Очередь, отсортированная по месту в очереди"
    )
