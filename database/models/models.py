from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID as PgUUID
import uuid
from datetime import datetime

from database.models._base_model import _BaseModel


class StageStatus(_BaseModel):
    """
    Processing stage status table
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='Unique identifier')
    code: Mapped[str] = mapped_column(String, unique=True, comment='Stage code (created, in_queue, in_processing, complete)')
    name: Mapped[str] = mapped_column(String, comment='Stage display name')
    queue_records: Mapped[list["CadastralQueueRecords"]] = relationship(back_populates="stage")


class PriorityLevel(_BaseModel):
    """Priority level table."""
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='Unique identifier')
    value: Mapped[int] = mapped_column(Integer, unique=True, comment='Priority value (1 or 2)')
    name: Mapped[str] = mapped_column(String, unique=True, comment='Priority name')
    queue_records: Mapped[list["CadastralQueueRecords"]] = relationship(back_populates="priority")


class CadastreNumbers(_BaseModel):
    """ Cadastre Number table."""
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='Unique identifier')
    cadastre_a: Mapped[str] = mapped_column(String, comment='Region code (2 digits)')
    cadastre_b: Mapped[str] = mapped_column(String, comment='District code (2 digits)')
    cadastre_c: Mapped[str] = mapped_column(String, comment='Partition code (6-8 digits)')
    cadastre_k: Mapped[str] = mapped_column(String, comment='Quarter code (2 digits)')
    objects: Mapped[list["ObjectsCadastres"]] = relationship(back_populates="cadastre_number")


class ObjectCoordinates(_BaseModel):
    """Coordinates model table.

    - Coordinate х
    - Coordinate у
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='Unique identifier')
    coordinate_x: Mapped[float] = mapped_column(Float, comment='Latitude coordinate')
    coordinate_y: Mapped[float] = mapped_column(Float, comment='Longitude coordinate')
    objects: Mapped[list["ObjectsCadastres"]] = relationship(back_populates="object_coordinates")


class ObjectsCadastres(_BaseModel):
    """Cadastral object — combines cadastre number and coordinates."""
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment='Unique identifier')
    object_coordinates_id: Mapped[int] = mapped_column(Integer, ForeignKey('objectcoordinates.id'),
                                                       comment='FK to ObjectCoordinates')
    cadastre_number_id: Mapped[int] = mapped_column(Integer, ForeignKey('cadastrenumbers.id'),
                                                    comment='FK to CadastreNumbers')
    cadastre_number: Mapped["CadastreNumbers"] = relationship(foreign_keys="CadastreNumbers.id", back_populates="objects")
    object_coordinates: Mapped["ObjectCoordinates"] = relationship(foreign_keys="ObjectCoordinates.id", back_populates="objects")
    queue_records: Mapped[list["CadastralQueueRecords"]] = relationship(foreign_keys="CadastralQueueRecords.object_cadastres_id", back_populates="object")



class CadastralQueueRecords(_BaseModel):
    """Cadastral queue record — queue item linked to a cadastral object."""
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment='Unique identifier')
    request_uuid: Mapped[uuid.UUID] = mapped_column(PgUUID(as_uuid=True), unique=True, index=True, index_type='BTree', default=uuid.uuid4, comment='Unique request identifier (auto-generated)')
    user_name: Mapped[str] = mapped_column(String(64), unique=True, index=True, comment='User-facing request number (max 64 chars)')
    # This field can be derived from stage.status == 'complete' and doesn't need to be stored
    # calculated: Mapped[bool] = mapped_column(default=False, comment='Whether calculation is complete')
    stage_id: Mapped[int] = mapped_column(Integer, ForeignKey('stagestatus.id'), comment='FK to StageStatus')
    priority_id: Mapped[int] = mapped_column(Integer, ForeignKey('prioritylevel.id'), comment='FK to PriorityLevel')
    object_cadastres_id: Mapped[int] = mapped_column(Integer, ForeignKey('objectscadastres.id'), comment='FK to ObjectsCadastres')

    stage: Mapped["StageStatus"] = relationship(foreign_keys="StageStatus.id", back_populates="queue_records")
    priority: Mapped["PriorityLevel"] = relationship(foreign_keys="PriorityLevel.id", back_populates="queue_records")
    object: Mapped["ObjectsCadastres"] = relationship(back_populates="queue_records")
    name_history: Mapped[list["UserNameHistory"]] = relationship(back_populates="record", cascade="all, delete-orphan")
    priority_history: Mapped[list["PriorityHistory"]] = relationship(back_populates="record", cascade="all, delete-orphan")


class UserNameHistory(_BaseModel):
    """History of user_name changes for each queue record."""
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='Unique identifier')
    record_id: Mapped[int] = mapped_column(Integer, ForeignKey('cadastralqueuerecords.id'), comment='FK to CadastralQueueRecords')
    old_user_name: Mapped[str] = mapped_column(String(64), comment='Previous user_name value')
    new_user_name: Mapped[str] = mapped_column(String(64), comment='New user_name value')
    changed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, comment='When the change occurred')

    record: Mapped["CadastralQueueRecords"] = relationship(back_populates="name_history")


class PriorityHistory(_BaseModel):
    """History of priority changes for each queue record."""
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='Unique identifier')
    record_id: Mapped[int] = mapped_column(Integer, ForeignKey('cadastralqueuerecords.id'), comment='FK to CadastralQueueRecords')
    old_priority_id: Mapped[int] = mapped_column(Integer, comment='Previous priority_id')
    new_priority_id: Mapped[int] = mapped_column(Integer, comment='New priority_id')
    changed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, comment='When the change occurred')

    record: Mapped["CadastralQueueRecords"] = relationship(back_populates="priority_history")
