import asyncio
import datetime
import typing
from types import TracebackType

from logger import BaseLogger
from managers.redis_manager import RedisManager
from managers.rabbit_mq_manager import CadastrePublisherRabbitMQManager

from worker_span.template import AsyncEventContext


class CadastreHandlerWorker:

    _logger: BaseLogger
    _broker_manager = None
    topic = 'cadastre'
    _check_delay = 10

    _stop = asyncio.Event()
    _force_rescan = asyncio.Event()
    _scanning_event = AsyncEventContext()

    # def __init__(self):
    #     _logger = BaseLogger('MessageManager')

    @classmethod
    async def run(cls) -> None:
        """
        Процедура запуска сканирования
        """
        cls._logger.debug(f'{cls.topic} manager main loop started')
        while not cls._stop.is_set():
            if cls._need_to_scan():
                cls._last_start_date = datetime.datetime.now()
                cls._force_rescan.clear()
                with cls._scanning_event:
                    await cls.exec_scan()
                cls._last_finish_date = datetime.datetime.now()
                await asyncio.sleep(5)
            else:
                await asyncio.sleep(1)

    @classmethod
    def stop(cls) -> None:
        """
        Остановка процедуры сканирования
        """
        cls._stop.is_set()

    @classmethod
    def _need_to_scan(cls) -> bool:
        """
        Выяснение нужно ли сканирование
        :return: True if scan is needed, False otherwise
        """
        time_has_come = (datetime.datetime.now() - cls._last_finish_date).seconds >= cls._check_delay
        return not cls._scanning_event.is_set() and (time_has_come or cls._force_rescan.is_set())

    async def exec_scan(self):
        """
        Сама процедура сканирования
        Получаем все наши записи
        :return:
        """
        scan = True
        while scan:
            # Берем последнее значение из очереди, удаляя его
            record = RedisManager.get_first_record_in_queue()
            if record:
                # Отправляем запись в rabbitMQ
                CadastrePublisherRabbitMQManager.send_message(message=record)
            # Если нет никакиъ
            else:
                RedisManager.reset_queue_count()
                break
