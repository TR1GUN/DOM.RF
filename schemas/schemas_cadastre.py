import pydantic


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

    # -Кадастровый номер
    # -Координата х
    # -Координата у
    """
    cadastre_number: CadastreNumber = pydantic.Field()
    coordinates: CoordinateObject = pydantic.Field()


class PositionInQueue(pydantic.BaseModel):
    """

    """
    position: int
    len_queue: int
    key:str



class QueueCadastre(pydantic.BaseModel):
    """

    """
    queue: list[str] = pydantic.Field()
