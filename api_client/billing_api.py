import random
import time

from api_client.schemas import AnswerBillingCadastre


class BillingApi:
    _url: str | None = None

    def __init__(self, url: str):
        self._url = url

    def calculate_cadastre(self, record:dict) -> AnswerBillingCadastre:
        """
        Отправка на расчет в биллинг
        :return:
        """
        print(f'request to {self._url}')
        time.sleep(random.randint(10, 60))
        answer = {'calculated': True}

        return AnswerBillingCadastre.model_validate(answer)
