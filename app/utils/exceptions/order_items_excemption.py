from fastapi import HTTPException
from starlette import status


class EmptyOrderItemsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Order items list is empty')
