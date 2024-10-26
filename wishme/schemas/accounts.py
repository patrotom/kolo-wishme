from datetime import datetime

from pydantic import BaseModel, EmailStr

from .base_schema import BaseSchema
from .wishes import WishBase


class AccountBase(BaseSchema):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    wishes: list[WishBase]


class AccountUpdate(BaseModel):
    email: EmailStr


class AccountDelete(BaseSchema):
    message: str
    data: AccountBase
