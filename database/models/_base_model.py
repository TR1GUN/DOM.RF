from sqlalchemy.orm import DeclarativeBase, declared_attr


class _BaseModel(DeclarativeBase):
    """
    Базовая модель для таблиц
    """
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
