from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.crud.crud_base import CRUDBase
from app.models import Order, OrderItem, Product
from app.schemas.order_schema import IOrderCreate
from app.utils.exceptions.common_exception import IdNotFoundException


class CRUDOrder(CRUDBase[Order]):
    async def create(
            self,
            *,
            order: IOrderCreate,
            db_session: AsyncSession | None = None,
    ) -> Order:
        db_session = db_session or self.get_db().session
        try:
            new_order = Order(**order.model_dump(exclude={'order_items'}))
            db_session.add(new_order)
            await db_session.flush()

            for item in order.order_items:
                product = await crud.product.fetch_one(id=item.product_id)
                if not product:
                    raise IdNotFoundException(
                        model=Product,
                        id=item.product_id
                    )
                if product.stock_quantity <= 0 or product.stock_quantity < item.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Product is unavailable due to insufficient stock quantity"
                    )
                if item.quantity <= 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='The quantity must be greater than 0'
                    )
                product.stock_quantity = product.stock_quantity - item.quantity
                new_item = OrderItem(
                    product_id=product.id,
                    order_id=new_order.id,
                    quantity=item.quantity,
                    unit_price=product.price,
                )
                new_order.total_amount += product.price * item.quantity
                db_session.add(new_item)
                db_session.add(product)

            await db_session.commit()
            await db_session.refresh(new_order)
            return new_order
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


order = CRUDOrder(Order)
