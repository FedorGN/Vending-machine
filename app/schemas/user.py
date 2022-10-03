from typing import Optional, Union

from pydantic import BaseModel, validator, ValidationError

from app.db.enums import UserRoles


class UserBase(BaseModel):
    """User schema base class."""
    username: str
    role: str


class UserResponse(UserBase):
    """User properties to return via API"""
    id: int
    deposit: Union[int, None]

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    """Properties to receive via API on create."""
    password: str
    role: str

    @validator('role')
    def validate_role(cls, v):
        """Validate a role."""
        if v not in [role.value for role in UserRoles]:
            raise ValueError(
                f'Role must be {UserRoles.BUYER.value} or {UserRoles.SELLER.value}.')
        return v


class UserUpdate(UserBase):
    """Properties to receive via API on update."""
    password: Optional[str] = None


class UserDeposit(BaseModel):
    """Properties to receive via API on deposit."""
    coin: int

    @validator('coin')
    def validate_coin(cls, v):
        """Validate a coin."""
        if v not in [5, 10, 20, 50, 100]:
            raise ValueError('Coin must be 5, 10, 20, 50 or 100.')
        return v


class BuyResponse(BaseModel):
    """Response schema for buy endpoint."""
    total_spent: int
    product_name: str
    charge: list[int]
