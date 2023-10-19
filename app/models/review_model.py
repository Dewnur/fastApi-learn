from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseUUIDModel

if TYPE_CHECKING:
    from app.models.product_model import Product


class Review(BaseUUIDModel):
    __tablename__ = "review"

    product_id: Mapped[UUID] = mapped_column(ForeignKey('product.id'))
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    rating: Mapped[int] = mapped_column(nullable=True)
    comment: Mapped[str] = mapped_column(nullable=False)

    product: Mapped['Product'] = relationship(back_populates='reviews')
