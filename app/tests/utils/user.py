from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate


def user_authentication_headers(
    *, client: TestClient, username: str, password: str
) -> Dict[str, str]:
    data = {"username": username, "password": password}

    r = client.post(f"{settings.API_V1_STR}/get-access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_username(
    *, client: TestClient, username: str, password: str, role: str, db: Session
) -> Dict[str, str]:
    """
    Return a valid token for the user with given username.

    If the user doesn't exist it is created first.
    """
    user = crud.user.get_by_username(db, username=username)
    if not user:
        user_in_create = UserCreate(
            username=username,
            password=password,
            role=role
        )
        user = crud.user.create(db, obj_in=user_in_create)
    return user_authentication_headers(client=client, username=username, password=password)
