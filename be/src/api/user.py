from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.models.user import User, UserRole
from src.db.session import get_db
from src.schemas.user import UserOut
from src.core.dependencies import get_current_user
from src.service.user_service import UserService

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=UserOut)
def read_me(user: User = Depends(get_current_user)):
    return user

@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    UserService.verify_role(current_user, UserRole.manager)
    return db.query(User).all()

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if current.role == UserRole.staff and current.id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    return user

# @app.post("/", response_model=UserOut)
# def create_user(payload: UserCreate, db: Session = Depends(get_db), current: User = Depends(require_role(UserRole.manager))):
#     hashed = hash_password(payload.password)
#     new_user = User(email=payload.email, role=payload.role, password_hash=hashed)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user