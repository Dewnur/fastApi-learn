from datetime import datetime
from typing import Callable, Any, Coroutine
from uuid import UUID

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError, ExpiredSignatureError
from app.db.session import async_session

from app import crud
from app.core.config import get_settings
from app.core.security import JWT_ALGORITHM
from app.models import User


def get_token(request: Request):
    token = request.cookies.get(get_settings().name_access_token)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


def get_current_user(required_roles: list[str] = None):
    async def current_user(
            token: str = Depends(get_token)
    ) -> User:
        try:
            payload = jwt.decode(
                token,
                key=get_settings().encrypt_key,
                algorithms=JWT_ALGORITHM,
            )
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        user_id: str = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        user = await crud.user.fetch_one(db_session=async_session, id=UUID(user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        if required_roles:
            is_valid_role = False
            for role in required_roles:
                if role == user.role.name:
                    is_valid_role = True

            if not is_valid_role:
                raise HTTPException(
                    status_code=403,
                    detail=f"""Role "{required_roles}" is required for this action""",
                )
        return user

    return current_user
