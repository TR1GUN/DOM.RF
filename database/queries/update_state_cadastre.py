from database.models import CadastralQueueRecords, StageStatus
from database.setup_db import DataBase
from sqlalchemy import select


async def update_state_cadastre(user_name: str, stage_code: str) -> None:
    """
    Update the processing stage of a cadastre record by its user_name.
    Uses ORM update to trigger SQLAlchemy event listeners (history tracking, calculated flag).
    """
    async with DataBase.session_factory() as session:
        # Get stage by value
        stmt = select(StageStatus).where(StageStatus.value == stage_code)
        result = await session.execute(stmt)
        stage = result.scalar_one_or_none()
        if stage is None:
            return

        # Use ORM to trigger event listeners
        stmt = select(CadastralQueueRecords).where(CadastralQueueRecords.user_name == user_name)
        result = await session.execute(stmt)
        record = result.scalar_one_or_none()

        if record:
            record.stage_id = stage.id
            await session.commit()
