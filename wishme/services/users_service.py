from sqlalchemy.orm import Session

from wishme.models.models import User
from wishme.schemas.users import UserCreate, UserUpdate
from wishme.utils.responses import ResponseHandler
from wishme.core.security import get_password_hash


class UserService:
    @staticmethod
    def get_all_users(db: Session, page: int, limit: int, role: str = "user") -> dict:
        users = (
            db.query(User)
            .order_by(User.id.asc())
            .filter(User.role == role)
            .limit(limit)
            .offset((page - 1) * limit)
            .all()
        )

        return {"message": f"Page {page} with {limit} users", "data": users}

    @staticmethod
    def get_user(db: Session, user_id: int) -> dict:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            ResponseHandler.not_found_error("User", user_id)

        return ResponseHandler.get_single_success(user.email, user_id, user)

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> dict:
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        db_user = User(id=None, **user.model_dump())

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return ResponseHandler.create_success(db_user.email, db_user.id, db_user)

    @staticmethod
    def update_user(db: Session, user_id: int, updated_user: UserUpdate) -> dict:
        db_user = db.query(User).filter(User.id == user_id).first()

        if not db_user:
            ResponseHandler.not_found_error("User", user_id)

        for key, value in updated_user.model_dump().items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)

        return ResponseHandler.update_success(db_user.email, db_user.id, db_user)

    @staticmethod
    def delete_user(db: Session, user_id: int) -> dict:
        db_user = db.query(User).filter(User.id == user_id).first()

        if not db_user:
            ResponseHandler.not_found_error("User", user_id)

        db.delete(db_user)
        db.commit()

        return ResponseHandler.delete_success(db_user.email, db_user.id, db_user)
