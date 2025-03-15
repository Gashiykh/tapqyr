from typing import Optional

from fastapi import (
    Depends,
    APIRouter,
    HTTPException,
    status,
    Response,
    Cookie
)

from app.api.dependencies import get_auth_service, set_tokens_in_cookies, delete_tokens_from_cookies
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
        auth_service: AuthService = Depends(get_auth_service),
):
    try:
        access_token, refresh_token = await auth_service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    set_tokens_in_cookies(response, access_token, refresh_token)

    return {"detail": "Пользователь успешно зарегистрирован."}

@router.post("/login")
async def login(
        user_login: UserLogin,
        response: Response,
        auth_service: AuthService = Depends(get_auth_service),
):
    try:
        access_token, refresh_token = await auth_service.login(user_login)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    set_tokens_in_cookies(response, access_token, refresh_token)

    return {"detail": "Пользователь успешно авторизован."}

@router.post("/refresh")
async def refresh(
        response: Response,
        refresh_token: Optional[str] = Cookie(None),
        auth_service: AuthService = Depends(get_auth_service),
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Токен не найден"
        )

    try:
        access_token, refresh_token = await auth_service.refresh_tokens(refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    set_tokens_in_cookies(response, access_token, refresh_token)

    return {"detail": "Токены успешно обновлены"}


@router.post("/logout")
async def logout(
        response: Response,
        refresh_token: Optional[str] = Cookie(None),
        auth_service: AuthService = Depends(get_auth_service),
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже вышел из аккаунта"
        )

    try:
        await auth_service.logout(refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    delete_tokens_from_cookies(response)

    return {"detail": "Вы успешно вышли из аккаунта"}