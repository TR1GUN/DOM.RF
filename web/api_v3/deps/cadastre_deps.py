from uuid import UUID

from fastapi import HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from database.setup_db import DataBase
from managers.redis_manager import RedisManager


async def get_db_session() -> AsyncSession:
    """Зависимость для получения сессии БД."""
    async with DataBase.session_factory() as session:
        yield session


def get_request_uuid(
    request_uuid: str = Path(..., description="Request UUID"),
) -> UUID:
    """Конвертация строкового request_uuid в UUID с проверкой."""
    try:
        return UUID(request_uuid)
    except (ValueError, AttributeError):
        raise HTTPException(status_code=400, detail="Invalid UUID format")


def get_redis_manager() -> RedisManager:
    """Зависимость для получения менеджера Redis-очереди."""
    return RedisManager()
