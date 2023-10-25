from fastapi import APIRouter, Depends
from fastapi_pagination import Params

router = APIRouter()


@router.get('')
async def create_products(
        params: Params = Depends(),
):
    pass
