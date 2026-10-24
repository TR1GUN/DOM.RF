from uuid import UUID

from fastapi import HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from database.setup_db import DataBase


async def get_db_session()->AsyncSession:
    """Зависимость для получения DB сессии."""
    return DataBase().get_scoped_session()



def get_user_uuid(user_uuid: str = Path(..., description="User UUID")) -> UUID:
    """Конвертация строкового user_uuid в UUID с проверкой."""
    try:
        return UUID(user_uuid)
    except (ValueError, AttributeError):
        raise HTTPException(status_code=400, detail="Invalid UUID format")
