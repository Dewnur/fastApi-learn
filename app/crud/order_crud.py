from app.crud.crud_base import CRUDBase
from app.models import Order


class CRUDOrder(CRUDBase[Order]):
    pass


order = CRUDOrder(Order)
