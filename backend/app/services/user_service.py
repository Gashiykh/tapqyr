from app.domain.schemas import UserCreate
from app.repositories import UserRepository
from app.security import hash_password, create_access_token, create_refresh_token


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
