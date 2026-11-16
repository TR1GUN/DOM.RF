from fastapi import APIRouter

from web.api_v3.endpoints.cadastre import cadastre as cadastre_api

v3 = APIRouter(
    prefix="/v3",
    tags=["Cadastre"],
    responses={404: {"description": "Not found"}},
)
v3.include_router(cadastre_api)
