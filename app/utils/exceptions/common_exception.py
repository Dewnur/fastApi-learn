from typing import Type, Any, Generic, TypeVar
from uuid import UUID

from fastapi import HTTPException
from starlette import status

from app.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class ContentNoChangeException(HTTPException):
    def __init__(
            self,
            detail: Any = None,
            headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers
        )


class IdNotFoundException(HTTPException, Generic[ModelType]):
    def __init__(
            self,
            model: Type[ModelType],
            id: UUID | str | None = None,
            headers: dict[str, Any] | None = None,
    ) -> None:
        if id:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find the {model.__tablename__} with id {id}.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__tablename__} id not found.",
            headers=headers,
        )


class NameNotFoundException(HTTPException, Generic[ModelType]):
    def __init__(
            self,
            model: Type[ModelType],
            name: str | None = None,
            headers: dict[str, Any] | None = None,
    ) -> None:
        if name:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unable to find the {model.__tablename__} named {name}.",
                headers=headers,
            )
        else:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{model.__tablename__} name not found.",
                headers=headers,
            )


class NameExistException(HTTPException, Generic[ModelType]):
    def __init__(
            self,
            model: Type[ModelType],
            name: str | None = None,
            headers: dict[str, Any] | None = None,
    ) -> None:
        if name:
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The {model.__tablename__} name {name} already exists.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The {model.__tablename__} name already exists.",
            headers=headers,
        )
