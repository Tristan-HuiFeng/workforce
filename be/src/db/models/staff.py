from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.session import Base
import uuid

class Staff(Base):
    __tablename__ = "staff"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    role_id: Mapped[uuid.UUID] = mapped_column(String, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)

    # Relationships
    user = relationship("User", back_populates="staff")
    staff_sites = relationship("StaffSite", back_populates="staff")
    staff_certifications = relationship("StaffCertification", back_populates="staff")
    incidents = relationship("Incident", back_populates="staff")
    notes = relationship("StaffNote", back_populates="staff")
    shift_assignments = relationship("ShiftAssignment", back_populates="staff")