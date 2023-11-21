import datetime
import hashlib
import os
import shutil

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models import Image


async def create_image(
        file: UploadFile,
        db_session: AsyncSession | None = None,
) -> Image:
    upload_dir = "app/static/images/"

    file_format = file.filename.split(".")[-1]

    image_name = get_hash_str(file.filename)[:7]

    file_path = get_file_path_dir(
        upload_dir=upload_dir,
        file_name=image_name,
        makedir=True,
    )

    with open(file_path, "wb") as dest_file:
        shutil.copyfileobj(file.file, dest_file)

    new_image = Image(
        path=f'{get_settings().API_V1_STR}/images/{image_name}',
        format=file_format,
        name=image_name
    )
    db_session.add(new_image)

    await db_session.commit()
    return new_image


def get_file_path_dir(upload_dir: str, file_name: str, makedir=False, depth=2) -> str:
    subdirectory = os.path.join(*[file_name[i:i + depth] for i in range(0, depth, depth)])
    file_path = os.path.normpath(os.path.join(upload_dir, subdirectory, file_name))
    if makedir:
        os.makedirs(os.path.join(upload_dir, subdirectory), exist_ok=True)
    return file_path


def get_hash_str(string: str) -> str:
    hasher = hashlib.sha256()
    name = str(datetime.datetime.utcnow()) + string
    hasher.update(name.encode("utf-8"))
    string_hash = hasher.hexdigest()
    return string_hash
