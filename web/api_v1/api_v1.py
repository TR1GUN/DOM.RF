from fastapi import APIRouter

from web.api_v1.endpoints.cadastre import cadastre as cadastre_api

v1 = APIRouter(
    prefix='/v1',
    tags=['Cadastre'],
    responses={404: {"description": "Not found"}},
)
v1.include_router(cadastre_api)
