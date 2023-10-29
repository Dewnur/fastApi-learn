from typing import TypeVar, Sequence

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.api.deps import model_id_existing
from app.crud.crud_base import CRUDBase
from app.models import Base

SchemaCreateType = TypeVar("SchemaCreateType", bound=BaseModel)
SchemaReadType = TypeVar("SchemaReadType", bound=BaseModel)
SchemaUpdateType = TypeVar("SchemaUpdateType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=Base)


class RouteDepends:
    def __init__(
            self,
            *,
            get_route: Sequence[Depends] | None = None,
            get_list_route: Sequence[Depends] | None = None,
            post_route: Sequence[Depends] | None = None,
            update_route: Sequence[Depends] | None = None,
            delete_route: Sequence[Depends] | None = None,
    ) -> None:
        self.get_route = get_route
        self.get_list_route = get_list_route
        self.post_route = post_route
        self.update_route = update_route
        self.delete_route = delete_route


class BaseAPIRouter(APIRouter):
    def __init__(
            self,
            *,
            model: type[ModelType],
            model_schema_read: type[SchemaReadType],
            model_schema_create: type[SchemaCreateType],
            model_schema_update: type[SchemaUpdateType],
            route_depends: RouteDepends,
    ):
        super().__init__()

        @self.get(
            path='/{obj_id}',
            dependencies=route_depends.get_route,
            status_code=status.HTTP_200_OK,
            name=f'Get {model.__name__} By Id',

        )
        async def get_object_by_id(
                object_by_id: model_schema_read = Depends(model_id_existing(model))
        ) -> model_schema_read:
            return object_by_id

        @self.get(
            path='',
            dependencies=route_depends.get_list_route,
            status_code=status.HTTP_200_OK,
            name=f'Get {model.__name__} List',
        )
        async def get_object_list(
        ) -> list[model_schema_read]:
            model_crud = CRUDBase(model)
            object_list: model_schema_read = await model_crud.fetch_all()
            return object_list

        @self.post(
            path='',
            dependencies=route_depends.post_route,
            status_code=status.HTTP_201_CREATED,
            name=f'Create {model.__name__}',
        )
        async def get_object_by_id(
                obj: model_schema_create
        ) -> None:
            model_crud = CRUDBase(model)
            return await model_crud.create(obj=obj)

        @self.put(
            '/{obj_id}',
            dependencies=route_depends.update_route,
            status_code=status.HTTP_200_OK,
            name=f'Update {model.__name__}',
        )
        async def update_object(
                obj: model_schema_update,
                object_by_id: model_schema_read = Depends(model_id_existing(model))
        ) -> None:
            model_crud = CRUDBase(model)
            await model_crud.update(obj_current=object_by_id, obj_new=obj)

        @self.delete(
            '/{obj_id}',
            dependencies=route_depends.delete_route,
            status_code=status.HTTP_200_OK,
            name=f'Delete {model.__name__}',
        )
        async def delete_object(
                object_by_id: model_schema_read = Depends(model_id_existing(model))
        ) -> model_schema_read:
            model_crud = CRUDBase(model)
            await model_crud.delete(id=object_by_id.id)
