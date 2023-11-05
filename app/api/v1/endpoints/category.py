from fastapi import Depends

from app.api.deps import get_current_user
from app.api.router_base import BaseAPIMethods
from app.api.router_base import BaseAPIRouter
from app.models import Category
from app.schemas.category_schema import ICategoryRead, ICategoryUpdate, ICategoryCreate
from app.schemas.role_schema import IRoleEnum


class CategoryAPIRouter(BaseAPIRouter[Category, ICategoryCreate, ICategoryRead, ICategoryUpdate]):
    pass


router = CategoryAPIRouter(
    Category,
    ICategoryCreate,
    ICategoryRead,
    ICategoryUpdate,
    depends_mapping={
        BaseAPIMethods.post: [Depends(get_current_user([IRoleEnum.admin, IRoleEnum.manager]))],
        BaseAPIMethods.put: [Depends(get_current_user([IRoleEnum.admin, IRoleEnum.manager]))],
        BaseAPIMethods.delete: [Depends(get_current_user([IRoleEnum.admin, IRoleEnum.manager]))],
    }
)
