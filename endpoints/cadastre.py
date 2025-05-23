from fastapi import APIRouter

from schemas.schemas_cadastre import RecordCadastre
from celery_tasks.celery_tasks import billing_request
cadastre = APIRouter(
    prefix='/cadastre',
    tags=['Cadastre'],
    responses={404: {"description": "Not found"}},
)


@cadastre.post('/accept', status_code=200)
async def set_cadastre_info(record_cadastre:RecordCadastre):
    """
    Принять запись кадастра
    :return:
    """
    print("--->")
    print(record_cadastre.dict(), type(record_cadastre.dict()))
    task = billing_request.apply_async(args=[*record_cadastre.dict()])
    print(task)
    lol = {"task_id": task.id}
    return lol



# @cadastre.get('/queue')
# def set_cadastre_info():
#     pass

# @cadastre.post('/queue')
# def set_cadastre_info():
#     pass

@cadastre.put('/queue')
def set_cadastre_info():
    """
    Поменять номер запроса в очереди запроса
    :return:
    """
    pass

@cadastre.post('/results')
def get_result_info():
    """
    Отдать результат запроса по ID
    :return:
    """
    pass

@cadastre.get('/results/{record}')
def get_result_info_by_id(record:int):
    """
    Отдать результат запроса по ID
    :return:
    """
    pass