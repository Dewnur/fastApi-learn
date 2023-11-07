from fastapi import APIRouter, status, Depends, HTTPException

from app import crud
from app.api.deps import get_current_user
from app.models import User, Profile
from app.schemas import IOrderStatus
from app.schemas.order_items_schema import IOrderItemCreate
from app.schemas.order_schema import IOrderRead, IOrderCreate
from app.schemas.role_schema import IRoleEnum

router = APIRouter()

