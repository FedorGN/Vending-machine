from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Product(Base):
    """Product model class."""
    id: int = Column(Integer, primary_key=True, index=True)
    cost: int = Column(Integer(), nullable=False)
    amountAvailable: int = Column(Integer, nullable=False, default=0)
    productName: str = Column(String(200), nullable=False)
    sellerId: int = Column(Integer, ForeignKey("user.id"), nullable=False)

    seller = relationship("User", back_populates="products")
