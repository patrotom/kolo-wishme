from sqlalchemy.orm import Session
from fastapi.security.http import HTTPAuthorizationCredentials

from wishme.models.models import Wish, WishItem, Product
from wishme.schemas.wishes import WishUpdate, WishCreate
from wishme.utils.responses import ResponseHandler
from sqlalchemy.orm import joinedload
from wishme.core.security import get_current_user


class WishService:
    # Get All Wishes
    @staticmethod
    def get_all_wishes(token: str, db: Session, page: int, limit: int) -> dict:
        user_id = get_current_user(token)
        carts = db.query(Wish).filter(Wish.user_id == user_id).offset((page - 1) * limit).limit(limit).all()
        message = f"Page {page} with {limit} carts"
        return ResponseHandler.success(message, carts)

    # Get A Wish By ID
    @staticmethod
    def get_wish(token: HTTPAuthorizationCredentials, db: Session, wish_id: int) -> dict:
        user_id = get_current_user(token)
        wish = db.query(Wish).filter(Wish.id == wish_id, Wish.user_id == user_id).first()

        if not wish:
            ResponseHandler.not_found_error("Wish", wish_id)

        return ResponseHandler.get_single_success("wish", wish_id, wish)

    # Create a new Wish
    @staticmethod
    def create_wish(token: HTTPAuthorizationCredentials, db: Session, wish: WishCreate) -> dict:
        user_id = get_current_user(token)
        wish_dict = wish.model_dump()

        wish_items_data = wish_dict.pop("wish_items", [])
        wish_items = []
        total_amount = 0
        for item_data in wish_items_data:
            product_id = item_data["product_id"]
            quantity = item_data["quantity"]

            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return ResponseHandler.not_found_error("Product", product_id)

            wish_item = WishItem(product_id=product_id, quantity=quantity)

            total_amount += quantity
            product.stock -= quantity

            wish_items.append(wish_item)

        wish_db = Wish(wish_items=wish_items, user_id=user_id, total_amount=total_amount, **wish_dict)

        db.add(wish_db)
        db.commit()
        db.refresh(wish_db)

        return ResponseHandler.create_success("Wish", wish_db.id, wish_db)

    # Update Wish & WishItem
    @staticmethod
    def update_wish(token: HTTPAuthorizationCredentials, db: Session, wish_id: int, updated_wish: WishUpdate) -> dict:
        user_id = get_current_user(token)

        wish = db.query(Wish).filter(Wish.id == wish_id, Wish.user_id == user_id).first()

        if not wish:
            return ResponseHandler.not_found_error("Wish", wish_id)

        # Delete existing wish_items
        db.query(WishItem).filter(WishItem.wish_id == wish_id).delete()

        for item in updated_wish.wish_items:
            product_id = item.product_id
            quantity = item.quantity

            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return ResponseHandler.not_found_error("Product", product_id)

            wish_item = WishItem(wish_id=wish_id, product_id=product_id, quantity=quantity)

            db.add(wish_item)

        wish.total_amount = sum(item.quantity for item in wish.wish_items)

        db.commit()
        db.refresh(wish)

        return ResponseHandler.update_success("wish", wish.id, wish)

    # Delete Both Wish and WishItems
    @staticmethod
    def delete_wish(token: HTTPAuthorizationCredentials, db: Session, wish_id: int) -> dict:
        user_id = get_current_user(token)
        wish = (
            db.query(Wish)
            .options(joinedload(Wish.wish_items).joinedload(WishItem.product))
            .filter(Wish.id == wish_id, Wish.user_id == user_id)
            .first()
        )
        if not wish:
            ResponseHandler.not_found_error("Wish", wish_id)

        for wish_item in wish.wish_items:
            db.delete(wish_item)

        db.delete(wish)
        db.commit()
        return ResponseHandler.delete_success("Wish", wish_id, wish)
