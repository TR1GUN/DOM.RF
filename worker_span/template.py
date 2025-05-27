
class AsyncEventContext:
    """
    Async event context
    """

    def __init__(self) -> None:
        self._event = asyncio.Event()

    def is_set(self) -> bool:
        """
        Return true if event is set
        """
        return self._event.is_set()

    def set(self) -> None:
        """
        Event context set
        """
        self._event.set()

    def clear(self) -> None:
        """
        Clear the event context
        """
        self._event.clear()

    def __enter__(self) -> None:
        self._event.set()

    def __exit__(self,
                 exc_type: Exception,
                 exc_val: Exception,
                 exc_tb: typing.Optional[TracebackType]
                 ) -> None:
        self._event.clear()
