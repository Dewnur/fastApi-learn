from fastapi import Depends

from app.api.deps import get_current_user
from app.schemas.role_schema import IRoleEnum

DEPEND_A_M = Depends(get_current_user([IRoleEnum.admin, IRoleEnum.manager]))
DEPEND_A = Depends(get_current_user([IRoleEnum.admin]))
DEPEND_U = Depends(get_current_user([IRoleEnum.user]))