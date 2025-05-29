import logging
import typing
import sys


class BaseLogger(logging.Logger):
    """
    Base Logger.
    """

    def __init__(
            self,
            name: str,
            level: typing.Optional[int] = None,
            printer: typing.Optional[logging.Handler] = None,
            **kwargs: typing.Any
    ) -> None:
        super().__init__(name)
        self.setLevel(level=level)

        datefmt = '%Y-%m-%d %H:%M:%S'
        info = f"{'|'.join([str(x) for x in kwargs.values()] + [name])}"
        self._handlers: typing.Dict[logging.Handler, logging.Formatter] = {}
        self._printer = printer
        if self._printer:
            self._printer.setLevel(level=level)
            self._handlers[self._printer] = logging.Formatter(
                fmt=f"[{info}] >>> [%(levelname)s] %(message)s", datefmt=datefmt)

    def _handle_record(self, handler: logging.Handler, record: logging.LogRecord) -> None:
        msg = record.msg
        record.msg = self._handlers[handler].format(record)
        handler.handle(record)
        record.msg = msg