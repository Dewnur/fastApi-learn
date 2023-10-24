from typing import TypeVar, Generic, Any, Sequence
from uuid import UUID
from fastapi_async_sqlalchemy import db
from pydantic import BaseModel
from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.base_model import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model
        self.db = db

    def get_db(self):
        return self.db

    async def fetch_one(
            self,
            *,
            db_session: AsyncSession | None = None,
            **filter,
    ) -> ModelType | None:
        db_session = db_session or self.get_db().session
        query = select(self.model).filter_by(**filter)
        result = await db_session.execute(query)
        result = result.scalar_one_or_none()
        return result

    async def fetch_all(
            self,
            *,
            db_session: AsyncSession | None = None,
            **filter,
    ) -> Sequence[Row | RowMapping | Any]:
        db_session = db_session or self.get_db().session
        query = select(self.model).filter_by(**filter)
        result = await db_session.execute(query)
        result = result.scalars().all()
        return result

    async def create(
            self,
            *,
            obj: BaseModel,
            db_session: AsyncSession | None = None,
    ) -> ModelType:
        db_session = db_session or self.get_db().session
        db_obj = self.model(**obj.model_dump())
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            *,
            obj_current: ModelType,
            obj_new: BaseModel,
            db_session: AsyncSession | None = None,
    ) -> None:
        db_session = db_session or self.get_db().session
        update_data = obj_new.model_dump(
            exclude_unset=True
        )
        for field in update_data:
            setattr(obj_current, field, update_data[field])
        db_session.add(obj_current)
        await db_session.commit()
        await db_session.refresh(obj_current)
        return obj_current

    async def delete(
            self,
            *,
            id: UUID,
            db_session: AsyncSession | None = None,
    ) -> None:
        db_session = db_session or self.get_db().session
        query = await db_session.execute(
            select(self.model).where(self.model.id == id)
        )
        obj = query.scalar_one()
        await db_session.delete(obj)
        await db_session.commit()
        return obj
