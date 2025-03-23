from sqlalchemy.ext.asyncio import AsyncSession


class LocationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_location_by_building(self):