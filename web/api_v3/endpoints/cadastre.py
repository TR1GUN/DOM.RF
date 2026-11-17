from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.queries.records_cadastres import (
    add_record_cadastre,
    get_cadastre_record_by_uuid,
)
from enums import Stage
from managers.redis_manager import RedisManager
from schemas.cadastre_info import RecordCadastreInRedis, RecordStageStatus
from web.api_v3.deps.cadastre_deps import (
    get_db_session,
    get_redis_manager,
    get_request_uuid,
)
from web.api_v3.schemas.cadastre_queue import (
    QueueInfo,
    QueueItem,
    RecordInfo,
    RecordMoveRequest,
    RecordMovedResponse,
    RecordRequestQueueCreate,
)

cadastre = APIRouter(
    prefix="/records",
    tags=["Cadastre V3"],
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
    redis: RedisManager = Depends(get_redis_manager),
):
    """Создание запроса и постановка его в Redis-очередь.

    1. Сохранить запись в БД со статусом ``created``.
    2. Добавить запись в конец Redis-очереди.
    3. Вернуть UUID, статус, место в очереди и число элементов перед запросом.
    """
    db_record = await add_record_cadastre(
        session=session,
        record_cadastre=record,
        status=Stage.CREATED,
    )

    if db_record is None or db_record.request_uuid is None:
        raise HTTPException(status_code=500, detail="Failed to create record")

    position = redis.add_record(
        record=RecordCadastreInRedis(
            request_uuid=db_record.request_uuid,
            cadastre_number=record.cadastre_number,
            coordinates=record.coordinates,
            calculated=False,
            user_name=db_record.user_name,
        )
    )

    return RecordInfo(
        request_uuid=db_record.request_uuid,
        status=_record_status(db_record.status),
        position_in_queue=position.position_in_queue,
        elements_before=position.position_in_queue,
    )


@cadastre.get("/queue", response_model=QueueInfo)
async def get_queue(
    redis: RedisManager = Depends(get_redis_manager),
):
    """Получение всей Redis-очереди с местами в очереди."""
    queue_items = []

    for position, key in enumerate(redis.get_queue().queue):
        try:
            request_uuid = UUID(key)
        except (ValueError, AttributeError, TypeError):
            continue

        queue_items.append(
            QueueItem(
                request_uuid=request_uuid,
                position_in_queue=position,
            )
        )

    return QueueInfo(
        queue_length=len(queue_items),
        queue=queue_items,
    )


@cadastre.get("/{request_uuid}", response_model=RecordInfo)
async def get_record(
    request_uuid: UUID = Depends(get_request_uuid),
    session: AsyncSession = Depends(get_db_session),
    redis: RedisManager = Depends(get_redis_manager),
):
    """Получение информации о запросе и его месте в очереди."""
    db_record = await get_cadastre_record_by_uuid(
        session=session,
        user_uuid=request_uuid,
    )

    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    position_in_queue = None
    elements_before = None

    if db_record.status != Stage.COMPLETE.value:
        position = redis.get_position_in_queue(key=str(request_uuid))
        if position.position_in_queue >= 0:
            position_in_queue = position.position_in_queue
            elements_before = position.position_in_queue

    return RecordInfo(
        request_uuid=db_record.request_uuid,
        status=_record_status(db_record.status),
        position_in_queue=position_in_queue,
        elements_before=elements_before,
    )


@cadastre.patch("/{request_uuid}", response_model=RecordMovedResponse)
async def move_record(
    data: RecordMoveRequest,
    request_uuid: UUID = Depends(get_request_uuid),
    session: AsyncSession = Depends(get_db_session),
    redis: RedisManager = Depends(get_redis_manager),
):
    """Перемещение запроса на новое место в Redis-очереди."""
    db_record = await get_cadastre_record_by_uuid(
        session=session,
        user_uuid=request_uuid,
    )

    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    if db_record.status == Stage.COMPLETE.value:
        raise HTTPException(
            status_code=400,
            detail="Completed record cannot be moved in queue",
        )

    key = str(request_uuid)
    old_position = redis.get_position_in_queue(key=key)

    if old_position.position_in_queue < 0:
        raise HTTPException(status_code=404, detail="Record is not in queue")

    new_position = redis.move_record_in_queue(
        new_position=data.new_position,
        key=key,
    )

    if new_position is None:
        raise HTTPException(status_code=404, detail="Record is not in queue")

    return RecordMovedResponse(
        request_uuid=request_uuid,
        old_position_in_queue=old_position.position_in_queue,
        new_position_in_queue=new_position,
        elements_before=new_position,
    )
