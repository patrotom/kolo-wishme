from sqlalchemy import Boolean, Column, Integer, Text, ForeignKey, Float, Enum
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

from wishme.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    email = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    is_active = Column(Boolean, server_default=text("true"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    role = Column(Enum("admin", "user", name="user_roles"), nullable=False, server_default="user")
    # organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True)

    wishes = relationship("Wish", back_populates="user")
    # organization = relationship("Organization", back_populates="user")


# class Organization(Base):
#     __tablename__ = "organizations"

#     id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
#     name = Column(Text, nullable=False)
#     # TODO: Add more fields
#     created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

#     user = relationship("User", back_populates="organization")


class Wish(Base):
    __tablename__ = "wishes"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    total_amount = Column(Integer, nullable=False)
    state = Column(
        Enum("created", "reserved", "fulfilled", "declined", name="wish_states"),
        nullable=False,
        server_default="created",
    )

    user = relationship("User", back_populates="wishes")
    wish_items = relationship("WishItem", back_populates="wish")


class WishItem(Base):
    __tablename__ = "wish_items"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    wish_id = Column(Integer, ForeignKey("wishes.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)

    wish = relationship("Wish", back_populates="wish_items")
    product = relationship("Product", back_populates="wish_items")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    stock = Column(Integer, nullable=False)
    thumbnail = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    is_published = Column(Boolean, server_default=text("true"), nullable=False)
    average_weight_in_kilos = Column(Float, nullable=False)
    # TODO: Add more fields from input data

    wish_items = relationship("WishItem", back_populates="product")
