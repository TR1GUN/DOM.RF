from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import PriorityLevel
from enums import Priority


async def create_priority_level(session: AsyncSession, priority: Priority) -> PriorityLevel:
    """Create priority level."""
    priority_record = PriorityLevel(value=priority.value)
    session.add(priority_record)
    await session.flush()
    return priority_record

async def get_priority_level_id_by_priority_value(session: AsyncSession, priority: Priority) -> PriorityLevel:
    """Get priority level by value."""
    stmt = select(PriorityLevel).where(PriorityLevel.value == priority.value)
    result = await session.execute(stmt)
    return result.scalar_one()


async def get_or_create_priority(session: AsyncSession, priority:Priority) -> PriorityLevel:
    """Get priority by value or create it if not exists."""
    stmt = select(PriorityLevel).where(PriorityLevel.value == priority.value)
    result = await session.execute(stmt)
    priority_record = result.scalar_one_or_none()
    if priority_record is None:
        priority_record = await create_priority_level(session=session, priority=priority)
    return priority_record

