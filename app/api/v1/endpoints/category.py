from fastapi import APIRouter, Depends
from starlette import status

from app import crud
from app.api.deps import model_id_existing, get_current_user
from app.models import Category
from app.schemas.category_schema import ICategoryRead, ICategoryCreate, ICategoryUpdate
from app.schemas.role_schema import IRoleEnum
from app.utils.exceptions.common_exception import NameExistException

router = APIRouter()


@router.get(
    path='/{obj_id}',
    status_code=status.HTTP_200_OK,
)
async def get_category_by_id(
        category_by_id: ICategoryRead = Depends(model_id_existing(Category))
) -> ICategoryRead:
    return category_by_id


@router.get(
    path='',
    status_code=status.HTTP_200_OK,
)
async def get_category_list() -> list[ICategoryRead]:
    return await crud.category.fetch_all()


@router.post(
    path='',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user([IRoleEnum.admin, IRoleEnum.manager]))],
)
async def post_category(
        category: ICategoryCreate
) -> ICategoryRead:
    category_exist = crud.product.fetch_one(name=category.name)
    if not category_exist:
        raise NameExistException(model=Category, name=category.name)
    return await crud.category.create(obj=category)


@router.put(
    path='/{obj_id}',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user([IRoleEnum.admin, IRoleEnum.manager]))],
)
async def update_category(
        category: ICategoryUpdate,
        category_by_id: ICategoryRead = Depends(model_id_existing(Category))
) -> ICategoryRead:
    return await crud.category.update(obj_current=category_by_id, obj_new=category)


@router.delete(
    path='/{obj_id}',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user([IRoleEnum.admin, IRoleEnum.manager]))],
)
async def delete_category(
        category_by_id: ICategoryRead = Depends(model_id_existing(Category))
) -> None:
    await crud.category.delete(id=category_by_id.id)
