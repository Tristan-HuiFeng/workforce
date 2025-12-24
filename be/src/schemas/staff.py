from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class StaffOut(BaseModel):
    id: UUID
    full_name: str
    role_id: UUID
    user_id: UUID
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True

class StaffNoteOut(BaseModel):
    staff_id: UUID
    note: str
    status: str
    created_by: UUID
    created_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True

class IncidentOut(BaseModel):
    staff_id: UUID
    description: str
    type: str  # "incident" or "commendation"
    created_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True

class CertificationOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True
