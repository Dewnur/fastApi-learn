from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_base import CRUDBase
from app.models import Product, Image
from app.services.image_service import create_image


class CRUDProduct(CRUDBase[Product]):
    async def update_image(
            self,
            *,
            file: UploadFile,
            product: Product,
            db_session: AsyncSession | None = None,
    ) -> Product:
        db_session = db_session or self.get_db().session
        image: Image = await create_image(file=file, db_session=db_session)
        product.image = image
        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product)
        return product


product = CRUDProduct(Product)
