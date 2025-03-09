from datetime import datetime, timedelta
import jwt

from app.core import settings


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.jwt.access_token_expire_minutes
    )
    to_encode.update({'exp': expire})
    return jwt.encode(
        to_encode,
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm
    )


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.jwt.refresh_token_expire_minutes
    )
    to_encode.update({'exp': expire})
    return jwt.encode(
        to_encode,
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm
    )


def decode_token(token: str):
    payload = jwt.decode(
        token,
        settings.jwt.secret_key,
        algorithms=[settings.jwt.algorithm]
    )
    user_id = payload('sub')
    username: str = payload.get('username')
    role: str = payload.get('role')
    return user_id, username, role