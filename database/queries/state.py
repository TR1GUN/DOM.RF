from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import StageStatus
from enums import Stage


async def get_or_create_stage(session: AsyncSession, stage: Stage) -> StageStatus:
    """Get stage by code or create it if not exists."""
    stmt = select(StageStatus).where(StageStatus.value == stage.value)
    result = await session.execute(stmt)
    stage_record = result.scalar_one_or_none()
    if stage_record is None:
        stage_record = StageStatus(value=stage.value)
        session.add(stage_record)
        await session.flush()
    return stage_record