from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.crud.crud_base import CRUDBase
from app.models import Role
from app.models.user_model import User


class CRUDRole(CRUDBase[Role]):

    async def get_role_by_name(
            self,
            *,
            name: str,
            db_session: async_sessionmaker[AsyncSession] | None = None,
    ) -> User:
        async with db_session() as session:
            role = await session.execute(select(Role).where(Role.name == name))
            return role.scalar_one_or_none()


role = CRUDRole(Role)
