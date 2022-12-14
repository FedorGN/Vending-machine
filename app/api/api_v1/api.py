from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, products

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(products.router, tags=["products"])
