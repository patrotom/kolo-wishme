from datetime import datetime

from pydantic import EmailStr

from .wishes import WishBase
from .base_schema import BaseSchema


class UserBase(BaseSchema):
    id: int
    email: EmailStr
    password: str
    role: str
    is_active: bool
    created_at: datetime
    wishes: list[WishBase]


class UserCreate(BaseSchema):
    email: str
    password: str


class UserUpdate(UserCreate): ...


class UserOut(BaseSchema):
    message: str
    data: UserBase


class UsersOut(BaseSchema):
    message: str
    data: list[UserBase]


class UserOutDelete(BaseSchema):
    message: str
    data: UserBase
