from sqlalchemy.orm import Session
from src.db.models.certification import Certification
from src.db.models.staff_certification import StaffCertification

class CertificationService:

    @staticmethod
    def list_certifications(db: Session):
        return db.query(Certification).all()

    @staticmethod
    def get_certification(db: Session, cert_id: str):
        return db.query(Certification).filter(Certification.id == cert_id).first()

    @staticmethod
    def get_staff_certifications(db: Session, staff_id: str):
        return (
            db.query(StaffCertification)
            .filter(StaffCertification.staff_id == staff_id)
            .all()
        )

    @staticmethod
    def add_or_update_staff_certification(db: Session, staff_cert):
        # staff_cert: Pydantic model with staff_id, certification_id, expires_at, status
        db_cert = db.query(StaffCertification).filter(
            StaffCertification.staff_id == staff_cert.staff_id,
            StaffCertification.certification_id == staff_cert.certification_id
        ).first()

        if db_cert:
            db_cert.expires_at = staff_cert.expires_at
            db_cert.status = staff_cert.status
        else:
            db_cert = StaffCertification(**staff_cert.model_dump())
            db.add(db_cert)

        db.commit()
        db.refresh(db_cert)
        return db_cert
