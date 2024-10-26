from sqlalchemy.orm import Session

from wishme.models.models import Product
from wishme.schemas.products import ProductCreate, ProductUpdate
from wishme.utils.responses import ResponseHandler


class ProductService:
    @staticmethod
    def get_all_products(db: Session, page: int, limit: int, search: str = "") -> dict:
        products = (
            db.query(Product)
            .order_by(Product.id.asc())
            .filter(Product.title.contains(search))
            .limit(limit)
            .offset((page - 1) * limit)
            .all()
        )
        return {"message": f"Page {page} with {limit} products", "data": products}

    @staticmethod
    def get_product(db: Session, product_id: int) -> dict:
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            ResponseHandler.not_found_error("Product", product_id)

        return ResponseHandler.get_single_success(product.title, product_id, product)

    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> dict:
        product_dict = product.model_dump()
        db_product = Product(**product_dict)

        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return ResponseHandler.create_success(db_product.title, db_product.id, db_product)

    @staticmethod
    def update_product(db: Session, product_id: int, updated_product: ProductUpdate) -> dict:
        db_product = db.query(Product).filter(Product.id == product_id).first()

        if not db_product:
            ResponseHandler.not_found_error("Product", product_id)

        for key, value in updated_product.model_dump().items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)

        return ResponseHandler.update_success(db_product.title, db_product.id, db_product)

    @staticmethod
    def delete_product(db: Session, product_id: int) -> dict:
        db_product = db.query(Product).filter(Product.id == product_id).first()

        if not db_product:
            ResponseHandler.not_found_error("Product", product_id)

        db.delete(db_product)
        db.commit()

        return ResponseHandler.delete_success(db_product.title, db_product.id, db_product)
