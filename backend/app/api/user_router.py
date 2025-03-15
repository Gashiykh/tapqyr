from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.domain.schemas import UserRead

router = APIRouter()

@router.get("/me", response_model=UserRead)
async def get_me(
        current_user = Depends(get_current_user)
):
    return UserRead.model_validate(current_user.__dict__)