from fastapi import APIRouter

from web.api_v2.endpoints.cadastre import cadastre as cadastre_api

v2 = APIRouter(
    prefix='/v2',
    tags=['Cadastre'],
    responses={404: {"description": "Not found"}},
)
v2.include_router(cadastre_api)
