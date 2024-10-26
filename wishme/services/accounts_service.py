from sqlalchemy.orm import Session

from wishme.models.models import User
from wishme.utils.responses import ResponseHandler
from wishme.core.security import get_token_payload
from wishme.schemas.accounts import AccountUpdate


class AccountService:
    @staticmethod
    def get_my_info(db: Session, token: str) -> dict:
        user_id = get_token_payload(token).get("id")
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            ResponseHandler.not_found_error("User", user_id)

        return ResponseHandler.get_single_success(user.email, user.id, user)

    @staticmethod
    def edit_my_info(db: Session, token: str, updated_user: AccountUpdate) -> dict:
        user_id = get_token_payload(token).get("id")
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            ResponseHandler.not_found_error("User", user_id)

        for key, value in updated_user.model_dump().items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return ResponseHandler.update_success(db_user.email, db_user.id, db_user)

    @staticmethod
    def remove_my_account(db: Session, token: str) -> dict:
        user_id = get_token_payload(token).get("id")
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            ResponseHandler.not_found_error("User", user_id)
        db.delete(db_user)
        db.commit()
        return ResponseHandler.delete_success(db_user.email, db_user.id, db_user)
