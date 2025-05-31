from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.schemas_cadastre import RecordCadastre, PositionInQueue, QueueCadastre
from celery_tasks.celery_tasks import billing_request
from managers.redis_manager import RedisManager
from database.queries.records_cadastres import add_record_cadastre, get_cadastres_by_id
from database.setup_db import DataBase


v2 = APIRouter(
    prefix='/v2',
    tags=['Cadastre'],
    responses={404: {"description": "Not found"}},
)


@cadastre.post('/records', status_code=200)
async def set_cadastre_info(
        record_cadastre:RecordCadastre,
        redis:RedisManager = Depends(),
        session: AsyncSession = Depends(DataBase.scoped_session_dependency)) -> PositionInQueue:
    """
    Принять запись кадастра
    :return:
    """
    # Добавляем в БД запись
    await add_record_cadastre(session=session, record_cadastre=record_cadastre)
    # добавляем в Redis полученную запись
    return redis.add_record(record=record_cadastre)


@cadastre.get('/records/{id}', status_code=200)
async def get_record_cadastre(
        id:int,
        session: AsyncSession = Depends(DataBase.scoped_session_dependency)) -> RecordCadastre:
    return await get_cadastres_by_id(session=session,cadastres_id=id)


@cadastre.get('queue', status_code=200)
async def get_all_queue(
        redis: RedisManager = Depends()) -> QueueCadastre:

    return redis.get_queue()


@cadastre.get('queue/records/{id}', status_code=200)
async def get_record_in_queue(
        key:str,
        redis: RedisManager = Depends()):
    return redis.get_record(key=key)


@cadastre.put('/queue/move', status_code=200)
async def set_cadastre_info(
        key: str,
        new_position:int,
        redis: RedisManager = Depends())-> None:
    """
    Поменять номер запроса в очереди запроса
    :param key:
    :param new_position:
    :param redis:
    :return:
    """
    redis.move_record_in_queue(new_position=new_position, key=key)

# @cadastre.post('/results')
# def get_result_info():
#     """
#     Отдать результат запроса по ID
#     :return:
#     """
#     pass
#
# @cadastre.get('/results/{record}')
# def get_result_info_by_id(record:int):
#     """
#     Отдать результат запроса по ID
#     :return:
#     """
#     pass