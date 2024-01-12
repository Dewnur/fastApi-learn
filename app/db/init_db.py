import json
import os

from fastapi import UploadFile
from sqlalchemy import insert
from sqlalchemy.ext.asyncio.session import AsyncSession

from app import crud
from app.core.config import get_settings
from app.db.session import engine
from app.models import Base, Category
from app.schemas.product_schema import IProductCreate
from app.schemas.profile_schema import IProfileCreate
from app.schemas.role_schema import IRoleCreate
from app.schemas.user_schema import IUserAccess

settings = get_settings()

roles: list[IRoleCreate] = [
    IRoleCreate(name="admin"),
    IRoleCreate(name="manager"),
    IRoleCreate(name="user"),
]

users: list[dict[str, str | IUserAccess | IProfileCreate]] = [
    {
        "data": IUserAccess(
            username="Admin",
            password='root',
            email="admin@example.com",
            is_superuser=True,
        ),
        "role": "admin",
        'profile': None,
    },
    {
        "data": IUserAccess(
            username="Manager",
            password='root',
            email="manager@example.com",
            is_superuser=False,
        ),
        "role": "manager",
        'profile': None,
    },
    {
        "data": IUserAccess(
            username="User",
            password='root',
            email="user@example.com",
            is_superuser=False,
        ),
        "role": "user",
        'profile': IProfileCreate(
            first_name='Иван',
            last_name='Иванов',
            gender='male',
            address='г. Москва, ул. Ленина 13',
            phone_number='+79824097321',
        ),
    },
]


async def init_db(async_session: AsyncSession):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    for role in roles:
        await crud.role.create(obj=role, db_session=async_session)

    for user in users:
        role = await crud.role.get_role_by_name(
            name=user["role"], db_session=async_session
        )
        user["data"].role_id = role.id
        new_user = await crud.user.create(obj=user["data"], db_session=async_session)
        if user['profile']:
            profile = user['profile']
            profile.user_id = new_user.id
            await crud.profile.create(obj=profile, db_session=async_session)

    def open_mock_json(model: str):
        path = os.path.join(settings.base_dir, 'app', 'data', f'{model}') + '.json'
        with open(path, encoding="utf-8") as file:
            return json.load(file)

    categories = open_mock_json("categories")
    products = open_mock_json("products")

    for Model, values in [
        (Category, categories),
    ]:
        query = insert(Model).values(values)
        await async_session.execute(query)

    await async_session.commit()

    for item in products:
        new_product_create = IProductCreate(**item['product'])
        new_product = await crud.product.create(obj=new_product_create, db_session=async_session)
        image_path = os.path.join(settings.base_dir, 'app', 'data', 'images', item['image'])
        with open(image_path, "rb") as file:
            upload_file = UploadFile(file=file, filename=file.name)
            await crud.product.update_image(file=upload_file, product=new_product, db_session=async_session)
