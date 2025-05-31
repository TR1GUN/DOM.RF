from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.schemas_cadastre import RecordCadastre, RecordCadastreInRedis, RecordCadastreControl, RecordInfoRedis
from managers.redis_manager import RedisManager
from database.queries.records_cadastres import add_record_cadastre, get_cadastre_record_by_id, rename_cadastre_index
from database.setup_db import DataBase
from enums import Stage

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
        session: AsyncSession = Depends(DataBase.scoped_session_dependency)) -> RecordInfoRedis:
    """
    Accept the cadastre record for calculation
    :return:
    """
    index = await add_record_cadastre(
        session=session,
        record_cadastre=record_cadastre
    )
    position = await redis.add_record(
        record=RecordCadastreInRedis(
            cadastre_number=record_cadastre.cadastre_number,
            coordinates=record_cadastre.coordinates,
            calcualated=False)
    )
    return RecordInfoRedis(index=index, position_in_queue=position)


# - Менять номер запроса в очереди запроса - Перемещение именно в очереди
@cadastre.put('/queue/move', status_code=200)
async def set_cadastre_info(
        key: str,
        new_position: int,
        redis: RedisManager = Depends()) -> None:
    """
    Change the request number in the request queue
    :param key:
    :param new_position:
    :param redis:
    :return:
    """
    redis.move_record_in_queue(new_position=new_position, key=key)


# - Менять номер запроса в очереди запроса - меняем именно номер
@cadastre.put('/records/rename/{name}', status_code=200)
async def set_cadastre_info(
        name: str,
        new_name: str,
        session: AsyncSession = Depends(DataBase.scoped_session_dependency)) -> None:
    """
    Change the request number in the request queue
    :param name:
    :param new_name:
    :param session:
    :return:
    """
    await rename_cadastre_index(session=session, old_name=name, new_name=new_name)


# - Отдать результат отчета по ID
@cadastre.get('queue/records/{key}', status_code=200)
async def get_record_in_queue(
        key: str,
        redis: RedisManager = Depends()) -> RecordInfoRedis:
    """
    View queue position and request information
    :param key:
    :param redis:
    :return:
    """
    record = redis.get_record(key=key)
    return RecordInfoRedis(
        record=record,
        index=record.index,
        position_in_queue=await redis.get_position_in_queue(key=key)
    )


@cadastre.get('/records/{id}', status_code=200)
async def get_record_cadastre(
        id: str,
        session: AsyncSession = Depends(DataBase.scoped_session_dependency),
        redis: RedisManager = Depends()
) -> RecordCadastreControl:
    """
    Get information by ID records
    :param redis:
    :param id:
    :param session:
    :return:
    """
    record_in_database = await get_cadastre_record_by_id(session=session, cadastres_id=id)
    if not record_in_database.stage == Stage.complete:
        position_in_queue = redis.get_position_in_queue(key=record_in_database.key)
    else:
        position_in_queue = None
    return RecordCadastreControl(record=record_in_database, position_in_queue=position_in_queue)
