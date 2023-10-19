from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseUUIDModel
from app.schemas import IOrderStatus

if TYPE_CHECKING:
    pass


class OrderHistory(BaseUUIDModel):
    __tablename__ = "order_history"

    order_id: Mapped[UUID] = mapped_column(ForeignKey('order.id'))
    status: Mapped[IOrderStatus] = mapped_column()
    status_date: Mapped[datetime] = mapped_column()
