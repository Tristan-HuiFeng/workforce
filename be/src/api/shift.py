from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.db.models.user import User, UserRole
from src.core.dependencies import get_current_user
from src.schemas.shift import ShiftIn, ShiftOut, ShiftAssignmentIn, ShiftAssignmentOut
from src.service.shift_service import ShiftService

router = APIRouter(prefix="/shifts", tags=["shifts"])

@router.get("/", response_model=list[ShiftOut])
def list_shifts(site_id: str = None, start_date: str = None, end_date: str = None,
        db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    if current_user.role == UserRole.manager:
        # Manager sees all shifts
        return ShiftService.list_shifts(db, site_id=site_id, start_date=start_date, end_date=end_date)
    elif current_user.role == UserRole.supervisor:
        # Supervisor sees shifts only for their site(s)
        # If site_id param is passed, further filter it
        return ShiftService.list_shifts(db, site_id=current_user.site_id, start_date=start_date, end_date=end_date)
    else:
        # Staff sees only their assigned shifts
        return ShiftService.list_shifts(db, user_id=current_user.id, site_id=site_id, start_date=start_date, end_date=end_date)

@router.get("/{shift_id}", response_model=ShiftOut)
def get_shift(shift_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    shift = ShiftService.get_shift(db, shift_id)
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    return shift

@router.post("/", response_model=ShiftOut)
def create_shift(shift: ShiftIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:

        if current_user.role == UserRole.manager:
            return ShiftService.create_shift(db, shift)
        
        if current_user.role == UserRole.supervisor and current_user.site_id == shift.site_id:
            return ShiftService.create_shift(db, shift)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

    raise HTTPException(status_code=403, detail="Not allowed")

@router.post("/assign", response_model=ShiftAssignmentOut)
def assign_staff(assignment: ShiftAssignmentIn, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.manager, UserRole.supervisor]:
        raise HTTPException(status_code=403, detail="Not allowed")
    try:
        return ShiftService.assign_staff(db, assignment.shift_id, assignment.staff_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
