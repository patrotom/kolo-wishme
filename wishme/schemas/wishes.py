from datetime import datetime

from pydantic import BaseModel

from .base_schema import BaseSchema
from .products import ProductBase


# Base Wish & WithItem
class WishItemBase(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductBase


class WishBase(BaseSchema):
    id: int
    user_id: int
    created_at: datetime
    total_amount: int
    wish_items: list[WishItemBase]


class WishOutBase(BaseSchema):
    id: int
    user_id: int
    created_at: datetime
    total_amount: float
    cart_items: list[WishItemBase]


# Get Wish
class WishOut(BaseSchema):
    message: str
    data: WishBase


class WishesOutList(BaseModel):
    message: str
    data: list[WishBase]


class WishesUserOutList(BaseSchema):
    message: str
    data: list[WishBase]


# Delete Wish
class WishOutDelete(BaseModel):
    message: str
    data: WishOutBase


# Create Wish
class WishItemCreate(BaseModel):
    product_id: int
    quantity: int


class WishCreate(BaseSchema):
    wish_items: list[WishItemCreate]


# Update Wish
class WishUpdate(WishCreate): ...
