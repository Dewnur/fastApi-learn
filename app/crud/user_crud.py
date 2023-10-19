from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.security import get_password_hash
from app.crud.crud_base import CRUDBase
from app.models.user_model import User


class CRUDUser(CRUDBase[User]):
    async def create(
            self,
            obj: BaseModel,
            db_session: async_sessionmaker[AsyncSession] | None = None,
    ) -> User:
        async with db_session() as session:
            db_obj = self.model()
            db_obj.email = obj.email
            db_obj.password_hash = get_password_hash(obj.password)
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj


user = CRUDUser(User)
