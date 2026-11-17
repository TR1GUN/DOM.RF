from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from database.models import CadastreNumbers, ObjectCoordinates, ObjectsCadastres
from schemas.cadastre_info import (
    ObjectsCadastres as ObjectsCadastresSchema,
    CoordinateObject as ObjectCoordinatesSchema,
    CadastreNumber as CadastreNumbersSchema,
)
from logger.logger import BaseLogger

logger = BaseLogger(__name__)


async def _get_or_create_object_coordinates_id(
        session: AsyncSession,
        coordinate_x: float,
        coordinate_y: float,
) -> int:
    """Атомарно получает или создаёт ObjectCoordinates. Возвращает ID."""
    stmt = pg_insert(ObjectCoordinates).values(
        coordinate_x=coordinate_x,
        coordinate_y=coordinate_y,
    ).on_conflict_do_nothing(
        index_elements=['coordinate_x', 'coordinate_y'],
    ).returning(ObjectCoordinates.id)

    result = await session.execute(stmt)
    record_id = result.scalar_one_or_none()

    if record_id is not None:
        return record_id

    # Conflict — получаем существующий ID
    result = await session.execute(
        select(ObjectCoordinates.id).where(
            (ObjectCoordinates.coordinate_x == coordinate_x) &
            (ObjectCoordinates.coordinate_y == coordinate_y)
        )
    )
    return result.scalar_one()


async def _get_or_create_cadastre_number_id(
        session: AsyncSession,
        cadastre_a: str,
        cadastre_b: str,
        cadastre_c: str,
        cadastre_k: str,
) -> int:
    """Атомарно получает или создаёт CadastreNumbers. Возвращает ID."""
    stmt = pg_insert(CadastreNumbers).values(
        cadastre_a=cadastre_a,
        cadastre_b=cadastre_b,
        cadastre_c=cadastre_c,
        cadastre_k=cadastre_k,
    ).on_conflict_do_nothing(
        index_elements=['cadastre_a', 'cadastre_b', 'cadastre_c', 'cadastre_k'],
    ).returning(CadastreNumbers.id)

    result = await session.execute(stmt)
    record_id = result.scalar_one_or_none()

    if record_id is not None:
        return record_id

    # Conflict — получаем существующий ID
    result = await session.execute(
        select(CadastreNumbers.id).where(
            (CadastreNumbers.cadastre_a == cadastre_a) &
            (CadastreNumbers.cadastre_b == cadastre_b) &
            (CadastreNumbers.cadastre_c == cadastre_c) &
            (CadastreNumbers.cadastre_k == cadastre_k)
        )
    )
    return result.scalar_one()


async def _get_or_create_object_cadastre_id(
        session: AsyncSession,
        cadastre_number_id: int,
        object_coordinates_id: int,
) -> int:
    """Атомарно получает или создаёт ObjectsCadastres. Возвращает ID."""
    stmt = pg_insert(ObjectsCadastres).values(
        cadastre_number_id=cadastre_number_id,
        object_coordinates_id=object_coordinates_id,
    ).on_conflict_do_nothing(
        index_elements=['object_coordinates_id', 'cadastre_number_id'],
    ).returning(ObjectsCadastres.id)

    result = await session.execute(stmt)
    record_id = result.scalar_one_or_none()

    if record_id is not None:
        return record_id

    # Conflict — получаем существующий ID
    result = await session.execute(
        select(ObjectsCadastres.id).where(
            (ObjectsCadastres.object_coordinates_id == object_coordinates_id) &
            (ObjectsCadastres.cadastre_number_id == cadastre_number_id)
        )
    )
    return result.scalar_one()


async def _flush_and_get(session: AsyncSession, model: type, record_id: int):
    """Flush и получить запись из identity map."""
    await session.flush()
    obj = await session.get(model, record_id)
    if obj is not None:
        return obj

    result = await session.execute(select(model).where(model.id == record_id))
    return result.scalar_one()


# Вариант 1 — Выполняем все одной транзакцией
async def get_id_cadastre_objects(
        session: AsyncSession,
        object_cadastre: ObjectsCadastresSchema,
) -> int | None:
    """
    Атомарно вставляет/получает цепочку через один CTE-запрос.
    
    Каждый шаг: INSERT с RETURNING + COALESCE с SELECT при конфликте.
    """

    # 1. Upsert CadastreNumbers
    stmt_cad = pg_insert(CadastreNumbers).values(
        cadastre_a=object_cadastre.cadastre_number.cadastre_a,
        cadastre_b=object_cadastre.cadastre_number.cadastre_b,
        cadastre_c=object_cadastre.cadastre_number.cadastre_c,
        cadastre_k=object_cadastre.cadastre_number.cadastre_k,
    ).on_conflict_do_nothing(
        index_elements=['cadastre_a', 'cadastre_b', 'cadastre_c', 'cadastre_k']
    )

    stmt_get_cad = select(CadastreNumbers.id).where(
        (CadastreNumbers.cadastre_a == object_cadastre.cadastre_number.cadastre_a) &
        (CadastreNumbers.cadastre_b == object_cadastre.cadastre_number.cadastre_b) &
        (CadastreNumbers.cadastre_c == object_cadastre.cadastre_number.cadastre_c) &
        (CadastreNumbers.cadastre_k == object_cadastre.cadastre_number.cadastre_k)
    )

    # 2. Upsert ObjectCoordinates
    stmt_coord = pg_insert(ObjectCoordinates).values(
        coordinate_x=object_cadastre.coordinates.coordinate_x,
        coordinate_y=object_cadastre.coordinates.coordinate_y,
    ).on_conflict_do_nothing(
        index_elements=['coordinate_x', 'coordinate_y']
    )

    stmt_get_coord = select(ObjectCoordinates.id).where(
        (ObjectCoordinates.coordinate_x == object_cadastre.coordinates.coordinate_x) &
        (ObjectCoordinates.coordinate_y == object_cadastre.coordinates.coordinate_y)
    )

    async with session.begin():  # транзакция
        res_cad = await session.execute(stmt_cad)
        if res_cad.rowcount == 0:
            # уже существует — ищем ID
            res = await session.execute(stmt_get_cad)
            cad_id = res.scalar()
        else:
            cad_id = res_cad.inserted_primary_key[0]

        res_coord = await session.execute(stmt_coord)
        if res_coord.rowcount == 0:
            res = await session.execute(stmt_get_coord)
            coord_id = res.scalar()
        else:
            coord_id = res_coord.inserted_primary_key[0]

        # 3. Upsert ObjectsCadastres (связь)
        stmt_link = pg_insert(ObjectsCadastres).values(
            object_coordinates_id=coord_id,
            cadastre_number_id=cad_id,
        ).on_conflict_do_nothing(
            index_elements=['object_coordinates_id', 'cadastre_number_id']
        )
        res_link = await session.execute(stmt_link)

        if res_link.rowcount != 0:
            cadastre_obj_id = res_link.inserted_primary_key[0]
        else:
            # связь уже есть — достаём ID
            stmt_get_link = select(ObjectsCadastres.id).where(
                (ObjectsCadastres.object_coordinates_id == coord_id) &
                (ObjectsCadastres.cadastre_number_id == cad_id)
            )
            res = await session.execute(stmt_get_link)
            cadastre_obj_id = res.scalars().first()

    return cadastre_obj_id


# Вариант 2 — атомарные операции с ON CONFLICT DO NOTHING RETURNING
# Расширяемо, безопасен при race condition благодаря UNIQUE constraint + RETURNING
async def get_or_create_object_coordinates(
        session: AsyncSession,
        coordinates: ObjectCoordinatesSchema,
) -> ObjectCoordinates:
    """Получает или создаёт ObjectCoordinates."""
    try:
        coord_id = await _get_or_create_object_coordinates_id(
            session,
            coordinate_x=coordinates.coordinate_x,
            coordinate_y=coordinates.coordinate_y,
        )
        return await _flush_and_get(session, ObjectCoordinates, coord_id)
    except Exception:
        logger.exception("Ошибка при создании ObjectCoordinates")
        raise


async def get_or_create_cadastre_number(
        session: AsyncSession,
        cadastre_number: CadastreNumbersSchema,
) -> CadastreNumbers:
    """Получает или создаёт CadastreNumbers."""
    try:
        cad_id = await _get_or_create_cadastre_number_id(
            session,
            cadastre_a=cadastre_number.cadastre_a,
            cadastre_b=cadastre_number.cadastre_b,
            cadastre_c=cadastre_number.cadastre_c,
            cadastre_k=cadastre_number.cadastre_k,
        )
        return await _flush_and_get(session, CadastreNumbers, cad_id)
    except Exception:
        logger.exception("Ошибка при создании CadastreNumbers")
        raise


async def get_or_create_cadastre_objects(
        session: AsyncSession,
        object_cadastre: ObjectsCadastresSchema,
) -> ObjectsCadastres:
    """Получает или создаёт ObjectsCadastres в одной транзакции."""
    cadastre_number = object_cadastre.cadastre_number
    coordinates = object_cadastre.coordinates

    try:
        # Транзакцией управляет вызывающий код: так проще комбинировать
        # создание объекта и постановку записи в очередь в одной транзакции.
        object_coordinates = await get_or_create_object_coordinates(session, coordinates)
        cadastre_number_record = await get_or_create_cadastre_number(session, cadastre_number)

        # 2. ObjectsCadastres — атомарно через ON CONFLICT DO NOTHING RETURNING
        obj_id = await _get_or_create_object_cadastre_id(
            session,
            cadastre_number_id=cadastre_number_record.id,
            object_coordinates_id=object_coordinates.id,
        )

        return await _flush_and_get(session, ObjectsCadastres, obj_id)

    except Exception:
        logger.exception(
            f"Ошибка при создании ObjectsCadastres "
            f"({cadastre_number.cadastre_a}, {coordinates.coordinate_x})"
        )
        raise


async def get_id_cadastre_objects_by_object_cadastre(
        session: AsyncSession,
        object_cadastre: ObjectsCadastresSchema,
) -> int | None:
    """Возвращает ID ObjectsCadastres, создавая цепочку если нет."""
    try:
        cadastre_objects = await get_or_create_cadastre_objects(
            session=session,
            object_cadastre=object_cadastre,
        )
        return cadastre_objects.id
    except Exception:
        logger.exception("Ошибка при получении ID ObjectsCadastres")
        await session.rollback()
        raise
