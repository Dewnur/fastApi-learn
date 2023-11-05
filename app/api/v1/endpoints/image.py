from fastapi import UploadFile, APIRouter, status
from starlette.responses import FileResponse

from app import crud
from app.schemas.image_schema import IImageRead

router = APIRouter()


@router.post('', status_code=status.HTTP_201_CREATED)
async def post_image(
        file: UploadFile
) -> IImageRead:
    return await crud.image.create(file=file)


@router.get("/{file_name}")
async def get_image(file_name: str):
    # Создаем путь к файлу на основе хеша
    image = await crud.image.fetch_one(name=file_name)
    file_path = image.path
    # # Проверяем существование файла
    # if not os.path.isfile(file_path):
    #     return {"error": "File not found"}

    # Отправляем файл в ответе
    return FileResponse(file_path, headers={f"Content-Type": "image/jpeg"})
