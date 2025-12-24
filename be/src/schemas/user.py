from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
import enum
import uuid
from datetime import datetime

class UserRole(str, enum.Enum):
    staff = "staff"
    supervisor = "supervisor"
    manager = "manager"

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole

# class UserCreate(UserBase):
#     password: str

# class UserUpdate(BaseModel):
#     email: Optional[EmailStr]
#     password: Optional[str]
#     role: Optional[UserRole]

class UserOut(UserBase):
    id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"