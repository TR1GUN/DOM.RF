from enum import Enum


class Stage(Enum):
    """Processing stages with code and human-readable label."""
    CREATED = "created"
    IN_QUEUE = "in_queue"
    IN_PROCESSING = "in_processing"
    COMPLETE = "complete"

    @property
    def label(self) -> str:
        """Human-readable label for the stage."""
        return {
            Stage.CREATED: "Создан",
            Stage.IN_QUEUE: "В очереди",
            Stage.IN_PROCESSING: "На обработке",
            Stage.COMPLETE: "Выполнен",
        }[self]
