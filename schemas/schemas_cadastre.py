import pydantic

from enums import Stage


class CadastreNumber(pydantic.BaseModel):
    """
    Cadastre Number schema
    """
    cadastre_a: str = pydantic.Field(alias='АА', min_length=2, max_length=2, description="AA ")
    cadastre_b: str = pydantic.Field(alias='ВВ', min_length=2, max_length=2, description="BB ")
    cadastre_c: str = pydantic.Field(alias='CCCCСCC', min_length=6, max_length=8, description="CCCCСCC ")
    cadastre_k: str = pydantic.Field(alias='КК', min_length=2, max_length=2, description="KK ")


class CoordinateObject(pydantic.BaseModel):
    """
    Coordinate Object
    """
    coordinate_x: float
    coordinate_y: float


class RecordCadastre(pydantic.BaseModel):
    """
    Record cadastre
    """
    cadastre_number: CadastreNumber = pydantic.Field()
    coordinates: CoordinateObject = pydantic.Field()


class RecordCadastreInRedis(pydantic.BaseModel):
    """
    Record cadastre in redis
    """
    cadastre_number: CadastreNumber = pydantic.Field()
    coordinates: CoordinateObject = pydantic.Field()
    calculated: bool
    index: str


class PositionInQueue(pydantic.BaseModel):
    """
    Position in queue schema
    """
    position: int
    len_queue: int
    key: str


class QueueCadastre(pydantic.BaseModel):
    """

    """
    queue: list[str] = pydantic.Field()


class RecordInfoRedis(pydantic.BaseModel):
    """
    Record info
    """
    index: str
    position_in_queue: PositionInQueue | None = pydantic.Field(default=None)
    record: RecordCadastreInRedis | None = pydantic.Field(default=None)


class RecordCadastreDataBase(pydantic.BaseModel):
    """
    Record cadastre in database
    """
    cadastre_number: CadastreNumber = pydantic.Field()
    coordinates: CoordinateObject = pydantic.Field()
    stage: Stage
    key: str


class RecordCadastreControl(pydantic.BaseModel):
    """
    Record cadastre in database
    """
    record:RecordCadastreDataBase
    position_in_queue: PositionInQueue | None = pydantic.Field(default=None)
