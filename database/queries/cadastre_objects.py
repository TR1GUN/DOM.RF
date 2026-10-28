from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import select


from database.models import CadastreNumbers, ObjectCoordinates, ObjectsCadastres
from schemas.cadastre_info import ObjectsCadastres as ObjectsCadastresSchema , CoordinateObject as ObjectCoordinatesSchema, CadastreNumber as CadastreNumbersSchema

# Вариант 1 - Выполняем все одной транзакцией
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


# Вариант 2 - Поскольку у нас есть асинхронность и есть не блокирующие вызовы - можно разделить все операции на атомарные транзакции
# Более расширяемо, но не всегда производительно
async def get_or_create_object_coordinates(session:AsyncSession , coordinates:ObjectCoordinatesSchema)->ObjectCoordinates:
    stmt = select(ObjectCoordinates).where((ObjectCoordinates.coordinate_x == coordinates.coordinate_x) &
            (ObjectCoordinates.coordinate_y == coordinates.coordinate_y))
    result = await session.execute(stmt)
    coordinates_record = result.scalar_one_or_none()
    if coordinates_record is None:
        coordinates_record = ObjectCoordinates(coordinate_x=coordinates.coordinate_x, coordinate_y=coordinates.coordinate_y)
        session.add(coordinates_record)
        await session.flush()
    return coordinates_record


async def get_or_create_cadastre_number(session:AsyncSession, cadastre_number:CadastreNumbersSchema)->CadastreNumbers:
    stmt = select(CadastreNumbers).where(
            (CadastreNumbers.cadastre_a == cadastre_number.cadastre_a) &
            (CadastreNumbers.cadastre_b == cadastre_number.cadastre_b) &
            (CadastreNumbers.cadastre_c == cadastre_number.cadastre_c) &
            (CadastreNumbers.cadastre_k == cadastre_number.cadastre_k)
    )
    result = await session.execute(stmt)
    cadastre_number_record = result.scalar_one_or_none()
    if cadastre_number_record is None:
        cadastre_number_record = CadastreNumbers(
            cadastre_a = cadastre_number.cadastre_a,
            cadastre_b = cadastre_number.cadastre_b,
            cadastre_c = cadastre_number.cadastre_c,
            cadastre_k = cadastre_number.cadastre_k
        )
        session.add(cadastre_number_record)
        await session.flush()
    return cadastre_number_record


async def get_or_create_cadastre_objects(session: AsyncSession, object_cadastre: ObjectsCadastresSchema,) -> ObjectsCadastres:
    """Get cadastre objects by value object cadastre or create it if not exists."""
    stmt = (
        select(
            ObjectsCadastres
        ).
        join(
            CadastreNumbers, CadastreNumbers.id == ObjectsCadastres.cadastre_number_id
        ).
        join(
            ObjectCoordinates, ObjectCoordinates.id == ObjectsCadastres.object_coordinates_id
        ).
        where(
            (ObjectCoordinates.coordinate_x == object_cadastre.coordinates.coordinate_x) &
            (ObjectCoordinates.coordinate_y == object_cadastre.coordinates.coordinate_y) &
            (CadastreNumbers.cadastre_a == object_cadastre.cadastre_number.cadastre_a) &
            (CadastreNumbers.cadastre_b == object_cadastre.cadastre_number.cadastre_b) &
            (CadastreNumbers.cadastre_c == object_cadastre.cadastre_number.cadastre_c) &
            (CadastreNumbers.cadastre_k == object_cadastre.cadastre_number.cadastre_k))
    )
    result = await session.execute(stmt)
    objects_cadastres_record = result.scalar_one_or_none()
    if objects_cadastres_record is None:
        object_coordinates = await get_or_create_object_coordinates(session=session, coordinates=object_cadastre.coordinates)
        cadastre_number = await  get_or_create_cadastre_number(session=session, cadastre_number=object_cadastre.cadastre_number)
        objects_cadastres_record = ObjectsCadastres(
            object_coordinates_id = object_coordinates.id ,
            cadastre_number_id= cadastre_number.id
            )
        session.add(objects_cadastres_record)
        await session.flush()
    return objects_cadastres_record


async def get_id_cadastre_objects_by_object_cadastre(
        session: AsyncSession,
        object_cadastre: ObjectsCadastresSchema,
) -> int | None:
    """
    """
    cadastre_objects = await get_or_create_cadastre_objects(session=session, object_cadastre=object_cadastre)
    if cadastre_objects:
        return cadastre_objects.id
    return None