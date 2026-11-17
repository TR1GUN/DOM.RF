from datetime import datetime

from sqlalchemy import event, insert, select
from sqlalchemy.exc import SQLAlchemyError

import logger
from database.models import (
    CadastralQueueRecords,
    PriorityHistory,
    UserNameHistory,
)


def register_event_listeners():
    """
    Register all SQLAlchemy event listeners.
    Call this function once during application startup.
    """
    # Listen for updates on CadastralQueueRecords
    event.listen(CadastralQueueRecords, "before_update", _capture_history_before_update)


def _capture_history_before_update(mapper, connection, target):
    """
    Capture changes to user_name and priority_id before an UPDATE
    and write history rows through the same connection.

    Reading through the connection (instead of the session identity map)
    is important: the ORM object already contains the new values, while
    the database still has the old ones.
    """
    try:
        current = connection.execute(
            select(
                CadastralQueueRecords.user_name,
                CadastralQueueRecords.priority_id,
            ).where(CadastralQueueRecords.id == target.id)
        ).first()

        if current is None:
            return

        changed_at = datetime.utcnow()

        # Check if user_name changed
        if current.user_name != target.user_name:
            connection.execute(
                insert(UserNameHistory).values(
                    record_id=target.id,
                    old_user_name=current.user_name,
                    new_user_name=target.user_name,
                    changed_at=changed_at,
                )
            )

        # Check if priority_id changed
        if current.priority_id != target.priority_id:
            connection.execute(
                insert(PriorityHistory).values(
                    record_id=target.id,
                    old_priority_id=current.priority_id,
                    new_priority_id=target.priority_id,
                    changed_at=changed_at,
                )
            )

    except SQLAlchemyError as e:
        logger.BaseLogger(name="HistoryEvent").error(
            f"Failed to create history record: {e}"
        )
