from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.session import Base
import uuid

class Certification(Base):
    __tablename__ = "certifications"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)

    staff_certifications = relationship("StaffCertification", back_populates="certification")
