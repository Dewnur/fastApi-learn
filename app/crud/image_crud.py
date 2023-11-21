from app.crud.crud_base import CRUDBase
from app.models import Image


class CRUDImage(CRUDBase[Image]):
    pass


image = CRUDImage(Image)
