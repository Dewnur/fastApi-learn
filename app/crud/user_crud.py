from app.crud.crud_base import CRUDBase
from app.models.user_model import User


class CRUDUser(CRUDBase[User]):
    pass


user = CRUDUser(User)
