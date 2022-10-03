from typing import Union

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models import User, Product
from app.schemas import UserCreate, UserUpdate, UserDeposit, BuyResponse


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def authenticate(self, db: Session, *, username: str, password: str) -> Union[User, None]:
        """Authenticate a user."""
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_by_username(self, db: Session, *, username: str) -> Union[User, None]:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create user."""
        db_obj = User(
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            role=obj_in.role
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: UserUpdate
    ) -> User:
        """Update user."""
        update_data = obj_in.dict()
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def add_deposit(self, db: Session, *, db_obj: User, obj_in: UserDeposit) -> User:
        """Add a coin to deposit."""
        db_obj.deposit += obj_in.coin
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def reset_deposit(self, db: Session, *, db_obj: User) -> User:
        """Reset user deposit to zero."""
        db_obj.deposit = 0
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def buy_product_by_id(self, db: Session, *, user: User, product_id: int) -> BuyResponse:
        """Buy a product."""
        product: Product = db.query(Product).filter(
            Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found.")
        if user.deposit < product.cost:
            raise HTTPException(
                status_code=400, detail="User hasn't enough deposit.")
        if product.amountAvailable < 1:
            raise HTTPException(
                status_code=400, detail="No products avaliable.")
        coins: list[int] = [100, 50, 20, 10, 5]
        charge: list[int] = []
        coins_number: list[int] = []
        dif: int = user.deposit - product.cost
        for coin in coins:
            coins_number.append(dif//coin)
            dif %= coin
        charge: list[int] = []
        for i in range(len(coins_number)):
            if coins_number[i]:
                charge += [coins[i]]*coins_number[i]
        user.deposit = 0
        product.amountAvailable -= 1
        db.add(user)
        db.add(product)
        db.commit()
        return BuyResponse(total_spent=product.cost, product_name=product.productName,
                           charge=charge)


user = CRUDUser(User)
