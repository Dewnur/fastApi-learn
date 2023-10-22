from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.security import get_password_hash, verify_password
from app.crud.crud_base import CRUDBase
from app.models.user_model import User


class CRUDUser(CRUDBase[User]):

    async def get_by_email(
            self,
            *,
            email: str,
            db_session: async_sessionmaker[AsyncSession] | None = None,
    ) -> User:
        async with db_session() as session:
            users = await session.execute(select(User).where(User.email == email))
            return users.scalar_one_or_none()

    async def create(
            self,
            *,
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

    async def authenticate(
            self,
            *,
            obj: BaseModel,
            db_session: async_sessionmaker[AsyncSession] | None = None
    ) -> User | None:
        auth_user = await self.get_by_email(db_session=db_session, email=obj.email)
        if not auth_user and not verify_password(obj.password, auth_user.password_hash):
            return None
        return auth_user


user = CRUDUser(User)
