from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    """User model class."""
    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String(150), unique=True,
                           nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role: str = Column(String(20), nullable=False)
    deposit: int = Column(Integer, nullable=True, default=0)

    products = relationship("Product", back_populates="seller")
