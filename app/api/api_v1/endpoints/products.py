from typing import Any

from fastapi import APIRouter, Body, Depends, Query as QueryAPI
from sqlalchemy.orm import Session

from app import crud
from app import models
from app import schemas
from app.api import deps


router = APIRouter()


@router.post("/product", response_model=schemas.ProductResponse, responses={
    401: {"model": schemas.Detail, "description": "User unathorized"}
})
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_seller_user)
) -> Any:
    """
    Create product.
    """
    todo = crud.product.create(
        db, obj_in=product, user_id=current_user.id)
    return todo


@router.get("/product", response_model=schemas.ProductResponse, responses={
    401: {"model": schemas.Detail, "description": "User unathorized"},
    404: {"model": schemas.Detail, "description": "Product not found."}
})
def get_product(
    product_id: int = QueryAPI(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Get product by id.
    """
    product = crud.product.get_by_id_or_404(db, id=product_id)
    return product


@router.put("/product", response_model=schemas.ProductResponse, responses={
    401: {"model": schemas.Detail, "description": "User unathorized"},
    404: {"model": schemas.Detail, "description": "Product not found."}
})
def update_product(
    product_update: schemas.ProductUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_seller_user)
) -> Any:
    """
    Update product.
    """
    product: models.Product = crud.product.get_by_id_or_404(
        db, product_id=product_update.id)
    product = crud.product.update(
        db, db_obj=product, obj_in=product_update, user_id=current_user.id)
    return product


@router.delete("/product", response_model=schemas.ProductResponse, responses={
    401: {"model": schemas.Detail, "description": "User unathorized."},
    404: {"model": schemas.Detail, "description": "Product not found."}
})
def remove_product(
    product_id: int = QueryAPI(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_seller_user)
) -> Any:
    """
    Delete product by id.
    """
    product = crud.product.remove(
        db=db, id=product_id, user_id=current_user.id)
    return product
