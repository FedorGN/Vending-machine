from typing import Union

from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models import Product
from app.schemas import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_id(self, db: Session, *, product_id: int) -> Union[Product, None]:
        """Get product by id."""
        return db.query(Product).filter(Product.id == product_id).first()

    def get_by_id_or_404(self, db: Session, *, product_id: int) -> Product:
        """Get product by id or raise HTTP exception 404."""
        product: Product = self.get_by_id(db, product_id=product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found.")
        return product

    def create(
        self, db: Session, *, obj_in: ProductCreate, user_id: int
    ) -> Product:
        """Create product."""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, sellerId=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Product, obj_in: ProductUpdate, user_id: int
    ) -> Product:
        """Update product."""
        if db_obj.sellerId != user_id:
            raise HTTPException(
                status_code=400, detail="User is not seller of this product.")
        update_data = obj_in.dict()
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def remove(self, db: Session, *, id: int, user_id: int) -> Product:
        """Remove product."""
        obj: Product = self.get_by_id_or_404(db, product_id=id)
        if obj.sellerId != user_id:
            raise HTTPException(
                status_code=400, detail="User is not seller of the product.")
        db.delete(obj)
        db.commit()
        return obj


product = CRUDProduct(Product)
