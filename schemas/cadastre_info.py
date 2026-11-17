from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field

from enums.stage import Stage

class CadastreNumber(BaseModel):
    """Cadastre Number schema."""

    model_config = ConfigDict(populate_by_name=True)

    cadastre_a: str = Field(alias="АА", min_length=2, max_length=2, description="Region code")
    cadastre_b: str = Field(alias="ВВ", min_length=2, max_length=2, description="District code")
    cadastre_c: str = Field(alias="CCCCСCC", min_length=6, max_length=8, description="Partition code")
    cadastre_k: str = Field(alias="КК", min_length=2, max_length=2, description="Quarter code")


class CoordinateObject(BaseModel):
    """Coordinate Object."""

    model_config = ConfigDict(populate_by_name=True)

    coordinate_x: float = Field(description="Latitude")
    coordinate_y: float = Field(description="Longitude")

class ObjectsCadastres(BaseModel):
    """Cadastre object schema."""
    cadastre_number: CadastreNumber = Field(description="Cadastre number")
    coordinates: CoordinateObject = Field(description="Object coordinates")


class RecordCadastre(BaseModel):
    """Данные кадастра, отправляемые на расчёт."""
    cadastre_number: CadastreNumber = Field(description="Кадастровый номер")
    coordinates: CoordinateObject = Field(description="Координаты объекта")


class RecordCadastreInRedis(RecordCadastre):
    """Запись кадастра, хранящаяся в Redis-очереди."""
    request_uuid: UUID = Field(description="UUID запроса")
    calculated: bool = Field(default=False, description="Признак завершения расчёта")
    user_name: str | None = Field(default=None, description="Имя пользователя")


class QueueCadastre(BaseModel):
    """Очередь запросов в Redis."""
    queue: list[str] = Field(default_factory=list, description="Ключи записей в порядке очереди")


class RecordCadastreDataBase(BaseModel):
    """Данные записи кадастра из БД."""
    cadastre_number: CadastreNumber = Field(description="Кадастровый номер")
    coordinates: CoordinateObject = Field(description="Координаты объекта")
    stage: str = Field(description="Статус обработки")
    user_name: str = Field(description="Имя пользователя")
    priority: int | None = Field(default=None, description="Приоритет обработки")
    key: str = Field(description="Ключ записи")



class RecordStageStatus(BaseModel):
    """Cadastre status schema."""
    status: Stage = Field(description="Cadastre status")

    @computed_field
    def name(self)-> str:
        return self.status.label

    @computed_field
    def color(self)-> str:
        return self.status.color


class PositionInQueue(BaseModel):
    """Схема позиции в очереди."""
    position_in_queue: int = Field(description="Позиция в очереди")
    queue_length: int = Field(description="Общая длина очереди")


# class RecordCadastreInRedis(pydantic.BaseModel):
#     """
#     Record cadastre in redis
#     """
#
#     cadastre_number: CadastreNumber = pydantic.Field()
#     coordinates: CoordinateObject = pydantic.Field()
#     calculated: bool
#     user_name: str = pydantic.Field(max_length=64)
#     key: str
#
#
# class PositionInQueue(pydantic.BaseModel):
#     """
#     Position in queue schema
#     """
#
#     position: int
#     len_queue: int
#     key: str
#
#
# class QueueCadastre(pydantic.BaseModel):
#     """ """
#
#     queue: list[str] = pydantic.Field()
#
#
# class RecordInfoRedis(pydantic.BaseModel):
#     """
#     Record info
#     """
#
#     user_name: str = pydantic.Field(max_length=64)
#     position_in_queue: PositionInQueue | None = pydantic.Field(default=None)
#     record: RecordCadastreInRedis | None = pydantic.Field(default=None)
#
#
# class RecordCadastreDataBase(pydantic.BaseModel):
#     """
#     Record cadastre in database
#     """
#
#     cadastre_number: CadastreNumber = pydantic.Field()
#     coordinates: CoordinateObject = pydantic.Field()
#     stage: str
#     user_name: str = pydantic.Field(max_length=64)
#     priority: int | None = pydantic.Field(default=None)
#     key: str
#
#
# class RecordCadastreControl(pydantic.BaseModel):
#     """
#     Record cadastre in database
#     """
#
#     record: RecordCadastreDataBase
#     position_in_queue: PositionInQueue | None = pydantic.Field(default=None)
#
#
# class UserNameHistorySchema(pydantic.BaseModel):
#     """Schema for user_name change history."""
#     id: int
#     old_user_name: str
#     new_user_name: str
#     changed_at: str
#
#
# class PriorityHistorySchema(pydantic.BaseModel):
#     """Schema for priority change history."""
#     id: int
#     old_priority_id: int
#     new_priority_id: int
#     changed_at: str
#
#
# class RecordWithHistory(pydantic.BaseModel):
#     """Record with history information."""
#     record: RecordCadastreDataBase
#     position_in_queue: PositionInQueue | None = pydantic.Field(default=None)
#     name_history: list[UserNameHistorySchema] = pydantic.Field(default_factory=list)
#     priority_history: list[PriorityHistorySchema] = pydantic.Field(default_factory=list)
