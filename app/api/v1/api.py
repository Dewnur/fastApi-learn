from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    product,
    role,
    user,
    profile,
    category
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(user.router, prefix='/users', tags=['users'])
api_router.include_router(profile.router, prefix='/profile', tags=['profile'])
api_router.include_router(role.router, prefix='/roles', tags=['role'])
api_router.include_router(product.router, prefix='/products', tags=['products'])
api_router.include_router(category.router, prefix='/categories', tags=['categories'])
