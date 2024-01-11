from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models import Order, Product, OrderItem
from app.schemas.order_items_schema import IOrderItemCreate
from app.schemas.order_schema import IOrderRead
from app.utils.exceptions.common_exception import IdNotFoundException
from app.utils.exceptions.order_items_excemption import EmptyOrderItemsException


async def create_order(
        profile_id: UUID,
        order_items: list[IOrderItemCreate],
        db_session: AsyncSession
) -> IOrderRead:
    """
    Создает новый заказ в базе данных.

    Args:
        profile_id (UUID): Идентификатор профиля пользователя, оформляющего заказ.
        order_items (list[IOrderItemCreate]): Список товаров и количества для заказа.
        db_session (AsyncSession): Асинхронная сессия базы данных для выполнения транзакции.

    Returns:
        IOrderRead: Объект заказа после успешного создания.

    Raises:
        EmptyOrderItemsException: Если список order_items пустой.
        IdNotFoundException: Если товар с указанным идентификатором не найден.
        HTTPException: Если произошла ошибка базы данных во время транзакции.

    Note:
        Функция создает новый заказ, добавляет товары в заказ, вычитает соответствующее количество товаров из
        остатков на складе и сохраняет изменения в базе данных в рамках асинхронной транзакции.
    """
    if not order_items:
        raise EmptyOrderItemsException()
    async with db_session.begin():
        try:
            new_order = Order(profile_id=profile_id)
            db_session.add(new_order)
            await db_session.flush()

            for item in order_items:
                product = await crud.product.fetch_one(id=item.product_id, db_session=db_session)
                if not product:
                    raise IdNotFoundException(model=Product, id=item.product_id)
                await product.decrease_stock_quantity(item.quantity)

                new_item = OrderItem(
                    product_id=product.id,
                    order_id=new_order.id,
                    quantity=item.quantity,
                    unit_price=product.price,
                )
                new_order.total_amount += product.price * item.quantity
                db_session.add(new_item)
                db_session.add(product)

            db_session.add(new_order)

            await db_session.commit()
            return new_order
        except SQLAlchemyError as e:
            await db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
        finally:
            await db_session.close()
