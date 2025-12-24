from sqlalchemy import ForeignKey, String, Enum, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from src.db.session import Base
import enum
import uuid
from datetime import datetime

class UserRole(enum.Enum):
    staff = "staff"
    supervisor = "supervisor"
    manager = "manager"

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    # created_at: Mapped = mapped_column(TIMESTAMP, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    site_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sites.id"), nullable=True)
    site = relationship("Site")
    staff = relationship("Staff", back_populates="user", uselist=False)