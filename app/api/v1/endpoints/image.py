from fastapi import UploadFile, APIRouter, status, HTTPException, Depends
from starlette.responses import FileResponse

from app import crud
from app.dependencies.image_deps import image_type_existing
from app.schemas.image_schema import IImageRead

router = APIRouter()


@router.post('', status_code=status.HTTP_201_CREATED)
async def post_image(
        file: UploadFile = Depends(image_type_existing)
) -> IImageRead:
    return await crud.image.create(file=file)


@router.get("/{file_name}")
async def get_image(file_name: str):
    image = await crud.image.fetch_one(name=file_name)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Image {file_name} not found')
    return FileResponse(image.path, headers={f"Content-Type": f"image/{image.format}"})
