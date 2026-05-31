from sqlalchemy import select
from sqlalchemy.orm import selectinload

from bot.database.models import City, University
from bot.database.session import AsyncSessionLocal


async def get_active_cities():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(City)
            .where(City.is_active == True)
            .order_by(City.name_en)
        )
        return result.scalars().all()


async def get_city_by_id(city_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(City)
            .where(City.id == city_id)
            .where(City.is_active == True)
        )
        return result.scalar_one_or_none()


async def get_city_with_universities(city_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(City)
            .options(selectinload(City.universities))
            .where(City.id == city_id)
            .where(City.is_active == True)
        )
        return result.scalar_one_or_none()


async def get_active_universities_by_city(city_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(University)
            .where(University.city_id == city_id)
            .where(University.is_active == True)
            .order_by(University.name_en)
        )
        return result.scalars().all()


async def get_university_by_id(university_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(University)
            .where(University.id == university_id)
            .where(University.is_active == True)
        )
        return result.scalar_one_or_none()
