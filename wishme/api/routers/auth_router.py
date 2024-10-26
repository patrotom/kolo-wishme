from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from wishme.services.auth_service import AuthService
from wishme.db.database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from wishme.schemas.auth import UserOut, Signup


router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/signup", status_code=status.HTTP_200_OK, response_model=UserOut)
async def user_signup(user: Signup, db: Session = Depends(get_db)):
    return await AuthService.signup(db, user)


@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await AuthService.login(user_credentials, db)


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(refresh_token: str = Header(), db: Session = Depends(get_db)):
    return await AuthService.get_refresh_token(token=refresh_token, db=db)
