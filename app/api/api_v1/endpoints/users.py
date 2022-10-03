from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/user", response_model=schemas.UserResponse, responses={
    400: {"model": schemas.Detail, "description": "The user with this username already exists in the system"},
})
def create_user_signup(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate
) -> Any:
    """
    User sign up.
    """
    user = crud.user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.post("/deposit", response_model=schemas.UserResponse, responses={
    401: {"model": schemas.Detail, "description": "User unathorized"},
})
def deposit_coin(
    *,
    user_deposit: schemas.UserDeposit,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_buyer_user)
) -> Any:
    """
    Deposit coin.
    """
    user = crud.user.add_deposit(db, db_obj=current_user, obj_in=user_deposit)
    return user


@router.delete("/reset", response_model=schemas.UserResponse, responses={
    401: {"model": schemas.Detail, "description": "User unathorized"},
})
def reset_user_deposit(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_buyer_user)
) -> Any:
    """
    Reset user deposit to 0.
    """
    user = crud.user.reset_deposit(db, db_obj=current_user)
    return user


@router.post("/buy", response_model=schemas.BuyResponse, responses={
    401: {"model": schemas.Detail, "description": "User unathorized"},
})
def buy_product_by_id(
    *,
    product_id: int = Body(..., description="Product id.", embed=True),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_buyer_user)
) -> Any:
    """
    Buy a product by id.
    """
    response: schemas.BuyResponse = crud.user.buy_product_by_id(
        db, user=current_user, product_id=product_id)
    return response
