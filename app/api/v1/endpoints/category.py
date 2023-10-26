from fastapi import APIRouter

router = APIRouter()


@router.get('/{obj_id}')
async def get_category_by_id():
    pass


@router.get('')
async def get_category_list():
    pass


@router.get('/{obj_id}/products')
async def get_category_list():
    pass


@router.put('/{obj_id}')
async def update_category():
    pass


@router.get('/{obj_id}')
async def delete_category():
    pass
