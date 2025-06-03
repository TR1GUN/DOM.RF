from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.schemas_cadastre import RecordCadastre, RecordCadastreControl, QueueCadastre
from tasks.celery_tasks import billing_request
from managers.redis_manager import RedisManager
from database.queries.records_cadastres import add_record_cadastre_with_priority, get_record_cadastre_with_priority, set_priority_record_cadastre
from database.setup_db import DataBase


cadastre = APIRouter(
    prefix='/cadastre',
    tags=['Cadastre'],
    responses={404: {"description": "Not found"}},
)


# - Отправить запись на расчет
# - Менять номер запроса в очереди запроса
# - Отдать результат отчета по ID

# - Отправить запись на расчет
@cadastre.post('/records', status_code=200)
async def set_cadastre_info(
        record_cadastre: RecordCadastre,
        session: AsyncSession = Depends(DataBase.scoped_session_dependency)) -> int:
    """
    Accept the cadastre record for calculation
    :return:
    """
    return await add_record_cadastre_with_priority(
        session=session,
        record_cadastre=record_cadastre,
        priority=1
    )


# - Менять номер запроса в очереди запроса - Задание приоритета
@cadastre.put('/records/{id}/queue_move', status_code=200)
async def set_cadastre_info(
        id: int,
        new_priority: int,
        session: AsyncSession = Depends(DataBase.scoped_session_dependency)) -> None:
    """
    Change the request number in the request queue
    :param key:
    :param new_position:
    :param redis:
    :return:
    """
    record = await get_record_cadastre_with_priority(
        session=session,
        record_cadastre_id=id)

    if record.calculated:
        raise Exception("record calculataed")

    return await set_priority_record_cadastre(
        session=session,
        record_cadastre_id=id,
        new_priority=new_priority
    )


# - Отдать результат отчета по ID
@cadastre.get('/records/{id}', status_code=200)
async def get_record_cadastre(
        id: str,
        session: AsyncSession = Depends(DataBase.scoped_session_dependency)
) -> RecordCadastreControl:
    """
    Get information by ID records
    :param redis:
    :param id:
    :param session:
    :return:
    """
    return await get_record_cadastre_with_priority(
        session=session,
        record_cadastre_id=id)
