from app.crud.crud_base import CRUDBase
from app.models import Product


class CRUDProduct(CRUDBase[Product]):
    pass


product = CRUDProduct(Product)
