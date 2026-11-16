from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from enums import Stage
from schemas.cadastre_info import RecordStageStatus, PositionInQueue
from web.api_v1.schemas.cadastre_queue import (
    RecordRequestQueueCreate,
    RecordInfo,
    RecordRenameRequest,
    RecordRenamedResponse,
    QueueInfo,
)
from web.api_v1.deps.cadastre_deps import get_db_session, get_user_uuid
from database.queries.records_cadastres import (
    add_record_cadastre,
    get_cadastre_record_by_uuid,
    get_position_in_names_queue, get_user_position_in_queue, update_record_cadastre, get_queue_requests_items
)
from schemas.app_data_containers import ModifiedUserName, DataBaseRecord

cadastre = APIRouter(
    prefix="/records",
    tags=["Cadastre V1"],
    responses={404: {"description": "Not found"}},
)


@cadastre.post("", response_model=RecordInfo)
async def create_record(
    record: RecordRequestQueueCreate,
    session: AsyncSession = Depends(get_db_session),
):
    """Создание запроса на расчет.
    
    1. Сохранить в БД со статусом 'in_queue'
    2. Посчитать позицию в очереди (ORDER BY user_name)
    3. Вернуть request_uuid, status, position_in_queue
    """
    # Создаем запись в БД
    db_record = await add_record_cadastre(
        session=session,
        record_cadastre=record.objects_cadastres,
        user_name=record.user_name,
        # Ставим запись сразу - в очереди, так как БД - и есть очередь
        status=Stage.IN_QUEUE,
    )
    
    if db_record is None or not db_record.request_uuid is not None or not db_record.user_name is not None:
        raise HTTPException(status_code=500, detail="Failed to create record")


    position_in_queue = await get_user_position_in_queue(
            session=session,
            user_name=db_record.user_name
        )

    return RecordInfo(
        request_uuid=db_record.request_uuid,
        user_name= db_record.user_name,
        status=RecordStageStatus(status=db_record.stage),
        position_in_queue=PositionInQueue(
            position_in_queue=position_in_queue.position_in_queue,
            queue_length=position_in_queue.queue_length
        )
    )


@cadastre.get("/{user_uuid}", response_model=RecordInfo)
async def get_record(
    user_uuid: UUID = Depends(get_user_uuid),
    session: AsyncSession = Depends(get_db_session),
):
    """Получение информации о запросе.
    
    1. Получить из БД по user_name
    2. Посчитать позицию в очереди (ORDER BY user_name)
    3. Вернуть request_uuid, status, position_in_queue, user_name
    """
    # Смотрим нашу запись в БД
    db_record = await get_cadastre_record_by_uuid(session=session, user_uuid=user_uuid)

    if db_record is None or not db_record.request_uuid is not None or not db_record.user_name is not None:
        raise HTTPException(status_code=500,  detail="Record not exist")

    position_in_queue = await get_user_position_in_queue(
            session=session,
            user_name=db_record.user_name
        )

    return RecordInfo(
        request_uuid=db_record.request_uuid,
        user_name=db_record.user_name,
        status=RecordStageStatus(status=db_record.stage),
        position_in_queue=PositionInQueue(
            position_in_queue=position_in_queue.position_in_queue,
            queue_length=position_in_queue.queue_length
        )
    )

@cadastre.patch("/{user_uuid}", response_model=RecordRenamedResponse)
async def rename_record(
    user_uuid: UUID = Depends(get_user_uuid),
    data: RecordRenameRequest = Depends(),
    session: AsyncSession = Depends(get_db_session),
):
    """Переименование запроса.
    
    1. Обновить user_name в БД
    2. Посчитать новую позицию в очереди
    3. Вернуть old_user_name, new_user_name, position_in_queue, status
    """
    # Переименовываем в БД
    result = await update_record_cadastre(
        session=session,
        user_uuid=user_uuid,
        new_user_name=data.user_name,
    )
    if result is None or result.user_name is None:
        raise HTTPException(status_code=500, detail="Record not exist")

    position_in_queue = await get_user_position_in_queue(
            session=session,
            user_name=result.user_name.new_user_name
        )

    return RecordRenamedResponse(
        request_uuid=user_uuid,
        old_user_name=result.user_name.old_user_name,
        new_user_name=result.user_name.new_user_name,
        position_in_queue =PositionInQueue(
            position_in_queue=position_in_queue.position_in_queue,
            queue_length=position_in_queue.queue_length
        )
    )


@cadastre.get("/queue", response_model=QueueInfo)
async def get_queue(
    session: AsyncSession = Depends(get_db_session),
):
    """Получение информации о всей очереди.
    
    1. Получить все записи со статусом 'in_queue' из БД
    2. Отсортировать по user_name (алфавитный порядок)
    3. Вернуть queue_length и массив QueueItemV1
    """

    queue_items = await get_queue_requests_items(session=session)

    return QueueInfo(
        queue_length=len(queue_items),
        data_in_queue=queue_items,
    )