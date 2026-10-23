from datetime import datetime

from sqlalchemy import event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import logger
from database.models import CadastralQueueRecords, UserNameHistory, PriorityHistory


def register_event_listeners():
    """
    Register all SQLAlchemy event listeners.
    Call this function once during application startup.
    """
    # Listen for updates on CadastralQueueRecords
    event.listen(CadastralQueueRecords, "before_update", _capture_history_before_update)


def _capture_history_before_update(mapper, connection, target):
    """
    SQLAlchemy event listener that captures changes to user_name and priority_id
    before an update operation and creates history records automatically.
    
    This event is triggered by SQLAlchemy ORM before any UPDATE statement is executed
    on the CadastralQueueRecords table.
    
    Args:
        mapper: The mapper object
        connection: The SQLAlchemy connection
        target: The instance being updated
    """
    # Get the current session
    session = Session.object_session(target)
    if not session:
        return
    
    try:
        # Query the current state from the database
        current = (
            session.query(CadastralQueueRecords)
            .filter(CadastralQueueRecords.id == target.id)
            .first()
        )
        
        if not current:
            return
        
        # Check if user_name changed
        if hasattr(current, 'user_name') and current.user_name != target.user_name:
            history = UserNameHistory(
                record_id=target.id,
                old_user_name=current.user_name,
                new_user_name=target.user_name,
                changed_at=datetime.utcnow()
            )
            session.add(history)
        
        # Check if priority_id changed
        if current.priority_id != target.priority_id:
            history = PriorityHistory(
                record_id=target.id,
                old_priority_id=current.priority_id,
                new_priority_id=target.priority_id,
                changed_at=datetime.utcnow()
            )
            session.add(history)
        
        # Check if stage changed to 'complete' - automatically mark as calculated
        #
        # Consider moving this logic to runtime (Celery task) instead of ORM event
        # This would make the code cleaner and separate concerns (business logic vs ORM hooks)
        # Currently kept here for automatic state management during updates
        # NOTE: 'calculated' field is commented out in model - can be derived from stage.status

        # if current.stage_id != target.stage_id:
        #     current_stage = session.query(StageStatus).filter_by(id=current.stage_id).first()
        #     new_stage = session.query(StageStatus).filter_by(id=target.stage_id).first()
        #     
        #     if current_stage and new_stage and new_stage.code == 'complete' and current_stage.code != 'complete':
        #         target.calculated = True
    
    except SQLAlchemyError as e:
        logger.BaseLogger(name="HistoryEvent").error(
            f"Failed to create history record: {e}"
        )
