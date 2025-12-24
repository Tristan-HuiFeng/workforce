from sqlalchemy.orm import Session
from src.db.models.staff import Staff
from src.db.models.staff_site import StaffSite
from src.db.models.user import User
from src.db.models.certification import Certification
from src.db.models.staff_certification import StaffCertification
from src.db.models.incident import Incident
from src.db.models.staff_note import StaffNote

class StaffService:

    @staticmethod
    def get_staff(db: Session, staff_id: str):
        return db.query(Staff).filter(Staff.id == staff_id).first()

    @staticmethod
    def get_staff_certifications(db: Session, staff_id: str):
        return (
            db.query(StaffCertification)
            .filter(StaffCertification.staff_id == staff_id)
            .all()
        )

    @staticmethod
    def get_staff_incidents(db: Session, staff_id: str, limit: int = 5):
        return (
            db.query(Incident)
            .filter(Incident.staff_id == staff_id)
            .order_by(Incident.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_staff_notes(db: Session, staff_id: str):
        return db.query(StaffNote).filter(StaffNote.staff_id == staff_id).all()
