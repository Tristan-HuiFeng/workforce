from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.core.dependencies import get_current_user
from src.db.models.user import User, UserRole
from src.schemas.certification import CertificationOut, StaffCertificationIn, StaffCertificationOut
from src.service.certification_service import CertificationService

router = APIRouter(prefix="/certifications", tags=["certifications"])

@router.get("/", response_model=list[CertificationOut])
def list_certifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CertificationService.list_certifications(db)

@router.get("/{cert_id}", response_model=CertificationOut)
def get_certification(cert_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cert = CertificationService.get_certification(db, cert_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    return cert

@router.get("/staff/{staff_id}", response_model=list[StaffCertificationOut])
def get_staff_certifications(staff_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return CertificationService.get_staff_certifications(db, staff_id)

@router.post("/staff", response_model=StaffCertificationOut)
def add_update_staff_certification(staff_cert: StaffCertificationIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.supervisor, UserRole.manager]:
        raise HTTPException(status_code=403, detail="Not allowed")
    return CertificationService.add_or_update_staff_certification(db, staff_cert)
