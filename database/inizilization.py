from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.setup_db import DataBase
from database.models._base_model import _BaseModel


@asynccontextmanager
async def lifespain(app: FastAPI):
    async with DataBase.engine.begin() as db:
        await db.run_sync(_BaseModel.metadata.create_all)
    yield
