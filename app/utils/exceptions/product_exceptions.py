from fastapi import HTTPException, status


class InsufficientStockException(HTTPException):
    def __init__(self, product_id: str, detail: str = None):
        detail = detail if detail else f"Product with ID {product_id} is unavailable due to insufficient stock quantity"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)