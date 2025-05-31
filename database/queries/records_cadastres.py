from database.models import CadastreNumbers, ObjectCoordinates, RecordsCadastres
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.schemas_cadastre import RecordCadastreInRedis


async def get_cadastres_by_id(session: AsyncSession, cadastres_id: int) -> RecordCadastreInRedis | None:
    return await session.get(RecordsCadastres, cadastres_id)


async def add_record_cadastre(session: AsyncSession, record_cadastre:RecordCadastreInRedis) -> int:
    pass

