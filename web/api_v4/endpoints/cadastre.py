import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.cadastre_info import RecordCadastre, RecordCadastreInRedis, RecordCadastreControl, RecordInfoRedis
from managers.redis_manager import RedisManager
from database.queries.records_cadastres import (
    add_record_cadastre,
    get_cadastre_record_by_id,
    rename_user_name,
)
from database.setup_db import DataBase


cadastre = APIRouter(
    prefix="/cadastre",
    tags=["Cadastre V1"],
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
    Accept the cadastre record for calculation
    :return:
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
    return RecordInfoRedis(user_name=user_name, position_in_queue=position)


# - Менять номер запроса в очереди запроса - Перемещение именно в очереди
@cadastre.put("/queue/move", status_code=200)
async def set_cadastre_info(key: str, new_position: int, redis: RedisManager = Depends()) -> None:
    """
    Change the request number in the request queue
    :param key:
    :param new_position:
    :param redis:
    :return:
    """
    redis.move_record_in_queue(new_position=new_position, key=key)


# - Менять номер запроса в очереди запроса - меняем именно номер
@cadastre.put("/records/rename/{old_user_name}", status_code=200)
async def set_cadastre_info(
    old_user_name: str,
    new_user_name: str,
    session: AsyncSession = Depends(DataBase.scoped_session_dependency),
) -> dict:
    """
    Change the request number in the request queue
    :param old_user_name:
    :param new_user_name:
    :param session:
    :return:
    """
    result = await rename_user_name(session=session, old_user_name=old_user_name, new_user_name=new_user_name)
    return result


# - Отдать результат отчета по ID
@cadastre.get("queue/records/{key}", status_code=200)
async def get_record_in_queue(key: str, redis: RedisManager = Depends()) -> RecordInfoRedis:
    """
    View queue position and request information
    :param key:
    :param redis:
    :return:
    """
    record = redis.get_record(key=key)
    return RecordInfoRedis(
        record=record, user_name=record.user_name, position_in_queue=await redis.get_position_in_queue(key=key)
    )


@cadastre.get("/records/{user_name}", status_code=200)
async def get_record_cadastre(
    user_name: str, session: AsyncSession = Depends(DataBase.scoped_session_dependency), redis: RedisManager = Depends()
) -> RecordCadastreControl:
    """
    Get information by ID records
    :param redis:
    :param user_name:
    :param session:
    :return:
    """
    record_in_database = await get_cadastre_record_by_id(session=session, user_name=user_name)
    if record_in_database is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Record not found")
    if record_in_database.stage != 'complete':
        position_in_queue = await redis.get_position_in_queue(key=record_in_database.key)
    else:
        position_in_queue = None
    return RecordCadastreControl(record=record_in_database, position_in_queue=position_in_queue)
