
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session
from src.db.models.user import User, UserRole
from src.db.session import get_db
from src.db.models.staff import Staff
from src.db.models.staff_site import StaffSite
from src.schemas.user import UserOut
from src.core.dependencies import get_current_user
from src.service.user_service import UserService

router = APIRouter(prefix="/site", tags=["site"])

# @router.get("/{site_id}/users", response_model=list[UserOut])
# def list_users_by_site(
#     site_id: str,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     # Supervisors and managers can access users in their sites
#     # Staff cannot
#     if current_user.role == UserRole.staff:
#         raise HTTPException(status_code=403, detail="Not allowed")

#     # Query users assigned to the site
#     query = (
#         db.query(User)
#         .join("staff")  # assumes User -> Staff relationship exists
#         .join("staff_sites")  # Staff -> StaffSites
#         .filter("staff_sites.site_id" == site_id)
#     )
#     return query.all()


@router.get("/{site_id}/users", response_model=list[UserOut])
def list_users_by_site(
    site_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Staff are not allowed
    if current_user.role == UserRole.staff:
        raise HTTPException(status_code=403, detail="Not allowed")

    query = db.query(User).join(User.staff).join(Staff.staff_sites).filter(StaffSite.site_id == site_id)

    # Supervisors can only see users in their assigned sites
    if current_user.role == UserRole.supervisor:
        # Get site IDs assigned to this supervisor
        supervisor_staff = current_user.staff
        if not supervisor_staff:
            raise HTTPException(status_code=403, detail="No staff record for supervisor")

        supervisor_site_ids = [ss.site_id for ss in supervisor_staff.staff_sites]
        if UUID(site_id) not in supervisor_site_ids:
            raise HTTPException(status_code=403, detail="Not allowed to access this site")

    users = query.all()
    return users