from app.domain.models import User
from app.repositories import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, user: User):
        exist_user = await self.user_repository.get_user_by_username(user.username)
        if exist_user:
            raise ValueError("Пользователь с таким username уже существует")

        exist_tg = await self.user_repository.get_user_by_tg(user.id)
        if exist_tg:
            raise ValueError("Пользователь с таким telegram уже существует")

        try:
            return await self.user_repository.create_user(user)
        except ValueError as e:
            raise ValueError(f"Ошибка при регистрации: {str(e)}")

