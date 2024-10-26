from datetime import datetime

from pydantic import BaseModel, EmailStr

from .base_schema import BaseSchema
from .wishes import WishBase


class UserBase(BaseSchema):
    id: int
    email: EmailStr
    password: str
    role: str
    is_active: bool
    created_at: datetime
    wishes: list[WishBase]


class Signup(BaseSchema):
    email: str
    password: str


class UserOut(BaseSchema):
    message: str
    data: UserBase


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
