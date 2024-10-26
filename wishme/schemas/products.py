from pydantic import BaseModel

from typing import ClassVar

from datetime import datetime

from .base_schema import BaseSchema


class ProductBase(BaseSchema):
    id: int
    title: str
    description: str
    stock: int
    thumbnail: str
    created_at: datetime
    is_published: bool
    average_weight_in_kilos: float


# Create Product
class ProductCreate(ProductBase):
    id: ClassVar[int]


# Update Product
class ProductUpdate(ProductCreate): ...


# Get Products
class ProductOut(BaseSchema):
    message: str
    data: ProductBase


class ProductsOut(BaseSchema):
    message: str
    data: list[ProductBase]


# Delete Product
class ProductDelete(ProductBase): ...


class ProductOutDelete(BaseModel):
    message: str
    data: ProductDelete
