from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.crud.crud_base import CRUDBase
from app.models import Role
from app.models.user_model import User


class CRUDRole(CRUDBase[Role]):

    async def get_role_by_name(
            self,
            *,
            name: str,
            db_session: AsyncSession | None = None,
    ) -> User:
        db_session = db_session or self.get_db().session
        role = await db_session.execute(select(Role).where(Role.name == name))
        return role.scalar_one_or_none()


role = CRUDRole(Role)
