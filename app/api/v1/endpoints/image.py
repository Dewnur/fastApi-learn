from fastapi import UploadFile, APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from app import crud
from app.api.deps import get_db_session
from app.dependencies.image_deps import image_type_existing
from app.schemas.image_schema import IImageRead
from app.services.image_service import get_file_path_dir, create_image

router = APIRouter()


@router.post('/uploads', status_code=status.HTTP_201_CREATED)
async def post_image(
        file: UploadFile = Depends(image_type_existing),
        db_session: AsyncSession = Depends(get_db_session)
) -> IImageRead:
    return await create_image(file=file, db_session=db_session)


@router.get("/{file_name}")
async def get_image(file_name: str):
    image = await crud.image.fetch_one(name=file_name)
    file_path = get_file_path_dir(
        upload_dir="app/static/images/",
        file_name=file_name,
    )
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Image {file_name} not found')
    return FileResponse(file_path, headers={f"Content-Type": f"image/{image.format}"})
