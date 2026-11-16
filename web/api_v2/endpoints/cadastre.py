from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.cadastre_info import RecordCadastre, RecordCadastreControl, RecordCadastreDataBase, PositionInQueue
from database.queries.records_cadastres import (
    add_record_cadastre_with_priority,
    get_record_cadastre_with_priority,
    set_priority_record_cadastre,
)
from database.setup_db import DataBase
from tasks.celery_tasks import billing_request

cadastre = APIRouter(
    prefix="/cadastre",
    tags=["Cadastre V2"],
    responses={404: {"description": "Not found"}},
)


# - Отправить запись на расчет с приоритетом
@cadastre.post("/records", status_code=200)
async def set_cadastre_info(
    record_cadastre: RecordCadastre,
    session: AsyncSession = Depends(DataBase.scoped_session_dependency),
    priority: int = 1,
) -> dict:
    """
    Accept the cadastre record for calculation with priority.
    Returns record ID, status, and priority.
    """
    user_name = await add_record_cadastre_with_priority(
        session=session, record_cadastre=record_cadastre, priority=priority
    )
    # Enqueue the Celery task
    billing_request.delay(record_cadastre.model_dump())
    return {
        "user_name": user_name,
        "status": "created",
        "priority": priority,
    }


# - Менять номер запроса в очереди запроса - Задание приоритета
@cadastre.put("/records/{user_name}/queue_move", status_code=200)
async def set_priority(
    user_name: str,
    new_priority: int,
    session: AsyncSession = Depends(DataBase.scoped_session_dependency),
) -> dict:
    """
    Change the priority of a record that has not been calculated yet.
    """
    record = await get_record_cadastre_with_priority(session=session, user_name=user_name)

    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    if record.stage == "complete":
        raise HTTPException(status_code=400, detail="Record already calculated")

    result = await set_priority_record_cadastre(session=session, user_name=user_name, new_priority_value=new_priority)

    # Re-enqueue the Celery task with new priority
    return {
        "user_name": user_name,
        "old_priority": result['old_priority_id'],
        "new_priority": result['new_priority_id'],
    }


# - Отдать результат отчета по ID
@cadastre.get("/records/{user_name}", status_code=200)
async def get_record_cadastre(
    user_name: str, session: AsyncSession = Depends(DataBase.scoped_session_dependency)
) -> RecordCadastreControl:
    """
    Get information by ID records.
    """
    record = await get_record_cadastre_with_priority(session=session, user_name=user_name)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return RecordCadastreControl(record=record, position_in_queue=None)
