from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.security.http import HTTPAuthorizationCredentials

from wishme.db.database import get_db
from wishme.services.accounts_service import AccountService
from wishme.schemas.accounts import AccountDelete, AccountUpdate
from wishme.core.security import auth_scheme


router = APIRouter(tags=["Account"], prefix="/me")


@router.get("/", response_model=AccountDelete)
def get_my_info(db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> dict:
    print(token)
    print(type(token))
    return AccountService.get_my_info(db, token.credentials)


@router.put("/", response_model=AccountDelete)
def edit_my_info(
    updated_user: AccountUpdate,
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict:
    return AccountService.edit_my_info(db, token.credentials, updated_user)


@router.delete("/", response_model=AccountDelete)
def remove_my_account(
    db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(auth_scheme)
) -> dict:
    return AccountService.remove_my_account(db, token.credentials)
