from app.crud.crud_base import CRUDBase
from app.models import Category


class CRUDCategory(CRUDBase[Category]):
    pass


category = CRUDCategory(Category)
