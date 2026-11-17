import uuid

from tasks.celery_app import celery_app
from api_client import BillingApi
from api_client.schemas import AnswerBillingCadastre
from schemas.cadastre_info import RecordCadastre, RecordCadastreInRedis, CadastreNumber, CoordinateObject
from settings.settings import settings_app


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
    name="cadastre:billing_request",
)
def billing_request(self, record: dict) -> dict:
    """
    Celery task that calls the Billing API to calculate cadastre data.
    Accepts a dict (serialized RecordCadastre), returns a dict.
    """
    try:
        record_obj = RecordCadastre(**record)
        api = BillingApi(url=settings_app.api.billing_cadastre_url)
        redis_record = RecordCadastreInRedis(
            request_uuid=uuid.uuid4(),
            cadastre_number=record_obj.cadastre_number,
            coordinates=record_obj.coordinates,
            calculated=False,
            user_name="",
        )
        result = api.calculate_cadastre(record=redis_record)
        return {"calculated": result.calculated}
    except Exception as exc:
        raise exc
