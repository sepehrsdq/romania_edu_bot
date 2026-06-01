from aiogram.types import User as TelegramAiogramUser
from sqlalchemy import select

from bot.config import ADMIN_IDS
from bot.database.models import TelegramUser
from bot.database.session import AsyncSessionLocal


async def register_or_update_user(telegram_user: TelegramAiogramUser):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser).where(
                TelegramUser.telegram_id == telegram_user.id
            )
        )

        user = result.scalar_one_or_none()
        is_admin = telegram_user.id in ADMIN_IDS

        if user is None:
            user = TelegramUser(
                telegram_id=telegram_user.id,
                full_name=telegram_user.full_name,
                username=telegram_user.username,
                language_code=telegram_user.language_code,
                is_admin=is_admin,
            )
            session.add(user)
        else:
            user.full_name = telegram_user.full_name
            user.username = telegram_user.username
            user.language_code = telegram_user.language_code
            user.is_admin = is_admin

        await session.commit()
        await session.refresh(user)

        return user


async def get_user_by_telegram_id(telegram_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser).where(
                TelegramUser.telegram_id == telegram_id
            )
        )
        return result.scalar_one_or_none()


async def update_user_phone(telegram_id: int, phone_number: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser).where(
                TelegramUser.telegram_id == telegram_id
            )
        )

        user = result.scalar_one_or_none()

        if user is None:
            return None

        user.phone_number = phone_number
        user.contact_shared = True

        await session.commit()
        await session.refresh(user)

        return user


async def get_all_active_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser)
            .where(TelegramUser.is_blocked == False)
            .order_by(TelegramUser.id)
        )
        return result.scalars().all()
