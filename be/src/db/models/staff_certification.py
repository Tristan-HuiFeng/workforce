from datetime import date
from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.db.session import Base
import uuid

class StaffCertification(Base):
    __tablename__ = "staff_certifications"

    staff_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("staff.id"), primary_key=True)
    certification_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("certifications.id"), primary_key=True)
    expires_at: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String, default="ok")

    staff = relationship("Staff", back_populates="staff_certifications")
    certification = relationship("Certification", back_populates="staff_certifications")
