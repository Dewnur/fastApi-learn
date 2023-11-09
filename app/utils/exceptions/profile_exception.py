from fastapi import HTTPException, status


class MissingPhoneNumberException(HTTPException):
    def __init__(self, detail: str = "No phone number provided for the profile"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class MissingAddressException(HTTPException):
    def __init__(self, detail: str = "Address not specified for the profile"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)
