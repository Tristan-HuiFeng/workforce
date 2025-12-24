from sqlalchemy import String, TIMESTAMP, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Time, Date
from src.db.session import Base
from datetime import datetime, date
import uuid
from datetime import datetime
import enum

class ShiftTypeEnum(str, enum.Enum):
    morning = "morning"
    afternoon = "afternoon"
    night = "night"

class Shift(Base):
    __tablename__ = "shifts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    site_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sites.id"), nullable=False)
    shift_date: Mapped[date] = mapped_column(Date, nullable=False)
    shift_type: Mapped[ShiftTypeEnum] = mapped_column(Enum(ShiftTypeEnum), nullable=False)
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

    site = relationship("Site", back_populates="shifts")    
    assignments = relationship("ShiftAssignment", back_populates="shift")
