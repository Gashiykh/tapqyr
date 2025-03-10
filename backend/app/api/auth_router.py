from fastapi import (
    Depends,
    APIRouter,
    HTTPException,
    status,
    Response
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_helper
from app.repositories import UserRepository
from app.services import AuthService
from app.domain.schemas import (
    UserCreate,
    UserLogin
)

router = APIRouter()

@router.post("/register")
async def register(
        user_data: UserCreate,
        response: Response,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    user_repo = UserRepository(session)
    auth_service = AuthService(user_repo)

    try:
        access_token, refresh_token = await auth_service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=False, # для localhost False; в продакшене True (HTTPS)
        samesite="strict"
    )

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False, # TODO поменять на True
        samesite="strict"
    )

    return {"detail": "Пользователь успешно зарегистрирован."}

@router.post("/login")
async def login(
        user_login: UserLogin,
        response: Response,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    user_repo = UserRepository(session)
    auth_service = AuthService(user_repo)

    try:
        access_token, refresh_token = await auth_service.login(user_login)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=False,  # для localhost False; в продакшене True (HTTPS)
        samesite="strict"
    )

    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=False,  # TODO поменять на True
        samesite="strict"
    )

    return {"detail": "Пользователь успешно авторизован."}