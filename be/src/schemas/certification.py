from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date

class StaffCertificationIn(BaseModel):
    staff_id: UUID
    certification_id: UUID
    expires_at: date
    status: str  # "ok", "needs_attention", "critical"

class StaffCertificationOut(BaseModel):
    staff_id: UUID
    certification_id: UUID
    expires_at: date
    status: str

    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True

class CertificationOut(BaseModel):
    id: UUID
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True
