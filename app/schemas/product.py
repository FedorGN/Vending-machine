from pydantic import BaseModel, validator


class ProductBase(BaseModel):
    """Product schema base class."""
    cost: int
    amountAvailable: int
    productName: str


class ProductResponse(ProductBase):
    """Product schema for properties to return via API."""
    id: int
    sellerId: int

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    """Product schema for properties to receive via API on create."""
    cost: int
    amountAvailable: int
    productName: str

    @validator('cost')
    def validate_cost(cls, v):
        """Validate cost of the product."""
        if v <= 0:
            raise ValueError('Cost must be greater than 0.')
        if v % 5 != 0:
            raise ValueError('Cost must be multiple of 5.')
        return v

    @validator('amountAvailable')
    def validate_amountAvailable(cls, v):
        """Validate avaliable amount of product."""
        if v < 0:
            raise ValueError('amountAvailable must be greater or equal to 0.')
        return v


class ProductUpdate(ProductCreate):
    """Product schema for properties to receive via API on update."""
    id: int
