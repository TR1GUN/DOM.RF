import logging
import typing
import sys


COMPLETE = 25


class StdoutFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    grey = '\033[90m'
    yellow = '\033[93m'
    white = '\33[97m'
    red = '\033[91m'
    green = '\033[92m'
    blue = '\033[34m'

    FORMATS = {
        logging.DEBUG: white,
        logging.INFO: blue,
        COMPLETE: green,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: red
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format record."""
        return f'{self.FORMATS.get(record.levelno)}{super(StdoutFormatter, self).format(record)}'


class BaseLogger(logging.Logger):
    """
    Base Logger.
    """
    _date_format = '%Y-%m-%d %H:%M:%S'

    _handlers: typing.Dict[logging.Handler, logging.Formatter] = {}

    def __init__(
            self,
            name: str,
            **kwargs: typing.Any
    ) -> None:
        super().__init__(name)
        self.setLevel(level=0)
        self._handlers[logging.StreamHandler(stream=sys.stdout)] = StdoutFormatter(
            fmt=f"[%(asctime)s][%(levelname)s]{name} >>>  %(message)s", datefmt=self._date_format)

    def callHandlers(self, record: logging.LogRecord) -> None:
        """Call handlers for record."""
        for handler in self._handlers:
            self._handle_record(handler, record)

    def _handle_record(self, handler: logging.Handler, record: logging.LogRecord) -> None:
        msg = record.msg
        record.msg = self._handlers[handler].format(record)
        handler.handle(record)
        record.msg = msg

    def complete(self, msg: str, *args: typing.Any, **kwargs: typing.Any) -> None:
        """
        Log with severity 'COMPLETE'.
        """
        if self.isEnabledFor(COMPLETE):
            self._log(COMPLETE, msg, args, **kwargs)
