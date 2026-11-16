import uuid

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from database.models import CadastralQueueRecords, StageStatus
from sqlalchemy.ext.asyncio import AsyncSession

from database.queries.cadastre_objects import get_or_create_cadastre_objects
from database.queries.priority import get_or_create_priority
from database.queries.state import get_or_create_stage
from enums import Stage, Priority
from logger.logger import BaseLogger
from schemas.app_data_containers import (
    ModifiedUserName,
    DataBaseRecord,
    ModifiedPositionInQueue,
    PositionInQueue,
    ModifiedUserData,
    ModifiedPriority,
    ModifiedStatus,
    QueueItem,
)
from schemas.cadastre_info import ObjectsCadastres as ObjectsCadastresSchema, RecordCadastreDataBase

logger = BaseLogger(__name__)


async def get_cadastre_record_by_id(session: AsyncSession, user_name: str) -> RecordCadastreDataBase | None:
    """Get record by its user_name."""
    stmt = select(CadastralQueueRecords).where(CadastralQueueRecords.user_name == user_name)
    result = await session.execute(stmt)
    record = result.scalar_one_or_none()
    if record is None:
        return None
    return _record_to_db_schema(record)


async def add_record_cadastre(
        session: AsyncSession,
        record_cadastre: ObjectsCadastresSchema,
        user_name: str | None = None,
        priority: Priority = Priority.STANDARD,
        status: Stage = Stage.CREATED,
) -> DataBaseRecord | None:
    """
    Add a new cadastre record to the database.
    Returns DataBaseRecord on success, None on failure.
    """
    if user_name is None:
        user_name = str(uuid.uuid4())[:64]

    try:
        async with session.begin():
            cadastre_objects = await get_or_create_cadastre_objects(
                session=session,
                object_cadastre=record_cadastre,
            )
            stage = await get_or_create_stage(session=session, stage=status)
            priority_record = await get_or_create_priority(session=session, priority=priority)

            new_record = CadastralQueueRecords(
                user_name=user_name,
                object_cadastres_id=cadastre_objects.id,
                stage_id=stage.id,
                priority_id=priority_record.id,
            )
            session.add(new_record)

        return DataBaseRecord(
            request_uuid=new_record.request_uuid,
            user_name=new_record.user_name,
            status=stage.value,
            priority_int=priority_record.value,
            position_in_queue=ModifiedPositionInQueue(
                old_position_in_queue=0,
                new_position_in_queue=0,
            ),
        )

    except SQLAlchemyError as e:
        logger.exception(f"Ошибка при добавлении записи {user_name}")
        return None


async def update_record_cadastre(
        session: AsyncSession,
        user_uuid: uuid.UUID,
        new_user_name: str | None = None,
        new_priority: Priority | None = None,
        new_status: Stage | None = None,
) -> ModifiedUserData | None:
    """
    Обновляет запись по user_uuid, модифицируя только те поля, которые не None.
    Возвращает ModifiedUserData с old/new значениями.
    """
    # Получаем запись
    stmt = select(CadastralQueueRecords).where(
        CadastralQueueRecords.request_uuid == user_uuid
    )
    try:
        result = await session.execute(stmt)
        record = result.scalar_one_or_none()

    except SQLAlchemyError as e:
        logger.exception(f"Ошибка при получении записи {user_uuid}")
        return None

    if record is None:
        return None

    # Сохраняем старые значения
    old_user_name = record.user_name
    old_priority = record.priority.value if record.priority else None
    old_status = record.stage.value if record.stage else None

    # Модифицируем только не-None поля
    if new_user_name is not None:
        record.user_name = new_user_name

    if new_priority is not None:
        new_priority_record = await get_or_create_priority(session=session, priority=new_priority)
        if not new_priority_record:
            return None
        record.priority_id = new_priority_record.id

    if new_status is not None:
        new_status_record = await get_or_create_stage(session=session, stage=new_status)
        if not new_status_record:
            return None
        record.stage_id = new_status_record.id

    try:
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        logger.exception(f"Ошибка при обновлении записи {user_uuid}")
        return None

    # Собираем результат
    return ModifiedUserData(
        user_name=ModifiedUserName(
            old_user_name=old_user_name,
            new_user_name=record.user_name,
        ) if new_user_name is not None else None,
        priority=ModifiedPriority(
            old_priority=old_priority,
            new_priority=record.priority.value if record.priority else None,
        ) if new_priority is not None else None,
        status=ModifiedStatus(
            old_status=old_status,
            new_status=record.stage.value if record.stage else None,
        ) if new_status is not None else None,
        position_in_queue=None,
    )

async def add_record_cadastre_with_priority(
        session: AsyncSession,
        record_cadastre: ObjectsCadastresSchema,
        priority: Priority,
        user_name: str | None = None,
) -> str | None:
    """
    Add a record with a priority level.
    Returns the user_name on success, None on failure.
    """
    if user_name is None:
        user_name = str(uuid.uuid4())[:64]

    try:
        async with session.begin():
            cadastre_objects = await get_or_create_cadastre_objects(
                session=session,
                object_cadastre=record_cadastre,
            )
            stage = await get_or_create_stage(
                session=session,
                stage=Stage.IN_QUEUE,
            )
            priority_record = await get_or_create_priority(
                session=session,
                priority=priority,
            )

            new_record = CadastralQueueRecords(
                user_name=user_name,
                object_cadastres_id=cadastre_objects.id,
                stage_id=stage.id,
                priority_id=priority_record.id,
            )
            session.add(new_record)

        return user_name

    except SQLAlchemyError as e:
        logger.exception(f"Ошибка при добавлении записи с приоритетом {user_name}")
        return None


async def get_record_cadastre_with_priority(session: AsyncSession, user_name: str):
    """
    Get a record by its user_name.
    Returns RecordCadastreDataBase schema.
    """
    stmt = select(CadastralQueueRecords).where(CadastralQueueRecords.user_name == user_name)
    result = await session.execute(stmt)
    record = result.scalar_one_or_none()
    if record is None:
        return None
    return _record_to_db_schema(record)


async def set_priority_record_cadastre(
        session: AsyncSession,
        user_name: str,
        new_priority_value: int,
) -> dict:
    """
    Change the priority of a record that has not been calculated yet.
    History is automatically created by SQLAlchemy event listener.
    """
    try:
        priority = Priority(new_priority_value)
        priority_record = await get_or_create_priority(session=session, priority=priority)

        stmt = select(CadastralQueueRecords).where(
            CadastralQueueRecords.user_name == user_name
        )
        result = await session.execute(stmt)
        record = result.scalar_one_or_none()

        if record is None:
            raise ValueError(f"Record with user_name '{user_name}' not found")

        old_priority_id = record.priority_id
        record.priority_id = priority_record.id
        await session.commit()
        await session.refresh(record)

        return {
            'old_priority_id': old_priority_id,
            'new_priority_id': priority_record.id,
        }

    except (SQLAlchemyError, ValueError) as e:
        await session.rollback()
        logger.exception(f"Ошибка при изменении приоритета для {user_name}")
        raise


def _record_to_db_schema(record: CadastralQueueRecords) -> RecordCadastreDataBase:
    """Convert ORM model to Pydantic schema."""
    obj = record.object
    cadastre_number = {
        'cadastre_a': obj.cadastre_number.cadastre_a,
        'cadastre_b': obj.cadastre_number.cadastre_b,
        'cadastre_c': obj.cadastre_number.cadastre_c,
        'cadastre_k': obj.cadastre_number.cadastre_k,
    }
    coordinates = {
        'coordinate_x': obj.object_coordinates.coordinate_x,
        'coordinate_y': obj.object_coordinates.coordinate_y,
    }
    stage_code = record.stage.value if record.stage else None
    priority_value = record.priority.value if record.priority else None
    return RecordCadastreDataBase(
        cadastre_number=cadastre_number,
        coordinates=coordinates,
        stage=stage_code,
        user_name=record.user_name,
        priority=priority_value,
        key=record.user_name,
    )


async def get_cadastre_record_by_uuid(
        session: AsyncSession,
        user_uuid: uuid.UUID,
) -> DataBaseRecord | None:
    """Получаем request_uuid и статус из БД по user_uuid."""
    stmt = select(
        CadastralQueueRecords.request_uuid,
        StageStatus.value.label("stage_value"),
        CadastralQueueRecords.priority_id,
        CadastralQueueRecords.user_name,
    ).join(
        StageStatus, CadastralQueueRecords.stage_id == StageStatus.id
    ).where(
        CadastralQueueRecords.request_uuid == user_uuid
    )
    result = await session.execute(stmt)
    row = result.one_or_none()

    if row is None:
        return None

    return DataBaseRecord(
        request_uuid=row.request_uuid,
        user_name=row.user_name,
        status=row.stage_value,
        priority_int=row.priority_id,
    )


async def get_position_in_names_queue(session: AsyncSession, user_name: str) -> int:
    """Позиция записи в очереди (ORDER BY user_name ASC)."""
    stmt = (
        select(func.count())
        .select_from(CadastralQueueRecords)
        .join(StageStatus, CadastralQueueRecords.stage_id == StageStatus.id)
        .where(
            StageStatus.value == Stage.IN_QUEUE.value,
            CadastralQueueRecords.user_name < user_name,
        )
    )
    result = await session.execute(stmt)
    return result.scalar() + 1


async def get_queue_length(session: AsyncSession) -> int:
    """Общее количество записей в очереди."""
    stmt = (
        select(func.count())
        .select_from(CadastralQueueRecords)
        .join(StageStatus, CadastralQueueRecords.stage_id == StageStatus.id)
        .where(StageStatus.value == Stage.IN_QUEUE.value)
    )
    result = await session.execute(stmt)
    return result.scalar()


async def get_user_position_in_queue(session: AsyncSession, user_name: str) -> PositionInQueue:
    """
    Возвращает позицию пользователя в очереди и общую длину очереди одним запросом.
    """
    stmt = (
        select(
            func.count().filter(
                (CadastralQueueRecords.stage_id == StageStatus.id) &
                (StageStatus.value == Stage.IN_QUEUE.value) &
                (CadastralQueueRecords.user_name < user_name)
            ).label("position"),
            func.count().filter(
                (CadastralQueueRecords.stage_id == StageStatus.id) &
                (StageStatus.value == Stage.IN_QUEUE.value)
            ).label("queue_length"),
        )
        .select_from(CadastralQueueRecords)
        .join(StageStatus, CadastralQueueRecords.stage_id == StageStatus.id)
    )
    result = await session.execute(stmt)
    row = result.one_or_none()

    return PositionInQueue(
        position_in_queue=row.position + 1 if row.position is not None else 0,
        queue_length=row.queue_length if row.queue_length is not None else 0,
    )


async def get_queue_requests_items(session: AsyncSession) -> tuple[QueueItem, ...]:
    """
    Получает все элементы очереди с позициями.
    Возвращает кортеж QueueItem, отсортированный по user_name.
    """
    stmt = (
        select(
            CadastralQueueRecords.request_uuid,
            CadastralQueueRecords.user_name,
        )
        .join(StageStatus, CadastralQueueRecords.stage_id == StageStatus.id)
        .where(StageStatus.value == Stage.IN_QUEUE.value)
        .order_by(CadastralQueueRecords.user_name.asc())
    )
    result = await session.execute(stmt)
    rows = result.all()

    queue_items = []
    for idx, row in enumerate(rows, start=1):
        queue_items.append(
            QueueItem(
                request_uuid=row.request_uuid,
                user_name=row.user_name,
                position_in_queue=idx,
            )
        )

    return tuple(queue_items)