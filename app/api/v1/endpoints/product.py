from fastapi import Depends, UploadFile, APIRouter, status

from app import crud
from app.api.deps import get_current_user, model_id_existing
from app.dependencies.image_deps import image_type_existing
from app.models import Product
from app.schemas.product_schema import IProductCreate, IProductRead, IProductUpdate
from app.schemas.role_schema import IRoleEnum
from app.utils.exceptions.common_exception import NameExistException

router = APIRouter()


@router.get(
    path='/{obj_id}',
    status_code=status.HTTP_200_OK,
)
async def get_product_by_id(
        product_by_id: IProductRead = Depends(model_id_existing(Product))
):
    return product_by_id


@router.get(
    path='',
    status_code=status.HTTP_200_OK,
)
async def get_product_list() -> list[IProductRead]:
    return await crud.product.fetch_all()


# TODO: Проверка на существующий товар
@router.post(
    path='',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user([IRoleEnum.admin, IRoleEnum.manager]))],
)
async def post_product(
        product: IProductCreate
):
    product_exist = crud.product.fetch_one(name=product.name)
    if not product_exist:
        raise NameExistException(model=Product, name=product.name)
    return await crud.product.create(obj=product)


@router.post(
    path='/uploads/{obj_id}/image',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user([IRoleEnum.admin, IRoleEnum.manager]))],
)
async def upload_product_image(
        file: UploadFile = Depends(image_type_existing),
        product_by_id: Product = Depends(model_id_existing(Product))
) -> IProductRead:
    return await crud.product.update_image(file=file, product=product_by_id)


@router.put(
    path='/{obj_id}',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user([IRoleEnum.admin, IRoleEnum.manager]))],
)
async def update_product(
        product: IProductUpdate,
        product_by_id: IProductRead = Depends(model_id_existing(Product))
) -> IProductRead:
    return await crud.product.update(obj_current=product_by_id, obj_new=product)


@router.delete(
    path='/{obj_id}',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user([IRoleEnum.admin, IRoleEnum.manager]))],
)
async def delete_product(
        product_by_id: IProductRead = Depends(model_id_existing(Product))
) -> None:
    await crud.product.delete(id=product_by_id.id)
