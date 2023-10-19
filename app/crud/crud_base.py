from typing import TypeVar, Generic, Any, Sequence
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models.base_model import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    async def fetch_one(
            self,
            db_session: async_sessionmaker[AsyncSession] | None = None,
            **filter,
    ) -> ModelType | None:
        async with db_session() as session:
            query = select(self.model).filter_by(**filter)
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            return result

    async def fetch_all(
            self,
            db_session: async_sessionmaker[AsyncSession] | None = None,
            **filter,
    ) -> Sequence[Row | RowMapping | Any]:
        async with db_session() as session:
            query = select(self.model).filter_by(**filter)
            result = await session.execute(query)
            result = result.scalars().all()
            return result

    async def create(
            self,
            obj: BaseModel,
            db_session: async_sessionmaker[AsyncSession] | None = None,
    ) -> ModelType:
        async with db_session() as session:
            db_obj = self.model(**obj.model_dump())
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def update(
            self,
            obj_current: ModelType,
            obj_new: BaseModel,
            db_session: async_sessionmaker[AsyncSession] | None = None,
    ) -> None:
        async with db_session() as session:
            update_data = obj_new.model_dump(
                exclude_unset=True
            )
            for field in update_data:
                setattr(obj_current, field, update_data[field])

            session.add(obj_current)
            await session.commit()
            await session.refresh(obj_current)
            return obj_current

    async def delete(
            self,
            id: UUID,
            db_session: async_sessionmaker[AsyncSession] | None = None,
    ) -> None:
        async with db_session() as session:
            query = await session.execute(
                select(self.model).where(self.model.id == id)
            )
            obj = query.scalar_one()
            await session.delete(obj)
            await session.commit()
            return obj
