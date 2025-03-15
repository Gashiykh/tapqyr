from app.domain.schemas import (
    UserCreate,
    UserLogin
)
from app.security import (
    hash_password,
    create_access_token,
    create_refresh_token,
    verify_password
)
from app.repositories import UserRepository
from app.security.jwt_handler import (
    verify_refresh_token,
    delete_refresh_token
)


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, user_data: UserCreate):
        exist_user = await self.user_repository.get_user_by_username(user_data.username)
        if exist_user:
            raise ValueError("Пользователь с таким username уже существует")

        exist_tg = await self.user_repository.get_user_by_tg(user_data.tg_username)
        if exist_tg:
            raise ValueError("Пользователь с таким telegram уже существует")

        hashed_pass = hash_password(user_data.password)
        user = user_data.model_copy(update={"password": hashed_pass})

        try:
            new_user = await self.user_repository.create_user(user)
        except Exception as e:
            raise ValueError(f"Ошибка при регистрации: {str(e)}")

        access_token = create_access_token(
            user_id=new_user.id,
            role=new_user.role,
        )
        refresh_token = await create_refresh_token(
            user_id=new_user.id,
        )

        return access_token, refresh_token

    async def login(self, user_data: UserLogin):
        user = await self.user_repository.get_user_by_username(user_data.username)

        if not user:
            raise ValueError("Неверный логин или пароль")

        if not verify_password(user_data.password, user.password):
            raise ValueError("Неверный логин или пароль")

        access_token = create_access_token(
            user_id=user.id,
            role=user.role,
        )
        refresh_token = await create_refresh_token(
            user_id=user.id,
        )

        return access_token, refresh_token

    async def verify_refresh_token(self, refresh_token: str):
        user_id = await verify_refresh_token(refresh_token)
        return user_id

    async def refresh_tokens(self, old_refresh_token: str):
        user_id = await verify_refresh_token(old_refresh_token)
        if not user_id:
            raise ValueError("Невалидный токен")

        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")

        await delete_refresh_token(user_id)

        access_token = create_access_token(
            user_id=user_id,
            role=user.role,
        )

        refresh_token = await create_refresh_token(user_id)

        return access_token, refresh_token

    async def logout(self, refresh_token: str):
        user_id = await verify_refresh_token(refresh_token)
        if not user_id:
            raise ValueError("Невалидный или просроченный refresh-токен")
        await delete_refresh_token(user_id)
        return True