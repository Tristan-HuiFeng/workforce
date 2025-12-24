from sqlalchemy.orm import Session
from src.db.models.user import User, UserRole
from src.service.auth_service import AuthService
from uuid import UUID
from fastapi import HTTPException, status

class UserService:
    @staticmethod
    def get_user(db: Session, user_id: UUID) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def list_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def create_user(db: Session, email: str, password: str, role: UserRole) -> User:
        hashed = AuthService.hash_password(password)
        new_user = User(email=email, password_hash=hashed, role=role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def update_user(db: Session, user: User, email: str = None, password: str = None, role: UserRole = None):
        if email:
            user.email = email
        if password:
            user.password_hash = AuthService.hash_password(password)
        if role:
            user.role = role
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user: User):
        db.delete(user)
        db.commit()

    @staticmethod
    def verify_role(current_user: User, required_role: UserRole):
        if current_user.role != required_role and current_user.role != UserRole.manager:
            raise HTTPException(status_code=403, detail="Not enough permissions")
