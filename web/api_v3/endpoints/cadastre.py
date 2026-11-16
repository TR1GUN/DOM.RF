import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.cadastre_info import (
    RecordCadastre,
    RecordCadastreInRedis,
    RecordCadastreControl,
    RecordInfoRedis,
    PositionInQueue,
)
from managers.redis_manager import RedisManager
from managers.rabbit_mq_manager import PublisherManager
from database.queries.records_cadastres import add_record_cadastre, get_cadastre_record_by_id, rename_user_name
from database.setup_db import DataBase


cadastre = APIRouter(
    prefix="/cadastre",
    tags=["Cadastre V3"],
    responses={404: {"description": "Not found"}},
)


# - Отправить запись на расчет
@cadastre.post("/records", status_code=200)
async def set_cadastre_info(
    record_cadastre: RecordCadastre,
    redis: RedisManager = Depends(),
    session: AsyncSession = Depends(DataBase.scoped_session_dependency),
) -> RecordInfoRedis:
    """
    Accept the cadastre record for calculation.
    Adds to Redis queue and publishes to RabbitMQ.
    """
    user_name = await add_record_cadastre(session=session, record_cadastre=record_cadastre)
    position = await redis.add_record(
        record=RecordCadastreInRedis(
            cadastre_number=record_cadastre.cadastre_number,
            coordinates=record_cadastre.coordinates,
            calculated=False,
            user_name=user_name,
            key=user_name,
        )
    )
    # Publish to RabbitMQ for processing
    publisher = PublisherManager(topic="cadastre")
    publisher.send_message(message=user_name, priority=1)
    return RecordInfoRedis(user_name=user_name, position_in_queue=position)


# - Менять номер запроса в очереди запроса - Перемещение именно в очереди
@cadastre.put("/queue/move", status_code=200)
async def move_in_queue(user_name: str, new_position: int, redis: RedisManager = Depends()) -> PositionInQueue:
    """
    Physically move a record to a new position in the queue.
    """
    redis.move_record_in_queue(new_position=new_position, key=user_name)
    return await redis.get_position_in_queue(key=user_name)


# - Менять номер запроса в очереди запроса - меняем именно номер
@cadastre.put("/records/rename/{old_user_name}", status_code=200)
async def rename_record(
    old_user_name: str,
    new_user_name: str,
    session: AsyncSession = Depends(DataBase.scoped_session_dependency),
) -> dict:
    """
    Change the user-facing name of a record.
    """
    result = await rename_user_name(session=session, old_user_name=old_user_name, new_user_name=new_user_name)
    return result


# - Отдать результат отчета по ID
@cadastre.get("/queue/records/{user_name}", status_code=200)
async def get_record_in_queue(user_name: str, redis: RedisManager = Depends()) -> RecordInfoRedis:
    """
    View queue position and request information.
    """
    record = redis.get_record(key=user_name)
    return RecordInfoRedis(
        record=record, user_name=record.user_name, position_in_queue=await redis.get_position_in_queue(key=user_name)
    )


@cadastre.get("/records/{user_name}", status_code=200)
async def get_record_cadastre(
    user_name: str, session: AsyncSession = Depends(DataBase.scoped_session_dependency), redis: RedisManager = Depends()
) -> RecordCadastreControl:
    """
    Get information by ID records.
    """
    record_in_database = await get_cadastre_record_by_id(session=session, user_name=user_name)
    if record_in_database is None:
        raise HTTPException(status_code=404, detail="Record not found")
    if record_in_database.stage != 'complete':
        position_in_queue = await redis.get_position_in_queue(key=record_in_database.key)
    else:
        position_in_queue = None
    return RecordCadastreControl(record=record_in_database, position_in_queue=position_in_queue)
