"""Здесь расположены контейнеры данных приложений для разных версий API"""

from dataclasses import dataclass, field
from uuid import UUID

from enums import Stage, Priority


@dataclass
class ModifiedUserName:
    """Схема измененного имени пользователя."""
    new_user_name: str = field(doc="Новое имя пользователя")
    old_user_name: str = field(doc="Старое имя пользователя")

@dataclass
class ModifiedPriority:
    """Схема измененного приоритета пользователя."""
    new_priority: int | None = field(doc="Новый приоритет")
    old_priority: int | None = field(doc="Старый приоритет")

@dataclass
class ModifiedStatus:
    """Схема измененного статуса пользователя."""
    new_status: str | None = field(doc="Новый статус")
    old_status: str | None = field(doc="Старый статус")

@dataclass
class PositionInQueue:
    """Позиция пользователя в очереди и общая длина очереди."""
    position_in_queue: int = field(default=0, doc="Позиция пользователя в очереди")
    queue_length: int = field(default=0, doc="Общая длина очереди")


@dataclass
class QueueItem:
    """Элемент очереди."""
    request_uuid: UUID = field(doc="UUID запроса")
    user_name: str = field(doc="Имя пользователя")
    position_in_queue: int = field(default=0, doc="Позиция в очереди")


@dataclass
class PriorityQueueItem:
    """Элемент очереди с приоритетом (API v2)."""
    request_uuid: UUID = field(doc="UUID запроса")
    priority: int = field(doc="Приоритет обработки")


@dataclass
class ModifiedPositionInQueue:
    """Схема измененной позиции в очереди."""
    new_position_in_queue: int = field(doc="Новая позиция в очереди")
    old_position_in_queue: int = field(doc="Старый номер в очереди")

@dataclass
class ModifiedUserData:
    """Схема измененных данных пользователя."""
    user_name: ModifiedUserName | None  = field(default=None, doc="Имя пользователя")
    priority: ModifiedPriority | None = field(default=None, doc="Приоритет пользователя")
    status: ModifiedStatus | None = field(default=None, doc="Статус пользователя")
    position_in_queue: ModifiedPositionInQueue | None = field(default=None, doc="Позиция в очереди")

@dataclass
class DataBaseRecord:
    """Схема базового записи в таблице базы данных."""
    request_uuid: UUID | None = field(default=None, doc="UUID запроса")
    user_name: str | None = field(default=None, doc="Имя пользователя")
    status: str | None = field(default=None, doc="Статус")
    priority_int: int | None = field(default=None, doc="Приоритет")
    position_in_queue: ModifiedPositionInQueue | None = field(default=None, doc="Позиция в очереди")

    @property
    def stage(self)-> Stage:
        return Stage(self.status)

    @property
    def priority(self)-> Priority:
        return Priority(self.priority_int)

    @property
    def request_uuid_is_empty(self)-> bool:
        return self.request_uuid is None

    @property
    def user_name_is_empty(self)-> bool:
        return self.user_name is None