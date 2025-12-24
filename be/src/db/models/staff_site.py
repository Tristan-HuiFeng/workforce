from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.session import Base
import uuid

class StaffSite(Base):
    __tablename__ = "staff_sites"

    staff_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("staff.id"), primary_key=True)
    site_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sites.id"), primary_key=True)

    # Relationships
    staff = relationship("Staff", back_populates="staff_sites")
    site = relationship("Site", back_populates="staff_sites")
