from enum import Enum


class Stage(Enum):
    """Processing stages with code and human-readable label."""
    CREATED = "created"
    IN_QUEUE = "in_queue"
    IN_PROCESSING = "in_processing"
    COMPLETE = "complete"
    FAILED = "failed"

    @property
    def label(self) -> str:
        """Human-readable label for the stage."""
        return {
            Stage.CREATED: "Создан",
            Stage.IN_QUEUE: "В очереди",
            Stage.IN_PROCESSING: "На обработке",
            Stage.COMPLETE: "Выполнен",
            Stage.FAILED: "Возникла ошибка",

        }[self]

    @property
    def color(self) -> str:
        """Human-readable label for the stage."""
        return {
            Stage.CREATED: "fefe22",   # Желтый
            Stage.IN_QUEUE: "0000ff", # Синий
            Stage.IN_PROCESSING: "8000ff", # Фиолетовый
            Stage.COMPLETE: "0f2e18", # Зеленый
            Stage.FAILED: "ff0000", # Красный
        }[self]