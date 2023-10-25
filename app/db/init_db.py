from sqlalchemy.ext.asyncio.session import AsyncSession

from app import crud
from app.schemas.role_schema import IRoleCreate
from app.schemas.user_schema import IUserAccess

roles: list[IRoleCreate] = [
    IRoleCreate(name="admin"),
    IRoleCreate(name="manager"),
    IRoleCreate(name="user"),
]

users: list[dict[str, str | IUserAccess]] = [
    {
        "data": IUserAccess(
            username="Admin",
            password='root',
            email="admin@example.com",
            is_superuser=True,
        ),
        "role": "admin",
    },
    {
        "data": IUserAccess(
            username="Manager",
            password='root',
            email="manager@example.com",
            is_superuser=False,
        ),
        "role": "manager",
    },
    {
        "data": IUserAccess(
            username="User",
            password='root',
            email="user@example.com",
            is_superuser=False,
        ),
        "role": "user",
    },
]


async def init_db(async_session: AsyncSession):
    for role in roles:
        role_current = await crud.role.get_role_by_name(
            name=role.name, db_session=async_session
        )
        if not role_current:
            await crud.role.create(obj=role, db_session=async_session)

    for user in users:
        current_user = await crud.user.get_by_email(
            email=user["data"].email, db_session=async_session
        )
        role = await crud.role.get_role_by_name(
            name=user["role"], db_session=async_session
        )
        if not current_user:
            user["data"].role_id = role.id
            await crud.user.create(obj=user["data"], db_session=async_session)
