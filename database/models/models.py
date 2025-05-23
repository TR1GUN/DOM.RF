from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String

from database.models._base_model import _BaseModel


class CadastreNumbers(_BaseModel):
    """
    Cadastre Number schema
    - Кадастровый номер
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cadastre_a: Mapped[str]
    cadastre_b: Mapped[str]
    cadastre_c: Mapped[str]
    cadastre_k: Mapped[str]


class ObjectCoordinates(_BaseModel):
    """
    - Координата х
    - Координата у
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    coordinate_x: Mapped[float]
    coordinate_y: Mapped[float]


class RecordsCadastres(_BaseModel):
    """
    Основная таблица

    - Кадастровый номер
    - Координаты х\у
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cadastre_number: Mapped['CadastreNumbers'] = relationship(foreign_keys='CadastreNumbers.id')
    object_coordinates: Mapped['ObjectCoordinates'] = relationship(foreign_keys='ObjectCoordinates.id')
    calculated: Mapped[bool]


