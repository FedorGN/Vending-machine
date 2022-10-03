from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


def test_deposit_coin(
    client: TestClient, buyer_token_headers: dict, db: Session
) -> None:
    data = {"coin": 10}
    response = client.post(
        f"{settings.API_V1_STR}/deposit", headers=buyer_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    deposit = content["deposit"]
    response = client.post(
        f"{settings.API_V1_STR}/deposit", headers=buyer_token_headers, json=data,
    )
    assert deposit + 10 == response.json()["deposit"]


def test_deposit_validation_coin(
    client: TestClient, buyer_token_headers: dict, db: Session
) -> None:
    # Deposit not multiple of 5
    data = {"coin": 12}
    response = client.post(
        f"{settings.API_V1_STR}/deposit", headers=buyer_token_headers, json=data,
    )
    assert response.status_code == 422

    # Negative deposit
    data = {"coin": -10}
    response = client.post(
        f"{settings.API_V1_STR}/deposit", headers=buyer_token_headers, json=data,
    )
    assert response.status_code == 422


def test_deposit_coin_with_seller(
    client: TestClient, seller_token_headers: dict, db: Session
) -> None:
    # Deposit coin with user seller
    data = {"coin": 10}
    response = client.post(
        f"{settings.API_V1_STR}/deposit", headers=seller_token_headers, json=data,
    )
    assert response.status_code == 403


def test_buy(
    client: TestClient, seller_token_headers: dict, buyer_token_headers: dict, db: Session
) -> None:
    # Add product and get it's id
    data = {
        "cost": 60,
        "amountAvailable": 10,
        "productName": "Juce"
    }
    response = client.post(
        f"{settings.API_V1_STR}/product", headers=seller_token_headers, json=data,
    )
    assert response.status_code == 200
    product_id: int = response.json()["id"]

    # Reset deposit for buyer
    response = client.delete(
        f"{settings.API_V1_STR}/reset", headers=buyer_token_headers, json=data,
    )
    assert response.status_code == 200

    # Try to buy product without deposit
    data = {"product_id": product_id}
    response = client.post(
        f"{settings.API_V1_STR}/buy", headers=buyer_token_headers, json=data,
    )
    assert response.status_code == 400

    # Add deposit
    data = {"coin": 100}
    response = client.post(
        f"{settings.API_V1_STR}/deposit", headers=buyer_token_headers, json=data,
    )
    assert response.status_code == 200

    # Buy product
    data = {"product_id": product_id}
    response = client.post(
        f"{settings.API_V1_STR}/buy", headers=buyer_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["total_spent"] == 60
    assert content["product_name"] == "Juce"
    assert content["charge"] == [20, 20]


def test_create_product_with_seller(
    client: TestClient, seller_token_headers: dict, db: Session
) -> None:
    # Create product with user seller
    data = {
        "cost": 10,
        "amountAvailable": 15,
        "productName": "Apple"
    }
    response = client.post(
        f"{settings.API_V1_STR}/product", headers=seller_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["amountAvailable"] == 15
    assert content["productName"] == "Apple"
    assert content["cost"] == 10


def test_create_product_with_buyer(
    client: TestClient, buyer_token_headers: dict, db: Session
) -> None:
    # Create product with user buyer
    data = {
        "cost": 10,
        "amountAvailable": 15,
        "productName": "Apple"
    }
    response = client.post(
        f"{settings.API_V1_STR}/product", headers=buyer_token_headers, json=data,
    )
    assert response.status_code == 403


def test_create_product_validation_errors(
    client: TestClient, seller_token_headers: dict, db: Session
) -> None:
    # Create product with negative price
    data = {
        "cost": -10,
        "amountAvailable": 15,
        "productName": "Apple"
    }
    response = client.post(
        f"{settings.API_V1_STR}/product", headers=seller_token_headers, json=data,
    )
    assert response.status_code == 422

    # Create product with 0 price
    data = {
        "cost": 0,
        "amountAvailable": 15,
        "productName": "Apple"
    }
    response = client.post(
        f"{settings.API_V1_STR}/product", headers=seller_token_headers, json=data,
    )
    assert response.status_code == 422

    # Create product with price not multiple of 5
    data = {
        "cost": 233,
        "amountAvailable": 15,
        "productName": "Apple"
    }
    response = client.post(
        f"{settings.API_V1_STR}/product", headers=seller_token_headers, json=data,
    )
    assert response.status_code == 422

    # Create product with negative amountAvailable
    data = {
        "cost": 30,
        "amountAvailable": -15,
        "productName": "Apple"
    }
    response = client.post(
        f"{settings.API_V1_STR}/product", headers=seller_token_headers, json=data,
    )
    assert response.status_code == 422
