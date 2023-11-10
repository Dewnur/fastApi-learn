from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseUUIDModel

if TYPE_CHECKING:
    from app.models.category_model import Category
    from app.models.image_model import Image
    from app.models.order_item_model import OrderItem


class Product(BaseUUIDModel):
    __tablename__ = "product"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    stock_quantity: Mapped[int] = mapped_column(nullable=False)
    category_id: Mapped[UUID] = mapped_column(ForeignKey('category.id'))
    image_id: Mapped[UUID] = mapped_column(ForeignKey('image.id'), nullable=True)

    category: Mapped['Category'] = relationship(back_populates='products', lazy='selectin')
    image: Mapped['Image'] = relationship(back_populates='product', lazy='selectin')
    order_items: Mapped[list['OrderItem']] = relationship(back_populates='product')

    def is_available_for(self, quantity: int) -> bool:
        return self.stock_quantity > 0 and self.stock_quantity >= quantity
