from fastapi import APIRouter

v3 = APIRouter(
    prefix='/v3',
    tags=['Cadastre'],
    responses={404: {"description": "Not found"}},
)

