from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.crud.crud_base import CRUDBase
from app.models import Product, Image


class CRUDProduct(CRUDBase[Product]):
    async def update_image(
            self,
            *,
            file: UploadFile,
            product: Product,
            db_session: AsyncSession | None = None,
    ) -> Product:
        db_session = db_session or self.get_db().session
        image: Image = await crud.image.create(file=file)
        product.image = image
        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product)
        return product


product = CRUDProduct(Product)
