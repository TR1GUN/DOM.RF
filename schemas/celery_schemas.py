import typing

from pydantic import BaseModel, Field


class CeleryTask(BaseModel):
    task_id: int = Field()
    task_status: typing.Any = Field()
    task_result: typing.Any = Field()
