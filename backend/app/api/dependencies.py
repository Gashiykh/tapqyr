import jwt
from fastapi import (
    Depends,
    Response,
    Cookie,
    HTTPException,
    status
)
from jwt import decode
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Optional

from app.core import db_helper, settings
from app.repositories import UserRepository
from app.security import decode_token
from app.services import AuthService


def get_auth_service(
        session: AsyncSession = Depends(db_helper.session_getter)
):
    user_repo = UserRepository(session)
    return AuthService(user_repo)


def set_tokens_in_cookies(
        response: Response,
        access_token: str,
        refresh_token: str
):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="strict",
        secure=False  # На продакшене: True (HTTPS)
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="strict",
        secure=False
    )


def delete_tokens_from_cookies(
        response: Response,
):
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        max_age=0,
        samesite="strict",
        secure=False  # На продакшене: True (HTTPS)
    )
    response.set_cookie(
        key="refresh_token",
        value="",
        httponly=True,
        max_age=0,
        samesite="strict",
        secure=False
    )


async def get_current_user(
        access_token: Optional[str] = Cookie(None),
        session: AsyncSession = Depends(db_helper.session_getter)
):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован"
        )
    try:
        user_id, role = decode_token(access_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен просрочен")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Невалидный токен")

    user_repo = UserRepository(session)
    user = await user_repo.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    return user
