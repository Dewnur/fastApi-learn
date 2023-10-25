from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseUUIDModel
from app.schemas.common_schema import IGenderEnum

if TYPE_CHECKING:
    from app.models.order_model import Order
    from app.models.user_model import User


class Profile(BaseUUIDModel):
    __tablename__ = "profile"

    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    gender: Mapped[IGenderEnum] = mapped_column(default=IGenderEnum.other, nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'), )

    user: Mapped['User'] = relationship(back_populates='profile', lazy='selectin')
    orders: Mapped[list['Order']] = relationship(back_populates='profile')
