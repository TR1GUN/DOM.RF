import logging
import typing
import sys


# class StdoutFormatter(logging.Formatter):
#     """Logging Formatter to add colors and count warning / errors"""
#
#     grey = '\033[90m'
#     yellow = '\033[93m'
#     white = '\33[97m'
#     red = '\033[91m'
#     green = '\033[92m'
#     bold_red = '\033[91m\033[1m'
#     blue = '\033[34m'
#     cyan = '\033[46m'
#     reset = '\033[0m'
#
#     FORMATS = {
#         logging.DEBUG: grey,
#         DEBUG_WARN: yellow,
#         logging.INFO: reset,
#         SUCCESS: green,
#         logging.WARNING: yellow,
#         logging.ERROR: red,
#         FAILURE: bold_red
#     }
#
#     def format(self, record: logging.LogRecord) -> str:
#         """Format record."""
#         return f'{self.FORMATS.get(record.levelno)}{super(StdoutFormatter, self).format(record)}{self.reset}'
#

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

        # self._primary_handler = logging.StreamHandler(stream=sys.stdout)
        # self._primary_handler.setLevel(level=level)
        # self._handlers[self._primary_handler] = logging.Formatter(
        #     fmt=f"[%(asctime)s] [{info}] >>> [%(levelname)s] %(message)s", datefmt=datefmt)

        self._printer = printer
        if self._printer:
            self._printer.setLevel(level=level)
            self._handlers[self._printer] = logging.Formatter(
                fmt=f"[{info}] >>> [%(levelname)s] %(message)s", datefmt=datefmt)

        # logging.addLevelName(SUCCESS, 'SUCCESS')
        # logging.addLevelName(FAILURE, 'FAILURE')

    # def success(self, msg: str, *args: typing.Any, **kwargs: typing.Any) -> None:
    #     """
    #     Log 'msg % args' with severity 'SUCCESS'.
    #     """
    #     if self.isEnabledFor(SUCCESS):
    #         self._log(SUCCESS, msg, args, **kwargs)
    #
    # def failure(self, msg: str, *args: typing.Any, **kwargs: typing.Any) -> None:
    #     """
    #     Log 'msg % args' with severity 'FAILURE'.
    #     """
    #     if self.isEnabledFor(FAILURE):
    #         self._log(FAILURE, msg, args, **kwargs)

    # def print(self, msg: str) -> None:
    #     """
    #     Directly writes message into stdout without formatting and level validation.
    #     For passing out machine-readable output.
    #     :param msg - message string
    #     """
    #     self._primary_handler.stream.write(f'{msg}{self._primary_handler.terminator}')
    #     self._primary_handler.flush()

    # def raw_emit(self, msg: str) -> None:
    #     """
    #     Writes to stdout, emits to websocket
    #     and stores in the printers content list
    #     passed message without formatting
    #     """
    #     if self._printer:
    #         self._printer.write(msg)

    # def callHandlers(self, record: logging.LogRecord) -> None:  # noqa: N802
    #     """Call handlers for record."""
    #     if record.levelno == logging.DEBUG:
    #         self._handle_record(self._primary_handler, record)
    #     else:
    #         for handler in self._handlers:
    #             self._handle_record(handler, record)

    def _handle_record(self, handler: logging.Handler, record: logging.LogRecord) -> None:
        msg = record.msg
        record.msg = self._handlers[handler].format(record)
        handler.handle(record)
        record.msg = msg