from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    product,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix='/auth', tags=['Аутентификация и Авторизация'])
api_router.include_router(product.router, prefix='/product', tags=['Товары'])
