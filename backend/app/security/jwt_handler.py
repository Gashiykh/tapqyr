from datetime import datetime, timedelta
import jwt

from app.core import settings
from app.core.redis import redis_client
from app.domain.enums import RoleEnum


def create_access_token(user_id: int, role: RoleEnum):
    to_encode = {
        "sub": user_id,
        "role": role.value,
    }
    expire = datetime.utcnow() + timedelta(
        minutes=settings.jwt.access_token_expire_minutes
    )
    to_encode["exp"] = expire
    return jwt.encode(
        to_encode,
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm
    )


async def create_refresh_token(user_id: int):
    to_encode = {
        "sub": str(user_id),
    }
    expire = datetime.utcnow() + timedelta(
        days=settings.jwt.refresh_token_expire_days
    )
    to_encode["exp"] = expire

    refresh_token = jwt.encode(
        to_encode,
        settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm
    )

    redis = await redis_client.get_redis()
    ttl_seconds = settings.jwt.refresh_token_expire_days * 86400
    await redis.setex(f"refresh_token:{user_id}", ttl_seconds, refresh_token)

    return refresh_token

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


async def verify_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.jwt.secret_key,
            algorithms=[settings.jwt.algorithm]
        )
        user_id: str = payload('sub')

        redis = await redis_client.get_redis()
        stored_token = await redis.get(f"refresh_token:{user_id}")

        if stored_token is None or stored_token != payload.get('refresh_token'):
            return None

        return user_id
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


async def delete_refresh_token(user_id: int):
    redis = await redis_client.get_redis()
    await redis.delete(f"refresh_token:{user_id}")


