from fastapi import (
    Depends,
    APIRouter,
    HTTPException,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_helper
from app.repositories import UserRepository
from app.services import AuthService
from app.domain.schemas import (
    UserCreate,
    TokenResponse, UserLogin
)

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
async def register(
        user_data: UserCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    user_repo = UserRepository(session)
    auth_service = AuthService(user_repo)

    try:
        access_token, refresh_token = await auth_service.register_user(user_data)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(
        user_login: UserLogin,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    user_repo = UserRepository(session)
    auth_service = AuthService(user_repo)

    try:
        access_token, refresh_token = await auth_service.login(user_login)
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )