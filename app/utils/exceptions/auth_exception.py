from fastapi import HTTPException, status


class MissingTokenException(HTTPException):
    def __init__(self, detail: str = "Access token is missing"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class TokenExpiredException(HTTPException):
    def __init__(self, detail: str = "Token has expired"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class InvalidTokenException(HTTPException):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class UserNotFoundException(HTTPException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InvalidRoleException(HTTPException):
    def __init__(self, detail: str = "User role is not valid for this operation"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
