from typing import Any

from datetime import datetime, timedelta, timezone

import jwt

from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from wishme.settings import JWT_ALGORITHM, JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

from wishme.schemas.auth import TokenResponse
from wishme.models.models import User
from wishme.db.database import get_db
from wishme.utils.responses import ResponseHandler


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_scheme = HTTPBearer()


# Create Hash Password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Verify Hash Password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Create Access & Refresh Token
async def get_user_token(id: int, refresh_token: str = None) -> TokenResponse:
    payload = {"id": id}

    access_token_expiry = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = await create_access_token(payload, access_token_expiry)

    if not refresh_token:
        refresh_token = await create_refresh_token(payload)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token, expires_in=access_token_expiry.seconds)


# Create Access Token
async def create_access_token(data: dict, access_token_expiry: timedelta) -> str:
    payload = data.copy()

    expire = datetime.now(timezone.utc) + access_token_expiry
    payload.update({"exp": expire})

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


# Create Refresh Token
async def create_refresh_token(data: dict[str, Any]) -> str:
    return jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


# Get Payload Of Token
def get_token_payload(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.DecodeError:
        raise ResponseHandler.invalid_token("access")


def get_current_user(token: str) -> int:
    user = get_token_payload(token.credentials)
    return user.get("id")


def check_admin_role(token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(get_db)) -> None:
    user = get_token_payload(token.credentials)
    user_id = user.get("id")
    role_user = db.query(User).filter(User.id == user_id).first()
    if role_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
