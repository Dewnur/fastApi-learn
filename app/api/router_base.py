from enum import Enum
from typing import TypeVar, Generic, Sequence

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.api.deps import model_id_existing
from app.crud.crud_base import CRUDBase
from app.models import Base

SchemaCreateType = TypeVar("SchemaCreateType", bound=BaseModel)
SchemaReadType = TypeVar("SchemaReadType", bound=BaseModel)
SchemaUpdateType = TypeVar("SchemaUpdateType", bound=BaseModel)
ModelType = TypeVar("ModelType", bound=Base)


class BaseAPIMethods(str, Enum):
    get = 'get'
    get_list = 'get_list'
    post = 'post'
    put = 'put'
    delete = 'delete'


class BaseAPIRouter(
    APIRouter,
    Generic[
        ModelType,
        SchemaCreateType,
        SchemaReadType,
        SchemaUpdateType
    ]
):
    def __init__(
            self,
            model: type[ModelType],
            schema_create_type: type[SchemaCreateType],
            schema_read_type: type[SchemaReadType],
            schema_update_type: type[SchemaUpdateType],
            depends_mapping: dict[str | BaseAPIMethods, Sequence[Depends]] = None,
    ):
        super().__init__()
        self.schema_read_type = schema_read_type
        self.schema_create_type = schema_create_type
        self.schema_update_type = schema_update_type
        self.model = model
        self.depends_mapping = depends_mapping or {}

        self.add_api_route(
            path='/{obj_id}',
            methods=['GET'],
            endpoint=self._get(),
            dependencies=self.depends_mapping.get(BaseAPIMethods.get, None),
            status_code=status.HTTP_200_OK,
            name=f'Get {model.__name__} By Id',
        )

        self.add_api_route(
            path='',
            methods=['GET'],
            endpoint=self._get_list(),
            dependencies=self.depends_mapping.get(BaseAPIMethods.get_list, None),
            status_code=status.HTTP_200_OK,
            name=f'Get {model.__name__} List',
        )

        self.add_api_route(
            path='',
            methods=['POST'],
            endpoint=self._post_object(),
            dependencies=self.depends_mapping.get(BaseAPIMethods.post, None),
            status_code=status.HTTP_201_CREATED,
            name=f'Create {model.__name__}',
        )

        self.add_api_route(
            path='/{obj_id}',
            methods=['PUT'],
            endpoint=self._put_object(),
            dependencies=self.depends_mapping.get(BaseAPIMethods.put, None),
            status_code=status.HTTP_200_OK,
            name=f'Update {model.__name__}',
        )

        self.add_api_route(
            path='/{obj_id}',
            methods=['DELETE'],
            endpoint=self._delete_object(),
            dependencies=self.depends_mapping.get(BaseAPIMethods.delete, None),
            status_code=status.HTTP_200_OK,
            name=f'Delete {model.__name__}',
        )

    def _get(self):
        schema_read_type = self.schema_read_type
        model = self.model

        async def get_object_by_id(
                object_by_id: schema_read_type = Depends(model_id_existing(model)),
        ) -> schema_read_type:
            return object_by_id

        return get_object_by_id

    def _get_list(self):
        schema_read_type = self.schema_read_type
        model = self.model

        async def get_object_list(
        ) -> list[schema_read_type]:
            model_crud = CRUDBase(model)
            object_list = await model_crud.fetch_all()
            return object_list

        return get_object_list

    def _post_object(self):
        schema_create_type = self.schema_create_type
        model = self.model

        async def post_object(
                obj: schema_create_type
        ) -> None:
            model_crud = CRUDBase(model)
            return await model_crud.create(obj=obj)

        return post_object

    def _put_object(self):
        schema_update_type = self.schema_update_type
        schema_read_type = self.schema_read_type
        model = self.model

        async def update_object(
                obj: schema_update_type,
                object_by_id: schema_read_type = Depends(model_id_existing(model))
        ) -> None:
            model_crud = CRUDBase(model)
            await model_crud.update(obj_current=object_by_id, obj_new=obj)

        return update_object

    def _delete_object(self):
        schema_read_type = self.schema_read_type
        model = self.model

        async def delete_object(
                object_by_id: schema_read_type = Depends(model_id_existing(model))
        ) -> schema_read_type:
            model_crud = CRUDBase(model)
            await model_crud.delete(id=object_by_id.id)

        return delete_object
