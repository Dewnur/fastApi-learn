import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    def __repr__(self):
        return f'{self.__class__.__name__}:{self.__dict__}'


class BaseUUIDModel(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("uuid_generate_v4()"),
        default=lambda: uuid.uuid4())
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        onupdate=datetime.utcnow(),
        default=datetime.utcnow(),
        nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        default=datetime.utcnow(),
        nullable=True)
