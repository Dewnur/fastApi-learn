from app.crud.crud_base import CRUDBase
from app.models import Profile


class CRUDProfile(CRUDBase[Profile]):
    pass


profile = CRUDProfile(Profile)
