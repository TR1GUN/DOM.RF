from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.schemas_cadastre import RecordCadastre, PositionInQueue, QueueCadastre, RecordCadastreInRedis, RecordInfo
from celery_tasks.celery_tasks import billing_request
from managers.redis_manager import RedisManager
from database.queries.records_cadastres import add_record_cadastre, get_cadastres_by_id
from database.setup_db import DataBase

cadastre = APIRouter(
    prefix='/cadastre',
    tags=['Cadastre'],
    responses={404: {"description": "Not found"}},
)


# - Отправить запись на расчет
@cadastre.post('/records', status_code=200)
async def set_cadastre_info(
        record_cadastre: RecordCadastre,
        redis: RedisManager = Depends(),
        session: AsyncSession = Depends(DataBase.scoped_session_dependency)) -> RecordInfo:
    """
    Accept the cadastre record for calculation
    :return:
    """
    record = RecordCadastreInRedis(
        cadastre_number=record_cadastre.cadastre_number,
        coordinates=record_cadastre.coordinates,
        calcualated=False)
    index = await add_record_cadastre(
        session=session,
        record_cadastre=record
    )
    position = await redis.add_record(record=record)
    return RecordInfo(index=index, position_in_queue=position)


# - Отдать результат отчета по ID

@cadastre.get('/records/{id}', status_code=200)
async def get_record_cadastre(
        id: int,
        session: AsyncSession = Depends(DataBase.scoped_session_dependency)) -> RecordCadastre:
    """
    get information by ID records
    :param id:
    :param session:
    :return:
    """
    return await get_cadastres_by_id(session=session, cadastres_id=id)


# @cadastre.get('queue', status_code=200)
# async def get_all_queue(
#         redis: RedisManager = Depends()) -> QueueCadastre:
#
#     return redis.get_queue()

# Менять номер запроса в очереди запроса
@cadastre.get('queue/records/{id}', status_code=200)
async def get_record_in_queue(
        key: str,
        redis: RedisManager = Depends()):
    return redis.get_record(key=key)


@cadastre.put('/queue/move', status_code=200)
async def set_cadastre_info(
        key: str,
        new_position: int,
        redis: RedisManager = Depends()) -> None:
    """
    Поменять номер запроса в очереди запроса
    :param key:
    :param new_position:
    :param redis:
    :return:
    """
    redis.move_record_in_queue(new_position=new_position, key=key)
