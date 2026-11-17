from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.queries.records_cadastres import (
    add_record_cadastre_with_priority,
    get_cadastre_record_by_uuid,
    get_priority_queue_records,
    set_priority_record_cadastre_by_uuid,
)
from enums import Priority, Stage
from schemas.cadastre_info import RecordStageStatus
from web.api_v2.deps.cadastre_deps import get_db_session, get_request_uuid
from web.api_v2.schemas.cadastre_queue import (
    QueueInfo,
    QueueItem,
    RecordInfo,
    RecordPriorityChangeRequest,
    RecordPriorityChangedResponse,
    RecordRequestQueueCreate,
)

cadastre = APIRouter(
    prefix="/records",
    tags=["Cadastre V2"],
    responses={404: {"description": "Not found"}},
)


def _record_status(status: str | None) -> RecordStageStatus:
    """Привести строковый статус из БД к схеме ответа."""
    if status is None:
        raise HTTPException(status_code=500, detail="Record status is missing")
    try:
        return RecordStageStatus(status=Stage(status))
    except ValueError:
        raise HTTPException(status_code=500, detail="Unknown record status")


@cadastre.post("", response_model=RecordInfo)
async def create_record(
    record: RecordRequestQueueCreate,
    session: AsyncSession = Depends(get_db_session),
):
    """Создание запроса на расчёт с приоритетом.

    1. Сохранить запись в БД со статусом ``created``.
    2. Вернуть UUID, статус и приоритет обработки.
    """
    db_record = await add_record_cadastre_with_priority(
        session=session,
        record_cadastre=record,
        priority=record.priority,
        status=Stage.CREATED,
    )

    if (
        db_record is None
        or db_record.request_uuid is None
        or db_record.priority_int is None
    ):
        raise HTTPException(status_code=500, detail="Failed to create record")

    return RecordInfo(
        request_uuid=db_record.request_uuid,
        status=_record_status(db_record.status),
        priority=Priority(db_record.priority_int),
    )


@cadastre.get("/queue", response_model=QueueInfo)
async def get_queue(
    session: AsyncSession = Depends(get_db_session),
):
    """Получение очереди, отсортированной по приоритету обработки."""
    queue_items = await get_priority_queue_records(session=session)

    return QueueInfo(
        queue_length=len(queue_items),
        queue=[
            QueueItem(
                request_uuid=item.request_uuid,
                priority=Priority(item.priority),
            )
            for item in queue_items
        ],
    )


@cadastre.get("/{request_uuid}", response_model=RecordInfo)
async def get_record(
    request_uuid: UUID = Depends(get_request_uuid),
    session: AsyncSession = Depends(get_db_session),
):
    """Получение информации о запросе по его UUID."""
    db_record = await get_cadastre_record_by_uuid(
        session=session,
        user_uuid=request_uuid,
    )

    if db_record is None or db_record.priority_int is None:
        raise HTTPException(status_code=404, detail="Record not found")

    return RecordInfo(
        request_uuid=db_record.request_uuid,
        status=_record_status(db_record.status),
        priority=Priority(db_record.priority_int),
    )


@cadastre.patch("/{request_uuid}", response_model=RecordPriorityChangedResponse)
async def change_priority(
    data: RecordPriorityChangeRequest,
    request_uuid: UUID = Depends(get_request_uuid),
    session: AsyncSession = Depends(get_db_session),
):
    """Изменение приоритета запроса.

    Приоритет можно менять только у запросов в статусе ``created``.
    """
    db_record = await get_cadastre_record_by_uuid(
        session=session,
        user_uuid=request_uuid,
    )

    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    if db_record.status != Stage.CREATED.value:
        raise HTTPException(
            status_code=400,
            detail="Priority can only be changed for records in 'created' status",
        )

    result = await set_priority_record_cadastre_by_uuid(
        session=session,
        request_uuid=request_uuid,
        new_priority_value=data.priority.value,
    )

    if result is None:
        raise HTTPException(status_code=500, detail="Failed to change priority")

    old_priority = result["old_priority"]

    return RecordPriorityChangedResponse(
        request_uuid=request_uuid,
        old_priority=Priority(old_priority) if old_priority is not None else None,
        new_priority=Priority(result["new_priority"]),
        status=_record_status(result["status"]),
    )
