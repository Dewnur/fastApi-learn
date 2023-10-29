from fastapi import Depends

from app.api.deps import model_id_existing
from app.api.router_base import BaseAPIRouter, RouteDepends
from app.dependencies.common_deps import DEPEND_A
from app.models import Category
from app.schemas.category_schema import ICategoryRead, ICategoryUpdate, ICategoryCreate

router = BaseAPIRouter(
    model=Category,
    model_schema_read=ICategoryRead,
    model_schema_create=ICategoryCreate,
    model_schema_update=ICategoryUpdate,
    route_depends=RouteDepends(
        post_route=[DEPEND_A],
        update_route=[DEPEND_A],
        delete_route=[DEPEND_A],
    )
)


@router.get('/{obj_id}/products')
async def get_category_products(
        category_by_id: ICategoryRead = Depends(model_id_existing(Category)),
):
    pass
