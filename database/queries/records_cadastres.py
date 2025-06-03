from database.models import CadastreNumbers, ObjectCoordinates, RecordsCadastres
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.schemas_cadastre import RecordCadastreDataBase, RecordCadastre


async def get_cadastre_record_by_id(session: AsyncSession, cadastres_id: str) -> RecordCadastreDataBase | None:
    return await session.get(RecordsCadastres, cadastres_id)


async def add_record_cadastre(session: AsyncSession, record_cadastre: RecordCadastre) -> str:
    pass


async def rename_cadastre_index(session: AsyncSession, old_name: str, new_name: str) -> None:
    pass


async def add_record_cadastre_with_priority(session: AsyncSession, record_cadastre: RecordCadastre, priority: int):
    pass


async def get_record_cadastre_with_priority(session: AsyncSession, record_cadastre_id: int):
    pass


async def set_priority_record_cadastre(session: AsyncSession, record_cadastre_id: int, new_priority: int):
    pass
