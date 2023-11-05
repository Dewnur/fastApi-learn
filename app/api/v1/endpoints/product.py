from fastapi import Depends

from app.api.deps import get_current_user
from app.api.router_base import BaseAPIRouter, BaseAPIMethods
from app.models import Product
from app.schemas.product_schema import IProductCreate, IProductUpdate, IProductRead
from app.schemas.role_schema import IRoleEnum


class ProductAPIRouter(BaseAPIRouter[Product, IProductCreate, IProductRead, IProductUpdate]):
    pass


router = ProductAPIRouter(
    Product,
    IProductCreate,
    IProductRead,
    IProductUpdate,
    depends_mapping={
        BaseAPIMethods.post: [Depends(get_current_user([IRoleEnum.admin, IRoleEnum.manager]))],
        BaseAPIMethods.put: [Depends(get_current_user([IRoleEnum.admin, IRoleEnum.manager]))],
        BaseAPIMethods.delete: [Depends(get_current_user([IRoleEnum.admin, IRoleEnum.manager]))],
    }
)
