from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseUUIDModel
from app.schemas.common_schema import IOrderStatus

if TYPE_CHECKING:
    from app.models.user_model import User
    from app.models.order_items_model import OrderItem


class Order(BaseUUIDModel):
    __tablename__ = "order"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    order_date: Mapped[datetime] = mapped_column()
    status: Mapped[IOrderStatus] = mapped_column(default=None)
    total_amount: Mapped[float] = mapped_column()

    users: Mapped['User'] = relationship(back_populates='orders', lazy='selectin')
    order_items: Mapped[list['OrderItem']] = relationship(back_populates='order', lazy='selectin')
