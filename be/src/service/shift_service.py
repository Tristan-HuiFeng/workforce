from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.db.models.site import Site
from src.db.models.shift import Shift, ShiftTypeEnum
from src.db.models.shift_assignment import ShiftAssignment
from src.db.models.staff_certification import StaffCertification
from src.db.models.staff_site import StaffSite
from datetime import datetime, timedelta

MAX_WEEKLY_HOURS = 40

class ShiftService:

    @staticmethod
    def list_shifts(db: Session, user_id: str = None, site_id: str = None, start_date: datetime = None, end_date: datetime = None):
        query = db.query(Shift)
        if user_id:
            query = query.join(Shift.assignments).filter(ShiftAssignment.staff_id == user_id)
        if site_id:
            query = query.filter(Shift.site_id == site_id)
        if start_date and end_date:
            query = query.filter(Shift.shift_date.between(start_date, end_date))
        return query.order_by(Shift.shift_date).all()

    @staticmethod
    def get_shift(db: Session, shift_id: str):
        return db.query(Shift).filter(Shift.id == shift_id).first()

    @staticmethod
    def create_shift(db: Session, shift_data):

        shift_start = shift_data.start_time
        shift_end = shift_data.end_time

        if shift_start >= shift_end:
            raise ValueError("Shift start time must be before end time")

        site_exists = db.query(Site).filter(Site.id == shift_data.site_id).first()
        if not site_exists:
            raise ValueError(f"Site with id {shift_data.site_id} does not exist")
    
        overlapping = db.query(Shift).filter(
            Shift.site_id == shift_data.site_id,
            Shift.start_time < shift_end,
            Shift.end_time > shift_start
        ).first()
        if overlapping:
            raise ValueError("Shift times overlap with existing shift")
        
        shift = Shift(**shift_data.model_dump())
        db.add(shift)
        db.commit()
        db.refresh(shift)
        return shift

    @staticmethod
    def assign_staff(db: Session, shift_id: str, staff_id: str):
        shift = db.query(Shift).filter(Shift.id == shift_id).first()
        if not shift:
            raise ValueError("Shift not found")

        # Check staff assigned to site
        from src.db.models.staff_site import StaffSite
        staff_site = db.query(StaffSite).filter(
            StaffSite.staff_id == staff_id,
            StaffSite.site_id == shift.site_id
        ).first()
        if not staff_site:
            raise ValueError("Staff is not assigned to this site")

        # Check overlapping shifts
        existing = (
            db.query(ShiftAssignment)
            .join(Shift)
            .filter(
                ShiftAssignment.staff_id == staff_id,
                Shift.start_time < shift.end_time,
                Shift.end_time > shift.start_time,
                Shift.id != shift_id
            )
            .first()
        )
        if existing:
            raise ValueError("Staff already has overlapping shift")

        # Check night shift certification
        from src.db.models.staff_certification import StaffCertification
        staff_certs = db.query(StaffCertification).filter(
            StaffCertification.staff_id == staff_id,
            StaffCertification.expires_at >= datetime.utcnow().date(),
            StaffCertification.status == "ok"
        ).all()

        if shift.shift_type == "night":
            has_night_cert = any(c.certification.name == "Night Shift Clearance" for c in staff_certs)
            if not has_night_cert:
                raise ValueError("Staff missing required certification for night shift")

        # Check weekly hours
        from datetime import timedelta
        week_start = shift.shift_date - timedelta(days=shift.shift_date.weekday())
        week_end = week_start + timedelta(days=6)
        assignments = (
            db.query(ShiftAssignment)
            .join(Shift)
            .filter(
                ShiftAssignment.staff_id == staff_id,
                Shift.shift_date.between(week_start, week_end)
            )
            .all()
        )

        total_hours = sum(
            (a.shift.end_time - a.shift.start_time).total_seconds() / 3600
            for a in assignments
        )

        shift_hours = (shift.end_time - shift.start_time).total_seconds() / 3600
        if total_hours + shift_hours > MAX_WEEKLY_HOURS:
            raise ValueError(f"Assigning this shift exceeds weekly limit of {MAX_WEEKLY_HOURS} hours")

        assignment = ShiftAssignment(shift_id=shift_id, staff_id=staff_id)
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return assignment