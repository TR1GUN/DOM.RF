from enum import IntEnum


class Priority(IntEnum):
    """Priority levels with numeric value and human-readable label."""
    STANDARD = 1
    PREMIUM = 2

    @property
    def label(self) -> str:
        """Human-readable label for the priority."""
        return {
            Priority.STANDARD: "Обычная подписка",
            Priority.PREMIUM: "Премиум подписка",
        }[self]
