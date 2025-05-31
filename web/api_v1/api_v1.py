from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.schemas_cadastre import RecordCadastre, PositionInQueue, QueueCadastre
from celery_tasks.celery_tasks import billing_request
from managers.redis_manager import RedisManager
from database.queries.records_cadastres import add_record_cadastre, get_cadastres_by_id
from database.setup_db import DataBase


v1 = APIRouter(
    prefix='/v1',
    tags=['Cadastre'],
    responses={404: {"description": "Not found"}},
)