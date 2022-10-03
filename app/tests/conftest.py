from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from pydantic import BaseSettings

from app.db.session import TestSession
from app.main import app
from app.tests.utils.user import authentication_token_from_username
from app.db.enums import UserRoles


class TestSettings(BaseSettings):
    user_seller_username: str = "user_seller"
    user_seller_password: str = "user_seller"
    user_buyer_username: str = "user_buyer"
    user_buyer_password: str = "user_buyer"


test_settings = TestSettings()


@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestSession()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def seller_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_username(
        client=client, username=test_settings.user_seller_username,
        password=test_settings.user_seller_password, role=UserRoles.SELLER.value, db=db
    )


@pytest.fixture(scope="module")
def buyer_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_username(
        client=client, username=test_settings.user_buyer_username,
        password=test_settings.user_buyer_password, role=UserRoles.BUYER.value, db=db
    )
