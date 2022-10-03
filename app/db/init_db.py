from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db.base import Base 
from app.db.session import engine
from app.db.enums import UserRoles


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But in this app we create during start of application
    Base.metadata.create_all(bind=engine)
    # Create user seller if not exist
    user = crud.user.get_by_username(db, username=settings.FIRST_USER_USERNAME)
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_USER_USERNAME,
            password=settings.FIRST_USER_PASSWORD,
            role=UserRoles.SELLER.value
        )
        user = crud.user.create(db, obj_in=user_in)
    # Create user buyer if not exist
    user = crud.user.get_by_username(db, username="John")
    if not user:
        user_in = schemas.UserCreate(
            username="John",
            password="John",
            role=UserRoles.BUYER.value
        )
        user = crud.user.create(db, obj_in=user_in)