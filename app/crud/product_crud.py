from io import BytesIO

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_base import CRUDBase
from app.models import Product, Image
from app.services.image_service import create_image
from app.utils.image_functions import resize_image


class CRUDProduct(CRUDBase[Product]):
    async def update_image(
            self,
            *,
            file: UploadFile,
            product: Product,
            db_session: AsyncSession | None = None,
    ) -> Product:
        db_session = db_session or super().get_db().session
        data = file.file.read()
        img = BytesIO(resize_image(data, 700, 700))
        resize_upload_file = UploadFile(file=img, filename=file.filename)
        image: Image = await create_image(file=resize_upload_file, db_session=db_session)
        product.image = image
        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product)
        return product


product = CRUDProduct(Product)
