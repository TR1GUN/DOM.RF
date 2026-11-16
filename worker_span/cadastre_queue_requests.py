import asyncio
import datetime

from api_client import BillingApi
from settings.settings import settings_app
from logger import BaseLogger
from managers.redis_manager import RedisManager
from schemas.cadastre_info import RecordCadastreInRedis
from worker_span.template import AsyncEventContext

from database.queries import update_state_cadastre


class CadastreHandlerWorker:

    _logger: BaseLogger
    _broker_manager: RedisManager | None = None
    _topic: str
    _check_delay = 10

    _stop = asyncio.Event()
    _force_rescan = asyncio.Event()
    _main_event = AsyncEventContext()

    def __init__(self, topic: str):
        self._topic = topic
        self._logger = BaseLogger(name=self._topic)
        self._broker_manager = RedisManager(topic=topic)

    @classmethod
    async def run(cls) -> None:
        """
        Started managers
        """
        cls._logger.debug(f"{cls._topic} manager main loop started")
        cls._last_finish_date = datetime.datetime.now()
        while not cls._stop.is_set():
            if cls._need_start():
                cls._last_start_date = datetime.datetime.now()
                cls._force_rescan.clear()
                with cls._main_event:
                    await cls.exec_record_processing()
                cls._last_finish_date = datetime.datetime.now()
                await asyncio.sleep(5)
            else:
                await asyncio.sleep(1)

    @classmethod
    def stop(cls) -> None:
        """
        Stop managers
        """
        cls._stop.set()

    @classmethod
    def _need_start(cls) -> bool:
        """
        Needed start main loop
        :return: True if scan is needed, False otherwise
        """
        time_has_come = (datetime.datetime.now() - cls._last_finish_date).seconds >= cls._check_delay
        return not cls._main_event.is_set() and (time_has_come or cls._force_rescan.is_set())

    async def exec_record_processing(self):
        """
        Execution of the procedure for calculating records
        :return:
        """
        scan = True
        while scan:
            record = self._broker_manager.get_first_record_in_queue()
            if record:
                await self.record_processing(record=record)
            else:
                self._broker_manager.reset_queue_count()
                break

    async def record_processing(self, record: RecordCadastreInRedis):
        """
        processing message
        :return:
        """
        result = await self._billing_request(record=record)
        if result:
            self._broker_manager.delete_record(key=record.key)
            stage = 'complete'
            self._logger.complete(f"Record for key {record.key} completed!")
        else:
            self._broker_manager.add_element_in_queue(key=record.key)
            self._logger.error(f"Record for key {record.key} error! message moved to the end of the queue")
            stage = 'in_queue'
        await update_state_cadastre(user_name=record.user_name, stage=stage)

    async def _billing_request(self, record: RecordCadastreInRedis) -> bool:
        api = BillingApi(url=settings_app.api.billing_cadastre_url)
        result = api.calculate_cadastre(record=record)
        return result.calculated
