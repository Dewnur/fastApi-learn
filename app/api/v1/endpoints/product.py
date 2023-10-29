from app.api.router_base import BaseAPIRouter, RouteDepends
from app.dependencies.common_deps import DEPEND_A_M
from app.models import Product
from app.schemas.product_schema import IProductUpdate, IProductCreate, IProductRead

router = BaseAPIRouter(
    model=Product,
    model_schema_read=IProductRead,
    model_schema_create=IProductCreate,
    model_schema_update=IProductUpdate,
    route_depends=RouteDepends(
        post_route=[DEPEND_A_M],
        update_route=[DEPEND_A_M],
        delete_route=[DEPEND_A_M],
    )
)
