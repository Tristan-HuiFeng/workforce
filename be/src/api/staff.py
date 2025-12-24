from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.db.models.user import User, UserRole
from src.core.dependencies import get_current_user
from src.schemas.staff import StaffOut, CertificationOut, IncidentOut, StaffNoteOut
from src.service.staff_service import StaffService

router = APIRouter(prefix="/staff", tags=["staff"])

@router.get("/{staff_id}", response_model=StaffOut)
def get_staff(staff_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    staff = StaffService.get_staff(db, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff

@router.get("/{staff_id}/certifications", response_model=list[CertificationOut])
def get_staff_certifications(staff_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StaffService.get_staff_certifications(db, staff_id)

@router.get("/{staff_id}/incidents", response_model=list[IncidentOut])
def get_staff_incidents(staff_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StaffService.get_staff_incidents(db, staff_id)

@router.get("/{staff_id}/notes", response_model=list[StaffNoteOut])
def get_staff_notes(staff_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return StaffService.get_staff_notes(db, staff_id)
