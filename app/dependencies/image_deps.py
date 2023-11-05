from fastapi import UploadFile, HTTPException, status


async def image_type_existing(file: UploadFile) -> UploadFile:
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='File is not an image')
    return file