import datetime
import hashlib
import os
import pathlib
import shutil

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models import Image


def directory_context_manager_async(func):
    async def wrapped(*args, **kwargs):
        # Сохраняем исходную текущую рабочую директорию
        original_cwd = os.getcwd()
        script_dir = pathlib.Path(__file__).parent.resolve()
        # Изменяем рабочую директорию, например, на директорию скрипта
        os.chdir(script_dir)
        result = await func(*args, **kwargs)
        # Возвращаемся обратно к исходной рабочей директории
        os.chdir(original_cwd)
        return result

    return wrapped


def directory_context_manager(func):
    def wrapped(*args, **kwargs):
        original_cwd = os.getcwd()
        script_dir = pathlib.Path(__file__).parent.resolve()
        os.chdir(script_dir)
        result = func(*args, **kwargs)
        os.chdir(original_cwd)
        return result

    return wrapped


@directory_context_manager_async
async def create_image(
        file: UploadFile,
        db_session: AsyncSession | None = None,
) -> Image:
    file_format = file.filename.split(".")[-1]

    image_name = get_hash_str(file.filename)[:7]

    file_path = get_file_path_dir(
        upload_dir=get_settings().FILE_SAVE_DIR,
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


@directory_context_manager
def get_file_path_dir(upload_dir: str, file_name: str, makedir=False, depth=2) -> str:
    abs_dir = os.path.abspath(upload_dir)
    subdirectory = os.path.join(*[file_name[i:i + depth] for i in range(0, depth, depth)])
    file_path = os.path.normpath(os.path.join(abs_dir, subdirectory, file_name))
    if makedir:
        os.makedirs(os.path.join(abs_dir, subdirectory), exist_ok=True)
    return file_path


def get_hash_str(string: str) -> str:
    hasher = hashlib.sha256()
    name = str(datetime.datetime.utcnow()) + string
    hasher.update(name.encode("utf-8"))
    string_hash = hasher.hexdigest()
    return string_hash
