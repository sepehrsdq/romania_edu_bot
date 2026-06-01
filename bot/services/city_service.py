from types import SimpleNamespace

from sqlalchemy import select, text

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


async def get_extra_infos(target_type: str, target_id: int, user_is_premium: bool = False):
    async with AsyncSessionLocal() as session:
        if target_type == "city":
            table_name = "city_extra_infos"
            id_column = "city_id"
        elif target_type == "university":
            table_name = "university_extra_infos"
            id_column = "university_id"
        else:
            return []

        premium_condition = "" if user_is_premium else "AND is_premium = false"

        query = text(f"""
            SELECT id, title, content, sort_order, is_active, is_premium
            FROM {table_name}
            WHERE {id_column} = :target_id
              AND is_active = true
              {premium_condition}
            ORDER BY sort_order ASC, id ASC
        """)

        result = await session.execute(
            query,
            {"target_id": target_id}
        )

        rows = result.mappings().all()

        return [
            SimpleNamespace(
                id=row["id"],
                title=row["title"],
                content=row["content"],
                sort_order=row["sort_order"],
                is_active=row["is_active"],
                is_premium=row["is_premium"],
            )
            for row in rows
        ]
