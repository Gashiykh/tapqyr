from fastapi import Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_helper
from app.repositories import UserRepository
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