import random
import time

from api_client.schemas import AnswerBillingCadastre
from schemas.schemas_cadastre import RecordCadastreInRedis


class BillingApi:
    """
    Mock class for billing api
    """
    _url: str | None = None

    def __init__(self, url: str):
        self._url = url

    def calculate_cadastre(self, record:RecordCadastreInRedis) -> AnswerBillingCadastre:
        """
        Sending for calculation to billing
        :return:
        """
        print(f'request to {self._url}', record)
        time.sleep(random.randint(10, 60))
        answer = {'calculated': True}

        return AnswerBillingCadastre.model_validate(answer)
