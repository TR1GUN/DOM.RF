from celery import shared_task

from api_client import BillingApi
from api_client.schemas import AnswerBillingCadastre
from config import Settings


@shared_task(bind=True,
             autoretry_for=(Exception,),
             retry_backoff=True,
             retry_kwargs={'max_retries': 5},
             name='cadastre:billing_request')
def billing_request(record: dict) -> AnswerBillingCadastre:
    api = BillingApi(url=Settings.api.billing_cadastre_url)
    return api.calculate_cadastre(record=record)
