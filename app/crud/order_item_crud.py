from app.crud.crud_base import CRUDBase
from app.models import OrderItem


class CRUDOrderItem(CRUDBase[OrderItem]):
    pass


order_item = CRUDOrderItem(OrderItem)
