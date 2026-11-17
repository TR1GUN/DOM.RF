from database.database_manager import DataBaseManager
from database.models import StageStatus, PriorityLevel
from database.models._base_model import _BaseModel
from sqlalchemy import select

DataBase = DataBaseManager()


async def init_db() -> None:
    """Создать таблицы, если они ещё не созданы."""
    async with DataBase.engine.begin() as connection:
        await connection.run_sync(_BaseModel.metadata.create_all)


async def init_stages():
    """
    Initialize default stage statuses in database.
    """
    async with DataBase.session_factory() as session:
        # Check if stages already exist
        result = await session.execute(select(StageStatus))
        if result.scalars().first():
            return

        stages = [
            StageStatus(value='created'),
            StageStatus(value='in_queue'),
            StageStatus(value='in_processing'),
            StageStatus(value='complete'),
        ]
        session.add_all(stages)
        await session.commit()


async def init_priorities():
    """
    Initialize default priority levels in database.
    """
    async with DataBase.session_factory() as session:
        # Check if priorities already exist
        result = await session.execute(select(PriorityLevel))
        if result.scalars().first():
            return

        priorities = [
            PriorityLevel(value=1),
            PriorityLevel(value=2),
        ]
        session.add_all(priorities)
        await session.commit()
