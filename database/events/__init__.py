"""
SQLAlchemy event listeners package.

This package contains event listeners that automatically track changes
and create history records.
"""

from .history_events import register_event_listeners

__all__ = ["register_event_listeners"]
