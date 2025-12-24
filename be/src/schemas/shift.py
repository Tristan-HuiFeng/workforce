from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime, date
from typing import Optional, List

class ShiftIn(BaseModel):
    site_id: UUID
    shift_date: date
    shift_type: str
    start_time: datetime
    end_time: datetime

class ShiftOut(ShiftIn):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True

class ShiftAssignmentIn(BaseModel):
    shift_id: UUID
    staff_id: UUID

class ShiftAssignmentOut(ShiftAssignmentIn):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True
