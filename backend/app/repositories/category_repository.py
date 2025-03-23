from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Category
from app.domain.schemas import CategoryCreate


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_category_by_name(self, name: str):
        query = select(Category).where(Category.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all_categories(self):
        query = select(Category.name)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create_category(self, category: CategoryCreate):
        new_category = Category(**category.model_dump())
        self.session.add(category)
        try:
            await self.session.commit()
            await self.session.refresh(new_category)
            return new_category
        except IntegrityError:
            await self.session.rollback()
            raise ValueError(f"Ошибка при создании категории")