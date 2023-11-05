import datetime
import hashlib
import os
import shutil

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_base import CRUDBase
from app.models import Image


class CRUDImage(CRUDBase[Image]):
    async def create(
            self,
            *,
            file: UploadFile,
            db_session: AsyncSession | None = None,
    ) -> Image:
        db_session = db_session or self.get_db().session

        file_format = file.filename.split(".")[-1]

        hasher = hashlib.sha256()
        file_name = str(datetime.datetime.utcnow()) + file.filename
        hasher.update(file_name.encode("utf-8"))
        file_hash = hasher.hexdigest()

        depth = 2
        subdirectory = os.path.join(*[file_hash[i:i + depth] for i in range(0, depth, depth)])
        upload_dir = "app/static/images/"
        file_path = os.path.normpath(os.path.join(upload_dir, subdirectory, file_hash))

        os.makedirs(os.path.join(upload_dir, subdirectory), exist_ok=True)

        with open(file_path, "wb") as dest_file:
            shutil.copyfileobj(file.file, dest_file)

        image = Image(path=file_path, format=file_format, name=file_hash[:11])

        db_session.add(image)
        await db_session.commit()
        await db_session.refresh(image)
        return image


image = CRUDImage(Image)
