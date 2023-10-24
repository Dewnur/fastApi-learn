from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette import status

from app.core.security import get_password_hash, verify_password
from app.crud.crud_base import CRUDBase
from app.models.user_model import User


class CRUDUser(CRUDBase[User]):

    async def get_by_email(
            self,
            *,
            email: str,
            db_session: AsyncSession | None = None,
    ) -> User:
        db_session = db_session or self.get_db().session
        users = await db_session.execute(select(User).where(User.email == email))
        return users.scalar_one_or_none()

    async def create(
            self,
            *,
            obj: BaseModel,
            db_session: AsyncSession | None = None,
    ) -> User:
        db_session = db_session or self.get_db().session
        data = obj.model_dump()
        password = data.pop('password')
        db_obj = self.model(**data)
        db_obj.password_hash = get_password_hash(password)
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def authenticate(
            self,
            *,
            obj: BaseModel,
            db_session: AsyncSession | None = None
    ) -> User | None:
        auth_user = await self.get_by_email(db_session=db_session, email=obj.email)
        if not auth_user and not verify_password(obj.password, auth_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The email or password you entered is incorrect",
            )
        return auth_user


user = CRUDUser(User)
